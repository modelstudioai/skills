# model inference

百炼平台提供丰富的模型推理能力，覆盖文本生成、视觉理解、图片生成、视频生成、语音合成、语音识别、语音转语音、向量与重排序、3D 模型生成、音乐生成以及全模态等场景。开发者可以根据业务需求选择合适的模型，通过统一的 API 接入方式（HTTP 或 WebSocket）完成推理调用。

## 文本生成

文本生成是最基础也最常用的推理能力，适用于 AI 智能体、聊天机器人、文档处理、代码生成等场景。推荐从 `qwen3.7-plus` 开始——能力与成本均衡，支持 1M 上下文、完整的 Function Calling 和内置工具。如需最强推理能力可选 `qwen3.7-max`，如需降低成本可尝试 `qwen3.6-flash`，效果接近旗舰且拥有相同的上下文长度和功能支持。详细的模型选型和功能对比参见[文本生成](../../raw/model-user-guide/model-inference/text-generation-model.md)。

百炼同时提供多家第三方文本模型，包括 `deepseek-v4-pro`、`deepseek-v4-flash`、`glm-5.2`、`kimi-k2.7-code`、`MiniMax-M2.5`、`mimo-v2.5-pro` 等，开发者可以在同一平台上按需切换。

### 关键功能

- **思考模式**：通过 `enable_thinking` 参数开启逐步推理，适用于多步数学计算、代码调试、架构规划等需要深度思考的场景。所有 Qwen3 及以上模型均支持。
- **Function Calling 与内置工具**：Function Calling 允许模型调用自定义工具（查询天气、操作数据库等），所有通用模型均支持。内置工具（联网搜索、代码解释器等）无需额外配置即可使用。
- **结构化输出**：获取有效的 JSON 返回，适用于从文本中提取结构化信息。
- **批量推理**：适用于大量请求且对延迟要求不高的场景，可降低请求成本。

### 推荐模型速览

| 模型 ID | 上下文 | 思考模式 | Function Calling | 内置工具 | 结构化输出 |
| --- | --- | --- | --- | --- | --- |
| `qwen3.7-max` | 1M | 支持 | 支持 | 支持 | 不支持 |
| `qwen3.7-plus` | 1M | 支持 | 支持 | 支持 | 支持 |
| `qwen3.6-flash` | 1M | 支持 | 支持 | 支持 | 支持 |
| `deepseek-v4-pro` | 1M | 支持 | 支持 | 不支持 | 不支持 |

## 视觉理解

视觉理解模型支持图像分析、视频理解、OCR 等场景。推荐从 `qwen3.7-plus` 开始，它支持 1M 上下文、最长 2 小时视频、Function Calling 和内置工具。详细信息参见[视觉理解](../../raw/model-user-guide/model-inference/vision-model.md)。

### 图像与视频能力

- **图像分辨率**：大多数模型支持每张图片最高 1600 万像素，Token 计算公式为 `h x w / (32 x 32) + 2`。
- **视频支持**：`qwen3.7-plus`、`qwen3.6-plus`、`qwen3.6-flash` 等支持最长 2 小时/2GB 的视频。
- **OCR 文档提取**：`qwen-vl-ocr` 专为文档、表格、手写内容的文字提取而优化。

### 推荐模型速览

| 模型 ID | 上下文 | 最大视频时长 | Function Calling | 内置工具 | 结构化输出 |
| --- | --- | --- | --- | --- | --- |
| `qwen3.7-plus` | 1M | 2 小时 | 支持 | 支持 | 支持 |
| `qwen3.6-flash` | 1M | 2 小时 | 支持 | 支持 | 支持 |
| `qwen3.5-omni-plus` | 64k | 1 小时 | 支持 | -- | 支持 |

## 图片生成与编辑

百炼提供文生图和图片编辑两类能力。推荐使用 `wan2.7-image-pro`，它在一个模型中集成了文字渲染、品牌色控制、角色一致性多图生成以及图片编辑功能，文生图最高支持 4096x4096 分辨率。详细信息参见[图片生成与编辑](../../raw/model-user-guide/model-inference/image-model.md)。

### 选型建议

| 模型 ID | 适用场景 | 文生图 | 编辑 | 最大分辨率 |
| --- | --- | --- | --- | --- |
| `wan2.7-image-pro` | 文字渲染、品牌色、角色一致性 | 支持 | 支持 | 4096x4096 |
| `z-image-turbo` | 快速生成、低成本、写实人像 | 支持 | 不支持 | 2048x2048 |
| `qwen-image-2.0-pro` | 负向提示词、多图变体 | 支持 | 支持 | 2048x2048 |

> **注意**：如果只需要生成图片且对速度和成本敏感，`z-image-turbo` 的生成速度快约 10 倍，价格约为 `wan2.7-image-pro` 的 1/5。

## 视频生成与编辑

视频生成覆盖文生视频、图生视频、参考生视频、视频编辑和角色动画等场景。文生视频推荐 `happyhorse-1.0-t2v`，支持 1080P 分辨率和最长 15 秒有声视频。详细信息参见[视频生成与编辑](../../raw/model-user-guide/model-inference/video-generate-edit-model.md)。

### 各场景推荐

| 场景 | 推荐模型 | 最大分辨率 | 最大时长 |
| --- | --- | --- | --- |
| 文生视频 | `happyhorse-1.0-t2v` | 1080P | 3-15 秒 |
| 首帧生视频 | `happyhorse-1.0-i2v` | 1080P | 3-15 秒 |
| 首尾帧生视频/视频续写 | `wan2.7-i2v-2026-04-25` | 1080P | 2-15 秒 |
| 参考生视频 | `happyhorse-1.0-r2v` | 1080P | 3-15 秒 |
| 视频编辑 | `happyhorse-1.0-video-edit` | 1080P | 3-15 秒 |
| 动作迁移 | `wan2.2-animate-move` | 720P | 2-30 秒 |

> **注意**：如果需要传入自定义音频文件（如旁白、配乐），文生视频应使用 `wan2.7-t2v-2026-04-25`，图生视频应使用 `wan2.7-i2v-2026-04-25`。HappyHorse 系列默认支持有声视频但不支持自定义音频输入。

## 语音合成（TTS）

语音合成模型将文本转换为自然语音，支持标准语音合成（使用内置音色库）和自定义音色（声音复刻/声音设计）。推荐使用 `cosyvoice-v3.5-plus`，同时支持声音复刻、声音设计和指令控制。详细信息参见[语音合成](../../raw/model-user-guide/model-inference/tts-model.md)。

### 接入方式

- **WebSocket**：双向流式通信，音频边合成边返回，延迟最低。适用于智能客服、语音助手等实时交互场景。
- **HTTP**：发送完整文本，支持流式返回音频。适用于有声阅读、音频内容制作等场景。

### 推荐模型速览

| 模型 ID | 系列 | API | 声音复刻 | 声音设计 | 指令控制 |
| --- | --- | --- | --- | --- | --- |
| `cosyvoice-v3.5-plus` | CosyVoice | WebSocket/HTTP | 支持 | 支持 | 支持 |
| `cosyvoice-v3-plus` | CosyVoice | WebSocket/HTTP | 支持 | 支持 | 不支持 |
| `MiniMax/speech-2.8-hd` | MiniMax | HTTP | 支持 | 不支持 | 不支持 |

## 语音识别（ASR）

语音识别模型将音频转换为文本，支持实时识别（WebSocket 流式输入输出）和非实时识别（HTTP 提交录音文件）。选型时需关注四个维度：实时/非实时、专业术语处理、说话人分离、情感识别。详细信息参见[语音识别](../../raw/model-user-guide/model-inference/asr-model.md)。

### 推荐模型速览

| 模型 ID | 模式 | 精度增强 | 情感识别 | 说话人分离 |
| --- | --- | --- | --- | --- |
| `fun-asr-realtime` | 实时 | 热词 | 不支持 | 不支持 |
| `fun-asr` | 非实时 | 热词 | 不支持 | 支持 |
| `qwen3.5-omni-plus-realtime` | 实时 | Prompt 上下文 | 支持 | 不支持 |
| `qwen3.5-omni-plus` | 非实时 | Prompt 上下文 | 支持 | 不支持 |

> **注意**：`qwen3.5-omni-plus` 不是传统 ASR 模型，而是能理解音频的大语言模型，通过 Prompt 注入上下文即可自适应专业术语，无需热词列表。说话人分离仅 Fun-ASR 非实时模型支持。

## 语音转语音（S2S）

语音转语音场景（语音对话、语音翻译、同声传译等）有两种实现方式：S2S 单模型路线和 Pipeline（ASR + LLM + TTS）路线。S2S 延迟更低、能感知语调和情绪；Pipeline 支持自定义音色且每个阶段可独立选型。详细信息参见[语音转语音](../../raw/model-user-guide/model-inference/s2s-model.md)。

### S2S 场景推荐

| 场景 | 推荐模型 | API |
| --- | --- | --- |
| 语音助手/客服对话 | `qwen3.5-omni-plus-realtime` | WebSocket |
| 成本敏感的对话 | `qwen3.5-omni-flash-realtime` | WebSocket |
| 同声传译/直播翻译 | `qwen3.5-livetranslate-flash-realtime` | WebSocket |
| 视频配音/播客翻译 | `qwen3-livetranslate-flash` | HTTP |

### 翻译能力

- **Qwen3.5-Livetranslate**：支持 60 种语言互译（29 种音频+文本，31 种仅文本），约 3 秒延迟，开箱即用。
- **Qwen3.5-Omni**：29 种输出语言 + 7 种中文方言，支持联网搜索和术语注入。
- **Qwen3-Omni-Flash**：11 种输出语言 + 8 种中文方言，成本更低。

## 全模态

全模态模型能同时理解文本、音频、图片和视频并输出文本和语音。提供三个系列：Qwen3.5-Omni（旗舰，能力最全）、Qwen3-Omni-Flash（轻量，成本低，支持思考模式）、Qwen3.5-Livetranslate（专业翻译）。详细信息参见[全模态](../../raw/model-user-guide/model-inference/omni.md)。

### 场景选型

| 场景 | 推荐模型 | API |
| --- | --- | --- |
| 实时语音/视频对话 | `qwen3.5-omni-plus-realtime` | WebSocket |
| 音视频内容分析 | `qwen3.5-omni-plus` | HTTP |
| 轻量音视频分析 | `qwen3-omni-flash` | HTTP |
| 实时语音翻译 | `qwen3.5-livetranslate-flash-realtime` | WebSocket |
| 音视频文件翻译 | `qwen3-livetranslate-flash` | HTTP |

Qwen3.5-Omni 在 S2S 路线下还附带 Function Calling、联网搜索等能力（联网搜索与 Function Calling 不可同时开启）。

## 向量与重排序

向量（Embedding）和重排序（Rerank）模型是 RAG [检索增强生成](../concepts/rag.md)的核心组件。详细信息参见[向量与重排序](../../raw/model-user-guide/model-inference/embedding-rerank-model.md)。

### 文本 Embedding

纯文本搜索、RAG 或聚类场景推荐 `text-embedding-v4`，支持 64~2048 维，最大 8192 Token。维度选择建议：大规模搜索选 256/512 维，通用场景选 1024 维（默认），高精度场景选 1536/2048 维。

### 多模态 Embedding

跨模态检索（文本搜图片/视频）推荐 `qwen3-vl-embedding`（融合+独立向量）或 `tongyi-embedding-vision-plus`（独立向量）。

### 重排序

- **纯文本重排序**：`qwen3-rerank`，支持 100+ 语言，最多 500 个文档。
- **多模态重排序**：`qwen3-vl-rerank`，支持文本、图片和视频混合排序。

## 3D 模型生成

通过百炼平台调用 Tripo 模型，支持文生 3D、单图生 3D 和多图生 3D 三种模式。采用异步任务方式调用：先提交生成任务获取 `task_id`，再轮询任务状态获取结果。详细信息参见[Tripo 3D模型生成](../../raw/model-user-guide/model-inference/tripo-3d-generation-guide.md)。

| 模型 | 产物最高面数 | 速度 | 适用场景 |
| --- | --- | --- | --- |
| `Tripo/Tripo-H3.1` | 200 万面 | 较慢 | 影视级渲染、高精度数字资产 |
| `Tripo/Tripo-P1.0` | 2 万面 | 更快 | 快速预览、游戏/AR、实时应用 |

> **注意**：3D 模型生成目前仅适用于华北2（北京）地域，必须使用该地域的 API Key。`prompt`、`image`、`images` 三个输入字段互斥，每次请求只能选一种。

## 音乐生成

百聆音乐生成大模型（Fun 音乐大模型）支持通过提示词或歌词生成整首歌曲，支持男/女声演唱，中文和英文歌词。可用模型为 `fun-music-v1` 和 `fun-music-preview`。详细信息参见[音乐生成](../../raw/model-user-guide/model-inference/fun-music.md)。

> **注意**：音乐生成模型目前处于邀测阶段，需要在模型广场申请开通，且仅在华北2（北京）地域可用。`lyrics` 和 `prompt` 参数必须至少提供一个；当同时传入时仅 `lyrics` 生效。

## 通用使用指南

### API 接入方式

百炼模型推理统一通过 DashScope API 接入，基础地址为 `https://dashscope.aliyuncs.com`。大部分模型兼容 OpenAI API 格式。调用前需要：

1. 开通对应模型服务
2. 获取 API Key 并配置到环境变量（`DASHSCOPE_API_KEY`）

### [异步任务模式](../concepts/async-task-pattern.md)

图片生成、视频生成、3D 模型生成和音乐生成等耗时较长的任务采用异步方式：提交任务获取 `task_id`，然后轮询任务状态直到完成。建议轮询间隔 15 秒，也可配置异步任务回调替代轮询。

### 模型版本管理

每个模型都有主线版本（如 `qwen3.7-plus`）和日期快照版本（如 `qwen3.7-plus-2026-05-26`）。主线版本会随时间更新到最新版本，快照版本锁定特定日期的模型行为。生产环境建议使用快照版本以保证稳定性。

## 来源文档

- [视觉理解](../../raw/model-user-guide/model-inference/vision-model.md)
- [视频生成与编辑](../../raw/model-user-guide/model-inference/video-generate-edit-model.md)
- [文本生成](../../raw/model-user-guide/model-inference/text-generation-model.md)
- [图片生成与编辑](../../raw/model-user-guide/model-inference/image-model.md)
- [Tripo 3D模型生成](../../raw/model-user-guide/model-inference/tripo-3d-generation-guide.md)
- [语音合成](../../raw/model-user-guide/model-inference/tts-model.md)
- [音乐生成](../../raw/model-user-guide/model-inference/fun-music.md)
- [语音识别](../../raw/model-user-guide/model-inference/asr-model.md)
- [语音转语音](../../raw/model-user-guide/model-inference/s2s-model.md)
- [向量与重排序](../../raw/model-user-guide/model-inference/embedding-rerank-model.md)
- [全模态](../../raw/model-user-guide/model-inference/omni.md)


