from __future__ import annotations
from datetime import datetime, timezone
import logging
"""
Interview Manager — orchestrator module.

Responsibility:
    Composes all interview modules into a single workflow.
    This is the only module the router interacts with.

    Pipeline (this prompt's scope):
    POST /api/interview → Router → InterviewManager →
        CandidateAnalyzer → InterviewPlanner → SessionManager →
        InterviewContextBuilder → return InterviewContext

    Future modules (not yet implemented):
        QuestionGenerator, FollowupGenerator, EvaluationEngine, FeedbackGenerator
"""

logger = logging.getLogger(__name__)

from models.schemas import (
    CandidateProfile,
    InterviewResponse,
    InterviewContext,
    EvaluationEvidence,
    QuestionRecord,
    Feedback,
)
from modules.candidate_loader import CandidateLoader
from modules.curriculum_loader import CurriculumLoader
from modules.candidate_analyzer import CandidateAnalyzer
from modules.interview_planner import InterviewPlanner
from modules.context_builder import InterviewContextBuilder
from modules.question_generator import QuestionGenerator
from modules.followup_generator import FollowupGenerator
from modules.evaluation_engine import EvaluationEngine
from modules.feedback_generator import FeedbackGenerator
from modules.session_manager import SessionManager
from config import MAX_QUESTIONS_PER_INTERVIEW, MAX_FOLLOWUPS_PER_TOPIC


class InterviewManager:
    """
    Top-level orchestrator for the interview workflow.

    Flow:
        start_interview() →
            1. Analyze candidate (deterministic)
            2. Build interview plan (deterministic)
            3. Create session (with analysis + plan)
            4. Build InterviewContext
            5. Generate first question (stub)

        continue_interview() →
            1. Retrieve session
            2. Record candidate's answer
            3. Evaluate the response (stub)
            4. Decide: follow-up, next topic, or end
            5. Generate next question or final feedback (stub)
    """

    def __init__(self):
        # Data loaders (shared, stateless after init)
        self.curriculum_loader = CurriculumLoader()
        self.candidate_loader = CandidateLoader()

        # Analysis & planning (deterministic, no AI)
        self.candidate_analyzer = CandidateAnalyzer(self.curriculum_loader)
        self.interview_planner = InterviewPlanner(self.curriculum_loader)

        # Context builder (stateless)
        self.context_builder = InterviewContextBuilder()

        # Natural language and answer-evaluation modules
        self.question_generator = QuestionGenerator()
        self.followup_generator = FollowupGenerator()
        self.evaluation_engine = EvaluationEngine()
        self.feedback_generator = FeedbackGenerator()

        # Session state
        self.session_manager = SessionManager()

    async def start_interview(
        self,
        session_id: str,
        candidate: CandidateProfile,
    ) -> InterviewResponse:
        """
        Initialize a new interview session.

        Steps:
        1. Analyze the candidate (deterministic)
        2. Build an interview plan (deterministic)
        3. Create session with analysis + plan attached
        4. Build InterviewContext
        5. Generate the first question (stub)
        """
        # Step 1: Deterministic analysis
        analysis = self.candidate_analyzer.analyze(candidate)

        # Step 2: Deterministic planning
        plan = self.interview_planner.create_plan(analysis)

        # Step 3: Create session with rich state
        state = self.session_manager.create_session(
            session_id=session_id,
            candidate=candidate,
            analysis=analysis,
            plan=plan,
            max_questions=MAX_QUESTIONS_PER_INTERVIEW,
        )
        state.phase = "asking"

        # Step 4: Build context
        context = self.context_builder.build(state)

        # Step 5: Generate first question and retain its evaluation rubric
        if not plan.planned_topics:
            state.phase = "complete"
            self.session_manager.update_session(session_id, state)
            return InterviewResponse(
                reply="No topics to cover based on your profile. Interview complete.",
                done=True,
            )

        first_topic = plan.planned_topics[0]
        generated_question = self.question_generator.generate(
            topic=first_topic,
            candidate=candidate,
            experience_level=analysis.experience_level.value,
            questions_already_asked=[],
        )

        # Record the question
        state.questions_asked.append(QuestionRecord(
            topic=first_topic.title,
            question=generated_question.question,
            difficulty=generated_question.estimated_difficulty,
            expected_points=generated_question.expected_points,
        ))
        state.total_questions = 1
        state.conversation_history.append({"role": "interviewer", "content": generated_question.question})
        self.session_manager.update_session(session_id, state)

        welcome = (
            f"Welcome, {candidate.member.name}. "
            f"I'll be conducting your technical interview today, "
            f"focusing on your experience with the AI curriculum. "
            f"Let's begin.\n\n{generated_question.question}"
        )

        return InterviewResponse(reply=welcome, done=False)

    async def continue_interview(
        self,
        session_id: str,
        message: str,
    ) -> InterviewResponse:
        """
        Process the candidate's response and return the next question or feedback.

        Steps:
        1. Retrieve session
        2. Record candidate's answer
        3. Build context
        4. Evaluate the response against its stored rubric
        5. Decide: follow-up, next topic, or end
        6. Generate next question or final feedback (stub)
        """
        state = self.session_manager.get_session(session_id)
        state.phase = "evaluating"

        # Record the answer
        state.conversation_history.append({"role": "candidate", "content": message})

        current_record = state.questions_asked[-1] if state.questions_asked else None
        evaluation_result = None
        
        if current_record and current_record.answer is None:
            current_record.answer = message

            context = self.context_builder.build(state)
            evaluation_result = self.evaluation_engine.evaluate_response(
                context=context,
                current_question=current_record,
                answer=message,
            )
            
            # Only store evaluation if it's not a fallback
            is_fallback = getattr(evaluation_result, '_fallback', False)
            
            if not is_fallback:
                current_record.score = evaluation_result.overall / 10
                state.evaluations.append(EvaluationEvidence(
                    question=current_record.question,
                    topic=current_record.topic,
                    candidate_answer=message,
                    expected_points=current_record.expected_points,
                    evaluation_result=evaluation_result,
                    timestamp=datetime.now(timezone.utc).isoformat(),
                ))
                state.topic_mastery = self.evaluation_engine.calculate_topic_mastery(state.evaluations)
            else:
                # Evaluation unavailable - log and continue safely
                logger.warning(f"[INTERVIEW] Evaluation unavailable for question, continuing interview")

        # Build context for decision-making
        context = self.context_builder.build(state)

        # Check if interview should end
        if state.total_questions >= state.max_questions:
            return self._end_interview(session_id, state)

        # Decide: follow-up or next topic
        # Pass evaluation_result to should_follow_up for intelligent decision
        if current_record and self.followup_generator.should_follow_up(
            current_record, evaluation_result, MAX_FOLLOWUPS_PER_TOPIC
        ):
            logger.info(f"[INTERVIEW] Generating follow-up (count: {current_record.followup_count + 1}/{MAX_FOLLOWUPS_PER_TOPIC})")
            
            generated_followup = self.followup_generator.generate(
                original_question=current_record.question,
                candidate_answer=message,
                topic_title=current_record.topic,
            )
            
            # CRITICAL FIX: Increment followup_count on the CURRENT record
            # The new question record inherits the count from its parent
            current_record.followup_count += 1
            
            state.questions_asked.append(QuestionRecord(
                topic=current_record.topic,
                question=generated_followup.question,
                difficulty=generated_followup.estimated_difficulty,
                expected_points=generated_followup.expected_points,
                followup_count=current_record.followup_count,  # Inherit count
            ))
            state.total_questions += 1
            state.phase = "asking"
            state.conversation_history.append({"role": "interviewer", "content": generated_followup.question})
            self.session_manager.update_session(session_id, state)
            return InterviewResponse(reply=generated_followup.question, done=False)

        # Move to next topic
        state.current_topic_index += 1
        if state.plan and state.current_topic_index >= len(state.plan.planned_topics):
            return self._end_interview(session_id, state)

        if state.plan:
            next_topic = state.plan.planned_topics[state.current_topic_index]
        else:
            return self._end_interview(session_id, state)

        asked_questions = [q.question for q in state.questions_asked]

        generated_question = self.question_generator.generate(
            topic=next_topic,
            candidate=state.candidate,
            experience_level=state.analysis.experience_level.value if state.analysis else "mid",
            questions_already_asked=asked_questions,
        )

        state.questions_asked.append(QuestionRecord(
            topic=next_topic.title,
            question=generated_question.question,
            difficulty=generated_question.estimated_difficulty,
            expected_points=generated_question.expected_points,
        ))
        state.total_questions += 1
        state.phase = "asking"
        state.conversation_history.append({"role": "interviewer", "content": generated_question.question})
        self.session_manager.update_session(session_id, state)

        return InterviewResponse(reply=generated_question.question, done=False)

    def _end_interview(self, session_id: str, state) -> InterviewResponse:
        """Generate feedback and complete the interview."""
        state.phase = "complete"

        score_summary = self.evaluation_engine.calculate_score_summary(state.evaluations)

        feedback = self.feedback_generator.generate(
            evaluations=state.evaluations,
            topic_mastery=state.topic_mastery,
            score_summary=score_summary,
        )

        self.session_manager.update_session(session_id, state)

        return InterviewResponse(
            reply="Thank you for completing the interview. Here is your assessment.",
            done=True,
            feedback=feedback,
        )

    def get_context(self, session_id: str) -> InterviewContext:
        """
        Public interface: retrieve the full InterviewContext for a session.
        Useful for debugging and for future modules that need the full picture.
        """
        state = self.session_manager.get_session(session_id)
        return self.context_builder.build(state)
