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


class FeedbackGenerator:
    """Generates structured interview feedback from evaluation results."""

    def generate(
        self,
        candidate: CandidateProfile,
        questions: list[QuestionRecord],
        topic_plan: list[TopicPlan],
        topic_scores: dict[str, float],
        overall_score: float,
    ) -> Feedback:
        """
        Generate final structured feedback.

        Args:
            candidate: The candidate's profile.
            questions: All question records from the interview.
            topic_plan: The planned topics.
            topic_scores: Per-topic average scores.
            overall_score: Overall interview score.

        Returns:
            Feedback object matching the technical specification.
        """
        # TODO: Replace with LLM-powered feedback synthesis
        strengths = [
            f"Strong understanding of {topic}"
            for topic, score in topic_scores.items()
            if score >= 0.7
        ]

        gaps = [
            f"Needs improvement in {topic}"
            for topic, score in topic_scores.items()
            if score < 0.5
        ]

        # Add skipped topics as gaps
        skipped_titles = {
            tp.title for tp in topic_plan if tp.priority == "high"
        }
        covered_titles = set(topic_scores.keys())
        uncovered = skipped_titles - covered_titles
        for title in uncovered:
            gaps.append(f"Topic not covered: {title}")

        next_steps = self._generate_next_steps(gaps, candidate)

        score_pct = round(overall_score * 100)
        summary = (
            f"Interview completed for {candidate.member.name} "
            f"({candidate.member.jobRole}). "
            f"Overall performance: {score_pct}%. "
            f"Covered {len(topic_scores)} topics across the curriculum."
        )

        return Feedback(
            summary=summary,
            strengths=strengths if strengths else ["Candidate showed willingness to engage with topics"],
            gaps=gaps if gaps else ["No significant gaps identified"],
            next=next_steps,
        )

    def _generate_next_steps(
        self,
        gaps: list[str],
        candidate: CandidateProfile,
    ) -> list[str]:
        """Generate actionable next steps based on identified gaps."""
        # TODO: Replace with LLM-powered recommendations
        steps = []
        if gaps:
            steps.append("Review and practice the topics identified as gaps")
            steps.append("Work through the curriculum exercises for weak areas")
        steps.append("Continue building projects to reinforce practical skills")
        return steps
