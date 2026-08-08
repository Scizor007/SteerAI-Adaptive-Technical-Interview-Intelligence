# Gemini API Quota Resolution Guide

**Status**: API quota exceeded - all LLM calls returning fallbacks  
**Impact**: Evaluation returns zero scores, generic questions/follow-ups, "temporarily unavailable" feedback

---

## Quick Diagnosis

Check if you're hitting quota limits:

```bash
# Look for these error patterns in backend logs:
"429 You exceeded your current quota"
"Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests"
"Limit: 20, model: gemini-2.5-flash"
```

OR:

```bash
# Look for fallback warnings:
"Max retries reached - returning fallback"
"FALLBACK ACTIVATED"
"Question generated without expected_points"
```

---

## Solution Options

### Option 1: Upgrade to Paid Tier (RECOMMENDED for Production)

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Navigate to billing settings
3. Enable billing for your project
4. Paid tier removes the 20 request/day limit
5. No code changes needed

**Cost**: Pay-as-you-go pricing  
**Timeline**: Immediate after billing setup  
**Viability**: Required for production

---

### Option 2: Switch to Different Model (Quick Fix)

Try a different Gemini model with separate quota:

```bash
# Edit backend/.env
MODEL_NAME=gemini-1.5-flash  # Instead of gemini-2.5-flash
```

Then restart the backend:

```bash
cd backend
.\.venv\Scripts\Activate.ps1  # Windows PowerShell
# or: source .venv/bin/activate  # Linux/Mac
python main.py
```

**Cost**: Free  
**Timeline**: Immediate  
**Viability**: Temporary workaround, may have own limits

---

### Option 3: Wait for Quota Reset

Free tier quota resets daily (based on UTC time).

**Cost**: Free  
**Timeline**: Wait until next day  
**Viability**: Not suitable for active development

---

### Option 4: Mock LLM for Development (Advanced)

Create a mock LLM service for local testing:

```python
# backend/services/mock_llm_service.py
class MockLLMService:
    def generate_json(self, prompt, fallback_type="question"):
        if "evaluation" in fallback_type:
            return {
                "accuracy": 7.5,
                "reasoning": 8.0,
                "depth": 6.5,
                # ... (return realistic mock data)
            }
        # ... handle other types
```

Then use dependency injection in modules:

```python
# For testing only
from services.mock_llm_service import MockLLMService
evaluation_engine = EvaluationEngine(llm_service=MockLLMService())
```

**Cost**: Free  
**Timeline**: Requires code changes  
**Viability**: Best for development/testing workflow

---

## Verification

After implementing a solution, verify the fix:

```bash
cd backend
.\.venv\Scripts\Activate.ps1
python test_evaluation_trace.py
```

Look for:
- ✅ No 429 errors
- ✅ Real scores (not all zeros)
- ✅ Specific questions with expected_points
- ✅ No "unavailable" fallback messages

---

## Current API Configuration

Check your current setup:

```bash
# View .env settings
cd backend
cat .env  # Linux/Mac
type .env  # Windows
```

Ensure you have:
```
GEMINI_API_KEY=<your-key-here>
MODEL_NAME=gemini-2.5-flash
```

---

## Monitoring Usage

Track your API usage:
- **Google AI Studio**: https://ai.google.dev/
- **Rate Limit Dashboard**: https://ai.dev/rate-limit
- **Quota Info**: https://ai.google.dev/gemini-api/docs/rate-limits

---

## For Production Deployment

**CRITICAL**: Do NOT deploy to production with free tier API.

✅ **Required before production:**
1. Upgrade to paid Gemini API tier
2. Set up quota alerts in Google Cloud Console
3. Implement rate limiting on your backend
4. Consider caching LLM responses where appropriate
5. Monitor API costs and usage patterns

---

## Additional Resources

- [Gemini API Pricing](https://ai.google.dev/pricing)
- [Gemini API Rate Limits Documentation](https://ai.google.dev/gemini-api/docs/rate-limits)
- [Google AI Studio](https://aistudio.google.com/)
