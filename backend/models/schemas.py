"""
Pydantic models for the interview API.
Matches the technical specification contract exactly.
"""

from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field


# --- Candidate Profile ---

class Mission(BaseModel):
    """A single curriculum mission completed (or skipped) by a candidate."""
    day: int
    title: str
    passed: Optional[bool] = None
    skipped: Optional[bool] = None
    attempts: Optional[int] = None


class Signals(BaseModel):
    """Aggregate performance signals for a candidate."""
    commitDays: int
    missionsCompleted: int
    missionsFirstTry: int


class Member(BaseModel):
    """Core candidate identity."""
    id: str
    name: str
    jobRole: str
    yearsExperience: int
    education: str
    status: str


class CandidateProfile(BaseModel):
    """Full candidate profile as supplied in candidates.json."""
    member: Member
    missions: list[Mission]
    signals: Signals


# --- API Request / Response ---

class InterviewRequest(BaseModel):
    """
    Unified request body for POST /api/interview.
    - Start: sessionId + candidate (no message)
    - Continue: sessionId + message (no candidate)
    """
    sessionId: str
    candidate: Optional[CandidateProfile] = None
    message: Optional[str] = None


class Feedback(BaseModel):
    """Structured feedback returned when the interview ends."""
    summary: str
    strengths: list[str]
    gaps: list[str]
    next: list[str] = Field(alias="next")


class InterviewResponse(BaseModel):
    """Response body for POST /api/interview."""
    reply: str
    done: bool = False
    feedback: Optional[Feedback] = None


# --- Curriculum ---

class DayObjective(BaseModel):
    """A single day in the curriculum."""
    day: int
    title: str
    type: str
    tools: list[str]
    objectives: list[str]


class Module(BaseModel):
    """A curriculum module spanning multiple days."""
    n: int
    title: str
    days: list[int]


class Curriculum(BaseModel):
    """Full curriculum structure."""
    cohort: str
    modules: list[Module]
    days: list[DayObjective]


# --- Interview State (internal) ---

class TopicPlan(BaseModel):
    """A planned interview topic with its priority."""
    day: int
    title: str
    module: str
    priority: str  # "high" | "medium" | "low"
    reason: str


class QuestionRecord(BaseModel):
    """Record of a question asked and the candidate's response."""
    topic: str
    question: str
    answer: Optional[str] = None
    score: Optional[float] = None
    followup_count: int = 0


class InterviewState(BaseModel):
    """Complete state for an active interview session."""
    session_id: str
    candidate: CandidateProfile
    topic_plan: list[TopicPlan] = []
    current_topic_index: int = 0
    questions_asked: list[QuestionRecord] = []
    conversation_history: list[dict] = []
    phase: str = "initializing"  # initializing | asking | listening | evaluating | complete
    total_questions: int = 0
    max_questions: int = 10
