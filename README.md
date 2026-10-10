# AI YouTube Shorts Automation

A free local Python app for creating YouTube Shorts using local AI (Ollama), text-to-speech, captions, and optional YouTube upload.

## Features
- Generate its own script from any topic
- Convert script to voice-over with Google TTS
- Add dynamic captions and image background
- Render a short video in MP4 format
- Schedule recurring daily jobs
- Run a local web dashboard
- Optional YouTube upload support

## Quick start

1. Install Ollama: https://ollama.com/
2. Pull a model:
   ```bash
   ollama pull llama3.2
   ```
3. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Start the app:
   ```bash
   python app.py
   ```
6. Open your browser at http://localhost:5000

## Optional YouTube upload
- Download your OAuth credentials as `client_secret.json`
- Place it in the repo root
- Login once through the app, or use the YouTube uploader helper
- Set `AUTO_UPLOAD_TO_YOUTUBE=true` in `.env`

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
