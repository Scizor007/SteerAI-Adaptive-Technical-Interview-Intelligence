from typing import List, Dict, Any
from models.schemas import InterviewContext, CandidateProfile, PlannedTopic, Difficulty

def build_question_prompt(
    topic: PlannedTopic,
    candidate: CandidateProfile,
    experience_level: str,
    questions_already_asked: List[str],
    target_difficulty: Difficulty = None,
) -> str:
    """
    Builds the prompt to generate a new interview question for a specific topic.
    
    Args:
        topic: The planned topic
        candidate: Candidate profile
        experience_level: Experience level string
        questions_already_asked: List of previous questions
        target_difficulty: Optional difficulty override from adaptive engine
    """
    
    # Use target difficulty if provided, otherwise use topic's difficulty
    effective_difficulty = target_difficulty or topic.difficulty
    
    # Format previously asked questions
    previous_q_text = "\n".join([f"- {q}" for q in questions_already_asked]) if questions_already_asked else "None"
    
    # Format learning objectives
    objectives_text = "\n".join([f"- {obj}" for obj in topic.objectives]) if topic.objectives else "- [General understanding of the topic]"
    
    # Format tools
    tools_text = ", ".join(topic.tools) if topic.tools else "None specified"
    
    # Build candidate learning history for this topic
    candidate_history = ""
    for mission in candidate.missions:
        if mission.day == topic.day:
            status = "COMPLETED" if mission.passed else ("SKIPPED" if mission.skipped else "FAILED")
            attempts_info = f" (attempts: {mission.attempts})" if mission.attempts else ""
            candidate_history = f"- Day {mission.day} '{mission.title}': {status}{attempts_info}"
            break
    
    if not candidate_history:
        candidate_history = f"- Day {topic.day} '{topic.title}': NOT ATTEMPTED"
    
    prompt = f"""
You are an expert Senior Technical Interviewer for a premium AI Assessment Platform called SteerAI.

Your mission is to generate ONE technical question that feels like it comes from a real senior engineer conducting a technical interview.

CRITICAL: VARY YOUR QUESTION STYLE AND STRUCTURE. Every question should feel fresh and different.

❌ DO NOT use repetitive openings like:
- "As a Software Engineer working with..."
- "As a [role] working with..."  
- "In your role as..."
- "Imagine you are..."
- "You are a Software Engineer..."

✅ DO ask questions directly and naturally:
- "How would you..."
- "What's your approach to..."
- "Walk me through..."
- "Compare X and Y for..."
- "Design a system that..."
- "Your app is experiencing X. How do you debug this?"

IMPORTANT: Check the previously asked questions below and make sure your new question:
- Uses a DIFFERENT opening style
- Tests a DIFFERENT technical concept
- Has DIFFERENT wording and structure
- Approaches the topic from a DIFFERENT angle

════════════════════════════════════════════════════════════════

CANDIDATE CONTEXT

Name: {candidate.member.name}
Role: {candidate.member.jobRole}
Experience Level: {experience_level.upper()} ({candidate.member.yearsExperience} years)
Education: {candidate.member.education}

Candidate's Learning Journey for This Topic:
{candidate_history}

════════════════════════════════════════════════════════════════

TOPIC TO ASSESS

Title: {topic.title}
Module: {topic.module_name}
Curriculum Day: {topic.day}
Target Difficulty: {effective_difficulty.value.upper()}
Priority: {topic.priority.value.upper()}

Learning Objectives:
{objectives_text}

Relevant Tools/Technologies:
{tools_text}

════════════════════════════════════════════════════════════════

QUESTIONS ALREADY ASKED (DO NOT REPEAT OR REPHRASE THESE)

{previous_q_text}

════════════════════════════════════════════════════════════════

INTERNAL QUESTION BLUEPRINT (DO NOT EXPOSE TO CANDIDATE)

Before generating the final question, internally determine:

1. TECHNICAL CONCEPT TO TEST
   What specific technical concept from the learning objectives should this question probe?

2. EVIDENCE CRITERIA
   What would distinguish a shallow answer from a strong answer?
   What technical details, reasoning, or trade-offs should a qualified candidate demonstrate?

3. QUESTION ANGLE
   Choose ONE angle that tests engineering thinking:
   - How would you build/design/implement this?
   - What happens when X fails or scales?
   - How do you choose between X and Y?
   - Debug this realistic problem
   - What trade-offs would you consider?
   - How would you optimize for X constraint?
   - Walk through your decision-making process

4. DIFFICULTY CALIBRATION
   - FOUNDATIONAL: Test basic understanding and core concepts
   - INTERMEDIATE: Test implementation knowledge and practical application
   - ADVANCED: Test architecture, trade-offs, debugging, and design decisions
   - EXPERT: Test production scenarios, failure handling, scaling, and deep system knowledge

5. PERSONALIZATION
   Adapt the question to the candidate's experience level and learning history.
   If they completed this topic, probe deeper.
   If they skipped it, assess foundational understanding.
   If they struggled (multiple attempts), start at appropriate depth.

════════════════════════════════════════════════════════════════

QUESTION GENERATION INSTRUCTIONS

1. Generate exactly ONE question that tests engineering reasoning, not memorization.

2. VARY YOUR QUESTION STYLE. Do NOT use the same opening for every question. Mix these approaches:
   
   **Direct Technical Question:**
   "How would you approach building a vector search system that needs to handle 10 million embeddings?"
   
   **Scenario-Based:**
   "You're debugging a RAG pipeline that returns irrelevant results 40% of the time. Walk me through your diagnostic process."
   
   **Design Challenge:**
   "Design a chunking strategy for a technical documentation system. What factors would influence your chunk size?"
   
   **Trade-off Discussion:**
   "When would you choose semantic search over keyword search for a knowledge base?"
   
   **Problem-Solving:**
   "Your vector database query latency jumped from 100ms to 2 seconds after adding 5M new documents. How do you fix this?"
   
   **Architecture Decision:**
   "Compare in-memory vector stores vs. persistent vector databases for a production RAG system."
   
   **Implementation Detail:**
   "Explain your approach to handling embeddings that need to be updated when source documents change."
   
   AVOID REPETITIVE PATTERNS LIKE:
   ❌ "As a Software Engineer working with..."
   ❌ "In your role as..."
   ❌ "Imagine you are..."
   
   Just ask the question directly and naturally.

3. The question should have clear technical purpose and test specific concepts from the learning objectives.

4. Match the target difficulty level ({effective_difficulty.value.upper()}).
   {experience_level.upper()} candidates should face {experience_level}-appropriate depth.

5. Do not reveal the answer in the question.

6. Ensure the question is COMPLETELY DIFFERENT from all previously asked questions:
   - Different topic/concept
   - Different question style
   - Different wording/structure
   - Different technical angle

7. Define clear expected_points that capture the technical evidence you're looking for in a strong answer.
   These should be specific, measurable indicators of understanding (not just topic keywords).

════════════════════════════════════════════════════════════════

OUTPUT FORMAT

Return STRICTLY valid JSON with no markdown, no code fences, no extra text:

{{
  "question": "<your generated question text>",
  "expected_points": [
    "<specific technical concept/detail 1 to look for>",
    "<specific technical concept/detail 2 to look for>",
    "<specific technical concept/detail 3 to look for>",
    "<specific technical concept/detail 4 to look for>"
  ],
  "estimated_difficulty": "<Foundational|Intermediate|Advanced|Expert>"
}}

Expected points should capture:
- Key technical concepts that should be mentioned
- Critical trade-offs or considerations
- Implementation details that demonstrate depth
- Common pitfalls or misconceptions to avoid
"""
    return prompt.strip()
