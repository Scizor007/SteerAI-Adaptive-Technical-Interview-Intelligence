"""
READ-ONLY audit of OpenRouter evaluation pipeline.
Collects statistics and evidence without modifying any code.
"""
import asyncio
import sys
import os
import json

# Add backend root to path
backend_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, backend_root)

# Fix Windows console encoding
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from modules.interview_manager import InterviewManager
from modules.candidate_loader import CandidateLoader
from services.llm_service import LLMService
from services.parsers.llm_parser import LLMParser

# Statistics tracking
eval_stats = {
    'total_requests': 0,
    'successful': 0,
    'fallback': 0,
    'parse_errors': 0,
    'api_errors': 0,
    'timeout_errors': 0,
    'successful_responses': [],
    'failed_responses': [],
    'error_details': []
}

# Monkey-patch to intercept evaluation calls
original_generate_json = LLMService.generate_json
original_parse_json = LLMParser.parse_json

def traced_parse_json(response_text: str):
    """Intercept parse_json to capture responses."""
    try:
        result = original_parse_json(response_text)
        return result
    except Exception as e:
        # Capture failed parse
        eval_stats['parse_errors'] += 1
        eval_stats['failed_responses'].append({
            'raw_response': response_text[:1000],
            'error': str(e),
            'error_type': type(e).__name__
        })
        raise

def traced_generate_json(self, prompt: str, fallback_type: str = "question", caller_module: str = "unknown"):
    """Intercept generate_json to track evaluation calls."""
    
    # Only track evaluation calls
    if fallback_type == "evaluation":
        eval_stats['total_requests'] += 1
    
    try:
        result = original_generate_json(self, prompt, fallback_type, caller_module)
        
        # Check if it's an evaluation call
        if fallback_type == "evaluation":
            if result.get('_fallback'):
                eval_stats['fallback'] += 1
                eval_stats['error_details'].append({
                    'reason': 'LLM returned fallback',
                    'details': 'Provider unavailable or all retries failed'
                })
            else:
                eval_stats['successful'] += 1
                # Store successful response sample
                if len(eval_stats['successful_responses']) < 2:
                    eval_stats['successful_responses'].append({
                        'accuracy': result.get('accuracy'),
                        'reasoning': result.get('reasoning'),
                        'depth': result.get('depth'),
                        'sample': str(result)[:500]
                    })
        
        return result
    except Exception as e:
        if fallback_type == "evaluation":
            eval_stats['api_errors'] += 1
            eval_stats['error_details'].append({
                'reason': f'Exception: {type(e).__name__}',
                'details': str(e)[:200]
            })
        raise

# Apply patches
LLMService.generate_json = traced_generate_json
LLMParser.parse_json = traced_parse_json

async def audit_evaluation_pipeline():
    """Run a complete interview and audit evaluation pipeline."""
    print("\n" + "="*80)
    print("OPENROUTER EVALUATION PIPELINE AUDIT")
    print("="*80 + "\n")
    
    # Load candidate
    loader = CandidateLoader()
    candidate = loader.candidates[0]
    print(f"Candidate: {candidate.member.name}")
    print(f"Starting interview to collect evaluation statistics...\n")
    
    manager = InterviewManager()
    session_id = "eval-audit-001"
    
    # Start interview
    response = await manager.start_interview(session_id, candidate)
    
    # Submit answers until complete (max 15)
    for i in range(1, 16):
        if response.done:
            break
        
        # Vary answer quality to test evaluation
        if i % 3 == 0:
            answer = "I don't know."
        elif i % 3 == 1:
            answer = "I have extensive experience with this. I've implemented production systems using best practices including error handling, logging, testing, monitoring, CI/CD, containerization, and cloud architectures."
        else:
            answer = "I understand the basic concepts and have worked with similar technologies in academic projects."
        
        response = await manager.continue_interview(session_id, answer)
    
    # Print statistics
    print("\n" + "="*80)
    print("EVALUATION STATISTICS")
    print("="*80 + "\n")
    
    print(f"1. Total Evaluation Requests: {eval_stats['total_requests']}")
    print(f"2. Successful Evaluations: {eval_stats['successful']}")
    print(f"3. Fallback Evaluations: {eval_stats['fallback']}")
    
    if eval_stats['successful'] > 0:
        success_rate = (eval_stats['successful'] / eval_stats['total_requests']) * 100
        print(f"   Success Rate: {success_rate:.1f}%")
    
    print(f"\n4. Failure Breakdown:")
    print(f"   - Parse Errors: {eval_stats['parse_errors']}")
    print(f"   - API Errors: {eval_stats['api_errors']}")
    print(f"   - Timeout Errors: {eval_stats['timeout_errors']}")
    
    # Analyze failure reasons
    print(f"\n5. Failure Analysis:")
    if eval_stats['error_details']:
        for idx, error in enumerate(eval_stats['error_details'][:5], 1):
            print(f"\n   Failure #{idx}:")
            print(f"   Reason: {error['reason']}")
            print(f"   Details: {error['details']}")
    else:
        print("   No failures detected")
    
    # Show successful response
    print(f"\n" + "="*80)
    print("6. SUCCESSFUL EVALUATION SAMPLE")
    print("="*80)
    if eval_stats['successful_responses']:
        sample = eval_stats['successful_responses'][0]
        print(f"\nAccuracy: {sample['accuracy']}")
        print(f"Reasoning: {sample['reasoning']}")
        print(f"Depth: {sample['depth']}")
        print(f"\nFull response preview:")
        print(sample['sample'])
    else:
        print("\nNo successful evaluations captured")
    
    # Show failed response
    print(f"\n" + "="*80)
    print("7. FAILED EVALUATION SAMPLE")
    print("="*80)
    if eval_stats['failed_responses']:
        failed = eval_stats['failed_responses'][0]
        print(f"\nError Type: {failed['error_type']}")
        print(f"Error Message: {failed['error']}")
        print(f"\nRaw Response (first 1000 chars):")
        print(failed['raw_response'])
        
        # Parse error analysis
        print(f"\n" + "="*80)
        print("8. PARSING FAILURE ANALYSIS")
        print("="*80)
        
        raw = failed['raw_response']
        error_msg = failed['error']
        
        print(f"\nError: {error_msg}")
        print(f"\nResponse length: {len(raw)} characters")
        
        # Check for common issues
        issues = []
        if 'Expecting value' in error_msg:
            issues.append("Missing value after colon")
        if 'Expecting \',\' delimiter' in error_msg:
            issues.append("Missing comma between fields")
        if raw.count('{') != raw.count('}'):
            issues.append(f"Unmatched braces: {raw.count('{')} opening, {raw.count('}')} closing")
        if raw.count('[') != raw.count(']'):
            issues.append(f"Unmatched brackets: {raw.count('[')} opening, {raw.count(']')} closing")
        if not raw.strip().endswith('}') and not raw.strip().endswith(']'):
            issues.append("Response appears truncated (doesn't end with } or ])")
        
        print(f"\nIdentified Issues:")
        for issue in issues:
            print(f"  - {issue}")
        
        # Check for truncation
        if "reasoning" in raw and ": ," in raw:
            print("\n⚠ CRITICAL: Empty values detected (e.g., 'reasoning': ,)")
            print("This indicates the model generated incomplete JSON")
        
        if len(raw) >= 900:
            print(f"\n⚠ WARNING: Response near token limit ({len(raw)} chars)")
            print("May be truncated due to max_tokens setting")
    else:
        print("\nNo failed evaluations captured")
    
    # Recommendations
    print(f"\n" + "="*80)
    print("9. RECOMMENDED FIXES")
    print("="*80 + "\n")
    
    if eval_stats['parse_errors'] > 0:
        print("PRIMARY ISSUE: JSON parsing failures")
        print("\nROOT CAUSE:")
        if eval_stats['failed_responses']:
            first_fail = eval_stats['failed_responses'][0]
            if ": ," in first_fail['raw_response']:
                print("  The model (meta-llama/llama-3.2-3b-instruct) generates incomplete JSON")
                print("  with empty values like 'reasoning': , instead of 'reasoning': 0")
            else:
                print("  Response is truncated or malformed")
        
        print("\nSMALLEST FIX (in order of preference):")
        print("\n  Option 1: Use more reliable model")
        print("    Change OPENROUTER_MODEL in .env to:")
        print("    - google/gemini-flash-1.5 (better JSON generation)")
        print("    - anthropic/claude-3-haiku (reliable structured output)")
        print("    - openai/gpt-3.5-turbo (good JSON compliance)")
        
        print("\n  Option 2: Add JSON repair in parser")
        print("    Modify services/parsers/llm_parser.py to:")
        print("    - Replace empty values: ': ,' → ': 0,'")
        print("    - Add missing closing braces")
        print("    - Strip trailing incomplete fields")
        
        print("\n  Option 3: Increase max_tokens")
        print("    Current: LLM_MAX_TOKENS=2048")
        print("    Try: LLM_MAX_TOKENS=4096")
        print("    (May reduce truncation but won't fix malformed JSON)")
        
        print("\n  Option 4: Simplify evaluation prompt")
        print("    Reduce expected output fields to minimize generation errors")
    
    elif eval_stats['api_errors'] > 0:
        print("PRIMARY ISSUE: API errors")
        print("\nCheck OpenRouter status and API key validity")
    
    elif eval_stats['timeout_errors'] > 0:
        print("PRIMARY ISSUE: Timeout errors")
        print("\nIncrease LLM_TIMEOUT in .env")
    
    else:
        print("✅ No issues detected - evaluation pipeline working correctly")
    
    print("\n" + "="*80)
    print("AUDIT COMPLETE")
    print("="*80)

if __name__ == "__main__":
    asyncio.run(audit_evaluation_pipeline())
