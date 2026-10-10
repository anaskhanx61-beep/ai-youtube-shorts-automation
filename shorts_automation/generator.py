import os
import re
from typing import List

try:
    from openai import OpenAI
except Exception:  # pragma: no cover
    OpenAI = None


def split_script(script: str) -> List[str]:
    if not script:
        return []
    sections = re.split(r"\n+|(?<=[.!?])\s+", script.strip())
    cleaned = [part.strip() for part in sections if part and part.strip()]
    return cleaned[:5]


def _fallback_script(topic: str, tone: str = "educational", audience: str = "beginners") -> str:
    topic_text = topic.strip() or "AI productivity"
    return (
        f"Here’s the big idea: {topic_text} can change your results fast. "
        f"Most people overthink it. The real win is simple action. "
        f"Start with one clear step, keep it consistent, and build momentum. "
        f"If you’re trying to get better at {topic_text}, focus on the boring basics first. "
        f"That’s where the real growth happens. "
        f"Follow for more practical tips for {audience} creators."
    )


def generate_script(topic: str, tone: str = "educational", audience: str = "beginners") -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and OpenAI is not None:
        client = OpenAI(api_key=api_key)
        prompt = (
            f"Write a short YouTube Shorts script about: {topic}. "
            f"Tone: {tone}. Audience: {audience}. "
            "Requirements: 20 to 35 seconds long, hook in first sentence, clear pacing, simple language, strong CTA. "
            "Only return the script text, no markdown."
        )
        try:
            response = client.responses.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                input=prompt,
            )
            result = getattr(response, "output_text", None)
            if not result and hasattr(response, "choices") and response.choices:
                result = response.choices[0].message.content
            if result and result.strip():
                return result.strip()
        except Exception:
            pass

    return _fallback_script(topic, tone=tone, audience=audience)


__all__ = ["generate_script", "split_script"]
