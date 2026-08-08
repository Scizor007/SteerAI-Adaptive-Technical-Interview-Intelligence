import sys
import os
import json
import logging

logging.basicConfig(level=logging.DEBUG)

# Add the backend dir to the path so imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.schemas import CandidateProfile, Member, Signals, PlannedTopic, Difficulty, TopicPriority, InterviewContext, QuestionRecord
from services.llm_service import LLMService
from modules.evaluation_engine import EvaluationEngine

def test_eval():
    llm = LLMService()
    engine = EvaluationEngine(llm_service=llm)

    context = InterviewContext(
        session_id="test-001",
        candidate=CandidateProfile(
            member=Member(id="1", name="Test", jobRole="Dev", yearsExperience=5, education="", status=""),
            missions=[],
            signals=Signals(commitDays=1, missionsCompleted=1, missionsFirstTry=1)
        ),
        plan=[],
        evaluations=[],
        topic_mastery={}
    )

    current_question = QuestionRecord(
        topic="FastAPI",
        question="What is FastAPI?",
        expected_points=["REST API", "Starlette", "Pydantic"],
        difficulty=Difficulty.INTERMEDIATE,
        answer="sss"
    )

    print("Evaluating 'sss'...")
    res = engine.evaluate_response(context, current_question, "sss")
    print("\nResult:")
    print(res.model_dump_json(indent=2))

if __name__ == "__main__":
    test_eval()
