"""Evidence-based evaluation and deterministic interview score aggregation."""

from __future__ import annotations

from statistics import pstdev
from typing import Any, Dict, List

from models.schemas import (
    EvaluationEvidence,
    EvaluationResult,
    InterviewContext,
    InterviewScoreSummary,
    QuestionRecord,
)
from services.llm_service import LLMService
from services.prompt_builders.evaluation_prompt import build_evaluation_prompt


class EvaluationEngine:
    """Uses Gemini for per-answer assessment and backend rules for all scoring math."""

    DIMENSIONS = (
        "accuracy",
        "reasoning",
        "depth",
        "completeness",
        "communication",
        "confidence",
    )
    ANSWER_WEIGHTS = {
        "accuracy": 0.30,
        "reasoning": 0.20,
        "depth": 0.20,
        "completeness": 0.10,
        "communication": 0.10,
        "confidence": 0.10,
    }

    def __init__(self, llm_service: LLMService = None):
        self.llm = llm_service or LLMService()

    def evaluate_response(
        self,
        context: InterviewContext,
        current_question: QuestionRecord,
        answer: str,
    ) -> EvaluationResult:
        """Evaluate one answer independently and normalize the structured LLM output."""
        import logging
        logger = logging.getLogger(__name__)
        
        if not answer or not answer.strip():
            logger.info("Empty answer submitted - returning zero score")
            return EvaluationResult(
                missing_points=["No answer was submitted."],
                interviewer_notes="The candidate submitted an empty response.",
                needs_followup=True,
                difficulty_recommendation="lower",
                knowledge_gap="No response provided",
            )

        prompt = build_evaluation_prompt(
            context=context,
            current_question=current_question,
            expected_points=current_question.expected_points,
            candidate_answer=answer,
            previous_evaluations=context.evaluations,
        )
        
        response = self.llm.generate_json(prompt, fallback_type="evaluation", caller_module="EvaluationEngine")
        
        # Detect fallback
        if response.get("_fallback"):
            logger.error("[FALLBACK] EVALUATION FALLBACK DETECTED - LLM unavailable, returning zero score")
        
        result = self._normalize_result(response)
        
        return result

    def _normalize_result(self, response: Dict[str, Any]) -> EvaluationResult:
        """Validate untrusted LLM JSON and compute the weighted per-answer score."""
        scores = {dimension: self._normalize_score(response.get(dimension)) for dimension in self.DIMENSIONS}
        overall = sum(scores[dimension] * self.ANSWER_WEIGHTS[dimension] for dimension in self.DIMENSIONS)
        missing_points = self._string_list(response.get("missing_points"))
        misconceptions = self._string_list(response.get("misconceptions"))
        strengths = self._string_list(response.get("strengths"))
        knowledge_gap = self._first_text(misconceptions) or self._first_text(missing_points)

        if overall < 4.0:
            difficulty_recommendation = "lower"
        elif overall >= 8.0:
            difficulty_recommendation = "raise"
        else:
            difficulty_recommendation = "maintain"

        return EvaluationResult(
            **scores,
            overall=round(overall, 2),
            strengths=strengths,
            missing_points=missing_points,
            misconceptions=misconceptions,
            suggested_followup=self._optional_text(response.get("suggested_followup")),
            topic_mastery=self._mastery_label(response.get("topic_mastery"), overall),
            interviewer_notes=self._optional_text(response.get("interviewer_notes")) or "",
            needs_followup=overall < 6.0 or bool(missing_points or misconceptions),
            difficulty_recommendation=difficulty_recommendation,
            knowledge_gap=knowledge_gap,
        )

    def calculate_topic_mastery(self, evaluations: List[EvaluationEvidence]) -> Dict[str, float]:
        """Average each topic's evidence scores and normalize mastery to 0-100."""
        grouped: Dict[str, List[float]] = {}
        for evidence in evaluations:
            grouped.setdefault(evidence.topic, []).append(evidence.evaluation_result.overall * 10)
        return {
            topic: round(sum(scores) / len(scores), 1)
            for topic, scores in grouped.items()
            if scores
        }

    def calculate_score_summary(self, evaluations: List[EvaluationEvidence]) -> InterviewScoreSummary:
        """Calculate the 0-100 interview score from answer evidence only."""
        if not evaluations:
            return InterviewScoreSummary()

        average = {
            dimension: sum(getattr(item.evaluation_result, dimension) for item in evaluations) / len(evaluations)
            for dimension in self.DIMENSIONS
        }
        topic_count = len({item.topic for item in evaluations})
        coverage_bonus = min(5.0, float(topic_count))
        answer_scores = [item.evaluation_result.overall for item in evaluations]
        consistency_bonus = round(max(0.0, 5.0 - min(5.0, pstdev(answer_scores))), 2)
        base_score = sum(average[dimension] * self.ANSWER_WEIGHTS[dimension] for dimension in self.DIMENSIONS) * 9
        return InterviewScoreSummary(
            overall_score=round(min(100.0, base_score + coverage_bonus + consistency_bonus), 1),
            accuracy=round(average["accuracy"] * 10, 1),
            reasoning=round(average["reasoning"] * 10, 1),
            depth=round(average["depth"] * 10, 1),
            completeness=round(average["completeness"] * 10, 1),
            communication=round(average["communication"] * 10, 1),
            confidence=round(average["confidence"] * 10, 1),
            coverage_bonus=coverage_bonus,
            consistency_bonus=consistency_bonus,
        )

    @staticmethod
    def _normalize_score(value: Any) -> float:
        try:
            return round(max(0.0, min(10.0, float(value))), 2)
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def _string_list(value: Any) -> List[str]:
        if not isinstance(value, list):
            return []
        return [str(item).strip() for item in value if str(item).strip()]

    @staticmethod
    def _optional_text(value: Any) -> str | None:
        if value is None:
            return None
        text = str(value).strip()
        return text or None

    @staticmethod
    def _first_text(values: List[str]) -> str | None:
        return values[0] if values else None

    @staticmethod
    def _mastery_label(value: Any, overall: float) -> str:
        normalized = str(value or "").strip().title()
        if normalized in {"Low", "Medium", "High"}:
            return normalized
        if overall >= 8:
            return "High"
        if overall >= 5:
            return "Medium"
        return "Low"
