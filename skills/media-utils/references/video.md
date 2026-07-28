# Video processing

## Contents

- [Basic timeline edits](#basic-timeline-edits)
- [Visual and audio transforms](#visual-and-audio-transforms)
- [Composition](#composition)
- [Scene analysis](#scene-analysis)
- [Green-screen Alpha](#green-screen-alpha)
- [Verification and limits](#verification-and-limits)

Use `python3 scripts/media_utils.py` below relative to the skill directory.

## Basic timeline edits

```bash
python3 scripts/media_utils.py video trim input.mp4 clip.mp4 --start 2.5 --end 9.0
python3 scripts/media_utils.py video concat joined.mp4 clip1.mp4 clip2.mp4
python3 scripts/media_utils.py video speed input.mp4 fast.mp4 --factor 1.25
```

Concatenated files must have compatible stream layouts, dimensions, frame rates, and time
bases. Normalize inputs first when they differ.

## Visual and audio transforms

```bash
python3 scripts/media_utils.py video flip input.mp4 flipped.mp4 --direction horizontal
python3 scripts/media_utils.py video volume input.mp4 quiet.mp4 --factor 0.6
python3 scripts/media_utils.py video fade-audio input.mp4 faded.mp4 \
  --fade-in 0.5 --fade-out 1.0
python3 scripts/media_utils.py video filter input.mp4 vivid.mp4 --preset vivid
```

Filter presets are deterministic ffmpeg color transforms, not semantic AI filters. Available
presets: `cinematic`, `cool`, `fair-skin`, `food`, `mono`, `spring`, `sunset`, `vivid`,
and `warm`.

## Composition

Overlay an image, optionally within a time range:

```bash
python3 scripts/media_utils.py video overlay input.mp4 logo.png watermarked.mp4 \
  --x "W-w-24" --y "H-h-24" --start 1 --end 8
```

Burn an SRT, VTT, or ASS subtitle file:

```bash
python3 scripts/media_utils.py video subtitle input.mp4 captions.srt captioned.mp4
```

This requires ffmpeg's `subtitles` filter/libass. Some ffmpeg builds omit it; check only
this operation's dependencies before installing anything:

```bash
python3 scripts/media_utils.py doctor --for-operation subtitle-burn --install-plan
```

Embed a selectable subtitle track without re-encoding the video or audio:

```bash
python3 scripts/media_utils.py video mux-subtitle input.mp4 captions.srt captioned.mp4
```

This avoids reliance on a player's sidecar-subtitle auto-discovery. MP4/M4V/MOV use
`mov_text`; MKV uses SubRip. The external subtitle becomes the sole, default subtitle track;
existing subtitle tracks in the input are not copied. Use `--language` and `--title` to
override the default `zho` and `中文字幕` metadata.

Replace or mix an audio track:

```bash
python3 scripts/media_utils.py video mux-audio input.mp4 narration.wav narrated.mp4 --shortest
python3 scripts/media_utils.py video mux-audio input.mp4 music.wav mixed.mp4 \
  --keep-original --shortest
python3 scripts/media_utils.py video extract-audio input.mp4 audio.m4a
```

Create a video from one still image:

```bash
python3 scripts/media_utils.py video image-to-video poster.png poster.mp4 \
  --duration 5 --size 1920x1080 --fps 30 --motion zoom-in
```

For multiple images, create one clip per image, then concatenate compatible clips.

## Scene analysis

Generate a JSON scene plan without cutting:

```bash
python3 scripts/media_utils.py video scenes input.mp4 scenes.json \
  --threshold 0.3 --min-duration 1.0 --max-duration 30
```

The threshold is ffmpeg's normalized scene-change score from 0 to 1. Lower values produce
more cuts. `--max-duration` inserts deterministic boundaries into long scenes.

Use the returned start/end times with `video trim` after reviewing the plan.

## Green-screen Alpha

Generate transparent video:

```bash
python3 scripts/media_utils.py video chroma-key green.mp4 foreground.webm \
  --color 00FF00 --similarity 0.12 --blend 0.05
```

Use `.webm` or `.mov`; other containers are rejected for Alpha output. For VP9/WebM,
`ffprobe` commonly reports `yuv420p` while the stream tag contains `alpha_mode=1`. Verify
that tag, decode an `alphaextract` frame with the `libvpx-vp9` decoder, and composite over
a contrasting background. Some ffmpeg builds' native VP9 decoder does not expose the alpha
plane even when it is present.

## Verification and limits

- Existing outputs are rejected unless `--force` is explicit.
- Use `--dry-run` before complex transforms.
- Timeline and filtered operations re-encode.
- MP4/MOV outputs default to H.264/AAC; WebM defaults to VP9/Opus.
- This tier does not perform portrait matting, generative restoration, intelligent subtitle
  inpainting, video OCR, or specialized highlight/storyline analysis.
