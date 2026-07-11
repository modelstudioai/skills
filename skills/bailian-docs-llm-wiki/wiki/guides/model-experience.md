# model experience

百炼平台模型体验中心提供覆盖文本、视觉、视频、图片、3D、语音、音乐、向量等全模态的模型选型指南。开发者可根据应用场景在各品类中快速定位推荐模型，并通过模型广场查看详细参数与计费信息。

## 文本生成

文本生成模型适用于聊天机器人、内容生成、摘要总结、文档处理、AI 编程与 Agent 开发等场景。推荐从 `qwen3.7-plus` 起步，能力与成本均衡，拥有 1M 上下文和完整内置工具支持。需要最强推理能力时选择 `qwen3.7-max`，追求低成本时可尝试 `qwen3.6-flash`。

核心能力包括：

- **思考模式**：通过 `enable_thinking` 参数开启逐步推理，适用于多步数学计算、代码调试等场景。所有 Qwen3 及以上模型均支持。
- **Function Calling 与内置工具**：所有通用模型支持自定义工具调用；部分模型还支持联网搜索、代码解释器等内置工具。
- **结构化输出**：获取有效 JSON 返回，适合信息提取场景。
- **批量推理**：大量请求且对延迟要求不高时，可降低请求成本。

三方模型方面，百炼还提供 DeepSeek（`deepseek-v4-pro`、`deepseek-v4-flash`）、GLM（`glm-5.2`）、Kimi（`kimi-k2.7-code`）、MiniMax（`MiniMax-M3`）等可选项。详见[文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)。

## 视觉理解

视觉理解模型支持图像分析、视频理解、OCR 等场景。推荐使用 `qwen3.7-plus`（旗舰，1M 上下文、最长 2 小时视频、Function Calling 和内置工具），稳定后可切换到 `qwen3.6-flash` 降低成本。

关键参数：

- **图像分辨率**：大多数模型支持每张图片最高 1600 万像素，Token 数按 `h x w / (32 x 32) + 2` 计算。
- **视频支持**：Qwen3.7/3.6/3.5 系列最长 2 小时 / 2GB。
- **OCR 与文档提取**：`qwen3.5-ocr` 专为文档、表格、手写内容优化。

详见[视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)。

## 视频生成与编辑

视频生成涵盖文生视频、图生视频、参考生视频、视频编辑和角色动画五大场景。

| 场景 | 推荐模型 | 最大分辨率 | 最大时长 |
|------|----------|-----------|---------|
| 文生视频 | `happyhorse-1.1-t2v` | 1080P | 3-15秒 |
| 首帧生视频 | `happyhorse-1.1-i2v` | 1080P | 3-15秒 |
| 首尾帧生视频 | `wan2.7-i2v-2026-04-25` | 1080P | 2-15秒 |
| 参考生视频 | `happyhorse-1.1-r2v` | 1080P | 3-15秒 |
| 视频编辑 | `happyhorse-1.0-video-edit` | 1080P | 3-15秒 |
| 动作迁移 | `wan2.2-animate-move` | 720P | 2-30秒 |

需要传入自定义音频文件时，使用 Wan 2.7 系列（如 `wan2.7-t2v-2026-06-12`）。构建长视频可使用首尾帧模型串联多个片段。详见[视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)。

## 图片生成与编辑

推荐使用 `wan2.7-image-pro`，集文字渲染、品牌色控制、角色一致性多图生成和图片编辑于一体，文生图最高支持 4096x4096 分辨率。

- **快速低成本**：`z-image-turbo`，生成速度快 10 倍，价格约 1/5，适合写实人像和产品照片。
- **负向提示词**：`qwen-image-2.0-pro`，支持排除特定元素，每次最多 6 张变体。

详见[图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)。

## 3D 模型生成

通过 Tripo 模型支持文生 3D、单图生 3D 和多图生 3D 三种模式，输出 GLB 格式的 PBR 材质模型。

- **Tripo-H3.1**：最高 200 万面，适合影视级渲染和高精度数字资产，速度较慢。
- **Tripo-P1.0**：最高 2 万面，适合快速预览、游戏/AR 场景，速度更快。

调用方式为异步任务：先创建任务获取 `task_id`，再轮询获取结果（建议间隔 15 秒）。通过 `texture_quality` 参数控制贴图质量（`standard` / `detailed`），Tripo-H3.1 还支持 `geometry_quality` 控制几何精度。详见[Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。

## 语音合成

语音合成（TTS）模型将文本转换为自然语音，分为标准语音合成和自定义音色两条路线：

- **标准语音合成**：使用内置音色库，推荐 `cosyvoice-v3-plus` 或 `MiniMax/speech-2.8-hd`。
- **自定义音色**：通过声音复刻（提供音频样本）或声音设计（文字描述创建），推荐 `cosyvoice-v3.5-plus`。

接入方式支持 WebSocket（流式，延迟最低）和 HTTP（完整文本输入）。CosyVoice 系列还支持通过自然语言指令控制语速、情绪和风格。详见[语音合成](../../raw/model-user-guide/model-experience/tts-model.md)。

## 语音转语音（S2S）

S2S 模型提供端到端的语音输入到语音输出能力，相比 ASR + LLM + TTS 三段式 Pipeline，延迟更低且能感知语调、情绪。

| 场景 | 推荐模型 | API |
|------|----------|-----|
| 语音助手 / 客服对话 | `qwen3.5-omni-plus-realtime` | WebSocket |
| 成本敏感对话 | `qwen3.5-omni-flash-realtime` | WebSocket |
| 同声传译 / 直播翻译 | `qwen3.5-livetranslate-flash-realtime` | WebSocket |
| 视频配音 / 播客翻译 | `qwen3-livetranslate-flash` | HTTP |

翻译方面，Qwen3.5-Livetranslate 支持 60 种语言互译，Qwen3.5-Omni 支持 29 种输出语言。详见[语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)。

## 语音识别（ASR）

语音识别分为实时（WebSocket，边说边转写）和非实时（HTTP，录音文件转写）两种模式。

- **实时识别**：推荐 `fun-asr-realtime`（热词、方言支持）或 `qwen3.5-omni-plus-realtime`（Prompt 上下文、多语种）。
- **非实时识别**：推荐 `fun-asr`（热词、说话人分离，最长 12 小时）或 `qwen3.5-omni-plus`（Prompt 上下文，最长 3 小时）。
- **情感识别**：Qwen-ASR 和 Qwen3.5-Omni 系列支持。
- **说话人分离**：仅 Fun-ASR 非实时模型支持。

处理专业术语有两种方式：Prompt 上下文注入（Qwen3.5-Omni，无需预配置）和热词列表（Fun-ASR，适合稳定术语）。详见[语音识别](../../raw/model-user-guide/model-experience/asr-model.md)。

## 音乐生成

Fun-Music 支持通过提示词描述风格或提供自定义歌词生成完整歌曲，也支持纯音乐模式。

- `fun-music-v1`：支持 [prompt](prompt.md)、lyrics、gender 参数，可选男声或女声。
- `fun-music-preview`：[prompt](prompt.md) 为必选参数，不支持 gender。

输出支持 MP3（有损压缩，适合网络传输）和 WAV（无损，适合后期处理）两种格式。

> **注意**：Fun-Music 目前处于邀测阶段，需在模型广场申请开通，且仅在华北2（北京）地域可用。

详见[音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)。

## 向量与重排序

向量（Embedding）和重排序（Rerank）模型用于语义搜索和 RAG 检索增强。

- **文本 Embedding**：推荐 `text-embedding-v4`，支持 64~2048 维，最大 8192 Token。通用场景选 1024 维，高精度选 1536 或 2048 维。
- **[多模态](../concepts/multimodal.md) Embedding**：`qwen3-vl-embedding`（融合向量，图文混合检索）或 `tongyi-embedding-vision-plus`（独立向量，跨模态搜索）。
- **重排序**：`qwen3-rerank`（纯文本，100+ 语言，最多 500 条）或 `qwen3-vl-rerank`（[多模态](../concepts/multimodal.md)，文本、图片、视频混合排序）。

详见[向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)。

## 全模态（Omni）

全模态模型同时理解文本、音频、图片和视频，并输出文本和语音。三个系列各有侧重：

- **Qwen3.5-Omni**（旗舰）：能力最全，支持 Function Calling、联网搜索、声音复刻，音频最长 3 小时、视频最长 1 小时。
- **Qwen3-Omni-Flash**（轻量）：成本更低，支持深度推理（思考模式），单次输入限 150 秒。
- **Qwen3.5-Livetranslate**（翻译专用）：60 种语言，约 3 秒延迟，开箱即用。

详见[全模态](../../raw/model-user-guide/model-experience/omni.md)。

## 选型总结

| 场景 | 首选模型 |
|------|---------|
| 通用文本 / Agent 开发 | `qwen3.7-plus` |
| 图像与视频理解 | `qwen3.7-plus` |
| 视频生成 | `happyhorse-1.1-t2v` / `happyhorse-1.1-i2v` |
| 图片生成 | `wan2.7-image-pro` |
| 3D 生成 | `Tripo/Tripo-P1.0`（快速）/ `Tripo/Tripo-H3.1`（高精度） |
| 语音合成 | `cosyvoice-v3.5-plus`（自定义音色）/ `cosyvoice-v3-plus`（标准） |
| 实时语音对话 | `qwen3.5-omni-plus-realtime` |
| 语音识别 | `fun-asr-realtime`（实时）/ `fun-asr`（非实时） |
| 语义搜索 / RAG | `text-embedding-v4` + `qwen3-rerank` |
| 同声传译 | `qwen3.5-livetranslate-flash-realtime` |

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



