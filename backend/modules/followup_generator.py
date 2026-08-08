from __future__ import annotations
"""
Follow-up Generator module.

Responsibility:
    Generate intelligent follow-up questions based on the candidate's
    response quality. Probes deeper when answers are vague, and moves
    on when answers demonstrate sufficient understanding.
"""

from models.schemas import QuestionRecord
from services.llm_service import LLMService
from services.prompt_builders.followup_prompt import build_followup_prompt


class FollowupGenerator:
    """Generates contextual follow-up questions based on candidate responses."""

    def __init__(self, llm_service: LLMService = None):
        """Initialize with optional LLMService for dependency injection."""
        self.llm = llm_service or LLMService()

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

        # Keeping the deterministic check based on prompt:
        # "The deterministic backend remains responsible for... interview progression"
        # We will follow up if the answer is short.
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
        Generate a follow-up question that probes deeper into the topic via Gemini.

        Args:
            original_question: The question that was asked.
            candidate_answer: The candidate's response.
            topic_title: The topic being discussed.

        Returns:
            A follow-up question string.
        """
        prompt = build_followup_prompt(
            original_question=original_question,
            candidate_answer=candidate_answer,
            topic_title=topic_title
        )
        
        response_data = self.llm.generate_json(prompt, fallback_type="followup")
        
        return response_data.get("question", "Could you elaborate further on that?")
