from __future__ import annotations
"""
Feedback Generator module.

Responsibility:
    Produce structured final feedback when the interview ends.
    Aggregates evaluation data into the format required by the
    technical specification: summary, strengths, gaps, next.
"""

from models.schemas import (
    EvaluationEvidence,
    Feedback,
    InterviewScoreSummary,
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
        evaluations: list[EvaluationEvidence],
        topic_mastery: dict[str, float],
        score_summary: InterviewScoreSummary,
    ) -> Feedback:
        """
        Generate final structured feedback via Gemini.

        Args:
            evaluations: Evidence collected for each submitted answer.
            topic_mastery: Deterministic per-topic mastery values.
            score_summary: Deterministic, evidence-based aggregate score.

        Returns:
            Feedback object matching the technical specification.
        """
        prompt = build_feedback_prompt(
            evaluations=evaluations,
            topic_mastery=topic_mastery,
            score_summary=score_summary,
        )
        
        response_data = self.llm.generate_json(prompt, fallback_type="feedback", caller_module="FeedbackGenerator")
        
        return Feedback(
            summary=response_data.get("summary", "Interview completed."),
            strengths=response_data.get("strengths", ["Completed the assessment"]),
            gaps=response_data.get("gaps", ["No significant gaps identified"]),
            next=response_data.get("next", response_data.get("recommendations", ["Keep practicing"])),
            overall_score=score_summary.overall_score,
            accuracy=score_summary.accuracy,
            reasoning=score_summary.reasoning,
            depth=score_summary.depth,
            completeness=score_summary.completeness,
            communication=score_summary.communication,
            confidence=score_summary.confidence,
            topic_mastery=topic_mastery,
            evidence=self._evidence_lines(evaluations),
            interviewer_notes=[item.evaluation_result.interviewer_notes for item in evaluations if item.evaluation_result.interviewer_notes],
        )

    @staticmethod
    def _evidence_lines(evaluations: list[EvaluationEvidence]) -> list[str]:
        """Expose concise traceable evidence without inventing profile-based claims."""
        lines = []
        for item in evaluations:
            result = item.evaluation_result
            if result.strengths:
                lines.append(f"{item.topic}: {result.strengths[0]}")
            elif result.knowledge_gap:
                lines.append(f"{item.topic}: {result.knowledge_gap}")
        return lines
