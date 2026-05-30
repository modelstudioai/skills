"""Append-only JSONL log of every model call made during a render.

Each line in ``projects/<id>/<episode>/logs/model_calls.jsonl`` is a
self-contained JSON record describing one HTTP call to an upstream model
endpoint (DashScope video, qwen-vl review, qwen-text rewrite, wan t2i
portrait, …). The record captures the request body, a summary of the
response, the timing, and the shot context active when the call happened
— giving us a complete audit trail for "what did we ask the model on
this episode, and what did it answer?".

Project-level calls (e.g. NPC portraits generated outside any episode)
are logged to ``projects/<id>/logs/model_calls.jsonl`` instead.

## Context propagation

Code paths thread through several modules (provider.submit → review →
rewrite → t2i) and the original ``project_id``/``episode_id``/
``shot_id`` aren't always in scope at the leaf. We use
``contextvars.ContextVar`` so each call site can ``log_call(...)`` with
no parameter plumbing — and so ``ThreadPoolExecutor`` (which copies the
context per task) automatically scopes log records to the right shot
when chain groups render in parallel.

## Schema (per JSONL line)

    {
      "ts":            ISO 8601 with timezone, ms precision,
      "kind":          "video_submit" | "video_wait" |
                       "review" | "rewrite" | "t2i_sync" | "t2i_async",
      "project_id":    str,
      "episode_id":    str | null,
      "shot_id":       str | null,
      "version":       int | null,
      "provider":      str | null,    # e.g. "happyhorse", "wan"
      "model":         str | null,
      "endpoint":      str | null,    # full URL
      "task_id":       str | null,
      "duration_ms":   float | null,
      "request":       dict | null,   # full body (Authorization header is never logged)
      "response":      dict | null,   # full body, large fields truncated
      "error":         str | null,
      "extra":         dict | null,   # caller-defined extras (retry round, etc.)
    }

The logger is best-effort: if the context is missing or the disk is
read-only, ``log_call`` swallows the error and returns. We never want
audit logging to break a render.
"""
from __future__ import annotations

import contextvars
import datetime as _dt
import json
import threading
from pathlib import Path
from typing import Any

from lib.config import SETTINGS

# ---------- context ----------------------------------------------------------

_CTX: contextvars.ContextVar[dict[str, Any] | None] = contextvars.ContextVar(
    "videogen_model_log_ctx", default=None,
)

# Single global lock — JSONL append is the bottleneck and per-shot files
# would fragment the audit trail.
_LOCK = threading.Lock()

# Cap on string length anywhere inside request/response bodies. Wan video URLs
# and qwen-vl base64 frames can balloon log size otherwise.
_MAX_STR_LEN = 8000


def set_context(
    *,
    project_id: str | None = None,
    episode_id: str | None = None,
    shot_id: str | None = None,
    version: int | None = None,
) -> contextvars.Token:
    """Bind one or more fields onto the current logging context.

    Returns the contextvars Token; pass it to ``reset_context`` when done.
    Fields not provided keep their previous value, so nested ``set_context``
    calls (e.g. episode-level → per-shot) compose naturally.
    """
    cur = dict(_CTX.get() or {})
    if project_id is not None:
        cur["project_id"] = project_id
    if episode_id is not None:
        cur["episode_id"] = episode_id
    if shot_id is not None:
        cur["shot_id"] = shot_id
    if version is not None:
        cur["version"] = version
    return _CTX.set(cur)


def reset_context(token: contextvars.Token) -> None:
    try:
        _CTX.reset(token)
    except (ValueError, LookupError):
        # Token came from a different context (e.g. ThreadPoolExecutor copied
        # the parent context, child bound new vars, child finishes). Best-effort.
        pass


def get_context() -> dict[str, Any]:
    return dict(_CTX.get() or {})


# ---------- redaction & truncation ------------------------------------------


_REDACT_KEYS = {"authorization", "api_key", "apikey", "x-api-key"}


def _redact_and_truncate(obj: Any, *, depth: int = 0) -> Any:
    """Return a copy of ``obj`` with sensitive keys redacted and long strings cut."""
    if depth > 8:
        return "<truncated:depth>"
    if isinstance(obj, dict):
        out: dict[str, Any] = {}
        for k, v in obj.items():
            if isinstance(k, str) and k.lower() in _REDACT_KEYS:
                out[k] = "<redacted>"
            else:
                out[k] = _redact_and_truncate(v, depth=depth + 1)
        return out
    if isinstance(obj, (list, tuple)):
        return [_redact_and_truncate(v, depth=depth + 1) for v in obj]
    if isinstance(obj, str) and len(obj) > _MAX_STR_LEN:
        return obj[:_MAX_STR_LEN] + f"…<+{len(obj) - _MAX_STR_LEN} chars>"
    return obj


# ---------- output paths -----------------------------------------------------


def _log_path_for(project_id: str, episode_id: str | None) -> Path:
    """Resolve the JSONL path; episode-level if episode given, else project-level."""
    base = SETTINGS.projects_dir / project_id
    if episode_id:
        # Mirror state.normalize_episode_id without importing state (avoid cycles).
        ep = episode_id.strip()
        if ep and not (ep.startswith("episode-") or ep.startswith("episode_")):
            if ep.replace("_", "").isalnum():
                ep = f"episode-{ep}"
        base = base / ep
    return base / "logs" / "model_calls.jsonl"


# ---------- public API -------------------------------------------------------


def log_call(
    *,
    kind: str,
    provider: str | None = None,
    model: str | None = None,
    endpoint: str | None = None,
    request: Any = None,
    response: Any = None,
    task_id: str | None = None,
    duration_ms: float | None = None,
    error: str | None = None,
    extra: dict | None = None,
) -> None:
    """Append one record to the current episode's model_calls.jsonl.

    Best-effort: silently no-ops if no project context is bound, or if
    writing to disk fails. Callers must never rely on log_call raising.
    """
    try:
        ctx = get_context()
        project_id = ctx.get("project_id")
        if not project_id:
            return
        episode_id = ctx.get("episode_id")

        record = {
            "ts": _dt.datetime.now().astimezone().isoformat(timespec="milliseconds"),
            "kind": kind,
            "project_id": project_id,
            "episode_id": episode_id,
            "shot_id": ctx.get("shot_id"),
            "version": ctx.get("version"),
            "provider": provider,
            "model": model,
            "endpoint": endpoint,
            "task_id": task_id,
            "duration_ms": round(duration_ms, 2) if duration_ms is not None else None,
            "request": _redact_and_truncate(request) if request is not None else None,
            "response": _redact_and_truncate(response) if response is not None else None,
            "error": error,
            "extra": _redact_and_truncate(extra) if extra else None,
        }

        path = _log_path_for(project_id, episode_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps(record, ensure_ascii=False, default=str)
        with _LOCK:
            with path.open("a", encoding="utf-8") as f:
                f.write(line + "\n")
    except Exception:
        # Never let logging break the render.
        return
