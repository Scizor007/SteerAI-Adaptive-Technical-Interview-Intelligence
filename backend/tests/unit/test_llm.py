import unittest
import json
import os
from unittest.mock import patch, MagicMock

# Set mock env vars before importing config to avoid test failure if API key is missing locally
os.environ["GEMINI_API_KEY"] = "mock_key"

from services.parsers.llm_parser import LLMParser
from services.prompt_builders.question_prompt import build_question_prompt
from models.schemas import CandidateProfile, Member, Mission, Signals, PlannedTopic, Difficulty, TopicPriority

class TestLLMParser(unittest.TestCase):
    def test_parse_valid_json(self):
        text = '{"question": "test?"}'
        result = LLMParser.parse_json(text)
        self.assertEqual(result["question"], "test?")

    def test_parse_markdown_json(self):
        text = "```json\n{\n\"question\": \"test?\"\n}\n```"
        result = LLMParser.parse_json(text)
        self.assertEqual(result["question"], "test?")
        
    def test_parse_invalid_json_raises_value_error(self):
        text = "This is just text"
        with self.assertRaises(ValueError):
            LLMParser.parse_json(text)

class TestPromptBuilders(unittest.TestCase):
    def test_build_question_prompt(self):
        candidate = CandidateProfile(
            member=Member(id="1", name="Alice", jobRole="Dev", yearsExperience=5, education="", status=""),
            missions=[],
            signals=Signals(commitDays=1, missionsCompleted=1, missionsFirstTry=1)
        )
        topic = PlannedTopic(
            day=1, title="FastAPI", module_name="Backend", priority=TopicPriority.HIGH,
            difficulty=Difficulty.INTERMEDIATE, reason="test"
        )
        prompt = build_question_prompt(topic, candidate, "mid", ["What is REST?"])
        
        self.assertIn("Alice", prompt)
        self.assertIn("FastAPI", prompt)
        self.assertIn("What is REST?", prompt)
        self.assertIn("JSON", prompt)

if __name__ == "__main__":
    unittest.main()
