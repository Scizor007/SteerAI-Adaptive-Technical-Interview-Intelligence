import logging
from typing import Any, Dict, Optional
import google.generativeai as genai
from google.generativeai.types import GenerationConfig
from google.api_core.exceptions import RetryError, GoogleAPIError

import config
from services.parsers.llm_parser import LLMParser

logger = logging.getLogger(__name__)

class LLMService:
    """
    Dedicated AI layer for communicating with Gemini.
    Handles configuration, retries, and parsing.
    """

    def __init__(self):
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
        
        while attempts < max_attempts:
            try:
                # Synchronous call (can be made async if needed, but keeping it simple as requested)
                response = self.model.generate_content(prompt)
                
                if not response.text:
                    raise ValueError("Empty response from Gemini")
                    
                return LLMParser.parse_json(response.text)
                
            except (ValueError, GoogleAPIError, RetryError, Exception) as e:
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
                "weaknesses": [],
                "recommendations": ["Review topics independently."],
                "overall_summary": "System error prevented full AI evaluation."
            }
        return {}
