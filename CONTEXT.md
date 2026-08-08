# CONTEXT.md — Project Context & Architecture

> Last updated: 2026-08-08

---

## Project Overview

**SteerAI** is a premium AI Assessment Platform that conducts personalized technical interviews based on candidate profiles from a 31-day AI curriculum.

**Core premise**: Analyze what a candidate completed, skipped, struggled with, and mastered — then conduct an adaptive interview that probes gaps, verifies claimed strengths, and generates structured feedback. The UI feels like a real SaaS product companies would buy (e.g., Linear, Stripe, Vercel), intentionally avoiding "ChatGPT clone" clichés.

---

## Architecture

### Backend Module System

```
POST /api/interview
        │
        ▼
  Interview Router
        │
        ▼
  Interview Manager (orchestrator)
  ├── Candidate Loader      → parses and exposes candidates.json
  ├── Curriculum Loader     → parses and indexes curriculum.json
  ├── Candidate Analyzer    → extracts strengths/weaknesses/gaps (deterministic)
  ├── Interview Planner     → builds prioritized topic list (deterministic)
  ├── Session Manager       → in-memory dict keyed by sessionId
  ├── Interview Context Builder → merges session state for LLM consumption
  ├── Question Generator    → produces adaptive questions (stub)
  ├── Follow-up Generator   → probes deeper based on response quality (stub)
  ├── Evaluation Engine     → scores responses, tracks performance (stub)
  └── Feedback Generator    → produces summary/strengths/gaps/next (stub)
```

### Frontend Architecture

```
src/
├── api/              → API client (sole HTTP layer)
├── hooks/            → useInterview, useCandidates, etc.
├── types/            → TypeScript interfaces (mirrors backend schemas)
├── utils/            → Pure functions
├── constants/        → Design tokens, app config
├── components/ui/    → Reusable primitives (Button, Card, Badge, etc.)
├── features/
│   ├── landing/      → Landing page
│   ├── candidates/   → Candidate selection
│   ├── interview/    → Interview Workspace (NOT a chat interface)
│   ├── feedback/     → Feedback report
│   └── architecture/ → Architecture overview
└── layouts/          → Page layout wrappers (Navbar, AppLayout)
```

---

## Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Frontend | React | 19.x |
| Build | Vite | 5.x |
| Language | TypeScript | strict |
| Styling | TailwindCSS | 4.x |
| Animation | Framer Motion | 13.x |
| Backend | FastAPI | 0.103.x |
| Backend Lang | Python | 3.11+ |
| Validation | Pydantic | 2.5.x |
| State | In-memory (dict) | — |

---

## Design System: SteerAI

### Visual Identity
- **Personality:** Premium, Intelligent, Calm, Confident, Technical, Human, Modern.
- **Inspiration:** Linear, Stripe, Raycast, Notion, Vercel.
- **Traits:** Lots of whitespace, large typography, strong hierarchy, subtle shadows, rounded corners, intentional motion.

### Color Tokens (Strict 8-Color System)

| Token | Hex | Role |
|-------|-----|------|
| `--bg-primary` | `#09090B` | Deep rich black |
| `--bg-secondary`| `#111114` | Subtle elevation |
| `--surface` | `#1A1A1F` | Cards and distinct blocks |
| `--text-primary`| `#F4F4F5` | High contrast text |
| `--text-secondary`|`#8B8B95` | Muted metadata |
| `--border` | `#2A2A30` | Subtle structural lines |
| `--accent` | `#5E6AD2` | Premium Indigo/Blurple |
| `--signal` | `#22C55E` | Success/Live state emerald |

### Typography

| Face | Font | Role |
|------|------|------|
| Display | Plus Jakarta Sans | Headings, signaling a premium tech product |
| Body | Inter | Clean, neutral UI text |
| Mono | IBM Plex Mono | Technical data, session IDs, assessment stats |

### Layout Concepts

| Page | Concept |
|------|---------|
| Landing | Centered hero with animated background and simplified typography. Architecture pushed down. |
| Candidate Selection | Premium profile cards (Photo, Name, Role, Completion %, Key Strength) with high whitespace. |
| Interview | **Total Focus Mode:** Massive centered question text. Left sidebar is collapsible. Immersive AI transitions between questions. |
| Feedback Report | Professional assessment report featuring a massive hero score, minimal borders, and strong visual hierarchy. |
| Architecture | Interactive topology diagram with module cards and flow animations. |

---

## API Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/interview` | Start / continue / end interview |
| GET | `/health` | Health check |

### Request/Response Flow

```
Start:    { sessionId, candidate }       → { reply, done: false }
Continue: { sessionId, message }         → { reply, done: false }
End:      (automatic)                    → { reply, done: true, feedback }
```

---

## Data Flow

```
candidates.json → Candidate Analyzer → Interview Planner
curriculum.json → Interview Planner → Question Generator
                                    → Follow-up Generator
candidate answer → Evaluation Engine → Feedback Generator → API Response
```

---

## Implemented Features

- [x] Project scaffolding (frontend + backend)
- [x] Backend module architecture (8 modules with stubs)
- [x] Pydantic schema models
- [x] FastAPI router with POST /api/interview
- [x] Frontend Vite + React + TypeScript project
- [x] **SteerAI Premium UI Redesign** (Framer motion, new design tokens, new typography)
- [x] Full UI Component System (20+ components)
- [x] Complete Frontend Pages (Landing, Candidates, Interview Workspace, Feedback, Architecture)
- [x] React Router setup

## Pending Features

- [ ] LLM integration for question generation (Backend)
- [ ] LLM integration for response evaluation (Backend)
- [ ] LLM integration for feedback synthesis (Backend)
- [ ] E2E Testing

## Current Sprint

**Sprint 2 — LLM Integration & Backend Logic** (upcoming)

---
