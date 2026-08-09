from __future__ import annotations
"""
Follow-up Generator module.

Responsibility:
    Generate intelligent follow-up questions based on the candidate's
    response quality. Probes deeper when answers are vague, and moves
    on when answers demonstrate sufficient understanding.
"""

from models.schemas import Difficulty, GeneratedQuestion, QuestionRecord
from services.llm_service import LLMService
from services.prompt_builders.followup_prompt import build_followup_prompt


class FollowupGenerator:
    """Generates contextual follow-up questions based on candidate responses."""

    def __init__(self, llm_service: LLMService = None):
        """Initialize with optional LLMService for dependency injection."""
        self.llm = llm_service or LLMService()

    def should_follow_up(
        self,
        record: QuestionRecord,
        evaluation_result,
        max_followups: int = 2
    ) -> bool:
        """
        Determine whether a follow-up question is warranted.

        Args:
            record: The current question record with the candidate's answer.
            evaluation_result: The evaluation result for this answer (or None if unavailable).
            max_followups: Maximum follow-ups allowed per topic.

        Returns:
            True if a follow-up should be asked.
        """
        # Strict maximum enforcement - ALWAYS respected
        if record.followup_count >= max_followups:
            return False

        # If evaluation unavailable (LLM failure), do NOT trigger follow-up
        # This prevents LLM failures from being interpreted as poor answers
        if evaluation_result is None or getattr(evaluation_result, '_fallback', False):
            return False

        # Primary decision: use evaluation result if available
        if hasattr(evaluation_result, 'needs_followup'):
            return evaluation_result.needs_followup

        # Fallback to deterministic rule only if evaluation lacks needs_followup
        # Empty or very short answers may need clarification
        if not record.answer or len(record.answer.strip()) < 20:
            return True

        return False

    def generate(
        self,
        original_question: str,
        candidate_answer: str,
        topic_title: str,
        evaluation_result = None,
        expected_points: list[str] = None,
        previous_followups: list[str] = None,
    ) -> GeneratedQuestion:
        """
        Generate a follow-up question that probes deeper into the topic via LLM.

        Args:
            original_question: The question that was asked.
            candidate_answer: The candidate's response.
            topic_title: The topic being discussed.
            evaluation_result: Optional EvaluationResult with missing points, misconceptions, strengths.
            expected_points: Optional expected points from the original question.
            previous_followups: Optional list of previous follow-up questions to avoid repetition.

        Returns:
            A follow-up question string.
        """
        import logging
        logger = logging.getLogger(__name__)
        
        prompt = build_followup_prompt(
            original_question=original_question,
            candidate_answer=candidate_answer,
            topic_title=topic_title,
            evaluation_result=evaluation_result,
            expected_points=expected_points,
            previous_followups=previous_followups,
        )
        
        response_data = self.llm.generate_json(prompt, fallback_type="followup", caller_module="FollowupGenerator")
        
        # Detect fallback and create topic-specific question instead of generic
        if response_data.get("_fallback"):
            logger.warning(f"[FOLLOWUP] LLM unavailable, using topic-specific fallback for: {topic_title}")
            return GeneratedQuestion(
                question=self._create_topic_fallback(topic_title, candidate_answer),
                expected_points=[],
                estimated_difficulty=Difficulty.INTERMEDIATE,
            )
        
        try:
            difficulty = Difficulty(str(response_data.get("estimated_difficulty")).lower())
        except ValueError:
            difficulty = Difficulty.INTERMEDIATE
        expected_points = response_data.get("expected_points", [])
        return GeneratedQuestion(
            question=str(response_data.get("question") or "Could you elaborate further on that?"),
            expected_points=[str(item).strip() for item in expected_points] if isinstance(expected_points, list) else [],
            estimated_difficulty=difficulty,
        )
    
    def _create_topic_fallback(self, topic: str, answer: str) -> str:
        """Create a topic-specific fallback question when LLM is unavailable."""
        # Basic topic-aware fallback
        topic_lower = topic.lower()
        
        if any(word in topic_lower for word in ['python', 'java', 'javascript', 'coding', 'programming']):
            return f"Can you explain your approach to solving {topic} problems and why you chose that method?"
        elif any(word in topic_lower for word in ['data', 'sql', 'database']):
            return f"Can you walk me through your data handling approach and the reasoning behind it?"
        elif any(word in topic_lower for word in ['api', 'rest', 'service']):
            return f"Can you describe the API design choices you made and why they were appropriate?"
        elif any(word in topic_lower for word in ['model', 'ml', 'ai', 'neural']):
            return f"Can you explain the model selection process and key considerations you evaluated?"
        elif any(word in topic_lower for word in ['project', 'experience']):
            return f"What was your specific role and contribution to the project you mentioned?"
        else:
            return f"Can you explain the main technical concept you used and why it was the right choice?"
