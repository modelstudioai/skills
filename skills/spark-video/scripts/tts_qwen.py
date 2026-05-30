# /// script
# requires-python = ">=3.10"
# dependencies = ["requests>=2.31"]
# ///
"""
tts_qwen.py — fallback TTS via DashScope qwen-tts (bl doesn't cover this).

Use only when SPARK_VIDEO_NARRATOR_TTS_MODEL is qwen-tts-flash / similar.
For the default cosyvoice path, the pipeline uses ./scripts/bl speech synthesize.

Output: a wav file at --out. Applies speech-rate via ffmpeg atempo post-process.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import requests

DASHSCOPE_BASE = os.environ.get(
    "DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com"
)
API_KEY = os.environ.get("DASHSCOPE_API_KEY") or os.environ.get("BAILIAN_API_KEY")


def synth(
    *, text: str, voice: str, model: str, language: str = "Auto",
    out_path: Path, speech_rate: float = 1.0,
) -> None:
    if not API_KEY:
        raise RuntimeError("DASHSCOPE_API_KEY not set")
    url = f"{DASHSCOPE_BASE}/api/v1/services/aigc/multimodal-generation/generation"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    body = {
        "model": model,
        "input": {"text": text, "voice": voice},
    }
    if language and language != "Auto":
        body["input"]["language"] = language
    resp = requests.post(url, headers=headers, json=body, timeout=120)
    resp.raise_for_status()
    data = resp.json()
    audio_url = (data.get("output", {}).get("audio") or {}).get("url")
    if not audio_url:
        raise RuntimeError(f"qwen-tts returned no audio url: {data}")

    # Download to temp, then atempo if needed
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    with requests.get(audio_url, stream=True, timeout=120) as r:
        r.raise_for_status()
        with open(tmp_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=64 * 1024):
                f.write(chunk)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    if abs(speech_rate - 1.0) < 0.01:
        # No tempo change
        tmp_path.replace(out_path)
        return

    # atempo accepts 0.5–2.0 per filter; chain if outside
    atempo_chain = _atempo_chain(speech_rate)
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(tmp_path),
         "-filter:a", atempo_chain, "-vn", str(out_path)],
        check=True, capture_output=True, timeout=60,
    )
    tmp_path.unlink(missing_ok=True)


def _atempo_chain(rate: float) -> str:
    """Build an atempo chain that supports rates outside [0.5, 2.0]."""
    parts = []
    remaining = rate
    while remaining < 0.5:
        parts.append("atempo=0.5")
        remaining /= 0.5
    while remaining > 2.0:
        parts.append("atempo=2.0")
        remaining /= 2.0
    parts.append(f"atempo={remaining:.3f}")
    return ",".join(parts)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--text", required=True)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--voice", default="Cherry")
    ap.add_argument("--model", default="qwen-tts-flash")
    ap.add_argument("--language", default="Auto")
    ap.add_argument("--rate", type=float, default=1.0)
    args = ap.parse_args()
    synth(text=args.text, voice=args.voice, model=args.model,
          language=args.language, out_path=args.out, speech_rate=args.rate)
    print(str(args.out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
