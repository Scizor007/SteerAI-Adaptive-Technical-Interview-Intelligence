"""
Complete end-to-end interview test with OpenRouter.
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

async def complete_interview():
    """Run a complete interview to test feedback generation."""
    print("\n" + "="*80)
    print("COMPLETE INTERVIEW TEST WITH OPENROUTER")
    print("="*80 + "\n")
    
    # Load candidate
    loader = CandidateLoader()
    candidate = loader.candidates[0]
    print(f"Candidate: {candidate.member.name}\n")
    
    manager = InterviewManager()
    session_id = "openrouter-complete-001"
    
    # Start interview
    print("[1/6] Starting interview...")
    response = await manager.start_interview(session_id, candidate)
    print(f"Q1: {response.reply[:150]}...")
    
    # Submit answers until interview completes (max 15)
    for i in range(2, 17):
        if response.done:
            break
        
        answer = f"Answer {i-1}: I have extensive professional experience in this area. I've implemented production systems using industry best practices including proper error handling, logging, testing, and monitoring. I use CI/CD pipelines, containerization, and cloud-native architectures."
        
        print(f"\n[{i}/16] Submitting answer {i-1}...")
        response = await manager.continue_interview(session_id, answer)
        
        if not response.done:
            print(f"Q{i}: {response.reply[:100]}...")
    
    # Check if interview completed
    if response.done and response.feedback:
        print("\n" + "="*80)
        print("INTERVIEW COMPLETED - CHECKING FEEDBACK")
        print("="*80 + "\n")
        
        print(f"Summary:\n{response.feedback.summary}\n")
        print(f"Strengths: {response.feedback.strengths}\n")
        print(f"Gaps: {response.feedback.gaps}\n")
        print(f"Next Steps: {response.feedback.next}\n")
        
        # Check for fallback message
        if "temporarily unavailable" in response.feedback.summary.lower():
            print("="*80)
            print("❌ FAILED: Feedback contains fallback message")
            print("="*80)
            return False
        else:
            print("="*80)
            print("✅ SUCCESS: Real feedback generated from OpenRouter!")
            print("No fallback messages detected.")
            print("="*80)
            return True
    else:
        print("\n❌ Interview did not complete")
        return False

if __name__ == "__main__":
    success = asyncio.run(complete_interview())
    sys.exit(0 if success else 1)
