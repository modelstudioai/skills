# model inference

百炼平台提供覆盖文本、图片、视频、音频、3D 等多种模态的模型推理能力，开发者可通过统一的 API 调用各类模型完成生成、理解、转换等任务。本页面汇总了各模态下的模型选型建议、关键参数与使用方式，帮助开发者快速定位适合自身场景的模型。

## 文本生成

文本生成是最基础的推理能力，适用于聊天机器人、内容生成、摘要总结、代码编写等场景。推荐从 `qwen3.7-plus` 起步，它在能力与成本之间取得平衡，拥有 1M 上下文窗口和完整的内置工具支持。如需最强推理能力可选 `qwen3.7-max`，如需降低成本可尝试 `qwen3.6-flash`。详见 [文本生成](../../raw/model-user-guide/model-inference/text-generation-model.md)。

### 核心能力

- **思考模式**：通过 `enable_thinking` 参数开启逐步推理，适用于多步数学计算、代码调试等场景。所有 Qwen3 及以上模型均支持。
- **Function Calling 与内置工具**：所有通用模型均支持 Function Calling；`qwen3.7-plus`、`qwen3.6-flash` 等还支持联网搜索、代码解释器等内置工具。
- **结构化输出**：获取有效 JSON 返回，适用于信息抽取场景。
- **批量推理**：大量请求且对延迟要求不高时，可降低请求成本。

### 推荐模型

| 模型 | 上下文 | 思考模式 | Function Calling | 内置工具 | 结构化输出 |
|------|--------|----------|-----------------|----------|-----------|
| `qwen3.7-max` | 1M | 支持 | 支持 | 支持 | 不支持 |
| `qwen3.7-plus` | 1M | 支持 | 支持 | 支持 | 支持 |
| `qwen3.6-flash` | 1M | 支持 | 支持 | 支持 | 支持 |
| `deepseek-v4-pro` | 1M | 支持 | 支持 | 不支持 | 不支持 |

百炼还提供第三方模型如 `deepseek-v4-flash`、`glm-5.1`、`kimi-k2.6`、`MiniMax-M2.5` 等。

## 视觉理解

视觉理解模型支持图像分析、视频理解和 OCR 等场景。推荐使用 `qwen3.7-plus`（1M 上下文、最长 2 小时视频），或 `qwen3.6-flash` 以降低成本。详见 [视觉理解](../../raw/model-user-guide/model-inference/vision-model.md)。

- **图像分辨率**：大多数模型支持每张图片最高 1600 万像素，Token 数计算公式为 `h x w / (32 x 32) + 2`。
- **视频支持**：`qwen3.7-plus`、`qwen3.6-flash` 等支持最长 2 小时 / 2GB 视频。
- **OCR**：`qwen-vl-ocr` 专为文档、表格、手写内容的文字提取优化。

## 图片生成与编辑

推荐使用 `wan2.7-image-pro`，集成文字渲染、品牌色控制、角色一致性多图生成和图片编辑功能，文生图最高支持 4096x4096 分辨率。详见 [图片生成与编辑](../../raw/model-user-guide/model-inference/image-model.md)。

| 模型 | 适用场景 | 文生图 | 编辑 | 最大分辨率 |
|------|---------|--------|------|-----------|
| `wan2.7-image-pro` | 文字渲染、品牌色、角色一致性 | 支持 | 支持 | 4096x4096（文生图） |
| `z-image-turbo` | 快速生成、低成本、写实人像 | 支持 | 不支持 | 2048x2048 |
| `qwen-image-2.0-pro` | 负向提示词、最多 6 张变体 | 支持 | 支持 | 2048x2048 |

## 视频生成与编辑

百炼提供文生视频、图生视频、参考生视频和视频编辑等能力。详见 [视频生成与编辑](../../raw/model-user-guide/model-inference/video-generate-edit-model.md)。

| 模型 | 适用场景 | 最大分辨率 | 最大时长 |
|------|---------|-----------|---------|
| `happyhorse-1.0-t2v` | 文生视频（有声） | 1080P | 3-15 秒 |
| `happyhorse-1.0-i2v` | 首帧生视频（有声） | 1080P | 3-15 秒 |
| `wan2.7-i2v-2026-04-25` | 首尾帧生视频、视频续写 | 1080P | 2-15 秒 |
| `happyhorse-1.0-video-edit` | 视频编辑 | 1080P | 3-15 秒 |
| `wan2.2-animate-move` | 动作迁移到静态人物 | 720P | 2-30 秒 |

> **注意**：Wan 2.7 系列支持自定义音频文件输入，HappyHorse 1.0 系列自动生成音频但不支持自定义音频。如需传入自定义音频，请使用 Wan 2.7 对应模型。

## 3D 模型生成

通过 Tripo 模型支持文生 3D、单图生 3D 和多图生 3D 三种模式。详见 [Tripo 3D 模型生成](../../raw/model-user-guide/model-inference/tripo-3d-generation-guide.md)。

- `Tripo/Tripo-P1.0`：最高 2 万面，速度更快，适合快速预览和游戏/AR 场景。
- `Tripo/Tripo-H3.1`：最高 200 万面，适合影视级渲染和高精度数字资产。
- 通过 `texture_quality` 参数控制贴图质量（`standard` / `detailed`），通过 `geometry_quality` 控制几何精度（仅 H3.1 支持）。

> **注意**：3D 生成仅适用于华北2（北京）地域，必须使用该地域的 API Key。

## 语音合成（TTS）

语音合成模型将文本转换为自然语音，支持标准合成、声音复刻和声音设计。详见 [语音合成](../../raw/model-user-guide/model-inference/tts-model.md)。

- **标准合成**：使用内置音色，推荐 `cosyvoice-v3-plus`。
- **声音复刻**：从音频样本复刻音色，推荐 `cosyvoice-v3.5-plus`。
- **声音设计**：用文字描述创建全新音色，推荐 `cosyvoice-v3.5-plus`。
- **接入方式**：WebSocket（流式，延迟最低）和 HTTP（支持流式返回）两种。
- **指令控制**：CosyVoice 和 Qwen-TTS-Instruct 系列支持通过自然语言描述控制语速、情绪和风格。

## 语音识别（ASR）

语音识别模型支持实时和非实时两种模式。详见 [语音识别](../../raw/model-user-guide/model-inference/asr-model.md)。

| 模型 | 模式 | 精度增强 | 说话人分离 | 情感识别 |
|------|------|---------|-----------|---------|
| `fun-asr-realtime` | 实时 | 热词 | 不支持 | 不支持 |
| `fun-asr` | 非实时 | 热词 | 支持 | 不支持 |
| `qwen3.5-omni-plus-realtime` | 实时 | Prompt 上下文 | 不支持 | 支持 |
| `qwen3.5-omni-plus` | 非实时 | Prompt 上下文 | 不支持 | 支持 |

处理专业术语有两种方式：Prompt 上下文注入（Qwen3.5-Omni，无需预配置）和热词（Fun-ASR，提供带权重的词汇表）。

## 语音转语音（S2S）

S2S 模型支持语音对话、语音翻译等场景，相比 Pipeline（ASR + LLM + TTS）方案延迟更低、能保留音频中的语调和情绪信息。详见 [语音转语音](../../raw/model-user-guide/model-inference/s2s-model.md) 和 [全模态](../../raw/model-user-guide/model-inference/omni.md)。

- **语音对话**：推荐 `qwen3.5-omni-plus-realtime`，支持 Function Calling 和联网搜索。
- **同声传译**：推荐 `qwen3.5-livetranslate-flash-realtime`，支持 60 种语言，约 3 秒延迟。
- **视频配音/播客翻译**：推荐 `qwen3-livetranslate-flash`（HTTP 文件模式）。

## 向量与重排序

向量（Embedding）和重排序（Rerank）模型服务于语义搜索和 RAG 场景。详见 [向量与重排序](../../raw/model-user-guide/model-inference/embedding-rerank-model.md)。

- **文本 Embedding**：推荐 `text-embedding-v4`，支持 64~2048 维，默认 1024 维。
- **多模态 Embedding**：融合向量推荐 `qwen3-vl-embedding`，独立向量推荐 `tongyi-embedding-vision-plus`。
- **重排序**：纯文本推荐 `qwen3-rerank`（100+ 语言，最多 500 文档），多模态推荐 `qwen3-vl-rerank`。

## 音乐生成

百聆音乐大模型（`fun-music-v1`）支持通过提示词或歌词生成整首歌曲，支持男/女声、中/英文、流式和非[流式输出](../concepts/streaming.md)。详见 [音乐生成](../../raw/model-user-guide/model-inference/fun-music.md)。

> **注意**：音乐生成模型目前处于邀测阶段，仅在华北2（北京）地域可用。`lyrics` 和 `prompt` 参数必须至少提供一个，同时传入时仅 `lyrics` 生效。

## 通用使用方式

所有模型通过 DashScope API 调用，基本流程为：

1. 获取 API Key 并配置到环境变量 `DASHSCOPE_API_KEY`。
2. 文本/图片/语音等同步模型通过 HTTP POST 直接调用。
3. 视频生成、3D 生成等异步模型先提交任务获取 `task_id`，再轮询获取结果。
4. 实时语音类模型通过 WebSocket 进行流式交互。

文本生成模型兼容 OpenAI SDK 的 Chat Completions 接口，可直接使用 `openai` SDK 对接。

## 来源文档

- [图片生成与编辑](../../raw/model-user-guide/model-inference/image-model.md)
- [视觉理解](../../raw/model-user-guide/model-inference/vision-model.md)
- [文本生成](../../raw/model-user-guide/model-inference/text-generation-model.md)
- [视频生成与编辑](../../raw/model-user-guide/model-inference/video-generate-edit-model.md)
- [Tripo 3D模型生成](../../raw/model-user-guide/model-inference/tripo-3d-generation-guide.md)
- [语音合成](../../raw/model-user-guide/model-inference/tts-model.md)
- [音乐生成](../../raw/model-user-guide/model-inference/fun-music.md)
- [语音识别](../../raw/model-user-guide/model-inference/asr-model.md)
- [语音转语音](../../raw/model-user-guide/model-inference/s2s-model.md)
- [全模态](../../raw/model-user-guide/model-inference/omni.md)
- [向量与重排序](../../raw/model-user-guide/model-inference/embedding-rerank-model.md)



