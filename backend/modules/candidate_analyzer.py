from __future__ import annotations
"""
Candidate Analyzer module.

Responsibility:
    Deterministic analysis of a candidate profile using supplied JSON data.
    No AI. No prompts. No LLM.

    Generates strongly-typed CandidateAnalysis with:
    - strengths, weaknesses, skipped, completed, struggled topics
    - confidence score
    - recommended difficulty
    - recommended starting topic
    - reasoning trail
"""

from models.schemas import (
    CandidateProfile,
    CandidateAnalysis,
    TopicInsight,
    MissionStatus,
    ExperienceLevel,
    Difficulty,
)
from modules.curriculum_loader import CurriculumLoader


class CandidateAnalyzer:
    """Deterministic analysis of a candidate profile. Zero AI dependency."""

    def __init__(self, curriculum_loader: CurriculumLoader):
        self._curriculum = curriculum_loader

    def analyze(self, candidate: CandidateProfile) -> CandidateAnalysis:
        """
        Analyze the candidate's profile and produce a CandidateAnalysis.

        The analysis is entirely deterministic — it examines:
        - Which missions were passed, skipped, failed, or struggled
        - Aggregate signals (commit days, first-try rate)
        - Experience level derived from years of experience
        - Curriculum days the candidate never attempted

        Returns:
            CandidateAnalysis — strongly typed, reusable by downstream modules.
        """
        experience_level = self._derive_experience_level(candidate.member.yearsExperience)

        # Classify every mission the candidate engaged with
        strengths: list[TopicInsight] = []
        weaknesses: list[TopicInsight] = []
        skipped_topics: list[TopicInsight] = []
        completed_topics: list[TopicInsight] = []
        struggled_topics: list[TopicInsight] = []
        engaged_days: set[int] = set()

        for mission in candidate.missions:
            day_num = mission.day
            engaged_days.add(day_num)
            module_name = self._curriculum.get_module_name_for_day(day_num)

            status = self._classify_mission(mission)
            insight = TopicInsight(
                day=day_num,
                title=mission.title,
                status=status,
                attempts=mission.attempts,
                module_name=module_name,
            )

            if status == MissionStatus.SKIPPED:
                skipped_topics.append(insight)
            elif status == MissionStatus.FAILED:
                weaknesses.append(insight)
            elif status == MissionStatus.STRUGGLED:
                struggled_topics.append(insight)
                completed_topics.append(insight)
            elif status in (MissionStatus.PASSED, MissionStatus.PASSED_FIRST_TRY):
                completed_topics.append(insight)
                if status == MissionStatus.PASSED_FIRST_TRY:
                    strengths.append(insight)

        # Find curriculum days the candidate never attempted
        not_attempted: list[TopicInsight] = []
        for day_num in self._curriculum.list_all_days():
            if day_num not in engaged_days:
                day_obj = self._curriculum.get_day(day_num)
                if day_obj:
                    module_name = self._curriculum.get_module_name_for_day(day_num)
                    not_attempted.append(TopicInsight(
                        day=day_num,
                        title=day_obj.title,
                        status=MissionStatus.NOT_ATTEMPTED,
                        module_name=module_name,
                    ))

        # Compute rates
        total_curriculum_days = self._curriculum.total_days()
        missions_completed = candidate.signals.missionsCompleted
        first_try = candidate.signals.missionsFirstTry

        completion_rate = missions_completed / max(total_curriculum_days, 1)
        first_try_rate = first_try / max(missions_completed, 1)

        # Confidence score: weighted composite
        confidence = self._compute_confidence(
            completion_rate=completion_rate,
            first_try_rate=first_try_rate,
            commit_ratio=candidate.signals.commitDays / max(total_curriculum_days, 1),
            struggled_count=len(struggled_topics),
            skipped_count=len(skipped_topics),
            not_attempted_count=len(not_attempted),
        )

        # Recommended difficulty
        recommended_difficulty = self._recommend_difficulty(experience_level, confidence)

        # Recommended starting topic — pick highest-priority gap
        recommended_starting = self._recommend_starting_topic(
            skipped_topics, weaknesses, struggled_topics, not_attempted
        )

        # Reasoning trail
        reasoning = self._build_reasoning(
            candidate, experience_level, completion_rate, first_try_rate,
            confidence, strengths, weaknesses, skipped_topics,
            struggled_topics, not_attempted,
        )

        return CandidateAnalysis(
            candidate_id=candidate.member.id,
            candidate_name=candidate.member.name,
            experience_level=experience_level,
            strengths=strengths,
            weaknesses=weaknesses,
            skipped_topics=skipped_topics,
            completed_topics=completed_topics,
            struggled_topics=struggled_topics,
            not_attempted_topics=not_attempted,
            completion_rate=round(completion_rate, 3),
            first_try_rate=round(first_try_rate, 3),
            confidence_score=round(confidence, 3),
            recommended_difficulty=recommended_difficulty,
            recommended_starting_topic=recommended_starting,
            reasoning=reasoning,
        )

    # ── Private helpers ──────────────────────────────────────────

    @staticmethod
    def _classify_mission(mission) -> MissionStatus:
        """Classify a single mission into a MissionStatus."""
        if mission.skipped:
            return MissionStatus.SKIPPED
        if mission.passed is False:
            return MissionStatus.FAILED
        if mission.passed and mission.attempts == 1:
            return MissionStatus.PASSED_FIRST_TRY
        if mission.passed and mission.attempts is not None and mission.attempts >= 3:
            return MissionStatus.STRUGGLED
        if mission.passed:
            return MissionStatus.PASSED
        return MissionStatus.NOT_ATTEMPTED

    @staticmethod
    def _derive_experience_level(years: int) -> ExperienceLevel:
        """Map years of experience to an ExperienceLevel enum."""
        if years <= 1:
            return ExperienceLevel.JUNIOR
        elif years <= 5:
            return ExperienceLevel.MID
        elif years <= 12:
            return ExperienceLevel.SENIOR
        return ExperienceLevel.EXPERT

    @staticmethod
    def _compute_confidence(
        completion_rate: float,
        first_try_rate: float,
        commit_ratio: float,
        struggled_count: int,
        skipped_count: int,
        not_attempted_count: int,
    ) -> float:
        """
        Compute a 0.0–1.0 confidence score.

        Weights:
            completion_rate:  40%
            first_try_rate:   25%
            commit_ratio:     15%
            penalties:        20% (struggled, skipped, not attempted)
        """
        base = (
            completion_rate * 0.40
            + first_try_rate * 0.25
            + commit_ratio * 0.15
        )
        # Penalty: each gap category deducts proportionally
        penalty_count = struggled_count + skipped_count * 2 + not_attempted_count
        penalty = min(penalty_count * 0.02, 0.20)  # cap at 20%
        return max(0.0, min(1.0, base + 0.20 - penalty))

    @staticmethod
    def _recommend_difficulty(
        experience: ExperienceLevel, confidence: float
    ) -> Difficulty:
        """Recommend starting difficulty based on experience + confidence."""
        if confidence < 0.3:
            return Difficulty.FOUNDATIONAL
        if experience == ExperienceLevel.JUNIOR:
            return Difficulty.FOUNDATIONAL if confidence < 0.5 else Difficulty.INTERMEDIATE
        if experience == ExperienceLevel.MID:
            return Difficulty.INTERMEDIATE
        if experience == ExperienceLevel.SENIOR:
            return Difficulty.INTERMEDIATE if confidence < 0.6 else Difficulty.ADVANCED
        # EXPERT
        return Difficulty.ADVANCED if confidence < 0.7 else Difficulty.EXPERT

    @staticmethod
    def _recommend_starting_topic(
        skipped: list[TopicInsight],
        weaknesses: list[TopicInsight],
        struggled: list[TopicInsight],
        not_attempted: list[TopicInsight],
    ) -> str | None:
        """Pick the best starting topic (highest-priority gap)."""
        # Priority order: skipped > failed > struggled > not attempted
        if skipped:
            return skipped[0].title
        if weaknesses:
            return weaknesses[0].title
        if struggled:
            return struggled[0].title
        if not_attempted:
            return not_attempted[0].title
        return None

    @staticmethod
    def _build_reasoning(
        candidate: CandidateProfile,
        experience: ExperienceLevel,
        completion_rate: float,
        first_try_rate: float,
        confidence: float,
        strengths: list[TopicInsight],
        weaknesses: list[TopicInsight],
        skipped: list[TopicInsight],
        struggled: list[TopicInsight],
        not_attempted: list[TopicInsight],
    ) -> list[str]:
        """Build a human-readable reasoning trail."""
        r: list[str] = []
        r.append(
            f"Candidate {candidate.member.name} ({candidate.member.jobRole}) "
            f"has {candidate.member.yearsExperience} years experience → {experience.value} level."
        )
        r.append(
            f"Curriculum completion: {completion_rate:.0%}, "
            f"first-try rate: {first_try_rate:.0%}, "
            f"confidence: {confidence:.0%}."
        )
        if strengths:
            r.append(f"Strengths ({len(strengths)}): {', '.join(s.title for s in strengths[:5])}.")
        if weaknesses:
            r.append(f"Weaknesses ({len(weaknesses)}): {', '.join(w.title for w in weaknesses[:5])}.")
        if skipped:
            r.append(f"Skipped ({len(skipped)}): {', '.join(s.title for s in skipped[:5])}.")
        if struggled:
            r.append(f"Struggled ({len(struggled)}): {', '.join(s.title for s in struggled[:5])}.")
        if not_attempted:
            r.append(f"Not attempted ({len(not_attempted)}): {', '.join(n.title for n in not_attempted[:5])}.")
        return r
