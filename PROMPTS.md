# PROMPTS.md — AI Prompt History

> Append-only. Never delete entries.

---

## PROMPT-001

- **Prompt ID**: PROMPT-001
- **Timestamp**: 2026-08-08T01:00:00+05:30
- **Goal**: Scaffold the entire ABTalks project — folder structure, backend modules, frontend foundation, design tokens, documentation
- **Prompt**: Full project scaffolding request including architecture design, tech stack setup (FastAPI + React/Vite/TS/Tailwind), modular interview system (8 modules), design token system, and 7 documentation files. 
- **Result**: Project fully scaffolded.

---

## PROMPT-002

- **Prompt ID**: PROMPT-002
- **Timestamp**: 2026-08-08T02:05:00+05:30
- **Goal**: Complete UI Redesign to "SteerAI" (Premium SaaS)
- **Prompt**: "You are an award-winning Product Designer, UX Architect... Completely redesign the frontend. Ignore the current UI... Brand: SteerAI. Premium, Intelligent, Calm, Modern... Avoid ChatGPT clones... Use Linear/Stripe as inspiration... Strict 8 color system. Plus Jakarta Sans, Inter, IBM Plex Mono... Interview Screen must be an Interview Workspace (3 panes) NOT a chat interface... Use Framer Motion... Update all documentation..."
- **Result**: Massive frontend overhaul across 43+ files. Created a full component system, implemented Framer Motion, set up React Router, and completely built out all 5 pages using the SteerAI design system. Updated all project documentation.

---

## PROMPT-003

- **Prompt ID**: PROMPT-003
- **Timestamp**: 2026-08-08T02:16:38+05:30
- **Goal**: UI Refinement (Reduce visual noise, increase whitespace, improve UX hierarchy)
- **Result**: Completely overhauled Landing, Candidate Selection, Interview Workspace, and Feedback pages. Simplified candidate cards to minimal data. Changed Interview Workspace to a centered focus mode with collapsible sidebar and immersive AI evaluation transitions. Reduced borders and cards on Feedback page to emphasize the hero score and typography.

---

## PROMPT-004

- **Prompt ID**: PROMPT-004 (User referred to as P002)
- **Timestamp**: 2026-08-08T10:30:00+05:30
- **Goal**: Deterministic Backend Foundation (Pre-LLM Pipeline)
- **Prompt**: "This prompt focuses ONLY on the backend foundation. Do NOT implement LLM integrations. Build the deterministic backend pipeline... Implement Candidate Loader, Curriculum Loader, Candidate Analyzer (deterministic), Interview Planner (deterministic), Interview Context Builder... Follow SOLID principles. Strongly typed Pydantic models... Separate pure logic from IO."
- **Result**: Completely rewrote the backend data ingestion and planning pipeline. Created robust Pydantic schemas (compatible with Python 3.7+ typing). Built `CandidateAnalyzer` to deterministically score candidates and find gaps. Built `InterviewPlanner` to schedule questions with escalating difficulty. Built `InterviewContextBuilder` to unify state for downstream LLM consumption. Verified the API end-to-end via `_smoke_test.py`.

---

## PROMPT-005

- **Prompt ID**: PROMPT-005
- **Timestamp**: 2026-08-08T11:20:00+05:30
- **Goal**: Configure Breeth MCP Development Tooling
- **Prompt**: "Configure Breeth MCP as a DEVELOPMENT MEMORY system only. Breeth is NOT part of the application runtime. The interview platform must work perfectly even if Breeth is unavailable. Do not modify application behavior. Do not add Breeth to frontend or backend runtime... Verify that the existing Breeth MCP configuration is correct... Update CONTEXT.md, INSTRUCTIONS.md, HANDOFF.md..."
- **Result**: Added Breeth MCP configuration to the global IDE `mcp_config.json` using the developer-provided JSON snippet. Updated project documentation to strictly enforce Breeth as development-only tooling with no secrets exposed.

---

## PROMPT-006

- **Prompt ID**: PROMPT-006
- **Timestamp**: 2026-08-08T11:46:15+05:30
- **Goal**: Integrate Gemini into the existing backend architecture.
- **Prompt**: "Integrate Gemini into the existing backend architecture. Gemini should ONLY generate natural language. The deterministic backend remains responsible for candidate analysis, interview planning, etc. Create a dedicated AI layer... LLMService, Prompt Builders, Output Parser... Do NOT implement RAG, LangChain, etc. Keep implementation lightweight."
- **Result**: Implemented a dedicated AI Layer using `google-generativeai`. Created `LLMService` to handle retries and config, `LLMParser` for robust JSON parsing with fallbacks, and strict Prompt Builders (`question_prompt`, `followup_prompt`, `feedback_prompt`). Refactored `QuestionGenerator`, `FollowupGenerator`, and `FeedbackGenerator` to use Gemini. Added lightweight tests in `test_llm.py` and updated `_smoke_test.py` to use dynamic session IDs. Verified successful backend compilation and E2E interview functionality.

---

## PROMPT-007

- **Prompt ID**: PROMPT-007
- **Timestamp**: 2026-08-08
- **Goal**: Implement real, evidence-based answer evaluation and connect the Feedback page to backend report data.
- **Result**: Added a constrained evaluation prompt, validated `EvaluationResult` schema, immutable session evaluation history, per-topic mastery, and deterministic weighted 0–100 scoring with coverage and consistency bonuses. Refactored final feedback to use interview evidence only. Replaced the frontend mock interview/report flow with the API-backed flow. Added tests for excellent, average, poor, empty, off-topic, and complete strong-vs-poor interviews.
