from typing import List, Dict, Any
from models.schemas import CandidateProfile, QuestionRecord

def build_feedback_prompt(
    candidate: CandidateProfile,
    questions: List[QuestionRecord],
    overall_score: float
) -> str:
    """
    Builds the prompt to generate the final interview feedback.
    """
    
    # Format the interview transcript
    transcript_text = ""
    for idx, q in enumerate(questions):
        transcript_text += f"\n--- Question {idx + 1} (Topic: {q.topic}, Difficulty: {q.difficulty.value}) ---\n"
        transcript_text += f"Interviewer: {q.question}\n"
        answer = q.answer if q.answer else "[No answer provided]"
        transcript_text += f"Candidate: {answer}\n"
        score = q.score if q.score is not None else 0.0
        transcript_text += f"Evaluated Score: {score:.1f}/1.0\n"
        
    prompt = f"""
You are an expert Senior Technical Interviewer and Assessor for a premium AI Assessment Platform called SteerAI.

You have just concluded a technical interview with the candidate.
Candidate Name: {candidate.member.name}
Role: {candidate.member.jobRole}
Overall Calculated Score: {overall_score * 100:.1f}%

Here is the transcript of the interview and the automated evaluation scores per question:
{transcript_text}

Instructions:
1. Synthesize the candidate's performance into a final assessment.
2. Identify 2-3 specific technical strengths demonstrated in the interview.
3. Identify 1-2 specific technical gaps or areas for improvement.
4. Provide 2-3 actionable next steps or recommendations.
5. Write a professional, concise executive summary (3-4 sentences max).
6. Return the result STRICTLY as a JSON object, with no markdown formatting, no code blocks, and no conversational text.

The JSON MUST match this exact structure:
{{
  "summary": "<executive summary text>",
  "strengths": [
    "<strength 1>",
    "<strength 2>"
  ],
  "gaps": [
    "<gap 1>",
    "<gap 2>"
  ],
  "next": [
    "<recommendation 1>",
    "<recommendation 2>"
  ]
}}
"""
    return prompt.strip()
