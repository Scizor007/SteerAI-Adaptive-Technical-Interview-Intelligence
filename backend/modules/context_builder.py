from __future__ import annotations
"""
Interview Context Builder module.

Responsibility:
    Merge all session data into a single InterviewContext object
    that downstream modules consume.

    This module collects:
    - Session state
    - Candidate profile
    - Candidate analysis
    - Interview plan
    - Progress tracking
    - Coverage state
    - Conversation history
    - Current topic

    Every future module (QuestionGenerator, EvaluationEngine, etc.)
    should consume InterviewContext instead of querying multiple services.
"""

from models.schemas import (
    InterviewState,
    InterviewContext,
    InterviewProgress,
    CoverageState,
    InterviewPhase,
    Difficulty,
    PlannedTopic,
    CandidateAnalysis,
    InterviewPlan,
)


class InterviewContextBuilder:
    """Builds a unified InterviewContext from session state."""

    @staticmethod
    def build(state: InterviewState) -> InterviewContext:
        """
        Build an InterviewContext from the current InterviewState.

        Raises:
            ValueError: If state is missing analysis or plan.
        """
        if state.analysis is None:
            raise ValueError(
                f"Session '{state.session_id}' has no CandidateAnalysis. "
                "Run CandidateAnalyzer before building context."
            )
        if state.plan is None:
            raise ValueError(
                f"Session '{state.session_id}' has no InterviewPlan. "
                "Run InterviewPlanner before building context."
            )

        analysis: CandidateAnalysis = state.analysis
        plan: InterviewPlan = state.plan

        # Determine current topic
        current_topic: PlannedTopic | None = None
        if (
            plan.planned_topics
            and 0 <= state.current_topic_index < len(plan.planned_topics)
        ):
            current_topic = plan.planned_topics[state.current_topic_index]

        # Determine current difficulty
        current_difficulty = Difficulty.INTERMEDIATE
        if current_topic:
            current_difficulty = current_topic.difficulty
        elif plan.starting_difficulty:
            current_difficulty = plan.starting_difficulty

        # Build coverage state from questions asked
        coverage = InterviewContextBuilder._build_coverage(state)

        # Build progress
        progress = InterviewContextBuilder._build_progress(state, plan)

        return InterviewContext(
            session_id=state.session_id,
            candidate=state.candidate,
            analysis=analysis,
            plan=plan,
            progress=progress,
            coverage=coverage,
            questions_asked=state.questions_asked,
            evaluations=state.evaluations,
            topic_mastery=state.topic_mastery,
            conversation_history=state.conversation_history,
            current_topic=current_topic,
            current_difficulty=current_difficulty,
        )

    @staticmethod
    def _build_coverage(state: InterviewState) -> CoverageState:
        """Build a CoverageState from the questions asked so far."""
        days_covered: set[int] = set()
        modules_covered: set[str] = set()
        topics_asked: list[str] = []

        if state.plan and state.plan.planned_topics:
            topic_lookup = {t.title: t for t in state.plan.planned_topics}
            for record in state.questions_asked:
                topics_asked.append(record.topic)
                planned = topic_lookup.get(record.topic)
                if planned:
                    days_covered.add(planned.day)
                    modules_covered.add(planned.module_name)

        return CoverageState(
            days_covered=days_covered,
            modules_covered=modules_covered,
            topics_asked=topics_asked,
        )

    @staticmethod
    def _build_progress(state: InterviewState, plan: InterviewPlan) -> InterviewProgress:
        """Build an InterviewProgress from session state."""
        questions_asked = state.total_questions
        total_planned = plan.total_planned_questions
        questions_remaining = max(0, min(state.max_questions, total_planned) - questions_asked)

        # Map the string phase to enum
        try:
            phase = InterviewPhase(state.phase)
        except ValueError:
            phase = InterviewPhase.INITIALIZING

        # Current difficulty from the current topic
        current_difficulty = Difficulty.INTERMEDIATE
        if (
            plan.planned_topics
            and 0 <= state.current_topic_index < len(plan.planned_topics)
        ):
            current_difficulty = plan.planned_topics[state.current_topic_index].difficulty

        return InterviewProgress(
            questions_asked=questions_asked,
            questions_remaining=questions_remaining,
            current_topic_index=state.current_topic_index,
            current_difficulty=current_difficulty,
            phase=phase,
        )
