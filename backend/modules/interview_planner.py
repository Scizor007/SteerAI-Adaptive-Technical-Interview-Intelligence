"""
Interview Planner module.

Responsibility:
    Create a prioritized topic plan for the interview based on
    the candidate's profile analysis and the curriculum structure.
    Determines which topics to cover and in what order.
"""

import json
from models.schemas import CandidateProfile, TopicPlan, Curriculum
from config import CURRICULUM_PATH


class InterviewPlanner:
    """Creates an adaptive interview plan based on candidate analysis and curriculum."""

    def __init__(self):
        self._curriculum: Curriculum | None = None

    @property
    def curriculum(self) -> Curriculum:
        """Lazy-load curriculum data."""
        if self._curriculum is None:
            with open(CURRICULUM_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._curriculum = Curriculum(**data)
        return self._curriculum

    def create_plan(
        self,
        candidate: CandidateProfile,
        analysis: dict,
    ) -> list[TopicPlan]:
        """
        Generate a prioritized list of topics to cover in the interview.

        Strategy:
        1. HIGH priority — skipped and failed topics (biggest gaps)
        2. MEDIUM priority — struggled topics (passed but with difficulty)
        3. LOW priority — strong topics (verify depth, not just completion)

        Returns:
            Ordered list of TopicPlan objects.
        """
        plan: list[TopicPlan] = []
        day_lookup = {d.day: d for d in self.curriculum.days}
        module_lookup = self._build_module_lookup()

        # HIGH: skipped topics — candidate never engaged
        for title in analysis.get("skipped", []):
            day_obj = self._find_day_by_title(title)
            if day_obj:
                plan.append(TopicPlan(
                    day=day_obj.day,
                    title=day_obj.title,
                    module=module_lookup.get(day_obj.day, "Unknown"),
                    priority="high",
                    reason=f"Candidate skipped this topic entirely",
                ))

        # HIGH: failed topics — candidate attempted but did not pass
        for title in analysis.get("weaknesses", []):
            day_obj = self._find_day_by_title(title)
            if day_obj:
                plan.append(TopicPlan(
                    day=day_obj.day,
                    title=day_obj.title,
                    module=module_lookup.get(day_obj.day, "Unknown"),
                    priority="high",
                    reason=f"Candidate failed this topic",
                ))

        # MEDIUM: struggled topics — passed but with 3+ attempts
        for title in analysis.get("struggled", []):
            day_obj = self._find_day_by_title(title)
            if day_obj:
                plan.append(TopicPlan(
                    day=day_obj.day,
                    title=day_obj.title,
                    module=module_lookup.get(day_obj.day, "Unknown"),
                    priority="medium",
                    reason=f"Candidate struggled (multiple attempts)",
                ))

        # LOW: strong topics — sample a few to verify depth
        for title in analysis.get("strengths", [])[:3]:
            day_obj = self._find_day_by_title(title)
            if day_obj:
                plan.append(TopicPlan(
                    day=day_obj.day,
                    title=day_obj.title,
                    module=module_lookup.get(day_obj.day, "Unknown"),
                    priority="low",
                    reason=f"Verify depth — candidate passed first try",
                ))

        return plan

    def _build_module_lookup(self) -> dict[int, str]:
        """Map each day number to its module title."""
        lookup = {}
        for module in self.curriculum.modules:
            start, end = module.days
            for day in range(start, end + 1):
                lookup[day] = module.title
        return lookup

    def _find_day_by_title(self, title: str):
        """Find a curriculum day object by its title."""
        for day in self.curriculum.days:
            if day.title == title:
                return day
        return None
