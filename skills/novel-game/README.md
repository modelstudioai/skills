# novel-game

> [中文版 / Chinese →](README.zh.md)

Turn novels and stories into browser-based interactive fiction games
(React SPA) — with AI-generated video portraits, cutscenes,
programmatic audio, and branching storylines.

## Features

- **Branching narrative engine** — multiple endings, flags system, collectible archives
- **AI asset generation** — character portraits and cutscene videos via `bl video generate` / `bl video ref`
- **LLM-assisted writing** — plot extraction, scene text generation, video prompt authoring via `bl text chat`
- **Programmatic audio** — BGM and SFX generated entirely with Web Audio API, zero external dependencies
- **Multiple UI themes** — pixel art / cyberpunk / ink-wash Chinese / minimal modern

## Prerequisites

- [Alibaba Cloud Model Studio CLI (`bl`)](https://bailian.aliyun.com/cli/install.md) — AI asset generation and LLM calls
- Node.js + npx — React project initialization

## Usage

In Claude Code (or any skill-aware agent), type:

```
/novel-game Adapt "The Three-Body Problem" into an interactive novel, cyberpunk style, 30-minute playthrough
```

The skill will:
1. Ask key design decisions (game type, UI style, length, AI assets)
2. Design the story structure with branching choices
3. Scaffold a React project with all components
4. Generate AI video assets (portraits + cutscenes) via `bl` CLI
5. Launch a dev server for browser testing

## Project structure (generated)

```
src/
├── components/       # UI components (TypeWriter, GameScene, ChoicePanel, ...)
├── data/             # Story graph, characters, archives
├── hooks/            # useGameState (reducer + hash routing), useAudio (Web Audio)
└── styles/           # Theme CSS (cyberpunk, pixel, ink-wash, ...)
scripts/
└── generate-assets.sh  # bl CLI asset generation script
public/assets/          # Downloaded AI-generated video files
```

## How it works

- **Story data** (`story.js`) defines a scene graph — each scene has text segments, choices with flag mutations, and optional cutscene/archive triggers
- **Game state** is managed via `useReducer` with hash-based routing for scene navigation
- **Character portraits** are 5-second looping videos (720P) displayed in a sidebar; fallback to text initials when videos aren't available
- **Cutscenes** are 5-second 1080P videos played as full-screen overlays at key story moments
- **BGM** uses fixed MIDI pitch arrays with multi-voice layering, convolution reverb, and ADSR envelopes
- **SFX** includes noise-pulse typing sounds, sweep + chord archive unlocks, and arpeggio scene transitions
