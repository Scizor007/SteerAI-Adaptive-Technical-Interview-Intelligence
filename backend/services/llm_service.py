import logging
from typing import Any, Dict, Optional

try:
    import google.generativeai as genai
    from google.generativeai.types import GenerationConfig
except ImportError:  # Allows deterministic tests and fallback mode without the optional SDK installed.
    genai = None
    GenerationConfig = None

import config
from services.parsers.llm_parser import LLMParser

logger = logging.getLogger(__name__)

class LLMService:
    """
    Dedicated AI layer for communicating with Gemini.
    Handles configuration, retries, and parsing.
    """

    def __init__(self):
        self.model = None
        if genai is None or GenerationConfig is None:
            logger.warning("google-generativeai is not installed. LLMService will use fallbacks.")
            return
        if not config.GEMINI_API_KEY:
            logger.warning("GEMINI_API_KEY is not set. LLMService will fail.")
            
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model_name = config.MODEL_NAME
        
        # Configure model parameters
        self.generation_config = GenerationConfig(
            temperature=config.LLM_TEMPERATURE,
            top_p=config.LLM_TOP_P,
            max_output_tokens=config.LLM_MAX_TOKENS,
            response_mime_type="application/json"
        )
        
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=self.generation_config
        )

    def generate_json(self, prompt: str, fallback_type: str = "question") -> Dict[str, Any]:
        """
        Sends the prompt to Gemini and parses the response as JSON.
        Implements single retry logic per configuration.
        """
        attempts = 0
        max_attempts = config.LLM_RETRY_COUNT + 1

        if self.model is None:
            return self._get_fallback(fallback_type)
        
        while attempts < max_attempts:
            try:
                # Synchronous call (can be made async if needed, but keeping it simple as requested)
                response = self.model.generate_content(prompt)
                
                if not response.text:
                    raise ValueError("Empty response from Gemini")
                    
                return LLMParser.parse_json(response.text)
                
            except Exception as e:
                attempts += 1
                logger.error(f"LLM Generation failed (attempt {attempts}/{max_attempts}): {e}")
                if attempts >= max_attempts:
                    logger.warning("Max retries reached. Returning fallback response.")
                    return self._get_fallback(fallback_type)

    def _get_fallback(self, fallback_type: str) -> Dict[str, Any]:
        """Returns a graceful fallback so the interview session doesn't crash."""
        if fallback_type == "question" or fallback_type == "followup":
            return {
                "question": "Could you elaborate a bit more on your previous experiences?",
                "expected_points": [],
                "estimated_difficulty": "Medium"
            }
        elif fallback_type == "feedback":
            return {
                "summary": "The candidate completed the interview, but detailed AI evaluation was temporarily unavailable.",
                "strengths": ["Completed the assessment."],
                "gaps": ["Detailed feedback could not be generated."],
                "next": ["Review the evidence collected during the assessment."],
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
            }
        return {}
