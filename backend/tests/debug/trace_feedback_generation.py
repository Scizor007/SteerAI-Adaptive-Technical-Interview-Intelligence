"""
Trace feedback generation to identify where fallback is triggered.

This script will:
1. Verify FeedbackGenerator is called
2. Verify LLMService.generate_json is called
3. Print the exact provider being used
4. Print the raw LLM response before parsing
5. Print the parsed JSON object
6. Print any exceptions with full stack trace
7. Identify the exact line causing fallback
"""
import asyncio
import logging
import sys
import traceback
import json

# Add backend root to path
import os
backend_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, backend_root)

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)

# Patch LLMService to trace execution
original_generate_json = None
original_generate_text = None
original_parse_json = None

def patch_llm_service():
    """Patch LLMService to add detailed tracing."""
    from services.llm_service import LLMService
    from services.parsers.llm_parser import LLMParser
    
    global original_generate_json, original_parse_json
    original_generate_json = LLMService.generate_json
    original_parse_json = LLMParser.parse_json
    
    def traced_generate_json(self, prompt: str, fallback_type: str = "question", caller_module: str = "unknown"):
        print("\n" + "="*80)
        print("[TRACE] LLMService.generate_json() CALLED")
        print(f"[TRACE] Caller: {caller_module}")
        print(f"[TRACE] Fallback Type: {fallback_type}")
        print(f"[TRACE] Provider: {self.provider}")
        print(f"[TRACE] Provider Type: {type(self.provider).__name__ if self.provider else 'None'}")
        print("="*80 + "\n")
        
        try:
            result = original_generate_json(self, prompt, fallback_type, caller_module)
            
            print("\n" + "="*80)
            print("[TRACE] LLMService.generate_json() RETURNED")
            print(f"[TRACE] Result keys: {list(result.keys())}")
            print(f"[TRACE] Has _fallback flag: {result.get('_fallback', False)}")
            if result.get('_fallback'):
                print("[TRACE] !!! FALLBACK WAS RETURNED !!!")
            print(f"[TRACE] Result preview: {json.dumps(result, indent=2)[:500]}...")
            print("="*80 + "\n")
            
            return result
        except Exception as e:
            print("\n" + "="*80)
            print("[TRACE] !!! EXCEPTION IN generate_json !!!")
            print(f"[TRACE] Exception type: {type(e).__name__}")
            print(f"[TRACE] Exception message: {str(e)}")
            print("[TRACE] Stack trace:")
            traceback.print_exc()
            print("="*80 + "\n")
            raise
    
    def traced_parse_json(response_text: str):
        print("\n" + "="*80)
        print("[TRACE] LLMParser.parse_json() CALLED")
        print(f"[TRACE] Response length: {len(response_text)} chars")
        print(f"[TRACE] Response preview (first 500 chars):")
        print(response_text[:500])
        print("="*80 + "\n")
        
        try:
            result = original_parse_json(response_text)
            
            print("\n" + "="*80)
            print("[TRACE] LLMParser.parse_json() SUCCESS")
            print(f"[TRACE] Parsed keys: {list(result.keys())}")
            print(f"[TRACE] Parsed result: {json.dumps(result, indent=2)[:500]}...")
            print("="*80 + "\n")
            
            return result
        except Exception as e:
            print("\n" + "="*80)
            print("[TRACE] !!! EXCEPTION IN parse_json !!!")
            print(f"[TRACE] Exception type: {type(e).__name__}")
            print(f"[TRACE] Exception message: {str(e)}")
            print("[TRACE] Stack trace:")
            traceback.print_exc()
            print("="*80 + "\n")
            raise
    
    LLMService.generate_json = traced_generate_json
    LLMParser.parse_json = traced_parse_json

def patch_provider():
    """Patch provider to trace raw responses."""
    try:
        from services.llm.gemini_provider import GeminiProvider
        
        global original_generate_text
        original_generate_text = GeminiProvider.generate_text
        
        def traced_generate_text(self, prompt: str) -> str:
            print("\n" + "="*80)
            print("[TRACE] GeminiProvider.generate_text() CALLED")
            print(f"[TRACE] Prompt length: {len(prompt)} chars")
            print("="*80 + "\n")
            
            try:
                response = original_generate_text(self, prompt)
                
                print("\n" + "="*80)
                print("[TRACE] GeminiProvider.generate_text() SUCCESS")
                print(f"[TRACE] Raw response length: {len(response)} chars")
                print("[TRACE] Raw response (first 1000 chars):")
                print(response[:1000])
                print("="*80 + "\n")
                
                return response
            except Exception as e:
                print("\n" + "="*80)
                print("[TRACE] !!! EXCEPTION IN GeminiProvider.generate_text !!!")
                print(f"[TRACE] Exception type: {type(e).__name__}")
                print(f"[TRACE] Exception message: {str(e)}")
                print("[TRACE] Stack trace:")
                traceback.print_exc()
                print("="*80 + "\n")
                raise
        
        GeminiProvider.generate_text = traced_generate_text
        print("[PATCH] GeminiProvider patched successfully\n")
    except ImportError:
        print("[PATCH] GeminiProvider not available\n")
    
    try:
        from services.llm.openrouter_provider import OpenRouterProvider
        
        original_generate_text_or = OpenRouterProvider.generate_text
        
        def traced_generate_text_or(self, prompt: str) -> str:
            print("\n" + "="*80)
            print("[TRACE] OpenRouterProvider.generate_text() CALLED")
            print(f"[TRACE] Prompt length: {len(prompt)} chars")
            print("="*80 + "\n")
            
            try:
                response = original_generate_text_or(self, prompt)
                
                print("\n" + "="*80)
                print("[TRACE] OpenRouterProvider.generate_text() SUCCESS")
                print(f"[TRACE] Raw response length: {len(response)} chars")
                print("[TRACE] Raw response (first 1000 chars):")
                print(response[:1000])
                print("="*80 + "\n")
                
                return response
            except Exception as e:
                print("\n" + "="*80)
                print("[TRACE] !!! EXCEPTION IN OpenRouterProvider.generate_text !!!")
                print(f"[TRACE] Exception type: {type(e).__name__}")
                print(f"[TRACE] Exception message: {str(e)}")
                print("[TRACE] Stack trace:")
                traceback.print_exc()
                print("="*80 + "\n")
                raise
        
        OpenRouterProvider.generate_text = traced_generate_text_or
        print("[PATCH] OpenRouterProvider patched successfully\n")
    except ImportError:
        print("[PATCH] OpenRouterProvider not available\n")

async def run_interview_and_trace():
    """Run a complete interview and trace feedback generation."""
    print("\n" + "="*100)
    print("FEEDBACK GENERATION TRACE")
    print("="*100 + "\n")
    
    # Apply patches BEFORE importing modules
    patch_llm_service()
    patch_provider()
    
    from modules.interview_manager import InterviewManager
    from modules.candidate_loader import CandidateLoader
    
    # Load candidate
    loader = CandidateLoader()
    candidates = loader.candidates
    if not candidates:
        print("[ERROR] No candidates found!")
        return
    
    candidate = candidates[0]
    print(f"[TEST] Using candidate: {candidate.member.name}\n")
    
    manager = InterviewManager()
    session_id = "feedback-trace-001"
    
    # Start interview
    print("[TEST] Starting interview...\n")
    response = await manager.start_interview(session_id, candidate)
    
    # Submit answers quickly to reach end
    print("[TEST] Submitting answers to complete interview...\n")
    for i in range(5):
        if response.done:
            break
        answer = f"This is answer {i+1}. I understand the concepts and have applied them in production environments."
        response = await manager.continue_interview(session_id, answer)
        print(f"[TEST] Answer {i+1} submitted, done={response.done}\n")
    
    # Check if interview completed
    if response.done:
        print("\n" + "="*100)
        print("[TEST] INTERVIEW COMPLETED - FEEDBACK GENERATED")
        print("="*100 + "\n")
        
        if response.feedback:
            print("[TEST] Feedback object received:")
            print(f"[TEST] Summary: {response.feedback.summary[:200]}...")
            print(f"[TEST] Strengths: {response.feedback.strengths}")
            print(f"[TEST] Gaps: {response.feedback.gaps}")
            print(f"[TEST] Next: {response.feedback.next}")
            
            # Check for fallback indicators
            if "temporarily unavailable" in response.feedback.summary.lower():
                print("\n[RESULT] !!! FALLBACK MESSAGE DETECTED IN FEEDBACK !!!")
                print("[RESULT] The feedback is using the fallback text from LLMService._get_fallback()")
            else:
                print("\n[RESULT] Feedback appears to be generated by LLM (not fallback)")
        else:
            print("[TEST] No feedback object in response!")
    else:
        print("[TEST] Interview did not complete!")

if __name__ == "__main__":
    asyncio.run(run_interview_and_trace())
