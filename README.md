# ABTalks — AI Interview Agent

> An AI-powered technical interview agent that conducts personalized interviews based on candidate profiles and curriculum data.

## Overview

ABTalks is an **Interview Operating System** — not a chatbot. It analyzes a candidate's learning journey through a 31-day AI curriculum, identifies strengths and gaps, and conducts an adaptive technical interview with intelligent follow-up questions and structured feedback.

## Architecture

```
Interview Manager (orchestrator)
├── Candidate Analyzer    — Profile analysis & signal extraction
├── Interview Planner     — Adaptive topic planning
├── Question Generator    — Context-aware question creation
├── Follow-up Generator   — Intelligent probing
├── Evaluation Engine     — Response scoring & tracking
├── Feedback Generator    — Structured assessment output
└── Session Manager       — In-memory state management
```

Every submitted answer is evaluated independently against the question's retained rubric. The session stores immutable evaluation evidence, topic mastery, and accumulated 0–100 score dimensions; final feedback is synthesized only from that interview evidence.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React + Vite + TypeScript + TailwindCSS |
| Backend | FastAPI + Python |
| State | In-memory sessions (sessionId) |
| Data | curriculum.json + candidates.json |

## Quick Start

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### API

Single endpoint:

```
POST /api/interview
```

See [technical-spec.md](./technical-spec.md) for the full API contract.

## Project Structure

```
ABTalks/
├── backend/
│   ├── main.py                 # FastAPI entry point
│   ├── config.py               # Environment & settings
│   ├── routers/
│   │   └── interview.py        # POST /api/interview
│   ├── models/
│   │   └── schemas.py          # Pydantic models
│   ├── modules/
│   │   ├── interview_manager.py    # Orchestrator
│   │   ├── candidate_analyzer.py   # Profile analysis
│   │   ├── interview_planner.py    # Topic planning
│   │   ├── question_generator.py   # Question creation
│   │   ├── followup_generator.py   # Follow-up logic
│   │   ├── evaluation_engine.py    # Response scoring
│   │   ├── feedback_generator.py   # Final feedback
│   │   └── session_manager.py      # Session state
│   ├── services/
│   │   ├── llm_service.py          # Gemini communication and fallbacks
│   │   └── prompt_builders/        # Question, follow-up, evaluation, feedback prompts
│   └── data/
│       ├── curriculum.json
│       └── candidates.json
├── frontend/
│   └── src/
│       ├── api/                # API client layer
│       ├── hooks/              # Custom React hooks
│       ├── types/              # TypeScript interfaces
│       ├── utils/              # Utility functions
│       ├── constants/          # Design tokens & config
│       ├── components/ui/      # Reusable primitives
│       ├── features/           # Feature-based pages
│       └── layouts/            # Page wrappers
├── README.md
├── CONTEXT.md
├── INSTRUCTIONS.md
├── PROMPTS.md
├── TASKS.md
├── DECISIONS.md
└── HANDOFF.md
```

## Documentation

| File | Purpose |
|------|---------|
| [CONTEXT.md](./CONTEXT.md) | Current project state & architecture |
| [INSTRUCTIONS.md](./INSTRUCTIONS.md) | Permanent AI/dev rules |
| [PROMPTS.md](./PROMPTS.md) | AI prompt history |
| [TASKS.md](./TASKS.md) | Kanban task board |
| [DECISIONS.md](./DECISIONS.md) | Architecture decision log |
| [HANDOFF.md](./HANDOFF.md) | Current working state |

## License

Hackathon project — 48-hour build.
