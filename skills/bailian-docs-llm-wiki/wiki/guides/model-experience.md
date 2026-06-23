# model experience

百炼平台的多模态体验模型覆盖视频生成与编辑、语音合成、语音识别三大场景。开发者可按"先定场景、再选模型"的思路，从 HappyHorse / Wan / CosyVoice / Qwen-TTS / Fun-ASR / Qwen-ASR 等系列中选择合适的模型 ID，通过 WebSocket 或 HTTP 接入。

## 视频生成与编辑

视频模型支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑与角色动画等场景，详见[视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)。

### 文生视频

- 推荐使用 `happyhorse-1.1-t2v`，支持 1080P、单片段 3–15 秒，输出有声视频。
- 如需传入自定义音频文件（旁白、配乐），推荐 `wan2.7-t2v-2026-04-25`（2–15 秒、30 fps）。

### 图生视频

- 首帧生视频：`happyhorse-1.1-i2v`（有声、1080P、3–15 秒）；需自定义音频时用 `wan2.7-i2v-2026-04-25`。
- 首尾帧生视频：用 `wan2.7-i2v-2026-04-25` 串联片段（上一片段末帧作为下一片段首帧），适合叙事、产品演示、教程。
- 参考生视频：`happyhorse-1.1-r2v` 保持角色一致性；需自定义音色或视频参考主体时用 `wan2.7-r2v`。

### 视频编辑与角色动画

- 视频编辑（风格转换、元素替换）：`happyhorse-1.0-video-edit`；特效/运镜复刻用 `wan2.7-videoedit`。
- 动作迁移（将参考视频动作迁移到静态人物）：`wan2.2-animate-move`，提供 wan-pro（接近真实拍摄）与 wan-std（更快更省）两种模式。
- 视频中替换人物：`wan2.2-animate-mix`，同样支持 pro/std 模式。

### 视频模型规格速查

| 模型 ID | 类型 | 最大分辨率 | 最大时长 |
| --- | --- | --- | --- |
| `happyhorse-1.1-t2v` / `happyhorse-1.1-i2v` / `happyhorse-1.1-r2v` | 文生/首帧/参考生 | 720P, 1080P | 3–15 秒 |
| `wan2.7-t2v-2026-04-25` / `wan2.7-i2v-2026-04-25` | 文生/图生（自定义音频） | 720P, 1080P | 2–15 秒 |
| `wan2.7-r2v` | 参考生视频 | 720P, 1080P | 2–10 秒 |
| `happyhorse-1.0-video-edit` / `wan2.7-videoedit` | 视频编辑 | 720P, 1080P | 3–15 秒 / 2–10 秒 |
| `wan2.2-animate-move` / `wan2.2-animate-mix` | 角色动画/替换 | 720P | 2–30 秒 |

Wan 2.1 系列（如 `wan2.1-t2v-plus`、`wan2.1-i2v-turbo`）无音频输出，官方推荐升级到 Wan 2.7。

## 语音合成

语音合成模型将文本转为自然语音，按"标准音色"还是"自定义音色"选择，详见[语音合成](../../raw/model-user-guide/model-experience/tts-model.md)。

### 选型决策

- **标准语音合成**：内置音色库即选即用，适合智能客服、有声阅读、电商直播。推荐 `cosyvoice-v3-plus`、`MiniMax/speech-2.8-hd`。
- **自定义音色**：
  - **声音复刻**：提供音频样本，合成音色与原说话人高度相似。推荐 `cosyvoice-v3.5-plus`、`cosyvoice-v3.5-flash`、`MiniMax/speech-2.8-hd`。
  - **声音设计**：用文字描述期望音色（如"温暖的低音女声"）从零生成。推荐 `cosyvoice-v3.5-plus`、`cosyvoice-v3.5-flash`。
  - 音色注册与管理服务：`voice-enrollment`。

### 接入方式

- **WebSocket**：双向流式，音频边合成边返回，延迟最低，适合智能客服、语音助手、呼叫中心。
- **HTTP**：发送完整文本，支持流式返回，适合有声阅读、音频内容制作。

CosyVoice 系列同一模型名称同时支持 WebSocket 和 HTTP；Qwen 系列通过后缀区分，`-realtime` 为 WebSocket，无后缀为 HTTP。CosyVoice 与 Qwen 的 WebSocket 模型可通过 [DashScope SDK](../concepts/dashscope-sdk.md)（Java、Python）接入，CosyVoice 还支持 Android/iOS SDK。

### 指令控制

用自然语言动态控制语速、情绪、风格，例如"用温柔的语气，语速稍慢"。支持的模型：CosyVoice（`cosyvoice-v3.5-plus`、`cosyvoice-v3.5-flash`、`cosyvoice-v3-flash`）和 Qwen-TTS（`qwen3-tts-instruct-flash-realtime`、`qwen3-tts-instruct-flash`）。

### 推荐 TTS 模型

| 模型 ID | 系列 | API | 声音复刻 | 声音设计 | 指令控制 |
| --- | --- | --- | --- | --- | --- |
| `cosyvoice-v3.5-plus` | CosyVoice | WebSocket / HTTP | 支持 | 支持 | 支持 |
| `cosyvoice-v3-plus` | CosyVoice | WebSocket / HTTP | 支持 | 支持 | 不支持 |
| `MiniMax/speech-2.8-hd` | MiniMax | HTTP | 支持 | 不支持 | 不支持 |

> **注意**：`cosyvoice-v3.5-plus` 与 `cosyvoice-v3.5-flash` 不提供系统音色，需通过声音复刻或声音设计创建音色后方可使用。

Qwen3-TTS 进一步拆分为 Flash（系统音色）、Instruct-Flash（指令控制）、VC（声音复刻）、VD（声音设计）四类，按需选择对应模型 ID。Qwen-TTS 旧版（如 `qwen-tts`、`qwen-tts-realtime`）按 Token 计费，建议迁移到 Qwen3-TTS。

## 语音识别

语音识别模型覆盖实时与非实时两类，详见[语音识别](../../raw/model-user-guide/model-experience/asr-model.md)。

### 选型决策维度

1. **实时还是非实时**
   - 实时（WebSocket，流式输入/输出）：适合实时字幕、语音助手、会议转写。推荐 `fun-asr-realtime`（热词、方言）或 `qwen3.5-omni-plus-realtime`（Prompt 上下文、多语种）。
   - 非实时（HTTP，提交文件）：适合呼叫中心录音、播客、访谈。推荐 `fun-asr`（热词、说话人分离）或 `qwen3.5-omni-plus`（Prompt 上下文、多语种）。
2. **处理专业术语**
   - Prompt 上下文注入：在系统提示词中描述领域背景，模型自适应，延迟略高。用 `qwen3.5-omni-plus-realtime` / `qwen3.5-omni-plus`。
   - 热词：带权重的词汇表，适合稳定术语。用 `fun-asr-realtime` / `fun-asr`。
3. **说话人分离**：仅 Fun-ASR 非实时模型（`fun-asr`、`fun-asr-mtl`）支持。
4. **情感识别**：Qwen-ASR 与 Qwen3.5-Omni 系列支持。实时推荐 `qwen3-asr-flash-realtime`，非实时推荐 `qwen3-asr-flash-filetrans`。

### 推荐 ASR 模型

| 模型 ID | 模式 | API | 精度增强 | 情感识别 | 说话人分离 | 音频上限 |
| --- | --- | --- | --- | --- | --- | --- |
| `fun-asr-realtime` | 实时 | WebSocket | 热词 | 不支持 | 不支持 | 无限制 |
| `fun-asr` | 非实时 | HTTP | 热词 | 不支持 | 支持 | 12 小时 / 2 GB |
| `qwen3.5-omni-plus-realtime` | 实时 | WebSocket | Prompt 上下文 | 支持 | 不支持 | 2 小时 |
| `qwen3.5-omni-plus` | 非实时 | HTTP（OpenAI 兼容） | Prompt 上下文 | 支持 | 不支持 | 3 小时 / 2 GB |

Fun-ASR 与 Qwen-ASR 的实时模型可通过 [DashScope SDK](../concepts/dashscope-sdk.md)（Java、Python）接入，Fun-ASR 还支持 Android/iOS SDK。

### 音频规格要点

- 实时模型均为单声道输入，支持 `pcm`、`wav`、`mp3`、`opus`、`aac`、`amr` 等格式；Qwen-ASR-Realtime 限 `pcm`/`opus`，采样率 8 kHz 或 16 kHz。
- 非实时模型通过公网可访问的文件 URL 提交（部分支持 Base64 或本地路径），Fun-ASR 单文件 ≤2 GB / ≤12 小时（启用说话人分离建议 ≤2 小时），Qwen3-ASR-Flash-Filetrans ≤2 GB / ≤12 小时，Qwen3-ASR-Flash ≤10 MB / ≤5 分钟。

Paraformer（如 `paraformer-realtime-v2`、`paraformer-v2`）为较早一代模型，官方建议迁移到 Fun-ASR 或 Qwen-ASR；`gummy-realtime-v1`、`sensevoice-v1` 等已计划下线，仅供存量业务参考。

## 限制和注意事项

- 视频模型单片段时长普遍为 2–15 秒（角色动画可达 30 秒），分辨率上限 1080P；Wan 系列为 30 fps，HappyHorse 为 24 fps。Wan 2.1 及更早系列无音频输出。
- 自定义音频文件需求优先选 Wan 2.7 系列（如 `wan2.7-t2v-2026-04-25`、`wan2.7-i2v-2026-04-25`），HappyHorse 1.1 默认输出有声视频但不支持自定义音频输入。
- TTS 中 `cosyvoice-v3.5-plus` / `cosyvoice-v3.5-flash` 无系统音色，必须先通过声音复刻或声音设计创建音色。
- ASR 说话人分离仅 Fun-ASR 非实时模型支持；情感识别仅 Qwen-ASR 与 Qwen3.5-Omni 系列支持。
- Qwen3.5-Omni / Qwen3-Omni 不是专用 ASR，是能理解音频的大语言模型，其音频规格与支持语言以各自用户指南为准。
- 部分旧版模型（Paraformer、Qwen-TTS 旧版、`gummy-*`、`sensevoice-v1`）已计划下线或按 Token 计费，新业务请优先使用推荐模型。

## 来源文档

- [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)
- [语音合成](../../raw/model-user-guide/model-experience/tts-model.md)
- [语音识别](../../raw/model-user-guide/model-experience/asr-model.md)


