# /// script
# requires-python = ">=3.10"
# dependencies = ["requests>=2.31"]
# ///
"""
DashScope wan2.7 provider — fallback when bl doesn't cover the feature.

Use this provider when you need:
- wan2.7-t2v-2026-04-25 / wan2.7-i2v-2026-04-25 / wan2.7-r2v
- precise first_frame chain bridging (last-frame of prev shot)
- negative_prompt support
- prompt_extend

For everything else, use scripts/providers/bl.py.

Public API:
    render(kind, prompt, media, voice, duration, out_path, extra) -> dict
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path
from typing import Literal

import requests

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent.parent))


DASHSCOPE_BASE = os.environ.get(
    "DASHSCOPE_BASE_URL",
    "https://dashscope.aliyuncs.com",
)
API_KEY = os.environ.get("DASHSCOPE_API_KEY") or os.environ.get("BAILIAN_API_KEY")

_MODEL_MAP = {
    "t2v": "wan2.7-t2v-2026-04-25",
    "i2v": "wan2.7-i2v-2026-04-25",
    "r2v": "wan2.7-r2v",
}


def _headers() -> dict[str, str]:
    if not API_KEY:
        raise RuntimeError(
            "DASHSCOPE_API_KEY (or BAILIAN_API_KEY) not set — wan27 provider needs it."
        )
    return {
        "Authorization": f"Bearer {API_KEY}",
        "X-DashScope-Async": "enable",
        "Content-Type": "application/json",
    }


def _upload(local_path: Path, model: str) -> str:
    """Upload a local file via `bl file upload` and return the OSS URL."""
    import subprocess
    repo_root = Path(__file__).resolve().parents[2]
    bl_wrapper = repo_root / "scripts" / "bl"
    proc = subprocess.run(
        [str(bl_wrapper), "--output", "json", "file", "upload",
         "--file", str(local_path), "--model", model],
        capture_output=True, text=True, timeout=180,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"file upload failed: {proc.stderr[-1000:]}")
    try:
        data = json.loads(proc.stdout)
        url = data.get("url") or data.get("file_url")
        if not url:
            raise ValueError(f"no url in upload response: {data}")
        return url
    except (json.JSONDecodeError, ValueError) as e:
        raise RuntimeError(f"can't parse upload response: {proc.stdout[:1000]}") from e


def _submit(model: str, body: dict) -> str:
    """Submit an async task, return task_id."""
    endpoint = f"{DASHSCOPE_BASE}/api/v1/services/aigc/video-generation/video-synthesis"
    resp = requests.post(endpoint, headers=_headers(), json={
        "model": model,
        "input": body.get("input", {}),
        "parameters": body.get("parameters", {}),
    }, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    task_id = data.get("output", {}).get("task_id")
    if not task_id:
        raise RuntimeError(f"submit returned no task_id: {data}")
    return task_id


def _wait(task_id: str, timeout_s: int = 900) -> str:
    """Poll task until SUCCEEDED, return video_url."""
    endpoint = f"{DASHSCOPE_BASE}/api/v1/tasks/{task_id}"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    deadline = time.time() + timeout_s
    poll = 5
    while time.time() < deadline:
        resp = requests.get(endpoint, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        status = data.get("output", {}).get("task_status")
        if status == "SUCCEEDED":
            return data["output"]["video_url"]
        if status in ("FAILED", "CANCELED", "UNKNOWN"):
            raise RuntimeError(f"task {task_id} {status}: {data}")
        time.sleep(poll)
        poll = min(poll + 2, 15)
    raise RuntimeError(f"task {task_id} timed out after {timeout_s}s")


def _download(url: str, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True, timeout=300) as r:
        r.raise_for_status()
        with open(out_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=64 * 1024):
                f.write(chunk)


def render(
    *,
    kind: Literal["t2v", "i2v", "r2v"],
    prompt: str,
    media: list[Path] | None = None,
    voice: Path | None = None,
    duration: int,
    out_path: Path,
    extra: dict | None = None,
) -> dict:
    media = media or []
    extra = extra or {}
    out_path = Path(out_path)

    model = extra.get("model") or _MODEL_MAP.get(kind)
    if not model:
        raise ValueError(f"unknown kind: {kind}")
    duration = max(2, min(15, int(duration)))

    # Upload local media → OSS URLs
    media_urls = [_upload(Path(m), model) for m in media]
    voice_url = _upload(voice, model) if voice else None

    parameters = {"duration": duration}
    if "resolution" in extra:
        parameters["resolution"] = extra["resolution"]
    if "ratio" in extra:
        parameters["ratio"] = extra["ratio"]
    if "seed" in extra and extra["seed"] is not None:
        parameters["seed"] = int(extra["seed"])
    if extra.get("negative_prompt"):
        parameters["negative_prompt"] = extra["negative_prompt"]
    if extra.get("prompt_extend") is not None:
        parameters["prompt_extend"] = bool(extra["prompt_extend"])

    input_block: dict = {"prompt": prompt}
    if kind == "i2v":
        if not media_urls:
            raise ValueError("i2v requires media[0] = first frame")
        input_block["img_url"] = media_urls[0]
        # wan2.7 also supports first_frame for chain bridging
        if extra.get("first_frame_url"):
            input_block["img_url"] = extra["first_frame_url"]
    elif kind == "r2v":
        input_block["ref_images"] = media_urls
        if voice_url:
            input_block["reference_voice"] = voice_url
        if extra.get("first_frame_url"):
            input_block["first_frame"] = extra["first_frame_url"]

    body = {"input": input_block, "parameters": parameters}

    started = time.time()
    task_id = _submit(model, body)
    timeout_s = int(os.environ.get("SPARK_VIDEO_RENDER_TIMEOUT_S", "900"))
    video_url = _wait(task_id, timeout_s=timeout_s)
    _download(video_url, out_path)
    elapsed = time.time() - started

    return {
        "video_path": str(out_path),
        "model": model,
        "elapsed_s": round(elapsed, 2),
        "task_id": task_id,
    }
