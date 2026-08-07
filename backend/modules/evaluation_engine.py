"""
Evaluation Engine module.

Responsibility:
    Score individual candidate responses and maintain cumulative
    performance tracking across the interview. Provides per-topic
    and overall assessment data to the Feedback Generator.
"""

from models.schemas import QuestionRecord


class EvaluationEngine:
    """Evaluates candidate responses and tracks cumulative performance."""

    def evaluate_response(
        self,
        question: str,
        answer: str,
        topic_title: str,
        experience_level: str,
    ) -> float:
        """
        Score a single candidate response.

        Args:
            question: The question that was asked.
            answer: The candidate's response.
            topic_title: The topic being assessed.
            experience_level: Expected competency level.

        Returns:
            Score between 0.0 and 1.0.
        """
        # TODO: Replace with LLM-based evaluation
        # Stub: score based on response length and basic heuristics
        if not answer or not answer.strip():
            return 0.0

        word_count = len(answer.split())
        if word_count < 10:
            return 0.2
        elif word_count < 30:
            return 0.5
        elif word_count < 80:
            return 0.7
        else:
            return 0.85

    def calculate_topic_score(self, records: list[QuestionRecord]) -> dict:
        """
        Calculate aggregate scores per topic.

        Returns:
            Dict mapping topic title to average score.
        """
        topic_scores: dict[str, list[float]] = {}
        for record in records:
            if record.score is not None:
                if record.topic not in topic_scores:
                    topic_scores[record.topic] = []
                topic_scores[record.topic].append(record.score)

        return {
            topic: sum(scores) / len(scores)
            for topic, scores in topic_scores.items()
            if scores
        }

    def calculate_overall_score(self, records: list[QuestionRecord]) -> float:
        """Calculate the overall interview score."""
        scores = [r.score for r in records if r.score is not None]
        if not scores:
            return 0.0
        return sum(scores) / len(scores)
