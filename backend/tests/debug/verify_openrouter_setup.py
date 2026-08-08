"""
Verify OpenRouter setup and perform end-to-end test.
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

import config
from services.llm_service import LLMService
from modules.interview_manager import InterviewManager
from modules.candidate_loader import CandidateLoader

def check_configuration():
    """Check if OpenRouter is properly configured."""
    print("="*80)
    print("OPENROUTER CONFIGURATION CHECK")
    print("="*80)
    
    print(f"LLM_PROVIDER: {config.LLM_PROVIDER}")
    print(f"OPENROUTER_MODEL: {config.OPENROUTER_MODEL}")
    
    if config.OPENROUTER_API_KEY:
        if config.OPENROUTER_API_KEY.startswith("<"):
            print(f"OPENROUTER_API_KEY: PLACEHOLDER (not configured)")
            print("\n❌ CRITICAL: You need to add a real OpenRouter API key!")
            print("Please visit: https://openrouter.ai/keys")
            print("Get your API key and update backend/.env")
            return False
        else:
            key_preview = config.OPENROUTER_API_KEY[:8] + "..." + config.OPENROUTER_API_KEY[-4:]
            print(f"OPENROUTER_API_KEY: {key_preview} (configured)")
    else:
        print(f"OPENROUTER_API_KEY: NOT SET")
        print("\n❌ CRITICAL: You need to add a real OpenRouter API key!")
        return False
    
    print("="*80)
    return True

async def test_openrouter_end_to_end():
    """Run a complete interview to verify OpenRouter integration."""
    print("\n" + "="*80)
    print("END-TO-END OPENROUTER TEST")
    print("="*80 + "\n")
    
    # Check LLMService initialization
    print("[1/5] Initializing LLMService...")
    llm = LLMService()
    
    if llm.provider is None:
        print("❌ FAILED: Provider is None")
        print("Check the logs above for API key validation errors")
        return False
    
    print(f"✅ Provider initialized: {llm.provider.display_name}")
    
    # Test question generation
    print("\n[2/5] Testing question generation via OpenRouter...")
    test_prompt = """Generate a technical interview question about Python.
Return ONLY valid JSON with this structure:
{
  "question": "Your question here",
  "expected_points": ["point1", "point2"],
  "estimated_difficulty": "Medium"
}"""
    
    try:
        result = llm.generate_json(test_prompt, fallback_type="question", caller_module="Test")
        if result.get("_fallback"):
            print("❌ FAILED: Received fallback instead of OpenRouter response")
            return False
        print(f"✅ Question generated: {result.get('question', '')[:100]}...")
    except Exception as e:
        print(f"❌ FAILED: {str(e)[:200]}")
        return False
    
    # Load candidate for full interview
    print("\n[3/5] Loading candidate...")
    loader = CandidateLoader()
    if not loader.candidates:
        print("❌ FAILED: No candidates found")
        return False
    candidate = loader.candidates[0]
    print(f"✅ Using candidate: {candidate.member.name}")
    
    # Start interview
    print("\n[4/5] Starting interview...")
    manager = InterviewManager()
    session_id = "openrouter-verify-001"
    
    try:
        response = await manager.start_interview(session_id, candidate)
        if not response.reply:
            print("❌ FAILED: No question in response")
            return False
        
        # Check if fallback message
        if "elaborate" in response.reply.lower() and "previous experiences" in response.reply.lower():
            print("❌ FAILED: Received fallback question instead of OpenRouter question")
            return False
        
        print(f"✅ First question received: {response.reply[:100]}...")
    except Exception as e:
        print(f"❌ FAILED: {str(e)[:200]}")
        return False
    
    # Submit an answer and get evaluation
    print("\n[5/5] Submitting answer and checking evaluation...")
    try:
        answer = "I have extensive experience with Python. I use list comprehensions, decorators, context managers, and async/await for concurrent programming. I follow PEP 8 standards."
        response = await manager.continue_interview(session_id, answer)
        
        if response.done:
            # Check feedback for fallback
            if response.feedback and "temporarily unavailable" in response.feedback.summary.lower():
                print("❌ FAILED: Feedback contains fallback message")
                return False
            print("✅ Interview completed with real feedback")
        else:
            print(f"✅ Next question received: {response.reply[:100]}...")
        
    except Exception as e:
        print(f"❌ FAILED: {str(e)[:200]}")
        return False
    
    print("\n" + "="*80)
    print("✅ ALL TESTS PASSED - OpenRouter is working correctly!")
    print("="*80)
    return True

if __name__ == "__main__":
    if not check_configuration():
        print("\nPlease configure OpenRouter API key and try again.")
        sys.exit(1)
    
    success = asyncio.run(test_openrouter_end_to_end())
    sys.exit(0 if success else 1)
