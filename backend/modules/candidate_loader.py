from __future__ import annotations
"""
Candidate Loader module.

Responsibility:
    Load candidate data from the JSON file.
    Validate and normalize candidate profiles.
    Expose typed models.

    This module contains NO interview logic.
    It is a pure data access layer.
"""

import json
from typing import Optional

from models.schemas import CandidateProfile
from config import CANDIDATES_PATH


class CandidateLoader:
    """Loads and provides typed access to candidate profiles."""

    def __init__(self, path: str = CANDIDATES_PATH):
        self._path = path
        self._candidates: Optional[list[CandidateProfile]] = None
        self._index: Optional[dict[str, CandidateProfile]] = None

    def _load(self) -> None:
        """Load and parse the candidates JSON file. Called lazily."""
        with open(self._path, "r", encoding="utf-8") as f:
            raw = json.load(f)

        candidates_raw = raw.get("candidates", raw if isinstance(raw, list) else [])
        self._candidates = [CandidateProfile(**c) for c in candidates_raw]
        self._index = {c.member.id: c for c in self._candidates}

    @property
    def candidates(self) -> list[CandidateProfile]:
        """All loaded candidate profiles."""
        if self._candidates is None:
            self._load()
        return self._candidates  # type: ignore

    @property
    def index(self) -> dict[str, CandidateProfile]:
        """Candidates indexed by member ID."""
        if self._index is None:
            self._load()
        return self._index  # type: ignore

    def get_by_id(self, candidate_id: str) -> CandidateProfile:
        """
        Retrieve a single candidate by their member ID.

        Raises:
            KeyError: If no candidate exists with the given ID.
        """
        candidate = self.index.get(candidate_id)
        if candidate is None:
            raise KeyError(f"Candidate '{candidate_id}' not found")
        return candidate

    def exists(self, candidate_id: str) -> bool:
        """Check if a candidate exists in the dataset."""
        return candidate_id in self.index

    def list_ids(self) -> list[str]:
        """Return all available candidate IDs."""
        return list(self.index.keys())

    def validate_candidate(self, candidate: CandidateProfile) -> list[str]:
        """
        Validate a candidate profile for completeness.

        Returns:
            List of validation warnings (empty = valid).
        """
        warnings: list[str] = []

        if not candidate.member.id:
            warnings.append("Missing member.id")
        if not candidate.member.name:
            warnings.append("Missing member.name")
        if not candidate.missions:
            warnings.append("No missions found — interview will have limited data")
        if candidate.signals.missionsCompleted < 0:
            warnings.append("missionsCompleted is negative")
        if candidate.signals.commitDays < 0:
            warnings.append("commitDays is negative")

        return warnings
