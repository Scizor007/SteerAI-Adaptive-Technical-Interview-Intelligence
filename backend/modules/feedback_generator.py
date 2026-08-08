from __future__ import annotations
"""
Feedback Generator module.

Responsibility:
    Produce structured final feedback when the interview ends.
    Aggregates evaluation data into the format required by the
    technical specification: summary, strengths, gaps, next.
"""

from models.schemas import (
    CandidateProfile,
    Feedback,
    QuestionRecord,
    TopicPlan,
)
from services.llm_service import LLMService
from services.prompt_builders.feedback_prompt import build_feedback_prompt


class FeedbackGenerator:
    """Generates structured interview feedback from evaluation results."""

    def __init__(self, llm_service: LLMService = None):
        """Initialize with optional LLMService for dependency injection."""
        self.llm = llm_service or LLMService()

    def generate(
        self,
        candidate: CandidateProfile,
        questions: list[QuestionRecord],
        topic_plan: list[TopicPlan],
        topic_scores: dict[str, float],
        overall_score: float,
    ) -> Feedback:
        """
        Generate final structured feedback via Gemini.

        Args:
            candidate: The candidate's profile.
            questions: All question records from the interview.
            topic_plan: The planned topics.
            topic_scores: Per-topic average scores.
            overall_score: Overall interview score.

        Returns:
            Feedback object matching the technical specification.
        """
        prompt = build_feedback_prompt(
            candidate=candidate,
            questions=questions,
            overall_score=overall_score
        )
        
        response_data = self.llm.generate_json(prompt, fallback_type="feedback")
        
        return Feedback(
            summary=response_data.get("summary", "Interview completed."),
            strengths=response_data.get("strengths", ["Completed the assessment"]),
            gaps=response_data.get("gaps", ["No significant gaps identified"]),
            next=response_data.get("next", response_data.get("recommendations", ["Keep practicing"]))
        )
