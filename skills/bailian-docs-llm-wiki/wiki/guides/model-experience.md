# model experience

百炼平台模型体验中心提供覆盖文本、视觉、音频、视频、3D、向量等多种模态的模型服务，开发者可根据业务场景按需选型并快速接入。本页按模态维度汇总各类模型的核心能力、推荐选型和关键参数，帮助开发者在一个页面内完成全景了解。

## 文本生成

文本生成模型适用于聊天机器人、内容生成、摘要总结、文档处理、AI Agent 等场景。推荐从 `qwen3.7-plus` 入手，能力与成本均衡，拥有 1M 上下文窗口和完整内置工具支持。如需最强推理能力，可选择 `qwen3.7-max`；追求低成本则可用 `qwen3.6-flash`，效果接近旗舰模型。

### 核心能力

| 能力 | 说明 |
|------|------|
| 思考模式 | 通过 `enable_thinking` 参数开启逐步推理，适用于多步数学计算、代码调试等场景。所有 Qwen3 及以上模型均支持 |
| Function Calling | 所有通用模型均支持自定义工具调用 |
| 内置工具 | 联网搜索、代码解释器、网页抓取等，无需复杂配置 |
| 结构化输出 | 返回有效 JSON，适合信息提取场景 |
| 批量推理 | 大量请求且对延迟要求不高的场景，可降低成本 |

### 主要推荐模型

| 模型 ID | 上下文 | 定位 |
|---------|--------|------|
| `qwen3.7-max` | 1M | 最强推理能力 |
| `qwen3.7-plus` | 1M | 能力与成本均衡（推荐起步） |
| `qwen3.6-flash` | 1M | 低成本，效果接近旗舰 |
| `deepseek-v4-pro` / `deepseek-v4-flash` | 1M | 三方模型 |

从 GPT、Claude 或 Gemini 迁移时，可按能力档对位选择：高能力对应 `qwen3.7-max`，平衡对应 `qwen3.7-plus`，轻量对应 `qwen3.6-flash`。详细模型列表和功能对比参见[文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)。

## 视觉理解

视觉理解模型支持图像分析、视频理解和 OCR 文档提取。推荐从 `qwen3.7-plus` 开始，支持 1M 上下文、最长 2 小时视频、Function Calling 和内置工具。

### 关键参数

- **图像分辨率**：大多数模型支持每张图片最高 1600 万像素，[Token](../concepts/token.md) 数按 `h x w / (32 x 32) + 2` 计算
- **视频支持**：最长 2 小时 / 2GB（Qwen3.7、Qwen3.6、Qwen3.5 系列），最长 1 小时 / 2GB（Qwen3.5-Omni 系列，同时支持音频输入）
- **OCR 专用**：`qwen-vl-ocr` 针对文档、表格、手写内容优化

详细参数和完整模型列表参见[视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)。

## 视频生成与编辑

百炼提供文生视频、图生视频、参考生视频、视频编辑和角色动画等能力。

### 按场景选型

| 场景 | 推荐模型 | 最大分辨率 | 最大时长 |
|------|---------|-----------|---------|
| 文生视频 | `happyhorse-1.1-t2v` | 1080P | 3-15 秒 |
| 首帧生视频 | `happyhorse-1.1-i2v` | 1080P | 3-15 秒 |
| 首尾帧生视频（长视频串联） | `wan2.7-i2v-2026-04-25` | 1080P | 2-15 秒 |
| 参考生视频（角色一致性） | `happyhorse-1.1-r2v` | 1080P | 3-15 秒 |
| 视频编辑 | `happyhorse-1.0-video-edit` | 1080P | 3-15 秒 |
| 动作迁移 | `wan2.2-animate-move` | 720P | 2-30 秒 |

如需传入自定义音频文件，推荐使用 Wan 2.7 系列。详细说明参见[视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)。

## 图片生成与编辑

推荐使用 `wan2.7-image-pro`，集成了文字渲染、品牌色控制、角色一致性多图生成和图片编辑功能，文生图最高 4096x4096，编辑最高 2048x2048。

| 模型 ID | 适用场景 | 最大分辨率 |
|---------|---------|-----------|
| `wan2.7-image-pro` | 文字渲染、品牌色、角色一致性、多图编辑 | 4096x4096 |
| `z-image-turbo` | 快速生成、低成本、写实人像 | 2048x2048 |
| `qwen-image-2.0-pro` | 负向提示词、最多 6 张变体 | 2048x2048 |

详细使用方式参见[图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)。

## 3D 模型生成

通过 Tripo 模型支持文生 3D、单图生 3D 和多图生 3D 三种模式，输出 GLB 格式的 PBR 材质模型。

| 模型 | 最高面数 | 速度 | 适用场景 |
|------|---------|------|---------|
| `Tripo/Tripo-H3.1` | 200 万面 | 较慢 | 影视级渲染、高精度数字资产 |
| `Tripo/Tripo-P1.0` | 2 万面 | 更快 | 快速预览、游戏/AR 场景 |

> **注意**：3D 生成为异步任务，通常需要数分钟，建议轮询间隔 15 秒。该服务仅在华北2（北京）地域可用。

调用流程为提交任务获取 `task_id`，再轮询任务状态直到 `SUCCEEDED`。详细 API 示例参见[Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。

## 语音合成（TTS）

语音合成模型将文本转换为自然语音，支持标准内置音色和自定义音色两种模式。

### 选型要点

- **标准语音合成**（内置音色）：推荐 `cosyvoice-v3-plus` 或 `MiniMax/speech-2.8-hd`，选择即用
- **声音复刻**（从音频样本复刻）：推荐 `cosyvoice-v3.5-plus` 或 `MiniMax/speech-2.8-hd`
- **声音设计**（文字描述创建音色）：推荐 `cosyvoice-v3.5-plus`
- **指令控制**（自然语言控制语速、情绪）：CosyVoice 系列和 Qwen3-TTS-Instruct 系列支持

### 接入方式

- **WebSocket**：流式输入和输出，延迟最低，适用于实时交互场景
- **HTTP**：发送完整文本，支持流式返回音频，适用于有声阅读等场景

详细说明参见[语音合成](../../raw/model-user-guide/model-experience/tts-model.md)。

## 语音转语音（S2S）

S2S 模型提供端到端的"语音输入到语音输出"能力，相比 ASR + LLM + TTS 的 Pipeline 方案延迟更低，且能感知语调和情绪。

| 场景 | 推荐模型 | API |
|------|---------|-----|
| 语音助手 / 客服对话 | `qwen3.5-omni-plus-realtime` | WebSocket |
| 成本敏感的对话 | `qwen3.5-omni-flash-realtime` | WebSocket |
| 同声传译 / 直播翻译 | `qwen3.5-livetranslate-flash-realtime` | WebSocket |
| 视频配音 / 播客翻译 | `qwen3-livetranslate-flash` | HTTP |

Qwen3.5-Livetranslate 支持 60 种语言互译。当需要自定义音色时，应选择 Pipeline 路线。详细对比参见[语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)。

## 语音识别（ASR）

语音识别模型将语音转换为文本，支持实时识别和录音文件识别。

### 选型决策

| 维度 | 推荐 |
|------|------|
| 实时识别 + 热词增强 | `fun-asr-realtime`（WebSocket） |
| 非实时识别 + 说话人分离 | `fun-asr`（HTTP，最长 12 小时 / 2GB） |
| 实时识别 + Prompt 上下文 | `qwen3.5-omni-plus-realtime`（WebSocket） |
| 情感识别 | `qwen3-asr-flash-realtime` / `qwen3-asr-flash-filetrans` |

Fun-ASR 系列支持热词（预配置术语列表），Qwen3.5-Omni 系列支持 Prompt 上下文注入（每次请求自适应，无需预配置）。详细说明参见[语音识别](../../raw/model-user-guide/model-experience/asr-model.md)。

## 音乐生成

Fun-Music 支持通过提示词描述或自定义歌词生成完整歌曲（含人声）或纯音乐，输出 MP3 或 WAV 格式。

| 模型 | 特点 |
|------|------|
| `fun-music-v1` | 支持 [prompt](prompt.md) 或 lyrics 输入，支持选择男/女声 |
| `fun-music-preview` | [prompt](prompt.md) 必选，不支持 gender 参数 |

> **注意**：该模型目前处于邀测阶段，仅在华北2（北京）地域可用，需申请开通。

详细 API 调用示例参见[音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)。

## 向量与重排序

向量（Embedding）和重排序（Rerank）模型用于语义搜索、RAG 检索和跨模态匹配。

### 文本 Embedding

推荐 `text-embedding-v4`，支持 64 至 2048 维（默认 1024），最大 8192 [Token](../concepts/token.md)。维度选择建议：大规模搜索选 256/512 维，通用场景选 1024 维，高精度选 1536/2048 维。

### [多模态](../concepts/multimodal.md) Embedding

- **融合向量**（图文混合检索）：`qwen3-vl-embedding`
- **独立向量**（跨模态搜索）：`tongyi-embedding-vision-plus`

### 重排序

- **纯文本**：`qwen3-rerank`，支持 100+ 语言，最多 500 个文档
- **[多模态](../concepts/multimodal.md)**：`qwen3-vl-rerank`，支持文本、图片和视频混合排序

详细说明参见[向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)。

## 全模态（Omni）

全模态模型同时理解文本、音频、图片和视频，并输出文本和语音。三个模型系列分别定位不同场景：

- **Qwen3.5-Omni**：旗舰，能力最全，支持 Function Calling 和联网搜索
- **Qwen3-Omni-Flash**：轻量低成本，支持深度推理（思考模式）
- **Qwen3.5-Livetranslate**：专业翻译，60 种语言，约 3 秒延迟

内容分析场景中，Qwen3.5-Omni 支持音频最长 3 小时、视频最长 1 小时。详细使用场景和模型对比参见[全模态](../../raw/model-user-guide/model-experience/omni.md)。

## 通用注意事项

- **上下文窗口**：100 万 [Token](../concepts/token.md) 约相当于 70 万个汉字。`qwen3.7-plus` 和 `qwen3.6-flash` 均支持 1M 上下文，常规任务 128k-256k 已足够
- **API 兼容性**：Qwen3.5-Omni 和 Qwen-ASR 等模型支持 OpenAI 兼容的 HTTP API，可降低迁移成本
- **模型版本锁定**：生产环境建议使用带日期后缀的快照版本（如 `qwen3.7-plus-2026-05-26`）以获得确定性行为
- **区域限制**：部分服务（如 Tripo 3D、Fun-Music）仅在华北2（北京）地域可用

## 来源文档

- [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)
- [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)
- [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)
- [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)
- [Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)
- [语音合成](../../raw/model-user-guide/model-experience/tts-model.md)
- [语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)
- [语音识别](../../raw/model-user-guide/model-experience/asr-model.md)
- [音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)
- [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)
- [全模态](../../raw/model-user-guide/model-experience/omni.md)


