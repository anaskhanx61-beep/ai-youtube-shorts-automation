import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
VIDEOS_DIR = OUTPUT_DIR / "videos"
AUDIOS_DIR = OUTPUT_DIR / "audio"
IMAGES_DIR = OUTPUT_DIR / "images"
LOGS_DIR = OUTPUT_DIR / "logs"

for directory in [OUTPUT_DIR, VIDEOS_DIR, AUDIOS_DIR, IMAGES_DIR, LOGS_DIR]:
    directory.mkdir(exist_ok=True, parents=True)

APP_PORT = int(os.getenv("APP_PORT", "5000"))
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
DEFAULT_TOPIC = os.getenv("DEFAULT_TOPIC", "AI tools for beginners")
AUTO_UPLOAD_TO_YOUTUBE = os.getenv("AUTO_UPLOAD_TO_YOUTUBE", "false").lower() == "true"
YOUTUBE_CLIENT_SECRETS_FILE = os.getenv("YOUTUBE_CLIENT_SECRETS_FILE", "client_secret.json")
YOUTUBE_VIDEO_CATEGORY = os.getenv("YOUTUBE_VIDEO_CATEGORY", "22")
