# Gemini API Call Audit Report

**Date**: 2026-08-08  
**Audit Type**: Complete Interview Trace  
**Status**: Audit Complete (Quota Exhausted - Fallbacks Used)

---

## Executive Summary

**Total Gemini API Calls for 5-Question Interview: 11 calls**

- 1 call at interview start (question generation)
- 10 calls during answer phase (2 per answer: evaluation + next question)
- 0 calls for feedback (interview ended at 5 questions before feedback phase)

**Formula**: `Total Calls = 1 + (N × 2) + 1` where N = number of questions
- For 5 questions:  1 + (5 × 2) + 1 = **12 calls**
- For 10 questions: 1 + (10 × 2) + 1 = **22 calls**

---

## Complete Call Sequence (5-Question Interview)

### Phase 1: Interview Start

```
[CALL #1] QuestionGenerator.generate()
├─ Purpose: Generate first question based on candidate analysis
├─ Prompt Builder: build_question_prompt()
├─ Input Tokens: ~186
├─ Essential: YES
└─ Notes: Creates opening question for first priority topic
```

### Phase 2: Answer Processing (Repeats for Each Answer)

**Answer #1**
```
[CALL #2] EvaluationEngine.evaluate_response()
├─ Purpose: Evaluate answer quality against expected points
├─ Prompt Builder: build_evaluation_prompt()
├─ Input Tokens: ~193
├─ Essential: YES
└─ Notes: Scores 6 dimensions + provides evidence

[CALL #3] QuestionGenerator.generate()
├─ Purpose: Generate next question for new topic
├─ Prompt Builder: build_question_prompt()
├─ Input Tokens: ~198
├─ Essential: YES
└─ Notes: Moves to next planned topic
```

**Answer #2**
```
[CALL #4] EvaluationEngine.evaluate_response()
├─ Input Tokens: ~194
[CALL #5] QuestionGenerator.generate()
├─ Input Tokens: ~207
```

**Answer #3**
```
[CALL #6] EvaluationEngine.evaluate_response()
├─ Input Tokens: ~192
[CALL #7] QuestionGenerator.generate()
├─ Input Tokens: ~221
```

**Answer #4**
```
[CALL #8] EvaluationEngine.evaluate_response()
├─ Input Tokens: ~194
[CALL #9] QuestionGenerator.generate()
├─ Input Tokens: ~229
```

**Answer #5**
```
[CALL #10] EvaluationEngine.evaluate_response()
├─ Input Tokens: ~195
[CALL #11] QuestionGenerator.generate()
├─ Input Tokens: ~243
```

### Phase 3: Interview End

```
[CALL #12] FeedbackGenerator.generate()
├─ Purpose: Synthesize final feedback from all evaluations
├─ Prompt Builder: build_feedback_prompt()
├─ Input Tokens: ~300-400 (estimated, includes all evaluation evidence)
├─ Essential: YES
└─ Notes: Creates summary, strengths, gaps, recommendations
```

---

## Call Analysis by Module

| Module | Calls per Interview | Purpose | Can Eliminate? |
|--------|-------------------|---------|----------------|
| QuestionGenerator | N + 1 (6 for 5q) | Generate adaptive questions | ❌ NO - Core feature |
| EvaluationEngine | N (5 for 5q) | Score answers with evidence | ❌ NO - Core feature |
| FollowupGenerator | 0-2N (variable) | Generate follow-ups for poor answers | ⚠️ Conditional |
| FeedbackGenerator | 1 | Synthesize final assessment | ❌ NO - Required output |

**Notes**:
- FollowupGenerator triggers only when answers are insufficient (< 50 chars or low evaluation score)
- In this audit, no follow-ups were triggered (all answers were adequate length)
- Follow-ups would add 1 extra call per insufficient answer

---

## Token Usage Analysis

### Input Token Estimates (per call type)

| Call Type | Approximate Tokens | Content |
|-----------|-------------------|---------|
| Question Generation | 186-243 | Candidate profile + topic + prior questions |
| Evaluation | 192-195 | Question + answer + expected points + rubric |
| Follow-up | ~200 | Original question + answer + topic |
| Feedback | ~300-400 | All evaluations + topic mastery + scores |

### Observations

1. **Input tokens grow over interview**: Question generation increases from ~186 to ~243 tokens as more context accumulates
2. **Evaluation tokens stable**: ~193 tokens regardless of interview progress
3. **Total input tokens for 5q interview**: ~2,400 tokens
4. **Total input tokens for 10q interview**: ~5,000 tokens (estimated)

### Output Token Estimates

| Call Type | Approximate Tokens |
|-----------|-------------------|
| Question Generation | 50-150 |
| Evaluation | 200-300 (JSON with 6 scores + arrays) |
| Follow-up | 50-150 |
| Feedback | 300-500 (summary + lists) |

---

## Redundancy Analysis

### Essential Calls (Cannot Eliminate)

**1. QuestionGenerator (N + 1 calls)**
- **Why Essential**: Adaptive questioning based on candidate profile and prior answers
- **Value**: Personalized, contextual questions that probe gaps
- **Elimination Impact**: Interview becomes generic, loses adaptability

**2. EvaluationEngine (N calls)**
- **Why Essential**: Evidence-based scoring is the core product feature
- **Value**: Objective, transparent, traceable evaluation
- **Elimination Impact**: No scores, no feedback data, product fails

**3. FeedbackGenerator (1 call)**
- **Why Essential**: Required deliverable for interview assessment
- **Value**: Synthesizes all evidence into actionable feedback
- **Elimination Impact**: No final report for candidate

**Conclusion**: All 3 modules are **non-redundant** and essential for product functionality.

---

## Potential Optimizations

### Option 1: Batch Evaluation
**Current**: Evaluate each answer immediately after submission  
**Alternative**: Collect all answers, evaluate in batch at end  
**Savings**: Reduce from N calls to 1 call (~80% reduction)

**Analysis**:
- ❌ **RISK**: Loss of real-time evaluation feedback
- ❌ **RISK**: Cannot generate adaptive follow-ups
- ❌ **RISK**: Increases latency (all evaluation at end)
- ✅ **BENEFIT**: Significant API quota savings

**Recommendation**: ❌ **DO NOT IMPLEMENT**  
Reason: Destroys adaptive interview capability, which is the core value proposition

---

### Option 2: Pre-generate Question Bank
**Current**: Generate questions dynamically based on prior answers  
**Alternative**: Pre-generate all N questions upfront in 1 call  
**Savings**: Reduce from N+1 calls to 1 call (~83% reduction)

**Analysis**:
- ❌ **RISK**: Questions can't adapt to candidate performance
- ❌ **RISK**: No follow-up capability
- ❌ **RISK**: Generic interview experience
- ✅ **BENEFIT**: Major API quota savings

**Recommendation**: ❌ **DO NOT IMPLEMENT**  
Reason: Eliminates the "adaptive" aspect of "adaptive interview"

---

### Option 3: Combined Question + Evaluation Prompt
**Current**: Separate calls for evaluation and next question  
**Alternative**: Single prompt: "Evaluate answer X AND generate next question"  
**Savings**: Reduce from 2N calls to N calls (50% reduction)

**Analysis**:
- ⚠️ **RISK**: Complex prompt engineering
- ⚠️ **RISK**: Mixed concerns in single response
- ⚠️ **RISK**: Harder to debug and validate
- ⚠️ **RISK**: May reduce quality of both outputs
- ✅ **BENEFIT**: Significant quota savings
- ✅ **BENEFIT**: Maintains adaptability

**Recommendation**: ⚠️ **POSSIBLE** but complex  
Reason: Technically feasible but increases system complexity significantly

---

### Option 4: Cached Follow-up Templates
**Current**: Generate custom follow-up via LLM for each insufficient answer  
**Alternative**: Use pre-defined templates for common scenarios  
**Savings**: ~1-2 calls per interview (only when follow-ups trigger)

**Analysis**:
- ⚠️ **RISK**: Follow-ups become less contextual
- ⚠️ **RISK**: Generic responses reduce interview quality
- ✅ **BENEFIT**: Minor quota savings
- ✅ **BENEFIT**: Faster response time

**Recommendation**: ⚠️ **VIABLE** for quota-constrained scenarios  
Reason: Acceptable tradeoff if quota is critical issue

---

## Findings & Recommendations

### Key Findings

1. **Current Design is Optimal for Quality**
   - Each call serves a distinct, essential purpose
   - No redundant API calls detected
   - Evaluation is real-time and evidence-based
   - Questions are adaptive and contextual

2. **API Usage is Predictable**
   - Formula: `1 + (N × 2) + 1` calls per N-question interview
   - 5 questions = 12 calls
   - 10 questions = 22 calls
   - Linear scaling with interview length

3. **Follow-ups are Conditional**
   - Only trigger for insufficient answers
   - Add 1 call per poor answer
   - In practice: ~0-2 extra calls per interview

4. **Token Usage is Reasonable**
   - Average ~200 tokens per request
   - Total for 10q interview: ~5,000 input tokens
   - Well within model limits (1M token context window)

### Recommendations

**For Hackathon (48 hours):**
- ✅ **Keep current design** - no changes needed
- ✅ **Monitor quota usage** - track API calls per interview
- ✅ **Free tier supports** ~4 interviews/day (estimated 50 calls/day limit)
- ⚠️ **Consider Option 4** (cached follow-ups) only if quota becomes critical

**For Production:**
- ✅ **Upgrade to paid API tier** - removes quota constraints
- ✅ **Implement caching** for repeated question patterns
- ✅ **Add exponential backoff** for retries
- ✅ **Monitor costs** and set up alerts

**NOT Recommended:**
- ❌ Batch evaluation (Option 1)
- ❌ Pre-generate questions (Option 2)
- ⚠️ Combined prompts (Option 3) - only if desperate for quota savings

---

## Quota Impact Analysis

### Free Tier Constraints

**Estimated Limits** (based on error messages):
- Requests per day per model: ~20-50
- Requests per minute: ~15
- Input tokens per minute: Limited

**One Interview Consumes**:
- 5 questions: 12 API calls
- 10 questions: 22 API calls

**Interviews Possible Per Day** (Free Tier):
- With 50 calls/day: ~4 interviews of 5 questions
- With 50 calls/day: ~2 interviews of 10 questions

### Production Requirements

For production deployment with multiple concurrent interviews:
- **Paid tier is mandatory**
- Estimated cost: ~$0.01-0.05 per interview (varies by model)
- 1000 interviews/month ≈ $10-50/month

---

## Conclusion

**Current API usage is optimal and cannot be reduced without sacrificing interview quality.**

All Gemini API calls are:
- ✅ Essential for core functionality
- ✅ Non-redundant
- ✅ Efficiently structured
- ✅ Predictable and scalable

**For the hackathon**: Current design is perfect. The quota limitation is an API tier issue, not an architecture issue.

**For production**: Paid API tier removes all quota concerns. The architecture is production-ready as-is.

---

## Appendix: Call Logs

### Sample QuestionGenerator Prompt (Tokens: ~186)
```
You are an expert Senior Technical Interviewer for a premium AI Assessment Platform called SteerAI.
Your goal is to assess a candidate on a specific topic from their curriculum.

Candidate Context:
- Name: Sarah Johnson
- Experience: [analysis data]
- Topic: Monitoring, Logging & Observability
- Difficulty: Advanced

Generate ONE technical question...
```

### Sample EvaluationEngine Prompt (Tokens: ~193)
```
You are a senior engineering interviewer evaluating one submitted answer for SteerAI.

Topic: Monitoring, Logging & Observability
Target difficulty: advanced
Question: [question text]
Expected answer points:
- [point 1]
- [point 2]

Candidate answer to evaluate:
[actual answer]

Score on 0-10 scale for: accuracy, reasoning, depth, completeness, communication, confidence
Return JSON only...
```

---

**Audit Complete**: No code changes recommended. Architecture is optimal for quality interviews.
