from __future__ import annotations
"""
Curriculum Loader module.

Responsibility:
    Load the curriculum JSON.
    Index by day number.
    Index by topic/module.
    Expose learning objectives and tools used per day.

    This module contains NO business logic.
    It is a pure data access layer.
"""

import json
from typing import Optional

from models.schemas import Curriculum, DayObjective, Module
from config import CURRICULUM_PATH


class CurriculumLoader:
    """Loads and provides indexed access to the curriculum structure."""

    def __init__(self, path: str = CURRICULUM_PATH):
        self._path = path
        self._curriculum: Optional[Curriculum] = None
        self._day_index: Optional[dict[int, DayObjective]] = None
        self._title_index: Optional[dict[str, DayObjective]] = None
        self._day_to_module: Optional[dict[int, Module]] = None

    def _load(self) -> None:
        """Load and parse the curriculum JSON file. Called lazily."""
        with open(self._path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        self._curriculum = Curriculum(**raw)
        self._build_indices()

    def _build_indices(self) -> None:
        """Build lookup indices after loading."""
        assert self._curriculum is not None

        self._day_index = {d.day: d for d in self._curriculum.days}
        self._title_index = {d.title: d for d in self._curriculum.days}

        self._day_to_module = {}
        for module in self._curriculum.modules:
            start, end = module.days[0], module.days[-1]
            for day_num in range(start, end + 1):
                self._day_to_module[day_num] = module

    @property
    def curriculum(self) -> Curriculum:
        """The full curriculum object."""
        if self._curriculum is None:
            self._load()
        return self._curriculum  # type: ignore

    @property
    def day_index(self) -> dict[int, DayObjective]:
        """Days indexed by day number."""
        if self._day_index is None:
            self._load()
        return self._day_index  # type: ignore

    @property
    def title_index(self) -> dict[str, DayObjective]:
        """Days indexed by title string."""
        if self._title_index is None:
            self._load()
        return self._title_index  # type: ignore

    @property
    def day_to_module(self) -> dict[int, Module]:
        """Map day number → its parent Module."""
        if self._day_to_module is None:
            self._load()
        return self._day_to_module  # type: ignore

    # ── Query Methods ────────────────────────────────────────────

    def get_day(self, day_number: int) -> Optional[DayObjective]:
        """Get a curriculum day by its number."""
        return self.day_index.get(day_number)

    def get_day_by_title(self, title: str) -> Optional[DayObjective]:
        """Get a curriculum day by its title."""
        return self.title_index.get(title)

    def get_module_for_day(self, day_number: int) -> Optional[Module]:
        """Get the parent module for a given day number."""
        return self.day_to_module.get(day_number)

    def get_module_name_for_day(self, day_number: int) -> str:
        """Get the module title for a given day, or 'Unknown'."""
        module = self.get_module_for_day(day_number)
        return module.title if module else "Unknown"

    def get_objectives(self, day_number: int) -> list[str]:
        """Get learning objectives for a specific day."""
        day = self.get_day(day_number)
        return day.objectives if day else []

    def get_tools(self, day_number: int) -> list[str]:
        """Get tools used on a specific day."""
        day = self.get_day(day_number)
        return day.tools if day else []

    def list_all_days(self) -> list[int]:
        """Return all day numbers in order."""
        return sorted(self.day_index.keys())

    def list_all_modules(self) -> list[Module]:
        """Return all modules in order."""
        return self.curriculum.modules

    def total_days(self) -> int:
        """Total number of curriculum days."""
        return len(self.day_index)
