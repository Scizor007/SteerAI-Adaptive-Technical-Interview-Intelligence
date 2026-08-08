"""Prompt construction for evidence-only answer evaluation."""

from typing import List

from models.schemas import EvaluationEvidence, InterviewContext, QuestionRecord


def build_evaluation_prompt(
    context: InterviewContext,
    current_question: QuestionRecord,
    expected_points: List[str],
    candidate_answer: str,
    previous_evaluations: List[EvaluationEvidence],
) -> str:
    """Build a constrained prompt that evaluates only one submitted answer."""
    prior_count = len(previous_evaluations)
    expected = "\n".join(f"- {point}" for point in expected_points) or "- No explicit rubric points were generated."

    return f"""
You are a senior engineering interviewer evaluating one submitted answer for SteerAI.

Topic: {current_question.topic}
Target difficulty: {current_question.difficulty.value}
Question: {current_question.question}
Expected answer points:
{expected}

Candidate answer to evaluate:
{candidate_answer}

There are {prior_count} earlier evaluations in this interview. They are context only; score this answer independently.

Rules:
1. Score ONLY evidence in the submitted answer. Never infer knowledge, experience, or competence that is not demonstrated.
2. Do not use candidate profile completion, previous curriculum performance, or answer length as a proxy for knowledge.
3. Do not inflate scores. An empty, evasive, or off-topic answer must score very low.
4. Score accuracy, reasoning, depth, completeness, communication, and confidence from 0 to 10.
5. Return concise, evidence-based strengths, missing points, and misconceptions. Use empty arrays when none apply.
6. Return JSON only, with no Markdown or explanatory text.

Return exactly this JSON shape:
{{
  "accuracy": 0,
  "reasoning": 0,
  "depth": 0,
  "completeness": 0,
  "communication": 0,
  "confidence": 0,
  "strengths": ["..."],
  "missing_points": ["..."],
  "misconceptions": ["..."],
  "suggested_followup": "...",
  "topic_mastery": "Low|Medium|High",
  "interviewer_notes": "..."
}}
""".strip()
