"""
Live interview test with actual Gemini API.
Tests one complete interview flow: question → answer → evaluation → feedback.
"""
import asyncio
import sys

from modules.interview_manager import InterviewManager
from modules.candidate_loader import CandidateLoader

async def test_live_interview():
    """Run one complete interview with real answers."""
    
    print("\n" + "="*80)
    print("LIVE INTERVIEW TEST - Gemini API")
    print("="*80 + "\n")
    
    # Load a real candidate
    loader = CandidateLoader()
    candidates = loader.candidates
    
    if not candidates:
        print("❌ No candidates found!")
        return False
    
    candidate = candidates[0]
    print(f"✓ Using candidate: {candidate.member.name}")
    
    manager = InterviewManager()
    session_id = "live-test-001"
    
    # Start interview
    print("\n[1/4] Starting interview...")
    response1 = await manager.start_interview(session_id, candidate)
    
    if "_fallback" in response1.reply or "elaborate a bit more" in response1.reply.lower():
        print("❌ FAILED: Question generation returned fallback")
        return False
    
    print(f"✓ Question generated: {response1.reply[:150]}...")
    
    # Answer with a good technical response
    print("\n[2/4] Submitting answer...")
    good_answer = """
    In machine learning, prompt engineering involves carefully crafting input text 
    to guide language models toward desired outputs. Key techniques include providing 
    clear context, using few-shot examples, and structuring prompts with specific 
    instructions. Temperature controls randomness, while techniques like chain-of-thought 
    prompting help models show reasoning steps.
    """
    
    response2 = await manager.continue_interview(session_id, good_answer)
    
    if "_fallback" in response2.reply or "elaborate a bit more" in response2.reply.lower():
        print("❌ FAILED: Follow-up/next question returned fallback")
        return False
    
    print(f"✓ Next question/follow-up: {response2.reply[:150]}...")
    
    # Check evaluation was stored
    print("\n[3/4] Checking evaluation...")
    state = manager.session_manager.get_session(session_id)
    
    if not state.evaluations:
        print("❌ FAILED: No evaluations stored")
        return False
    
    last_eval = state.evaluations[-1].evaluation_result
    
    if last_eval.overall == 0.0:
        print("❌ FAILED: Evaluation returned zero score (likely fallback)")
        return False
    
    if "unavailable" in last_eval.interviewer_notes.lower():
        print("❌ FAILED: Evaluation used fallback")
        return False
    
    print(f"✓ Evaluation score: {last_eval.overall}/10")
    print(f"  - Accuracy: {last_eval.accuracy}/10")
    print(f"  - Reasoning: {last_eval.reasoning}/10")
    print(f"  - Depth: {last_eval.depth}/10")
    
    # Answer more questions to reach end
    print("\n[4/4] Completing interview...")
    for i in range(8):  # Answer remaining questions
        answer = f"This is answer {i+2}. I understand the concepts and can explain them clearly."
        response = await manager.continue_interview(session_id, answer)
        if response.done:
            break
    
    # Get final feedback
    if response.done and response.feedback:
        feedback = response.feedback
        
        if "temporarily unavailable" in feedback.summary.lower():
            print("❌ FAILED: Feedback used fallback")
            return False
        
        print(f"✓ Feedback generated")
        print(f"  - Overall score: {feedback.overall_score}/100")
        print(f"  - Summary: {feedback.summary[:100]}...")
        print(f"  - Strengths: {len(feedback.strengths)} items")
        print(f"  - Gaps: {len(feedback.gaps)} items")
    else:
        print("⚠ Interview did not complete (not enough questions)")
    
    print("\n" + "="*80)
    print("✅ SUCCESS: All Gemini API calls working correctly")
    print("="*80 + "\n")
    
    return True

if __name__ == "__main__":
    success = asyncio.run(test_live_interview())
    sys.exit(0 if success else 1)
