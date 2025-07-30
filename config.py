"""
Configuration settings for the Video Learning Assistant
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
VIDEODB_API_KEY = os.getenv("VIDEODB_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# App Settings
APP_TITLE = "Video Learning Assistant"
APP_ICON = "🎓"
MAX_TRANSCRIPT_LENGTH = 500
MAX_SUMMARY_SENTENCES = 4

# OpenAI Settings
OPENAI_MODEL = "gpt-4o-mini"  # Latest OpenAI model
MAX_TOKENS = 150
TEMPERATURE = 0.3

# VideoDB Settings
DEFAULT_COLLECTION_NAME = "Video Learning Collection"