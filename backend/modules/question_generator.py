from __future__ import annotations
"""
Question Generator module.

Responsibility:
    Generate adaptive interview questions for a given topic,
    calibrated to the candidate's experience level and the
    topic's priority in the interview plan.
"""

from models.schemas import CandidateProfile, PlannedTopic
from services.llm_service import LLMService
from services.prompt_builders.question_prompt import build_question_prompt


class QuestionGenerator:
    """Generates contextual interview questions based on topic and candidate profile."""

    def __init__(self, llm_service: LLMService = None):
        """Initialize with optional LLMService for dependency injection."""
        self.llm = llm_service or LLMService()

    def generate(
        self,
        topic: PlannedTopic,
        candidate: CandidateProfile,
        experience_level: str,
        questions_already_asked: list[str],
    ) -> str:
        """
        Generate a single interview question for the given topic via Gemini.

        Args:
            topic: The current topic plan entry.
            candidate: Full candidate profile.
            experience_level: "junior" | "mid" | "senior" | "expert"
            questions_already_asked: List of previously asked question texts.

        Returns:
            A question string to present to the candidate.
        """
        # Build prompt
        prompt = build_question_prompt(
            topic=topic,
            candidate=candidate,
            experience_level=experience_level,
            questions_already_asked=questions_already_asked
        )
        
        # Generate and parse JSON via LLMService
        response_data = self.llm.generate_json(prompt, fallback_type="question")
        
        # Extract the question text
        return response_data.get("question", "Could you explain your understanding of this topic?")
