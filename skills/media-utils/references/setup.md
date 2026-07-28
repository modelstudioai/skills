# Setup and Repair

Read this file when a scoped `doctor` check reports `"ok": false`, an operation
returns `DependencyMissing`, or the user asks to install or repair dependencies.

## Dependency tiers

- Require Python 3.10+, `ffmpeg`, and `ffprobe` for core local transforms.
- Require `bl` for ASR and speaker diarization.
- Require an ffmpeg build compiled with `libass` for subtitle rendering.
- Require an ffmpeg build compiled with `libwebp` for WebP output.

`libass` supplies ffmpeg's `subtitles` filter. `libwebp` supplies its WebP encoder.
Installing those libraries beside an already-built ffmpeg binary does not add the
features; install a feature-complete ffmpeg build instead.

Installing `bl` means installing the `bailian-cli` npm package. Installing the
separate `modelstudioai/cli` agent Skills is useful for an agent environment, but
is not a runtime dependency of `media-utils`.

## Repair workflow

Check the core once, then generate a plan only for the operation being requested:

```bash
python3 scripts/media_utils.py doctor
python3 scripts/media_utils.py doctor --for-operation subtitle-burn --install-plan
python3 scripts/media_utils.py doctor --for-operation image-webp --install-plan
python3 scripts/media_utils.py doctor --for-operation dialogue-transcribe --install-plan
```

Tell the user which capability is missing and ask before executing each command in
the returned `actions[].commands` list. Do not install every optional dependency
preemptively. Re-run the same scoped check afterward.

On macOS with Homebrew, use `brew install ffmpeg` for the core. Use
`brew install ffmpeg-full` only when a requested capability needs libass or
libwebp and the selected FFmpeg build lacks it. `ffmpeg-full` is keg-only, so this
tool automatically prefers:

```text
/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg
/opt/homebrew/opt/ffmpeg-full/bin/ffprobe
```

The Intel Homebrew paths under `/usr/local/opt` are also detected. To select another
build explicitly, set:

```bash
export MEDIA_UTILS_FFMPEG=/absolute/path/to/ffmpeg
export MEDIA_UTILS_FFPROBE=/absolute/path/to/ffprobe
export MEDIA_UTILS_BL=/absolute/path/to/bl
```

Do not require `uv`: the bundled Python entry point uses only the standard library.
Add `uv` only if future scripts introduce declared third-party Python dependencies.
