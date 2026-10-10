import re

from services.ollama_client import OllamaClient


class ScriptGenerator:
    def __init__(self, ollama_client=None):
        self.ollama_client = ollama_client or OllamaClient()

    def generate_script(self, topic: str, tone: str = "viral, punchy, engaging") -> dict:
        prompt = f"""
        Write a YouTube Shorts script for this topic: {topic}

        Requirements:
        - 20 to 35 seconds long
        - Start with a strong hook in the first 2 seconds
        - Clear, simple, and engaging voice-over
        - Include a call to action at the end
        - No markdown or bullets

        Tone: {tone}

        Format exactly:
        TITLE: <short catchy title>
        SCRIPT: <full spoken script>
        """

        ai_text = self.ollama_client.generate(prompt)

        if ai_text and "TITLE:" in ai_text and "SCRIPT:" in ai_text:
            title = ai_text.split("TITLE:", 1)[1].split("SCRIPT:", 1)[0].strip()
            script = ai_text.split("SCRIPT:", 1)[1].strip()
            if title and script:
                return {"title": title, "script": self.clean_script(script)}

        return {
            "title": self.make_title(topic),
            "script": self.fallback_script(topic),
        }

    def clean_script(self, script: str) -> str:
        script = script.replace("\r", " ")
        script = re.sub(r"\s+", " ", script).strip()
        return script

    def make_title(self, topic: str) -> str:
        title = (topic or "AI Shortcut").strip()
        return title[:55].rstrip() if len(title) > 55 else title

    def fallback_script(self, topic: str) -> str:
        return (
            f"Here is the truth: {topic} is easier than most people think. "
            f"If you start small, stay consistent, and take action early, results come faster than you expect. "
            f"Most people wait forever for the perfect moment. The secret is to start now, improve as you go, and keep moving. "
            f"If you want more ideas like this, follow for the next tip."
        )
