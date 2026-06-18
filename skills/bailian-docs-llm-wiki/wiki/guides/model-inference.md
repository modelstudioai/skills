# model inference

百炼平台提供覆盖文本、视觉、音频、视频、3D 等多种模态的模型推理能力，开发者可通过 [OpenAI 兼容接口](../concepts/openai-compatible.md)或 DashScope API 调用。本文汇总各模态下的模型选型要点、关键参数与使用方式，帮助快速找到适合场景的模型。

## 文本生成

文本生成是最常用的推理场景，覆盖聊天机器人、AI 智能体、文档处理、代码生成等。

### 推荐模型

| 模型 ID | 上下文 | 思考模式 | Function Calling | 内置工具 | 结构化输出 | 批量调用 |
|---------|--------|---------|-----------------|---------|-----------|---------|
| `qwen3.7-max` | 1M | 支持 | 支持 | 支持 | 不支持 | 支持 |
| `qwen3.7-plus` | 1M | 支持 | 支持 | 支持 | 支持 | 支持 |
| `qwen3.6-flash` | 1M | 支持 | 支持 | 支持 | 支持 | 支持 |
| `deepseek-v4-pro` | 1M | 支持 | 支持 | 不支持 | 不支持 | 不支持 |
| `deepseek-v4-flash` | 1M | 支持 | 支持 | 不支持 | 不支持 | 不支持 |

- **能力优先**选 `qwen3.7-max`（1M 上下文，256k 思考预算）；**均衡场景**选 `qwen3.7-plus`；**低成本**选 `qwen3.6-flash`，效果接近旗舰。
- 100 万 Token 上下文约相当于 70 万汉字或 10 本小说，适合长文档和大型代码库。
- 所有 Qwen3 及以上模型支持**思考模式**（`enable_thinking` 参数），适用于多步推理场景。
- 第三方模型 `deepseek-v4-pro`、`glm-5.2`、`kimi-k2.7-code`、`MiniMax-M2.5`、`mimo-v2.5-pro` 等也可通过百炼统一接口调用。

详见 [文本生成](../../raw/model-user-guide/model-inference/text-generation-model.md)。

## 视觉理解

支持图像分析、视频理解、OCR 等场景。

### 推荐模型

| 模型 ID | 上下文 | 最大视频时长 | Function Calling | 内置工具 | 结构化输出 |
|---------|--------|------------|-----------------|---------|-----------|
| `qwen3.7-plus` | 1M | 2 小时 | 支持 | 支持 | 支持 |
| `qwen3.6-flash` | 1M | 2 小时 | 支持 | 支持 | 支持 |
| `qwen3.5-omni-plus` | 64k | 1 小时 | 支持 | -- | 支持 |

- 大多数模型支持每张图片最高 1600 万像素，Token 消耗公式为 `h x w / (32 x 32) + 2`。
- OCR 场景可使用专用的 `qwen-vl-ocr` 模型。
- 支持从视觉输入获取结构化 JSON 输出（非思考模式下）。

详见 [视觉理解](../../raw/model-user-guide/model-inference/vision-model.md)。

## 图片生成与编辑

### 推荐模型

| 模型 ID | 文生图 | 编辑 | 最大输出数 | 最大分辨率 |
|---------|-------|------|-----------|-----------|
| `wan2.7-image-pro` | 支持 | 支持 | 4（连续 12） | 4096x4096（文生图）/ 2048x2048（编辑） |
| `z-image-turbo` | 支持 | 不支持 | 1 | 2048x2048 |
| `qwen-image-2.0-pro` | 支持 | 支持 | 6 | 2048x2048 |

- **文生图**推荐 `wan2.7-image-pro`，集成文字渲染、品牌色控制和角色一致性多图生成。
- **速度或成本优先**选 `z-image-turbo`，生成速度快 10 倍，价格约为 1/5。
- 需要**负向提示词**或一次生成最多 6 张变体时选 `qwen-image-2.0-pro`。

详见 [图片生成与编辑](../../raw/model-user-guide/model-inference/image-model.md)。

## 视频生成与编辑

### 推荐模型

| 模型 ID | 适用场景 | 最大分辨率 | 最大时长 |
|---------|---------|-----------|---------|
| `happyhorse-1.0-t2v` | 文生视频 | 1080P | 3-15 秒 |
| `happyhorse-1.0-i2v` | 首帧生视频 | 1080P | 3-15 秒 |
| `wan2.7-i2v-2026-04-25` | 首帧/首尾帧生视频、视频续写 | 1080P | 2-15 秒 |
| `happyhorse-1.0-r2v` | 参考图像生视频 | 1080P | 3-15 秒 |
| `happyhorse-1.0-video-edit` | 视频编辑 | 1080P | 3-15 秒 |
| `wan2.2-animate-move` | 动作迁移到静态人物 | 720P | 2-30 秒 |

- **文生有声视频**推荐 HappyHorse 1.0 系列；若需传入自定义音频文件，使用 Wan 2.7 系列。
- 可通过首尾帧模型串联多片段构建长视频。
- 角色动画支持 `wan-pro`（更接近真实拍摄）和 `wan-std`（速度更快、成本更低）两种模式。

详见 [视频生成与编辑](../../raw/model-user-guide/model-inference/video-generate-edit-model.md)。

## 语音合成（TTS）

### 推荐模型

| 模型 ID | 系列 | API | 声音复刻 | 声音设计 | 指令控制 |
|---------|------|-----|---------|---------|---------|
| `cosyvoice-v3.5-plus` | CosyVoice | WebSocket / HTTP | 支持 | 支持 | 支持 |
| `cosyvoice-v3-plus` | CosyVoice | WebSocket / HTTP | 支持 | 支持 | 不支持 |
| `MiniMax/speech-2.8-hd` | MiniMax | HTTP | 支持 | 不支持 | 不支持 |

- **标准语音合成**（使用内置音色）推荐 `cosyvoice-v3-plus`；**自定义音色**（声音复刻或声音设计）推荐 `cosyvoice-v3.5-plus`。
- **指令控制**可通过自然语言动态控制语速、情绪和风格（如"用温柔的语气，语速稍慢"）。
- WebSocket 适合实时交互（语音助手、客服），HTTP 适合有声阅读、音频内容制作。

详见 [语音合成](../../raw/model-user-guide/model-inference/tts-model.md)。

## 语音识别（ASR）

### 推荐模型

| 模型 ID | 模式 | API | 精度增强 | 情感识别 | 说话人分离 |
|---------|------|-----|---------|---------|-----------|
| `fun-asr-realtime` | 实时 | WebSocket | 热词 | 不支持 | 不支持 |
| `fun-asr` | 非实时 | HTTP | 热词 | 不支持 | 支持 |
| `qwen3.5-omni-plus-realtime` | 实时 | WebSocket | Prompt 上下文 | 支持 | 不支持 |
| `qwen3.5-omni-plus` | 非实时 | HTTP | Prompt 上下文 | 支持 | 不支持 |

- **实时字幕/语音助手**选 `fun-asr-realtime`（热词、方言支持）或 `qwen3.5-omni-plus-realtime`（Prompt 上下文、多语种）。
- 需要**说话人分离**只能使用 Fun-ASR 非实时模型。
- 需要**情感识别**推荐 Qwen-ASR 系列（`qwen3-asr-flash-realtime` / `qwen3-asr-flash-filetrans`）。

详见 [语音识别](../../raw/model-user-guide/model-inference/asr-model.md)。

## 语音转语音（S2S）与全模态

### S2S 推荐模型

| 模型 ID | API | 场景 |
|---------|-----|------|
| `qwen3.5-omni-plus-realtime` | WebSocket | 语音助手 / 客服对话 |
| `qwen3.5-omni-flash-realtime` | WebSocket | 成本敏感的对话 |
| `qwen3.5-livetranslate-flash-realtime` | WebSocket | 同声传译 / 直播翻译（60 种语言） |
| `qwen3-livetranslate-flash` | HTTP | 视频配音 / 播客翻译 |

S2S 与 Pipeline（ASR + LLM + TTS）两种架构各有优劣：S2S 延迟更低、能感知语调情绪；Pipeline 支持音色定制，可为每阶段选最优模型。

全模态模型（Qwen3.5-Omni）能同时理解文本、音频、图片和视频，支持 Function Calling、联网搜索等附带能力。

详见 [语音转语音](../../raw/model-user-guide/model-inference/s2s-model.md) 和 [全模态](../../raw/model-user-guide/model-inference/omni.md)。

## 3D 模型生成

通过 Tripo 模型支持**文生 3D、单图生 3D、多图生 3D** 三种模式。

| 模型 ID | 产物最高面数 | 速度 | 适用场景 |
|---------|------------|------|---------|
| `Tripo/Tripo-H3.1` | 200 万面 | 较慢 | 影视级渲染、高精度数字资产 |
| `Tripo/Tripo-P1.0` | 2 万面 | 更快 | 快速预览、游戏/AR 场景 |

- 3D 生成为异步任务，建议轮询间隔 15 秒。
- 通过 `texture_quality` 控制贴图质量（`standard` / `detailed`），`geometry_quality` 控制几何精度（仅 H3.1 支持）。

> **注意**：Tripo 模型目前仅适用于华北 2（北京）地域，需使用该地域的 API Key。

详见 [Tripo 3D模型生成](../../raw/model-user-guide/model-inference/tripo-3d-generation-guide.md)。

## 音乐生成

百聆音乐大模型（`fun-music-v1`）支持通过提示词或自定义歌词生成整首歌曲，支持男/女声、中英文、流式和非[流式输出](../concepts/streaming.md)。

> **注意**：该模型目前处于邀测阶段，仅在华北 2（北京）地域可用。

详见 [音乐生成](../../raw/model-user-guide/model-inference/fun-music.md)。

## 向量与重排序

### 推荐模型

| 模型 ID | 类型 | 向量维度 | 最大 Token 数 | 适用场景 |
|---------|------|---------|-------------|---------|
| `text-embedding-v4` | 文本 Embedding | 64~2048（默认 1024） | 8,192 | 文本搜索、RAG、聚类 |
| `qwen3-vl-embedding` | 多模态 Embedding | 256~2560（默认 2560） | 32,000 | 图文混合检索 |
| `qwen3-rerank` | 重排序 | - | 4,000/条 | 文本搜索结果重排序、RAG |
| `qwen3-vl-rerank` | 重排序 | - | 8,000/条 | 多模态搜索结果重排序 |

- 纯文本场景用 `text-embedding-v4`，维度选择：大规模搜索选 256/512 维，通用场景用 1024 维（默认），高精度需求选 1536/2048 维。
- **融合向量**（图文混合检索）推荐 `qwen3-vl-embedding`；**独立向量**（跨模态搜索）推荐 `tongyi-embedding-vision-plus`。
- 在 Embedding 检索后追加重排序（Rerank）可通过交叉注意力机制显著提升 RAG 精度。

详见 [向量与重排序](../../raw/model-user-guide/model-inference/embedding-rerank-model.md)。

## 通用使用方式

百炼平台的模型推理主要通过以下方式接入：

1. **[OpenAI 兼容接口](../concepts/openai-compatible.md)**：文本生成、视觉理解等模型支持 OpenAI SDK 直接调用，降低迁移成本。
2. **DashScope API**：百炼原生 API，支持全部模型和特性（异步任务、WebSocket 实时流等）。
3. **[DashScope SDK](../concepts/dashscope-sdk.md)**：Java / Python SDK 封装，简化 WebSocket 等复杂协议的接入。
4. **移动端 SDK**：Fun-ASR、CosyVoice 等模型支持 Android / iOS SDK 接入。

### 关键通用参数

- **`enable_thinking`**：开启思考模式，适用于多步推理（Qwen3 及以上模型）。
- **结构化输出**：从文本或视觉输入获取有效 JSON 返回。
- **Function Calling**：让模型调用自定义工具执行操作。
- **内置工具**：联网搜索、代码解释器等，无需额外配置。
- **批量推理**：大量请求、对延迟不敏感的场景，可降低成本。

## 注意事项

- 不同模态的模型**计费方式不同**（文本按 Token、图片按张、视频按秒等），具体以模型广场标注为准。
- 部分模型（如 Tripo 3D、Fun 音乐）有**地域限制**，仅在华北 2（北京）可用。
- 旧版模型（如 Qwen2.5-VL、Wan 2.1 等）仍可调用但不再作为首选推荐，新项目建议使用最新系列。

## 来源文档

- [图片生成与编辑](../../raw/model-user-guide/model-inference/image-model.md)
- [视觉理解](../../raw/model-user-guide/model-inference/vision-model.md)
- [文本生成](../../raw/model-user-guide/model-inference/text-generation-model.md)
- [视频生成与编辑](../../raw/model-user-guide/model-inference/video-generate-edit-model.md)
- [Tripo 3D模型生成](../../raw/model-user-guide/model-inference/tripo-3d-generation-guide.md)
- [语音合成](../../raw/model-user-guide/model-inference/tts-model.md)
- [音乐生成](../../raw/model-user-guide/model-inference/fun-music.md)
- [语音转语音](../../raw/model-user-guide/model-inference/s2s-model.md)
- [全模态](../../raw/model-user-guide/model-inference/omni.md)
- [语音识别](../../raw/model-user-guide/model-inference/asr-model.md)
- [向量与重排序](../../raw/model-user-guide/model-inference/embedding-rerank-model.md)


