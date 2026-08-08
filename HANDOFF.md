# HANDOFF.md — Current Project State

> Last updated: 2026-08-08

---

## Current Task

**Complete.** The real Evaluation Engine is implemented. Every answer is independently evaluated by Gemini against the stored question rubric, normalized by backend rules, appended to session evidence, and used to calculate topic mastery plus the final 0–100 report score.

## Next Phase

**Adaptive interview logic.** `EvaluationResult` now exposes `needs_followup`, `difficulty_recommendation`, and `knowledge_gap`; the next milestone may consume these signals to adapt interview progression.

## Current Blocker

The repository virtual environment references a missing Python 3.11 executable. Backend compilation and tests pass with the bundled workspace Python; restore or recreate `backend/.venv` before running the local FastAPI server.

## Next AI Instruction

1. Consume `EvaluationResult.needs_followup`, `difficulty_recommendation`, and `knowledge_gap` in a dedicated adaptive-planning pass.
2. Recreate `backend/.venv`, install backend dependencies, and run a live Gemini API acceptance test.
3. Keep feedback grounded in `state.evaluations` and `state.topic_mastery`; never use candidate completion signals in the final score.

## Last Modified Files

| File | Change |
|------|--------|
| `backend/services/prompt_builders/evaluation_prompt.py` | New constrained per-answer evaluation prompt. |
| `backend/modules/evaluation_engine.py` | Gemini JSON validation, weighted evaluation, mastery, and aggregate score calculation. |
| `backend/models/schemas.py` | Added evaluation evidence, result, and score-summary schemas. |
| `backend/modules/interview_manager.py` | Stores every answer evaluation and builds reports from evidence. |
| `backend/modules/feedback_generator.py` | Returns backend-computed metric dimensions and evidence-only report data. |
| `frontend/src/hooks/useInterviewUI.ts` | Uses the real interview API instead of mock questions. |
| `frontend/src/features/feedback/FeedbackPage.tsx` | Displays backend report metrics and topic mastery. |
| `backend/test_evaluation_engine.py` | Covers excellent, average, poor, empty, off-topic, and complete interview score separation. |

---
