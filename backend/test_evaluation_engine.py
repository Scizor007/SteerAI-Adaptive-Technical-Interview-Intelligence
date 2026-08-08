"""Tests for evidence-based answer evaluation and deterministic score aggregation."""

import unittest
import asyncio
import json
from pathlib import Path

from models.schemas import CandidateProfile, EvaluationEvidence, QuestionRecord
from modules.evaluation_engine import EvaluationEngine
from modules.interview_manager import InterviewManager


class FakeLLMService:
    """Returns controlled LLM JSON so score math is tested without network access."""

    RESPONSES = {
        "excellent": {
            "accuracy": 9,
            "reasoning": 9,
            "depth": 8,
            "completeness": 9,
            "communication": 9,
            "confidence": 8,
            "strengths": ["Explains the retrieval pipeline and trade-offs."],
            "missing_points": [],
            "misconceptions": [],
            "topic_mastery": "High",
            "interviewer_notes": "Strong, evidence-based answer.",
        },
        "average": {
            "accuracy": 6,
            "reasoning": 5,
            "depth": 5,
            "completeness": 5,
            "communication": 6,
            "confidence": 5,
            "strengths": ["Identifies the main component."],
            "missing_points": ["Does not discuss trade-offs."],
            "misconceptions": [],
            "topic_mastery": "Medium",
            "interviewer_notes": "Basic but incomplete answer.",
        },
        "poor": {
            "accuracy": 2,
            "reasoning": 2,
            "depth": 1,
            "completeness": 1,
            "communication": 3,
            "confidence": 2,
            "strengths": [],
            "missing_points": ["Does not address the question."],
            "misconceptions": ["Claims embeddings are databases."],
            "topic_mastery": "Low",
            "interviewer_notes": "Incorrect response.",
        },
        "off-topic": {
            "accuracy": 1,
            "reasoning": 1,
            "depth": 1,
            "completeness": 0,
            "communication": 3,
            "confidence": 2,
            "strengths": [],
            "missing_points": ["Answer is unrelated to retrieval."],
            "misconceptions": [],
            "topic_mastery": "Low",
            "interviewer_notes": "Off-topic response.",
        },
    }

    def generate_json(self, prompt, fallback_type="evaluation"):
        for marker, response in self.RESPONSES.items():
            if marker in prompt:
                return response
        raise AssertionError("Test answer marker was not present in the evaluation prompt")


class FakeInterviewLLM:
    """Controlled model responses for an end-to-end interview-manager test."""

    def generate_json(self, prompt, fallback_type="question"):
        if fallback_type in {"question", "followup"}:
            return {
                "question": "Explain the technical trade-offs in this design.",
                "expected_points": ["Explains a trade-off", "Supports it with reasoning"],
                "estimated_difficulty": "intermediate",
            }
        if fallback_type == "feedback":
            return {
                "summary": "Assessment synthesized from submitted answers.",
                "strengths": ["Uses evidence in answers."],
                "gaps": ["Review weak concepts identified in evidence."],
                "next": ["Practice the identified gaps."],
            }
        if "strong answer" in prompt:
            return FakeLLMService.RESPONSES["excellent"]
        return FakeLLMService.RESPONSES["poor"]


class TestEvaluationEngine(unittest.TestCase):
    def setUp(self):
        self.engine = EvaluationEngine(llm_service=FakeLLMService())
        self.context = type("Context", (), {"evaluations": []})()
        self.question = QuestionRecord(
            topic="RAG",
            question="How would you design a retrieval pipeline?",
            expected_points=["Explain retrieval", "Explain ranking trade-offs"],
        )

    def evaluate(self, answer):
        return self.engine.evaluate_response(self.context, self.question, answer)

    def test_excellent_average_poor_and_off_topic_answers_score_differently(self):
        excellent = self.evaluate("excellent answer")
        average = self.evaluate("average answer")
        poor = self.evaluate("poor answer")
        off_topic = self.evaluate("off-topic answer")

        self.assertGreater(excellent.overall, average.overall)
        self.assertGreater(average.overall, poor.overall)
        self.assertGreater(poor.overall, off_topic.overall)
        self.assertFalse(excellent.needs_followup)
        self.assertTrue(poor.needs_followup)
        self.assertEqual(excellent.difficulty_recommendation, "raise")
        self.assertEqual(poor.difficulty_recommendation, "lower")

    def test_empty_answer_is_independently_scored_at_zero(self):
        result = self.evaluate("   ")

        self.assertEqual(result.overall, 0.0)
        self.assertEqual(result.accuracy, 0.0)
        self.assertTrue(result.needs_followup)
        self.assertEqual(result.knowledge_gap, "No response provided")

    def test_topic_mastery_and_interview_score_use_evaluation_evidence_only(self):
        strong = self.evaluate("excellent answer")
        weak = self.evaluate("poor answer")
        evaluations = [
            EvaluationEvidence(
                question=self.question.question,
                topic="RAG",
                candidate_answer="excellent answer",
                expected_points=self.question.expected_points,
                evaluation_result=strong,
                timestamp="2026-08-08T00:00:00+00:00",
            ),
            EvaluationEvidence(
                question="Explain vector search.",
                topic="Vector DB",
                candidate_answer="poor answer",
                expected_points=[],
                evaluation_result=weak,
                timestamp="2026-08-08T00:01:00+00:00",
            ),
        ]

        mastery = self.engine.calculate_topic_mastery(evaluations)
        summary = self.engine.calculate_score_summary(evaluations)

        self.assertGreater(mastery["RAG"], mastery["Vector DB"])
        self.assertGreater(summary.accuracy, 0)
        self.assertLess(summary.overall_score, 100)
        self.assertGreater(summary.coverage_bonus, 0)

    def test_complete_interviews_with_strong_and_poor_answers_have_distinct_final_scores(self):
        candidate_data = json.loads(
            (Path(__file__).parent / "data" / "candidates.json").read_text(encoding="utf-8")
        )["candidates"][0]
        candidate = CandidateProfile(**candidate_data)

        strong_feedback = self._run_complete_interview(candidate, "strong answer with reasoning and a concrete trade-off explained in detail.")
        poor_feedback = self._run_complete_interview(candidate, "poor answer with unrelated claims and no relevant technical reasoning provided here.")

        self.assertGreater(strong_feedback.overall_score, poor_feedback.overall_score + 40)
        self.assertTrue(strong_feedback.topic_mastery)
        self.assertTrue(poor_feedback.evidence)

    @staticmethod
    def _run_complete_interview(candidate, answer):
        manager = InterviewManager()
        fake_llm = FakeInterviewLLM()
        manager.question_generator.llm = fake_llm
        manager.followup_generator.llm = fake_llm
        manager.evaluation_engine.llm = fake_llm
        manager.feedback_generator.llm = fake_llm

        async def run():
            response = await manager.start_interview(f"test-{answer[:6]}", candidate)
            while not response.done:
                response = await manager.continue_interview(f"test-{answer[:6]}", answer)
            return response.feedback

        return asyncio.run(run())


if __name__ == "__main__":
    unittest.main()
