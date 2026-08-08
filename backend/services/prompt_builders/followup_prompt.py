def build_followup_prompt(
    original_question: str,
    candidate_answer: str,
    topic_title: str
) -> str:
    """
    Builds the prompt to generate a follow-up question.
    """
    
    prompt = f"""
You are an expert Senior Technical Interviewer for a premium AI Assessment Platform called SteerAI.

You asked the candidate the following question on the topic "{topic_title}":
Question: "{original_question}"

The candidate provided the following answer:
Answer: "{candidate_answer}"

Instructions:
1. Generate exactly ONE follow-up question.
2. The follow-up must probe their reasoning, clarify ambiguity, or increase the depth of the technical discussion.
3. NEVER repeat the original question.
4. Stay strictly on the topic of "{topic_title}".
5. Return the result STRICTLY as a JSON object, with no markdown formatting or extra text.

The JSON MUST match this exact structure:
{{
  "question": "<the follow-up question text>",
  "expected_points": [
    "<point 1 to look for in their follow-up answer>",
    "<point 2 to look for in their follow-up answer>"
  ],
  "estimated_difficulty": "<Foundational, Intermediate, Advanced, or Expert>"
}}
"""
    return prompt.strip()
