# model inference

百炼平台提供覆盖文本、图片、视频、3D、语音、音乐和向量等多种模态的模型推理能力。开发者可通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)、DashScope REST API 或 WebSocket 协议调用这些模型，按需完成各类 AI 任务。本文汇总各模态的推荐模型、核心参数和选型要点，帮助快速定位适合的模型。

## 文本生成

文本生成模型适用于聊天机器人、内容生成、摘要总结、代码生成等场景。推荐从 `qwen3.7-plus` 起步——1M 上下文、完整工具调用、能力与成本均衡；需要最强推理时选择 `qwen3.7-max`；追求低成本时可用 `qwen3.6-flash`。详见[文本生成](../../raw/model-user-guide/model-inference/text-generation-model.md)。

| 模型ID | 上下文 | 思考模式 | Function Calling | 内置工具 | 结构化输出 |
|--------|--------|----------|-----------------|----------|-----------|
| `qwen3.7-max` | 1M | 支持 | 支持 | 支持 | 不支持 |
| `qwen3.7-plus` | 1M | 支持 | 支持 | 支持 | 支持 |
| `qwen3.6-flash` | 1M | 支持 | 支持 | 支持 | 支持 |
| `deepseek-v4-pro` | 1M | 支持 | 支持 | 不支持 | 不支持 |

关键能力说明：

- **思考模式**：通过 `enable_thinking` 参数开启逐步推理，适用于数学计算、代码调试、架构规划。所有 Qwen3 及以上模型均支持。
- **Function Calling 与内置工具**：让模型调用外部函数或使用联网搜索、代码解释器等内置工具。
- **结构化输出**：获取有效 JSON 返回，适合从文本中提取结构化信息。
- **批量推理**：大量请求且对延迟不敏感时可降低成本。

第三方模型方面，百炼还提供 `deepseek-v4-pro`/`deepseek-v4-flash`、`glm-5.1`、`kimi-k2.7-code`、`MiniMax-M2.5`、`mimo-v2.5-pro` 等选择。

## 视觉理解

视觉理解模型支持图像分析、视频理解和 OCR。推荐 `qwen3.7-plus`（1M 上下文、最长 2 小时视频、完整功能集）或 `qwen3.6-flash`（接近旗舰效果、成本更低）。OCR 场景可使用专用的 `qwen-vl-ocr`。详见[视觉理解](../../raw/model-user-guide/model-inference/vision-model.md)。

- 图像分辨率：大多数模型支持每张最高 1600 万像素，Token 计算公式为 `h x w / (32 x 32) + 2`。
- 视频支持：Qwen3.7/3.6/3.5 系列支持最长 2 小时 / 2GB 视频。
- 结构化输出：Qwen3.7、Qwen3.6、Qwen3.5、Qwen3-VL 系列在非思考模式下支持 JSON 输出。

## 图片生成与编辑

图片生成推荐 `wan2.7-image-pro`，集成文字渲染、品牌色控制、角色一致性多图生成和图片编辑，文生图最高 4096x4096。快速低成本场景选 `z-image-turbo`（速度快 10 倍、价格约 1/5）。需要负向提示词或最多 6 张变体时选 `qwen-image-2.0-pro`。详见[图片生成与编辑](../../raw/model-user-guide/model-inference/image-model.md)。

| 模型ID | 文生图 | 编辑 | 最大输出数 | 最大分辨率 |
|--------|--------|------|-----------|-----------|
| `wan2.7-image-pro` | 支持 | 支持 | 4（连续12） | 4096x4096（文生图）/ 2048x2048（编辑） |
| `z-image-turbo` | 支持 | 不支持 | 1 | 2048x2048 |
| `qwen-image-2.0-pro` | 支持 | 支持 | 6 | 2048x2048 |

## 视频生成与编辑

视频生成覆盖文生视频、图生视频、参考生视频、视频编辑和角色动画等场景。详见[视频生成与编辑](../../raw/model-user-guide/model-inference/video-generate-edit-model.md)。

| 场景 | 推荐模型 | 最大分辨率 | 最大时长 |
|------|---------|-----------|---------|
| 文生视频（有声） | `happyhorse-1.0-t2v` | 1080P | 3-15秒 |
| 文生视频（自定义音频） | `wan2.7-t2v-2026-04-25` | 1080P | 2-15秒 |
| 首帧生视频 | `happyhorse-1.0-i2v` | 1080P | 3-15秒 |
| 首尾帧生视频 | `wan2.7-i2v-2026-04-25` | 1080P | 2-15秒 |
| 参考生视频 | `happyhorse-1.0-r2v` | 1080P | 3-15秒 |
| 视频编辑 | `happyhorse-1.0-video-edit` | 1080P | 3-15秒 |
| 动作迁移 | `wan2.2-animate-move` | 720P | 2-30秒 |

可通过首尾帧模型串联多片段构建长视频——将上一片段末帧作为下一片段首帧实现无缝过渡。

## 3D 模型生成

通过 Tripo 模型支持文生 3D、单图生 3D 和多图生 3D 三种模式。`Tripo/Tripo-P1.0` 适合快速预览（2 万面、速度更快），`Tripo/Tripo-H3.1` 适合高精度场景（200 万面）。3D 生成为[异步任务](../concepts/async-task.md)，通常需数分钟，建议 15 秒轮询。详见 [Tripo 3D模型生成](../../raw/model-user-guide/model-inference/tripo-3d-generation-guide.md)。

> **注意**：Tripo 模型仅适用于华北2（北京）地域，必须使用该地域的 API Key。

## 语音合成（TTS）

语音合成模型将文本转为自然语音，支持标准内置音色和自定义音色（声音复刻 + 声音设计）。详见[语音合成](../../raw/model-user-guide/model-inference/tts-model.md)。

| 模型ID | 系列 | 声音复刻 | 声音设计 | 指令控制 |
|--------|------|---------|---------|---------|
| `cosyvoice-v3.5-plus` | CosyVoice | 支持 | 支持 | 支持 |
| `cosyvoice-v3-plus` | CosyVoice | 支持 | 支持 | 不支持 |
| `MiniMax/speech-2.8-hd` | MiniMax | 支持 | 不支持 | 不支持 |

接入方式选择：

- **WebSocket**：双向流式，延迟最低，适合实时交互（智能客服、语音助手）。
- **HTTP**：发送完整文本，支持流式返回，适合有声阅读、内容制作。

指令控制功能支持用自然语言描述语速、情绪和风格（如"用温柔的语气，语速稍慢"），CosyVoice 和 Qwen-TTS-Instruct 系列支持。

## 语音识别（ASR）

语音识别分实时和非实时两种模式。详见[语音识别](../../raw/model-user-guide/model-inference/asr-model.md)。

| 模型ID | 模式 | 精度增强 | 情感识别 | 说话人分离 |
|--------|------|---------|---------|-----------|
| `fun-asr-realtime` | 实时 | 热词 | 不支持 | 不支持 |
| `fun-asr` | 非实时 | 热词 | 不支持 | 支持 |
| `qwen3.5-omni-plus-realtime` | 实时 | Prompt上下文 | 支持 | 不支持 |
| `qwen3.5-omni-plus` | 非实时 | Prompt上下文 | 支持 | 不支持 |

处理专业术语有两种方式：热词（Fun-ASR 系列，适合稳定术语列表）和 Prompt 上下文注入（Qwen3.5-Omni，灵活但延迟略高）。说话人分离仅 Fun-ASR 非实时模型支持。

## 语音转语音（S2S）与全模态

语音转语音有两种架构：S2S 单模型（低延迟、保留音频细微信息）和 Pipeline（ASR + LLM + TTS，灵活定制音色）。推荐 `qwen3.5-omni-plus-realtime` 用于实时语音对话，`qwen3.5-livetranslate-flash-realtime` 用于同声传译（60 种语言、约 3 秒延迟）。详见[语音转语音](../../raw/model-user-guide/model-inference/s2s-model.md)和[全模态](../../raw/model-user-guide/model-inference/omni.md)。

全模态模型（Qwen3.5-Omni 系列）同时理解文本、音频、图片和视频并输出文本与语音，支持 Function Calling、联网搜索和声音复刻。内容分析场景支持音频最长 3 小时、视频最长 1 小时。

## 音乐生成

百聆音乐生成大模型（`fun-music-v1`）支持通过提示词或自定义歌词生成完整歌曲，支持男/女声和中英文。详见[音乐生成](../../raw/model-user-guide/model-inference/fun-music.md)。

> **注意**：该模型处于邀测阶段，仅华北2（北京）地域可用。`lyrics` 和 `prompt` 必须至少提供一个；同时传入时仅 `lyrics` 生效。

## 向量与重排序

用于语义搜索、RAG 检索和跨模态匹配。详见[向量与重排序](../../raw/model-user-guide/model-inference/embedding-rerank-model.md)。

- **文本 Embedding**：推荐 `text-embedding-v4`，支持 64~2048 维，最大 8192 Token。
- **多模态 Embedding**：融合向量用 `qwen3-vl-embedding`（图文混合检索），独立向量用 `tongyi-embedding-vision-plus`（跨模态搜索）。
- **重排序**：纯文本用 `qwen3-rerank`（100+ 语言，最多 500 文档），多模态用 `qwen3-vl-rerank`。

## 通用调用说明

- **API 接入**：文本和视觉模型支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)；语音、视频、3D 等模型通过 DashScope REST API 或 WebSocket 调用。
- **[异步任务](../concepts/async-task.md)**：视频生成、3D 生成等耗时任务采用异步模式，提交后通过任务 ID 轮询结果，建议配置回调通知。
- **地域限制**：部分模型（Tripo、音乐生成）仅限华北2（北京）地域；国际地域（新加坡、美国、法兰克福）可用模型范围不同，需查阅模型广场。
- **版本管理**：主线模型 ID（如 `qwen3.7-plus`）会持续更新，快照版本（如 `qwen3.7-plus-2026-05-26`）锁定特定日期，适合对稳定性有要求的生产环境。

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




