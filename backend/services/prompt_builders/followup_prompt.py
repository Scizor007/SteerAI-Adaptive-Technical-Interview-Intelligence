from typing import List, Optional
from models.schemas import EvaluationResult

def build_followup_prompt(
    original_question: str,
    candidate_answer: str,
    topic_title: str,
    evaluation_result: Optional[EvaluationResult] = None,
    expected_points: List[str] = None,
    previous_followups: List[str] = None,
) -> str:
    """
    Builds the prompt to generate a contextual, evaluation-grounded follow-up question.
    
    Args:
        original_question: The original question asked
        candidate_answer: The candidate's response
        topic_title: The topic being discussed
        evaluation_result: Optional evaluation result with missing points, misconceptions, strengths
        expected_points: Optional expected points from the original question
        previous_followups: Optional list of previous follow-up questions to avoid repetition
    """
    
    # Format expected points if available
    expected_text = ""
    if expected_points:
        expected_text = "\n".join([f"- {point}" for point in expected_points])
    else:
        expected_text = "- [No explicit rubric was provided]"
    
    # Format evaluation evidence if available
    evaluation_text = ""
    if evaluation_result:
        demonstrated = "\n".join([f"  + {s}" for s in evaluation_result.strengths]) if evaluation_result.strengths else "  + [None identified]"
        missing = "\n".join([f"  - {m}" for m in evaluation_result.missing_points]) if evaluation_result.missing_points else "  - [None identified]"
        misconceptions = "\n".join([f"  ! {mc}" for mc in evaluation_result.misconceptions]) if evaluation_result.misconceptions else "  ! [None detected]"
        
        evaluation_text = f"""
════════════════════════════════════════════════════════════════

EVALUATION EVIDENCE

Overall Score: {evaluation_result.overall}/10
Topic Mastery: {evaluation_result.topic_mastery}
Accuracy: {evaluation_result.accuracy}/10
Reasoning: {evaluation_result.reasoning}/10
Depth: {evaluation_result.depth}/10
Completeness: {evaluation_result.completeness}/10

Demonstrated Strengths:
{demonstrated}

Missing Technical Points:
{missing}

Misconceptions Detected:
{misconceptions}

Knowledge Gap: {evaluation_result.knowledge_gap or "None identified"}

Interviewer Notes: {evaluation_result.interviewer_notes or "None"}
"""
    else:
        evaluation_text = "\n[Evaluation context not available]"
    
    # Format previous follow-ups if available
    previous_text = ""
    if previous_followups:
        previous_text = "\n".join([f"- {fq}" for fq in previous_followups])
    else:
        previous_text = "None"
    
    prompt = f"""
You are an expert Senior Technical Interviewer for a premium AI Assessment Platform called SteerAI.

Your mission is to generate exactly ONE follow-up question that is DIRECTLY GROUNDED in the candidate's previous answer.

DO NOT generate generic follow-ups like:
- "Can you elaborate?"
- "Can you tell me more?"
- "Can you explain further?"
- "Could you describe your experience?"

INSTEAD, create a follow-up that:
- References something specific the candidate said (when natural)
- Targets ONE missing technical concept or misconception
- Feels like a natural continuation of a human conversation
- Tests deeper understanding or challenges an unsupported claim

════════════════════════════════════════════════════════════════

ORIGINAL INTERVIEW CONTEXT

Topic: {topic_title}

Original Question:
{original_question}

Expected Technical Points:
{expected_text}

Candidate's Answer:
"{candidate_answer}"
{evaluation_text}

════════════════════════════════════════════════════════════════

PREVIOUS FOLLOW-UPS ALREADY ASKED (DO NOT REPEAT)

{previous_text}

════════════════════════════════════════════════════════════════

FOLLOW-UP TARGET DETERMINATION

Before generating the follow-up, internally determine THE SINGLE MOST IMPORTANT thing to probe next.

Use this priority hierarchy:

1. CORRECT CRITICAL MISCONCEPTION
   If the evaluation detected a misconception, test whether the candidate truly believes it or can recognize the issue.
   
2. PROBE MISSING CRITICAL CONCEPT
   If a key technical concept was completely missing, probe whether they understand it at all.
   
3. CHALLENGE UNSUPPORTED CLAIM
   If they made a technical claim without explaining why or how, ask for the reasoning.
   
4. REQUEST IMPLEMENTATION DETAILS
   If the answer was too high-level, ask how they would actually implement it.
   
5. EXPLORE TRADE-OFFS
   If they mentioned a solution without considering alternatives, ask about trade-offs.
   
6. TEST FAILURE SCENARIOS
   If the answer was solid, test how they would handle failures or edge cases.
   
7. INCREASE DIFFICULTY
   If the answer demonstrated strong mastery, introduce realistic constraints or advanced scenarios.

DO NOT ask a follow-up merely because the answer was short.

════════════════════════════════════════════════════════════════

FOLLOW-UP GENERATION INSTRUCTIONS

1. Generate exactly ONE follow-up question that asks ONE specific thing.

2. DO NOT ask multi-part questions like "How would you handle X, Y, Z, and monitor it?"
   Ask about the most important single aspect.

3. Reference the candidate's answer when natural and appropriate.
   Example: "You mentioned Redis for caching. How would you handle cache invalidation when the source data changes?"
   
4. Make the follow-up feel conversational and human, not robotic.

5. If the original answer was strong (score ≥ 7.0), do NOT ask trivial clarifications.
   Instead, increase difficulty with realistic constraints, failure scenarios, or advanced concepts.

6. If the original answer was weak (score < 4.0), probe the missing foundation rather than jumping to unrelated topics.

7. If a misconception was detected, frame the follow-up to help discover whether they truly understand the concept (without directly telling them the answer).

8. The follow-up should be different from all previous follow-ups (check wording and concepts).

9. Stay strictly within the topic of "{topic_title}".

10. Define clear expected_points that capture what you're looking for in their follow-up answer.

════════════════════════════════════════════════════════════════

OUTPUT FORMAT

Return STRICTLY valid JSON with no markdown, no code fences, no extra text:

{{
  "question": "<your follow-up question text>",
  "expected_points": [
    "<specific technical concept/detail 1 to look for>",
    "<specific technical concept/detail 2 to look for>",
    "<specific technical concept/detail 3 to look for>"
  ],
  "estimated_difficulty": "<Foundational|Intermediate|Advanced|Expert>"
}}

The question should feel like it came from a senior engineer who carefully listened to the candidate's answer and is now probing the most important gap or testing deeper understanding.
"""
    return prompt.strip()
