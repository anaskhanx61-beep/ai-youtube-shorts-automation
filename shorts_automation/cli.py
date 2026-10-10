import argparse
from pathlib import Path

from .config import get_settings
from .generator import generate_script
from .renderer import render_preview


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a YouTube Shorts script and preview image.")
    parser.add_argument("--topic", default=None, help="Topic to write about")
    parser.add_argument("--tone", default="educational", help="Writing tone (educational, funny, dramatic, etc.)")
    parser.add_argument("--audience", default="beginners", help="Target audience")
    parser.add_argument("--output-dir", default=None, help="Directory for the generated preview")
    return parser


def main() -> None:
    settings = get_settings()
    parser = _build_parser()
    args = parser.parse_args()

    topic = args.topic or settings.default_topic
    output_dir = Path(args.output_dir) if args.output_dir else settings.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    script = generate_script(topic, tone=args.tone, audience=args.audience)
    preview_path = render_preview(script, output_dir, title=topic)

    print("Generated script:")
    print("-" * 60)
    print(script)
    print("-" * 60)
    print(f"Preview image saved to: {preview_path}")


if __name__ == "__main__":
    main()
