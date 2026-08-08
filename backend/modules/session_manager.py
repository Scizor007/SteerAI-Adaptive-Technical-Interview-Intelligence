from __future__ import annotations
"""
Session Manager module.

Responsibility:
    In-memory session store keyed by sessionId.
    Creates, retrieves, updates, and deletes interview state.
    Tracks interview progress, stores previous answers,
    asked questions, curriculum coverage, and interview state.

    No database — sessions live for the process lifetime.
"""

from models.schemas import (
    InterviewState,
    CandidateProfile,
    CandidateAnalysis,
    InterviewPlan,
    CoverageState,
    InterviewProgress,
)
from pydantic import Field


class SessionManager:
    """Manages in-memory interview sessions."""

    def __init__(self):
        self._sessions: dict[str, InterviewState] = {}

    def create_session(
        self,
        session_id: str,
        candidate: CandidateProfile,
        analysis: CandidateAnalysis,
        plan: InterviewPlan,
        max_questions: int = 10,
    ) -> InterviewState:
        """
        Create a new interview session with analysis and plan pre-attached.

        Args:
            session_id: Unique session identifier from the client.
            candidate: The candidate's full profile.
            analysis: Deterministic candidate analysis.
            plan: Deterministic interview plan.
            max_questions: Maximum questions for this interview.

        Returns:
            The newly created InterviewState.

        Raises:
            ValueError: If session already exists.
        """
        if session_id in self._sessions:
            raise ValueError(f"Session '{session_id}' already exists")

        state = InterviewState(
            session_id=session_id,
            candidate=candidate,
            analysis=analysis,
            plan=plan,
            max_questions=max_questions,
            phase="initializing",
        )
        self._sessions[session_id] = state
        return state

    def get_session(self, session_id: str) -> InterviewState:
        """
        Retrieve an existing session.

        Raises:
            KeyError: If session does not exist.
        """
        if session_id not in self._sessions:
            raise KeyError(f"Session '{session_id}' not found")
        return self._sessions[session_id]

    def update_session(self, session_id: str, state: InterviewState) -> None:
        """Update the state of an existing session."""
        self._sessions[session_id] = state

    def delete_session(self, session_id: str) -> None:
        """Remove a session (e.g., after interview completion)."""
        self._sessions.pop(session_id, None)

    def list_sessions(self) -> list[str]:
        """List all active session IDs."""
        return list(self._sessions.keys())

    def session_exists(self, session_id: str) -> bool:
        """Check if a session exists."""
        return session_id in self._sessions

    def get_session_count(self) -> int:
        """Return the number of active sessions."""
        return len(self._sessions)
