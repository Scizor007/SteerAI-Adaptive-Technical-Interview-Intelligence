## PROMPT-001

- **Prompt ID**: PROMPT-001- **Timestamp**: 2026-08-08T01:00:00+05:30- **Goal**: Scaffold the entire ABTalks project — folder structure, backend modules, frontend foundation, design tokens, documentation- **Prompt**: Full project scaffolding request including architecture design, tech stack setup (FastAPI + React/Vite/TS/Tailwind), modular interview system (8 modules), design token system, and 7 documentation files.- **Result**: Project fully scaffolded.

---

## PROMPT-002

- **Prompt ID**: PROMPT-002- **Timestamp**: 2026-08-08T02:05:00+05:30- **Goal**: Complete UI Redesign to "SteerAI" (Premium SaaS)- **Prompt**: "You are an award-winning Product Designer, UX Architect... Completely redesign the frontend. Ignore the current UI... Brand: SteerAI. Premium, Intelligent, Calm, Modern... Avoid ChatGPT clones... Use Linear/Stripe as inspiration... Strict 8 color system. Plus Jakarta Sans, Inter, IBM Plex Mono... Interview Screen must be an Interview Workspace (3 panes) NOT a chat interface... Use Framer Motion... Update all documentation..."- **Result**: Massive frontend overhaul across 43+ files. Created a full component system, implemented Framer Motion, set up React Router, and completely built out all 5 pages using the SteerAI design system. Updated all project documentation.

---

## PROMPT-003

- **Prompt ID**: PROMPT-003- **Timestamp**: 2026-08-08T02:16:38+05:30- **Goal**: UI Refinement (Reduce visual noise, increase whitespace, improve UX hierarchy)- **Result**: Completely overhauled Landing, Candidate Selection, Interview Workspace, and Feedback pages. Simplified candidate cards to minimal data. Changed Interview Workspace to a centered focus mode with collapsible sidebar and immersive AI evaluation transitions. Reduced borders and cards on Feedback page to emphasize the hero score and typography.

---

## PROMPT-004

- **Prompt ID**: PROMPT-004 (User referred to as P002)- **Timestamp**: 2026-08-08T10:30:00+05:30- **Goal**: Deterministic Backend Foundation (Pre-LLM Pipeline)- **Prompt**: "This prompt focuses ONLY on the backend foundation. Do NOT implement LLM integrations. Build the deterministic backend pipeline... Implement Candidate Loader, Curriculum Loader, Candidate Analyzer (deterministic), Interview Planner (deterministic), Interview Context Builder... Follow SOLID principles. Strongly typed Pydantic models... Separate pure logic from IO."- **Result**: Completely rewrote the backend data ingestion and planning pipeline. Created robust Pydantic schemas (compatible with Python 3.7+ typing). Built `CandidateAnalyzer` to deterministically score candidates and find gaps. Built `InterviewPlanner` to schedule questions with escalating difficulty. Built `InterviewContextBuilder` to unify state for downstream LLM consumption. Verified the API end-to-end via `_smoke_test.py`.

---

## PROMPT-005

- **Prompt ID**: PROMPT-005- **Timestamp**: 2026-08-08T11:20:00+05:30- **Goal**: Configure Breeth MCP Development Tooling- **Prompt**: "Configure Breeth MCP as a DEVELOPMENT MEMORY system only. Breeth is NOT part of the application runtime. The interview platform must work perfectly even if Breeth is unavailable. Do not modify application behavior. Do not add Breeth to frontend or backend runtime... Verify that the existing Breeth MCP configuration is correct... Update CONTEXT.md, INSTRUCTIONS.md, HANDOFF.md..."- **Result**: Added Breeth MCP configuration to the global IDE `mcp_config.json` using the developer-provided JSON snippet. Updated project documentation to strictly enforce Breeth as development-only tooling with no secrets exposed.

---

## PROMPT-006

- **Prompt ID**: PROMPT-006- **Timestamp**: 2026-08-08T11:46:15+05:30- **Goal**: Integrate Gemini into the existing backend architecture.- **Prompt**: "Integrate Gemini into the existing backend architecture. Gemini should ONLY generate natural language. The deterministic backend remains responsible for candidate analysis, interview planning, etc. Create a dedicated AI layer... LLMService, Prompt Builders, Output Parser... Do NOT implement RAG, LangChain, etc. Keep implementation lightweight."- **Result**: Implemented a dedicated AI Layer using `google-generativeai`. Created `LLMService` to handle retries and config, `LLMParser` for robust JSON parsing with fallbacks, and strict Prompt Builders (`question_prompt`, `followup_prompt`, `feedback_prompt`). Refactored `QuestionGenerator`, `FollowupGenerator`, and `FeedbackGenerator` to use Gemini. Added lightweight tests in `test_llm.py` and updated `_smoke_test.py` to use dynamic session IDs. Verified successful backend compilation and E2E interview functionality.

---

## PROMPT-007

- **Prompt ID**: PROMPT-007- **Timestamp**: 2026-08-08- **Goal**: Implement real, evidence-based answer evaluation and connect the Feedback page to backend report data.- **Result**: Added a constrained evaluation prompt, validated `EvaluationResult` schema, immutable session evaluation history, per-topic mastery, and deterministic weighted 0–100 scoring with coverage and consistency bonuses. Refactored final feedback to use interview evidence only. Replaced the frontend mock interview/report flow with the API-backed flow. Added tests for excellent, average, poor, empty, off-topic, and complete strong-vs-poor interviews.

---

## PROMPT-008

- **Prompt ID**: PROMPT-008- **Timestamp**: 2026-08-08- **Goal**: Implement OpenRouter as the primary LLM provider without changing the interview architecture.- **Result**: Created an `LLMProvider` abstraction. Implemented `OpenRouterProvider` (REST) and `GeminiProvider` (SDK). Refactored `LLMService` to route to providers based on `.env` settings while preserving all central retry, parsing, and fallback logic. Business logic, prompts, and schemas remained entirely untouched.

---

## PROMPT-009

- **Prompt ID**: PROMPT-009- **Timestamp**: 2026-08-08- **Goal**: Diagnose and resolve Gemini API configuration and quota issues.- **Result**: Audited Gemini model availability and SDK configuration, identified the invalid `gemini-1.5-flash` configuration, switched to a supported Gemini model, diagnosed exhausted free-tier quota, and documented the configuration and quota findings. Created temporary audit/debug tooling to trace LLM calls and understand per-interview API usage.

---

## PROMPT-010

- **Prompt ID**: PROMPT-010- **Timestamp**: 2026-08-08- **Goal**: Diagnose excessive LLM API usage and verify the interview evaluation pipeline.- **Result**: Traced the complete LLM call sequence and established the expected request pattern of `1 + (N × 2) + 1` for an N-question interview. Confirmed separate calls for question generation, evaluation, follow-ups where applicable, and final feedback. Verified that the calls were serving distinct responsibilities rather than being accidental duplicate requests.

---

## PROMPT-011

- **Prompt ID**: PROMPT-011- **Timestamp**: 2026-08-08- **Goal**: Introduce OpenRouter as an alternative LLM provider while preserving the existing architecture.- **Result**: Implemented provider abstraction with `LLMProvider`, `OpenRouterProvider`, and `GeminiProvider`. Updated `LLMService` to select the provider through configuration. Existing question generation, evaluation, follow-up, feedback, schemas, and interview progression remained unchanged. Verified the complete interview pipeline using OpenRouter.

---

## PROMPT-012

- **Prompt ID**: PROMPT-012- **Timestamp**: 2026-08-08- **Goal**: Improve reliability of structured LLM responses.- **Result**: Added a lightweight JSON recovery layer to the LLM parser to handle malformed structured responses such as empty numeric values, truncated JSON, missing closing brackets, trailing commas, incomplete fields, and markdown fences. Added unit and performance tests. The recovery layer acts as a safety net without changing interview logic or provider behavior.

---

## PROMPT-013

- **Prompt ID**: PROMPT-013- **Timestamp**: 2026-08-08- **Goal**: Select a reliable OpenRouter model for structured technical interview evaluation.- **Result**: Compared model behavior using the evaluation pipeline. `meta-llama/llama-3.2-3b-instruct` produced malformed JSON in a significant percentage of evaluation responses. Switched the configured OpenRouter model to `openai/gpt-3.5-turbo` and verified a complete interview with 100% successful evaluation responses and no fallback evaluations in the test run.

---

## PROMPT-014

- **Prompt ID**: PROMPT-014- **Timestamp**: 2026-08-08- **Goal**: Diagnose and fix interview flow reliability issues.- **Result**: Fixed duplicate-question detection, follow-up count inheritance, strict follow-up limits, evaluation fallback handling, topic-specific fallback questions, and API-key configuration validation. Added comprehensive interview-flow tests. Verified that the interview progresses without infinite loops and that unavailable LLM evaluations are not incorrectly stored as candidate scores.

---

## PROMPT-015

- **Prompt ID**: PROMPT-015- **Timestamp**: 2026-08-09- **Goal**: Reorganize project documentation and development files.- **Result**: Kept essential project documentation at the repository root and moved historical/debugging material into `docs/archive/` and `docs/dev-notes/`. Organized backend test/debug files under `backend/tests/`. Preserved development history while reducing root-level clutter.

---

## PROMPT-016

- **Prompt ID**: PROMPT-016- **Timestamp**: 2026-08-09- **Goal**: Resolve GitHub secret-scanning and repository hygiene issues.- **Result**: Removed real API credentials from tracked documentation/configuration, replaced credentials with placeholders, verified `.env` is ignored and not tracked, and reorganized temporary verification files. GitHub push protection was satisfied after cleaning the exposed secret from the repository history/working state.

---

## PROMPT-017

- **Prompt ID**: PROMPT-017- **Timestamp**: 2026-08-09- **Goal**: Fix frontend layout constraints affecting the Landing page.- **Result**: Identified the conflict between `AppLayout`'s `container-steer` constraint and the Landing page's full-width hero breakout. Updated the Landing page to use `AppLayout fullBleed`, eliminating the horizontal layout issue while preserving functionality and the behavior of other pages.

---

## PROMPT-018

- **Prompt ID**: PROMPT-018- **Timestamp**: 2026-08-09- **Goal**: Refine the Interview Workspace UI without changing application functionality.- **Result**: Reworked the Interview Workspace into a full-viewport three-column desktop workspace consisting of the candidate/session sidebar, central interview area, and Live Evaluation panel. Improved viewport utilization and removed excessive unused space while preserving all interview functionality and backend behavior.

---

## PROMPT-019

- **Prompt ID**: PROMPT-019- **Timestamp**: 2026-08-09- **Goal**: Improve Interview Workspace typography and visual hierarchy.- **Result**: Refined typography, text sizing, spacing, hierarchy, readability, and visual emphasis while preserving the existing layout and all application functionality. The question became the primary visual focus, with clearer hierarchy for candidate information, answer input, evaluation status, and supporting metadata.

PROMPT-020

Prompt ID: PROMPT-020

Timestamp: 2026-08-09

Goal: Add adaptive interview decisions and voice answer input without changing the existing interview architecture.

Prompt: Add an adaptive decision layer that uses existing evaluation evidence to decide whether the interview should move to the next topic, ask a related follow-up, increase difficulty, decrease difficulty, or end when sufficient evidence has been collected. Also add browser-native voice input so candidates can speak an answer, review/edit the resulting transcript, and submit it through the existing answer pipeline. Preserve existing scoring, follow-up limits, duplicate detection, provider abstraction, API contracts, and backend safeguards.

Result: Implemented AdaptiveDecisionEngine with guarded decision types and integrated it into interview progression. Added browser-native speech recognition through useVoiceRecording.ts, allowing spoken answers to become editable text before submission. Existing typed-answer flow remains available as a fallback. No external voice dependency was added.

PROMPT-021

Prompt ID: PROMPT-021

Timestamp: 2026-08-09

Goal: Verify the adaptive interview and voice implementation without breaking the existing working pipeline.

Prompt: Verify that the adaptive interview flow still respects maximum question/follow-up limits, duplicate-question protection, evaluation fallback handling, and existing scoring. Verify that voice transcription feeds the same answer submission path as typed answers. Check TypeScript/Python compilation, backend health, frontend hot reload, and runtime behavior. Do not change backend scoring or LLM provider behavior during verification.

Result: Backend and frontend remained operational after the changes. Voice input was manually verified in the interview workspace: the candidate can start speech capture, stop it, review the generated transcript, and submit it as a normal answer. Adaptive question progression continued through the existing interview pipeline.

PROMPT-022

Prompt ID: PROMPT-022

Timestamp: 2026-08-09

Goal: Improve the Interview Workspace UI so the existing adaptive interview and voice functionality is presented as a polished, full-viewport technical interview product.

Prompt: Refine the Interview Workspace visual design without changing any application functionality, backend logic, API contracts, interview progression, scoring, question generation, follow-up generation, voice behavior, or evaluation behavior. Use the available viewport efficiently, eliminate large unused areas, strengthen typography and hierarchy, make the current question the primary focus, and maintain clear candidate/session information, answer input, voice controls, evaluation state, and supporting metadata. Preserve the three-column interview workspace concept and make the interface responsive.

Result: Refined the Interview Workspace layout, viewport utilization, typography, spacing, and hierarchy while preserving the underlying interview functionality. The workspace now presents the question, answer area, candidate context, and Live Evaluation panel more clearly.

PROMPT-023

Prompt ID: PROMPT-023

Timestamp: 2026-08-09

Goal: Add interviewer-style spoken question delivery to complement the existing voice-answer experience.

Prompt: Extend the existing interview voice experience so every generated interview question can also be read aloud by the browser using text-to-speech, while keeping the question visible on screen. The candidate must be able to listen to the AI question, read it visually, type an answer, or use the existing speech-to-text answer control. Do not replace the existing text question, typed input, transcript review, answer submission, evaluation, adaptive decision engine, or backend pipeline. Speech synthesis must be optional, gracefully handle unsupported browsers/errors, and never block interview progression.

Status: Planned enhancement / prompt recorded. Do not treat this entry as an implemented feature until runtime verification is completed.
