from __future__ import annotations
"""
Interview Planner module.

Responsibility:
    Build a deterministic InterviewPlan from CandidateAnalysis + Curriculum.
    No AI. No prompts. No LLM.

    Rules:
    - Minimum 8 questions planned
    - Minimum 4 unique curriculum days
    - Avoid consecutive duplicate topics
    - Start at medium difficulty
    - Increase difficulty gradually
    - Prioritize weak areas
    - Do not revisit mastered topics unless verification is needed
    - Returns metadata only — no natural-language questions
"""

from models.schemas import (
    CandidateAnalysis,
    InterviewPlan,
    PlannedTopic,
    TopicInsight,
    TopicPriority,
    Difficulty,
)
from modules.curriculum_loader import CurriculumLoader


# ── Constants ────────────────────────────────────────────────────

MIN_PLANNED_QUESTIONS = 8
MIN_UNIQUE_DAYS = 4
MAX_STRENGTH_VERIFICATION = 3  # max strength topics to include for verification

DIFFICULTY_LADDER = [
    Difficulty.FOUNDATIONAL,
    Difficulty.INTERMEDIATE,
    Difficulty.ADVANCED,
    Difficulty.EXPERT,
]


class InterviewPlanner:
    """Creates deterministic interview plans. Zero AI dependency."""

    def __init__(self, curriculum_loader: CurriculumLoader):
        self._curriculum = curriculum_loader

    def create_plan(self, analysis: CandidateAnalysis) -> InterviewPlan:
        """
        Generate an InterviewPlan from a CandidateAnalysis.

        Strategy:
            1. HIGH priority — skipped topics (biggest gaps)
            2. HIGH priority — failed topics (weaknesses)
            3. MEDIUM priority — struggled topics (passed with difficulty)
            4. MEDIUM priority — not-attempted topics (unknown territory)
            5. LOW priority — sample strengths for depth verification

        Then:
            - Deduplicate
            - Ensure minimum 4 unique days
            - Ensure minimum 8 planned questions
            - Order to avoid consecutive duplicate modules
            - Apply gradual difficulty escalation
        """
        reasoning: list[str] = []
        topics: list[PlannedTopic] = []
        seen_days: set[int] = set()

        starting_difficulty = analysis.recommended_difficulty

        # 1. Skipped topics → HIGH
        for insight in analysis.skipped_topics:
            topic = self._insight_to_planned(insight, TopicPriority.HIGH, starting_difficulty,
                                              "Candidate skipped this topic entirely")
            if topic and topic.day not in seen_days:
                topics.append(topic)
                seen_days.add(topic.day)

        # 2. Failed topics → HIGH
        for insight in analysis.weaknesses:
            topic = self._insight_to_planned(insight, TopicPriority.HIGH, starting_difficulty,
                                              "Candidate failed this topic")
            if topic and topic.day not in seen_days:
                topics.append(topic)
                seen_days.add(topic.day)

        # 3. Struggled topics → MEDIUM
        for insight in analysis.struggled_topics:
            topic = self._insight_to_planned(insight, TopicPriority.MEDIUM,
                                              self._step_up(starting_difficulty),
                                              f"Candidate struggled ({insight.attempts} attempts)")
            if topic and topic.day not in seen_days:
                topics.append(topic)
                seen_days.add(topic.day)

        # 4. Not-attempted topics → MEDIUM (fill coverage gaps)
        for insight in analysis.not_attempted_topics:
            topic = self._insight_to_planned(insight, TopicPriority.MEDIUM, starting_difficulty,
                                              "Candidate never attempted this topic")
            if topic and topic.day not in seen_days:
                topics.append(topic)
                seen_days.add(topic.day)
                # Stop adding once we have enough
                if len(topics) >= MIN_PLANNED_QUESTIONS:
                    break

        # 5. Strength verification → LOW (sample up to MAX_STRENGTH_VERIFICATION)
        verified = 0
        for insight in analysis.strengths:
            if verified >= MAX_STRENGTH_VERIFICATION:
                break
            topic = self._insight_to_planned(insight, TopicPriority.LOW,
                                              self._step_up(self._step_up(starting_difficulty)),
                                              "Verify depth — candidate passed first try")
            if topic and topic.day not in seen_days:
                topics.append(topic)
                seen_days.add(topic.day)
                verified += 1

        # Ensure minimum unique days
        if len(seen_days) < MIN_UNIQUE_DAYS:
            topics = self._fill_coverage_gaps(topics, seen_days, analysis, starting_difficulty)
            reasoning.append(f"Added extra topics to meet minimum {MIN_UNIQUE_DAYS} unique days")

        # Ensure minimum planned questions
        if len(topics) < MIN_PLANNED_QUESTIONS:
            topics = self._fill_to_minimum(topics, seen_days, analysis, starting_difficulty)
            reasoning.append(f"Added extra topics to meet minimum {MIN_PLANNED_QUESTIONS} questions")

        # Reorder to avoid consecutive duplicate modules
        topics = self._interleave_modules(topics)

        # Apply gradual difficulty escalation
        topics = self._apply_difficulty_ladder(topics, starting_difficulty)

        # Build reasoning
        reasoning.insert(0,
            f"Starting difficulty: {starting_difficulty.value}. "
            f"Planned {len(topics)} topics across {len(seen_days)} unique days."
        )
        reasoning.append(
            f"Priority breakdown: "
            f"{sum(1 for t in topics if t.priority == TopicPriority.HIGH)} HIGH, "
            f"{sum(1 for t in topics if t.priority == TopicPriority.MEDIUM)} MEDIUM, "
            f"{sum(1 for t in topics if t.priority == TopicPriority.LOW)} LOW."
        )

        unique_modules = {t.module_name for t in topics}

        return InterviewPlan(
            candidate_id=analysis.candidate_id,
            planned_topics=topics,
            total_planned_questions=len(topics),
            unique_days_covered=len(seen_days),
            unique_modules_covered=len(unique_modules),
            starting_difficulty=starting_difficulty,
            reasoning=reasoning,
        )

    # ── Private helpers ──────────────────────────────────────────

    def _insight_to_planned(
        self,
        insight: TopicInsight,
        priority: TopicPriority,
        difficulty: Difficulty,
        reason: str,
    ) -> PlannedTopic | None:
        """Convert a TopicInsight into a PlannedTopic with curriculum enrichment."""
        day_obj = self._curriculum.get_day(insight.day)
        if day_obj is None:
            day_obj = self._curriculum.get_day_by_title(insight.title)
        if day_obj is None:
            return None

        module_name = self._curriculum.get_module_name_for_day(day_obj.day)

        return PlannedTopic(
            day=day_obj.day,
            title=day_obj.title,
            module_name=module_name,
            priority=priority,
            difficulty=difficulty,
            reason=reason,
            objectives=day_obj.objectives,
            tools=day_obj.tools,
        )

    def _fill_coverage_gaps(
        self,
        topics: list[PlannedTopic],
        seen_days: set[int],
        analysis: CandidateAnalysis,
        difficulty: Difficulty,
    ) -> list[PlannedTopic]:
        """Add topics from uncovered modules to meet minimum day coverage."""
        all_days = self._curriculum.list_all_days()
        for day_num in all_days:
            if len(seen_days) >= MIN_UNIQUE_DAYS:
                break
            if day_num in seen_days:
                continue
            day_obj = self._curriculum.get_day(day_num)
            if day_obj is None:
                continue
            module_name = self._curriculum.get_module_name_for_day(day_num)
            topics.append(PlannedTopic(
                day=day_num,
                title=day_obj.title,
                module_name=module_name,
                priority=TopicPriority.MEDIUM,
                difficulty=difficulty,
                reason="Added to meet minimum curriculum day coverage",
                objectives=day_obj.objectives,
                tools=day_obj.tools,
            ))
            seen_days.add(day_num)
        return topics

    def _fill_to_minimum(
        self,
        topics: list[PlannedTopic],
        seen_days: set[int],
        analysis: CandidateAnalysis,
        difficulty: Difficulty,
    ) -> list[PlannedTopic]:
        """Add more topics to reach the minimum question count."""
        # Pull from strengths we haven't used yet
        for insight in analysis.strengths:
            if len(topics) >= MIN_PLANNED_QUESTIONS:
                break
            if insight.day in seen_days:
                continue
            topic = self._insight_to_planned(
                insight, TopicPriority.LOW, self._step_up(difficulty),
                "Added to meet minimum question count (strength verification)"
            )
            if topic:
                topics.append(topic)
                seen_days.add(topic.day)

        # If still short, pull from completed topics
        for insight in analysis.completed_topics:
            if len(topics) >= MIN_PLANNED_QUESTIONS:
                break
            if insight.day in seen_days:
                continue
            topic = self._insight_to_planned(
                insight, TopicPriority.LOW, difficulty,
                "Added to meet minimum question count"
            )
            if topic:
                topics.append(topic)
                seen_days.add(topic.day)

        # If still short, pull from any curriculum days
        for day_num in self._curriculum.list_all_days():
            if len(topics) >= MIN_PLANNED_QUESTIONS:
                break
            if day_num in seen_days:
                continue
            day_obj = self._curriculum.get_day(day_num)
            if day_obj is None:
                continue
            module_name = self._curriculum.get_module_name_for_day(day_num)
            topics.append(PlannedTopic(
                day=day_num,
                title=day_obj.title,
                module_name=module_name,
                priority=TopicPriority.LOW,
                difficulty=difficulty,
                reason="Added to meet minimum question count (curriculum fill)",
                objectives=day_obj.objectives,
                tools=day_obj.tools,
            ))
            seen_days.add(day_num)

        return topics

    @staticmethod
    def _interleave_modules(topics: list[PlannedTopic]) -> list[PlannedTopic]:
        """
        Reorder topics to avoid consecutive topics from the same module.
        Uses a greedy approach: always pick the highest-priority topic
        whose module differs from the previous one.
        """
        if len(topics) <= 1:
            return topics

        # Sort by priority (HIGH first) then day
        priority_order = {TopicPriority.HIGH: 0, TopicPriority.MEDIUM: 1, TopicPriority.LOW: 2}
        remaining = sorted(topics, key=lambda t: (priority_order[t.priority], t.day))
        result: list[PlannedTopic] = []

        while remaining:
            placed = False
            for i, topic in enumerate(remaining):
                if not result or topic.module_name != result[-1].module_name:
                    result.append(remaining.pop(i))
                    placed = True
                    break
            if not placed:
                # No non-duplicate available; just take the first one
                result.append(remaining.pop(0))

        return result

    @staticmethod
    def _apply_difficulty_ladder(
        topics: list[PlannedTopic], starting: Difficulty
    ) -> list[PlannedTopic]:
        """
        Apply gradual difficulty escalation across the topic sequence.

        First third: starting difficulty
        Second third: one step up
        Final third: two steps up (capped at EXPERT)
        """
        if not topics:
            return topics

        start_idx = DIFFICULTY_LADDER.index(starting)
        total = len(topics)
        third = max(total // 3, 1)

        for i, topic in enumerate(topics):
            if topic.priority == TopicPriority.HIGH:
                # HIGH priority topics start at starting difficulty (gaps = fundamentals)
                topic.difficulty = starting
            elif i < third:
                topic.difficulty = DIFFICULTY_LADDER[min(start_idx, len(DIFFICULTY_LADDER) - 1)]
            elif i < 2 * third:
                topic.difficulty = DIFFICULTY_LADDER[min(start_idx + 1, len(DIFFICULTY_LADDER) - 1)]
            else:
                topic.difficulty = DIFFICULTY_LADDER[min(start_idx + 2, len(DIFFICULTY_LADDER) - 1)]

        return topics

    @staticmethod
    def _step_up(difficulty: Difficulty) -> Difficulty:
        """Move one step up on the difficulty ladder, capped at EXPERT."""
        idx = DIFFICULTY_LADDER.index(difficulty)
        return DIFFICULTY_LADDER[min(idx + 1, len(DIFFICULTY_LADDER) - 1)]
