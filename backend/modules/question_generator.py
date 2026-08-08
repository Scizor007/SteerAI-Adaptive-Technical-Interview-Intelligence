from __future__ import annotations
"""
Question Generator module.

Responsibility:
    Generate adaptive interview questions for a given topic,
    calibrated to the candidate's experience level and the
    topic's priority in the interview plan.
"""

from models.schemas import CandidateProfile


class QuestionGenerator:
    """Generates contextual interview questions based on topic and candidate profile."""

    def generate(
        self,
        topic,  # PlannedTopic or TopicPlan — duck-typed on .title / .priority
        candidate: CandidateProfile,
        experience_level: str,
        questions_already_asked: list[str],
    ) -> str:
        """
        Generate a single interview question for the given topic.

        The question difficulty and framing adapt based on:
        - The topic's priority (high = fundamental, low = depth-check)
        - The candidate's experience level
        - Previously asked questions (avoid repetition)

        Args:
            topic: The current topic plan entry.
            candidate: Full candidate profile.
            experience_level: "junior" | "mid" | "senior" | "expert"
            questions_already_asked: List of previously asked question texts.

        Returns:
            A question string to present to the candidate.
        """
        # TODO: Replace with LLM-powered question generation
        # This stub returns a template-based question for scaffolding validation
        priority = topic.priority.value if hasattr(topic.priority, 'value') else topic.priority
        difficulty = self._map_difficulty(priority, experience_level)

        return (
            f"Regarding {topic.title}: "
            f"Can you explain your understanding of this topic "
            f"and how you would apply it in a real-world scenario? "
            f"[Difficulty: {difficulty}]"
        )

    def _map_difficulty(self, priority: str, experience_level: str) -> str:
        """Map topic priority + experience to question difficulty."""
        if priority == "high":
            # Gap topic — start with fundamentals regardless of experience
            return "foundational"
        elif priority == "medium":
            # Struggled topic — match to experience
            level_map = {
                "junior": "intermediate",
                "mid": "intermediate",
                "senior": "advanced",
                "expert": "advanced",
            }
            return level_map.get(experience_level, "intermediate")
        else:
            # Strong topic — push deeper
            level_map = {
                "junior": "intermediate",
                "mid": "advanced",
                "senior": "expert",
                "expert": "expert",
            }
            return level_map.get(experience_level, "advanced")
