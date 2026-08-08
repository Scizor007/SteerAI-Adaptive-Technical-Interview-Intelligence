# HANDOFF.md — Current Project State

> Last updated: 2026-08-08

---

## Current Task

**Complete.** The LLM provider abstraction has been implemented. `LLMService` now routes requests to either `OpenRouterProvider` or `GeminiProvider` based on environment variables, leaving all business logic and prompts identical. OpenRouter via REST API is active.

## Next Phase

**Adaptive interview logic.** `EvaluationResult` now exposes `needs_followup`, `difficulty_recommendation`, and `knowledge_gap`; the next milestone may consume these signals to adapt interview progression.

## Current Blocker

The repository virtual environment references a missing Python 3.11 executable. Backend compilation and tests pass with the bundled workspace Python; restore or recreate `backend/.venv` before running the local FastAPI server.

## Next AI Instruction

1. Consume `EvaluationResult.needs_followup`, `difficulty_recommendation`, and `knowledge_gap` in a dedicated adaptive-planning pass.
2. Keep feedback grounded in `state.evaluations` and `state.topic_mastery`; never use candidate completion signals in the final score.

## Last Modified Files

| File | Change |
|------|--------|
| `backend/config.py` | Added LLM_PROVIDER, OPENROUTER_API_KEY, and OPENROUTER_MODEL. |
| `backend/services/llm/provider.py` | New `LLMProvider` abstract base class. |
| `backend/services/llm/openrouter_provider.py` | New OpenRouter REST API implementation. |
| `backend/services/llm/gemini_provider.py` | Encapsulated Gemini SDK implementation. |
| `backend/services/llm_service.py` | Refactored to delegate to provider while keeping parsing and fallbacks intact. |

---
