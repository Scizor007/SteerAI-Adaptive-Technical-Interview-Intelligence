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
        target_difficulty: Difficulty = None,
    ) -> GeneratedQuestion:
        """
        Generate a single interview question for the given topic via LLM.

        Args:
            topic: The current topic plan entry.
            candidate: Full candidate profile.
            experience_level: "junior" | "mid" | "senior" | "expert"
            questions_already_asked: List of previously asked question texts.
            target_difficulty: Optional difficulty override from adaptive engine.

        Returns:
            A question string to present to the candidate.
        """
        import logging
        logger = logging.getLogger(__name__)
        
        # Use target difficulty if provided, otherwise use topic's difficulty
        effective_difficulty = target_difficulty or topic.difficulty
        
        # Build prompt
        prompt = build_question_prompt(
            topic=topic,
            candidate=candidate,
            experience_level=experience_level,
            questions_already_asked=questions_already_asked,
            target_difficulty=effective_difficulty,
        )
        
        # Generate and parse JSON via LLMService
        response_data = self.llm.generate_json(prompt, fallback_type="question", caller_module="QuestionGenerator")
        
        # Check for fallback
        is_fallback = response_data.get("_fallback", False)
        question_text = str(response_data.get("question") or "")
        
        # If fallback or duplicate, use topic-specific fallback
        if is_fallback or self._is_duplicate(question_text, questions_already_asked):
            if is_fallback:
                logger.warning(f"[QUESTION] LLM unavailable, using topic-specific fallback for: {topic.title}")
            else:
                logger.warning(f"[QUESTION] Duplicate question detected, using fallback for: {topic.title}")
            
            question_text = self._create_topic_fallback(topic, experience_level)
        
        # Validate expected_points
        expected_points = self._string_list(response_data.get("expected_points"))
        if not expected_points and not is_fallback:
            logger.warning(f"[VALIDATION] Question generated without expected_points for topic: {topic.title}")
        
        difficulty = self._parse_difficulty(response_data.get("estimated_difficulty"), effective_difficulty)
        return GeneratedQuestion(
            question=question_text,
            expected_points=expected_points,
            estimated_difficulty=difficulty,
        )
    
    @staticmethod
    def _is_duplicate(question: str, previous_questions: list[str]) -> bool:
        """Check if question is duplicate (case-insensitive, normalized)."""
        if not question:
            return False
        
        normalized = question.lower().strip()
        normalized = ' '.join(normalized.split())  # Collapse whitespace
        
        for prev in previous_questions:
            prev_normalized = prev.lower().strip()
            prev_normalized = ' '.join(prev_normalized.split())
            if normalized == prev_normalized:
                return True
        
        return False
    
    @staticmethod
    def _create_topic_fallback(topic: PlannedTopic, experience_level: str) -> str:
        """Create a topic-specific fallback question when LLM is unavailable or returns duplicate."""
        topic_title = topic.title.lower()
        
        # Topic-aware fallback questions
        if any(word in topic_title for word in ['python', 'java', 'javascript', 'code', 'programming']):
            return f"Can you describe a recent coding challenge you faced in {topic.title} and how you approached it?"
        elif any(word in topic_title for word in ['data', 'sql', 'database']):
            return f"Explain how you would design a data model for {topic.title}. What key considerations would you evaluate?"
        elif any(word in topic_title for word in ['api', 'rest', 'service', 'endpoint']):
            return f"Describe your approach to designing reliable APIs for {topic.title}. What principles do you follow?"
        elif any(word in topic_title for word in ['model', 'ml', 'ai', 'neural', 'learning']):
            return f"Walk me through your process for selecting and evaluating models for {topic.title} use cases."
        elif any(word in topic_title for word in ['test', 'testing', 'quality']):
            return f"What testing strategies do you use for {topic.title} and why are they effective?"
        elif any(word in topic_title for word in ['deploy', 'devops', 'ci/cd', 'infrastructure']):
            return f"Describe your deployment workflow for {topic.title}. What are the critical steps?"
        elif any(word in topic_title for word in ['monitor', 'logging', 'observability']):
            return f"What metrics and logging strategies do you implement for {topic.title}?"
        elif any(word in topic_title for word in ['security', 'auth', 'authentication']):
            return f"What security considerations are most important for {topic.title} and how do you address them?"
        else:
            return f"Can you explain the key concepts in {topic.title} and how you've applied them in practice?"

    @staticmethod
    def _parse_difficulty(value, fallback: Difficulty) -> Difficulty:
        try:
            return Difficulty(str(value).lower())
        except ValueError:
            return fallback

    @staticmethod
    def _string_list(value) -> list[str]:
        return [str(item).strip() for item in value] if isinstance(value, list) else []
