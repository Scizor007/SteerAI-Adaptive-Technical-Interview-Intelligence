import json
import re
from typing import Any, Dict

class LLMParser:
    """Parses and validates LLM JSON output."""

    @staticmethod
    def parse_json(text: str) -> Dict[str, Any]:
        """
        Extracts and parses JSON from the LLM output.
        Strips markdown formatting if present.
        """
        if not text:
            raise ValueError("Empty response from LLM")
            
        # Remove markdown code blocks if present
        text = text.strip()
        if text.startswith("```"):
            # Use regex to remove opening ```json (or similar) and closing ```
            text = re.sub(r"^```[a-zA-Z]*\n", "", text)
            text = re.sub(r"\n```$", "", text)
            text = text.strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse LLM response as JSON: {str(e)}\nRaw Output: {text}")

    @staticmethod
    def extract_fallback_question(text: str) -> Dict[str, Any]:
        """Graceful fallback if JSON fails completely for a question generation."""
        # If the LLM didn't return JSON, just wrap the raw text in our schema
        return {
            "question": text,
            "expected_points": [],
            "estimated_difficulty": "Medium"
        }
