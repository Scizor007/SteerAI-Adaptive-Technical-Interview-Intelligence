"""
Candidate Analyzer module.

Responsibility:
    Parse a candidate profile and extract actionable signals for interview planning.
    Identifies strengths, weaknesses, skipped topics, struggled topics,
    and overall readiness level.
"""

from models.schemas import CandidateProfile


class CandidateAnalyzer:
    """Analyzes a candidate profile to extract interview-relevant insights."""

    def analyze(self, candidate: CandidateProfile) -> dict:
        """
        Analyze the candidate's profile and return structured insights.

        Returns:
            dict with keys:
                - strengths: list[str] — topics mastered (passed first try)
                - weaknesses: list[str] — topics with many attempts or failed
                - skipped: list[str] — topics the candidate skipped entirely
                - struggled: list[str] — topics passed but with 3+ attempts
                - experience_level: str — "junior" | "mid" | "senior" | "expert"
                - completion_rate: float — missions completed / total available
                - first_try_rate: float — first-try passes / missions completed
        """
        strengths = []
        weaknesses = []
        skipped = []
        struggled = []

        for mission in candidate.missions:
            if mission.skipped:
                skipped.append(mission.title)
            elif mission.passed is False:
                weaknesses.append(mission.title)
            elif mission.passed and mission.attempts == 1:
                strengths.append(mission.title)
            elif mission.passed and mission.attempts is not None and mission.attempts >= 3:
                struggled.append(mission.title)

        years = candidate.member.yearsExperience
        if years == 0:
            experience_level = "junior"
        elif years <= 5:
            experience_level = "mid"
        elif years <= 12:
            experience_level = "senior"
        else:
            experience_level = "expert"

        total_missions = len(candidate.missions)
        completed = candidate.signals.missionsCompleted
        first_try = candidate.signals.missionsFirstTry

        return {
            "strengths": strengths,
            "weaknesses": weaknesses,
            "skipped": skipped,
            "struggled": struggled,
            "experience_level": experience_level,
            "completion_rate": completed / max(total_missions, 1),
            "first_try_rate": first_try / max(completed, 1),
        }
