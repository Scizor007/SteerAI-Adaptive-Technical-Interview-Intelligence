import logging
from typing import Any, Dict

import config
from services.parsers.llm_parser import LLMParser
from services.llm.provider import LLMProvider

logger = logging.getLogger(__name__)

class LLMService:
    """
    Dedicated AI layer for communicating with LLMs.
    Handles configuration, routing to providers, retries, and parsing.
    """

    def __init__(self):
        self.provider: LLMProvider | None = None
        
        provider_name = config.LLM_PROVIDER
        
        # Startup validation and logging
        logger.info("="*80)
        logger.info("[LLM CONFIG] Initializing LLM Service")
        logger.info(f"[LLM CONFIG] Provider: {provider_name}")
        
        if provider_name == "openrouter":
            from services.llm.openrouter_provider import OpenRouterProvider
            
            if not config.OPENROUTER_API_KEY or config.OPENROUTER_API_KEY.startswith("<"):
                logger.error("[LLM CONFIG] CRITICAL: OPENROUTER_API_KEY is not configured!")
                logger.error("[LLM CONFIG] Application will use fallbacks for all LLM calls")
                logger.error("[LLM CONFIG] Set OPENROUTER_API_KEY in .env file")
                self.provider = None
            else:
                logger.info(f"[LLM CONFIG] Model: {config.OPENROUTER_MODEL}")
                logger.info(f"[LLM CONFIG] API Key: configured (not shown)")
                self.provider = OpenRouterProvider()
                
        elif provider_name == "gemini":
            from services.llm.gemini_provider import GeminiProvider
            
            if not config.GEMINI_API_KEY or config.GEMINI_API_KEY.startswith("<"):
                logger.error("[LLM CONFIG] CRITICAL: GEMINI_API_KEY is not configured!")
                logger.error("[LLM CONFIG] Application will use fallbacks for all LLM calls")
                logger.error("[LLM CONFIG] Set GEMINI_API_KEY in .env file")
                self.provider = None
            else:
                logger.info(f"[LLM CONFIG] Model: {config.MODEL_NAME}")
                logger.info(f"[LLM CONFIG] API Key: configured (not shown)")
                self.provider = GeminiProvider()
        else:
            logger.error(f"[LLM CONFIG] Unknown LLM_PROVIDER '{provider_name}'")
            logger.error("[LLM CONFIG] Valid options: 'gemini', 'openrouter'")
            logger.error("[LLM CONFIG] Application will use fallbacks for all LLM calls")
            self.provider = None
            
        logger.info("="*80)

    def generate_json(self, prompt: str, fallback_type: str = "question", caller_module: str = "unknown") -> Dict[str, Any]:
        """
        Sends the prompt to the configured provider and parses the response as JSON.
        Implements single retry logic per configuration.
        """
        # AUDIT: Log every API call attempt
        import inspect
        if caller_module == "unknown":
            frame = inspect.currentframe()
            if frame and frame.f_back and frame.f_back.f_back:
                caller_module = frame.f_back.f_back.f_code.co_filename.split('\\')[-1].replace('.py', '')
        
        prompt_tokens = len(prompt.split())  # Rough approximation
        
        logger.info("="*80)
        logger.info(f"[AUDIT] LLM API CALL #{getattr(self, '_call_count', 0) + 1}")
        logger.info(f"[AUDIT] Caller Module: {caller_module}")
        logger.info(f"[AUDIT] Call Type: {fallback_type}")
        logger.info(f"[AUDIT] Provider: {self.provider.display_name if self.provider else 'None'}")
        logger.info(f"[AUDIT] Approximate Input Tokens: {prompt_tokens}")
        logger.info(f"[AUDIT] Prompt Preview (first 200 chars): {prompt[:200]}...")
        logger.info("="*80)
        
        if not hasattr(self, '_call_count'):
            self._call_count = 0
        self._call_count += 1
        
        attempts = 0
        max_attempts = config.LLM_RETRY_COUNT + 1

        if self.provider is None:
            logger.warning(f"[AUDIT] Provider unavailable - returning fallback for: {fallback_type}")
            return self._get_fallback(fallback_type)
        
        while attempts < max_attempts:
            try:
                # Synchronous call via provider abstraction
                response_text = self.provider.generate_text(prompt)
                
                output_tokens = len(response_text.split())
                logger.info(f"[AUDIT] Response received - Approximate Output Tokens: {output_tokens}")
                    
                return LLMParser.parse_json(response_text)
                
            except Exception as e:
                attempts += 1
                logger.error(f"[AUDIT] LLM call failed (attempt {attempts}/{max_attempts}): {str(e)[:200]}")
                if attempts >= max_attempts:
                    logger.warning(f"[AUDIT] Max retries reached - returning fallback for: {fallback_type}")
                    return self._get_fallback(fallback_type)

    def _get_fallback(self, fallback_type: str) -> Dict[str, Any]:
        """Returns a graceful fallback so the interview session doesn't crash."""
        logger.warning(f"[FALLBACK ACTIVATED] Returning fallback response for type: {fallback_type}")
        logger.warning("[FALLBACK ACTIVATED] This indicates LLM unavailability - check API quota/key")
        
        if fallback_type == "question" or fallback_type == "followup":
            return {
                "question": "Could you elaborate a bit more on your previous experiences?",
                "expected_points": [],
                "estimated_difficulty": "Medium",
                "_fallback": True,  # Flag for detection
            }
        elif fallback_type == "feedback":
            return {
                "summary": "The candidate completed the interview, but detailed AI evaluation was temporarily unavailable.",
                "strengths": ["Completed the assessment."],
                "gaps": ["Detailed feedback could not be generated."],
                "next": ["Review the evidence collected during the assessment."],
                "_fallback": True,  # Flag for detection
            }
        elif fallback_type == "evaluation":
            return {
                "accuracy": 0,
                "reasoning": 0,
                "depth": 0,
                "completeness": 0,
                "communication": 0,
                "confidence": 0,
                "strengths": [],
                "missing_points": ["Automated evaluation was unavailable."],
                "misconceptions": [],
                "suggested_followup": None,
                "topic_mastery": "Low",
                "interviewer_notes": "No LLM evaluation was available for this answer.",
                "_fallback": True,  # Flag for detection
            }
        return {}
