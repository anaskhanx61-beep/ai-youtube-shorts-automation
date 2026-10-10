import os
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, jsonify, render_template, request

from config import APP_PORT, DEFAULT_TOPIC
from services.script_generator import ScriptGenerator
from services.video_processor import VideoProcessor
from services.youtube_uploader import YouTubeUploader

app = Flask(__name__)

script_generator = ScriptGenerator()
video_processor = VideoProcessor()
youtube_uploader = YouTubeUploader()
scheduler = BackgroundScheduler()


def generate_video_for_topic(topic: str, upload_to_youtube: bool = False):
    script_data = script_generator.generate_script(topic)
    video_path = video_processor.create_short_video(
        topic=topic,
        title=script_data["title"],
        script=script_data["script"],
    )

    result = {
        "title": script_data["title"],
        "script": script_data["script"],
        "video_path": video_path,
        "status": "created",
    }

    if upload_to_youtube:
        try:
            result["youtube_upload"] = youtube_uploader.upload_video(
                video_path,
                script_data["title"],
                script_data["script"],
            )
        except Exception as exc:
            result["youtube_upload"] = {"status": "failed", "error": str(exc)}

    return result


@app.route("/")
def index():
    return render_template("index.html", default_topic=DEFAULT_TOPIC)


@app.route("/api/generate", methods=["POST"])
def generate_endpoint():
    payload = request.get_json(silent=True) or {}
    topic = (payload.get("topic") or DEFAULT_TOPIC).strip()
    upload_to_youtube = bool(payload.get("upload_to_youtube", False))

    if not topic:
        return jsonify({"error": "Topic is required."}), 400

    result = generate_video_for_topic(topic, upload_to_youtube=upload_to_youtube)
    return jsonify(result)


@app.route("/api/schedule", methods=["POST"])
def schedule_endpoint():
    payload = request.get_json(silent=True) or {}
    topic = (payload.get("topic") or DEFAULT_TOPIC).strip()
    hour = int(payload.get("hour", 9))
    minute = int(payload.get("minute", 0))
    upload_to_youtube = bool(payload.get("upload_to_youtube", False))

    if not topic:
        return jsonify({"error": "Topic is required."}), 400

    for job in scheduler.get_jobs():
        if job.id == "daily_short_job":
            scheduler.remove_job(job.id)

    scheduler.add_job(
        func=generate_video_for_topic,
        trigger="cron",
        hour=hour,
        minute=minute,
        args=[topic],
        kwargs={"upload_to_youtube": upload_to_youtube},
        id="daily_short_job",
        replace_existing=True,
    )

    return jsonify({
        "status": "scheduled",
        "topic": topic,
        "time": f"{hour:02d}:{minute:02d}",
        "upload_to_youtube": upload_to_youtube,
    })


@app.route("/api/jobs")
def jobs_endpoint():
    jobs = []
    for job in scheduler.get_jobs():
        jobs.append({
            "id": job.id,
            "next_run_time": job.next_run_time.isoformat() if job.next_run_time else None,
            "trigger": str(job.trigger),
        })
    return jsonify({"jobs": jobs})


@app.route("/health")
def health():
    return jsonify({"status": "ok", "timestamp": datetime.utcnow().isoformat()})


if __name__ == "__main__":
    if not scheduler.running:
        scheduler.start()
    app.run(host="0.0.0.0", port=APP_PORT, debug=False)
