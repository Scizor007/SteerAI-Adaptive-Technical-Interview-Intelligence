# Runtime Configuration Audit - READ-ONLY Analysis

**Date:** August 8, 2026  
**Status:** ✅ AUDIT COMPLETE

---

## Task 1: Inspect backend/.env

**Configuration Values (API keys masked):**

```bash
LLM_PROVIDER=gemini
MODEL_NAME=gemini-2.0-flash
OPENROUTER_MODEL=google/gemini-2.5-flash
GEMINI_API_KEY=<YOUR_GEMINI_API_KEY>          # ← PLACEHOLDER
OPENROUTER_API_KEY=<YOUR_OPENROUTER_API_KEY>  # ← PLACEHOLDER
```

**Key Findings:**
- **Provider selected:** `gemini`
- **Gemini API key:** Placeholder (not configured)
- **OpenRouter API key:** Placeholder (not configured)
- **Both keys are placeholders** - no real API keys configured

---

## Task 2: Inspect backend/config.py

**Provider Selection Logic:**

```python
# Line 30
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower()
```

**How it's read:**
1. Reads `LLM_PROVIDER` from environment variable
2. **Default:** `"gemini"` if variable is missing
3. Converts to lowercase

**Current runtime value:** `"gemini"` (from .env file)

**Default provider if missing:** `"gemini"`

**Other relevant values:**
```python
# Gemini configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")           # None or placeholder
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")  # Default model

# OpenRouter configuration  
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")  # None or placeholder
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "deepseek/deepseek-r1")  # Default model
```

**Note:** The .env file has `MODEL_NAME=gemini-2.0-flash`, overriding config.py's default of `gemini-2.5-flash`.

---

## Task 3: Inspect backend/services/llm_service.py

**Provider Instantiation Logic:**

```python
def __init__(self):
    self.provider: LLMProvider | None = None
    provider_name = config.LLM_PROVIDER
    
    if provider_name == "openrouter":
        from services.llm.openrouter_provider import OpenRouterProvider
        
        if not config.OPENROUTER_API_KEY or config.OPENROUTER_API_KEY.startswith("<"):
            # ← VALIDATION CHECK
            logger.error("[LLM CONFIG] CRITICAL: OPENROUTER_API_KEY is not configured!")
            self.provider = None  # ← FALLBACK MODE
        else:
            self.provider = OpenRouterProvider()  # ← NORMAL MODE
            
    elif provider_name == "gemini":
        from services.llm.gemini_provider import GeminiProvider
        
        if not config.GEMINI_API_KEY or config.GEMINI_API_KEY.startswith("<"):
            # ← VALIDATION CHECK
            logger.error("[LLM CONFIG] CRITICAL: GEMINI_API_KEY is not configured!")
            self.provider = None  # ← FALLBACK MODE
        else:
            self.provider = GeminiProvider()  # ← NORMAL MODE
    else:
        logger.error(f"[LLM CONFIG] Unknown LLM_PROVIDER '{provider_name}'")
        self.provider = None  # ← FALLBACK MODE
```

**Runtime Execution Path:**

1. **Read:** `provider_name = "gemini"` (from config.LLM_PROVIDER)
2. **Branch:** Takes `elif provider_name == "gemini"` branch
3. **Check:** `config.GEMINI_API_KEY.startswith("<")` → **TRUE** (placeholder detected)
4. **Result:** `self.provider = None` (fallback mode activated)
5. **Log:** `"CRITICAL: GEMINI_API_KEY is not configured!"`

**Provider Class Instantiated:** `None` (not `GeminiProvider()`)

**Fallback Logic:**
- No fallback forces Gemini
- If OpenRouter selected but key invalid → `provider = None`
- If Gemini selected but key invalid → `provider = None`
- Configuration is respected; validation determines whether provider is instantiated

**generate_json() execution when provider=None:**

```python
def generate_json(self, prompt: str, fallback_type: str = "question", ...):
    # ... logging ...
    
    if self.provider is None:  # ← TRUE in current configuration
        logger.warning(f"[AUDIT] Provider unavailable - returning fallback")
        return self._get_fallback(fallback_type)  # ← IMMEDIATE RETURN
    
    # This code NEVER executes when provider=None:
    # while attempts < max_attempts:
    #     response_text = self.provider.generate_text(prompt)
    #     return LLMParser.parse_json(response_text)
```

---

## Task 4: Search for Provider Instantiations

### GeminiProvider Instantiations

**File:** `backend/services/llm_service.py`  
**Line:** 50  
**Function:** `LLMService.__init__()`  
**Code:** `self.provider = GeminiProvider()`  
**Purpose:** Instantiate Gemini provider when LLM_PROVIDER=gemini AND API key is valid  
**Executed:** **NO** (API key is placeholder)

**File:** `backend/services/llm/gemini_provider.py`  
**Line:** 13  
**Function:** Class definition  
**Code:** `class GeminiProvider(LLMProvider):`  
**Purpose:** Provider class definition  
**Executed:** Class exists but not instantiated

### OpenRouterProvider Instantiations

**File:** `backend/services/llm_service.py`  
**Line:** 37  
**Function:** `LLMService.__init__()`  
**Code:** `self.provider = OpenRouterProvider()`  
**Purpose:** Instantiate OpenRouter provider when LLM_PROVIDER=openrouter AND API key is valid  
**Executed:** **NO** (LLM_PROVIDER=gemini, not openrouter)

**File:** `backend/services/llm/openrouter_provider.py`  
**Line:** 19  
**Function:** Class definition  
**Code:** `class OpenRouterProvider(LLMProvider):`  
**Purpose:** Provider class definition  
**Executed:** Class exists but not instantiated

### LLMService Instantiations

**Total occurrences:** 6

1. **File:** `backend/modules/evaluation_engine.py`  
   **Line:** 40  
   **Function:** `EvaluationEngine.__init__()`  
   **Code:** `self.llm = llm_service or LLMService()`  
   **Purpose:** Dependency injection with fallback to new instance  
   **When executed:** When EvaluationEngine is created without explicit LLMService

2. **File:** `backend/modules/feedback_generator.py`  
   **Line:** 25  
   **Function:** `FeedbackGenerator.__init__()`  
   **Code:** `self.llm = llm_service or LLMService()`  
   **Purpose:** Dependency injection with fallback to new instance  
   **When executed:** When FeedbackGenerator is created without explicit LLMService

3. **File:** `backend/modules/followup_generator.py`  
   **Line:** 21  
   **Function:** `FollowupGenerator.__init__()`  
   **Code:** `self.llm = llm_service or LLMService()`  
   **Purpose:** Dependency injection with fallback to new instance  
   **When executed:** When FollowupGenerator is created without explicit LLMService

4. **File:** `backend/modules/question_generator.py`  
   **Line:** 21  
   **Function:** `QuestionGenerator.__init__()`  
   **Code:** `self.llm = llm_service or LLMService()`  
   **Purpose:** Dependency injection with fallback to new instance  
   **When executed:** When QuestionGenerator is created without explicit LLMService

5. **File:** `backend/tests/debug/test_eval.py`  
   **Line:** 16  
   **Function:** `test_eval()`  
   **Code:** `llm = LLMService()`  
   **Purpose:** Test script  
   **When executed:** Test only

6. **File:** `backend/tests/unit/test_evaluation_engine.py`  
   **Line:** 102  
   **Function:** `TestEvaluationEngine.setUp()`  
   **Code:** `self.engine = EvaluationEngine(llm_service=FakeLLMService())`  
   **Purpose:** Unit test with mock  
   **When executed:** Unit test only

### google.generativeai Usage

**File:** `backend/services/llm/gemini_provider.py`  
**Line:** 19  
**Function:** `GeminiProvider.__init__()`  
**Code:** `import google.generativeai as genai`  
**Purpose:** Import Gemini SDK  
**Executed:** Only if GeminiProvider is instantiated (currently NO)

**File:** `backend/tests/debug/test_quota.py`  
**Line:** 1  
**Function:** Top-level import  
**Code:** `import google.generativeai as genai`  
**Purpose:** Test script for Gemini API  
**Executed:** Test only

### genai.configure Usage

**File:** `backend/services/llm/gemini_provider.py`  
**Line:** 29  
**Function:** `GeminiProvider.__init__()`  
**Code:** `genai.configure(api_key=config.GEMINI_API_KEY)`  
**Purpose:** Configure Gemini SDK with API key  
**Executed:** Only if GeminiProvider is instantiated (currently NO)

**File:** `backend/tests/debug/test_quota.py`  
**Line:** 6  
**Function:** Top-level  
**Code:** `genai.configure(api_key=os.getenv('GEMINI_API_KEY'))`  
**Purpose:** Test script  
**Executed:** Test only

### OPENROUTER_API_KEY Usage

1. **File:** `backend/config.py`  
   **Line:** 39  
   **Purpose:** Read from environment variable

2. **File:** `backend/services/llm_service.py`  
   **Lines:** 29-33  
   **Purpose:** Validation check (detects placeholder)

3. **File:** `backend/services/llm/openrouter_provider.py`  
   **Lines:** 23-26  
   **Purpose:** Store API key in provider instance

### GEMINI_API_KEY Usage

1. **File:** `backend/config.py`  
   **Line:** 35  
   **Purpose:** Read from environment variable

2. **File:** `backend/services/llm_service.py`  
   **Lines:** 42-46  
   **Purpose:** Validation check (detects placeholder) **← TRIGGERS IN CURRENT CONFIG**

3. **File:** `backend/services/llm/gemini_provider.py`  
   **Lines:** 25-29  
   **Purpose:** Configure Gemini SDK

4. **File:** `backend/tests/debug/test_quota.py`  
   **Line:** 6  
   **Purpose:** Test only

5. **File:** `backend/tests/unit/test_llm.py`  
   **Line:** 7  
   **Purpose:** Mock for unit tests

---

## Task 5: Verify Generator LLMService Usage

### InterviewManager Instantiation

**File:** `backend/modules/interview_manager.py`  
**Lines:** 76-80

```python
def __init__(self):
    # ...
    self.question_generator = QuestionGenerator()      # ← No LLMService passed
    self.followup_generator = FollowupGenerator()      # ← No LLMService passed
    self.evaluation_engine = EvaluationEngine()        # ← No LLMService passed
    self.feedback_generator = FeedbackGenerator()      # ← No LLMService passed
```

**Result:** Each generator creates its own `LLMService()` instance via the fallback pattern:
```python
self.llm = llm_service or LLMService()
```

### Do They Share the Same Instance?

**Answer:** **NO** - Each module creates a separate LLMService instance.

**Instances Created:**
1. `QuestionGenerator.llm` → New `LLMService()` instance
2. `FollowupGenerator.llm` → New `LLMService()` instance
3. `EvaluationEngine.llm` → New `LLMService()` instance
4. `FeedbackGenerator.llm` → New `LLMService()` instance

**Do they all behave the same?**

**YES** - All instances:
1. Read the same `config.LLM_PROVIDER` value (`"gemini"`)
2. Read the same `config.GEMINI_API_KEY` value (`"<YOUR_GEMINI_API_KEY>"`)
3. Detect the placeholder (starts with `<`)
4. Set `self.provider = None`
5. Use fallback mode for all operations

**Result:** All four modules use fallback responses, not actual LLM calls.

### Do Any Instantiate Their Own Provider?

**Answer:** **NO**

All modules use the `LLMService` abstraction. None directly instantiate `GeminiProvider` or `OpenRouterProvider`.

The only provider instantiation occurs in `LLMService.__init__()`, which is currently failing validation.

---

## Task 6: Identify Runtime Provider

**Current Configuration:**
- `.env`: `LLM_PROVIDER=gemini`
- `.env`: `GEMINI_API_KEY=<YOUR_GEMINI_API_KEY>` (placeholder)

**Runtime Execution:**

1. Application starts
2. `config.LLM_PROVIDER` reads `"gemini"`
3. Each module creates `LLMService()` instance
4. `LLMService.__init__()` executes:
   - Reads `provider_name = "gemini"`
   - Takes gemini branch
   - Checks `config.GEMINI_API_KEY.startswith("<")` → **TRUE**
   - Sets `self.provider = None`
   - Logs CRITICAL error

**Runtime Provider:** **NONE** (`provider = None`)

**Why:**
- Gemini is selected via configuration
- Gemini API key is a placeholder
- Validation detects placeholder
- Provider instantiation is skipped
- All operations use fallback mode

**Would OpenRouter be used?**

**NO** - Even if `OPENROUTER_API_KEY` were valid:
- Configuration has `LLM_PROVIDER=gemini`
- Code never reaches the OpenRouter branch
- OpenRouter would only be used if `.env` had `LLM_PROVIDER=openrouter`

---

## Task 7: Explain Feedback Fallback Message

**Message Displayed:**
> "The candidate completed the interview, but detailed AI evaluation was temporarily unavailable."

**Source Analysis:**

### Source File
**File:** `backend/services/llm_service.py`  
**Method:** `_get_fallback()`  
**Lines:** 117-138

```python
elif fallback_type == "feedback":
    return {
        "summary": "The candidate completed the interview, but detailed AI evaluation was temporarily unavailable.",
        # ↑ EXACT TEXT FROM FEEDBACK PAGE
        "strengths": ["Completed the assessment."],
        "gaps": ["Detailed feedback could not be generated."],
        "next": ["Review the evidence collected during the assessment."],
        "_fallback": True,
    }
```

### Execution Path

1. **Interview completes**
   ```
   InterviewManager.continue_interview()
   → Interview done, generate feedback
   ```

2. **FeedbackGenerator called**
   ```
   FeedbackGenerator.generate(evaluations, topic_mastery, score_summary)
   → Line 43: self.llm.generate_json(prompt, fallback_type="feedback", ...)
   ```

3. **LLMService.generate_json() called**
   ```
   → Line 71: if self.provider is None:  # TRUE
   → Line 73: return self._get_fallback("feedback")  # IMMEDIATE RETURN
   ```

4. **_get_fallback("feedback") returns**
   ```
   → Returns dict with fallback message
   → No LLM call made
   → No API request
   → No JSON parsing
   ```

5. **FeedbackGenerator receives fallback**
   ```python
   # backend/modules/feedback_generator.py, line 50
   response_data = self.llm.generate_json(...)
   
   # response_data = {
   #   "summary": "The candidate completed...",
   #   "_fallback": True
   # }
   
   # NO CHECK FOR _fallback FLAG
   
   return Feedback(
       summary=str(response_data.get("summary") or ""),  # ← Gets fallback text
       strengths=self._string_list(response_data.get("strengths")),
       gaps=self._string_list(response_data.get("gaps")),
       next=self._string_list(response_data.get("next")),
   )
   ```

6. **Feedback returned to frontend**
   ```
   Frontend displays: "The candidate completed the interview, but detailed AI evaluation was temporarily unavailable."
   ```

### Why Does It Come From Fallback?

**Root Cause Chain:**

1. **Configuration:** `GEMINI_API_KEY=<YOUR_GEMINI_API_KEY>` (placeholder)
2. **Validation:** LLMService detects placeholder, sets `provider = None`
3. **Fallback Mode:** All `generate_json()` calls return fallbacks
4. **No Detection:** FeedbackGenerator doesn't check `_fallback` flag
5. **Result:** Fallback message displayed as if it were real feedback

### Is It From OpenRouter or Gemini Fallback?

**Answer:** **NEITHER** - It's from `LLMService._get_fallback()`

**Not from OpenRouter because:**
- OpenRouter is not selected (`LLM_PROVIDER=gemini`)
- OpenRouter is never instantiated
- OpenRouter code is never executed

**Not from Gemini because:**
- GeminiProvider is not instantiated (API key validation failed)
- Gemini SDK is never imported
- No Gemini API calls are made

**It's from LLMService because:**
- `provider = None` due to validation failure
- `generate_json()` detects `provider is None`
- Immediately returns hardcoded fallback dict
- No provider-specific code is executed

---

## Task 8: Is Provider Selection Being Overridden?

**Answer:** **NO**

**Evidence:**

1. **Configuration reads correctly:**
   ```python
   # config.py, line 30
   LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower()
   # Result: "gemini"
   ```

2. **LLMService reads configuration correctly:**
   ```python
   # llm_service.py, line 23
   provider_name = config.LLM_PROVIDER
   # Result: "gemini"
   ```

3. **Correct branch is taken:**
   ```python
   # llm_service.py, line 39
   elif provider_name == "gemini":  # ← This branch executes
       # ...
   ```

4. **Validation prevents instantiation:**
   ```python
   if not config.GEMINI_API_KEY or config.GEMINI_API_KEY.startswith("<"):
       self.provider = None  # ← Validation check, not override
   ```

**Conclusion:**
- Configuration is respected: Gemini is selected
- No code overrides the selection to OpenRouter
- Validation prevents instantiation due to placeholder key
- This is **intended behavior** (the validation fix we implemented)

**If LLM_PROVIDER were set to openrouter:**
- Would read `"openrouter"`
- Would take OpenRouter branch
- Would check `OPENROUTER_API_KEY.startswith("<")`
- Would set `provider = None` (also a placeholder)
- Same fallback behavior

---

## Task 9: Why Feedback Comes From "Gemini Fallback"?

**Correction:** It does NOT come from "Gemini fallback" or "OpenRouter fallback"

**Accurate Description:**

The feedback comes from **`LLMService._get_fallback()`**, which is a:
- **Provider-agnostic fallback**
- **Generic safety mechanism**
- **Not specific to Gemini or OpenRouter**

**Execution Flow:**

```
FeedbackGenerator.generate()
  ↓
  calls: self.llm.generate_json(prompt, fallback_type="feedback")
  ↓
LLMService.generate_json()
  ↓
  checks: if self.provider is None
  ↓ (TRUE)
  returns: self._get_fallback("feedback")
  ↓
_get_fallback("feedback")
  ↓
  returns: {
    "summary": "The candidate completed the interview, but detailed AI evaluation was temporarily unavailable.",
    "_fallback": True
  }
  ↓
FeedbackGenerator receives fallback dict
  ↓
  Does NOT check _fallback flag
  ↓
  Creates Feedback object with fallback text
  ↓
Frontend displays fallback message
```

**Why Not a "Real" Fallback From Provider?**

Because no provider exists:
- GeminiProvider was never instantiated (validation failed)
- OpenRouterProvider was never instantiated (not selected)
- No API calls are made
- No provider-specific errors occur
- No provider-specific fallbacks are returned

The fallback is **pre-emptive** - it prevents attempting to call a null provider.

---

## Summary: Complete Execution Path

### Configuration Phase (Application Startup)

1. `.env` file loaded
2. `config.py` reads:
   - `LLM_PROVIDER = "gemini"`
   - `GEMINI_API_KEY = "<YOUR_GEMINI_API_KEY>"`
3. `InterviewManager.__init__()` creates modules
4. Each module creates `LLMService()` instance
5. `LLMService.__init__()`:
   - Reads `provider_name = "gemini"`
   - Takes gemini branch
   - Detects placeholder API key
   - Sets `self.provider = None`
   - Logs CRITICAL error

### Interview Question Phase

1. `QuestionGenerator.generate()` called
2. Calls `self.llm.generate_json(prompt, fallback_type="question")`
3. `LLMService.generate_json()`:
   - Checks `if self.provider is None` → TRUE
   - Returns `self._get_fallback("question")`
4. QuestionGenerator receives fallback with `_fallback=True`
5. **QuestionGenerator detects fallback** ✅
6. Uses topic-specific fallback question
7. Different question shown based on topic

### Evaluation Phase

1. `EvaluationEngine.evaluate()` called
2. Calls `self.llm.generate_json(prompt, fallback_type="evaluation")`
3. `LLMService.generate_json()`:
   - Checks `if self.provider is None` → TRUE
   - Returns `self._get_fallback("evaluation")`
4. EvaluationEngine receives fallback with scores=0
5. **EvaluationEngine marks fallback** ✅
6. **InterviewManager detects fallback** ✅
7. Evaluation not stored (correct behavior)

### Feedback Phase

1. Interview completes
2. `FeedbackGenerator.generate()` called
3. Calls `self.llm.generate_json(prompt, fallback_type="feedback")`
4. `LLMService.generate_json()`:
   - Checks `if self.provider is None` → TRUE
   - Returns `self._get_fallback("feedback")`
5. FeedbackGenerator receives fallback dict
6. **FeedbackGenerator does NOT check _fallback flag** ❌
7. Creates Feedback object with fallback text
8. Returns feedback with message:
   > "The candidate completed the interview, but detailed AI evaluation was temporarily unavailable."
9. Frontend displays this exact message

---

## Root Cause Conclusion

**Configuration:**
- `LLM_PROVIDER=gemini` (correct, not overridden)
- `GEMINI_API_KEY=<YOUR_GEMINI_API_KEY>` (placeholder, not real key)
- `OPENROUTER_API_KEY=<YOUR_OPENROUTER_API_KEY>` (placeholder, not used anyway)

**Runtime Provider:** `None` (no provider instantiated)

**Why:** API key validation detects placeholder, prevents instantiation

**Feedback Message Source:** `LLMService._get_fallback("feedback")` - line in llm_service.py

**Why Displayed:** FeedbackGenerator doesn't check `_fallback` flag, treats fallback as valid response

**Is Provider Selection Overridden?** NO - Gemini is correctly selected, but validation prevents instantiation

**Solution:** Add real Gemini API key to `.env`, OR add fallback detection to FeedbackGenerator

---

## Answer to "Why Still Receive Fallback Message?"

You receive the fallback message because:

1. **Both API keys are placeholders** (start with `<`)
2. **LLMService validation detects placeholders**
3. **Sets `provider = None` for safety**
4. **All LLM calls return fallbacks**
5. **QuestionGenerator handles fallback** → Uses topic questions ✅
6. **EvaluationEngine handles fallback** → Doesn't store scores ✅
7. **FeedbackGenerator does NOT handle fallback** → Displays fallback text ❌

The application is working as designed with one gap: FeedbackGenerator needs fallback detection like the other modules.

**Current behavior is NOT a bug in provider selection** - it's working correctly with no valid API keys.

The feedback message accurately reflects reality: no AI evaluation was available because no API key is configured.
