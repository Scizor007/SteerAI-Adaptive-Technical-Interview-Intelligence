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
  ├── Session Manager       → stores questions, evaluation evidence, and topic mastery
  ├── Interview Context Builder → merges session state for LLM consumption
  ├── Question Generator    → produces adaptive questions (stub)
  ├── Follow-up Generator   → probes deeper based on response quality (stub)
  ├── Evaluation Prompt Builder → prepares a single-answer evidence rubric
  ├── Evaluation Engine     → validates 0–10 rubric dimensions and calculates aggregates
  ├── Feedback Generator    → synthesizes final feedback only from recorded interview evidence
  └── LLM Provider Layer    → LLMService routes to OpenRouterProvider or GeminiProvider
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

| Layer        | Technology       | Version |
| ------------ | ---------------- | ------- |
| Frontend     | React            | 19.x    |
| Build        | Vite             | 5.x     |
| Language     | TypeScript       | strict  |
| Styling      | TailwindCSS      | 4.x     |
| Animation    | Framer Motion    | 13.x    |
| Backend      | FastAPI          | 0.103.x |
| Backend Lang | Python           | 3.11+   |
| Validation   | Pydantic         | 2.5.x   |
| State        | In-memory (dict) | —       |

---

## Design System: SteerAI

### Visual Identity

- **Personality:** Premium, Intelligent, Calm, Confident, Technical, Human, Modern.
- **Inspiration:** Linear, Stripe, Raycast, Notion, Vercel.
- **Traits:** Lots of whitespace, large typography, strong hierarchy, subtle shadows, rounded corners, intentional motion.

### Color Tokens (Strict 8-Color System)

| Token              | Hex       | Role                       |
| ------------------ | --------- | -------------------------- |
| `--bg-primary`     | `#09090B` | Deep rich black            |
| `--bg-secondary`   | `#111114` | Subtle elevation           |
| `--surface`        | `#1A1A1F` | Cards and distinct blocks  |
| `--text-primary`   | `#F4F4F5` | High contrast text         |
| `--text-secondary` | `#8B8B95` | Muted metadata             |
| `--border`         | `#2A2A30` | Subtle structural lines    |
| `--accent`         | `#5E6AD2` | Premium Indigo/Blurple     |
| `--signal`         | `#22C55E` | Success/Live state emerald |

### Typography

| Face    | Font              | Role                                          |
| ------- | ----------------- | --------------------------------------------- |
| Display | Plus Jakarta Sans | Headings, signaling a premium tech product    |
| Body    | Inter             | Clean, neutral UI text                        |
| Mono    | IBM Plex Mono     | Technical data, session IDs, assessment stats |

### Layout Concepts

| Page                | Concept                                                                                                                        |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Landing             | Centered hero with animated background and simplified typography. Architecture pushed down.                                    |
| Candidate Selection | Premium profile cards (Photo, Name, Role, Completion %, Key Strength) with high whitespace.                                    |
| Interview           | **Total Focus Mode:** Massive centered question text. Left sidebar is collapsible. Immersive AI transitions between questions. |
| Feedback Report     | Professional assessment report featuring a massive hero score, minimal borders, and strong visual hierarchy.                   |
| Architecture        | Interactive topology diagram with module cards and flow animations.                                                            |

---

## Development Tooling

### Breeth MCP

**Purpose**: Developer memory only.

**Usage**:

- Architecture summaries
- Milestone summaries
- Bug summaries
- Next-step handoffs

_Note: Breeth MCP is not used by the application runtime._

## API Endpoints

| Method | Path             | Purpose                          |
| ------ | ---------------- | -------------------------------- |
| POST   | `/api/interview` | Start / continue / end interview |
| GET    | `/health`        | Health check                     |

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
candidate answer → Evaluation Prompt → LLMProvider (OpenRouter/Gemini) → JSON → Evaluation Engine
                 → Session evaluations[] + topic mastery → Feedback Generator → API Response
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
- [x] LLM integration for question generation (Backend)
- [x] LLM integration for follow-up generation (Backend)
- [x] LLM integration for feedback synthesis (Backend)
- [x] Evidence-based LLM response evaluation (Backend)
- [x] Session evaluation history and per-topic mastery tracking
- [x] Evidence-based feedback metrics wired to the Feedback page
- [x] Session evaluation history and per-topic mastery tracking
- [x] Evidence-based feedback metrics wired to the Feedback page
- [x] **Evaluation pipeline traced, verified, and documented**
- [x] **LLM Provider Abstraction** (OpenRouter + Gemini support)

- [ ] Live Gemini API acceptance test with paid/upgraded API key

## Known Issues

- ⚠️ **Gemini API Free Tier Limitation**: The free tier allows only 20 requests/day per model, which causes all LLM calls to fall back to default responses when quota is exceeded. Production deployment requires a paid API key.
- ⚠️ **Fallback Detection**: System includes fallback responses to prevent crashes, but these provide zero evaluation scores and generic questions. Enhanced logging and fallback flags help detect when this occurs.

## Current Sprint

**Sprint 2 — LLM Integration & Backend Logic** (Complete)

---

---

## Adaptive Interview System (DEC-012)

### Adaptive Decision Engine

**Purpose**: Intelligently route interview flow based on candidate performance evidence.

**Decision Types**:

- `NEXT_TOPIC` - Strong answer, move forward
- `FOLLOW_UP` - Incomplete/unclear, probe deeper
- `HARDER` - High mastery, increase challenge
- `SIMPLER` - Struggling, decrease difficulty
- `END_INTERVIEW` - Sufficient evidence collected

**Thresholds**:

- Strong answer: ≥7.0/10
- Weak answer: <4.0/10
- High mastery: ≥70%
- Low mastery: <40%

**Integration Point**: Called after `EvaluationEngine` in `InterviewManager.continue_interview()`

**Safety**: Respects all existing limits (max questions, max follow-ups, duplicate detection)

### Question Difficulty Adaptation

**Mechanism**: `QuestionGenerator.generate()` accepts optional `target_difficulty` parameter from adaptive decision

**Difficulty Levels** (ordered):

1. Foundational
2. Intermediate
3. Advanced
4. Expert

**Adaptation Logic**:

- Strong performance → increase difficulty by one level
- Weak performance → decrease difficulty by one level
- Maintains current level for acceptable answers (5.0-7.9)

---

## Voice Answer Input (DEC-013)

### Client-Side Implementation

**Technology**: Web Speech API (`SpeechRecognition` / `webkitSpeechRecognition`)

**Hook**: `useVoiceRecording()` in `frontend/src/hooks/useVoiceRecording.ts`

**States**:

- `idle` - Ready to record
- `listening` - Microphone active, capturing speech
- `processing` - Transcribing audio to text
- `error` - Permission denied, no speech, or network error

**Features**:

- Real-time duration counter
- Live recording indicator with animated pulse
- Continuous recording with interim results
- Manual stop control (candidate decides when done speaking)
- Cancel option during recording
- Error messages with clear next steps

### UI Integration

**Location**: Interview Workspace answer section

**Controls**:

- **Speak Button**: Initiates recording (only shown if browser supports API)
- **Recording Indicator**: Shows elapsed time with animated red dot
- **Stop Button**: Ends recording and processes transcript
- **Cancel Button**: Aborts recording and clears transcript

**Flow**:

1. Candidate clicks "Speak"
2. Browser requests microphone permission
3. Recording starts (shows timer and indicator)
4. Candidate speaks their answer
5. Candidate clicks "Stop"
6. Transcript appears in answer textarea
7. Candidate reviews/edits transcript
8. Candidate clicks "Send Answer" (existing flow)

**Backend Impact**: None - transcript sent as regular answer string

**Graceful Degradation**:

- If API unsupported: button hidden, typed mode always available
- If permission denied: error message shown, falls back to typing
- If no speech detected: helpful error, allows retry

---

## Enhanced Question Quality System (DEC-014)

### Question Generation Enhancement

**Purpose**: Generate questions that feel like they come from a senior technical interviewer, not a generic AI chatbot.

**Key Improvements**:

1. **Comprehensive Context** (`question_prompt.py`):
   - Curriculum learning objectives (what concepts to test)
   - Tools/technologies for the topic
   - Candidate learning history (completed, skipped, struggled, attempts)
   - Experience level and years of experience
   - Job role and education

2. **Internal Blueprint Framework**:
   - Technical concept to test
   - Evidence criteria (what distinguishes shallow vs strong answers)
   - Difficulty calibration per experience level
   - Personalization based on candidate journey

3. **Engineering-Focused Questions**:
   - Test architecture, trade-offs, debugging, failure scenarios
   - Design decisions, scalability, reliability, security, cost, latency
   - Real-world implementation details and production considerations
   - Scenario-based framing over definition-based questions

4. **Anti-Patterns Prevention**:
   - Explicit rejection of generic questions ("What is X?", "Tell me about Y")
   - Preference for realistic problem contexts
   - Specific, measurable expected_points (not just topic keywords)

**Example Transformation**:

- **Before**: "What is RAG?"
- **After**: "You're building a RAG system for an internal knowledge base. How would you design the retrieval pipeline from document ingestion through context construction, and what would you do if the system frequently retrieves technically similar but irrelevant chunks?"

### Follow-up Generation Enhancement

**Purpose**: Generate follow-ups that are directly grounded in the candidate's actual answer, targeting specific gaps or misconceptions.

**Key Improvements**:

1. **Evaluation-Grounded Context** (`followup_prompt.py`):
   - Full `EvaluationResult` (scores, mastery, strengths, missing points, misconceptions)
   - Knowledge gaps explicitly identified
   - Expected points from original question
   - Previous follow-ups to avoid repetition

2. **Priority Hierarchy** for Follow-up Targeting:
   1. Correct critical misconception
   2. Probe missing critical concept
   3. Challenge unsupported claim
   4. Request implementation details
   5. Explore trade-offs
   6. Test failure scenarios
   7. Increase difficulty (for strong answers ≥7.0)

3. **Conversational Grounding**:
   - Reference specific things the candidate said (when natural)
   - Ask ONE thing (no multi-part questions)
   - Adapt to answer quality:
     - Strong (≥7.0): Increase challenge, don't ask trivial clarifications
     - Weak (<4.0): Probe missing foundations, don't jump topics
     - Misconception: Frame questions to discover understanding without revealing answer

4. **Anti-Patterns Prevention**:
   - Explicit rejection of generic follow-ups ("Can you elaborate?", "Tell me more")
   - Must target specific missing technical point from evaluation
   - Must be different from all previous follow-ups
   - Must stay within the topic

**Example Transformation**:

- **Before**: "Can you explain more about your RAG experience?"
- **After**: "You mentioned storing embeddings in a vector database and retrieving similar documents. How would you reduce the chance of irrelevant chunks being included in the final context, especially when several documents have high semantic similarity?"

### Implementation Details

**Modified Files**:

- `backend/services/prompt_builders/question_prompt.py` - Added comprehensive context, blueprint framework, engineering focus
- `backend/services/prompt_builders/followup_prompt.py` - Added evaluation grounding, priority hierarchy, conversational instructions
- `backend/modules/followup_generator.py` - Updated `generate()` signature to accept `evaluation_result`, `expected_points`, `previous_followups`
- `backend/modules/interview_manager.py` - Pass evaluation context to `FollowupGenerator` when `FOLLOW_UP` decision made

**Quality Assurance**:

- Both prompts include internal validation checkpoints
- Questions must relate to curriculum and test specific concepts
- Questions must match target difficulty and candidate experience
- Follow-ups must be grounded in candidate's actual answer
- Follow-ups must target ONE specific gap or concept
- All must be different from previous questions/follow-ups

**Expected Outcomes**:

- Interview feels like real technical conversation with senior engineer
- Questions test depth and reasoning, not just memorization
- Follow-ups are contextual and directly address demonstrated evidence
- Generic prompts completely eliminated
- Adaptive flow uses evidence to guide conversation intelligently

**Integration**: Works seamlessly with existing `AdaptiveDecisionEngine`, `EvaluationEngine`, and session management. No changes to API contracts, scoring formulas, or frontend functionality.

---
