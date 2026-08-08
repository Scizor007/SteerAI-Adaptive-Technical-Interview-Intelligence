import json
import logging
import re
from typing import Any, Dict

logger = logging.getLogger(__name__)

class LLMParser:
    """Parses and validates LLM JSON output with automatic recovery."""

    @staticmethod
    def parse_json(text: str) -> Dict[str, Any]:
        """
        Extracts and parses JSON from the LLM output.
        
        Pipeline:
        1. Attempt normal parsing
        2. If fails, attempt lightweight recovery
        3. If recovery succeeds, log and return
        4. If recovery fails, raise exception for fallback
        """
        if not text:
            raise ValueError("Empty response from LLM")
        
        original_length = len(text)
        text = text.strip()
        
        # Step 1: Remove markdown code blocks if present
        if text.startswith("```"):
            text = re.sub(r"^```[a-zA-Z]*\n", "", text)
            text = re.sub(r"\n```$", "", text)
            text = text.strip()

        # Step 2: Attempt normal JSON parsing
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            # Step 3: Normal parsing failed, attempt recovery
            logger.debug(f"[JSON RECOVERY] Initial parse failed: {str(e)}")
            logger.debug(f"[JSON RECOVERY] Original length: {original_length} chars")
            
            try:
                repaired_text, repairs = LLMParser._repair_json(text)
                
                # Step 4: Attempt parsing repaired JSON
                result = json.loads(repaired_text)
                
                # Step 5: Recovery succeeded - log details
                logger.warning(f"[JSON RECOVERY] Successfully repaired malformed JSON")
                logger.warning(f"[JSON RECOVERY] Original length: {original_length} chars")
                logger.warning(f"[JSON RECOVERY] Repaired length: {len(repaired_text)} chars")
                logger.warning(f"[JSON RECOVERY] Repairs applied: {', '.join(repairs)}")
                
                return result
                
            except (json.JSONDecodeError, Exception) as recovery_error:
                # Step 6: Recovery failed, raise original error for fallback
                logger.error(f"[JSON RECOVERY] Recovery failed: {str(recovery_error)}")
                raise ValueError(f"Failed to parse LLM response as JSON: {str(e)}\nRaw Output: {text[:500]}")

    @staticmethod
    def _repair_json(text: str) -> tuple[str, list[str]]:
        """
        Attempt to repair common JSON syntax errors from LLM responses.
        
        Returns:
            tuple: (repaired_text, list_of_repairs_applied)
        """
        repairs = []
        original = text
        
        # Repair 1: Remove trailing commas before closing braces/brackets
        if re.search(r',\s*[}\]]', text):
            text = re.sub(r',(\s*[}\]])', r'\1', text)
            repairs.append("removed trailing commas")
        
        # Repair 2: Fix incomplete fields at end - "key": \n or "key": EOF
        # Strip the incomplete field entirely
        text = re.sub(r',?\s*"[^"]+"\s*:\s*$', '', text)
        
        # Repair 3: Fix empty numeric values - "key": , or "key": } or "key": ]
        # Replace with "key": 0
        if re.search(r':\s*[,}\]]', text):
            text = re.sub(r':\s*,', ': 0,', text)
            text = re.sub(r':\s*}', ': 0}', text)
            text = re.sub(r':\s*]', ': 0]', text)
            repairs.append("filled empty numeric values with 0")
        
        # Repair 4: Fix truncated strings - "key": "value (missing closing quote)
        # Look for quotes followed by newline or EOF without closing quote
        if re.search(r':\s*"[^"]*$', text):
            text = re.sub(r':\s*"([^"]*?)$', r': "\1"', text)
            repairs.append("closed truncated string")
        
        # Repair 5: Fix incomplete array at end - "key": [
        # Complete as empty array
        text = re.sub(r':\s*\[\s*$', ': []', text)
        
        # Repair 6: Close array values if we have open bracket
        # Add closing bracket before closing brace if needed
        # Pattern: [ ... no closing bracket before }
        if '[' in text and text.count('[') > text.count(']'):
            # Find positions
            last_open_bracket = text.rfind('[')
            last_close_brace = text.rfind('}')
            
            # If there's a { after the [, we need to close both
            if last_close_brace == -1 or last_open_bracket > last_close_brace:
                # No closing brace yet, will be added in next step
                pass
            else:
                # There's a closing brace, add ] before it
                text = text[:last_close_brace] + ']' + text[last_close_brace:]
                repairs.append("closed array before closing brace")
        
        # Repair 7: Close missing braces/brackets
        open_braces = text.count('{')
        close_braces = text.count('}')
        open_brackets = text.count('[')
        close_brackets = text.count(']')
        
        # Close brackets first (inner structures)
        if open_brackets > close_brackets:
            missing = open_brackets - close_brackets
            text += ']' * missing
            repairs.append(f"added {missing} missing closing bracket(s)")
        
        # Then close braces (outer structures)
        if open_braces > close_braces:
            missing = open_braces - close_braces
            text += '}' * missing
            repairs.append(f"added {missing} missing closing brace(s)")
        
        if repairs:
            logger.debug(f"[JSON RECOVERY] Original: {original[:200]}...")
            logger.debug(f"[JSON RECOVERY] Repaired: {text[:200]}...")
        
        return text, repairs

    @staticmethod
    def extract_fallback_question(text: str) -> Dict[str, Any]:
        """Graceful fallback if JSON fails completely for a question generation."""
        # If the LLM didn't return JSON, just wrap the raw text in our schema
        return {
            "question": text,
            "expected_points": [],
            "estimated_difficulty": "Medium"
        }
