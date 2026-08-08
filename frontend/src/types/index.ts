/**
 * TypeScript interfaces matching backend Pydantic schemas.
 * Single source of truth for frontend types.
 */

// --- Candidate Profile ---

export interface Mission {
  day: number;
  title: string;
  passed?: boolean;
  skipped?: boolean;
  attempts?: number;
}

export interface Signals {
  commitDays: number;
  missionsCompleted: number;
  missionsFirstTry: number;
}

export interface Member {
  id: string;
  name: string;
  jobRole: string;
  yearsExperience: number;
  education: string;
  status: string;
}

export interface CandidateProfile {
  member: Member;
  missions: Mission[];
  signals: Signals;
}

// --- API Request / Response ---

export interface InterviewStartRequest {
  sessionId: string;
  candidate: CandidateProfile;
}

export interface InterviewContinueRequest {
  sessionId: string;
  message: string;
}

export type InterviewRequest = InterviewStartRequest | InterviewContinueRequest;

export interface Feedback {
  summary: string;
  strengths: string[];
  gaps: string[];
  next: string[];
  overall_score: number;
  accuracy: number;
  reasoning: number;
  depth: number;
  completeness: number;
  communication: number;
  confidence: number;
  topic_mastery: Record<string, number>;
  evidence: string[];
  interviewer_notes: string[];
}

export interface InterviewResponse {
  reply: string;
  done: boolean;
  feedback?: Feedback;
}

// --- Curriculum ---

export interface DayObjective {
  day: number;
  title: string;
  type: string;
  tools: string[];
  objectives: string[];
}

export interface CurriculumModule {
  n: number;
  title: string;
  days: [number, number];
}

export interface Curriculum {
  cohort: string;
  modules: CurriculumModule[];
  days: DayObjective[];
}

// --- Interview State (frontend) ---

export type InterviewPhase =
  | 'idle'
  | 'initializing'
  | 'asking'
  | 'listening'
  | 'evaluating'
  | 'complete';

export interface ConversationMessage {
  role: 'interviewer' | 'candidate';
  content: string;
  timestamp: number;
}

export interface InterviewSession {
  sessionId: string;
  candidate: CandidateProfile;
  phase: InterviewPhase;
  messages: ConversationMessage[];
  feedback?: Feedback;
  currentTopic?: string;
  questionsAsked: number;
}

// --- Candidates Data ---

export interface CandidatesData {
  candidates: CandidateProfile[];
}
