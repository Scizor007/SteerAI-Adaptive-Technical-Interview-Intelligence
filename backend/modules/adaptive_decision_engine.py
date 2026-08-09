"""
Adaptive Decision Engine module.

Responsibility:
    Determine the next interview action based on evaluation evidence
    and interview context. This is a lightweight decision layer that
    consumes existing evaluation results without creating a parallel
    scoring system.

Decision types:
    NEXT_TOPIC   - Strong answer, move to next topic
    FOLLOW_UP    - Weak/incomplete, probe deeper
    HARDER       - Strong answer, increase difficulty
    SIMPLER      - Very weak answer, decrease difficulty
    END_INTERVIEW - Sufficient evidence collected
"""

from __future__ import annotations
import logging
from typing import List, Optional

from models.schemas import (
    AdaptiveDecision,
    AdaptiveDecisionResult,
    Difficulty,
    EvaluationResult,
    InterviewPlan,
    QuestionRecord,
)

logger = logging.getLogger(__name__)


class AdaptiveDecisionEngine:
    """
    Pure function-based decision engine.
    Consumes evaluation evidence and returns next action.
    """

    # Thresholds for decision-making
    STRONG_ANSWER_THRESHOLD = 7.0  # out of 10
    WEAK_ANSWER_THRESHOLD = 4.0  # out of 10
    HIGH_MASTERY_THRESHOLD = 70.0  # out of 100
    LOW_MASTERY_THRESHOLD = 40.0  # out of 100

    @classmethod
    def decide(
        cls,
        evaluation: Optional[EvaluationResult],
        current_record: QuestionRecord,
        questions_asked: List[QuestionRecord],
        max_questions: int,
        max_followups: int,
        plan: Optional[InterviewPlan],
        current_topic_index: int,
        topic_mastery: dict,
    ) -> AdaptiveDecisionResult:
        """
        Make an adaptive decision based on evaluation evidence.

        Args:
            evaluation: Result from EvaluationEngine (may be None if LLM failed)
            current_record: The question just answered
            questions_asked: All questions asked so far
            max_questions: Maximum questions allowed
            max_followups: Maximum follow-ups per topic
            plan: Interview plan with topics
            current_topic_index: Current position in plan
            topic_mastery: Current topic mastery scores

        Returns:
            AdaptiveDecisionResult with decision, reason, and metadata
        """
        total_questions = len(questions_asked)

        # Decision 1: END_INTERVIEW if max questions reached
        if total_questions >= max_questions:
            return AdaptiveDecisionResult(
                decision=AdaptiveDecision.END_INTERVIEW,
                reason="Maximum number of questions reached",
                difficulty=Difficulty.INTERMEDIATE,
            )

        # Decision 2: END_INTERVIEW if no more topics
        if plan and current_topic_index >= len(plan.planned_topics) - 1:
            # Check if we have enough evidence
            if total_questions >= max_questions * 0.6:  # At least 60% coverage
                return AdaptiveDecisionResult(
                    decision=AdaptiveDecision.END_INTERVIEW,
                    reason="All planned topics covered with sufficient evidence",
                    difficulty=Difficulty.INTERMEDIATE,
                )

        # If evaluation unavailable (LLM failure), default to NEXT_TOPIC
        if evaluation is None or getattr(evaluation, "_fallback", False):
            logger.info(
                "[ADAPTIVE] Evaluation unavailable, defaulting to NEXT_TOPIC"
            )
            return AdaptiveDecisionResult(
                decision=AdaptiveDecision.NEXT_TOPIC,
                reason="Evaluation unavailable, moving to next topic",
                difficulty=Difficulty.INTERMEDIATE,
            )

        # Extract evaluation metrics
        overall_score = evaluation.overall  # 0-10 scale
        accuracy = evaluation.accuracy
        reasoning = evaluation.reasoning
        depth = evaluation.depth
        topic_name = current_record.topic
        current_mastery = topic_mastery.get(topic_name, 0.0)  # 0-100 scale

        # Decision 3: FOLLOW_UP if needs clarification and under limit
        if (
            current_record.followup_count < max_followups
            and evaluation.needs_followup
        ):
            # But only if answer shows some engagement
            if overall_score > 1.0:  # Not completely empty/off-topic
                return AdaptiveDecisionResult(
                    decision=AdaptiveDecision.FOLLOW_UP,
                    reason=f"Answer incomplete or unclear (score: {overall_score}/10)",
                    target_topic=topic_name,
                    difficulty=current_record.difficulty,
                )

        # Decision 4: SIMPLER if very weak answer on first try
        if (
            overall_score < cls.WEAK_ANSWER_THRESHOLD
            and current_record.followup_count == 0
            and current_record.difficulty != Difficulty.FOUNDATIONAL
        ):
            # Only simplify if not already at lowest difficulty
            new_difficulty = cls._decrease_difficulty(current_record.difficulty)
            return AdaptiveDecisionResult(
                decision=AdaptiveDecision.SIMPLER,
                reason=f"Weak answer (score: {overall_score}/10), providing simpler question on same topic",
                target_topic=topic_name,
                difficulty=new_difficulty,
            )

        # Decision 5: HARDER if strong answer and high mastery
        if (
            overall_score >= cls.STRONG_ANSWER_THRESHOLD
            and current_mastery >= cls.HIGH_MASTERY_THRESHOLD
            and current_record.difficulty != Difficulty.EXPERT
        ):
            # Strong understanding, can challenge more
            new_difficulty = cls._increase_difficulty(current_record.difficulty)
            return AdaptiveDecisionResult(
                decision=AdaptiveDecision.HARDER,
                reason=f"Strong answer (score: {overall_score}/10, mastery: {current_mastery}%), advancing difficulty",
                target_topic=topic_name,
                difficulty=new_difficulty,
            )

        # Decision 6: NEXT_TOPIC (default for acceptable answers)
        return AdaptiveDecisionResult(
            decision=AdaptiveDecision.NEXT_TOPIC,
            reason=f"Acceptable answer (score: {overall_score}/10), moving to next topic",
            difficulty=cls._adjust_difficulty_based_on_trend(
                current_record.difficulty, overall_score
            ),
        )

    @staticmethod
    def _increase_difficulty(current: Difficulty) -> Difficulty:
        """Increase difficulty by one level."""
        order = [
            Difficulty.FOUNDATIONAL,
            Difficulty.INTERMEDIATE,
            Difficulty.ADVANCED,
            Difficulty.EXPERT,
        ]
        try:
            idx = order.index(current)
            return order[min(idx + 1, len(order) - 1)]
        except ValueError:
            return Difficulty.INTERMEDIATE

    @staticmethod
    def _decrease_difficulty(current: Difficulty) -> Difficulty:
        """Decrease difficulty by one level."""
        order = [
            Difficulty.FOUNDATIONAL,
            Difficulty.INTERMEDIATE,
            Difficulty.ADVANCED,
            Difficulty.EXPERT,
        ]
        try:
            idx = order.index(current)
            return order[max(idx - 1, 0)]
        except ValueError:
            return Difficulty.INTERMEDIATE

    @staticmethod
    def _adjust_difficulty_based_on_trend(
        current: Difficulty, score: float
    ) -> Difficulty:
        """Adjust difficulty based on performance trend."""
        if score >= 8.0:
            return AdaptiveDecisionEngine._increase_difficulty(current)
        elif score < 5.0:
            return AdaptiveDecisionEngine._decrease_difficulty(current)
        return current
