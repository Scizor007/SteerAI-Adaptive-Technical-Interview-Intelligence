"""
Application configuration.
Centralizes all environment and runtime settings.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Server
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

# CORS
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

# Interview settings
MAX_QUESTIONS_PER_INTERVIEW = int(os.getenv("MAX_QUESTIONS", "10"))
MAX_FOLLOWUPS_PER_TOPIC = int(os.getenv("MAX_FOLLOWUPS", "2"))

# Data paths
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
CURRICULUM_PATH = os.path.join(DATA_DIR, "curriculum.json")
CANDIDATES_PATH = os.path.join(DATA_DIR, "candidates.json")

# LLM Provider (Gemini) Settings
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))
LLM_TOP_P = float(os.getenv("LLM_TOP_P", "0.9"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "1024"))
LLM_RETRY_COUNT = int(os.getenv("LLM_RETRY_COUNT", "1"))
LLM_TIMEOUT = float(os.getenv("LLM_TIMEOUT", "15.0"))
