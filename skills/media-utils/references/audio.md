# Audio processing

## Contents

- [Inspect and convert](#inspect-and-convert)
- [Edit and combine](#edit-and-combine)
- [Silence removal plans](#silence-removal-plans)
- [Reusable meeting cleanup](#reusable-meeting-cleanup)
- [Dialogue transcription and cleanup](#dialogue-transcription-and-cleanup)
- [Output behavior](#output-behavior)

Use `python3 scripts/media_utils.py` below relative to the skill directory.

## Inspect and convert

```bash
python3 scripts/media_utils.py probe input.wav
python3 scripts/media_utils.py audio convert input.wav output.mp3
python3 scripts/media_utils.py audio convert input.wav output.wav --sample-rate 16000 --channels 1
```

Supported output extensions: `.aac`, `.flac`, `.m4a`, `.mp3`, `.ogg`, `.opus`, `.wav`.
Conversion always re-encodes with an explicit codec selected from the extension.
For `.ogg`, prefer `libvorbis` and fall back to ffmpeg's experimental native `vorbis`
encoder when that is the only available implementation. `doctor` reports `ogg_output`.
Check it directly with:

```bash
python3 scripts/media_utils.py doctor --for-operation audio-ogg --install-plan
```

## Edit and combine

```bash
# Accurate time-based trim; --end is absolute source time.
python3 scripts/media_utils.py audio trim input.wav clip.wav --start 3.2 --end 12.8

# Inputs must have compatible stream layouts.
python3 scripts/media_utils.py audio concat joined.mp3 a.mp3 b.mp3 c.mp3

python3 scripts/media_utils.py audio speed input.wav fast.wav --factor 1.25
python3 scripts/media_utils.py audio volume input.wav quieter.wav --factor 0.7
python3 scripts/media_utils.py audio volume input.wav normalized.wav --loudnorm
python3 scripts/media_utils.py audio fade input.wav faded.wav --fade-in 0.5 --fade-out 1.0
python3 scripts/media_utils.py audio mix mixed.mp3 voice.wav music.wav
```

`speed` chains multiple `atempo` filters when the factor is outside ffmpeg's single-filter
range. `mix` keeps the longest input and applies a limiter after summing.

## Silence removal plans

Generate a plan without editing the source:

```bash
python3 scripts/media_utils.py audio silence-plan input.wav silence-plan.json \
  --noise-db -35 --min-duration 0.7 --keep 0.25
```

The plan retains the first `--keep` seconds of every detected silence and proposes removal
of the remainder. Inspect `analysis.detected` and `remove` before applying:

```bash
python3 scripts/media_utils.py dialogue apply input.wav silence-plan.json cleaned.wav --approve
```

Adjust the noise floor for the recording. A value that is too high can classify quiet speech
as silence.

## Reusable meeting cleanup

Use the top-level command when one request includes trimming, speaker diarization,
reviewable verbal cleanup, a smooth edit, and final speaker-labelled SRT. Exact matching
remains the default:

```bash
python3 scripts/media_utils.py meeting-cleanup meeting.mp4 cleaned.mp4 \
  --end 600 --language zh --approve
```

The command performs this workflow:

1. Optionally trim the source with `--start` and absolute `--end` seconds.
2. Extract 16 kHz mono PCM directly from the selected source range.
3. Run `bl speech recognize` with speaker diarization.
4. Plan removals with exact rules or AI semantic classification.
5. Refine cut boundaries against low-energy PCM and apply short equal-power crossfades.
6. Re-transcribe the cleaned output and create a matching `人物N：说话内容` SRT.

By default, use only conservative vocal fillers (`嗯`, `呃`, `额`, `啊`, `哦`, `唔`,
`哎`, `um`, `uh`, and `erm`). Repeat `--filler` to replace this preset with an
explicit list, or pass `--no-fillers`. The default cleanup also shortens same-speaker
pauses longer than 1800 ms to 400 ms and removes adjacent exact repetitions. Inspect
`meeting-cleanup --help` to tune or disable each behavior.

Use AI mode when semantic context or multiple languages make exact lists insufficient:

```bash
python3 scripts/media_utils.py meeting-cleanup meeting.mp4 cleaned.mp4 \
  --cleanup-mode ai --ai-level conservative --language zh --approve
```

AI mode defaults to `qwen3.7-max`. It assigns stable IDs to existing ASR words and asks
the model to return only consecutive IDs, a category, confidence, and reason. The local
validator rejects invented IDs, cross-speaker spans, protected numbers and negations,
low-confidence decisions, disallowed categories, overlong spans, and cuts too close to
neighboring speech. The model never creates timestamps or edits media directly.

AI levels combine prompt policy with local hard limits:

| Level | Minimum confidence | Maximum words | Maximum span | Additional scope |
| --- | ---: | ---: | ---: | --- |
| `conservative` | 0.90 | 3 | 1.5 s | Fillers, verbal tics, self-confirmation, false starts, exact repetition |
| `balanced` | 0.75 | 10 | 3.5 s | Also discourse markers, speech repairs, redundant rephrases |
| `aggressive` | 0.60 | 30 | 8 s | Also redundant clauses and low-information speech |

Override the threshold with `--ai-min-confidence`, the model with `--ai-model`, or forbid
categories by repeating `--ai-exclude-category`. `--no-fillers` disables AI `filler` and
`verbal_tic` categories. Physical cut protections do not change with AI level.

For review-first use, omit `--approve`. The command writes the source transcript and
`edit-plan.json`, plus `ai-decisions.json` in AI mode, then stops:

```bash
python3 scripts/media_utils.py meeting-cleanup meeting.mp4 cleaned.mp4 \
  --end 600 --language zh
```

Review or edit the plan, then reuse all completed ASR artifacts:

```bash
python3 scripts/media_utils.py meeting-cleanup meeting.mp4 cleaned.mp4 \
  --end 600 --language zh --approve --resume
```

By default, intermediate artifacts live under
`<output-directory>/.media-utils/<output-stem>-meeting-cleanup/`. Use `--work-dir`
to select another location. The sidecar SRT defaults to the cleaned output basename;
override it with `--srt-output`. `--resume` validates `request.json` and refuses to
reuse transcripts or plans when the input identity, trim range, ASR settings, or cleanup
settings changed.

## Dialogue transcription and cleanup

### 1. Transcribe

Use an audio input. Extract audio from a video first when necessary.

```bash
python3 scripts/media_utils.py dialogue transcribe meeting.wav transcript.json \
  --language zh --diarization --speaker-count 3
```

`--speaker-count` requires `--diarization`. Bailian speaker separation works on mono audio;
convert the original video directly to PCM mono unless channel-specific transcription is
intended. Do not insert an AAC/M4A intermediate because encoder priming can shift word
timestamps:

```bash
python3 scripts/media_utils.py audio convert meeting.mp4 meeting-mono.wav \
  --sample-rate 16000 --channels 1
```

### 2. Generate an explicit cut plan

Pass exact removable words or phrases in the default `exact` mode:

```bash
python3 scripts/media_utils.py dialogue plan transcript.json dialogue-plan.json \
  --filler "嗯" --filler "呃" --filler "you know" \
  --max-pause-ms 1200 --keep-pause-ms 300 \
  --min-neighbor-gap-ms 60 \
  --media meeting.mp4 --boundary-search-ms 60
```

Use `--use-default-fillers` only after the user asks for the bundled Chinese/English list.
Exact token matching is deliberate: it avoids guessing whether a word such as “然后” is
semantically necessary.

Use AI semantic selection independently of `meeting-cleanup`:

```bash
python3 scripts/media_utils.py dialogue plan transcript.json dialogue-plan.json \
  --cleanup-mode ai --ai-level conservative --ai-model qwen3.7-max \
  --ai-decisions-output ai-decisions.json \
  --min-neighbor-gap-ms 60 \
  --media meeting.mp4 --boundary-search-ms 60
```

The AI report contains the immutable word index, accepted decisions, rejected decisions
with local rejection reasons, per-level constraints, and raw chunk responses. Long
transcripts are split into overlapping context chunks; only decisions beginning in each
chunk's core range are eligible, then duplicate ID spans are consolidated.

The output uses `media-utils-edit-plan/v1`, sets `approved` to `false`, and contains
second-based `remove` intervals. Show these intervals before editing.

Use `--remove-repetitions` to remove the first token from adjacent exact repetitions by
the same speaker, such as “然后 然后”. Adjust `--repetition-gap-ms` when necessary.
Use `--min-neighbor-gap-ms` to keep filler words that are tightly coarticulated with an
adjacent word. With `--media`, `--boundary-search-ms` moves each proposed boundary inward
to a nearby low-energy point, preserving more of neighboring phonemes.

### 3. Apply after review

```bash
python3 scripts/media_utils.py dialogue apply original.wav dialogue-plan.json cleaned.wav --approve
python3 scripts/media_utils.py dialogue apply original.mp4 dialogue-plan.json cleaned.mp4 --approve
python3 scripts/media_utils.py dialogue apply original.mp4 dialogue-plan.json smooth.mp4 \
  --approve --smooth --crossfade-ms 20
```

Application hard-cuts the approved intervals and re-encodes the result. The same plan can be
applied to the source video when the transcript timebase came from that video's unshifted
audio.

Prefer `--smooth` for conversational video. It normalizes input timestamps, concatenates
audio independently from video, applies an equal-power micro-crossfade at every audio join,
and slightly retimes the concatenated video to the measured audio duration. This avoids
per-segment audio padding caused by frame-quantized video cuts. Keep crossfades short enough
that they do not smear neighboring words; 15–30 ms is a practical starting range.

### 4. Export speaker-labelled SRT

Export subtitles against the original timeline:

```bash
python3 scripts/media_utils.py dialogue srt transcript.json captions.srt
```

Pass the approved edit plan to remove filler tokens and remap every timestamp to the edited
timeline:

```bash
python3 scripts/media_utils.py dialogue srt transcript.json cleaned.srt \
  --plan dialogue-plan.json --speaker-prefix "人物"
```

Each cue uses `人物N：说话内容`. Speaker numbers follow first appearance order and do not
claim real names unless a separate reviewed mapping is available.
The exporter writes UTF-8 with LF line endings and a final blank cue separator. If a player
does not discover the sidecar automatically, validate it by explicitly adding the subtitle;
use `video mux-subtitle` when playback must not depend on filename or directory matching.

Plan-based remapping follows the ideal second-based cut timeline. A large number of video
hard cuts can accumulate frame-boundary rounding in the encoded output. When final subtitle
sync matters, extract the edited video's audio, transcribe that edited audio again, and export
SRT from the second transcript without `--plan`.

## Output behavior

- Existing outputs are rejected unless `--force` is explicit.
- Most transforms support `--dry-run`.
- Always probe the output after timeline edits.
- Preserve the original file; use a new descriptive output name.
