# /// script
# requires-python = ">=3.10"
# dependencies = ["pydantic>=2.5", "python-dotenv>=1.0"]
# ///
"""
build_viewer.py — emit a self-contained viewer.html for one episode.

Walks <project>/ and <episode>/ artifacts and renders a single HTML page
that shows premise, lore, direction, script, cast/sets/props, every shot
(with all clip versions + review scores, winner highlighted), and the
final stitched mp4. All media is referenced via relative paths — no
files are copied.

Run:
    SPARK_VIDEO_PROJECT=foo SPARK_VIDEO_EPISODE=001 \\
        uv run scripts/build_viewer.py [--no-open]

The page auto-opens on macOS unless --no-open is passed.
"""
from __future__ import annotations

import argparse
import html
import json
import os
import platform
import re
import subprocess
import sys
import urllib.parse
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from lib.state import episode_dir, project_dir, normalize_episode_id  # noqa: E402


IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}
AUDIO_EXTS = {".mp3", ".wav", ".m4a"}
VIDEO_EXTS = {".mp4", ".mov", ".webm"}


# ---------- helpers ---------------------------------------------------------


def _resolve_ids() -> tuple[str, str]:
    proj = os.environ.get("SPARK_VIDEO_PROJECT", "")
    ep = os.environ.get("SPARK_VIDEO_EPISODE", "")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--project", default=proj or None)
    ap.add_argument("--episode", default=ep or None)
    ap.add_argument("--no-open", action="store_true")
    args, _rest = ap.parse_known_args()
    if not args.project or not args.episode:
        print("ERROR: --project/--episode or SPARK_VIDEO_PROJECT/SPARK_VIDEO_EPISODE required",
              file=sys.stderr)
        sys.exit(2)
    return args.project, args.episode, args.no_open


def _rel(target: Path, base: Path) -> str:
    """Relative URL path from base file (not its dir) to target. URL-encoded."""
    try:
        rel = os.path.relpath(target, base)
    except ValueError:
        rel = str(target)
    return urllib.parse.quote(rel.replace(os.sep, "/"), safe="/")


def _read_text(p: Path) -> str | None:
    try:
        return p.read_text(encoding="utf-8")
    except Exception:
        return None


def _load_json(p: Path):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def _sorted_dir(p: Path) -> list[Path]:
    try:
        return sorted(p.iterdir(), key=lambda x: x.name)
    except FileNotFoundError:
        return []


def _strip_frontmatter(md: str) -> tuple[dict, str]:
    """Extract a simple YAML-ish front matter (--- key: value ---) prefix."""
    fm: dict = {}
    body = md
    if md.startswith("---"):
        end = md.find("\n---", 3)
        if end > 0:
            block = md[3:end].strip()
            body = md[end + 4:].lstrip("\n")
            for line in block.splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if ":" in line:
                    k, v = line.split(":", 1)
                    fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm, body


# ---------- collectors ------------------------------------------------------


def _collect_assets(root: Path, ep_dir: Path) -> dict[str, list[str]]:
    """Group asset URLs (relative to viewer.html) by type for one folder."""
    images, audios, videos, others = [], [], [], []
    for f in _sorted_dir(root):
        if not f.is_file():
            continue
        url = _rel(f, ep_dir)
        ext = f.suffix.lower()
        if ext in IMAGE_EXTS:
            images.append(url)
        elif ext in AUDIO_EXTS:
            audios.append(url)
        elif ext in VIDEO_EXTS:
            videos.append(url)
        elif f.name not in ("cast.md", "set.md", "prop.md"):
            others.append(url)
    return {"images": images, "audios": audios, "videos": videos, "others": others}


def _collect_entities(parent: Path, ep_dir: Path, md_name: str) -> list[dict]:
    """Walk <parent>/<name>/ folders and emit cast/set/prop entries."""
    out = []
    if not parent.exists():
        return out
    for d in _sorted_dir(parent):
        if not d.is_dir():
            continue
        md = _read_text(d / md_name) or ""
        fm, body = _strip_frontmatter(md)
        assets = _collect_assets(d, ep_dir)
        out.append({
            "name": d.name,
            "frontmatter": fm,
            "body": body,
            **assets,
        })
    return out


def _collect_scenes(ep_dir: Path) -> list[dict]:
    out = []
    scenes_dir = ep_dir / "scenes"
    if not scenes_dir.exists():
        return out
    md_files = sorted(scenes_dir.glob("scene-*.md"))
    for md in md_files:
        body = _read_text(md) or ""
        js = _load_json(scenes_dir / md.with_suffix(".json").name)
        out.append({"name": md.stem, "body": body, "json": js})
    return out


def _collect_shots(
    ep_dir: Path,
    storyboard: dict | None,
    sent_by_shot_ver: dict[str, str] | None = None,
) -> list[dict]:
    """For each shot in storyboard order, find all clip versions on disk."""
    state = _load_json(ep_dir / "shots_state.json") or {}
    clips_dir = ep_dir / "clips"
    frames_dir = ep_dir / "frames"
    reviews_dir = ep_dir / "reviews"
    sent_by_shot_ver = sent_by_shot_ver or {}

    shot_specs: list[dict] = []
    if storyboard:
        for sc in storyboard.get("scenes", []):
            for sh in sc.get("shots", []) if isinstance(sc.get("shots"), list) else []:
                shot_specs.append(sh)
        # Some storyboards keep shots at top level instead
        if not shot_specs and isinstance(storyboard.get("shots"), list):
            shot_specs = storyboard["shots"]

    # Fallback: derive from state keys if storyboard absent
    if not shot_specs:
        shot_specs = [{"id": sid} for sid in sorted(state.keys())]

    ver_re = re.compile(r"^(?P<id>.+)-ver(?P<n>\d+)\.mp4$")

    out = []
    for spec in shot_specs:
        sid = spec.get("id") or spec.get("shot_id")
        if not sid:
            continue
        entry = state.get(sid) or {}
        winner = entry.get("winner_version")

        # discover versions on disk (truth) — don't trust state paths
        versions = []
        if clips_dir.exists():
            for clip in sorted(clips_dir.glob(f"{sid}-ver*.mp4")):
                m = ver_re.match(clip.name)
                if not m:
                    continue
                n = int(m.group("n"))
                attempt = next(
                    (a for a in entry.get("attempts", []) if a.get("version") == n),
                    {},
                )
                review = attempt.get("review")
                if not review:
                    review = _load_json(reviews_dir / f"{sid}-ver{n}.json")
                thumb = frames_dir / f"{sid}-ver{n}_last.png"
                recorded_prompt = attempt.get("prompt")
                sent_prompt = sent_by_shot_ver.get(f"{sid}::{n}")
                versions.append({
                    "version": n,
                    "clip_url": _rel(clip, ep_dir),
                    "thumb_url": _rel(thumb, ep_dir) if thumb.exists() else None,
                    "prompt": recorded_prompt,
                    "sent_prompt": sent_prompt,
                    "review": review,
                    "status": attempt.get("status"),
                    "task_id": attempt.get("task_id"),
                })

        out.append({
            "id": sid,
            "scene": spec.get("scene"),
            "narrative_purpose": spec.get("narrative_purpose"),
            "duration": spec.get("duration"),
            "kind": spec.get("kind"),
            "characters": spec.get("characters", []),
            "prompt": spec.get("prompt"),
            "winner_version": winner,
            "versions": versions,
        })
    return out


def _extract_sent_prompt(rec: dict) -> str | None:
    """Recover the literal prompt that hit the model from one log record.

    Handles two logger schemas:
      * lib/model_log.py — ``request`` is a dict that contains ``input.prompt``
        (DashScope shape) or ``parameters.prompt`` on some endpoints.
      * scripts/bl wrapper — records have a ``cmd`` array; we grep it for
        the value following ``--prompt``.
    Returns None when no prompt is identifiable (e.g. wait / review calls).
    """
    req = rec.get("request")
    if isinstance(req, dict):
        inp = req.get("input")
        if isinstance(inp, dict) and isinstance(inp.get("prompt"), str):
            return inp["prompt"]
        params = req.get("parameters")
        if isinstance(params, dict) and isinstance(params.get("prompt"), str):
            return params["prompt"]
        if isinstance(req.get("prompt"), str):
            return req["prompt"]
    cmd = rec.get("cmd")
    if isinstance(cmd, list):
        for i, tok in enumerate(cmd):
            if tok == "--prompt" and i + 1 < len(cmd):
                return cmd[i + 1]
    return None


def _is_video_render_record(rec: dict) -> bool:
    """Best-effort: does this log record correspond to a video render submit?"""
    k = (rec.get("kind") or "").lower()
    if k in {"video_submit", "video_render", "video"}:
        return True
    cmd = rec.get("cmd")
    if isinstance(cmd, list) and len(cmd) >= 3 and cmd[0] == "bl" and cmd[1] == "video":
        return cmd[2] in {"generate", "ref", "edit"}
    return False


def _collect_calls(ep_dir: Path) -> dict:
    """Group model_calls.jsonl by shot; return summary + raw + sent-prompt index.

    Two logger schemas coexist in the repo (see lib/model_log.py docstring
    and scripts/bl). Field names differ:
      * Python logger: shot_id / version / duration_ms / kind
      * Shell wrapper: shot   / attempt / duration_ms / (no kind, infer from cmd)
    We accept both so the calls table populates per-shot in either case, and
    we also harvest the actual ``--prompt`` value sent to the video model so
    the shots section can show it as ground truth.
    """
    log = ep_dir / "logs" / "model_calls.jsonl"
    by_shot: dict = {}
    raw: list = []
    sent_by_shot_ver: dict[str, str] = {}
    total = 0
    if not log.exists():
        return {
            "by_shot": by_shot, "total": 0, "raw_count": 0,
            "raw": [], "sent_by_shot_ver": sent_by_shot_ver,
        }
    for line in log.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
        except Exception:
            continue
        total += 1
        raw.append(rec)
        sid = rec.get("shot_id") or rec.get("shot") or "_project_"
        slot = by_shot.setdefault(sid, {"count": 0, "duration_ms": 0.0, "kinds": {}})
        slot["count"] += 1
        d = rec.get("duration_ms") or 0
        try:
            slot["duration_ms"] += float(d)
        except (TypeError, ValueError):
            pass
        k = rec.get("kind")
        if not k:
            cmd = rec.get("cmd")
            if isinstance(cmd, list) and len(cmd) >= 3 and cmd[0] == "bl":
                k = f"bl_{cmd[1]}_{cmd[2]}"
            else:
                k = "?"
        slot["kinds"][k] = slot["kinds"].get(k, 0) + 1

        if _is_video_render_record(rec):
            prompt = _extract_sent_prompt(rec)
            if prompt:
                ver = rec.get("version") or rec.get("attempt")
                if ver is not None:
                    key = f"{sid}::{ver}"
                    # Keep the first occurrence per (shot, version). render_shot
                    # passes the prompt only once per attempt so collisions are
                    # rare and the first call is the truthful one.
                    sent_by_shot_ver.setdefault(key, prompt)
    return {
        "by_shot": by_shot, "total": total, "raw_count": len(raw),
        "raw": raw, "sent_by_shot_ver": sent_by_shot_ver,
    }


def _collect_final(ep_dir: Path, project: str, episode_norm: str) -> dict | None:
    final_dir = ep_dir / "final"
    if not final_dir.exists():
        return None
    # primary expected name
    cands = list(final_dir.glob("*.mp4"))
    if not cands:
        return None
    # prefer "<project>-<episode>.mp4"
    expected = f"{project}-{episode_norm}.mp4"
    chosen = next((c for c in cands if c.name == expected), cands[0])
    return {
        "name": chosen.name,
        "url": _rel(chosen, ep_dir),
        "size_bytes": chosen.stat().st_size,
    }


def _collect_bgm(proj_dir: Path, ep_dir: Path) -> list[dict]:
    bgm_dir = proj_dir / "bgm"
    out = []
    if not bgm_dir.exists():
        return out
    for f in _sorted_dir(bgm_dir):
        if f.suffix.lower() in AUDIO_EXTS:
            out.append({"name": f.name, "url": _rel(f, ep_dir)})
    return out


# ---------- HTML emission ---------------------------------------------------


_MARKED_JS = (_HERE.parent / "lib" / "vendor" / "marked.min.js").read_text(encoding="utf-8")


def _html(payload: dict) -> str:
    data_json = json.dumps(payload, ensure_ascii=False, default=str)
    # Defend the closing </script> sentinel inside JSON.
    data_json = data_json.replace("</", "<\\/")
    title = html.escape(f"{payload['project']} · {payload['episode']} · viewer")
    marked_js = _MARKED_JS.replace("</script>", "<\\/script>")

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8" />
<title>{title}</title>
<script>{marked_js}</script>
<style>
:root {{
  --bg:#0e1116; --panel:#161b22; --panel2:#1e242d; --border:#2a313c;
  --fg:#e6edf3; --mute:#8b949e; --accent:#58a6ff; --gold:#f0b429;
  --good:#3fb950; --bad:#f85149;
  --code:#1f262f;
}}
* {{ box-sizing: border-box; }}
html, body {{ margin:0; padding:0; background:var(--bg); color:var(--fg);
  font: 14px/1.55 -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC",
        "Microsoft YaHei", Helvetica, Arial, sans-serif; }}
a {{ color: var(--accent); }}
.layout {{ display: grid; grid-template-columns: 220px 1fr; min-height: 100vh; }}
nav {{ position: sticky; top:0; height:100vh; overflow:auto; padding:18px 14px;
  background:var(--panel); border-right:1px solid var(--border); }}
nav h1 {{ font-size:13px; color:var(--mute); margin:0 0 12px; font-weight:600; letter-spacing:.5px; text-transform:uppercase; }}
nav .meta {{ font-size:12px; color:var(--mute); margin-bottom:16px; }}
nav .meta b {{ color: var(--fg); }}
nav ul {{ list-style:none; padding:0; margin:0; }}
nav li a {{ display:block; padding:6px 10px; border-radius:6px; color:var(--fg);
  text-decoration:none; font-size:13px; }}
nav li a:hover {{ background:var(--panel2); }}
main {{ padding:32px 48px; max-width: 1200px; }}
section {{ margin-bottom: 48px; scroll-margin-top: 20px; }}
section h2 {{ font-size:20px; margin:0 0 16px; padding-bottom:8px; border-bottom:1px solid var(--border); }}
section h3 {{ font-size:15px; margin:24px 0 8px; color:var(--mute); }}
.card {{ background:var(--panel); border:1px solid var(--border); border-radius:8px; padding:16px; margin-bottom:16px; }}
.md {{ background:var(--panel); border:1px solid var(--border); border-radius:8px; padding:16px 20px; }}
.md h1,.md h2,.md h3 {{ color:var(--fg); border:none; margin-top:18px; }}
.md p {{ margin: .6em 0; }}
.md code {{ background:var(--code); padding:1px 4px; border-radius:3px; font-size:12.5px; }}
.md pre {{ background:var(--code); padding:12px; border-radius:6px; overflow:auto; }}
.md blockquote {{ border-left:3px solid var(--accent); margin:0; padding:.2em 1em; color:var(--mute); }}
details {{ background:var(--panel); border:1px solid var(--border); border-radius:6px; padding:8px 12px; margin: 6px 0; }}
details > summary {{ cursor:pointer; color:var(--mute); font-size:13px; user-select:none; }}
details[open] > summary {{ color: var(--fg); margin-bottom: 8px; }}
.grid {{ display:grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap:14px; }}
.entity {{ background:var(--panel); border:1px solid var(--border); border-radius:8px; padding:12px; }}
.entity img {{ width:100%; height:180px; object-fit:cover; border-radius:6px; background:var(--bg); }}
.entity h4 {{ margin: 10px 0 4px; font-size: 15px; }}
.entity audio {{ width:100%; margin-top:6px; }}
.entity .fm {{ font-size:12px; color:var(--mute); }}
.entity .fm span {{ display:inline-block; margin-right:8px; }}
.shot {{ background:var(--panel); border:1px solid var(--border); border-radius:10px; padding:16px; margin-bottom:18px; }}
.shot-head {{ display:flex; flex-wrap:wrap; align-items:baseline; gap:10px; margin-bottom:10px; }}
.shot-head .id {{ font-weight:600; font-size:15px; }}
.shot-head .pill {{ background:var(--panel2); color:var(--mute); font-size:11px; padding:2px 8px; border-radius: 20px; }}
.shot-head .purpose {{ color:var(--mute); font-size:13px; flex:1; min-width:200px; }}
.tabs {{ display:flex; gap:6px; margin: 10px 0 12px; flex-wrap:wrap; }}
.tab {{ background:var(--panel2); color:var(--fg); border:1px solid var(--border);
  padding:5px 12px; border-radius: 6px; cursor:pointer; font-size:13px; }}
.tab.active {{ background:var(--accent); color:#fff; border-color:transparent; }}
.tab.winner::after {{ content: " ★"; color: var(--gold); }}
.tab.active.winner::after {{ color: #fff; }}
.version-body {{ gap: 14px; align-items: start; }}
.version-body video {{ width:100%; max-height: 420px; background:#000; border-radius:6px; }}
.review {{ font-size: 13px; }}
.review .score {{ font-size: 22px; font-weight: 600; }}
.review .verdict {{ display:inline-block; padding:1px 8px; border-radius:4px; font-size:11px;
  margin-left:8px; vertical-align: middle; }}
.review .verdict.ACCEPT {{ background:var(--good); color:#fff; }}
.review .verdict.REJECT {{ background:var(--bad); color:#fff; }}
.review .verdict.UNKNOWN {{ background:var(--mute); color:#fff; }}
.review table {{ width:100%; border-collapse:collapse; margin: 8px 0; }}
.review td {{ padding: 3px 6px; border-bottom: 1px solid var(--border); font-size: 12.5px; }}
.review td:last-child {{ text-align:right; color:var(--accent); font-variant-numeric: tabular-nums; }}
.review .critique {{ color: var(--mute); white-space: pre-wrap; font-size: 12.5px; margin-top: 8px; }}
.thumb {{ width:100%; border-radius:4px; margin-top:8px; }}
.calls table {{ width:100%; border-collapse:collapse; }}
.calls th, .calls td {{ padding:6px 10px; border-bottom:1px solid var(--border); text-align:left; font-size:13px; }}
.calls th {{ color: var(--mute); font-weight:500; }}
.calls tr.row:hover {{ background: var(--panel2); cursor:pointer; }}
.modal {{ position:fixed; inset:0; background:rgba(0,0,0,.7); display:none; align-items:center; justify-content:center; z-index: 99; }}
.modal.open {{ display:flex; }}
.modal .box {{ background:var(--panel); border:1px solid var(--border); border-radius:8px;
  max-width: 80vw; max-height: 80vh; overflow: auto; padding: 20px; }}
.modal pre {{ font-size:12px; background:var(--code); padding:12px; border-radius:6px; }}
.final video {{ width:100%; max-height: 70vh; background:#000; border-radius:6px; }}
.empty {{ color: var(--mute); font-style: italic; }}
.pill-bar {{ display:flex; flex-wrap:wrap; gap:6px; }}
.kpill {{ background:var(--panel2); color:var(--mute); font-size:11px; padding:1px 8px; border-radius: 4px; }}
</style>
</head>
<body>
<div class="layout">
<nav>
  <h1>spark-video viewer</h1>
  <div class="meta">
    <div>project · <b>{html.escape(payload['project'])}</b></div>
    <div>episode · <b>{html.escape(payload['episode'])}</b></div>
    <div>shots · <b>{len(payload['shots'])}</b></div>
  </div>
  <ul>
    <li><a href="#final">Final cut</a></li>
    <li><a href="#premise">Premise</a></li>
    <li><a href="#lore">Lore</a></li>
    <li><a href="#direction">Direction</a></li>
    <li><a href="#script">Script</a></li>
    <li><a href="#scenes">Scenes</a></li>
    <li><a href="#cast">Cast</a></li>
    <li><a href="#sets">Sets</a></li>
    <li><a href="#props">Props</a></li>
    <li><a href="#bgm">BGM</a></li>
    <li><a href="#shots">Shots</a></li>
    <li><a href="#calls">Model calls</a></li>
  </ul>
</nav>
<main>
  <section id="final"><h2>Final cut</h2><div id="x-final" class="final"></div></section>
  <section id="premise"><h2>Premise (initial prompt)</h2><div id="x-premise"></div></section>
  <section id="lore"><h2>Lore (story bible)</h2><div id="x-lore"></div></section>
  <section id="direction"><h2>Direction</h2><div id="x-direction"></div></section>
  <section id="script"><h2>Script</h2><div id="x-script"></div></section>
  <section id="scenes"><h2>Scenes</h2><div id="x-scenes"></div></section>
  <section id="cast"><h2>Cast</h2><div id="x-cast" class="grid"></div></section>
  <section id="sets"><h2>Movie sets</h2><div id="x-sets" class="grid"></div></section>
  <section id="props"><h2>Props</h2><div id="x-props" class="grid"></div></section>
  <section id="bgm"><h2>BGM</h2><div id="x-bgm"></div></section>
  <section id="shots"><h2>Shots</h2><div id="x-shots"></div></section>
  <section id="calls"><h2>Model calls</h2><div id="x-calls" class="calls"></div></section>
</main>
</div>

<div id="modal" class="modal"><div class="box"><pre id="modal-body"></pre></div></div>

<script type="application/json" id="data">{data_json}</script>
<script>
const D = JSON.parse(document.getElementById('data').textContent);
const $ = (id) => document.getElementById(id);
const esc = (s) => (s == null ? '' : String(s).replace(/[&<>"']/g, c => (
  {{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c])));
const md = (txt) => {{
  if (!txt) return '<div class="empty">(empty)</div>';
  try {{ return marked.parse(txt); }} catch (e) {{ return '<pre>' + esc(txt) + '</pre>'; }}
}};
const missing = (msg) => `<div class="empty">${{esc(msg || '(missing)')}}</div>`;

// ---- markdown sections
$('x-premise').innerHTML = D.premise
  ? `<div class="md">${{md(D.premise)}}</div>` +
    (D.premise_source ? `<div style="margin-top:6px;font-size:11px;color:var(--mute)">source · <code>${{esc(D.premise_source)}}</code></div>` : '')
  : missing('(no initialPrompt.md / premise.md found in project or episode dir)');
$('x-lore').innerHTML = D.lore ? `<div class="md">${{md(D.lore)}}</div>` : missing('(no lore.md found)');
$('x-script').innerHTML = D.script ? `<div class="md">${{md(D.script)}}</div>` : missing('(no script.md found)');

// ---- direction
if (D.direction) {{
  const dd = D.direction;
  const av = dd.audiovisual_decisions || {{}};
  const tones = dd.tone_dimensions || {{}};
  const motifs = (dd.imagery_system && dd.imagery_system.motifs) || [];
  $('x-direction').innerHTML = `
    <div class="card">
      <div><b>Tone:</b> ${{esc(tones.primary||'')}} ${{tones.secondary?'· '+esc(tones.secondary):''}}</div>
      <div><b>Director ref:</b> ${{esc(dd.director_reference||'')}}</div>
    </div>
    <div class="card">
      ${{Object.entries(av).map(([k,v]) => `<div style="margin:4px 0;font-size:13px;"><b>${{esc(k)}}:</b> <span style="color:var(--mute)">${{esc(v)}}</span></div>`).join('')}}
    </div>
    ${{motifs.length ? `<div class="card"><h3 style="margin-top:0">Motifs</h3>${{motifs.map(m=>`<div style="margin:6px 0"><b>${{esc(m.name)}}</b> — <span style="color:var(--mute)">${{esc(m.meaning)}}</span> ${{(m.landings||[]).map(l=>`<span class=\"kpill\">${{esc(l)}}</span>`).join(' ')}}</div>`).join('')}}</div>` : ''}}
  `;
}} else {{ $('x-direction').innerHTML = missing('(no direction.json)'); }}

// ---- scenes
$('x-scenes').innerHTML = (D.scenes && D.scenes.length) ? D.scenes.map(s => `
  <details><summary>${{esc(s.name)}}${{s.json && s.json.shots ? ' · '+s.json.shots.length+' shots' : ''}}</summary>
    <div class="md">${{md(s.body)}}</div>
  </details>`).join('') : missing('(no scenes/)');

// ---- entity grids
const renderEntity = (e, basePath) => {{
  const portrait = e.images && e.images[0];
  const fm = e.frontmatter || {{}};
  const fmKeys = ['age','gender','occupation','archetype','voice_style'].filter(k => fm[k]);
  return `<div class="entity">
    ${{portrait ? `<img src="${{portrait}}" alt="${{esc(e.name)}}">` : `<div style="height:180px;background:var(--bg);border-radius:6px;display:flex;align-items:center;justify-content:center;color:var(--mute)">no image</div>`}}
    <h4>${{esc(e.name)}}</h4>
    ${{fmKeys.length ? `<div class="fm">${{fmKeys.map(k=>`<span><b>${{k}}</b>: ${{esc(fm[k])}}</span>`).join('')}}</div>` : ''}}
    ${{(e.audios||[]).map(u=>`<audio controls src="${{u}}"></audio>`).join('')}}
    ${{e.body ? `<details><summary>soul card</summary><div class="md">${{md(e.body)}}</div></details>` : ''}}
    ${{(e.images||[]).length > 1 ? `<details><summary>${{e.images.length}} images</summary>${{e.images.map(u=>`<img class="thumb" src="${{u}}">`).join('')}}</details>` : ''}}
  </div>`;
}};
$('x-cast').innerHTML = (D.cast||[]).length ? D.cast.map(c => renderEntity(c)).join('') : missing('(no cast)');
$('x-sets').innerHTML = (D.sets||[]).length ? D.sets.map(c => renderEntity(c)).join('') : missing('(no movie-set/)');
$('x-props').innerHTML = (D.props||[]).length ? D.props.map(c => renderEntity(c)).join('') : missing('(no props/)');

// ---- bgm
$('x-bgm').innerHTML = (D.bgm||[]).length ? D.bgm.map(b => `<div class="card"><b>${{esc(b.name)}}</b><br><audio controls src="${{b.url}}" style="width:100%"></audio></div>`).join('') : missing('(no bgm/)');

// ---- shots
const renderReview = (r) => {{
  if (!r) return missing('(no review)');
  const bd = r.breakdown || {{}};
  const verdict = r.verdict || 'UNKNOWN';
  return `<div class="review">
    <div><span class="score">${{esc(r.score ?? '—')}}</span><span class="verdict ${{esc(verdict)}}">${{esc(verdict)}}</span></div>
    <table>${{Object.entries(bd).map(([k,v])=>`<tr><td>${{esc(k)}}</td><td>${{esc(v)}}</td></tr>`).join('')}}</table>
    ${{r.critique ? `<details><summary>critique</summary><div class="critique">${{esc(r.critique)}}</div></details>` : ''}}
  </div>`;
}};

const shotsHtml = (D.shots||[]).map((shot, si) => {{
  const versions = shot.versions || [];
  if (!versions.length) {{
    return `<div class="shot"><div class="shot-head"><span class="id">${{esc(shot.id)}}</span><span class="pill">no clips</span></div></div>`;
  }}
  const winner = shot.winner_version;
  const tabs = versions.map(v => `<div class="tab ${{v.version===winner?'winner':''}}" data-shot="${{si}}" data-ver="${{v.version}}">v${{v.version}}</div>`).join('');
  const renderPromptBlock = (v) => {{
    // The storyboard's director prompt is shown once at the shot level
    // (shotPromptBlock below). Per-version, we surface:
    //   1. sent_prompt — pulled from logs/model_calls.jsonl --prompt arg.
    //      This is GROUND TRUTH — exactly what the video model received.
    //   2. prompt      — shots_state.json attempts[].prompt — what
    //      render_shot.py was invoked with. Should equal #1; if it does,
    //      we collapse the two into one block.
    const sent = v.sent_prompt;
    const rec = v.prompt;
    const same = (a, b) => (a||'').trim() === (b||'').trim();
    const out = [];
    if (sent) {{
      out.push(`<details open><summary>prompt actually sent to model <span class="kpill">model_calls.jsonl</span></summary><div class="md"><pre>${{esc(sent)}}</pre></div></details>`);
    }}
    if (rec && !same(rec, sent)) {{
      const badge = sent
        ? `<span class="kpill" style="background:#5a3a00;color:#f0b429">differs from sent</span>`
        : `<span class="kpill">recorded by render_shot.py</span>`;
      out.push(`<details${{sent?'':' open'}}><summary>render_shot prompt ${{badge}}</summary><div class="md"><pre>${{esc(rec)}}</pre></div></details>`);
    }}
    return out.join('');
  }};

  const panels = versions.map(v => `<div class="version-panel" data-shot="${{si}}" data-ver="${{v.version}}" style="display:none">
    <div class="version-body">
      <div>
        <video controls preload="metadata" src="${{v.clip_url}}"></video>
        ${{v.thumb_url ? `<details><summary>last frame</summary><img class="thumb" src="${{v.thumb_url}}"></details>` : ''}}
        ${{renderPromptBlock(v)}}
        ${{v.task_id ? `<div style="font-size:11px;color:var(--mute);margin-top:6px">task: ${{esc(v.task_id)}}</div>` : ''}}
      </div>
      <div>${{renderReview(v.review)}}</div>
    </div>
  </div>`).join('');
  const shotPromptBlock = shot.prompt
    ? `<details style="margin:8px 0"><summary>storyboard prompt (director's intent) · ${{(shot.prompt||'').length}} chars</summary><div class="md"><pre>${{esc(shot.prompt)}}</pre></div></details>`
    : '';
  return `<div class="shot">
    <div class="shot-head">
      <span class="id">${{esc(shot.id)}}</span>
      ${{shot.scene ? `<span class="pill">${{esc(shot.scene)}}</span>` : ''}}
      ${{shot.kind ? `<span class="pill">${{esc(shot.kind)}}</span>` : ''}}
      ${{shot.duration ? `<span class="pill">${{shot.duration}}s</span>` : ''}}
      ${{(shot.characters||[]).map(c=>`<span class="kpill">${{esc(c)}}</span>`).join('')}}
      ${{shot.narrative_purpose ? `<div class="purpose">${{esc(shot.narrative_purpose)}}</div>` : ''}}
    </div>
    ${{shotPromptBlock}}
    <div class="tabs">${{tabs}}</div>
    ${{panels}}
  </div>`;
}}).join('');
$('x-shots').innerHTML = shotsHtml || missing('(no shots)');

// activate winner (or first) version on each shot
document.querySelectorAll('.shot').forEach((node, si) => {{
  const tabs = node.querySelectorAll('.tab');
  if (!tabs.length) return;
  let initial = Array.from(tabs).find(t=>t.classList.contains('winner')) || tabs[0];
  const activate = (ver) => {{
    node.querySelectorAll('.tab').forEach(t => t.classList.toggle('active', t.dataset.ver===String(ver)));
    node.querySelectorAll('.version-panel').forEach(p => p.style.display = (p.dataset.ver===String(ver)) ? '' : 'none');
  }};
  activate(initial.dataset.ver);
  tabs.forEach(t => t.addEventListener('click', () => activate(t.dataset.ver)));
}});

// ---- calls
const calls = D.calls || {{}};
const byShot = calls.by_shot || {{}};
const shotKeys = Object.keys(byShot).sort();
if (!shotKeys.length) {{
  $('x-calls').innerHTML = missing('(no logs/model_calls.jsonl)');
}} else {{
  const rows = shotKeys.map(sid => {{
    const s = byShot[sid];
    const kinds = Object.entries(s.kinds).map(([k,v])=>`${{esc(k)}}:${{v}}`).join(' · ');
    return `<tr class="row" data-shot="${{esc(sid)}}"><td>${{esc(sid)}}</td><td>${{s.count}}</td><td>${{(s.duration_ms/1000).toFixed(2)}}s</td><td>${{kinds}}</td></tr>`;
  }}).join('');
  $('x-calls').innerHTML = `<div class="card" style="margin-bottom:10px;color:var(--mute);font-size:13px">total ${{calls.total}} calls — click a row for raw JSON</div>
    <table><thead><tr><th>shot</th><th>count</th><th>duration</th><th>kinds</th></tr></thead><tbody>${{rows}}</tbody></table>`;
  document.querySelectorAll('.calls tr.row').forEach(r => r.addEventListener('click', () => {{
    const sid = r.dataset.shot;
    const recs = (calls.raw||[]).filter(x => (x.shot_id||'_project_')===sid);
    $('modal-body').textContent = JSON.stringify(recs, null, 2);
    $('modal').classList.add('open');
  }}));
  $('modal').addEventListener('click', (e) => {{ if (e.target.id==='modal') $('modal').classList.remove('open'); }});
}}

// ---- final
if (D.final) {{
  $('x-final').innerHTML = `<div class="card">
    <div style="margin-bottom:8px"><b>${{esc(D.final.name)}}</b> · ${{(D.final.size_bytes/1024/1024).toFixed(1)}} MB</div>
    <video controls preload="metadata" src="${{D.final.url}}"></video>
  </div>`;
}} else {{ $('x-final').innerHTML = missing('(not stitched yet)'); }}
</script>
</body>
</html>
"""


def main() -> int:
    project, episode, no_open = _resolve_ids()
    ep_norm = normalize_episode_id(episode)
    ep_dir = episode_dir(project, episode)
    proj_dir = project_dir(project)

    storyboard = _load_json(ep_dir / "storyboard.json")
    calls = _collect_calls(ep_dir)

    # Try a few plausible filenames for the user's original premise. The
    # repo doesn't enforce a single canonical name yet — agents may write
    # it as initialPrompt.md (legacy) or premise.md (newer convention),
    # at the project or episode tier. First non-empty wins.
    premise_candidates = (
        ep_dir / "initialPrompt.md",
        ep_dir / "premise.md",
        proj_dir / "initialPrompt.md",
        proj_dir / "premise.md",
    )
    premise_text = None
    premise_source = None
    for cand in premise_candidates:
        text = _read_text(cand)
        if text and text.strip():
            premise_text = text
            premise_source = str(cand.relative_to(proj_dir.parent))
            break

    payload = {
        "project": project,
        "episode": ep_norm,
        "premise": premise_text,
        "premise_source": premise_source,
        "lore": _read_text(proj_dir / "lore.md"),
        "direction": _load_json(ep_dir / "direction.json"),
        "script": _read_text(ep_dir / "script.md"),
        "scenes": _collect_scenes(ep_dir),
        "cast": (
            _collect_entities(proj_dir / "cast", ep_dir, "cast.md")
            + _collect_entities(ep_dir / "cast", ep_dir, "cast.md")
        ),
        "sets": _collect_entities(proj_dir / "movie-set", ep_dir, "set.md"),
        "props": _collect_entities(proj_dir / "props", ep_dir, "prop.md"),
        "bgm": _collect_bgm(proj_dir, ep_dir),
        "shots": _collect_shots(
            ep_dir, storyboard, calls.get("sent_by_shot_ver"),
        ),
        "calls": calls,
        "final": _collect_final(ep_dir, project, ep_norm),
    }

    out = ep_dir / "viewer.html"
    out.write_text(_html(payload), encoding="utf-8")
    print(f"[viewer] wrote {out}")

    if not no_open and platform.system() == "Darwin":
        try:
            subprocess.run(["open", str(out)], check=False)
        except Exception as e:
            print(f"[viewer] open failed: {e}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
