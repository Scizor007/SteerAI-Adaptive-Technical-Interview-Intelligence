# DECISIONS.md — Architecture Decision Log

> Append-only. Each decision is final unless explicitly revisited.

---

## DEC-001: Modular Interview Architecture

- **Timestamp**: 2026-08-08
- **Problem**: How to structure the backend interview logic — monolithic controller vs modular system?
- **Chosen option**: Eight modules + Interview Manager orchestrator
- **Reason**: Maximizes maintainability, testability, and extensibility. Each module can be LLM-enhanced independently.

---

## DEC-002: Design Token System — Assessment Console Direction (REVISITED IN DEC-006)

- **Timestamp**: 2026-08-08
- **Problem**: Visual direction for the frontend.
- **Chosen option**: Assessment console with navy-charcoal base.
- **Note**: This was entirely superseded by DEC-006.

---

## DEC-003: Single API Endpoint Design

- **Timestamp**: 2026-08-08
- **Problem**: How to structure the API?
- **Chosen option**: Single `POST /api/interview` as specified in technical-spec.md. Phase detection via presence of `candidate` vs `message` field.

---

## DEC-004: In-Memory Session Storage

- **Timestamp**: 2026-08-08
- **Problem**: How to persist interview state between requests?
- **Chosen option**: In-memory dict in SessionManager. (No DB allowed per hackathon rules).

---

## DEC-005: Frontend Framework — Vite + React + TypeScript

- **Timestamp**: 2026-08-08
- **Problem**: Which frontend framework and build tool?
- **Chosen option**: Vite + React + TypeScript (strict) + TailwindCSS.

---

## DEC-006: Complete UI Redesign to Premium SaaS (SteerAI)

- **Timestamp**: 2026-08-08
- **Problem**: The initial UI felt too generic and too close to a standard AI chatbot.
- **Options considered**:
  1. Keep current dark mode and just add better components.
  2. Complete overhaul to mirror premium products like Linear, Stripe, and Vercel.
- **Chosen option**: Option 2 — Complete overhaul.
- **Reason**: To make a strong impression ("stop scrolling and think this is a real startup"), the UI must avoid ChatGPT clones entirely.
- **Impact**:
  - The project is now named **SteerAI**.
  - Replaced the standard chat interface with an **Interview Workspace** featuring a 3-pane layout (Progress, Question Stage, Live Evaluation).
  - Adopted a strict 8-color system, Plus Jakarta Sans, Inter, and IBM Plex Mono.
  - Added Framer Motion for intentional, smooth micro-interactions.

---

## DEC-007: Aggressive Visual Noise Reduction (UX Refinement)

- **Timestamp**: 2026-08-08
- **Problem**: The SteerAI redesign still felt too dense and "dashboard-like", overwhelming the user with metrics.
- **Chosen option**: Massive whitespace increase and layout simplification across all 4 main screens.
- **Reason**: A premium product guides the user by answering one question per screen. Removing unnecessary borders, hiding sidebars during the interview, and enlarging typography creates a calm, confident UX.
- **Impact**: Interview workspace is now centered on the question alone. Sidebars are collapsible. Candidate cards show 60% less text. Landing page hero is drastically simplified. Immersive AI transitions replaced static loading indicators.

---

## DEC-008: Deterministic Backend Pipeline (Pre-LLM)

- **Timestamp**: 2026-08-08
- **Problem**: How to ensure the AI doesn't hallucinate candidate gaps or invent curriculum topics?
- **Chosen option**: Build a fully deterministic pipeline (Loader → Analyzer → Planner → ContextBuilder) that feeds structured data to the downstream LLM modules.
- **Reason**: Separating pure logic from IO (LLMs) ensures the core business logic (who is the candidate, what are their gaps, what is the plan) is testable, fast, and 100% accurate. The LLM acts only as a natural language interface on top of this rock-solid foundation.
- **Impact**: Created `CandidateAnalysis`, `InterviewPlan`, and `InterviewContext` schemas. Rewired `InterviewManager` to run the deterministic pipeline on startup. Future LLM modules will simply consume the unified `InterviewContext`.

---

## DEC-009: Dedicated LLM AI Layer

- **Timestamp**: 2026-08-08
- **Problem**: How to integrate Gemini for dynamic question/follow-up/feedback generation without leaking prompt engineering and API logic into the core business modules.
- **Chosen option**: Create a dedicated `LLMService`, `LLMParser`, and `prompt_builders` layer.
- **Reason**: Decoupling the API communication (retries, timeouts) and prompt construction from the generators (`QuestionGenerator`, etc.) adheres to the single responsibility principle. It also centralizes JSON parsing and error recovery (fallbacks).
- **Impact**: Added `google-generativeai` dependency. Prompts are constructed purely from the deterministic `InterviewContext` and returned JSON is robustly parsed to avoid crashing the interview workflow.

---

## DEC-010: Evidence-Based Interview Evaluation

- **Timestamp**: 2026-08-08
- **Problem**: The previous interview score used answer-length heuristics and could not prove that final feedback reflected submitted answers.
- **Chosen option**: Gemini evaluates one answer at a time against the stored question rubric; the backend validates dimensions, retains immutable evidence, and calculates all mastery and aggregate scores deterministically.
- **Reason**: This preserves Gemini as a constrained evaluator while keeping scoring, session state, normalization, coverage, and consistency decisions testable and explainable.
- **Impact**: Sessions now retain `evaluations[]` and `topic_mastery`; final feedback receives only interview evidence plus deterministic score summaries. Candidate profile completion is excluded from final score calculation.

---

## DEC-011: Evaluation Pipeline Diagnosis and Fallback Improvements

- **Timestamp**: 2026-08-08
- **Problem**: Live behavior indicated evaluation engine not correctly influencing interviews: incorrect answers produced scores, generic follow-ups appeared, and "evaluation temporarily unavailable" messages showed in feedback.
- **Investigation**: Complete runtime trace with comprehensive logging from question generation through evaluation, session storage, and feedback generation.
- **Root Cause**: Gemini API free-tier quota exceeded (429 error). All LLM calls (question, evaluation, follow-up, feedback) fell back to default responses with zero scores and generic content.
- **Verification**: Pipeline architecture is correct - prompts include exact candidate answers, expected points are passed correctly, session storage works, and context flows through all modules. The issue is purely LLM service unavailability.
- **Chosen option**: Enhanced fallback detection with `_fallback` flags, added validation warnings for empty expected_points, improved error logging to surface quota issues clearly.
- **Impact**: System now clearly indicates when operating in degraded mode. Production requires paid API tier. Added validation that questions should never generate without evaluation rubrics.
- **Related Documents**: `docs/dev-notes/EVALUATION_DIAGNOSIS.md`, `docs/archive/EVALUATION_FIX_SUMMARY.md`

---

## DEC-012: Adaptive Interview Decision Engine

- **Timestamp**: 2026-08-08
- **Problem**: Interview flow was purely linear (follow-up or next topic), lacking intelligence to adjust difficulty or end early based on performance.
- **Chosen option**: Lightweight `AdaptiveDecisionEngine` that consumes existing `EvaluationResult` and makes five decision types: `NEXT_TOPIC`, `FOLLOW_UP`, `HARDER`, `SIMPLER`, `END_INTERVIEW`.
- **Reason**: The existing `EvaluationEngine` provides rich evidence (scores, mastery, needs_followup). Rather than create a parallel scoring system, we use a pure function to interpret that evidence and route the interview intelligently.
- **Implementation**:
  - New module: `backend/modules/adaptive_decision_engine.py`
  - Decision thresholds: Strong (≥7.0), Weak (<4.0), High mastery (≥70%), Low mastery (<40%)
  - Respects all existing limits: max questions, max follow-ups, duplicate detection
  - Returns structured `AdaptiveDecisionResult` with decision type, reason, target topic, and difficulty
- **Integration**: Modified `InterviewManager.continue_interview()` to call `adaptive_engine.decide()` after evaluation, then route based on the decision instead of using hardcoded follow-up logic.
- **Safety**: Preserves all existing guardrails - no infinite loops, no repeated questions, respects maximum limits.
- **Impact**: Interviews now adapt difficulty in real-time, can simplify questions when candidates struggle, increase challenge when they excel, and end early when sufficient evidence is collected.
- **Related Schema**: Added `AdaptiveDecision` enum and `AdaptiveDecisionResult` model to `models/schemas.py`

---

## DEC-013: Browser-Native Voice Answer Input

- **Timestamp**: 2026-08-08
- **Problem**: Typing long technical answers is tedious; voice input would improve candidate experience.
- **Chosen option**: Client-side Web Speech API integration with manual transcript review before submission.
- **Reason**: Browser-native API requires no additional dependencies, works offline, and keeps voice processing client-side. Candidates can speak naturally, review/edit the transcript, then submit through the existing answer pipeline.
- **Implementation**:
  - New hook: `frontend/src/hooks/useVoiceRecording.ts`
  - Uses `SpeechRecognition` / `webkitSpeechRecognition` API
  - States: idle, listening, processing, error
  - Graceful degradation if API unsupported or permission denied
  - Real-time duration counter and animated recording indicator
- **UI Integration**: Added microphone button to Interview Workspace answer section:
  - "Speak" button starts recording (changes to "Stop" button with timer)
  - Live recording indicator shows elapsed time
  - Transcript automatically populates answer textarea when recording stops
  - Candidate can edit transcript before clicking existing "Send Answer" button
  - Cancel option available during recording
  - Error states shown inline (permission denied, no speech detected, etc.)
- **Backend Impact**: Zero - voice is transcribed client-side; backend receives normal answer string
- **Safety**: Typed answer mode always works; voice is purely optional enhancement
- **Related Files**: `frontend/src/hooks/useVoiceRecording.ts`, modifications to `InterviewWorkspacePage.tsx`

---
