# ai-youtube-shorts-automation

A simple starter project for generating AI-powered YouTube Shorts scripts and a local preview video from a topic.

This repo intentionally keeps the workflow lightweight and free-to-start:
- OpenAI API is optional for script generation
- local rendering uses Pillow so no heavy video pipeline is required up front
- YouTube upload logic is scaffolded but left explicit and safe by default

## What this prototype does

- accepts a topic/keyword
- generates a short-form script (or a fallback script if no API key is configured)
- renders a simple text-on-video preview into `output/`
- provides a clean CLI for iteration and extension

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py --help
```

## Generate a short

```bash
export OPENAI_API_KEY="your_key_here"
python app.py generate --topic "AI productivity mistakes" --output-dir output
```

If no API key is set, the app falls back to a built-in script template so you can still test the workflow locally.

## Files

- `app.py` - CLI entry point
- `shorts_automation/generator.py` - OpenAI-powered or fallback script generation
- `shorts_automation/renderer.py` - local preview rendering
- `shorts_automation/uploader.py` - YouTube upload scaffolding
- `shorts_automation/cli.py` - command parsing and orchestration

## Notes

This is intentionally a starter implementation. The YouTube upload flow is not enabled automatically and still requires proper OAuth credentials and app setup from Google.
