"""
Complete evaluation trace test.
Tests the entire pipeline with real answers to identify where the evaluation fails.
"""
import asyncio
import logging
import sys

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)

from modules.interview_manager import InterviewManager
from modules.candidate_loader import CandidateLoader

async def test_evaluation_pipeline():
    """Run a complete interview with test answers to trace evaluation."""
    
    print("\n" + "="*80)
    print("EVALUATION PIPELINE TRACE TEST")
    print("="*80 + "\n")
    
    # Load a real candidate from the data file
    loader = CandidateLoader()
    candidates = loader.candidates
    
    if not candidates:
        print("❌ No candidates found in data file!")
        return
    
    # Use the first candidate
    candidate = candidates[0]
    print(f"Using candidate: {candidate.member.name}")
    
    manager = InterviewManager()
    session_id = "trace-test-001"
    
    # Test Case 1: Meaningless answer "sss"
    print("\n" + "-"*80)
    print("TEST CASE 1: Meaningless Answer 'sss'")
    print("-"*80 + "\n")
    
    response1 = await manager.start_interview(session_id, candidate)
    print(f"First question: {response1.reply[:200]}...")
    
    response2 = await manager.continue_interview(session_id, "sss")
    print(f"\nResponse after 'sss': {response2.reply[:200]}...")
    
    # Get session state to check evaluations
    state = manager.session_manager.get_session(session_id)
    if state.evaluations:
        last_eval = state.evaluations[-1].evaluation_result
        print(f"\nEvaluation Result for 'sss':")
        print(f"  Overall: {last_eval.overall}")
        print(f"  Accuracy: {last_eval.accuracy}")
        print(f"  Reasoning: {last_eval.reasoning}")
        print(f"  Depth: {last_eval.depth}")
        print(f"  Completeness: {last_eval.completeness}")
        print(f"  Communication: {last_eval.communication}")
        print(f"  Confidence: {last_eval.confidence}")
        print(f"  Missing points: {last_eval.missing_points}")
        print(f"  Misconceptions: {last_eval.misconceptions}")
        print(f"  Interviewer notes: {last_eval.interviewer_notes}")
    else:
        print("\n❌ ERROR: No evaluations stored!")
    
    # Test Case 2: "I don't know"
    print("\n" + "-"*80)
    print("TEST CASE 2: 'I don't know'")
    print("-"*80 + "\n")
    
    response3 = await manager.continue_interview(session_id, "I don't know")
    print(f"\nResponse after 'I don't know': {response3.reply[:200]}...")
    
    if len(state.evaluations) >= 2:
        last_eval = state.evaluations[-1].evaluation_result
        print(f"\nEvaluation Result for 'I don't know':")
        print(f"  Overall: {last_eval.overall}")
        print(f"  Accuracy: {last_eval.accuracy}")
        print(f"  Reasoning: {last_eval.reasoning}")
    
    # Test Case 3: Good technical answer
    print("\n" + "-"*80)
    print("TEST CASE 3: Good Technical Answer")
    print("-"*80 + "\n")
    
    good_answer = """
    Prompt engineering is the practice of designing and optimizing text prompts to get better 
    responses from large language models. Key techniques include few-shot learning where you 
    provide examples, chain-of-thought prompting to encourage step-by-step reasoning, and 
    role-based prompting where you set context. It's important to be specific, provide clear 
    instructions, and iterate on prompts based on the model's outputs.
    """
    
    response4 = await manager.continue_interview(session_id, good_answer)
    print(f"\nResponse after good answer: {response4.reply[:200]}...")
    
    if len(state.evaluations) >= 3:
        last_eval = state.evaluations[-1].evaluation_result
        print(f"\nEvaluation Result for good answer:")
        print(f"  Overall: {last_eval.overall}")
        print(f"  Accuracy: {last_eval.accuracy}")
        print(f"  Reasoning: {last_eval.reasoning}")
        print(f"  Strengths: {last_eval.strengths}")
    
    # Final summary
    print("\n" + "="*80)
    print("TRACE SUMMARY")
    print("="*80 + "\n")
    print(f"Total questions asked: {state.total_questions}")
    print(f"Total evaluations: {len(state.evaluations)}")
    print(f"Topic mastery: {state.topic_mastery}")
    
    # Score summary
    if state.evaluations:
        from modules.evaluation_engine import EvaluationEngine
        engine = EvaluationEngine()
        score_summary = engine.calculate_score_summary(state.evaluations)
        print(f"\nScore Summary:")
        print(f"  Overall Score: {score_summary.overall_score}")
        print(f"  Accuracy: {score_summary.accuracy}")
        print(f"  Reasoning: {score_summary.reasoning}")
        print(f"  Coverage Bonus: {score_summary.coverage_bonus}")
        print(f"  Consistency Bonus: {score_summary.consistency_bonus}")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    asyncio.run(test_evaluation_pipeline())
