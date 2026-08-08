from __future__ import annotations
"""
Follow-up Generator module.

Responsibility:
    Generate intelligent follow-up questions based on the candidate's
    response quality. Probes deeper when answers are vague, and moves
    on when answers demonstrate sufficient understanding.
"""

from models.schemas import QuestionRecord


class FollowupGenerator:
    """Generates contextual follow-up questions based on candidate responses."""

    def should_follow_up(self, record: QuestionRecord, max_followups: int = 2) -> bool:
        """
        Determine whether a follow-up question is warranted.

        Args:
            record: The current question record with the candidate's answer.
            max_followups: Maximum follow-ups allowed per topic.

        Returns:
            True if a follow-up should be asked.
        """
        if record.followup_count >= max_followups:
            return False

        # TODO: Replace with LLM-based evaluation of answer completeness
        # For now, follow up if the answer is very short (likely incomplete)
        if record.answer and len(record.answer.strip()) < 50:
            return True

        return False

    def generate(
        self,
        original_question: str,
        candidate_answer: str,
        topic_title: str,
    ) -> str:
        """
        Generate a follow-up question that probes deeper into the topic.

        Args:
            original_question: The question that was asked.
            candidate_answer: The candidate's response.
            topic_title: The topic being discussed.

        Returns:
            A follow-up question string.
        """
        # TODO: Replace with LLM-powered follow-up generation
        return (
            f"That's a good start on {topic_title}. "
            f"Could you elaborate further on the practical implications "
            f"and any challenges you've encountered?"
        )
