# novel-game

> [中文版 / Chinese →](README.zh.md)

Turn novels and stories into browser-based interactive fiction games
(React SPA) — with AI-generated video/image assets, optional TTS narration,
programmatic audio, and branching storylines.

## Features

- **Branching narrative engine** — multiple endings, flags system, collectible archives
- **AI asset generation** — character portraits and cutscenes via video (`bl video generate` / `bl video ref`) or image (`bl image generate`), mixable
- **Optional TTS narration** — scene narration and character monologues via `bl speech synthesize`
- **Programmatic audio** — BGM and SFX generated entirely with Web Audio API, zero external dependencies
- **Save system** — auto-save + 3 manual save slots (localStorage)
- **Mobile-first** — portrait layout, touch-optimized, safe-area support
- **Multiple UI themes** — pixel art / cyberpunk / ink-wash Chinese / minimal modern

## Prerequisites

- [Alibaba Cloud Model Studio CLI (`bl`)](https://bailian.aliyun.com/cli/install.md) — AI asset generation (video/image/speech)
- Node.js + npx — React project initialization

## Usage

In Claude Code (or any skill-aware agent), type:

```
/novel-game Adapt "The Three-Body Problem" into an interactive novel, cyberpunk style, 30-minute playthrough
```

The skill will:
1. Ask key design decisions (game type, UI style, length, asset mode)
2. Design the story structure with branching choices
3. Scaffold a React project with all components
4. Generate AI assets (video/image/speech) via `bl` CLI
5. Launch a dev server for browser testing

## Project structure (generated)

```
src/
├── components/       # UI components (TypeWriter, GameScene, ChoicePanel, SaveLoadPanel, ...)
├── data/             # Story graph, characters, archives, asset index
├── hooks/            # useGameState (reducer + hash routing + save), useAudio (Web Audio)
└── styles/           # Theme CSS (cyberpunk, pixel, ink-wash, ...)
scripts/
└── generate-assets.sh  # bl CLI asset generation script (supports parallel generation)
public/assets/          # Downloaded AI-generated asset files
```

## How it works

- **Story data** (`story.js`) defines a scene graph — each scene has text segments, choices with flag mutations, and optional cutscene/archive triggers
- **Game state** is managed via `useReducer` with hash-based routing for scene navigation
- **Character portraits** support video (5-second looping 720P) or image (with CSS breathing animation), auto-detected
- **Cutscenes** support video (full-screen playback) or image (Ken Burns pan/zoom effect), auto-detected
- **Save system** — auto-save after each choice + 3 manual save slots in localStorage
- **BGM** uses fixed MIDI pitch arrays with multi-voice layering, convolution reverb, and ADSR envelopes
- **SFX** includes noise-pulse typing sounds, sweep + chord archive unlocks, and arpeggio scene transitions
- **TTS narration** (optional) — pre-generated MP3 files play automatically during scenes
