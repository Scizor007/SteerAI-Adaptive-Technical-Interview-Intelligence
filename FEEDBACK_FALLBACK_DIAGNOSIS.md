# Feedback Fallback - Root Cause Analysis

**Date:** August 8, 2026  
**Status:** ✅ ROOT CAUSE IDENTIFIED

---

## Problem Statement

The interview behaves correctly during Q&A:
- ✅ Different questions are generated
- ✅ Evaluation assigns 0/100 for poor answers  
- ✅ Infinite follow-up loops fixed

However, the final feedback page ALWAYS displays:
> "The candidate completed the interview, but detailed AI evaluation was temporarily unavailable."

---

## Execution Trace Results

### Question #1: Does InterviewManager call FeedbackGenerator?

**Answer:** The interview never completes in the test.

**Evidence:**
```
[TEST] Answer 5 submitted, done=False
[TEST] Interview did not complete!
```

The interview requires more than 5 answers to complete. However, this is NOT the root cause because you stated the interview DOES complete in your real testing.

---

### Question #2: Does FeedbackGenerator invoke LLMService?

**Answer:** Yes, when the interview completes, FeedbackGenerator DOES call LLMService.generate_json().

**Evidence from code inspection:**
```python
# backend/modules/feedback_generator.py
def generate(self, evaluations, topic_mastery, score_summary) -> FeedbackReport:
    prompt = build_feedback_prompt(evaluations, topic_mastery, score_summary)
    
    response_data = self.llm.generate_json(
        prompt,
        fallback_type="feedback",
        caller_module="FeedbackGenerator"
    )
```

---

### Question #3: Which provider is being used?

**Answer:** **NO PROVIDER** - Provider is `None`

**Evidence from trace:**
```
[TRACE] Provider: None
[TRACE] Provider Type: None
```

**Evidence from logs:**
```
[LLM CONFIG] Provider: gemini
[LLM CONFIG] CRITICAL: GEMINI_API_KEY is not configured!
[LLM CONFIG] Application will use fallbacks for all LLM calls
[LLM CONFIG] Set GEMINI_API_KEY in .env file
```

---

### Question #4: Why is Provider None?

**Root Cause:** API key is a placeholder string.

**Evidence from .env:**
```bash
LLM_PROVIDER=gemini
GEMINI_API_KEY=<YOUR_GEMINI_API_KEY>
```

**Code in backend/services/llm_service.py:**
```python
if config.LLM_PROVIDER == "gemini":
    if not config.GEMINI_API_KEY or config.GEMINI_API_KEY.startswith("<"):
        logger.error("[LLM CONFIG] CRITICAL: GEMINI_API_KEY is not configured!")
        self.provider = None  # ← THIS LINE
    else:
        self.provider = GeminiProvider()
```

**Result:** Because `GEMINI_API_KEY=<YOUR_GEMINI_API_KEY>` starts with `<`, the provider is set to `None`.

---

### Question #5: Does OpenRouter return a valid JSON response?

**Answer:** OpenRouter is NOT being used.

**Reason:** `LLM_PROVIDER=gemini` in `.env`, not `openrouter`.

---

### Question #6: Does LLMParser reject the response?

**Answer:** LLMParser is NEVER called because provider is `None`.

**Execution path when provider is None:**
```python
# backend/services/llm_service.py - generate_json()

if not self.provider:
    logger.warning(f"[AUDIT] Provider unavailable - returning fallback for: {fallback_type}")
    return self._get_fallback(fallback_type)  # ← IMMEDIATE RETURN
```

The method returns the fallback BEFORE attempting any LLM call or parsing.

---

### Question #7: Is an exception being swallowed?

**Answer:** NO exceptions occur.

The fallback path is a normal control flow when `provider=None`.

---

### Question #8: Is the fallback path being triggered?

**Answer:** YES - ALWAYS.

**Evidence:**
```
[TRACE] Has _fallback flag: True
[TRACE] !!! FALLBACK WAS RETURNED !!!
```

Every single LLM call (questions, evaluations, and feedback) returns fallback because `provider=None`.

---

### Question #9: What is the raw LLM response before parsing?

**Answer:** There is NO LLM response.

Provider is `None`, so no API call is made. The method immediately returns a hardcoded fallback object.

---

### Question #10: What is the parsed object?

**Answer:** The fallback object for feedback type.

**Fallback for "feedback" type:**
```python
# backend/services/llm_service.py - _get_fallback()

elif fallback_type == "feedback":
    return {
        "summary": "The candidate completed the interview, but detailed AI evaluation was temporarily unavailable.",
        "strengths": [
            "Completed the interview process",
            "Provided responses to all questions"
        ],
        "gaps": [
            "AI evaluation service was not available"
        ],
        "next": [
            "Please retry the assessment when the service is restored",
            "Contact support if this issue persists"
        ],
        "_fallback": True,
    }
```

**This exact text appears on the feedback page.**

---

## The Exact Line Causing Fallback

**File:** `backend/services/llm_service.py`  
**Method:** `generate_json()`  
**Lines:**

```python
def generate_json(self, prompt: str, fallback_type: str = "question", caller_module: str = "unknown"):
    # ... audit logging ...
    
    if not self.provider:  # ← Line 1: Condition check
        logger.warning(f"[AUDIT] Provider unavailable - returning fallback for: {fallback_type}")
        return self._get_fallback(fallback_type)  # ← Line 2: IMMEDIATE FALLBACK RETURN
```

**Specifically:** The `return self._get_fallback(fallback_type)` line returns the fallback message that appears on the feedback page.

---

## Why Does Provider == None?

**File:** `backend/services/llm_service.py`  
**Method:** `__init__()`  
**Lines:**

```python
if config.LLM_PROVIDER == "gemini":
    if not config.GEMINI_API_KEY or config.GEMINI_API_KEY.startswith("<"):  # ← Detects placeholder
        logger.error("[LLM CONFIG] CRITICAL: GEMINI_API_KEY is not configured!")
        logger.error("[LLM CONFIG] Application will use fallbacks for all LLM calls")
        logger.error("[LLM CONFIG] Set GEMINI_API_KEY in .env file")
        self.provider = None  # ← THIS LINE CAUSES provider=None
```

**The condition `config.GEMINI_API_KEY.startswith("<")` is TRUE** because:
```bash
GEMINI_API_KEY=<YOUR_GEMINI_API_KEY>
```

---

## Complete Execution Flow

1. **Application starts**
   ```
   LLMService.__init__()
   → Reads config.GEMINI_API_KEY = "<YOUR_GEMINI_API_KEY>"
   → Detects placeholder (starts with "<")
   → Sets self.provider = None
   → Logs CRITICAL warning
   ```

2. **Interview progresses**
   ```
   Every LLM call:
   → LLMService.generate_json() is called
   → Checks if self.provider exists
   → self.provider == None
   → IMMEDIATE return of fallback object
   → No API call made
   → No parsing attempted
   ```

3. **Interview completes**
   ```
   FeedbackGenerator.generate()
   → Calls self.llm.generate_json(prompt, fallback_type="feedback")
   → LLMService returns feedback fallback
   → FeedbackGenerator receives:
      {
        "summary": "The candidate completed the interview, but detailed AI evaluation was temporarily unavailable.",
        ...
      }
   → This exact text is shown on feedback page
   ```

---

## Why Questions and Evaluations Work

You stated:
> "The interview now behaves correctly. Different questions are generated. The evaluation engine correctly assigns 0/100 for poor answers."

**Explanation:**

### Questions
- LLMService returns fallback with `_fallback=True`
- QuestionGenerator detects the fallback flag
- QuestionGenerator uses topic-specific fallback questions (9 patterns)
- Different fallback questions shown based on topic
- Appears to work correctly from user perspective

**Code:**
```python
# backend/modules/question_generator.py
if is_fallback or self._is_duplicate(question_text, questions_already_asked):
    question_text = self._create_topic_fallback(topic, experience_level)
```

### Evaluations
- LLMService returns evaluation fallback with all scores = 0
- EvaluationEngine marks it with `_fallback=True`
- InterviewManager detects fallback and doesn't store evaluation
- Interview progresses without storing invalid scores
- From user perspective: interview continues, but no evaluations stored

**Code:**
```python
# backend/modules/interview_manager.py
is_fallback = getattr(evaluation_result, '_fallback', False)

if is_fallback:
    logger.warning("[INTERVIEW] Evaluation unavailable for question, continuing interview")
    # Don't store fallback evaluations
else:
    state.evaluations.append(...)
```

### Feedback
- FeedbackGenerator has NO fallback detection logic
- FeedbackGenerator receives the fallback object
- FeedbackGenerator treats it as a valid LLM response
- FeedbackGenerator creates FeedbackReport with fallback text
- Fallback message displayed on frontend

**Code:**
```python
# backend/modules/feedback_generator.py
def generate(self, evaluations, topic_mastery, score_summary) -> FeedbackReport:
    response_data = self.llm.generate_json(prompt, fallback_type="feedback", ...)
    
    # NO CHECK FOR _fallback FLAG HERE
    
    return FeedbackReport(
        summary=str(response_data.get("summary") or ""),
        strengths=self._string_list(response_data.get("strengths")),
        gaps=self._string_list(response_data.get("gaps")),
        next=self._string_list(response_data.get("next")),
    )
```

---

## Summary

### Root Cause Chain

1. **Configuration Issue:**
   - `GEMINI_API_KEY=<YOUR_GEMINI_API_KEY>` (placeholder)

2. **Validation Triggers:**
   - LLMService detects placeholder (starts with `<`)
   - Sets `provider=None`

3. **Fallback Always Active:**
   - All LLM calls return fallback objects
   - No actual API calls made

4. **Question Generator Handles It:**
   - Detects `_fallback` flag
   - Uses topic-specific fallbacks
   - Works correctly

5. **Evaluation Engine Handles It:**
   - Detects `_fallback` flag
   - Doesn't store evaluations
   - Works correctly

6. **Feedback Generator Does NOT Handle It:**
   - NO `_fallback` flag check
   - Treats fallback as valid response
   - Displays fallback message

---

## The Exact Answer

**Question:** Where does the fallback message appear?

**Answer:** `backend/services/llm_service.py`, line in `_get_fallback()` method:

```python
elif fallback_type == "feedback":
    return {
        "summary": "The candidate completed the interview, but detailed AI evaluation was temporarily unavailable.",
        # ↑ THIS EXACT STRING appears on feedback page
```

**Question:** Why is this fallback triggered?

**Answer:** Because `provider=None` due to placeholder API key, and FeedbackGenerator doesn't check for the `_fallback` flag like QuestionGenerator and InterviewManager do.

---

## Solution (DO NOT IMPLEMENT YET)

To fix this, FeedbackGenerator needs the same fallback detection as the other modules:

```python
# backend/modules/feedback_generator.py
def generate(self, evaluations, topic_mastery, score_summary) -> FeedbackReport:
    response_data = self.llm.generate_json(prompt, fallback_type="feedback", ...)
    
    # ADD THIS CHECK:
    is_fallback = response_data.get("_fallback", False)
    if is_fallback:
        # Return a deterministic feedback based on stored evaluations
        # OR raise an exception
        # OR return a clear "evaluation unavailable" report
        pass
```

But the REAL solution is:

**Add a valid Gemini API key to `.env`:**
```bash
GEMINI_API_KEY=AIzaSy...actual_key_here
```

Then the provider will be initialized and all LLM calls will work properly.

---

## Verification Commands

To confirm this diagnosis, check the logs at startup:

```bash
cd backend
python main.py
```

You should see:
```
[LLM CONFIG] CRITICAL: GEMINI_API_KEY is not configured!
[LLM CONFIG] Application will use fallbacks for all LLM calls
```

This confirms the root cause.
