import os
import re
from typing import List

from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import AudioFileClip, CompositeVideoClip, ImageClip, TextClip

from config import AUDIOS_DIR, IMAGES_DIR, VIDEOS_DIR


class VideoProcessor:
    def create_short_video(self, topic: str, title: str, script: str) -> str:
        safe_name = self.slugify(title or topic)
        audio_path = os.path.join(AUDIOS_DIR, f"{safe_name}.mp3")
        image_path = self.create_background_image(topic, safe_name)

        speech = gTTS(text=script, lang="en", slow=False)
        speech.save(audio_path)

        audio = AudioFileClip(audio_path)
        duration = max(20, min(35, int(round(audio.duration))))

        image = ImageClip(image_path, duration=duration)
        image = image.resize(height=1920)
        image = image.resize(width=1080)

        captions = self.build_captions(script)
        subtitle_clips = []
        start_time = 0.0
        segment_duration = max(2.5, duration / max(len(captions), 1))

        for caption in captions:
            text_clip = TextClip(
                caption.upper(),
                fontsize=52,
                color="white",
                stroke_color="black",
                stroke_width=4,
                method="caption",
                align="center",
                font="DejaVu-Sans-Bold",
                size=(900, None),
            )
            text_clip = text_clip.set_position(("center", "bottom")).set_duration(segment_duration)
            text_clip = text_clip.set_start(start_time)
            subtitle_clips.append(text_clip)
            start_time += segment_duration

        final_video = CompositeVideoClip([image] + subtitle_clips, size=(1080, 1920))
        final_video = final_video.set_audio(audio)

        output_path = os.path.join(VIDEOS_DIR, f"{safe_name}.mp4")
        final_video.write_videofile(
            output_path,
            fps=30,
            codec="libx264",
            audio_codec="aac",
            threads=4,
            preset="veryfast",
            logger=None,
        )

        return output_path

    def create_background_image(self, topic: str, safe_name: str) -> str:
        image_path = os.path.join(IMAGES_DIR, f"{safe_name}.png")
        width, height = 1080, 1920
        img = Image.new("RGB", (width, height), color=(12, 14, 20))
        draw = ImageDraw.Draw(img)

        for y in range(0, height, 60):
            fill = (10 + (y // 60) % 30, 20 + (y // 50) % 30, 48)
            draw.rectangle([0, y, width, y + 60], fill=fill)

        draw.ellipse((120, 160, 980, 900), fill=(255, 120, 75))
        draw.ellipse((600, 980, 1020, 1360), fill=(80, 160, 255))

        try:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", 84)
            small_font = ImageFont.truetype("DejaVuSans.ttf", 42)
        except Exception:
            font = ImageFont.load_default()
            small_font = ImageFont.load_default()

        wrapped = self.wrap_text(topic, 14)
        y_pos = 170
        for line in wrapped[:3]:
            draw.text((100, y_pos), line.upper(), fill=(255, 255, 255), font=font)
            y_pos += 110

        draw.text((100, 1520), "AI SHORTS", fill=(255, 255, 255), font=small_font)
        img.save(image_path)
        return image_path

    def wrap_text(self, text: str, max_chars: int) -> List[str]:
        words = text.split()
        lines = []
        current = ""
        for word in words:
            if len(current) + len(word) + 1 <= max_chars:
                current = f"{current} {word}".strip()
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    def build_captions(self, script: str) -> List[str]:
        sentences = re.split(r"(?<=[.!?])\s+", script.strip())
        captions = [s.strip() for s in sentences if s.strip()]
        if not captions:
            captions = [script.strip()]
        return captions[:5]

    def slugify(self, text: str) -> str:
        text = (text or "ai-short").lower()
        text = re.sub(r"[^a-z0-9]+", "-", text)
        text = re.sub(r"-+", "-", text).strip("-")
        return text or "ai-short"
