"""Cast (角色) management — folder-per-character.

Filesystem convention (one folder per character):

    projects/<id>/cast/<name>/             ← project-level (shared across episodes)
        cast.md                            ← soul card (front-matter + body)
        <anything>.{jpg,png,webp}          ← portraits (>=1 required)
        <anything>.{mp3,wav}               ← voice samples (optional)

    projects/<id>/<episode>/cast/<name>/   ← episode-level (NPCs unique to this episode)
        cast.md
        <portrait>.png

The folder *name* is the character's display name. Anything inside the folder
belongs to that character — no name-prefix matching needed.

If a character has more than one portrait inside its own folder, the CLI builds
a grid composite (``<id>.grid.png``) and feeds that as ``reference_image`` to
the active video provider. Both Wan and HappyHorse r2v accept multi-pane
reference images. Grids are NEVER built across different characters.

Two-tier discovery (per episode build):

  1. **Episode tier**  ``projects/<id>/<episode>/cast/`` — adds + overrides
  2. **Project tier**  ``projects/<id>/cast/``           — shared baseline

If the same character appears in both tiers, episode files are *prepended*
(so they are picked first as reference_image), and the episode soul card
overrides the project one.

Composites and ASCII-renamed singletons are written to
``projects/<id>/<episode>/cast_built/`` per episode (never mutating user input).
"""
from __future__ import annotations

import hashlib
import re
import shutil
import subprocess
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from PIL import Image
from rich.console import Console

from lib import soul as soul_mod, state
from lib.config import SETTINGS

class _UploadStub:
    @staticmethod
    def upload(*a, **kw):
        raise NotImplementedError(
            'lib.upload removed; bl auto-uploads. This path is unused by '
            'scripts/scaffold.py — call with do_upload=False.'
        )
up = _UploadStub()

console = Console()

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
AUDIO_EXTS = {".mp3", ".wav"}
SOUL_FILENAME = "cast.md"
VOICE_MAX_S = 10.0  # r2v reference_voice upper bound


@dataclass
class Character:
    name: str
    id: str = ""  # ASCII slug used for OSS paths; populated in init_episode
    images_local: list[str] = field(default_factory=list)
    audios_local: list[str] = field(default_factory=list)
    soul_local: str | None = None
    image_local: str | None = None  # final local file we upload (always ASCII basename)
    audio_local: str | None = None
    image_url: str | None = None
    audio_url: str | None = None
    soul: dict[str, Any] | None = None
    composite_image: bool = False
    composite_audio: bool = False
    source: str = "project"  # "project" | "episode"


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------

_SKIP_BASENAMES = {"readme.md", "readme", ".gitkeep", ".ds_store", "thumbs.db"}

_ID_OK = re.compile(r"^[a-z0-9][a-z0-9_-]{0,63}$")


def _is_ascii_safe(s: str) -> bool:
    """ASCII alnum + _ - only — safe as both filename and OSS path."""
    return bool(s) and all(c.isascii() and (c.isalnum() or c in "_-") for c in s)


def derive_id(name: str, *, soul_id: str | None = None) -> str:
    """Pick an ASCII slug for OSS paths.

    Priority:
      1. soul_id (validated against [a-z0-9_-]+)
      2. name itself if already ASCII-safe
      3. cast_<6-char-hash> (deterministic by name)
    """
    if soul_id:
        sid = soul_id.strip().lower()
        if _ID_OK.match(sid):
            return sid
        console.print(f"[yellow]soul id {soul_id!r} ignored: must match [a-z0-9_-]+[/]")
    if _is_ascii_safe(name):
        return name.lower()
    h = hashlib.sha256(name.encode("utf-8")).hexdigest()[:6]
    return f"cast_{h}"


def _scan_character_folder(char_dir: Path) -> tuple[list[Path], list[Path], Path | None]:
    """Walk one character folder; return (images, audios, soul_path).

    Files inside subdirectories are ignored — keep the layout flat.
    """
    images: list[Path] = []
    audios: list[Path] = []
    soul: Path | None = None
    for p in sorted(char_dir.iterdir()):
        if p.is_dir():
            continue
        if p.name.lower() in _SKIP_BASENAMES:
            continue
        ext = p.suffix.lower()
        if ext in IMAGE_EXTS:
            images.append(p)
        elif ext in AUDIO_EXTS:
            audios.append(p)
        elif p.name == SOUL_FILENAME:
            soul = p
    return images, audios, soul


def _scan_cast_root(root: Path, source: str) -> dict[str, dict[str, Any]]:
    """Return ``{character_name: {images, audios, soul, source}}`` for one tier.

    The character display name is the immediate subfolder name.
    """
    out: dict[str, dict[str, Any]] = {}
    if not root.exists() or not root.is_dir():
        return out
    for child in sorted(root.iterdir()):
        if not child.is_dir():
            continue
        if child.name.startswith(".") or child.name.lower() in _SKIP_BASENAMES:
            continue
        images, audios, soul = _scan_character_folder(child)
        if not images and not soul:
            console.print(
                f"[yellow]skip {source}/{child.name}: no portrait and no {SOUL_FILENAME}[/]"
            )
            continue
        out[child.name] = {
            "images": images,
            "audios": audios,
            "soul": soul,
            "source": source,
        }
    return out


def _merge(project_buckets: dict, episode_buckets: dict) -> dict[str, dict[str, Any]]:
    """Layered merge — episode overrides project, but never blends portraits
    across characters (grid building stays per-folder upstream).

    For a character present in both tiers:
      * episode images/audios are *prepended* (referenced first by the model).
      * episode soul card overrides project soul card if present.
      * source flips to ``episode``.
    """
    merged: dict[str, dict[str, Any]] = {}
    for name, b in project_buckets.items():
        merged[name] = {
            "images": list(b["images"]),
            "audios": list(b["audios"]),
            "soul": b["soul"],
            "source": "project",
        }
    for name, eb in episode_buckets.items():
        if name in merged:
            pb = merged[name]
            pb["images"] = list(eb["images"]) + pb["images"]
            pb["audios"] = list(eb["audios"]) + pb["audios"]
            if eb["soul"]:
                pb["soul"] = eb["soul"]
            pb["source"] = "episode"
        else:
            merged[name] = {
                "images": list(eb["images"]),
                "audios": list(eb["audios"]),
                "soul": eb["soul"],
                "source": "episode",
            }
    return merged


# ---------------------------------------------------------------------------
# Composites (built per character — never mixing characters)
# ---------------------------------------------------------------------------

def _build_grid(images: list[Path], out: Path, *, max_side: int = 1280) -> Path:
    """Compose N (>=2) portraits *of the same character* into a grid PNG."""
    if len(images) < 2:
        raise ValueError("_build_grid expects 2+ images of the same character.")
    out.parent.mkdir(parents=True, exist_ok=True)
    n = len(images)
    if n == 2:
        cols, rows = 2, 1
    elif n <= 4:
        cols, rows = 2, 2
    else:
        cols, rows = 3, 3
    cell_w = max_side // cols
    cell_h = max_side // rows

    canvas = Image.new("RGB", (cell_w * cols, cell_h * rows), color=(20, 20, 20))
    for i, p in enumerate(images[: cols * rows]):
        try:
            im = Image.open(p).convert("RGB")
        except Exception as e:
            console.print(f"[yellow]grid: skip {p.name} ({e})[/]")
            continue
        im.thumbnail((cell_w, cell_h), Image.LANCZOS)
        x = (i % cols) * cell_w + (cell_w - im.width) // 2
        y = (i // cols) * cell_h + (cell_h - im.height) // 2
        canvas.paste(im, (x, y))

    canvas.save(out, format="PNG", optimize=True)
    return out


def _audio_duration_s(path: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path),
    ]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(r.stdout.strip())
    except Exception:
        return 0.0


def _build_voice_mix(audios: list[Path], out: Path, *, max_s: float = VOICE_MAX_S) -> Path:
    """Concatenate 2+ audios *of the same character* via ffmpeg, trim to max_s."""
    if len(audios) < 2:
        raise ValueError("_build_voice_mix expects 2+ audios of the same character.")
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("ffmpeg not on PATH; install with `brew install ffmpeg`.")
    out.parent.mkdir(parents=True, exist_ok=True)

    listfile = out.with_suffix(".concat.txt")
    listfile.write_text(
        "\n".join(f"file '{a.resolve()}'" for a in audios), encoding="utf-8"
    )
    concat_mp3 = out.with_suffix(".concat.mp3")
    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(listfile), "-c:a", "libmp3lame", "-b:a", "192k",
        str(concat_mp3),
    ]
    subprocess.run(cmd, check=True, capture_output=True)

    cmd2 = [
        "ffmpeg", "-y", "-i", str(concat_mp3),
        "-t", f"{max_s}", "-c:a", "libmp3lame", "-b:a", "192k",
        str(out),
    ]
    subprocess.run(cmd2, check=True, capture_output=True)

    listfile.unlink(missing_ok=True)
    concat_mp3.unlink(missing_ok=True)
    return out


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def project_cast_dir(project_id: str) -> Path:
    return state.project_dir(project_id) / "cast"


def episode_cast_dir(project_id: str, episode_id: str) -> Path:
    return state.episode_dir(project_id, episode_id) / "cast"


def discover(project_id: str, episode_id: str) -> list[Character]:
    """Layered discovery — episode tier overrides project tier."""
    proj_buckets = _scan_cast_root(project_cast_dir(project_id), "project")
    ep_buckets = _scan_cast_root(episode_cast_dir(project_id, episode_id), "episode")
    merged = _merge(proj_buckets, ep_buckets)

    chars: list[Character] = []
    for name, b in sorted(merged.items()):
        images: list[Path] = b.get("images", []) or []
        audios: list[Path] = b.get("audios", []) or []
        if not images:
            console.print(f"[yellow]skip {name}: no portrait[/]")
            continue

        soul_path: Path | None = b.get("soul")
        soul_dict: dict | None = None
        if soul_path:
            try:
                soul_dict = soul_mod.parse(soul_path).to_dict()
            except Exception as e:
                console.print(f"[red]soul parse failed for {name}: {e}[/]")

        chars.append(
            Character(
                name=name,
                images_local=[str(p) for p in images],
                audios_local=[str(p) for p in audios],
                soul_local=str(soul_path) if soul_path else None,
                soul=soul_dict,
                source=b.get("source", "project"),
            )
        )
    return chars


def _ensure_ascii_basename(src: Path, build_dir: Path, *, cid: str) -> Path:
    """Copy non-ASCII basename src to build_dir/<cid>.<ext>; otherwise pass through."""
    if _is_ascii_safe(src.stem) and _is_ascii_safe(src.suffix.lstrip(".")):
        return src
    dst = build_dir / f"{cid}{src.suffix.lower()}"
    if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
        return dst
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    return dst


def init_episode(
    project_id: str,
    episode_id: str,
    *,
    do_upload: bool = False,
) -> dict:
    """Build cast.json for one episode.

    Scans ``projects/<id>/cast/`` (shared) and
    ``projects/<id>/<episode>/cast/`` (episode-only), merges by character name,
    builds grids/voice mixes within each character folder, uploads to OSS,
    writes ``projects/<id>/<episode>/cast.json``.
    """
    chars = discover(project_id, episode_id)
    if not chars:
        proj = project_cast_dir(project_id)
        ep = episode_cast_dir(project_id, episode_id)
        raise RuntimeError(
            f"no characters found in {proj} or {ep}. "
            f"Drop a character folder (with cast.md + a portrait) into either."
        )

    build_dir = state.episode_dir(project_id, episode_id) / "cast_built"
    build_dir.mkdir(parents=True, exist_ok=True)

    seen_ids: dict[str, str] = {}
    for c in chars:
        # ---------- derive ASCII id ---------------------------------------
        soul_id = (c.soul or {}).get("front", {}).get("id") if c.soul else None
        c.id = derive_id(c.name, soul_id=soul_id)
        if c.id in seen_ids and seen_ids[c.id] != c.name:
            extra = hashlib.sha256(c.name.encode("utf-8")).hexdigest()[6:10]
            c.id = f"{c.id}_{extra}"
        seen_ids[c.id] = c.name

        # ---------- portraits → 1 file (only same-character images merged) -
        if len(c.images_local) == 1:
            src = Path(c.images_local[0])
            c.image_local = str(_ensure_ascii_basename(src, build_dir, cid=c.id))
        else:
            grid = build_dir / f"{c.id}.grid.png"
            _build_grid([Path(p) for p in c.images_local], grid)
            c.image_local = str(grid)
            c.composite_image = True
            console.print(f"[cyan]· {c.name} ({c.id}): composed {len(c.images_local)}-pane grid[/]")

        # ---------- audios → 1 file ---------------------------------------
        if not c.audios_local:
            c.audio_local = None
        elif len(c.audios_local) == 1:
            src = Path(c.audios_local[0])
            dur = _audio_duration_s(src)
            if dur > VOICE_MAX_S:
                trimmed = build_dir / f"{c.id}.trimmed.mp3"
                cmd = [
                    "ffmpeg", "-y", "-i", str(src),
                    "-t", f"{VOICE_MAX_S}", "-c:a", "libmp3lame", "-b:a", "192k",
                    str(trimmed),
                ]
                subprocess.run(cmd, check=True, capture_output=True)
                c.audio_local = str(trimmed)
                console.print(f"[cyan]· {c.name} ({c.id}): trimmed voice from {dur:.1f}s to {VOICE_MAX_S}s[/]")
            else:
                c.audio_local = str(_ensure_ascii_basename(src, build_dir, cid=c.id))
        else:
            mix = build_dir / f"{c.id}.mix.mp3"
            _build_voice_mix([Path(p) for p in c.audios_local], mix)
            c.audio_local = str(mix)
            c.composite_audio = True
            console.print(f"[cyan]· {c.name} ({c.id}): mixed {len(c.audios_local)} voice samples[/]")

        # ---------- upload ------------------------------------------------
        if do_upload:
            console.print(f"[cyan]uploading {c.name} ({c.id}) image…[/]")
            c.image_url = up.upload(c.image_local)
            if c.audio_local:
                console.print(f"[cyan]uploading {c.name} ({c.id}) voice…[/]")
                c.audio_url = up.upload(c.audio_local)

    payload = {
        "project_id": project_id,
        "episode_id": state.normalize_episode_id(episode_id),
        "project_cast_dir": str(project_cast_dir(project_id).resolve()),
        "episode_cast_dir": str(episode_cast_dir(project_id, episode_id).resolve()),
        "characters": [asdict(c) for c in chars],
    }
    state.write_json(project_id, "cast.json", payload, episode_id=episode_id)
    state.merge_state(project_id, {
        "cast_count": len(chars),
        "cast_uploaded": do_upload,
        "cast_with_soul": sum(1 for c in chars if c.soul),
        "cast_episode_only": sum(1 for c in chars if c.source == "episode"),
    }, episode_id=episode_id)
    return payload


def load(project_id: str, episode_id: str) -> dict:
    data = state.read_json(project_id, "cast.json", episode_id=episode_id)
    if not data:
        raise FileNotFoundError(
            f"cast.json missing for {project_id}/{state.normalize_episode_id(episode_id)}. "
            f"Run:\n    SPARK_VIDEO_PROJECT={project_id} SPARK_VIDEO_EPISODE={episode_id} "
            f"uv run scripts/scaffold.py cast-init"
        )
    return data
