"""
Interview Manager — orchestrator module.

Responsibility:
    Composes all interview modules into a single workflow.
    This is the only module the router interacts with.
    Delegates to: CandidateAnalyzer, InterviewPlanner, QuestionGenerator,
    FollowupGenerator, EvaluationEngine, FeedbackGenerator, SessionManager.
"""

from models.schemas import (
    CandidateProfile,
    InterviewResponse,
    QuestionRecord,
)
from modules.candidate_analyzer import CandidateAnalyzer
from modules.interview_planner import InterviewPlanner
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
        start_interview() → analyze candidate → create plan → ask first question
        continue_interview() → evaluate answer → follow-up or next topic → or end
    """

    def __init__(self):
        self.candidate_analyzer = CandidateAnalyzer()
        self.interview_planner = InterviewPlanner()
        self.question_generator = QuestionGenerator()
        self.followup_generator = FollowupGenerator()
        self.evaluation_engine = EvaluationEngine()
        self.feedback_generator = FeedbackGenerator()
        self.session_manager = SessionManager()

    async def start_interview(
        self,
        session_id: str,
        candidate: CandidateProfile,
    ) -> InterviewResponse:
        """
        Initialize a new interview session.

        Steps:
        1. Analyze the candidate profile
        2. Create an interview plan
        3. Create a session
        4. Generate the first question
        """
        # Step 1: Analyze candidate
        analysis = self.candidate_analyzer.analyze(candidate)

        # Step 2: Plan the interview
        topic_plan = self.interview_planner.create_plan(candidate, analysis)

        # Step 3: Create session
        state = self.session_manager.create_session(
            session_id=session_id,
            candidate=candidate,
            max_questions=MAX_QUESTIONS_PER_INTERVIEW,
        )
        state.topic_plan = topic_plan
        state.phase = "asking"

        # Step 4: Generate first question
        if not topic_plan:
            state.phase = "complete"
            self.session_manager.update_session(session_id, state)
            return InterviewResponse(
                reply="No topics to cover based on your profile. Interview complete.",
                done=True,
            )

        first_topic = topic_plan[0]
        question = self.question_generator.generate(
            topic=first_topic,
            candidate=candidate,
            experience_level=analysis["experience_level"],
            questions_already_asked=[],
        )

        # Record the question
        state.questions_asked.append(QuestionRecord(
            topic=first_topic.title,
            question=question,
        ))
        state.total_questions = 1
        state.conversation_history.append({"role": "interviewer", "content": question})

        self.session_manager.update_session(session_id, state)

        welcome = (
            f"Welcome, {candidate.member.name}. "
            f"I'll be conducting your technical interview today, "
            f"focusing on your experience with the AI curriculum. "
            f"Let's begin.\n\n{question}"
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
        3. Evaluate the response
        4. Decide: follow-up, next topic, or end
        5. Generate next question or final feedback
        """
        state = self.session_manager.get_session(session_id)
        state.phase = "evaluating"

        # Record the answer
        state.conversation_history.append({"role": "candidate", "content": message})

        current_record = state.questions_asked[-1] if state.questions_asked else None
        if current_record and current_record.answer is None:
            current_record.answer = message

            # Evaluate the response
            analysis = self.candidate_analyzer.analyze(state.candidate)
            score = self.evaluation_engine.evaluate_response(
                question=current_record.question,
                answer=message,
                topic_title=current_record.topic,
                experience_level=analysis["experience_level"],
            )
            current_record.score = score

        # Check if interview should end
        if state.total_questions >= state.max_questions:
            return self._end_interview(session_id, state)

        # Decide: follow-up or next topic
        if current_record and self.followup_generator.should_follow_up(
            current_record, MAX_FOLLOWUPS_PER_TOPIC
        ):
            # Generate follow-up
            followup = self.followup_generator.generate(
                original_question=current_record.question,
                candidate_answer=message,
                topic_title=current_record.topic,
            )
            current_record.followup_count += 1
            state.questions_asked.append(QuestionRecord(
                topic=current_record.topic,
                question=followup,
            ))
            state.total_questions += 1
            state.phase = "asking"
            state.conversation_history.append({"role": "interviewer", "content": followup})
            self.session_manager.update_session(session_id, state)
            return InterviewResponse(reply=followup, done=False)

        # Move to next topic
        state.current_topic_index += 1
        if state.current_topic_index >= len(state.topic_plan):
            return self._end_interview(session_id, state)

        next_topic = state.topic_plan[state.current_topic_index]
        analysis = self.candidate_analyzer.analyze(state.candidate)
        asked_questions = [q.question for q in state.questions_asked]

        question = self.question_generator.generate(
            topic=next_topic,
            candidate=state.candidate,
            experience_level=analysis["experience_level"],
            questions_already_asked=asked_questions,
        )

        state.questions_asked.append(QuestionRecord(
            topic=next_topic.title,
            question=question,
        ))
        state.total_questions += 1
        state.phase = "asking"
        state.conversation_history.append({"role": "interviewer", "content": question})
        self.session_manager.update_session(session_id, state)

        return InterviewResponse(reply=question, done=False)

    def _end_interview(self, session_id: str, state) -> InterviewResponse:
        """Generate feedback and complete the interview."""
        state.phase = "complete"

        topic_scores = self.evaluation_engine.calculate_topic_score(state.questions_asked)
        overall_score = self.evaluation_engine.calculate_overall_score(state.questions_asked)

        feedback = self.feedback_generator.generate(
            candidate=state.candidate,
            questions=state.questions_asked,
            topic_plan=state.topic_plan,
            topic_scores=topic_scores,
            overall_score=overall_score,
        )

        self.session_manager.update_session(session_id, state)

        return InterviewResponse(
            reply="Thank you for completing the interview. Here is your assessment.",
            done=True,
            feedback=feedback,
        )
