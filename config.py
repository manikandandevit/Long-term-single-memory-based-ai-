import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

MODEL_NAME = "xiaomi/mimo-v2-flash:free"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

