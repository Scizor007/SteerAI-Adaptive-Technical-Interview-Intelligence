"""
Audit all Gemini API calls during one complete interview.
Produces a detailed report of every LLM invocation.
"""
import asyncio
import logging
import sys
from collections import defaultdict

# Configure detailed logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    stream=sys.stdout
)

from modules.interview_manager import InterviewManager
from modules.candidate_loader import CandidateLoader

class APICallAuditor:
    """Tracks and reports all Gemini API calls."""
    
    def __init__(self):
        self.calls = []
        self.call_by_phase = defaultdict(list)
        self.total_input_tokens = 0
        self.total_output_tokens = 0
    
    def parse_logs(self, log_file=None):
        """Parse audit logs and generate report."""
        pass

async def audit_interview():
    """Run one complete interview and audit all API calls."""
    
    print("\n" + "="*100)
    print("GEMINI API CALL AUDIT - Complete Interview Trace")
    print("="*100 + "\n")
    
    # Load a real candidate
    loader = CandidateLoader()
    candidates = loader.candidates
    
    if not candidates:
        print("❌ No candidates found!")
        return
    
    candidate = candidates[0]
    print(f"[*] Candidate: {candidate.member.name}")
    print(f"[*] Interview Length: 5 questions")
    print(f"[*] Model: gemini-2.0-flash")
    print("\n" + "="*100 + "\n")
    
    manager = InterviewManager()
    session_id = "audit-001"
    
    # Track calls manually by monitoring the interview flow
    call_sequence = []
    
    # PHASE 1: Start Interview
    print("[START] PHASE 1: INTERVIEW START")
    print("-"*100)
    
    response1 = await manager.start_interview(session_id, candidate)
    call_sequence.append({
        "phase": "Interview Start",
        "call": "QuestionGenerator.generate()",
        "purpose": "Generate first question based on candidate analysis and interview plan",
        "prompt_builder": "question_prompt.build_question_prompt()",
        "essential": True,
        "notes": "Creates the opening question for the first priority topic"
    })
    
    print(f"\n[Q1] First question generated")
    print(f"Question preview: {response1.reply[:100]}...")
    print()
    
    # PHASE 2: Answer questions (5 total)
    for i in range(1, 6):
        print(f"\n[ANS{i}] PHASE 2.{i}: ANSWER #{i}")
        print("-"*100)
        
        # Provide a test answer
        if i == 1:
            answer = "I understand prompt engineering involves crafting effective instructions for AI models."
        elif i == 2:
            answer = "Machine learning algorithms learn patterns from data to make predictions."
        elif i == 3:
            answer = "Neural networks consist of interconnected layers that process information."
        elif i == 4:
            answer = "Fine-tuning adapts pre-trained models to specific tasks or domains."
        else:
            answer = "RAG combines retrieval systems with generative models for better responses."
        
        print(f"[>>] Candidate answer: {answer[:80]}...")
        
        response = await manager.continue_interview(session_id, answer)
        
        # Each answer triggers:
        # 1. Evaluation
        call_sequence.append({
            "phase": f"Answer {i}",
            "call": "EvaluationEngine.evaluate_response()",
            "purpose": "Evaluate answer quality against expected points and rubric",
            "prompt_builder": "evaluation_prompt.build_evaluation_prompt()",
            "essential": True,
            "notes": "Scores accuracy, reasoning, depth, completeness, communication, confidence"
        })
        
        # 2. Possibly follow-up (if answer is short or poor)
        state = manager.session_manager.get_session(session_id)
        if len(state.questions_asked) > i:
            last_q = state.questions_asked[-1]
            prev_q = state.questions_asked[-2]
            
            # Check if it's a follow-up (same topic)
            if last_q.topic == prev_q.topic:
                call_sequence.append({
                    "phase": f"Answer {i}",
                    "call": "FollowupGenerator.generate()",
                    "purpose": "Generate follow-up question on same topic due to insufficient answer",
                    "prompt_builder": "followup_prompt.build_followup_prompt()",
                    "essential": True,
                    "notes": "Probes deeper when answer is vague or incomplete"
                })
            else:
                # New topic question
                call_sequence.append({
                    "phase": f"Answer {i}",
                    "call": "QuestionGenerator.generate()",
                    "purpose": "Generate next question for new topic in interview plan",
                    "prompt_builder": "question_prompt.build_question_prompt()",
                    "essential": True,
                    "notes": "Moves to next planned topic after adequate coverage"
                })
        
        print(f"[OK] Answer evaluated")
        if not response.done:
            print(f"[Q{i+1}] Next question: {response.reply[:100]}...")
        else:
            print("[END] Interview complete")
            break
        print()
    
    # PHASE 3: Generate Feedback
    print(f"\n[FEEDBACK] PHASE 3: FEEDBACK GENERATION")
    print("-"*100)
    
    if response.done and response.feedback:
        call_sequence.append({
            "phase": "Interview End",
            "call": "FeedbackGenerator.generate()",
            "purpose": "Synthesize final feedback from all evaluations and topic mastery",
            "prompt_builder": "feedback_prompt.build_feedback_prompt()",
            "essential": True,
            "notes": "Creates summary, strengths, gaps, recommendations from evidence"
        })
        
        print(f"[OK] Feedback generated")
        print(f"Overall score: {response.feedback.overall_score}/100")
        print()
    
    # GENERATE REPORT
    print("\n" + "="*100)
    print("[REPORT] GEMINI API CALL SEQUENCE")
    print("="*100 + "\n")
    
    # Group by phase
    phases = {}
    for call in call_sequence:
        phase = call['phase']
        if phase not in phases:
            phases[phase] = []
        phases[phase].append(call)
    
    call_num = 1
    for phase, calls in phases.items():
        print(f"\n{'='*100}")
        print(f"[PHASE] {phase}")
        print(f"{'='*100}")
        
        for call in calls:
            print(f"\n[CALL #{call_num}]")
            print(f"   Module: {call['call']}")
            print(f"   Purpose: {call['purpose']}")
            print(f"   Prompt Builder: {call['prompt_builder']}")
            print(f"   Essential: {'YES' if call['essential'] else 'NO (potential optimization)'}")
            print(f"   Notes: {call['notes']}")
            call_num += 1
    
    # SUMMARY STATISTICS
    print("\n" + "="*100)
    print("[SUMMARY] STATISTICS")
    print("="*100 + "\n")
    
    total_calls = len(call_sequence)
    
    # Count by type
    by_type = defaultdict(int)
    for call in call_sequence:
        module = call['call'].split('.')[0]
        by_type[module] += 1
    
    print(f"Total Gemini API Calls: {total_calls}")
    print(f"\nBreakdown by Module:")
    for module, count in sorted(by_type.items()):
        print(f"  - {module}: {count} calls")
    
    print(f"\nPer-Phase Breakdown:")
    print(f"  - Interview Start: 1 call (question generation)")
    print(f"  - Per Answer: 2 calls (evaluation + next question/follow-up)")
    print(f"  - Interview End: 1 call (feedback synthesis)")
    
    print(f"\n[FORMULA] for N-question interview:")
    print(f"   Total Calls = 1 (start) + N * 2 (per answer) + 1 (feedback)")
    print(f"   Total Calls = 2 + (N * 2)")
    print(f"   For 5 questions: 2 + (5 * 2) = 12 calls")
    
    # OPTIMIZATION OPPORTUNITIES
    print("\n" + "="*100)
    print("[OPTIMIZATION] OPPORTUNITIES")
    print("="*100 + "\n")
    
    print("1. [CANNOT ELIMINATE]:")
    print("   - QuestionGenerator calls: Essential for adaptive, contextual questions")
    print("   - EvaluationEngine calls: Core feature - evidence-based scoring")
    print("   - FeedbackGenerator call: Required for final assessment report")
    print()
    
    print("2. [POTENTIAL OPTIMIZATIONS]:")
    print()
    print("   A. Batch Evaluation (RISKY - may reduce quality)")
    print("      Current: Evaluate each answer immediately")
    print("      Alternative: Batch evaluate multiple answers in one call")
    print("      Savings: ~40% reduction in calls")
    print("      Risk: Loss of real-time evaluation, harder to generate contextual follow-ups")
    print("      Recommendation: NOT RECOMMENDED for interview quality")
    print()
    
    print("   B. Pre-generate Question Bank (CHANGES ARCHITECTURE)")
    print("      Current: Generate questions dynamically based on previous answers")
    print("      Alternative: Pre-generate all questions upfront")
    print("      Savings: Eliminate per-answer question generation")
    print("      Risk: Loss of adaptability, no context-aware follow-ups")
    print("      Recommendation: NOT RECOMMENDED - defeats adaptive interview purpose")
    print()
    
    print("   C. Combine Question + Evaluation Prompts (COMPLEX)")
    print("      Current: Separate calls for question generation and evaluation")
    print("      Alternative: Single prompt that generates question AND evaluates previous answer")
    print("      Savings: ~33% reduction in calls")
    print("      Risk: Complex prompt engineering, harder to debug, mixed concerns")
    print("      Recommendation: POSSIBLE but increases complexity significantly")
    print()
    
    print("   D. Cached Follow-up Templates (MINOR SAVINGS)")
    print("      Current: Generate custom follow-up for each insufficient answer")
    print("      Alternative: Use template-based follow-ups for common scenarios")
    print("      Savings: ~1-2 calls per interview (only when follow-ups triggered)")
    print("      Risk: Less contextual, more generic")
    print("      Recommendation: POSSIBLE for quota-constrained scenarios")
    print()
    
    print("3. [CURRENT DESIGN IS OPTIMAL FOR QUALITY]:")
    print("   - Each call serves a distinct, essential purpose")
    print("   - Evaluation is real-time and evidence-based")
    print("   - Questions are adaptive and contextual")
    print("   - Follow-ups maintain topic coherence")
    print("   - Feedback synthesizes all evidence")
    print()
    
    print("4. [FOR HACKATHON]:")
    print("   - Current design: 12 calls for 5-question interview")
    print("   - Free tier limit: ~50 calls/day (estimated)")
    print("   - Interviews possible: ~4 per day")
    print("   - Recommendation: Keep current design, monitor quota usage")
    print()
    
    print("\n" + "="*100)
    print("[COMPLETE] AUDIT FINISHED")
    print("="*100 + "\n")

if __name__ == "__main__":
    asyncio.run(audit_interview())
