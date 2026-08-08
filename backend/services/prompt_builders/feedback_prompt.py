from typing import Dict, List

from models.schemas import EvaluationEvidence, InterviewScoreSummary

def build_feedback_prompt(
    evaluations: List[EvaluationEvidence],
    topic_mastery: Dict[str, float],
    score_summary: InterviewScoreSummary,
) -> str:
    """
    Builds the prompt to generate the final interview feedback.
    """
    
    evidence_text = ""
    for idx, evidence in enumerate(evaluations):
        result = evidence.evaluation_result
        evidence_text += f"\n--- Answer {idx + 1}: {evidence.topic} ---\n"
        evidence_text += f"Question: {evidence.question}\n"
        evidence_text += f"Answer: {evidence.candidate_answer}\n"
        evidence_text += f"Scores: accuracy={result.accuracy}, reasoning={result.reasoning}, depth={result.depth}, communication={result.communication}\n"
        evidence_text += f"Strengths: {', '.join(result.strengths) or 'None'}\n"
        evidence_text += f"Missing points: {', '.join(result.missing_points) or 'None'}\n"
        evidence_text += f"Misconceptions: {', '.join(result.misconceptions) or 'None'}\n"
        
    prompt = f"""
You are an expert Senior Technical Interviewer and Assessor for a premium AI Assessment Platform called SteerAI.

Generate a final assessment ONLY from the interview evidence below. Do not use or infer profile, curriculum completion, employment history, or unobserved skills.
Overall evidence-based score: {score_summary.overall_score:.1f}%
Topic mastery: {topic_mastery}
Evidence:
{evidence_text}

Instructions:
1. Synthesize the candidate's demonstrated performance into a final assessment.
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
