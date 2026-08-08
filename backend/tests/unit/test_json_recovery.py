"""
Unit tests for JSON recovery layer in LLMParser.
"""
import unittest
import sys
import os

# Add backend root to path
backend_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, backend_root)

from services.parsers.llm_parser import LLMParser


class TestJSONRecovery(unittest.TestCase):
    """Test JSON recovery capabilities."""
    
    def test_valid_json_unchanged(self):
        """Valid JSON should parse without modification."""
        valid_json = '{"accuracy": 5, "reasoning": 7, "depth": 6}'
        result = LLMParser.parse_json(valid_json)
        
        self.assertEqual(result['accuracy'], 5)
        self.assertEqual(result['reasoning'], 7)
        self.assertEqual(result['depth'], 6)
    
    def test_markdown_fenced_json(self):
        """Markdown-fenced JSON should be extracted and parsed."""
        fenced = '''```json
{
  "accuracy": 8,
  "reasoning": 9
}
```'''
        result = LLMParser.parse_json(fenced)
        
        self.assertEqual(result['accuracy'], 8)
        self.assertEqual(result['reasoning'], 9)
    
    def test_trailing_comma(self):
        """Trailing commas should be removed."""
        with_trailing = '{"accuracy": 5, "reasoning": 7,}'
        result = LLMParser.parse_json(with_trailing)
        
        self.assertEqual(result['accuracy'], 5)
        self.assertEqual(result['reasoning'], 7)
    
    def test_empty_numeric_value_comma(self):
        """Empty numeric values like 'key': , should become 'key': 0."""
        empty_value = '{"accuracy": 5, "reasoning": , "depth": 3}'
        result = LLMParser.parse_json(empty_value)
        
        self.assertEqual(result['accuracy'], 5)
        self.assertEqual(result['reasoning'], 0)
        self.assertEqual(result['depth'], 3)
    
    def test_empty_numeric_value_at_end(self):
        """Empty numeric value before closing brace."""
        empty_at_end = '{"accuracy": 5, "reasoning": }'
        result = LLMParser.parse_json(empty_at_end)
        
        self.assertEqual(result['accuracy'], 5)
        self.assertEqual(result['reasoning'], 0)
    
    def test_missing_closing_brace(self):
        """Missing closing brace should be added."""
        missing_brace = '{"accuracy": 5, "reasoning": 7'
        result = LLMParser.parse_json(missing_brace)
        
        self.assertEqual(result['accuracy'], 5)
        self.assertEqual(result['reasoning'], 7)
    
    def test_missing_multiple_closing_braces(self):
        """Multiple missing closing braces should be added."""
        nested = '{"outer": {"inner": {"accuracy": 5'
        result = LLMParser.parse_json(nested)
        
        self.assertEqual(result['outer']['inner']['accuracy'], 5)
    
    def test_missing_closing_bracket(self):
        """Missing closing bracket in array should be added."""
        missing_bracket = '{"items": [1, 2, 3'
        result = LLMParser.parse_json(missing_bracket)
        
        self.assertEqual(result['items'], [1, 2, 3])
    
    def test_empty_array_truncated(self):
        """Truncated empty array should be completed."""
        truncated_array = '{"items": ['
        result = LLMParser.parse_json(truncated_array)
        
        self.assertEqual(result['items'], [])
    
    def test_complex_recovery(self):
        """Multiple issues should all be repaired."""
        complex = '{"accuracy": 5, "reasoning": , "items": [1, 2,], "depth":'
        result = LLMParser.parse_json(complex)
        
        self.assertEqual(result['accuracy'], 5)
        self.assertEqual(result['reasoning'], 0)
        self.assertEqual(result['items'], [1, 2])
        # 'depth' field should be stripped as incomplete
    
    def test_real_llama_truncation(self):
        """Real truncation pattern from llama-3.2-3b."""
        # Pattern 1: Stops after colon
        truncated = '''{
  "accuracy": 2,
  "reasoning":'''
        result = LLMParser.parse_json(truncated)
        
        self.assertEqual(result['accuracy'], 2)
        # Incomplete field 'reasoning' should be stripped
        # We accept either it's not present or repaired to 0
        self.assertIsInstance(result, dict)
    
    def test_real_llama_empty_values(self):
        """Real empty value pattern from llama-3.2-3b."""
        empty_vals = '''{
  "accuracy": 0,
  "reasoning": ,
  "depth": 0,
  "completeness": 0'''
        result = LLMParser.parse_json(empty_vals)
        
        self.assertEqual(result['accuracy'], 0)
        self.assertEqual(result['reasoning'], 0)
        self.assertEqual(result['depth'], 0)
        self.assertEqual(result['completeness'], 0)
    
    def test_complete_evaluation_valid(self):
        """Complete valid evaluation should parse normally."""
        complete = '''{
  "accuracy": 6,
  "reasoning": 8,
  "depth": 5,
  "completeness": 4,
  "communication": 7,
  "confidence": 5,
  "strengths": ["Good explanation"],
  "missing_points": ["Lacked details"],
  "misconceptions": [],
  "suggested_followup": "Ask for more details",
  "topic_mastery": "Medium"
}'''
        result = LLMParser.parse_json(complete)
        
        self.assertEqual(result['accuracy'], 6)
        self.assertEqual(result['reasoning'], 8)
        self.assertEqual(len(result['strengths']), 1)
        self.assertEqual(result['topic_mastery'], 'Medium')
    
    def test_irreparable_json_raises(self):
        """Completely invalid JSON should still raise exception."""
        invalid = 'not json at all { broken'
        
        with self.assertRaises(ValueError):
            LLMParser.parse_json(invalid)
    
    def test_empty_response_raises(self):
        """Empty response should raise exception."""
        with self.assertRaises(ValueError):
            LLMParser.parse_json('')


if __name__ == '__main__':
    unittest.main()
