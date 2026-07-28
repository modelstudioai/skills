#!/usr/bin/env python3
"""Deterministic media operations backed by ffmpeg/ffprobe and optional bl ASR."""

from __future__ import annotations

import argparse
import array
import hashlib
import json
import math
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import wave
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable, Sequence


DEFAULT_FILLERS = [
    "嗯",
    "呃",
    "额",
    "啊",
    "唔",
    "那个",
    "就是",
    "然后",
    "其实",
    "基本上",
    "怎么说",
    "um",
    "uh",
    "erm",
    "you know",
    "like",
]

MEETING_FILLERS = [
    "嗯",
    "呃",
    "额",
    "啊",
    "哦",
    "唔",
    "哎",
    "um",
    "uh",
    "erm",
]

AI_CLEANUP_LEVELS = {
    "conservative": {
        "min_confidence": 0.90,
        "max_tokens": 3,
        "max_span_seconds": 1.5,
        "categories": {
            "filler",
            "verbal_tic",
            "self_confirmation",
            "false_start",
            "exact_repeat",
        },
    },
    "balanced": {
        "min_confidence": 0.75,
        "max_tokens": 10,
        "max_span_seconds": 3.5,
        "categories": {
            "filler",
            "verbal_tic",
            "self_confirmation",
            "false_start",
            "exact_repeat",
            "discourse_marker",
            "speech_repair",
            "redundant_rephrase",
        },
    },
    "aggressive": {
        "min_confidence": 0.60,
        "max_tokens": 30,
        "max_span_seconds": 8.0,
        "categories": {
            "filler",
            "verbal_tic",
            "self_confirmation",
            "false_start",
            "exact_repeat",
            "discourse_marker",
            "speech_repair",
            "redundant_rephrase",
            "redundant_clause",
            "low_information",
        },
    },
}

AI_PROTECTED_NEGATIONS = {
    "不",
    "不是",
    "别",
    "否",
    "没有",
    "没",
    "未",
    "无",
    "no",
    "not",
    "never",
    "dont",
    "don't",
    "cant",
    "can't",
    "wont",
    "won't",
    "ない",
    "ません",
    "안",
    "못",
}

AUDIO_CODEC_ARGS = {
    ".aac": ["-c:a", "aac", "-b:a", "192k"],
    ".flac": ["-c:a", "flac"],
    ".m4a": ["-c:a", "aac", "-b:a", "192k"],
    ".mp3": ["-c:a", "libmp3lame", "-q:a", "2"],
    ".opus": ["-c:a", "libopus", "-b:a", "160k"],
    ".wav": ["-c:a", "pcm_s16le"],
}

VIDEO_PRESETS = {
    "cinematic": "eq=contrast=1.08:saturation=0.90:brightness=-0.02,colorbalance=bs=.05",
    "cool": "eq=contrast=1.04:saturation=0.95,colorbalance=bs=.08:rs=-.03",
    "fair-skin": "eq=brightness=.025:contrast=.98:saturation=.92",
    "food": "eq=contrast=1.08:saturation=1.25:brightness=.01,colorbalance=rs=.04",
    "mono": "hue=s=0,eq=contrast=1.10",
    "spring": "eq=brightness=.02:saturation=1.12,colorbalance=gs=.035:rs=.02",
    "sunset": "eq=contrast=1.05:saturation=1.18,colorbalance=rs=.10:bs=-.05",
    "vivid": "eq=contrast=1.08:saturation=1.28",
    "warm": "eq=contrast=1.03:saturation=1.08,colorbalance=rs=.07:bs=-.04",
}


class MediaError(RuntimeError):
    pass


class DependencyError(MediaError):
    def __init__(self, operation: str, missing: Sequence[str]):
        self.operation = operation
        self.missing = list(dict.fromkeys(missing))
        super().__init__(
            f"{operation} is unavailable because dependencies are missing: "
            + ", ".join(self.missing)
        )


def command_path(name: str) -> str | None:
    override_name = {
        "ffmpeg": "MEDIA_UTILS_FFMPEG",
        "ffprobe": "MEDIA_UTILS_FFPROBE",
        "bl": "MEDIA_UTILS_BL",
    }.get(name)
    if override_name and os.environ.get(override_name):
        override = os.environ[override_name]
        resolved = shutil.which(override)
        if resolved:
            return resolved
        candidate = Path(override).expanduser()
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate.resolve())
        return None
    if name in {"ffmpeg", "ffprobe"}:
        for prefix in [
            Path("/opt/homebrew/opt/ffmpeg-full/bin"),
            Path("/usr/local/opt/ffmpeg-full/bin"),
        ]:
            candidate = prefix / name
            if candidate.is_file() and os.access(candidate, os.X_OK):
                return str(candidate.resolve())
    return shutil.which(name)


def require_command(name: str) -> str:
    path = command_path(name)
    if not path:
        raise DependencyError("command execution", [f"command:{name}"])
    return path


def is_url(value: str) -> bool:
    return bool(re.match(r"^https?://", value, re.IGNORECASE))


def require_input(value: str) -> str:
    if not is_url(value) and not Path(value).expanduser().is_file():
        raise MediaError(f"Input file not found: {value}")
    return str(Path(value).expanduser().resolve()) if not is_url(value) else value


def prepare_output(value: str, force: bool, dry_run: bool = False) -> Path:
    output = Path(value).expanduser().resolve()
    if output.exists() and not force:
        raise MediaError(f"Output already exists: {output}. Pass --force to overwrite it.")
    if not dry_run:
        output.parent.mkdir(parents=True, exist_ok=True)
    return output


def run_command(
    command: Sequence[str],
    *,
    dry_run: bool = False,
    capture: bool = False,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    if dry_run:
        print(json.dumps({"command": list(command)}, ensure_ascii=False, indent=2))
        return subprocess.CompletedProcess(command, 0, "", "")
    try:
        return subprocess.run(
            list(command),
            check=True,
            text=True,
            capture_output=capture,
            env=env,
        )
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout or "").strip()
        raise MediaError(f"Command failed ({exc.returncode}): {' '.join(command)}\n{detail}") from exc


def ffmpeg_prefix(force: bool) -> list[str]:
    return [
        require_command("ffmpeg"),
        "-hide_banner",
        "-loglevel",
        "warning",
        "-stats",
        "-nostdin",
        "-y" if force else "-n",
    ]


def probe_media(input_value: str) -> dict[str, Any]:
    source = require_input(input_value)
    result = run_command(
        [
            require_command("ffprobe"),
            "-v",
            "error",
            "-show_format",
            "-show_streams",
            "-of",
            "json",
            source,
        ],
        capture=True,
    )
    return json.loads(result.stdout)


def media_duration(input_value: str) -> float:
    data = probe_media(input_value)
    duration = data.get("format", {}).get("duration")
    if duration is None:
        durations = [
            stream.get("duration")
            for stream in data.get("streams", [])
            if stream.get("duration") is not None
        ]
        if durations:
            duration = max(float(value) for value in durations)
    if duration is None:
        raise MediaError(f"Could not determine media duration: {input_value}")
    return float(duration)


def has_stream(data: dict[str, Any], codec_type: str) -> bool:
    return any(stream.get("codec_type") == codec_type for stream in data.get("streams", []))


def write_json(path: Path, payload: Any, force: bool) -> None:
    if path.exists() and not force:
        raise MediaError(f"Output already exists: {path}. Pass --force to overwrite it.")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


@lru_cache(maxsize=1)
def ffmpeg_encoder_names() -> frozenset[str]:
    result = run_command(
        [require_command("ffmpeg"), "-hide_banner", "-encoders"],
        capture=True,
    )
    return frozenset(
        match.group(1)
        for match in re.finditer(
            r"^\s*[A-Z.]{6}\s+(\S+)(?:\s|$)", result.stdout, re.MULTILINE
        )
    )


def require_ffmpeg_encoders(operation: str, names: Sequence[str]) -> None:
    available = ffmpeg_encoder_names()
    missing = [f"encoder:{name}" for name in names if name not in available]
    if missing:
        raise DependencyError(operation, missing)


def require_ffmpeg_filter(operation: str, name: str) -> None:
    if not ffmpeg_has_filter(name):
        raise DependencyError(operation, [f"filter:{name}"])


def audio_codec_args(output: Path) -> list[str]:
    if output.suffix.lower() == ".ogg":
        encoders = ffmpeg_encoder_names()
        if "libvorbis" in encoders:
            return ["-c:a", "libvorbis", "-q:a", "6"]
        if "vorbis" in encoders:
            return ["-c:a", "vorbis", "-strict", "experimental", "-q:a", "6"]
        raise DependencyError("OGG audio output", ["encoder:libvorbis|vorbis"])
    try:
        args = AUDIO_CODEC_ARGS[output.suffix.lower()]
    except KeyError as exc:
        supported = ", ".join(sorted(AUDIO_CODEC_ARGS))
        raise MediaError(f"Unsupported audio output extension {output.suffix!r}; use {supported}") from exc
    require_ffmpeg_encoders(f"{output.suffix.lower()} audio output", [args[1]])
    return args


def video_codec_args(
    output: Path, *, alpha: bool = False, with_audio: bool = True
) -> list[str]:
    suffix = output.suffix.lower()
    if alpha:
        if suffix == ".webm":
            require_ffmpeg_encoders(
                "alpha WebM output",
                ["libvpx-vp9", *(["libopus"] if with_audio else [])],
            )
            args = [
                "-c:v",
                "libvpx-vp9",
                "-pix_fmt",
                "yuva420p",
                "-auto-alt-ref",
                "0",
                "-crf",
                "30",
                "-b:v",
                "0",
            ]
            return [*args, "-c:a", "libopus"] if with_audio else args
        if suffix == ".mov":
            require_ffmpeg_encoders(
                "alpha MOV output",
                ["qtrle", *(["pcm_s16le"] if with_audio else [])],
            )
            args = ["-c:v", "qtrle", "-pix_fmt", "argb"]
            return [*args, "-c:a", "pcm_s16le"] if with_audio else args
        raise MediaError("Alpha video output must use .webm or .mov")
    if suffix in {".mp4", ".m4v", ".mov"}:
        require_ffmpeg_encoders(
            f"{suffix} video output",
            ["libx264", *(["aac"] if with_audio else [])],
        )
        args = [
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "18",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
        ]
        return [*args, "-c:a", "aac", "-b:a", "192k"] if with_audio else args
    if suffix == ".webm":
        require_ffmpeg_encoders(
            "WebM video output",
            ["libvpx-vp9", *(["libopus"] if with_audio else [])],
        )
        args = ["-c:v", "libvpx-vp9", "-crf", "30", "-b:v", "0"]
        return [*args, "-c:a", "libopus"] if with_audio else args
    if suffix == ".mkv":
        require_ffmpeg_encoders(
            "MKV video output",
            ["libx264", *(["aac"] if with_audio else [])],
        )
        args = ["-c:v", "libx264", "-crf", "18"]
        return [*args, "-c:a", "aac", "-b:a", "192k"] if with_audio else args
    raise MediaError("Unsupported video output extension; use .mp4, .m4v, .mov, .mkv, or .webm")


def image_codec_args(output: Path) -> list[str]:
    suffix = output.suffix.lower()
    if suffix == ".png":
        require_ffmpeg_encoders("PNG image output", ["png"])
        return ["-c:v", "png"]
    if suffix in {".jpg", ".jpeg"}:
        require_ffmpeg_encoders("JPEG image output", ["mjpeg"])
        return ["-c:v", "mjpeg", "-q:v", "2"]
    if suffix == ".webp":
        require_ffmpeg_encoders("WebP image output", ["libwebp"])
        return ["-c:v", "libwebp", "-quality", "90"]
    if suffix in {".bmp", ".tif", ".tiff"}:
        return []
    raise MediaError("Unsupported image output extension; use .png, .jpg, .webp, .bmp, or .tiff")


def single_image_output_args(output: Path) -> list[str]:
    return [*image_codec_args(output), "-update", "1"]


def ffmpeg_has_filter(name: str) -> bool:
    result = run_command(
        [require_command("ffmpeg"), "-hide_banner", "-filters"],
        capture=True,
    )
    return bool(re.search(rf"\b{re.escape(name)}\b", result.stdout))


def atempo_chain(factor: float) -> str:
    if factor <= 0:
        raise MediaError("Speed factor must be greater than zero")
    pieces: list[float] = []
    remaining = factor
    while remaining > 2.0:
        pieces.append(2.0)
        remaining /= 2.0
    while remaining < 0.5:
        pieces.append(0.5)
        remaining /= 0.5
    pieces.append(remaining)
    return ",".join(f"atempo={piece:.8g}" for piece in pieces)


def escape_concat_path(path: str) -> str:
    return path.replace("'", "'\\''")


def escape_filter_path(path: str) -> str:
    escaped = path.replace("\\", "\\\\")
    for character in [":", "'", "[", "]", ",", ";"]:
        escaped = escaped.replace(character, f"\\{character}")
    return escaped


def detect_package_manager() -> str | None:
    for name in ["brew", "apt-get", "dnf", "yum", "pacman", "choco"]:
        if shutil.which(name):
            return name
    return None


DOCTOR_OPERATIONS = {
    "core": {
        "commands": ["ffmpeg", "ffprobe"],
        "filters": [],
        "encoders_all": [],
        "encoders_any": [],
    },
    "subtitle-burn": {
        "commands": ["ffmpeg", "ffprobe"],
        "filters": ["subtitles"],
        "encoders_all": ["libx264"],
        "encoders_any": [],
    },
    "image-webp": {
        "commands": ["ffmpeg"],
        "filters": [],
        "encoders_all": ["libwebp"],
        "encoders_any": [],
    },
    "video-alpha-webm": {
        "commands": ["ffmpeg", "ffprobe"],
        "filters": ["chromakey"],
        "encoders_all": ["libvpx-vp9", "libopus"],
        "encoders_any": [],
    },
    "audio-ogg": {
        "commands": ["ffmpeg"],
        "filters": [],
        "encoders_all": [],
        "encoders_any": ["libvorbis", "vorbis"],
    },
    "dialogue-transcribe": {
        "commands": ["bl"],
        "filters": [],
        "encoders_all": [],
        "encoders_any": [],
    },
    "dialogue-ai-plan": {
        "commands": ["bl"],
        "filters": [],
        "encoders_all": [],
        "encoders_any": [],
    },
    "meeting-cleanup": {
        "commands": ["ffmpeg", "ffprobe", "bl"],
        "filters": ["acrossfade", "concat"],
        "encoders_all": [],
        "encoders_any": [],
    },
}


def dependency_install_plan(
    missing: Sequence[str],
    required_for: Sequence[str],
) -> dict[str, Any]:
    manager = detect_package_manager()
    actions: list[dict[str, Any]] = []
    missing_set = set(missing)
    missing_ffmpeg = bool({"command:ffmpeg", "command:ffprobe"} & missing_set)
    missing_full_features = bool(
        {"filter:subtitles", "encoder:libwebp"} & missing_set
    ) or any(
        "subtitle" in name.casefold() or "webp" in name.casefold()
        for name in required_for
    )

    if missing_ffmpeg or missing_full_features:
        full = missing_full_features
        optional_features = []
        if "filter:subtitles" in missing_set or any(
            "subtitle" in name.casefold() for name in required_for
        ):
            optional_features.append("libass/subtitles")
        if "encoder:libwebp" in missing_set or any(
            "webp" in name.casefold() for name in required_for
        ):
            optional_features.append("libwebp")
        reason = (
            "This operation requires an ffmpeg build with "
            + " and ".join(optional_features)
            if full
            else "This operation requires ffmpeg and/or ffprobe"
        )
        if manager == "brew":
            commands = [f"brew install {'ffmpeg-full' if full else 'ffmpeg'}"]
        elif manager == "apt-get":
            commands = [
                "sudo apt-get update",
                "sudo apt-get install -y ffmpeg",
            ]
        elif manager == "dnf":
            commands = ["sudo dnf install -y ffmpeg"]
        elif manager == "yum":
            commands = ["sudo yum install -y ffmpeg"]
        elif manager == "pacman":
            commands = ["sudo pacman -S --needed ffmpeg"]
        elif manager == "choco":
            commands = [f"choco install {'ffmpeg-full' if full else 'ffmpeg'}"]
        else:
            commands = ["Install FFmpeg from https://ffmpeg.org/download.html"]
            if full:
                commands = [
                    "Install an ffmpeg build compiled with the requested libass/libwebp feature"
                ]
        actions.append(
            {
                "id": "ffmpeg-full" if full else "ffmpeg",
                "required_for": list(required_for),
                "reason": reason,
                "commands": commands,
            }
        )

    if "command:bl" in missing_set:
        actions.append(
            {
                "id": "bl",
                "required_for": list(required_for),
                "reason": "Bailian CLI is required for ASR and speaker diarization",
                "commands": ["npm install -g bailian-cli"],
            }
        )

    remaining = sorted(
        missing_set
        - {"command:ffmpeg", "command:ffprobe", "command:bl"}
        - {"filter:subtitles", "encoder:libwebp"}
    )
    if remaining:
        actions.append(
            {
                "id": "ffmpeg-feature-build",
                "required_for": list(required_for),
                "reason": "The selected ffmpeg build lacks operation-specific features",
                "missing": remaining,
                "commands": [
                    "Install an ffmpeg build containing the missing filters/encoders"
                ],
            }
        )

    return {
        "mode": "install-plan",
        "os": platform.system().lower(),
        "package_manager": manager,
        "actions": actions,
    }


def operation_missing_dependencies(
    operation: str,
    commands: dict[str, str | None],
    filters: Sequence[str],
    encoders: Sequence[str],
) -> list[str]:
    requirements = DOCTOR_OPERATIONS[operation]
    missing = [
        f"command:{name}"
        for name in requirements["commands"]
        if not commands.get(name)
    ]
    if commands.get("ffmpeg"):
        missing.extend(
            f"filter:{name}"
            for name in requirements["filters"]
            if name not in filters
        )
        missing.extend(
            f"encoder:{name}"
            for name in requirements["encoders_all"]
            if name not in encoders
        )
        alternatives = requirements["encoders_any"]
        if alternatives and not any(name in encoders for name in alternatives):
            missing.append("encoder:" + "|".join(alternatives))
    return missing


def command_doctor(args: argparse.Namespace) -> None:
    commands = {name: command_path(name) for name in ["ffmpeg", "ffprobe", "bl"]}
    filters: list[str] = []
    encoders: list[str] = []
    if commands["ffmpeg"]:
        filters_result = run_command(
            [commands["ffmpeg"] or "ffmpeg", "-hide_banner", "-filters"],
            capture=True,
        )
        filter_text = filters_result.stdout
        filters = [
            name
            for name in [
                "acrossfade",
                "afade",
                "amix",
                "atempo",
                "chromakey",
                "colorkey",
                "concat",
                "overlay",
                "scdet",
                "silencedetect",
                "subtitles",
                "xfade",
            ]
            if re.search(rf"\b{re.escape(name)}\b", filter_text)
        ]
        encoder_text = run_command(
            [commands["ffmpeg"] or "ffmpeg", "-hide_banner", "-encoders"],
            capture=True,
        ).stdout
        encoders = [
            name
            for name in [
                "aac",
                "flac",
                "libmp3lame",
                "libopus",
                "libvorbis",
                "libvpx-vp9",
                "libwebp",
                "libx264",
                "mjpeg",
                "opus",
                "pcm_s16le",
                "png",
                "qtrle",
                "vorbis",
            ]
            if re.search(rf"\b{re.escape(name)}\b", encoder_text)
        ]
    capabilities = {
        "subtitles": "subtitles" in filters,
        "webp_output": "libwebp" in encoders,
        "alpha_webm": "chromakey" in filters and "libvpx-vp9" in encoders,
        "bailian_asr": commands["bl"] is not None,
        "ogg_output": "libvorbis" in encoders or "vorbis" in encoders,
    }
    operation = args.for_operation or "core"
    missing = operation_missing_dependencies(operation, commands, filters, encoders)
    payload: dict[str, Any] = {
        "ok": not missing,
        "operation": operation,
        "missing": missing,
        "python": {
            "path": sys.executable,
            "version": platform.python_version(),
            "ok": sys.version_info >= (3, 10),
        },
        "commands": commands,
        "filters": filters,
        "encoders": encoders,
        "capabilities": capabilities,
    }
    if args.install_plan:
        payload.update(dependency_install_plan(missing, [operation]))
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def command_probe(args: argparse.Namespace) -> None:
    payload = probe_media(args.input)
    if args.output:
        output = prepare_output(args.output, args.force)
        write_json(output, payload, args.force)
        print(output)
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))


def command_trim(args: argparse.Namespace, *, video: bool) -> None:
    source = require_input(args.input)
    output = prepare_output(args.output, args.force, args.dry_run)
    if args.start < 0:
        raise MediaError("--start must be non-negative")
    if args.end is not None and args.end <= args.start:
        raise MediaError("--end must be greater than --start")
    command = ffmpeg_prefix(args.force)
    command += ["-ss", f"{args.start:.6f}", "-i", source]
    if args.end is not None:
        command += ["-t", f"{args.end - args.start:.6f}"]
    command += ["-map", "0:v?", "-map", "0:a?"]
    command += video_codec_args(output) if video else ["-vn", *audio_codec_args(output)]
    command.append(str(output))
    run_command(command, dry_run=args.dry_run)


def command_concat(args: argparse.Namespace, *, video: bool) -> None:
    sources = [require_input(value) for value in args.inputs]
    if len(sources) < 1:
        raise MediaError("At least one input is required")
    output = prepare_output(args.output, args.force, args.dry_run)
    if args.dry_run:
        payload = {
            "operation": "concat",
            "inputs": sources,
            "output": str(output),
            "media_type": "video" if video else "audio",
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    with tempfile.NamedTemporaryFile("w", suffix=".txt", encoding="utf-8") as manifest:
        for source in sources:
            manifest.write(f"file '{escape_concat_path(source)}'\n")
        manifest.flush()
        command = ffmpeg_prefix(args.force)
        command += ["-f", "concat", "-safe", "0", "-i", manifest.name]
        command += video_codec_args(output) if video else ["-vn", *audio_codec_args(output)]
        command.append(str(output))
        run_command(command)


def command_audio_speed(args: argparse.Namespace) -> None:
    if not 0.1 <= args.factor <= 100:
        raise MediaError("--factor must be between 0.1 and 100")
    source = require_input(args.input)
    output = prepare_output(args.output, args.force, args.dry_run)
    command = ffmpeg_prefix(args.force)
    command += ["-i", source, "-vn", "-filter:a", atempo_chain(args.factor)]
    command += audio_codec_args(output)
    command.append(str(output))
    run_command(command, dry_run=args.dry_run)


def command_audio_volume(args: argparse.Namespace) -> None:
    source = require_input(args.input)
    output = prepare_output(args.output, args.force, args.dry_run)
    if args.loudnorm:
        audio_filter = "loudnorm=I=-16:LRA=11:TP=-1.5"
    else:
        if args.factor < 0:
            raise MediaError("--factor must be non-negative")
        audio_filter = f"volume={args.factor:.8g}"
    command = ffmpeg_prefix(args.force)
    command += ["-i", source, "-vn", "-filter:a", audio_filter]
    command += audio_codec_args(output)
    command.append(str(output))
    run_command(command, dry_run=args.dry_run)


def command_audio_fade(args: argparse.Namespace) -> None:
    source = require_input(args.input)
    output = prepare_output(args.output, args.force, args.dry_run)
    duration = media_duration(source)
    if min(args.fade_in, args.fade_out) < 0:
        raise MediaError("Fade durations must be non-negative")
    if args.fade_out > duration:
        raise MediaError("--fade-out cannot exceed the input duration")
    filters: list[str] = []
    if args.fade_in:
        filters.append(f"afade=t=in:st=0:d={args.fade_in:.6f}")
    if args.fade_out:
        filters.append(f"afade=t=out:st={duration - args.fade_out:.6f}:d={args.fade_out:.6f}")
    command = ffmpeg_prefix(args.force)
    command += ["-i", source, "-vn"]
    if filters:
        command += ["-filter:a", ",".join(filters)]
    command += audio_codec_args(output)
    command.append(str(output))
    run_command(command, dry_run=args.dry_run)


def command_audio_mix(args: argparse.Namespace) -> None:
    sources = [require_input(value) for value in args.inputs]
    output = prepare_output(args.output, args.force, args.dry_run)
    command = ffmpeg_prefix(args.force)
    for source in sources:
        command += ["-i", source]
    command += [
        "-filter_complex",
        f"amix=inputs={len(sources)}:duration=longest:dropout_transition=0:normalize=0,alimiter=limit=.95",
        "-vn",
    ]
    command += audio_codec_args(output)
    command.append(str(output))
    run_command(command, dry_run=args.dry_run)


def command_audio_convert(args: argparse.Namespace) -> None:
    source = require_input(args.input)
    output = prepare_output(args.output, args.force, args.dry_run)
    command = ffmpeg_prefix(args.force)
    command += ["-i", source, "-vn"]
    if args.sample_rate:
        command += ["-ar", str(args.sample_rate)]
    if args.channels:
        command += ["-ac", str(args.channels)]
    command += audio_codec_args(output)
    command.append(str(output))
    run_command(command, dry_run=args.dry_run)


def parse_silence(stderr: str) -> list[dict[str, Any]]:
    starts = [float(value) for value in re.findall(r"silence_start:\s*([0-9.]+)", stderr)]
    ends = [
        (float(end), float(duration))
        for end, duration in re.findall(
            r"silence_end:\s*([0-9.]+)\s*\|\s*silence_duration:\s*([0-9.]+)",
            stderr,
        )
    ]
    ranges: list[dict[str, Any]] = []
    for index, start in enumerate(starts):
        if index < len(ends):
            end, duration = ends[index]
            ranges.append(
                {
                    "start": round(start, 6),
                    "end": round(end, 6),
                    "duration": round(duration, 6),
                    "reason": "silence",
                }
            )
    return ranges


def command_silence_plan(args: argparse.Namespace) -> None:
    source = require_input(args.input)
    output = prepare_output(args.output, args.force, args.dry_run)
    command = [
        require_command("ffmpeg"),
        "-hide_banner",
        "-nostdin",
        "-i",
        source,
        "-af",
        f"silencedetect=noise={args.noise_db}dB:d={args.min_duration}",
        "-f",
        "null",
        "-",
    ]
    if args.dry_run:
        run_command(command, dry_run=True)
        return
    result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode != 0:
        raise MediaError(result.stderr.strip())
    detected = parse_silence(result.stderr)
    remove: list[dict[str, Any]] = []
    for item in detected:
        removable_start = item["start"] + args.keep
        if item["end"] > removable_start:
            remove.append(
                {
                    "start": round(removable_start, 6),
                    "end": item["end"],
                    "reason": "excess-silence",
                    "detected_duration": item["duration"],
                }
            )
    payload = {
        "schema": "media-utils-edit-plan/v1",
        "approved": False,
        "source": source,
        "duration": media_duration(source),
        "analysis": {
            "noise_db": args.noise_db,
            "min_duration": args.min_duration,
            "keep": args.keep,
            "detected": detected,
        },
        "remove": remove,
    }
    write_json(output, payload, args.force)
    print(output)


def command_image_convert(args: argparse.Namespace) -> None:
    source = require_input(args.input)
    output = prepare_output(args.output, args.force, args.dry_run)
    command = ffmpeg_prefix(args.force)
    command += ["-i", source, "-map_metadata", "-1", "-frames:v", "1"]
    command += single_image_output_args(output)
    command.append(str(output))
    run_command(command, dry_run=args.dry_run)


def command_image_resize(args: argparse.Namespace) -> None:
    if args.width is None and args.height is None:
        raise MediaError("Pass --width, --height, or both")
    if args.width is not None and args.width <= 0:
        raise MediaError("--width must be positive")
    if args.height is not None and args.height <= 0:
        raise MediaError("--height must be positive")
    source = require_input(args.input)
    output = prepare_output(args.output, args.force, args.dry_run)
    width = args.width if args.width is not None else -2
    height = args.height if args.height is not None else -2
    force = "" if args.stretch or -2 in {width, height} else ":force_original_aspect_ratio=decrease"
    video_filter = f"scale={width}:{height}{force}"
    command = ffmpeg_prefix(args.force)
    command += ["-i", source, "-vf", video_filter, "-map_metadata", "-1", "-frames:v", "1"]
    command += single_image_output_args(output)
    command.append(str(output))
    run_command(command, dry_run=args.dry_run)


def command_image_crop(args: argparse.Namespace) -> None:
    if min(args.width, args.height) <= 0 or min(args.x, args.y) < 0:
        raise MediaError("Crop dimensions must be positive and offsets non-negative")
    source = require_input(args.input)
    output = prepare_output(args.output, args.force, args.dry_run)
    command = ffmpeg_prefix(args.force)
    command += [
        "-i",
        source,
        "-vf",
        f"crop={args.width}:{args.height}:{args.x}:{args.y}",
        "-map_metadata",
        "-1",
        "-frames:v",
        "1",
    ]
    command += single_image_output_args(output)
    command.append(str(output))
    run_command(command, dry_run=args.dry_run)


def command_image_rotate(args: argparse.Namespace) -> None:
    filters = {90: "transpose=clock", 180: "hflip,vflip", 270: "transpose=cclock"}
    source = require_input(args.input)
    output = prepare_output(args.output, args.force, args.dry_run)
    command = ffmpeg_prefix(args.force)
    command += [
        "-i",
        source,
        "-vf",
        filters[args.degrees],
        "-map_metadata",
        "-1",
        "-frames:v",
        "1",
    ]
    command += single_image_output_args(output)
    command.append(str(output))
    run_command(command, dry_run=args.dry_run)


def command_image_flip(args: argparse.Namespace) -> None:
    source = require_input(args.input)
    output = prepare_output(args.output, args.force, args.dry_run)
    command = ffmpeg_prefix(args.force)
    command += [
        "-i",
        source,
        "-vf",
        "hflip" if args.direction == "horizontal" else "vflip",
        "-map_metadata",
        "-1",
        "-frames:v",
        "1",
    ]
    command += single_image_output_args(output)
    command.append(str(output))
    run_command(command, dry_run=args.dry_run)


def command_image_thumbnail(args: argparse.Namespace) -> None:
    if min(args.width, args.height) <= 0:
        raise MediaError("Thumbnail dimensions must be positive")
    source = require_input(args.input)
    output = prepare_output(args.output, args.force, args.dry_run)
    video_filter = (
        f"scale={args.width}:{args.height}:force_original_aspect_ratio=decrease,"
        f"pad={args.width}:{args.height}:(ow-iw)/2:(oh-ih)/2:color={args.background}"
    )
    command = ffmpeg_prefix(args.force)
    command += ["-i", source, "-vf", video_filter, "-map_metadata", "-1", "-frames:v", "1"]
    command += single_image_output_args(output)
    command.append(str(output))
    run_command(command, dry_run=args.dry_run)


def command_video_speed(args: argparse.Namespace) -> None:
    if not 0.1 <= args.factor <= 100:
        raise MediaError("--factor must be between 0.1 and 100")
    source = require_input(args.input)
    output = prepare_output(args.output, args.force, args.dry_run)
    data = probe_media(source)
    has_audio = has_stream(data, "audio")
    command = ffmpeg_prefix(args.force)
    command += ["-i", source, "-filter:v", f"setpts=PTS/{args.factor:.8g}"]
    if has_audio:
        command += ["-filter:a", atempo_chain(args.factor)]
    command += video_codec_args(output, with_audio=has_audio)
    command.append(str(output))
    run_command(command, dry_run=args.dry_run)


def command_video_volume(args: argparse.Namespace) -> None:
    if args.factor < 0:
        raise MediaError("--factor must be non-negative")
    source = require_input(args.input)
    output = prepare_output(args.output, args.force, args.dry_run)
    command = ffmpeg_prefix(args.force)
    command += ["-i", source, "-filter:a", f"volume={args.factor:.8g}"]
    command += video_codec_args(output)
    command.append(str(output))
    run_command(command, dry_run=args.dry_run)


def command_video_flip(args: argparse.Namespace) -> None:
    source = require_input(args.input)
    output = prepare_output(args.output, args.force, args.dry_run)
    command = ffmpeg_prefix(args.force)
    command += ["-i", source, "-vf", "hflip" if args.direction == "horizontal" else "vflip"]
    command += video_codec_args(output)
    command.append(str(output))
    run_command(command, dry_run=args.dry_run)


def command_video_filter(args: argparse.Namespace) -> None:
    source = require_input(args.input)
    output = prepare_output(args.output, args.force, args.dry_run)
    command = ffmpeg_prefix(args.force)
    command += ["-i", source, "-vf", VIDEO_PRESETS[args.preset]]
    command += video_codec_args(output)
    command.append(str(output))
    run_command(command, dry_run=args.dry_run)


def command_video_overlay(args: argparse.Namespace) -> None:
    video = require_input(args.input)
    image = require_input(args.image)
    output = prepare_output(args.output, args.force, args.dry_run)
    overlay = f"overlay=x={args.x}:y={args.y}"
    if args.start is not None or args.end is not None:
        start = args.start or 0.0
        end = args.end if args.end is not None else media_duration(video)
        overlay += f":enable='between(t,{start:.6f},{end:.6f})'"
    command = ffmpeg_prefix(args.force)
    command += ["-i", video, "-i", image, "-filter_complex", f"[0:v][1:v]{overlay}[v]"]
    command += ["-map", "[v]", "-map", "0:a?"]
    command += video_codec_args(output)
    command.append(str(output))
    run_command(command, dry_run=args.dry_run)


def command_video_subtitle(args: argparse.Namespace) -> None:
    require_ffmpeg_filter("subtitle burn-in", "subtitles")
    source = require_input(args.input)
    subtitle = require_input(args.subtitle)
    output = prepare_output(args.output, args.force, args.dry_run)
    video_filter = f"subtitles=filename={escape_filter_path(subtitle)}"
    if args.fonts_dir:
        fonts_dir = str(Path(args.fonts_dir).expanduser().resolve())
        if not Path(fonts_dir).is_dir():
            raise MediaError(f"Fonts directory not found: {fonts_dir}")
        video_filter += f":fontsdir={escape_filter_path(fonts_dir)}"
    command = ffmpeg_prefix(args.force)
    command += ["-i", source, "-vf", video_filter]
    command += video_codec_args(output)
    command.append(str(output))
    run_command(command, dry_run=args.dry_run)


def command_video_fade_audio(args: argparse.Namespace) -> None:
    source = require_input(args.input)
    output = prepare_output(args.output, args.force, args.dry_run)
    duration = media_duration(source)
    if min(args.fade_in, args.fade_out) < 0:
        raise MediaError("Fade durations must be non-negative")
    filters: list[str] = []
    if args.fade_in:
        filters.append(f"afade=t=in:st=0:d={args.fade_in:.6f}")
    if args.fade_out:
        filters.append(f"afade=t=out:st={duration - args.fade_out:.6f}:d={args.fade_out:.6f}")
    command = ffmpeg_prefix(args.force)
    command += ["-i", source]
    if filters:
        command += ["-filter:a", ",".join(filters)]
    command += video_codec_args(output)
    command.append(str(output))
    run_command(command, dry_run=args.dry_run)


def command_video_mux_audio(args: argparse.Namespace) -> None:
    video = require_input(args.input)
    audio = require_input(args.audio)
    output = prepare_output(args.output, args.force, args.dry_run)
    command = ffmpeg_prefix(args.force)
    command += ["-i", video, "-i", audio]
    if args.keep_original:
        command += [
            "-filter_complex",
            "[0:a][1:a]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=.95[a]",
            "-map",
            "0:v",
            "-map",
            "[a]",
        ]
    else:
        command += ["-map", "0:v", "-map", "1:a"]
    if args.shortest:
        command.append("-shortest")
    command += video_codec_args(output)
    command.append(str(output))
    run_command(command, dry_run=args.dry_run)


def command_video_mux_subtitle(args: argparse.Namespace) -> None:
    video = require_input(args.input)
    subtitle = require_input(args.subtitle)
    output = prepare_output(args.output, args.force, args.dry_run)
    suffix = output.suffix.lower()
    if suffix in {".mp4", ".m4v", ".mov"}:
        subtitle_codec = "mov_text"
    elif suffix == ".mkv":
        subtitle_codec = "srt"
    else:
        raise MediaError("Subtitle mux output must be .mp4, .m4v, .mov, or .mkv")

    command = ffmpeg_prefix(args.force)
    command += [
        "-i",
        video,
        "-i",
        subtitle,
        "-map",
        "0:v?",
        "-map",
        "0:a?",
        "-map",
        "1:0",
        "-map_metadata",
        "0",
        "-map_chapters",
        "0",
        "-c:v",
        "copy",
        "-c:a",
        "copy",
        "-c:s",
        subtitle_codec,
        "-metadata:s:s:0",
        f"language={args.language}",
        "-metadata:s:s:0",
        f"title={args.title}",
        "-disposition:s:0",
        "default",
        str(output),
    ]
    run_command(command, dry_run=args.dry_run)


def command_extract_audio(args: argparse.Namespace) -> None:
    source = require_input(args.input)
    output = prepare_output(args.output, args.force, args.dry_run)
    command = ffmpeg_prefix(args.force)
    command += ["-i", source, "-vn"]
    command += audio_codec_args(output)
    command.append(str(output))
    run_command(command, dry_run=args.dry_run)


def command_image_to_video(args: argparse.Namespace) -> None:
    source = require_input(args.input)
    output = prepare_output(args.output, args.force, args.dry_run)
    width, height = (int(value) for value in args.size.lower().split("x", 1))
    if min(width, height, args.fps) <= 0 or args.duration <= 0:
        raise MediaError("Size, fps, and duration must be positive")
    base = (
        f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
        f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color={args.background}"
    )
    if args.motion == "none":
        video_filter = base
    else:
        frames = max(1, round(args.duration * args.fps))
        if args.motion == "zoom-in":
            zoom = "min(zoom+0.0015,1.15)"
        else:
            zoom = "if(eq(on,1),1.15,max(1.0,zoom-0.0015))"
        video_filter = (
            f"{base},zoompan=z='{zoom}':d={frames}:s={width}x{height}:fps={args.fps}"
        )
    command = ffmpeg_prefix(args.force)
    command += [
        "-loop",
        "1",
        "-i",
        source,
        "-t",
        f"{args.duration:.6f}",
        "-vf",
        video_filter,
        "-r",
        str(args.fps),
        "-an",
    ]
    command += video_codec_args(output, with_audio=False)
    command.append(str(output))
    run_command(command, dry_run=args.dry_run)


def scene_boundaries(
    source: str,
    threshold: float,
    min_duration: float,
    max_duration: float | None,
) -> tuple[float, list[float]]:
    duration = media_duration(source)
    command = [
        require_command("ffmpeg"),
        "-hide_banner",
        "-nostdin",
        "-i",
        source,
        "-filter:v",
        f"select='gt(scene,{threshold})',showinfo",
        "-an",
        "-f",
        "null",
        "-",
    ]
    result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode != 0:
        raise MediaError(result.stderr.strip())
    candidates = [float(value) for value in re.findall(r"pts_time:([0-9.]+)", result.stderr)]
    boundaries = [0.0]
    for candidate in candidates:
        if candidate - boundaries[-1] >= min_duration and duration - candidate >= min_duration:
            boundaries.append(candidate)
    if max_duration:
        expanded = [boundaries[0]]
        for boundary in [*boundaries[1:], duration]:
            while boundary - expanded[-1] > max_duration:
                expanded.append(expanded[-1] + max_duration)
            if boundary < duration:
                expanded.append(boundary)
        boundaries = expanded
    boundaries.append(duration)
    return duration, sorted(set(round(value, 6) for value in boundaries))


def command_video_scenes(args: argparse.Namespace) -> None:
    if not 0 <= args.threshold <= 1:
        raise MediaError("--threshold must be between 0 and 1")
    if args.min_duration < 0:
        raise MediaError("--min-duration must be non-negative")
    source = require_input(args.input)
    output = prepare_output(args.output, args.force, args.dry_run)
    if args.dry_run:
        print(
            json.dumps(
                {
                    "operation": "scene-detection",
                    "input": source,
                    "threshold": args.threshold,
                    "min_duration": args.min_duration,
                    "max_duration": args.max_duration,
                },
                indent=2,
            )
        )
        return
    duration, boundaries = scene_boundaries(
        source,
        args.threshold,
        args.min_duration,
        args.max_duration,
    )
    scenes = [
        {
            "index": index,
            "start": start,
            "end": end,
            "duration": round(end - start, 6),
        }
        for index, (start, end) in enumerate(zip(boundaries, boundaries[1:]), start=1)
    ]
    payload = {
        "schema": "media-utils-scenes/v1",
        "source": source,
        "duration": duration,
        "threshold": args.threshold,
        "scenes": scenes,
    }
    write_json(output, payload, args.force)
    print(output)


def command_video_chroma_key(args: argparse.Namespace) -> None:
    source = require_input(args.input)
    output = prepare_output(args.output, args.force, args.dry_run)
    color = args.color.removeprefix("#").removeprefix("0x")
    if not re.fullmatch(r"[0-9A-Fa-f]{6}", color):
        raise MediaError("--color must be a six-digit hex color")
    if not 0 <= args.similarity <= 1 or not 0 <= args.blend <= 1:
        raise MediaError("--similarity and --blend must be between 0 and 1")
    require_ffmpeg_filter("chroma-key video", "chromakey")
    red, green, blue = (int(color[index : index + 2], 16) for index in (0, 2, 4))
    video_filter = f"chromakey=0x{color}:{args.similarity:.6f}:{args.blend:.6f}"
    if green >= max(red, blue):
        video_filter += ",despill=type=green"
    elif blue >= max(red, green):
        video_filter += ",despill=type=blue"
    has_audio = has_stream(probe_media(source), "audio")
    command = ffmpeg_prefix(args.force)
    command += ["-i", source, "-vf", video_filter]
    command += video_codec_args(output, alpha=True, with_audio=has_audio)
    command.append(str(output))
    run_command(command, dry_run=args.dry_run)


def command_dialogue_transcribe(args: argparse.Namespace) -> None:
    source = require_input(args.input)
    output = prepare_output(args.output, args.force, args.dry_run)
    bl = require_command("bl")
    if output.exists() and args.force and not args.dry_run:
        output.unlink()
    command = [bl, "speech", "recognize", "--url", source, "--out", str(output)]
    if args.language:
        command += ["--language", args.language]
    if args.diarization:
        command.append("--diarization")
    if args.speaker_count:
        if not args.diarization:
            raise MediaError("--speaker-count requires --diarization")
        command += ["--speaker-count", str(args.speaker_count)]
    env = dict(os.environ)
    env["NO_COLOR"] = "1"
    run_command(command, dry_run=args.dry_run, env=env)


def normalize_token(value: str) -> str:
    return re.sub(r"[\s\W_]+", "", value, flags=re.UNICODE).casefold()


def transcript_words(data: Any) -> list[dict[str, Any]]:
    documents = data if isinstance(data, list) else [data]
    words: list[dict[str, Any]] = []
    for document in documents:
        for transcript in document.get("transcripts", []):
            for sentence in transcript.get("sentences", []):
                speaker = sentence.get("speaker_id")
                for word in sentence.get("words", []):
                    if "begin_time" not in word or "end_time" not in word:
                        continue
                    words.append(
                        {
                            "begin_ms": int(word["begin_time"]),
                            "end_ms": int(word["end_time"]),
                            "text": str(word.get("text", "")),
                            "punctuation": str(word.get("punctuation", "")),
                            "speaker_id": speaker,
                        }
                    )
    return sorted(words, key=lambda item: (item["begin_ms"], item["end_ms"]))


def transcript_sentences(data: Any) -> list[dict[str, Any]]:
    documents = data if isinstance(data, list) else [data]
    sentences: list[dict[str, Any]] = []
    for document in documents:
        for transcript in document.get("transcripts", []):
            for sentence in transcript.get("sentences", []):
                words = [
                    {
                        "begin_ms": int(word["begin_time"]),
                        "end_ms": int(word["end_time"]),
                        "text": str(word.get("text", "")),
                        "punctuation": str(word.get("punctuation", "")),
                    }
                    for word in sentence.get("words", [])
                    if "begin_time" in word and "end_time" in word
                ]
                if not words:
                    continue
                sentences.append(
                    {
                        "begin_ms": int(sentence.get("begin_time", words[0]["begin_ms"])),
                        "end_ms": int(sentence.get("end_time", words[-1]["end_ms"])),
                        "text": str(sentence.get("text", "")),
                        "speaker_id": sentence.get("speaker_id"),
                        "words": words,
                    }
                )
    return sorted(sentences, key=lambda item: (item["begin_ms"], item["end_ms"]))


def merged_removals(items: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    ordered = sorted(items, key=lambda item: (item["start"], item["end"]))
    merged: list[dict[str, Any]] = []
    for item in ordered:
        if item["end"] <= item["start"]:
            continue
        if merged and item["start"] <= merged[-1]["end"]:
            merged[-1]["end"] = max(merged[-1]["end"], item["end"])
            reasons = set(merged[-1].get("reasons", [merged[-1].get("reason", "edit")]))
            reasons.add(item.get("reason", "edit"))
            merged[-1]["reasons"] = sorted(reasons)
            merged[-1].pop("reason", None)
        else:
            merged.append(dict(item))
    for item in merged:
        item["start"] = round(float(item["start"]), 6)
        item["end"] = round(float(item["end"]), 6)
    return merged


def mono_pcm_samples(input_value: str, sample_rate: int = 16000) -> tuple[array.array, int]:
    source = require_input(input_value)
    with tempfile.TemporaryDirectory(prefix="media-utils-pcm-") as directory:
        wav_path = Path(directory) / "audio.wav"
        run_command(
            [
                require_command("ffmpeg"),
                "-hide_banner",
                "-loglevel",
                "error",
                "-nostdin",
                "-y",
                "-i",
                source,
                "-vn",
                "-ar",
                str(sample_rate),
                "-ac",
                "1",
                "-c:a",
                "pcm_s16le",
                str(wav_path),
            ]
        )
        with wave.open(str(wav_path), "rb") as wav:
            samples = array.array("h", wav.readframes(wav.getnframes()))
            if sys.byteorder != "little":
                samples.byteswap()
            return samples, wav.getframerate()


def lowest_energy_time(
    samples: array.array,
    sample_rate: int,
    start: float,
    end: float,
    *,
    window_ms: int = 6,
) -> float:
    if end <= start:
        return start
    radius = max(1, round(window_ms * sample_rate / 2000))
    step = max(1, round(sample_rate / 1000))
    first = max(radius, round(start * sample_rate))
    last = min(len(samples) - radius - 1, round(end * sample_rate))
    if last <= first:
        return start
    best_index = first
    best_score = math.inf
    for index in range(first, last + 1, step):
        window = samples[index - radius : index + radius + 1]
        mean_square = sum(value * value for value in window) / len(window)
        score = mean_square + samples[index] * samples[index]
        if score < best_score:
            best_score = score
            best_index = index
    return best_index / sample_rate


def refine_removal_boundaries(
    input_value: str,
    removals: list[dict[str, Any]],
    search_ms: int,
) -> list[dict[str, Any]]:
    if search_ms <= 0 or not removals:
        return removals
    samples, sample_rate = mono_pcm_samples(input_value)
    search = search_ms / 1000
    minimum_cut = 0.03
    refined: list[dict[str, Any]] = []
    for item in removals:
        original_start = float(item["start"])
        original_end = float(item["end"])
        start_limit = min(original_end - minimum_cut, original_start + search)
        end_limit = max(original_start + minimum_cut, original_end - search)
        new_start = lowest_energy_time(
            samples, sample_rate, original_start, max(original_start, start_limit)
        )
        new_end = lowest_energy_time(
            samples, sample_rate, min(original_end, end_limit), original_end
        )
        updated = dict(item)
        if new_end - new_start >= minimum_cut:
            updated["start"] = round(new_start, 6)
            updated["end"] = round(new_end, 6)
            updated["boundary_adjustment"] = {
                "original_start": round(original_start, 6),
                "original_end": round(original_end, 6),
                "search_ms": search_ms,
            }
        refined.append(updated)
    return merged_removals(refined)


def parse_ai_cleanup_json(value: str) -> dict[str, Any]:
    text = value.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text)
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        start = text.find("{")
        end = text.rfind("}")
        if start < 0 or end <= start:
            raise MediaError("AI cleanup response did not contain a JSON object") from exc
        try:
            payload = json.loads(text[start : end + 1])
        except json.JSONDecodeError as nested:
            raise MediaError("AI cleanup response contained invalid JSON") from nested
    if not isinstance(payload, dict):
        raise MediaError("AI cleanup response must be a JSON object")
    return payload


def ai_cleanup_system_prompt(level: str) -> str:
    level_guidance = {
        "conservative": (
            "Delete only unmistakably dispensable vocal fillers, verbal tics, "
            "self-confirmations, false starts, or accidental exact repetitions. "
            "When uncertain, keep the words."
        ),
        "balanced": (
            "Also allow short discourse markers, speech repairs, and redundant "
            "rephrases when removing them preserves the speaker's complete meaning."
        ),
        "aggressive": (
            "Also allow clearly redundant clauses and low-information speech, but "
            "preserve every distinct fact, stance, decision, question, and action."
        ),
    }[level]
    return (
        "You are a multilingual spoken-dialogue cleanup classifier. "
        "The input contains ASR words with immutable integer IDs, timestamps, speakers, "
        "and a core ID range. Decide which existing consecutive word IDs can be removed "
        "without changing meaning. Never invent IDs or timestamps. Never cross speakers. "
        "Preserve names, numbers, dates, negation, uncertainty, questions, answers, "
        "agreements with another speaker, disagreements, decisions, commitments, action "
        "items, and technical terms. A word such as 对/yes/right may be removed only when "
        "it is clearly the current speaker's self-confirmation or stalling device, not a "
        "response to another person. Only return decisions whose first word ID is inside "
        "the core range. "
        + level_guidance
        + ' Return JSON only: {"decisions":[{"word_ids":[1],"category":"filler",'
        '"confidence":0.98,"reason":"brief explanation"}]}. '
        "Use only the allowed categories supplied by the user payload."
    )


def run_ai_cleanup_chunk(
    *,
    words: list[dict[str, Any]],
    core_start_id: int,
    core_end_id: int,
    args: argparse.Namespace,
    allowed_categories: Sequence[str],
) -> tuple[list[dict[str, Any]], str]:
    bl = require_command("bl")
    payload = {
        "task": "select_semantically_dispensable_spoken_words",
        "level": args.ai_level,
        "core_id_range": [core_start_id, core_end_id],
        "allowed_categories": list(allowed_categories),
        "filler_hints": list(args.filler or []),
        "exact_repetition_max_gap_ms": args.repetition_gap_ms,
        "words": [
            {
                "id": word["id"],
                "text": word["text"],
                "punctuation": word.get("punctuation", ""),
                "speaker": word.get("speaker_id"),
                "begin_ms": word["begin_ms"],
                "end_ms": word["end_ms"],
            }
            for word in words
        ],
    }
    command = [
        bl,
        "text",
        "chat",
        "--model",
        args.ai_model,
        "--system",
        ai_cleanup_system_prompt(args.ai_level),
        "--message",
        json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
        "--temperature",
        "0.1",
        "--max-tokens",
        "4096",
        "--output",
        "json",
        "--quiet",
    ]
    env = dict(os.environ)
    env["NO_COLOR"] = "1"
    last_error: MediaError | None = None
    for _ in range(2):
        result = run_command(command, capture=True, env=env)
        raw = result.stdout.strip()
        try:
            response = parse_ai_cleanup_json(raw)
            decisions = response.get("decisions", [])
            if not isinstance(decisions, list):
                raise MediaError("AI cleanup response field 'decisions' must be an array")
            return decisions, raw
        except MediaError as exc:
            last_error = exc
    raise last_error or MediaError("AI cleanup response could not be parsed")


def ai_cleanup_decisions(
    words: list[dict[str, Any]],
    args: argparse.Namespace,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    level = AI_CLEANUP_LEVELS[args.ai_level]
    minimum_confidence = (
        args.ai_min_confidence
        if args.ai_min_confidence is not None
        else level["min_confidence"]
    )
    if not 0 <= minimum_confidence <= 1:
        raise MediaError("--ai-min-confidence must be between 0 and 1")
    if args.ai_chunk_words < 50:
        raise MediaError("--ai-chunk-words must be at least 50")
    if args.ai_context_words < 0 or args.ai_context_words >= args.ai_chunk_words:
        raise MediaError("--ai-context-words must be non-negative and smaller than the chunk")

    indexed_words = [
        {**word, "id": index}
        for index, word in enumerate(words, start=1)
    ]
    by_id = {word["id"]: word for word in indexed_words}
    allowed_categories = set(level["categories"])
    if not args.remove_repetitions:
        allowed_categories.discard("exact_repeat")
    allowed_categories.difference_update(args.ai_exclude_category or [])
    if not allowed_categories:
        raise MediaError("AI cleanup has no allowed categories after exclusions")

    candidates: dict[tuple[int, ...], dict[str, Any]] = {}
    raw_chunks: list[dict[str, Any]] = []
    total = len(indexed_words)
    for core_start_index in range(0, total, args.ai_chunk_words):
        core_end_index = min(total, core_start_index + args.ai_chunk_words)
        context_start = max(0, core_start_index - args.ai_context_words)
        context_end = min(total, core_end_index + args.ai_context_words)
        chunk_words = indexed_words[context_start:context_end]
        core_start_id = core_start_index + 1
        core_end_id = core_end_index
        decisions, raw = run_ai_cleanup_chunk(
            words=chunk_words,
            core_start_id=core_start_id,
            core_end_id=core_end_id,
            args=args,
            allowed_categories=sorted(allowed_categories),
        )
        raw_chunks.append(
            {
                "core_id_range": [core_start_id, core_end_id],
                "context_id_range": [
                    chunk_words[0]["id"],
                    chunk_words[-1]["id"],
                ],
                "response": raw,
            }
        )
        context_ids = {word["id"] for word in chunk_words}
        for decision in decisions:
            if not isinstance(decision, dict):
                continue
            raw_ids = decision.get("word_ids")
            if not isinstance(raw_ids, list) or not raw_ids:
                key = tuple()
            else:
                try:
                    key = tuple(int(value) for value in raw_ids)
                except (TypeError, ValueError):
                    key = tuple()
            annotated = {
                **decision,
                "word_ids": list(key),
                "_core_id_range": [core_start_id, core_end_id],
                "_context_ids": sorted(context_ids),
            }
            existing = candidates.get(key)
            try:
                confidence = float(decision.get("confidence", 0))
                existing_confidence = (
                    float(existing.get("confidence", 0)) if existing else -1
                )
            except (TypeError, ValueError):
                confidence = -1
                existing_confidence = -1
            if existing is None or confidence > existing_confidence:
                candidates[key] = annotated

    def is_adjacent_exact_repeat(ids: tuple[int, ...]) -> bool:
        if not ids:
            return False
        selected = [by_id[value] for value in ids]
        signature = [normalize_token(word["text"]) for word in selected]
        if not all(signature):
            return False
        length = len(ids)
        first_index = ids[0] - 1
        last_index = ids[-1] - 1
        neighbors: list[tuple[list[dict[str, Any]], int]] = []
        if first_index >= length:
            previous = indexed_words[first_index - length : first_index]
            gap = selected[0]["begin_ms"] - previous[-1]["end_ms"]
            neighbors.append((previous, gap))
        if last_index + length < total:
            following = indexed_words[last_index + 1 : last_index + 1 + length]
            gap = following[0]["begin_ms"] - selected[-1]["end_ms"]
            neighbors.append((following, gap))
        for neighbor, gap in neighbors:
            if gap > args.repetition_gap_ms:
                continue
            if len({word.get("speaker_id") for word in [*selected, *neighbor]}) != 1:
                continue
            if [normalize_token(word["text"]) for word in neighbor] == signature:
                return True
        return False

    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    for ids, decision in candidates.items():
        rejection: str | None = None
        category = str(decision.get("category", "")).strip().casefold()
        try:
            confidence = float(decision.get("confidence", 0))
        except (TypeError, ValueError):
            confidence = -1
        core_start_id, core_end_id = decision["_core_id_range"]
        context_ids = set(decision["_context_ids"])
        selected = [by_id[value] for value in ids if value in by_id]
        if not ids:
            rejection = "missing-word-ids"
        elif list(ids) != sorted(set(ids)) or any(
            right != left + 1 for left, right in zip(ids, ids[1:])
        ):
            rejection = "word-ids-must-be-unique-consecutive-and-sorted"
        elif any(value not in context_ids or value not in by_id for value in ids):
            rejection = "unknown-or-out-of-context-word-id"
        elif not core_start_id <= ids[0] <= core_end_id:
            rejection = "first-word-outside-core-range"
        elif category not in allowed_categories:
            rejection = "category-not-allowed-at-this-level"
        elif confidence < minimum_confidence:
            rejection = "confidence-below-threshold"
        elif len(ids) > int(level["max_tokens"]):
            rejection = "too-many-words"
        elif len({word.get("speaker_id") for word in selected}) != 1:
            rejection = "cross-speaker-removal"
        elif selected and (
            selected[-1]["end_ms"] - selected[0]["begin_ms"]
        ) / 1000 > float(level["max_span_seconds"]):
            rejection = "span-too-long"
        elif any(re.search(r"\d", word["text"]) for word in selected):
            rejection = "contains-number"
        elif any(
            normalize_token(word["text"]) in AI_PROTECTED_NEGATIONS for word in selected
        ):
            rejection = "contains-protected-negation"
        elif category == "exact_repeat" and not is_adjacent_exact_repeat(ids):
            rejection = "not-an-adjacent-exact-repeat"
        elif selected and args.min_neighbor_gap_ms:
            first_index = ids[0] - 1
            last_index = ids[-1] - 1
            left_gap = (
                selected[0]["begin_ms"] - indexed_words[first_index - 1]["end_ms"]
                if first_index > 0
                else math.inf
            )
            right_gap = (
                indexed_words[last_index + 1]["begin_ms"] - selected[-1]["end_ms"]
                if last_index + 1 < total
                else math.inf
            )
            if (
                left_gap < args.min_neighbor_gap_ms
                or right_gap < args.min_neighbor_gap_ms
            ):
                rejection = "too-close-to-neighboring-speech"

        public_decision = {
            key: value
            for key, value in decision.items()
            if not key.startswith("_")
        }
        if rejection:
            rejected.append({**public_decision, "rejection": rejection})
            continue
        text = "".join(
            f"{word['text']}{word.get('punctuation', '')}" for word in selected
        )
        accepted_decision = {
            **public_decision,
            "category": category,
            "confidence": confidence,
            "text": text,
        }
        accepted.append(accepted_decision)

    removals: list[dict[str, Any]] = []
    accepted_by_ids = {tuple(item["word_ids"]): item for item in accepted}
    for ids, decision in accepted_by_ids.items():
        selected = [by_id[value] for value in ids]
        removals.append(
            {
                "start": selected[0]["begin_ms"] / 1000,
                "end": selected[-1]["end_ms"] / 1000,
                "reason": f"ai:{decision['category']}",
                "text": "".join(
                    f"{word['text']}{word.get('punctuation', '')}" for word in selected
                ),
                "speaker_id": selected[0].get("speaker_id"),
                "ai_decision": {
                    "word_ids": list(ids),
                    "category": decision["category"],
                    "confidence": decision["confidence"],
                    "reason": str(decision.get("reason", "")),
                },
            }
        )
    report = {
        "schema": "media-utils-ai-cleanup-decisions/v1",
        "model": args.ai_model,
        "level": args.ai_level,
        "constraints": {
            "min_confidence": minimum_confidence,
            "max_tokens": level["max_tokens"],
            "max_span_seconds": level["max_span_seconds"],
            "allowed_categories": sorted(allowed_categories),
            "min_neighbor_gap_ms": args.min_neighbor_gap_ms,
        },
        "chunk_count": len(raw_chunks),
        "words": [
            {
                "id": word["id"],
                "text": word["text"],
                "punctuation": word.get("punctuation", ""),
                "speaker_id": word.get("speaker_id"),
                "begin_ms": word["begin_ms"],
                "end_ms": word["end_ms"],
            }
            for word in indexed_words
        ],
        "accepted": accepted,
        "rejected": rejected,
        "chunks": raw_chunks,
    }
    return removals, report


def command_dialogue_plan(args: argparse.Namespace) -> None:
    transcript_path = Path(args.transcript).expanduser().resolve()
    if not transcript_path.is_file():
        raise MediaError(f"Transcript not found: {transcript_path}")
    output = prepare_output(args.output, args.force, args.dry_run)
    data = json.loads(transcript_path.read_text(encoding="utf-8"))
    words = transcript_words(data)
    if not words:
        raise MediaError("No word-level timestamps found in transcript")
    if args.min_neighbor_gap_ms < 0:
        raise MediaError("--min-neighbor-gap-ms must be non-negative")
    if args.boundary_search_ms < 0:
        raise MediaError("--boundary-search-ms must be non-negative")
    if args.boundary_search_ms and not args.media:
        raise MediaError("--boundary-search-ms requires --media")
    if args.cleanup_mode != "ai" and args.ai_decisions_output:
        raise MediaError("--ai-decisions-output requires --cleanup-mode ai")
    ai_decisions_output = (
        prepare_output(args.ai_decisions_output, args.force, args.dry_run)
        if args.ai_decisions_output
        else None
    )
    fillers = list(args.filler or [])
    if args.use_default_fillers and args.cleanup_mode == "exact":
        fillers.extend(DEFAULT_FILLERS)
    if args.cleanup_mode == "ai" and args.dry_run:
        payload = {
            "operation": "dialogue-plan",
            "cleanup_mode": "ai",
            "transcript": str(transcript_path),
            "output": str(output),
            "ai_decisions_output": (
                str(ai_decisions_output) if ai_decisions_output else None
            ),
            "word_count": len(words),
            "ai_model": args.ai_model,
            "ai_level": args.ai_level,
            "ai_min_confidence": args.ai_min_confidence,
            "ai_chunk_words": args.ai_chunk_words,
            "ai_context_words": args.ai_context_words,
            "ai_exclude_categories": args.ai_exclude_category or [],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    normalized_fillers = []
    for filler in fillers:
        tokens = [normalize_token(token) for token in filler.split() if normalize_token(token)]
        if not tokens:
            continue
        normalized_fillers.append((filler, tokens))
    normalized_words = [normalize_token(word["text"]) for word in words]
    removals: list[dict[str, Any]] = []
    matched_indices: set[int] = set()
    skipped_tight_fillers = 0
    ai_report: dict[str, Any] | None = None
    if args.cleanup_mode == "exact":
        for label, tokens in normalized_fillers:
            for index in range(0, len(words) - len(tokens) + 1):
                if any(
                    position in matched_indices
                    for position in range(index, index + len(tokens))
                ):
                    continue
                if normalized_words[index : index + len(tokens)] == tokens:
                    first = words[index]
                    last = words[index + len(tokens) - 1]
                    left_gap = (
                        first["begin_ms"] - words[index - 1]["end_ms"]
                        if index > 0
                        else math.inf
                    )
                    right_index = index + len(tokens)
                    right_gap = (
                        words[right_index]["begin_ms"] - last["end_ms"]
                        if right_index < len(words)
                        else math.inf
                    )
                    if args.min_neighbor_gap_ms and (
                        left_gap < args.min_neighbor_gap_ms
                        or right_gap < args.min_neighbor_gap_ms
                    ):
                        skipped_tight_fillers += 1
                        continue
                    removals.append(
                        {
                            "start": max(
                                0.0, (first["begin_ms"] - args.padding_ms) / 1000
                            ),
                            "end": (last["end_ms"] + args.padding_ms) / 1000,
                            "reason": "filler",
                            "text": label,
                            "speaker_id": first.get("speaker_id"),
                        }
                    )
                    matched_indices.update(range(index, index + len(tokens)))
    else:
        ai_removals, ai_report = ai_cleanup_decisions(words, args)
        removals.extend(ai_removals)
        skipped_tight_fillers = sum(
            item.get("rejection") == "too-close-to-neighboring-speech"
            for item in ai_report["rejected"]
        )
    if args.max_pause_ms is not None:
        if args.keep_pause_ms < 0 or args.keep_pause_ms >= args.max_pause_ms:
            raise MediaError("--keep-pause-ms must be non-negative and smaller than --max-pause-ms")
        for previous, current in zip(words, words[1:]):
            gap = current["begin_ms"] - previous["end_ms"]
            same_speaker = previous.get("speaker_id") == current.get("speaker_id")
            if gap > args.max_pause_ms and same_speaker:
                removals.append(
                    {
                        "start": (previous["end_ms"] + args.keep_pause_ms) / 1000,
                        "end": current["begin_ms"] / 1000,
                        "reason": "excess-pause",
                        "speaker_id": previous.get("speaker_id"),
                        "original_pause_ms": gap,
                    }
                )
    if args.cleanup_mode == "exact" and args.remove_repetitions:
        for index, (previous, current) in enumerate(zip(words, words[1:])):
            if index in matched_indices:
                continue
            repeated = (
                normalized_words[index]
                and normalized_words[index] == normalized_words[index + 1]
            )
            same_speaker = previous.get("speaker_id") == current.get("speaker_id")
            gap = current["begin_ms"] - previous["end_ms"]
            if repeated and same_speaker and gap <= args.repetition_gap_ms:
                removals.append(
                    {
                        "start": previous["begin_ms"] / 1000,
                        "end": previous["end_ms"] / 1000,
                        "reason": "repetition",
                        "text": previous["text"].strip(),
                        "speaker_id": previous.get("speaker_id"),
                    }
                )
    merged = merged_removals(removals)
    if args.media:
        merged = refine_removal_boundaries(
            require_input(args.media), merged, args.boundary_search_ms
        )
    payload = {
        "schema": "media-utils-edit-plan/v1",
        "approved": False,
        "transcript": str(transcript_path),
        "transcript_sha256": hashlib.sha256(transcript_path.read_bytes()).hexdigest(),
        "analysis": {
            "word_count": len(words),
            "cleanup_mode": args.cleanup_mode,
            "fillers": fillers,
            "padding_ms": args.padding_ms,
            "max_pause_ms": args.max_pause_ms,
            "keep_pause_ms": args.keep_pause_ms,
            "remove_repetitions": args.remove_repetitions,
            "repetition_gap_ms": args.repetition_gap_ms,
            "min_neighbor_gap_ms": args.min_neighbor_gap_ms,
            "skipped_tight_fillers": skipped_tight_fillers,
            "media": str(Path(args.media).expanduser().resolve()) if args.media else None,
            "boundary_search_ms": args.boundary_search_ms,
            "ai": (
                {
                    "model": ai_report["model"],
                    "level": ai_report["level"],
                    "constraints": ai_report["constraints"],
                    "chunk_count": ai_report["chunk_count"],
                    "accepted_count": len(ai_report["accepted"]),
                    "rejected_count": len(ai_report["rejected"]),
                    "decisions_output": (
                        str(ai_decisions_output) if ai_decisions_output else None
                    ),
                }
                if ai_report
                else None
            ),
        },
        "remove": merged,
    }
    if args.dry_run:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    if ai_report and ai_decisions_output:
        write_json(ai_decisions_output, ai_report, args.force)
    write_json(output, payload, args.force)
    print(output)


def keep_intervals(duration: float, removals: list[dict[str, Any]]) -> list[tuple[float, float]]:
    clamped = []
    for item in removals:
        start = max(0.0, min(duration, float(item["start"])))
        end = max(0.0, min(duration, float(item["end"])))
        if end > start:
            clamped.append({"start": start, "end": end, "reason": item.get("reason", "edit")})
    merged = merged_removals(clamped)
    keep: list[tuple[float, float]] = []
    cursor = 0.0
    for item in merged:
        if item["start"] > cursor:
            keep.append((cursor, float(item["start"])))
        cursor = max(cursor, float(item["end"]))
    if cursor < duration:
        keep.append((cursor, duration))
    return [(start, end) for start, end in keep if end - start > 0.001]


def stream_duration(data: dict[str, Any], codec_type: str, fallback: float) -> float:
    values = [
        float(stream["duration"])
        for stream in data.get("streams", [])
        if stream.get("codec_type") == codec_type and stream.get("duration") is not None
    ]
    return max(values) if values else fallback


def kept_video_frame_duration(
    source: str, keep: list[tuple[float, float]]
) -> float:
    result = run_command(
        [
            require_command("ffprobe"),
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_frames",
            "-show_entries",
            "frame=best_effort_timestamp_time,pkt_duration_time",
            "-of",
            "json",
            source,
        ],
        capture=True,
    )
    frames = json.loads(result.stdout).get("frames", [])
    timed: list[tuple[float, float | None]] = []
    for frame in frames:
        timestamp = frame.get("best_effort_timestamp_time")
        if timestamp is None:
            continue
        duration = frame.get("pkt_duration_time")
        timed.append((float(timestamp), float(duration) if duration is not None else None))
    if not timed:
        raise MediaError("Could not inspect video frame timestamps for smooth dialogue edit")
    origin = timed[0][0]
    normalized = [(timestamp - origin, duration) for timestamp, duration in timed]
    inferred = [
        next_timestamp - timestamp
        for (timestamp, _), (next_timestamp, _) in zip(normalized, normalized[1:])
        if next_timestamp > timestamp
    ]
    fallback_duration = sorted(inferred)[len(inferred) // 2] if inferred else 1 / 30
    total = 0.0
    for start, end in keep:
        selected = [
            (timestamp, duration)
            for timestamp, duration in normalized
            if start <= timestamp < end
        ]
        if not selected:
            continue
        first_timestamp = selected[0][0]
        last_timestamp, last_duration = selected[-1]
        total += last_timestamp - first_timestamp + (last_duration or fallback_duration)
    if total <= 0:
        raise MediaError("Edit plan retained no video frames")
    return total


def command_dialogue_apply_smooth(
    args: argparse.Namespace,
    source: str,
    output: Path,
    data: dict[str, Any],
    duration: float,
    removals: list[dict[str, Any]],
) -> None:
    video = has_stream(data, "video")
    audio = has_stream(data, "audio")
    if not audio:
        raise MediaError("--smooth requires an audio stream")
    keep = keep_intervals(duration, removals)
    if not keep:
        raise MediaError("Edit plan would remove the entire file")
    crossfade = args.crossfade_ms / 1000
    if crossfade < 0:
        raise MediaError("--crossfade-ms must be non-negative")
    if crossfade and any(end - start <= crossfade for start, end in keep):
        raise MediaError("--crossfade-ms must be shorter than every retained interval")

    filters: list[str] = []
    if video:
        for index, (start, end) in enumerate(keep):
            filters.append(
                f"[0:v]setpts=PTS-STARTPTS,trim=start={start:.6f}:end={end:.6f},"
                f"setpts=PTS-STARTPTS[v{index}]"
            )
        video_inputs = "".join(f"[v{index}]" for index in range(len(keep)))
        filters.append(f"{video_inputs}concat=n={len(keep)}:v=1:a=0[vcat]")

    audio_duration = stream_duration(data, "audio", duration)
    audio_keep = [
        (start, min(end, audio_duration))
        for start, end in keep
        if start < audio_duration and min(end, audio_duration) - start > 0.001
    ]
    if len(audio_keep) != len(keep):
        raise MediaError("Audio and video retained interval counts differ")
    for index, (start, end) in enumerate(audio_keep):
        filters.append(
            f"[0:a]asetpts=PTS-STARTPTS,atrim=start={start:.6f}:end={end:.6f},"
            f"asetpts=PTS-STARTPTS[a{index}]"
        )
    if len(audio_keep) == 1:
        audio_label = "a0"
    elif crossfade:
        previous = "a0"
        for index in range(1, len(audio_keep)):
            current = f"ax{index}"
            filters.append(
                f"[{previous}][a{index}]acrossfade=d={crossfade:.6f}:"
                f"c1=qsin:c2=qsin[{current}]"
            )
            previous = current
        audio_label = previous
    else:
        audio_inputs = "".join(f"[a{index}]" for index in range(len(audio_keep)))
        filters.append(f"{audio_inputs}concat=n={len(audio_keep)}:v=0:a=1[acat]")
        audio_label = "acat"

    target_audio_duration = sum(end - start for start, end in audio_keep)
    target_audio_duration -= crossfade * max(0, len(audio_keep) - 1)
    video_label = None
    if video:
        raw_video_duration = kept_video_frame_duration(source, keep)
        video_scale = target_audio_duration / raw_video_duration
        filters.append(f"[vcat]setpts=PTS*{video_scale:.12f}[vsync]")
        video_label = "vsync"

    command = ffmpeg_prefix(args.force)
    command += ["-i", source, "-filter_complex", ";".join(filters)]
    if video_label:
        command += ["-map", f"[{video_label}]"]
    command += ["-map", f"[{audio_label}]"]
    command += (
        video_codec_args(output, with_audio=True)
        if video
        else audio_codec_args(output)
    )
    if video:
        command.append("-shortest")
    command.append(str(output))
    run_command(command, dry_run=args.dry_run)


def command_dialogue_apply(args: argparse.Namespace) -> None:
    if not args.approve:
        raise MediaError("Refusing to edit without --approve; review the plan first")
    source = require_input(args.input)
    plan_path = Path(args.plan).expanduser().resolve()
    if not plan_path.is_file():
        raise MediaError(f"Plan not found: {plan_path}")
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    if plan.get("schema") != "media-utils-edit-plan/v1":
        raise MediaError("Unsupported edit plan schema")
    removals = plan.get("remove", [])
    if not removals:
        raise MediaError("Edit plan contains no removal intervals")
    output = prepare_output(args.output, args.force, args.dry_run)
    data = probe_media(source)
    duration = media_duration(source)
    if args.smooth:
        command_dialogue_apply_smooth(
            args, source, output, data, duration, removals
        )
        return
    keep = keep_intervals(duration, removals)
    if not keep:
        raise MediaError("Edit plan would remove the entire file")
    video = has_stream(data, "video")
    audio = has_stream(data, "audio")
    if not audio and not video:
        raise MediaError("Input has no audio or video stream")
    filters: list[str] = []
    if video:
        for index, (start, end) in enumerate(keep):
            filters.append(
                f"[0:v]trim=start={start:.6f}:end={end:.6f},setpts=PTS-STARTPTS[v{index}]"
            )
    if audio:
        for index, (start, end) in enumerate(keep):
            filters.append(
                f"[0:a]atrim=start={start:.6f}:end={end:.6f},asetpts=PTS-STARTPTS[a{index}]"
            )
    if video and audio:
        inputs = "".join(f"[v{index}][a{index}]" for index in range(len(keep)))
        filters.append(f"{inputs}concat=n={len(keep)}:v=1:a=1[v][a]")
    elif video:
        inputs = "".join(f"[v{index}]" for index in range(len(keep)))
        filters.append(f"{inputs}concat=n={len(keep)}:v=1:a=0[v]")
    else:
        inputs = "".join(f"[a{index}]" for index in range(len(keep)))
        filters.append(f"{inputs}concat=n={len(keep)}:v=0:a=1[a]")
    command = ffmpeg_prefix(args.force)
    command += ["-i", source, "-filter_complex", ";".join(filters)]
    if video:
        command += ["-map", "[v]"]
    if audio:
        command += ["-map", "[a]"]
    command += (
        video_codec_args(output, with_audio=audio) if video else audio_codec_args(output)
    )
    command.append(str(output))
    run_command(command, dry_run=args.dry_run)


def removal_intervals(plan: dict[str, Any]) -> list[dict[str, Any]]:
    return merged_removals(
        {
            "start": max(0.0, float(item["start"])),
            "end": max(0.0, float(item["end"])),
            "reason": item.get("reason", "edit"),
        }
        for item in plan.get("remove", [])
    )


def remap_time(seconds: float, removals: list[dict[str, Any]]) -> float:
    removed = 0.0
    for item in removals:
        start = float(item["start"])
        end = float(item["end"])
        if seconds >= end:
            removed += end - start
        elif seconds > start:
            removed += seconds - start
            break
        else:
            break
    return max(0.0, seconds - removed)


def word_is_removed(word: dict[str, Any], removals: list[dict[str, Any]]) -> bool:
    start = word["begin_ms"] / 1000
    end = word["end_ms"] / 1000
    return any(start < float(item["end"]) and end > float(item["start"]) for item in removals)


def srt_timestamp(seconds: float) -> str:
    milliseconds = max(0, round(seconds * 1000))
    hours, remainder = divmod(milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    whole_seconds, milliseconds = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{whole_seconds:02d},{milliseconds:03d}"


def command_dialogue_srt(args: argparse.Namespace) -> None:
    transcript_path = Path(args.transcript).expanduser().resolve()
    if not transcript_path.is_file():
        raise MediaError(f"Transcript not found: {transcript_path}")
    output = prepare_output(args.output, args.force, args.dry_run)
    transcript_data = json.loads(transcript_path.read_text(encoding="utf-8"))
    sentences = transcript_sentences(transcript_data)
    if not sentences:
        raise MediaError("No sentence-level word timestamps found in transcript")
    removals: list[dict[str, Any]] = []
    if args.plan:
        plan_path = Path(args.plan).expanduser().resolve()
        if not plan_path.is_file():
            raise MediaError(f"Plan not found: {plan_path}")
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        if plan.get("schema") != "media-utils-edit-plan/v1":
            raise MediaError("Unsupported edit plan schema")
        expected_hash = plan.get("transcript_sha256")
        actual_hash = hashlib.sha256(transcript_path.read_bytes()).hexdigest()
        if expected_hash and expected_hash != actual_hash:
            raise MediaError("Edit plan was generated from a different transcript")
        removals = removal_intervals(plan)

    speaker_numbers: dict[Any, int] = {}
    cues: list[dict[str, Any]] = []
    for sentence in sentences:
        kept_words = [
            word for word in sentence["words"] if not word_is_removed(word, removals)
        ]
        if not kept_words:
            continue
        text = "".join(
            f"{word['text']}{word['punctuation']}" for word in kept_words
        ).strip()
        if not text:
            continue
        speaker = sentence.get("speaker_id")
        if speaker not in speaker_numbers:
            speaker_numbers[speaker] = len(speaker_numbers) + 1
        start = remap_time(kept_words[0]["begin_ms"] / 1000, removals)
        end = remap_time(kept_words[-1]["end_ms"] / 1000, removals)
        if end <= start:
            end = start + 0.08
        cues.append(
            {
                "start": start,
                "end": end,
                "text": f"{args.speaker_prefix}{speaker_numbers[speaker]}：{text}",
            }
        )

    if args.dry_run:
        print(
            json.dumps(
                {
                    "operation": "dialogue-srt",
                    "transcript": str(transcript_path),
                    "plan": str(Path(args.plan).expanduser().resolve()) if args.plan else None,
                    "output": str(output),
                    "cue_count": len(cues),
                    "speaker_count": len(speaker_numbers),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return
    content = "\n\n".join(
        f"{index}\n{srt_timestamp(cue['start'])} --> {srt_timestamp(cue['end'])}\n{cue['text']}"
        for index, cue in enumerate(cues, start=1)
    )
    # Keep the final blank cue separator. Some players accept a single trailing
    # newline, while stricter SubRip loaders (including some IINA/mpv paths) do not.
    output.write_text(content + "\n\n", encoding="utf-8")
    print(output)


def meeting_media_summary(input_value: str) -> dict[str, Any]:
    data = probe_media(input_value)
    return {
        "path": str(Path(input_value).expanduser().resolve()),
        "duration": media_duration(input_value),
        "streams": [
            {
                "type": stream.get("codec_type"),
                "codec": stream.get("codec_name"),
                "duration": stream.get("duration"),
            }
            for stream in data.get("streams", [])
            if stream.get("codec_type") in {"audio", "video"}
        ],
    }


def meeting_input_identity(source: str) -> dict[str, Any]:
    if is_url(source):
        return {"url": source}
    path = Path(source)
    stat = path.stat()
    return {
        "path": str(path),
        "size": stat.st_size,
        "modified_ns": stat.st_mtime_ns,
    }


def command_meeting_cleanup(args: argparse.Namespace) -> None:
    source = require_input(args.input)
    source_data = probe_media(source)
    if not has_stream(source_data, "audio"):
        raise MediaError("meeting-cleanup requires an audio stream")
    if args.start < 0:
        raise MediaError("--start must be non-negative")
    if args.end is not None and args.end <= args.start:
        raise MediaError("--end must be greater than --start")
    if args.speaker_count and not args.diarization:
        raise MediaError("--speaker-count requires speaker diarization")
    if args.max_pause_ms is not None and args.max_pause_ms <= 0:
        raise MediaError("--max-pause-ms must be positive; use --keep-all-pauses to disable")

    output = Path(args.output).expanduser().resolve()
    srt_output = (
        Path(args.srt_output).expanduser().resolve()
        if args.srt_output
        else output.with_suffix(".srt")
    )
    work_dir = (
        Path(args.work_dir).expanduser().resolve()
        if args.work_dir
        else output.parent / ".media-utils" / f"{output.stem}-meeting-cleanup"
    )
    source_has_video = has_stream(source_data, "video")
    clipped_source = work_dir / ("source-clip.mp4" if source_has_video else "source-clip.wav")
    source_audio = work_dir / "source-asr.wav"
    source_transcript = work_dir / "source-transcript.json"
    ai_decisions = work_dir / "ai-decisions.json"
    edit_plan = work_dir / "edit-plan.json"
    cleaned_audio = work_dir / "cleaned-asr.wav"
    cleaned_transcript = work_dir / "cleaned-transcript.json"
    request_path = work_dir / "request.json"
    result_path = work_dir / "result.json"
    if args.cleanup_mode == "ai":
        fillers = [] if args.no_fillers else list(args.filler or [])
    else:
        fillers = [] if args.no_fillers else list(args.filler or MEETING_FILLERS)
    ai_exclude_categories = list(args.ai_exclude_category or [])
    if args.cleanup_mode == "ai" and args.no_fillers:
        ai_exclude_categories.extend(["filler", "verbal_tic"])
    ai_exclude_categories = sorted(set(ai_exclude_categories))
    trim_requested = args.start > 0 or args.end is not None

    resume_request = {
        "input": meeting_input_identity(source),
        "trim": {"start": args.start, "end": args.end},
        "asr": {
            "language": args.language,
            "diarization": args.diarization,
            "speaker_count": args.speaker_count,
        },
        "plan": {
            "cleanup_mode": args.cleanup_mode,
            "fillers": fillers,
            "max_pause_ms": None if args.keep_all_pauses else args.max_pause_ms,
            "keep_pause_ms": args.keep_pause_ms,
            "remove_repetitions": args.remove_repetitions,
            "repetition_gap_ms": args.repetition_gap_ms,
            "min_neighbor_gap_ms": args.min_neighbor_gap_ms,
            "boundary_search_ms": args.boundary_search_ms,
            "ai_model": args.ai_model if args.cleanup_mode == "ai" else None,
            "ai_level": args.ai_level if args.cleanup_mode == "ai" else None,
            "ai_min_confidence": (
                args.ai_min_confidence if args.cleanup_mode == "ai" else None
            ),
            "ai_chunk_words": (
                args.ai_chunk_words if args.cleanup_mode == "ai" else None
            ),
            "ai_context_words": (
                args.ai_context_words if args.cleanup_mode == "ai" else None
            ),
            "ai_exclude_categories": (
                ai_exclude_categories if args.cleanup_mode == "ai" else None
            ),
        },
    }
    request_fingerprint = hashlib.sha256(
        json.dumps(
            resume_request, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    ).hexdigest()
    workflow = {
        "operation": "meeting-cleanup",
        "input": source,
        "output": str(output),
        "srt_output": str(srt_output),
        "work_dir": str(work_dir),
        "review_gate": "apply only with --approve",
        "trim": {"start": args.start, "end": args.end},
        "asr": {
            "language": args.language,
            "diarization": args.diarization,
            "speaker_count": args.speaker_count,
        },
        "cleanup": {
            "mode": args.cleanup_mode,
            "fillers": fillers,
            "max_pause_ms": None if args.keep_all_pauses else args.max_pause_ms,
            "keep_pause_ms": args.keep_pause_ms,
            "remove_repetitions": args.remove_repetitions,
            "min_neighbor_gap_ms": args.min_neighbor_gap_ms,
            "boundary_search_ms": args.boundary_search_ms,
            "crossfade_ms": args.crossfade_ms,
            "ai_model": args.ai_model if args.cleanup_mode == "ai" else None,
            "ai_level": args.ai_level if args.cleanup_mode == "ai" else None,
            "ai_min_confidence": (
                args.ai_min_confidence if args.cleanup_mode == "ai" else None
            ),
            "ai_exclude_categories": (
                ai_exclude_categories if args.cleanup_mode == "ai" else None
            ),
        },
        "artifacts": {
            "request": str(request_path),
            "source_transcript": str(source_transcript),
            "ai_decisions": (
                str(ai_decisions) if args.cleanup_mode == "ai" else None
            ),
            "edit_plan": str(edit_plan),
            "cleaned_transcript": str(cleaned_transcript),
            "result": str(result_path),
        },
    }
    if args.dry_run:
        print(json.dumps(workflow, ensure_ascii=False, indent=2))
        return

    if output.exists() and not (args.force or args.resume):
        raise MediaError(f"Output already exists: {output}. Pass --force or --resume.")
    if srt_output.exists() and not (args.force or args.resume):
        raise MediaError(f"Output already exists: {srt_output}. Pass --force or --resume.")
    work_dir.mkdir(parents=True, exist_ok=True)
    request_payload = {
        "schema": "media-utils-meeting-cleanup-request/v1",
        "fingerprint": request_fingerprint,
        "request": resume_request,
    }
    if args.resume:
        if not request_path.is_file():
            raise MediaError(
                f"Cannot safely resume because the request manifest is missing: {request_path}"
            )
        existing_request = json.loads(request_path.read_text(encoding="utf-8"))
        if existing_request.get("fingerprint") != request_fingerprint:
            raise MediaError(
                "Cannot resume: input, trim, ASR, or cleanup settings differ from request.json"
            )
    else:
        write_json(request_path, request_payload, args.force)

    media_input = source
    if trim_requested:
        if not (args.resume and clipped_source.is_file()):
            command_trim(
                argparse.Namespace(
                    input=source,
                    output=str(clipped_source),
                    start=args.start,
                    end=args.end,
                    force=args.force,
                    dry_run=False,
                ),
                video=source_has_video,
            )
        media_input = str(clipped_source)

    if not (args.resume and source_audio.is_file()):
        command_audio_convert(
            argparse.Namespace(
                input=media_input,
                output=str(source_audio),
                sample_rate=16000,
                channels=1,
                force=args.force,
                dry_run=False,
            )
        )
    if not (args.resume and source_transcript.is_file()):
        command_dialogue_transcribe(
            argparse.Namespace(
                input=str(source_audio),
                output=str(source_transcript),
                language=args.language,
                diarization=args.diarization,
                speaker_count=args.speaker_count,
                force=args.force,
                dry_run=False,
            )
        )
    if not (args.resume and edit_plan.is_file()):
        command_dialogue_plan(
            argparse.Namespace(
                transcript=str(source_transcript),
                output=str(edit_plan),
                cleanup_mode=args.cleanup_mode,
                filler=fillers,
                use_default_fillers=False,
                padding_ms=0,
                max_pause_ms=None if args.keep_all_pauses else args.max_pause_ms,
                keep_pause_ms=args.keep_pause_ms,
                remove_repetitions=args.remove_repetitions,
                repetition_gap_ms=args.repetition_gap_ms,
                min_neighbor_gap_ms=args.min_neighbor_gap_ms,
                media=media_input,
                boundary_search_ms=args.boundary_search_ms,
                ai_model=args.ai_model,
                ai_level=args.ai_level,
                ai_min_confidence=args.ai_min_confidence,
                ai_chunk_words=args.ai_chunk_words,
                ai_context_words=args.ai_context_words,
                ai_exclude_category=ai_exclude_categories,
                ai_decisions_output=(
                    str(ai_decisions) if args.cleanup_mode == "ai" else None
                ),
                force=args.force,
                dry_run=False,
            )
        )

    plan = json.loads(edit_plan.read_text(encoding="utf-8"))
    removals = plan.get("remove", [])
    review_summary = {
        **workflow,
        "status": "review-required" if not args.approve else "approved",
        "plan_summary": {
            "word_count": plan.get("analysis", {}).get("word_count"),
            "removal_count": len(removals),
            "removed_seconds": round(
                sum(float(item["end"]) - float(item["start"]) for item in removals),
                6,
            ),
            "skipped_tight_fillers": plan.get("analysis", {}).get(
                "skipped_tight_fillers"
            ),
            "ai": plan.get("analysis", {}).get("ai"),
        },
    }
    if not args.approve:
        write_json(result_path, review_summary, args.force or args.resume)
        print(json.dumps(review_summary, ensure_ascii=False, indent=2))
        return

    if not (args.resume and output.is_file()):
        if removals:
            command_dialogue_apply(
                argparse.Namespace(
                    input=media_input,
                    plan=str(edit_plan),
                    output=str(output),
                    approve=True,
                    smooth=True,
                    crossfade_ms=args.crossfade_ms,
                    force=args.force,
                    dry_run=False,
                )
            )
        else:
            command_trim(
                argparse.Namespace(
                    input=media_input,
                    output=str(output),
                    start=0.0,
                    end=None,
                    force=args.force,
                    dry_run=False,
                ),
                video=source_has_video,
            )

    if not (args.resume and cleaned_audio.is_file()):
        command_audio_convert(
            argparse.Namespace(
                input=str(output),
                output=str(cleaned_audio),
                sample_rate=16000,
                channels=1,
                force=args.force,
                dry_run=False,
            )
        )
    if not (args.resume and cleaned_transcript.is_file()):
        command_dialogue_transcribe(
            argparse.Namespace(
                input=str(cleaned_audio),
                output=str(cleaned_transcript),
                language=args.language,
                diarization=args.diarization,
                speaker_count=args.speaker_count,
                force=args.force,
                dry_run=False,
            )
        )
    if not (args.resume and srt_output.is_file()):
        command_dialogue_srt(
            argparse.Namespace(
                transcript=str(cleaned_transcript),
                output=str(srt_output),
                plan=None,
                speaker_prefix=args.speaker_prefix,
                force=args.force,
                dry_run=False,
            )
        )

    completed = {
        **review_summary,
        "status": "complete",
        "output_media": meeting_media_summary(str(output)),
        "srt_output": str(srt_output),
    }
    write_json(result_path, completed, args.force or args.resume)
    print(json.dumps(completed, ensure_ascii=False, indent=2))


def add_processing_flags(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--force", action="store_true", help="Overwrite an existing output")
    parser.add_argument("--dry-run", action="store_true", help="Print the planned command only")


def add_trim_parser(
    parent: argparse._SubParsersAction[argparse.ArgumentParser], media_type: str
) -> None:
    parser = parent.add_parser("trim", help=f"Trim {media_type}")
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--start", type=float, default=0.0)
    parser.add_argument("--end", type=float)
    add_processing_flags(parser)


def add_concat_parser(
    parent: argparse._SubParsersAction[argparse.ArgumentParser], media_type: str
) -> None:
    parser = parent.add_parser("concat", help=f"Concatenate compatible {media_type} files")
    parser.add_argument("output")
    parser.add_argument("inputs", nargs="+")
    add_processing_flags(parser)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Deterministic media operations using ffmpeg/ffprobe and optional bl ASR."
    )
    commands = parser.add_subparsers(dest="domain", required=True)

    doctor = commands.add_parser("doctor", help="Check required and optional dependencies")
    doctor.add_argument(
        "--install-plan",
        action="store_true",
        help="Include OS-aware commands for missing dependencies and ffmpeg features",
    )
    doctor.add_argument(
        "--for-operation",
        choices=sorted(DOCTOR_OPERATIONS),
        help="Check only the dependencies needed by one operation",
    )

    probe = commands.add_parser("probe", help="Print ffprobe metadata as JSON")
    probe.add_argument("input")
    probe.add_argument("--output")
    probe.add_argument("--force", action="store_true")

    meeting = commands.add_parser(
        "meeting-cleanup",
        help="Clean a meeting recording and export speaker-labelled SRT",
        description=(
            "Run the reusable meeting workflow: optional trim, mono PCM extraction, "
            "Bailian ASR diarization, exact-rule or AI semantic cleanup planning, "
            "smooth ffmpeg edit, final ASR, and speaker-labelled SRT export. Without "
            "--approve, stop after writing the reviewable edit plan."
        ),
    )
    meeting.add_argument("input", help="Meeting audio or video")
    meeting.add_argument("output", help="Cleaned audio or video")
    meeting.add_argument("--start", type=float, default=0.0, help="Source start time in seconds")
    meeting.add_argument("--end", type=float, help="Absolute source end time in seconds")
    meeting.add_argument("--language", help="ASR language hint, for example zh or en")
    meeting.add_argument(
        "--diarization",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Enable speaker diarization (default: enabled)",
    )
    meeting.add_argument("--speaker-count", type=int, help="Expected number of speakers")
    meeting.add_argument(
        "--cleanup-mode",
        choices=["exact", "ai"],
        default="exact",
        help="Use exact rules or AI semantic word selection (default: exact)",
    )
    meeting.add_argument(
        "--filler",
        action="append",
        help=(
            "Exact-mode removable phrase or AI-mode semantic hint; repeat the flag"
        ),
    )
    meeting.add_argument(
        "--no-fillers",
        action="store_true",
        help="Disable exact filler matching or AI filler/verbal-tic categories",
    )
    meeting.add_argument("--max-pause-ms", type=int, default=1800)
    meeting.add_argument("--keep-pause-ms", type=int, default=400)
    meeting.add_argument(
        "--keep-all-pauses",
        action="store_true",
        help="Disable long-pause shortening",
    )
    meeting.add_argument(
        "--remove-repetitions",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Remove adjacent exact repetitions (default: enabled)",
    )
    meeting.add_argument("--repetition-gap-ms", type=int, default=500)
    meeting.add_argument("--min-neighbor-gap-ms", type=int, default=60)
    meeting.add_argument("--boundary-search-ms", type=int, default=60)
    meeting.add_argument("--crossfade-ms", type=float, default=20.0)
    meeting.add_argument("--ai-model", default="qwen3.7-max")
    meeting.add_argument(
        "--ai-level",
        choices=sorted(AI_CLEANUP_LEVELS),
        default="conservative",
    )
    meeting.add_argument("--ai-min-confidence", type=float)
    meeting.add_argument("--ai-chunk-words", type=int, default=240)
    meeting.add_argument("--ai-context-words", type=int, default=40)
    meeting.add_argument(
        "--ai-exclude-category",
        action="append",
        choices=sorted(
            set().union(
                *(level["categories"] for level in AI_CLEANUP_LEVELS.values())
            )
        ),
        help="AI category to forbid; repeat the flag",
    )
    meeting.add_argument("--speaker-prefix", default="人物")
    meeting.add_argument(
        "--srt-output",
        help="SRT path; defaults to the cleaned output basename with .srt",
    )
    meeting.add_argument(
        "--work-dir",
        help="Intermediate transcript/plan directory",
    )
    meeting.add_argument(
        "--approve",
        action="store_true",
        help="Apply the generated or resumed edit plan",
    )
    meeting.add_argument(
        "--resume",
        action="store_true",
        help="Reuse existing work artifacts and continue the workflow",
    )
    add_processing_flags(meeting)

    audio = commands.add_parser("audio", help="Audio processing")
    audio_commands = audio.add_subparsers(dest="action", required=True)
    add_trim_parser(audio_commands, "audio")
    add_concat_parser(audio_commands, "audio")

    audio_speed = audio_commands.add_parser("speed")
    audio_speed.add_argument("input")
    audio_speed.add_argument("output")
    audio_speed.add_argument("--factor", type=float, required=True)
    add_processing_flags(audio_speed)

    audio_volume = audio_commands.add_parser("volume")
    audio_volume.add_argument("input")
    audio_volume.add_argument("output")
    audio_volume.add_argument("--factor", type=float, default=1.0)
    audio_volume.add_argument("--loudnorm", action="store_true")
    add_processing_flags(audio_volume)

    audio_fade = audio_commands.add_parser("fade")
    audio_fade.add_argument("input")
    audio_fade.add_argument("output")
    audio_fade.add_argument("--fade-in", type=float, default=1.0)
    audio_fade.add_argument("--fade-out", type=float, default=1.0)
    add_processing_flags(audio_fade)

    audio_mix = audio_commands.add_parser("mix")
    audio_mix.add_argument("output")
    audio_mix.add_argument("inputs", nargs="+")
    add_processing_flags(audio_mix)

    audio_convert = audio_commands.add_parser("convert")
    audio_convert.add_argument("input")
    audio_convert.add_argument("output")
    audio_convert.add_argument("--sample-rate", type=int)
    audio_convert.add_argument("--channels", type=int)
    add_processing_flags(audio_convert)

    silence = audio_commands.add_parser("silence-plan")
    silence.add_argument("input")
    silence.add_argument("output")
    silence.add_argument("--noise-db", type=float, default=-35.0)
    silence.add_argument("--min-duration", type=float, default=0.7)
    silence.add_argument("--keep", type=float, default=0.25)
    add_processing_flags(silence)

    image = commands.add_parser("image", help="Image processing")
    image_commands = image.add_subparsers(dest="action", required=True)
    image_convert = image_commands.add_parser("convert")
    image_convert.add_argument("input")
    image_convert.add_argument("output")
    add_processing_flags(image_convert)

    image_resize = image_commands.add_parser("resize")
    image_resize.add_argument("input")
    image_resize.add_argument("output")
    image_resize.add_argument("--width", type=int)
    image_resize.add_argument("--height", type=int)
    image_resize.add_argument("--stretch", action="store_true")
    add_processing_flags(image_resize)

    image_crop = image_commands.add_parser("crop")
    image_crop.add_argument("input")
    image_crop.add_argument("output")
    image_crop.add_argument("--width", type=int, required=True)
    image_crop.add_argument("--height", type=int, required=True)
    image_crop.add_argument("--x", type=int, default=0)
    image_crop.add_argument("--y", type=int, default=0)
    add_processing_flags(image_crop)

    image_rotate = image_commands.add_parser("rotate")
    image_rotate.add_argument("input")
    image_rotate.add_argument("output")
    image_rotate.add_argument("--degrees", type=int, choices=[90, 180, 270], required=True)
    add_processing_flags(image_rotate)

    image_flip = image_commands.add_parser("flip")
    image_flip.add_argument("input")
    image_flip.add_argument("output")
    image_flip.add_argument("--direction", choices=["horizontal", "vertical"], required=True)
    add_processing_flags(image_flip)

    thumbnail = image_commands.add_parser("thumbnail")
    thumbnail.add_argument("input")
    thumbnail.add_argument("output")
    thumbnail.add_argument("--width", type=int, required=True)
    thumbnail.add_argument("--height", type=int, required=True)
    thumbnail.add_argument("--background", default="black")
    add_processing_flags(thumbnail)

    video = commands.add_parser("video", help="Video processing")
    video_commands = video.add_subparsers(dest="action", required=True)
    add_trim_parser(video_commands, "video")
    add_concat_parser(video_commands, "video")

    video_speed = video_commands.add_parser("speed")
    video_speed.add_argument("input")
    video_speed.add_argument("output")
    video_speed.add_argument("--factor", type=float, required=True)
    add_processing_flags(video_speed)

    video_volume = video_commands.add_parser("volume")
    video_volume.add_argument("input")
    video_volume.add_argument("output")
    video_volume.add_argument("--factor", type=float, required=True)
    add_processing_flags(video_volume)

    video_flip = video_commands.add_parser("flip")
    video_flip.add_argument("input")
    video_flip.add_argument("output")
    video_flip.add_argument("--direction", choices=["horizontal", "vertical"], required=True)
    add_processing_flags(video_flip)

    video_filter = video_commands.add_parser("filter")
    video_filter.add_argument("input")
    video_filter.add_argument("output")
    video_filter.add_argument("--preset", choices=sorted(VIDEO_PRESETS), required=True)
    add_processing_flags(video_filter)

    overlay = video_commands.add_parser("overlay")
    overlay.add_argument("input")
    overlay.add_argument("image")
    overlay.add_argument("output")
    overlay.add_argument("--x", default="W-w-24")
    overlay.add_argument("--y", default="H-h-24")
    overlay.add_argument("--start", type=float)
    overlay.add_argument("--end", type=float)
    add_processing_flags(overlay)

    subtitle = video_commands.add_parser("subtitle")
    subtitle.add_argument("input")
    subtitle.add_argument("subtitle")
    subtitle.add_argument("output")
    subtitle.add_argument("--fonts-dir")
    add_processing_flags(subtitle)

    fade_audio = video_commands.add_parser("fade-audio")
    fade_audio.add_argument("input")
    fade_audio.add_argument("output")
    fade_audio.add_argument("--fade-in", type=float, default=1.0)
    fade_audio.add_argument("--fade-out", type=float, default=1.0)
    add_processing_flags(fade_audio)

    mux = video_commands.add_parser("mux-audio")
    mux.add_argument("input")
    mux.add_argument("audio")
    mux.add_argument("output")
    mux.add_argument("--keep-original", action="store_true")
    mux.add_argument("--shortest", action="store_true")
    add_processing_flags(mux)

    mux_subtitle = video_commands.add_parser("mux-subtitle")
    mux_subtitle.add_argument("input")
    mux_subtitle.add_argument("subtitle")
    mux_subtitle.add_argument("output")
    mux_subtitle.add_argument("--language", default="zho")
    mux_subtitle.add_argument("--title", default="中文字幕")
    add_processing_flags(mux_subtitle)

    extract = video_commands.add_parser("extract-audio")
    extract.add_argument("input")
    extract.add_argument("output")
    add_processing_flags(extract)

    image_video = video_commands.add_parser("image-to-video")
    image_video.add_argument("input")
    image_video.add_argument("output")
    image_video.add_argument("--duration", type=float, default=3.0)
    image_video.add_argument("--size", default="1920x1080")
    image_video.add_argument("--fps", type=int, default=30)
    image_video.add_argument("--motion", choices=["none", "zoom-in", "zoom-out"], default="none")
    image_video.add_argument("--background", default="black")
    add_processing_flags(image_video)

    scenes = video_commands.add_parser("scenes")
    scenes.add_argument("input")
    scenes.add_argument("output")
    scenes.add_argument("--threshold", type=float, default=0.3)
    scenes.add_argument("--min-duration", type=float, default=1.0)
    scenes.add_argument("--max-duration", type=float)
    add_processing_flags(scenes)

    chroma = video_commands.add_parser("chroma-key")
    chroma.add_argument("input")
    chroma.add_argument("output")
    chroma.add_argument("--color", default="00FF00")
    chroma.add_argument("--similarity", type=float, default=0.12)
    chroma.add_argument("--blend", type=float, default=0.05)
    add_processing_flags(chroma)

    dialogue = commands.add_parser("dialogue", help="ASR transcription and review-first cuts")
    dialogue_commands = dialogue.add_subparsers(dest="action", required=True)
    transcribe = dialogue_commands.add_parser("transcribe")
    transcribe.add_argument("input")
    transcribe.add_argument("output")
    transcribe.add_argument("--language")
    transcribe.add_argument("--diarization", action="store_true")
    transcribe.add_argument("--speaker-count", type=int)
    add_processing_flags(transcribe)

    plan = dialogue_commands.add_parser("plan")
    plan.add_argument("transcript")
    plan.add_argument("output")
    plan.add_argument(
        "--cleanup-mode",
        choices=["exact", "ai"],
        default="exact",
        help="Use exact rules or AI semantic word selection",
    )
    plan.add_argument("--filler", action="append")
    plan.add_argument("--use-default-fillers", action="store_true")
    plan.add_argument("--padding-ms", type=int, default=0)
    plan.add_argument("--max-pause-ms", type=int)
    plan.add_argument("--keep-pause-ms", type=int, default=250)
    plan.add_argument("--remove-repetitions", action="store_true")
    plan.add_argument("--repetition-gap-ms", type=int, default=500)
    plan.add_argument("--min-neighbor-gap-ms", type=int, default=0)
    plan.add_argument("--media")
    plan.add_argument("--boundary-search-ms", type=int, default=0)
    plan.add_argument("--ai-model", default="qwen3.7-max")
    plan.add_argument(
        "--ai-level",
        choices=sorted(AI_CLEANUP_LEVELS),
        default="conservative",
    )
    plan.add_argument("--ai-min-confidence", type=float)
    plan.add_argument("--ai-chunk-words", type=int, default=240)
    plan.add_argument("--ai-context-words", type=int, default=40)
    plan.add_argument(
        "--ai-exclude-category",
        action="append",
        choices=sorted(
            set().union(
                *(level["categories"] for level in AI_CLEANUP_LEVELS.values())
            )
        ),
    )
    plan.add_argument("--ai-decisions-output")
    add_processing_flags(plan)

    apply_plan = dialogue_commands.add_parser("apply")
    apply_plan.add_argument("input")
    apply_plan.add_argument("plan")
    apply_plan.add_argument("output")
    apply_plan.add_argument("--approve", action="store_true")
    apply_plan.add_argument("--smooth", action="store_true")
    apply_plan.add_argument("--crossfade-ms", type=float, default=20.0)
    add_processing_flags(apply_plan)

    srt = dialogue_commands.add_parser("srt")
    srt.add_argument("transcript")
    srt.add_argument("output")
    srt.add_argument("--plan")
    srt.add_argument("--speaker-prefix", default="人物")
    add_processing_flags(srt)

    return parser


def dispatch(args: argparse.Namespace) -> None:
    if args.domain == "doctor":
        command_doctor(args)
    elif args.domain == "probe":
        command_probe(args)
    elif args.domain == "meeting-cleanup":
        command_meeting_cleanup(args)
    elif args.domain == "audio":
        handlers = {
            "trim": lambda value: command_trim(value, video=False),
            "concat": lambda value: command_concat(value, video=False),
            "speed": command_audio_speed,
            "volume": command_audio_volume,
            "fade": command_audio_fade,
            "mix": command_audio_mix,
            "convert": command_audio_convert,
            "silence-plan": command_silence_plan,
        }
        handlers[args.action](args)
    elif args.domain == "image":
        handlers = {
            "convert": command_image_convert,
            "resize": command_image_resize,
            "crop": command_image_crop,
            "rotate": command_image_rotate,
            "flip": command_image_flip,
            "thumbnail": command_image_thumbnail,
        }
        handlers[args.action](args)
    elif args.domain == "video":
        handlers = {
            "trim": lambda value: command_trim(value, video=True),
            "concat": lambda value: command_concat(value, video=True),
            "speed": command_video_speed,
            "volume": command_video_volume,
            "flip": command_video_flip,
            "filter": command_video_filter,
            "overlay": command_video_overlay,
            "subtitle": command_video_subtitle,
            "fade-audio": command_video_fade_audio,
            "mux-audio": command_video_mux_audio,
            "mux-subtitle": command_video_mux_subtitle,
            "extract-audio": command_extract_audio,
            "image-to-video": command_image_to_video,
            "scenes": command_video_scenes,
            "chroma-key": command_video_chroma_key,
        }
        handlers[args.action](args)
    elif args.domain == "dialogue":
        handlers = {
            "transcribe": command_dialogue_transcribe,
            "plan": command_dialogue_plan,
            "apply": command_dialogue_apply,
            "srt": command_dialogue_srt,
        }
        handlers[args.action](args)
    else:
        raise MediaError(f"Unknown domain: {args.domain}")


def main() -> int:
    try:
        dispatch(build_parser().parse_args())
        return 0
    except DependencyError as exc:
        payload = {
            "error": "DependencyMissing",
            "operation": exc.operation,
            "missing": exc.missing,
            **dependency_install_plan(exc.missing, [exc.operation]),
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    except MediaError as exc:
        print(f"media-utils: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
