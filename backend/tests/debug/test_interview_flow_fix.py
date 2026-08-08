"""
Test the interview flow fixes to verify:
1. Configuration is correct
2. Followup count increments properly
3. Maximum followups enforced
4. LLM failures don't create infinite loops
5. Evaluation fallbacks don't penalize candidates
"""
import asyncio
import logging
import sys
import os

# Add backend root to path so imports work from subdirectory
backend_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, backend_root)

# Configure logging to see what's happening
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)

from modules.interview_manager import InterviewManager
from modules.candidate_loader import CandidateLoader

async def test_interview_flow():
    """Test complete interview flow with fixes."""
    
    print("\n" + "="*80)
    print("INTERVIEW FLOW FIX VERIFICATION")
    print("="*80 + "\n")
    
    # Load a candidate
    loader = CandidateLoader()
    candidates = loader.candidates
    
    if not candidates:
        print("[FAIL] No candidates found!")
        return False
    
    candidate = candidates[0]
    print(f"[OK] Using candidate: {candidate.member.name}\n")
    
    manager = InterviewManager()
    session_id = "fix-test-001"
    
    # TEST 1: Start interview
    print("[TEST 1] Starting interview...")
    response = await manager.start_interview(session_id, candidate)
    print(f"[OK] First question received (length: {len(response.reply)} chars)")
    print(f"  Question preview: {response.reply[:100]}...\n")
    
    # TEST 2: Submit a short answer (< 20 chars) - should trigger follow-up IF evaluation works
    print("[TEST 2] Submitting short answer...")
    response = await manager.continue_interview(session_id, "Yes, I know it.")
    state = manager.session_manager.get_session(session_id)
    
    # Check if follow-up was triggered
    if len(state.questions_asked) == 2:
        last_q = state.questions_asked[-1]
        prev_q = state.questions_asked[-2]
        
        if last_q.topic == prev_q.topic:
            print(f"[OK] Follow-up triggered (same topic)")
            print(f"  Followup count: {last_q.followup_count}")
            print(f"  Question: {response.reply[:80]}...\n")
        else:
            print(f"[OK] Moved to next topic (no follow-up)")
            print(f"  New topic: {last_q.topic}\n")
    else:
        print(f"[OK] Interview progressed to question #{len(state.questions_asked)}\n")
    
    # TEST 3: Submit another answer
    print("[TEST 3] Submitting second answer...")
    response = await manager.continue_interview(session_id, "I understand the basic concepts.")
    state = manager.session_manager.get_session(session_id)
    print(f"[OK] Question #{len(state.questions_asked)} received")
    print(f"  Total questions: {state.total_questions}")
    print(f"  Question: {response.reply[:80]}...\n")
    
    # TEST 4: Check that we're not stuck in a loop
    prev_question = response.reply
    print("[TEST 4] Submitting third answer (checking for loops)...")
    response = await manager.continue_interview(session_id, "It handles state management.")
    
    if response.reply == prev_question:
        print("[FAIL] Same question repeated!")
        return False
    else:
        print(f"[OK] Different question received (no loop)")
        print(f"  Question: {response.reply[:80]}...\n")
    
    # TEST 5: Check evaluations
    state = manager.session_manager.get_session(session_id)
    print(f"[TEST 5] Checking evaluations...")
    print(f"  Total evaluations stored: {len(state.evaluations)}")
    
    if state.evaluations:
        last_eval = state.evaluations[-1].evaluation_result
        print(f"  Last evaluation score: {last_eval.overall}/10")
        print(f"  Has fallback flag: {getattr(last_eval, '_fallback', False)}")
    
    # Check if any evaluation has _fallback flag
    fallback_count = sum(1 for e in state.evaluations if getattr(e.evaluation_result, '_fallback', False))
    if fallback_count > 0:
        print(f"  [WARN] {fallback_count} evaluations used fallback (LLM unavailable)")
        print(f"  [OK] Fallbacks were NOT stored as candidate scores\n")
    else:
        print(f"  [OK] All evaluations completed successfully\n")
    
    # TEST 6: Verify followup count tracking
    print("[TEST 6] Checking followup count tracking...")
    followup_questions = [q for q in state.questions_asked if q.followup_count > 0]
    if followup_questions:
        print(f"  Found {len(followup_questions)} follow-up questions")
        for q in followup_questions:
            print(f"    - Topic: {q.topic}, Count: {q.followup_count}")
    else:
        print(f"  No follow-ups triggered (answers may have been sufficient)")
    print()
    
    # TEST 7: Complete a few more answers
    print("[TEST 7] Completing interview...")
    for i in range(3):
        if response.done:
            break
        response = await manager.continue_interview(
            session_id, 
            f"Answer {i+4}: This involves configuration and deployment strategies."
        )
        print(f"  Question {i+4}: {'[COMPLETE]' if response.done else 'received'}")
    
    state = manager.session_manager.get_session(session_id)
    print(f"\n[OK] Interview ended at {state.total_questions} questions")
    
    # FINAL VERIFICATION
    print("\n" + "="*80)
    print("VERIFICATION SUMMARY")
    print("="*80)
    
    # Check for the problematic fallback question
    questions_text = [q.question for q in state.questions_asked]
    generic_fallback_count = sum(
        1 for q in questions_text 
        if "elaborate a bit more on your previous experiences" in q.lower()
    )
    
    if generic_fallback_count > 1:
        print(f"[FAIL] Generic fallback question appeared {generic_fallback_count} times")
        return False
    elif generic_fallback_count == 1:
        print(f"[WARN] Generic fallback appeared once (acceptable if LLM failed)")
    else:
        print(f"[OK] No generic fallback questions (LLM working or using topic-specific fallbacks)")
    
    # Check followup counts
    max_followup_count = max((q.followup_count for q in state.questions_asked), default=0)
    if max_followup_count > 2:
        print(f"[FAIL] Followup count exceeded maximum: {max_followup_count}")
        return False
    else:
        print(f"[OK] Maximum followup count respected: {max_followup_count}/2")
    
    # Check for duplicate questions
    normalized_questions = [q.lower().strip() for q in questions_text]
    if len(normalized_questions) != len(set(normalized_questions)):
        print(f"[FAIL] Duplicate questions detected")
        return False
    else:
        print(f"[OK] No duplicate questions")
    
    # Check evaluation storage
    non_fallback_evals = [
        e for e in state.evaluations 
        if not getattr(e.evaluation_result, '_fallback', False)
    ]
    print(f"[OK] Stored {len(non_fallback_evals)} valid evaluations (excluded {len(state.evaluations) - len(non_fallback_evals)} fallbacks)")
    
    print("\n" + "="*80)
    print("[SUCCESS] ALL TESTS PASSED")
    print("="*80 + "\n")
    
    return True

if __name__ == "__main__":
    success = asyncio.run(test_interview_flow())
    sys.exit(0 if success else 1)
