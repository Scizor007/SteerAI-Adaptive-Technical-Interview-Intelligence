from __future__ import annotations
"""
Question Generator module.

Responsibility:
    Generate adaptive interview questions for a given topic,
    calibrated to the candidate's experience level and the
    topic's priority in the interview plan.
"""

from models.schemas import CandidateProfile, Difficulty, GeneratedQuestion, PlannedTopic
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
    ) -> GeneratedQuestion:
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
        
        difficulty = self._parse_difficulty(response_data.get("estimated_difficulty"), topic.difficulty)
        return GeneratedQuestion(
            question=str(response_data.get("question") or "Could you explain your understanding of this topic?"),
            expected_points=self._string_list(response_data.get("expected_points")),
            estimated_difficulty=difficulty,
        )

    @staticmethod
    def _parse_difficulty(value, fallback: Difficulty) -> Difficulty:
        try:
            return Difficulty(str(value).lower())
        except ValueError:
            return fallback

    @staticmethod
    def _string_list(value) -> list[str]:
        return [str(item).strip() for item in value] if isinstance(value, list) else []
