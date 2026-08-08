"""
Test JSON recovery performance with at least 20 evaluations.
"""
import asyncio
import sys
import os

# Add backend root to path
backend_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, backend_root)

# Fix Windows console encoding
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from modules.interview_manager import InterviewManager
from modules.candidate_loader import CandidateLoader
import logging

# Track statistics via log messages
class RecoveryStatsHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.total_evaluations = 0
        self.parsed_normally = 0
        self.parsed_after_repair = 0
        self.true_fallbacks = 0
        self.current_eval_had_recovery = False
        
    def emit(self, record):
        msg = record.getMessage()
        
        # Track evaluation calls
        if '[AUDIT] LLM API CALL' in msg and 'EvaluationEngine' in msg:
            if self.current_eval_had_recovery:
                self.parsed_after_repair += 1
            elif self.total_evaluations > 0:  # Previous call completed
                self.parsed_normally += 1
            
            self.total_evaluations += 1
            self.current_eval_had_recovery = False
        
        # Track recovery
        if '[JSON RECOVERY] Successfully repaired' in msg:
            self.current_eval_had_recovery = True
        
        # Track fallbacks
        if '[FALLBACK] EVALUATION FALLBACK DETECTED' in msg:
            if not self.current_eval_had_recovery:
                self.true_fallbacks += 1

# Set up tracking
stats_handler = RecoveryStatsHandler()
stats_handler.setLevel(logging.DEBUG)
logging.getLogger().addHandler(stats_handler)
logging.getLogger().setLevel(logging.WARNING)

async def test_recovery_performance():
    """Run interview with at least 20 evaluations."""
    print("\n" + "="*80)
    print("JSON RECOVERY PERFORMANCE TEST")
    print("="*80 + "\n")
    
    # Load candidate
    loader = CandidateLoader()
    candidate = loader.candidates[0]
    print(f"Candidate: {candidate.member.name}")
    print("Running extended interview to collect 20+ evaluations...\n")
    
    manager = InterviewManager()
    session_id = "recovery-perf-001"
    
    # Start interview
    response = await manager.start_interview(session_id, candidate)
    
    # Submit answers until we have 20+ evaluations
    answer_count = 0
    while not response.done and answer_count < 25:
        answer_count += 1
        
        # Vary answer quality
        if answer_count % 4 == 0:
            answer = "I don't have experience with that."
        elif answer_count % 4 == 1:
            answer = "I have extensive professional experience implementing production systems with best practices including error handling, logging, testing, monitoring, CI/CD pipelines, containerization, orchestration, and cloud-native architectures."
        elif answer_count % 4 == 2:
            answer = "I understand the basic concepts and have worked with similar technologies in academic and personal projects."
        else:
            answer = "I've used this in several projects and understand the key principles."
        
        response = await manager.continue_interview(session_id, answer)
        
        if answer_count % 5 == 0:
            print(f"Progress: {answer_count} answers, {stats_handler.total_evaluations} evaluations...")
    
    # Handle last evaluation
    if stats_handler.current_eval_had_recovery:
        stats_handler.parsed_after_repair += 1
    elif stats_handler.total_evaluations > stats_handler.parsed_normally + stats_handler.parsed_after_repair + stats_handler.true_fallbacks:
        stats_handler.parsed_normally += 1
    
    # Print results
    print("\n" + "="*80)
    print("RESULTS")
    print("="*80 + "\n")
    
    total = stats_handler.total_evaluations
    normal = stats_handler.parsed_normally
    repaired = stats_handler.parsed_after_repair
    fallback = stats_handler.true_fallbacks
    
    print(f"1. Total Evaluations: {total}")
    print(f"2. Parsed Normally: {normal} ({normal/total*100:.1f}%)")
    print(f"3. Parsed After Repair: {repaired} ({repaired/total*100:.1f}%)")
    print(f"4. True Fallbacks: {fallback} ({fallback/total*100:.1f}%)")
    
    success_rate = ((normal + repaired) / total * 100) if total > 0 else 0
    print(f"\n5. Final Success Rate: {success_rate:.1f}%")
    
    print("\n" + "="*80)
    
    if success_rate >= 95:
        print("✅ SUCCESS: Recovery layer achieves >= 95% success rate")
        print("✅ Current model (meta-llama/llama-3.2-3b-instruct) is acceptable with recovery")
        print("✅ No model change needed")
    else:
        print(f"⚠ BELOW TARGET: {success_rate:.1f}% success rate (target: 95%)")
        print(f"\nRECOMMENDATION: Switch to more reliable model")
        print(f"\nSuggested models (in order of preference):")
        print(f"  1. google/gemini-flash-1.5 (best JSON reliability, cost-effective)")
        print(f"  2. anthropic/claude-3-haiku (excellent structured output)")
        print(f"  3. openai/gpt-3.5-turbo (good JSON compliance)")
        print(f"  4. meta-llama/llama-3.1-8b-instruct (larger Llama)")
        print(f"\nWhy: Even with recovery layer, {fallback} evaluations ({fallback/total*100:.1f}%) could not be repaired.")
        print(f"Recovery layer successfully repairs truncated/malformed JSON, but some responses")
        print(f"are too severely damaged. A more reliable model will reduce recovery overhead.")
    
    print("="*80)

if __name__ == "__main__":
    asyncio.run(test_recovery_performance())
