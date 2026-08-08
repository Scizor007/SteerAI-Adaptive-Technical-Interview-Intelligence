from typing import List, Dict, Any
from models.schemas import InterviewContext, CandidateProfile, PlannedTopic

def build_question_prompt(
    topic: PlannedTopic,
    candidate: CandidateProfile,
    experience_level: str,
    questions_already_asked: List[str]
) -> str:
    """
    Builds the prompt to generate a new interview question for a specific topic.
    """
    
    # Format previously asked questions
    previous_q_text = "\n".join([f"- {q}" for q in questions_already_asked]) if questions_already_asked else "None"
    
    prompt = f"""
You are an expert Senior Technical Interviewer for a premium AI Assessment Platform called SteerAI.
Your goal is to assess a candidate on a specific topic from their curriculum.

Candidate Context:
- Name: {candidate.member.name}
- Role: {candidate.member.jobRole}
- Experience Level: {experience_level.upper()}

Current Topic:
- Title: {topic.title}
- Module: {topic.module_name}
- Curriculum Day: {topic.day}
- Target Difficulty: {topic.difficulty.value.upper()}
- Priority: {topic.priority.value.upper()}

Previously Asked Questions (DO NOT REPEAT THESE):
{previous_q_text}

Instructions:
1. Act as a senior interviewer. Ask exactly ONE question.
2. The question should match the target difficulty. If the candidate is senior/expert, make the question more architectural or complex. If they are junior, focus on fundamentals.
3. Do not reveal the answer in your question.
4. Keep it focused on the current topic.
5. Return the result STRICTLY as a JSON object, with no markdown formatting or extra text.

The JSON MUST match this exact structure:
{{
  "question": "<the actual question text>",
  "expected_points": [
    "<point 1 to look for in their answer>",
    "<point 2 to look for in their answer>"
  ],
  "estimated_difficulty": "<Foundational, Intermediate, Advanced, or Expert>"
}}
"""
    return prompt.strip()
