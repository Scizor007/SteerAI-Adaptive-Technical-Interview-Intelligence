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
