# model experience

百炼平台模型体验中心提供覆盖文本生成、视觉理解、视频生成与编辑、图片生成与编辑、3D模型生成、语音合成、语音转语音、语音识别、音乐生成、向量与重排序以及全模态等多个领域的模型。开发者可根据应用场景快速选型，并通过统一的 API 接入调用。

## 文本生成

文本生成模型适用于聊天机器人、内容生成、摘要总结、文档处理、AI 编程与 Agent 开发等场景。

**推荐模型**：

| 模型ID | 上下文 | 定位 |
|--------|--------|------|
| `qwen3.7-max` | 1M | 最强推理能力 |
| `qwen3.7-plus` | 1M | 能力与成本均衡，完整工具调用 |
| `qwen3.6-flash` | 1M | 低成本，效果接近旗舰 |
| `deepseek-v4-pro` | 1M | 第三方深度推理 |

核心功能包括：思考模式（`enable_thinking` 参数开启逐步推理）、Function Calling（自定义工具调用）、内置工具（联网搜索、代码解释器等）、结构化输出（JSON）、批量推理。所有 Qwen3 及以上模型均支持思考模式。

生产环境建议固定到具体快照版本（如 `qwen3.7-max-2026-06-08`）以保证输出稳定。详见[文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)。

## 视觉理解

视觉理解模型支持图像分析、视频理解和 OCR 等场景。推荐从 `qwen3.7-plus` 开始，支持 1M 上下文、最长 2 小时视频、Function Calling 和内置工具。

**关键参数**：

- 图像分辨率：每张最高 1600 万像素，[Token](../concepts/token.md) 计算公式 `h x w / (32 x 32) + 2`
- 视频支持：Qwen3.7/3.6/3.5 系列最长 2 小时/2GB；Qwen3-VL 系列最长 1 小时
- OCR 专用模型：`qwen-vl-ocr`，针对文档、表格、手写内容优化

详见[视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)。

## 视频生成与编辑

支持文生视频、图生视频、参考生视频、视频编辑和角色动画等场景。

| 场景 | 推荐模型 | 最大分辨率 | 最大时长 |
|------|----------|-----------|----------|
| 文生视频 | `happyhorse-1.1-t2v` | 1080P | 3-15秒 |
| 首帧生视频 | `happyhorse-1.1-i2v` | 1080P | 3-15秒 |
| 首尾帧生视频 | `wan2.7-i2v-2026-04-25` | 1080P | 2-15秒 |
| 参考生视频 | `happyhorse-1.1-r2v` | 1080P | 3-15秒 |
| 视频编辑 | `happyhorse-1.0-video-edit` | 1080P | 3-15秒 |
| 动作迁移 | `wan2.2-animate-move` | 720P | 2-30秒 |

HappyHorse 1.1 系列支持有声视频输出。需要自定义音频文件时选择 Wan 2.7 系列。详见[视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)。

## 图片生成与编辑

推荐使用 `wan2.7-image-pro`，集成文字渲染、品牌色控制、角色一致性多图生成和图片编辑，文生图最高 4096x4096 分辨率。

| 模型ID | 适用场景 | 最大分辨率 |
|--------|----------|-----------|
| `wan2.7-image-pro` | 全功能（文字渲染、品牌色、多图生成、编辑） | 4096x4096 |
| `z-image-turbo` | 快速生成、低成本、写实人像 | 2048x2048 |
| `qwen-image-2.0-pro` | 负向提示词、最多6张变体 | 2048x2048 |

详见[图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)。

## 3D模型生成

通过 Tripo 模型支持文生3D、单图生3D和多图生3D三种模式，异步任务接口，产物为 GLB 格式。

| 模型 | 最高面数 | 速度 | 适用场景 |
|------|---------|------|----------|
| `Tripo/Tripo-H3.1` | 200万面 | 较慢 | 影视级渲染、高精度数字资产 |
| `Tripo/Tripo-P1.0` | 2万面 | 更快 | 快速预览、游戏/AR |

支持 `texture_quality`（standard/detailed）和 `geometry_quality`（standard/ultra，仅H3.1）参数控制精度。详见[Tripo 3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。

## 语音合成

语音合成模型将文本转换为自然语音，支持标准合成、声音复刻和声音设计。

**推荐模型**：

| 模型ID | 声音复刻 | 声音设计 | 指令控制 |
|--------|---------|---------|---------|
| `cosyvoice-v3.5-plus` | 支持 | 支持 | 支持 |
| `cosyvoice-v3-plus` | 支持 | 支持 | 不支持 |
| `MiniMax/speech-2.8-hd` | 支持 | 不支持 | 不支持 |

接入方式：WebSocket（实时流式，延迟最低）和 HTTP（完整文本输入，适合有声阅读）。指令控制支持用自然语言动态调节语速、情绪和风格。详见[语音合成](../../raw/model-user-guide/model-experience/tts-model.md)。

## 语音转语音（S2S）

S2S 模型实现端到端语音交互，相比 ASR+LLM+TTS 流水线延迟更低、能感知语调和情绪。

| 场景 | 推荐模型 | API |
|------|----------|-----|
| 语音助手/客服 | `qwen3.5-omni-plus-realtime` | WebSocket |
| 成本敏感对话 | `qwen3.5-omni-flash-realtime` | WebSocket |
| 同声传译 | `qwen3.5-livetranslate-flash-realtime` | WebSocket |
| 视频配音/播客翻译 | `qwen3-livetranslate-flash` | HTTP |

S2S 模型同时支持 Function Calling、联网搜索和翻译（Qwen3.5-Livetranslate 支持 60 种语言）。详见[语音转语音](../../raw/model-user-guide/model-experience/s2s-model.md)。

## 语音识别

语音识别分为实时（WebSocket）和非实时（HTTP）两种模式。

| 模型ID | 模式 | 精度增强 | 说话人分离 | 情感识别 |
|--------|------|---------|-----------|---------|
| `fun-asr-realtime` | 实时 | 热词 | 不支持 | 不支持 |
| `fun-asr` | 非实时 | 热词 | 支持 | 不支持 |
| `qwen3.5-omni-plus-realtime` | 实时 | Prompt上下文 | 不支持 | 支持 |
| `qwen3.5-omni-plus` | 非实时 | Prompt上下文 | 不支持 | 支持 |

处理专业术语有两种方式：Prompt 上下文注入（灵活，无需预配置）和热词（适合稳定术语列表）。详见[语音识别](../../raw/model-user-guide/model-experience/asr-model.md)。

## 音乐生成

Fun 音乐大模型支持通过提示词或自定义歌词生成完整歌曲，支持男/女声演唱、中英文、流式与非流式输出。

- 模型：`fun-music-v1`、`fun-music-preview`
- 输入：`prompt`（描述风格场景，自动创作歌词）或 `lyrics`（自定义歌词谱曲）
- 输出：MP3 或 WAV 格式

> **注意**：该模型目前处于邀测阶段，需在模型广场申请开通，仅华北2（北京）地域可用。

详见[音乐生成](../../raw/model-user-guide/model-experience/fun-music.md)。

## 向量与重排序

用于语义搜索、RAG 检索和跨模态匹配。

| 模型ID | 类型 | 维度 | 适用场景 |
|--------|------|------|----------|
| `text-embedding-v4` | 文本Embedding | 64~2048 | 文本搜索、RAG、聚类 |
| `qwen3-vl-embedding` | [多模态](../concepts/multimodal.md)Embedding | 256~2560 | 图文混合检索 |
| `tongyi-embedding-vision-plus` | [多模态](../concepts/multimodal.md)Embedding | 64~1152 | 跨模态搜索 |
| `qwen3-rerank` | 重排序 | - | 文本搜索结果重排序 |
| `qwen3-vl-rerank` | 重排序 | - | [多模态](../concepts/multimodal.md)重排序 |

Embedding 维度选择建议：大规模搜索选 256/512 维，通用场景选 1024 维（默认），高精度选 1536/2048 维。详见[向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)。

## 全模态

全模态模型同时理解文本、音频、图片和视频，并输出文本和语音。三个系列：Qwen3.5-Omni（旗舰）、Qwen3-Omni-Flash（轻量低成本）、Qwen3.5-Livetranslate（专业翻译）。

- 实时交互：`qwen3.5-omni-plus-realtime`（WebSocket），支持 Function Calling 和联网搜索
- 音视频分析：`qwen3.5-omni-plus`（HTTP），音频最长 3 小时、视频最长 1 小时
- 深度推理：`qwen3-omni-flash`（HTTP），支持思考模式，成本更低
- 语音翻译：`qwen3.5-livetranslate-flash-realtime`（WebSocket），60 种语言约 3 秒延迟

详见[全模态](../../raw/model-user-guide/model-experience/omni.md)。

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


