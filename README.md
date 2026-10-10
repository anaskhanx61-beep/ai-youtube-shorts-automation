# AI YouTube Shorts Automation

A free local Python app that generates AI scripts, creates Shorts videos with captions, and can auto-upload to YouTube when configured.

Features:
- Generates its own scripts using Ollama (free local AI)
- Creates a 20–35 second Shorts video with captions
- Adds background visuals and voice-over using Google Text-to-Speech
- Supports YouTube upload via Google API
- Runs on a schedule using APScheduler
- Includes a local web dashboard

## Tech stack
- Python
- Flask
- MoviePy
- Pillow
- gTTS
- APScheduler
- Ollama (local, free)

## Quick start

1. Install Ollama: https://ollama.com/
2. Pull a model:
   ```bash
   ollama pull llama3.2
   ```
3. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   # .venv\Scripts\activate  # Windows
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Start the app:
   ```bash
   python app.py
   ```
6. Open: http://localhost:5000

## Environment
Copy `.env.example` to `.env` and edit it:

```bash
cp .env.example .env
```

Example:
```env
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
DEFAULT_TOPIC=AI tools for beginners
APP_PORT=5000
AUTO_UPLOAD_TO_YOUTUBE=false
YOUTUBE_CLIENT_SECRETS_FILE=client_secret.json
YOUTUBE_VIDEO_CATEGORY=22
```

## Typical workflow
1. Enter a topic in the dashboard.
2. Click Generate
3. The app creates a script, voice-over, visuals, and captions.
4. Optionally upload to YouTube.
5. Schedule recurring daily or hourly jobs.

## YouTube upload setup (optional)
1. Create Google OAuth credentials at Google Cloud Console.
2. Download `client_secret.json`.
3. Place it in the project root.
4. Run the upload flow once; the app will save `token.json`.
5. Set `AUTO_UPLOAD_TO_YOUTUBE=true` or use the dashboard to upload.

## Notes
- This app uses local AI through Ollama, so there is no paid AI key requirement.
- If you do not have Ollama installed or the model is unavailable, the app falls back to a built-in script generator.

## Project structure
```text
app.py
config.py
requirements.txt
.env.example
services/
  __init__.py
  ollama_client.py
  script_generator.py
  video_processor.py
  youtube_uploader.py
templates/
  index.html
static/
  styles.css
output/
```

## License
MIT
