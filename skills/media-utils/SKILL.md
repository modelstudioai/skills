---
name: media-utils
description: Deterministic, review-first processing for local audio, image, and video files using ffmpeg/ffprobe, with optional Bailian `bl` ASR speaker diarization and multilingual AI semantic dialogue cleanup. Use for meeting recording cleanup, meeting video or audio trimming, exact-rule or AI-enhanced filler/self-confirmation/false-start/repetition removal, speaker-attributed transcripts and SRT, media inspection, conversion, concatenation, resizing, cropping, overlays, subtitles, speed/volume/fades, mixing, audio extraction, image-to-video, scene detection, green-screen removal, and silence planning. Trigger when users ask to clean or condense a meeting, semantically remove verbal filler or self-confirming words such as non-responsive “对”, handle multilingual disfluencies, identify speakers, create `人物：说的话` subtitles, or edit, convert, inspect, transcribe, subtitle, split, combine, or batch-process common multimedia files.
---

# Media Utils

Prefer reproducible local transforms. Use `bl` only for ASR transcription and speaker
diarization; execute all approved timeline edits with ffmpeg.

## Run the tool

Set the skill directory explicitly, then run the bundled Python entry point:

```bash
MEDIA_UTILS_SKILL=/absolute/path/to/media-utils
python3 "$MEDIA_UTILS_SKILL/scripts/media_utils.py" doctor
python3 "$MEDIA_UTILS_SKILL/scripts/media_utils.py" probe ./input.mp4
```

Prefer the top-level `meeting-cleanup` command when the request combines meeting
trimming, dialogue cleanup, speaker diarization, and SRT delivery:

```bash
python3 "$MEDIA_UTILS_SKILL/scripts/media_utils.py" meeting-cleanup \
  meeting.mp4 cleaned.mp4 --end 600 --language zh --approve
```

Choose AI semantic cleanup explicitly when exact filler matching is insufficient:

```bash
python3 "$MEDIA_UTILS_SKILL/scripts/media_utils.py" meeting-cleanup \
  meeting.mp4 cleaned.mp4 --cleanup-mode ai --ai-level conservative --approve
```

Omit `--approve` to stop after producing the transcript and reviewable edit plan.
After reviewing or editing the plan, rerun the same command with `--approve --resume`.
Read [references/audio.md](references/audio.md) for all meeting options and artifact paths.

Require Python 3.10+, `ffmpeg`, and `ffprobe` for core transforms. Do not require
every optional dependency up front. Require `bl` only for `dialogue transcribe`,
`meeting-cleanup`, the `subtitles` filter/libass only for subtitle burn-in, and the `libwebp` encoder
only for WebP output.

Run a scoped check before an operation that needs an optional capability. If it
reports missing dependencies, read [references/setup.md](references/setup.md),
inspect the OS-aware repair plan, and ask before running any install command:

```bash
python3 "$MEDIA_UTILS_SKILL/scripts/media_utils.py" doctor
python3 "$MEDIA_UTILS_SKILL/scripts/media_utils.py" doctor \
  --for-operation subtitle-burn --install-plan
```

Valid scoped checks are `core`, `subtitle-burn`, `image-webp`,
`video-alpha-webm`, `audio-ogg`, `dialogue-transcribe`, `dialogue-ai-plan`, and
`meeting-cleanup`. A failed operation
also returns a structured `DependencyMissing` object with a scoped install plan.

## Route by media type

- Read [references/audio.md](references/audio.md) for audio transforms, silence plans,
  ASR diarization, filler detection, and review-first cuts.
- Read [references/image.md](references/image.md) for deterministic image conversion,
  resizing, cropping, rotation, flipping, and thumbnails.
- Read [references/video.md](references/video.md) for video editing, scene plans,
  overlays, subtitles, image-to-video, and green-screen Alpha output.

Use `probe` when the file type, streams, duration, resolution, frame rate, codec, or
Alpha support is uncertain.

## Follow the safe workflow

1. Resolve every input and output path. Keep the source file unchanged.
2. Run `doctor`, then `probe` the source.
3. Choose the smallest matching subcommand from the modality reference.
4. Use `--dry-run` before a complex or batch operation.
5. Write to a new output path. Pass `--force` only when the user explicitly wants to
   replace an existing derived file.
6. Probe the output and verify duration, streams, dimensions, codec, and pixel format.
7. Re-transcribe an edited video before final SRT export when many hard cuts can accumulate
   frame-boundary rounding.
8. Report the output path and any quality-affecting re-encode.

Never interpolate untrusted user text into a shell command. Pass arguments as separate
process arguments or invoke this script directly.

## Handle dialogue edits conservatively

Use `meeting-cleanup` instead of manually assembling the following steps when the user
requests the complete meeting workflow. Pass `--approve` only when the request explicitly
authorizes removing the planned material.

Treat ASR as analysis, not approval:

1. Run `dialogue transcribe` with `--diarization` when speakers matter.
2. For video, create ASR input directly as PCM mono; do not use an AAC intermediate.
3. Run `dialogue plan --cleanup-mode exact` for predictable phrase matching, or use
   `--cleanup-mode ai` for multilingual semantic judgments. Keep AI at `conservative`
   unless the user requests stronger compression.
4. In AI mode, require existing consecutive ASR word IDs, validate confidence/category/span
   locally, and preserve the full audit in `ai-decisions.json`.
5. Use neighbor-gap guards and media-aware low-energy boundary refinement for fluent speech.
6. Show the generated JSON removal intervals to the user.
7. Run `dialogue apply ... --approve --smooth` for conversational video only after the
   removals are accepted.

Do not silently enable the built-in filler list. Avoid cutting across speaker changes.
The plan generator only shortens long pauses between words attributed to the same speaker.

Before executing `bl`, follow the installed `bailian-cli` skill pre-flight and command
reference. Pass local files directly; do not ask the user to host them.

## Keep these capabilities out of the deterministic tier

Do not claim support for:

- vocal/accompaniment source separation;
- semantic image enhancement or fixed image-quality scores;
- reliable OCR boxes/confidence;
- production Alpha matting from arbitrary image or portrait video;
- generative video restoration, intelligent subtitle inpainting, or specialized
  highlight/storyline models.

Do not call Volcengine APIs, CLIs, SDKs, endpoints, or tools.
