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
