"""
Pydantic models for the interview API.
Matches the technical specification contract exactly.

This file contains:
  - Candidate Profile models (from candidates.json)
  - Curriculum models (from curriculum.json)
  - API Request / Response models
  - Internal interview state models
  - Analysis / Planning / Context output models

Compatible with Python 3.7+ via typing imports.
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field


# ────────────────────────────────────────────────────────────────
# Enums
# ────────────────────────────────────────────────────────────────

class Difficulty(str, Enum):
    """Question difficulty levels, ordered by increasing complexity."""
    FOUNDATIONAL = "foundational"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class ExperienceLevel(str, Enum):
    """Candidate experience tiers derived from years of experience."""
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    EXPERT = "expert"


class TopicPriority(str, Enum):
    """Priority for covering a topic in the interview plan."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class InterviewPhase(str, Enum):
    """Phases an interview session can be in."""
    INITIALIZING = "initializing"
    ASKING = "asking"
    LISTENING = "listening"
    EVALUATING = "evaluating"
    COMPLETE = "complete"


class AdaptiveDecision(str, Enum):
    """Adaptive decision types for interview flow."""
    NEXT_TOPIC = "next_topic"
    FOLLOW_UP = "follow_up"
    HARDER = "harder"
    SIMPLER = "simpler"
    END_INTERVIEW = "end_interview"


class MissionStatus(str, Enum):
    """Derived status of a single curriculum mission for a candidate."""
    PASSED = "passed"
    PASSED_FIRST_TRY = "passed_first_try"
    STRUGGLED = "struggled"
    FAILED = "failed"
    SKIPPED = "skipped"
    NOT_ATTEMPTED = "not_attempted"


# ────────────────────────────────────────────────────────────────
# Candidate Profile (from candidates.json)
# ────────────────────────────────────────────────────────────────

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
    missions: List[Mission]
    signals: Signals


# ────────────────────────────────────────────────────────────────
# Curriculum (from curriculum.json)
# ────────────────────────────────────────────────────────────────

class DayObjective(BaseModel):
    """A single day in the curriculum."""
    day: int
    title: str
    type: str
    tools: List[str]
    objectives: List[str]


class Module(BaseModel):
    """A curriculum module spanning multiple days."""
    n: int
    title: str
    days: List[int]


class Curriculum(BaseModel):
    """Full curriculum structure."""
    cohort: str
    modules: List[Module]
    days: List[DayObjective]


# ────────────────────────────────────────────────────────────────
# API Request / Response
# ────────────────────────────────────────────────────────────────

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
    strengths: List[str]
    gaps: List[str]
    next: List[str] = Field(alias="next")
    overall_score: float = 0.0
    accuracy: float = 0.0
    reasoning: float = 0.0
    depth: float = 0.0
    completeness: float = 0.0
    communication: float = 0.0
    confidence: float = 0.0
    topic_mastery: Dict[str, float] = Field(default_factory=dict)
    evidence: List[str] = Field(default_factory=list)
    interviewer_notes: List[str] = Field(default_factory=list)


class InterviewResponse(BaseModel):
    """Response body for POST /api/interview."""
    reply: str
    done: bool = False
    feedback: Optional[Feedback] = None


# ────────────────────────────────────────────────────────────────
# Candidate Analysis (output of CandidateAnalyzer)
# ────────────────────────────────────────────────────────────────

class TopicInsight(BaseModel):
    """Analysis of a candidate's performance on one curriculum topic."""
    day: int
    title: str
    status: MissionStatus
    attempts: Optional[int] = None
    module_name: str = ""


class CandidateAnalysis(BaseModel):
    """
    Complete deterministic analysis of a candidate profile.
    Produced by CandidateAnalyzer. Consumed by InterviewPlanner.
    """
    candidate_id: str
    candidate_name: str
    experience_level: ExperienceLevel
    strengths: List[TopicInsight] = []
    weaknesses: List[TopicInsight] = []
    skipped_topics: List[TopicInsight] = []
    completed_topics: List[TopicInsight] = []
    struggled_topics: List[TopicInsight] = []
    not_attempted_topics: List[TopicInsight] = []
    completion_rate: float = 0.0
    first_try_rate: float = 0.0
    confidence_score: float = 0.0
    recommended_difficulty: Difficulty = Difficulty.INTERMEDIATE
    recommended_starting_topic: Optional[str] = None
    reasoning: List[str] = []


# ────────────────────────────────────────────────────────────────
# Interview Plan (output of InterviewPlanner)
# ────────────────────────────────────────────────────────────────

class PlannedTopic(BaseModel):
    """A single topic scheduled for the interview, with metadata."""
    day: int
    title: str
    module_name: str
    priority: TopicPriority
    difficulty: Difficulty
    reason: str
    objectives: List[str] = []
    tools: List[str] = []


class InterviewPlan(BaseModel):
    """
    Deterministic interview plan produced by InterviewPlanner.
    Contains metadata only — no natural-language questions.
    """
    candidate_id: str
    planned_topics: List[PlannedTopic] = []
    total_planned_questions: int = 0
    unique_days_covered: int = 0
    unique_modules_covered: int = 0
    starting_difficulty: Difficulty = Difficulty.INTERMEDIATE
    reasoning: List[str] = []


# ────────────────────────────────────────────────────────────────
# Coverage & Progress (tracked across the session)
# ────────────────────────────────────────────────────────────────

class CoverageState(BaseModel):
    """Tracks which curriculum days and modules have been covered."""
    days_covered: List[int] = []
    modules_covered: List[str] = []
    topics_asked: List[str] = []


class InterviewProgress(BaseModel):
    """Tracks overall interview progression."""
    questions_asked: int = 0
    questions_remaining: int = 0
    current_topic_index: int = 0
    current_difficulty: Difficulty = Difficulty.INTERMEDIATE
    phase: InterviewPhase = InterviewPhase.INITIALIZING


# ────────────────────────────────────────────────────────────────
# Question Record (kept per asked question)
# ────────────────────────────────────────────────────────────────

class QuestionRecord(BaseModel):
    """Record of a question asked and the candidate's response."""
    topic: str
    question: str
    difficulty: Difficulty = Difficulty.INTERMEDIATE
    expected_points: List[str] = Field(default_factory=list)
    answer: Optional[str] = None
    score: Optional[float] = None
    followup_count: int = 0


class GeneratedQuestion(BaseModel):
    """LLM-generated question metadata retained for answer evaluation."""
    question: str
    expected_points: List[str] = Field(default_factory=list)
    estimated_difficulty: Difficulty = Difficulty.INTERMEDIATE


class EvaluationResult(BaseModel):
    """Normalized, evidence-based evaluation for one submitted answer."""
    accuracy: float = Field(default=0.0, ge=0.0, le=10.0)
    reasoning: float = Field(default=0.0, ge=0.0, le=10.0)
    depth: float = Field(default=0.0, ge=0.0, le=10.0)
    completeness: float = Field(default=0.0, ge=0.0, le=10.0)
    communication: float = Field(default=0.0, ge=0.0, le=10.0)
    confidence: float = Field(default=0.0, ge=0.0, le=10.0)
    overall: float = Field(default=0.0, ge=0.0, le=10.0)
    strengths: List[str] = Field(default_factory=list)
    missing_points: List[str] = Field(default_factory=list)
    misconceptions: List[str] = Field(default_factory=list)
    suggested_followup: Optional[str] = None
    topic_mastery: str = "Low"
    interviewer_notes: str = ""
    needs_followup: bool = False
    difficulty_recommendation: str = "maintain"
    knowledge_gap: Optional[str] = None


class EvaluationEvidence(BaseModel):
    """Immutable evidence captured for each candidate answer in a session."""
    question: str
    topic: str
    candidate_answer: str
    expected_points: List[str] = Field(default_factory=list)
    evaluation_result: EvaluationResult
    timestamp: str


class InterviewScoreSummary(BaseModel):
    """Accumulated evidence-based interview dimensions, normalized to 0-100."""
    overall_score: float = 0.0
    accuracy: float = 0.0
    reasoning: float = 0.0
    depth: float = 0.0
    completeness: float = 0.0
    communication: float = 0.0
    confidence: float = 0.0
    coverage_bonus: float = 0.0
    consistency_bonus: float = 0.0


class AdaptiveDecisionResult(BaseModel):
    """Result from the adaptive decision engine."""
    decision: AdaptiveDecision
    reason: str
    target_topic: Optional[str] = None
    difficulty: Difficulty = Difficulty.INTERMEDIATE


# ────────────────────────────────────────────────────────────────
# Interview State (persisted in SessionManager)
# ────────────────────────────────────────────────────────────────

# Keep the original TopicPlan for backward-compat with existing stubs
class TopicPlan(BaseModel):
    """A planned interview topic with its priority (legacy compat)."""
    day: int
    title: str
    module: str
    priority: str  # "high" | "medium" | "low"
    reason: str


class InterviewState(BaseModel):
    """Complete state for an active interview session."""
    session_id: str
    candidate: CandidateProfile
    analysis: Optional[CandidateAnalysis] = None
    plan: Optional[InterviewPlan] = None
    topic_plan: List[TopicPlan] = []  # legacy compat
    current_topic_index: int = 0
    questions_asked: List[QuestionRecord] = []
    evaluations: List[EvaluationEvidence] = Field(default_factory=list)
    topic_mastery: Dict[str, float] = Field(default_factory=dict)
    conversation_history: List[Dict[str, Any]] = []
    phase: str = "initializing"
    total_questions: int = 0
    max_questions: int = 10
    coverage: CoverageState = Field(default_factory=CoverageState)
    progress: InterviewProgress = Field(default_factory=InterviewProgress)


# ────────────────────────────────────────────────────────────────
# Interview Context (built by InterviewContextBuilder)
# ────────────────────────────────────────────────────────────────

class InterviewContext(BaseModel):
    """
    Single object merging all information needed by downstream modules.
    Every future module (QuestionGenerator, EvaluationEngine, etc.)
    should consume this instead of querying multiple services.
    """
    session_id: str
    candidate: CandidateProfile
    analysis: CandidateAnalysis
    plan: InterviewPlan
    progress: InterviewProgress
    coverage: CoverageState
    questions_asked: List[QuestionRecord] = []
    evaluations: List[EvaluationEvidence] = Field(default_factory=list)
    topic_mastery: Dict[str, float] = Field(default_factory=dict)
    conversation_history: List[Dict[str, Any]] = []
    current_topic: Optional[PlannedTopic] = None
    current_difficulty: Difficulty = Difficulty.INTERMEDIATE
