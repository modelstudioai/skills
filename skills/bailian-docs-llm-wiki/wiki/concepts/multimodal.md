# 多模态

多模态（Multimodal）是指模型同时处理和生成多种信息形态（文本、图像、音频、视频、3D 等）的能力。在百炼平台中，多模态贯穿模型调用、知识库检索、向量化与排序等核心环节，是实现跨媒体理解与生成的基础技术概念。

## 多模态理解

百炼平台提供多种模型用于理解不同模态的输入内容：

- **视觉理解**：`qwen3.7-plus`、`qwen3.6-flash` 等模型支持图像分析和视频理解，单张图片最高 1600 万像素，视频最长 2 小时。[Token](token.md) 计算公式为 `h x w / (32 x 32) + 2`。`qwen3.5-ocr` 专为文档、表格、手写内容的 OCR 场景优化。
- **实时多模态交互**：Qwen-Omni-Realtime 系列模型通过 WebSocket 长连接实现低延迟的语音、视频、图像实时对话，支持 VAD 自动检测与 Manual 手动控制两种交互模式，并提供声音复刻、工具调用、联网搜索等能力。

## 多模态生成

平台覆盖图像、视频、3D 等生成场景：

- **图像生成与编辑**：千问（Qwen-Image）系列擅长文字渲染与图文混合布局；万相（Wan）系列覆盖文生图、图像编辑、多图参考生成；Z-Image 提供轻量快速的文生图能力。
- **视频生成**：万相 2.7 系列为主力模型，支持文生视频、图生视频、参考生视频、视频编辑、风格转换等。HappyHorse、Pixverse、Vidu、Kling 等第三方模型提供补充能力。所有视频生成 API 均采用[异步调用](async-invocation.md)模式（创建任务 → 轮询获取）。
- **3D 模型生成**：通过 Tripo 模型支持文生 3D、单图生 3D 和多图生 3D。

## 多模态向量与排序

向量化和排序模型将多模态内容统一到同一语义空间，是 RAG 检索和跨模态搜索的基础：

- **多模态向量模型**：`qwen3-vl-embedding`（2560 维）可将文本、图像、视频转换为同一语义空间的向量，支持独立向量（逐项对比）和融合向量（综合理解）两种类型，适用于以文搜图、以图搜视频等跨模态检索场景。`multimodal-embedding-v1`（1024 维）用于图片问答类知识库。
- **多模态排序模型**：`qwen3-vl-rerank` 支持对文本、图片、视频混合文档进行相关性排序，最大支持 100 条文本 / 40 张图片 / 4 个视频，单条最大 8,000 [Token](token.md)。多模态知识库的排序必须选用此模型。

## 多模态知识库

百炼知识库支持多种多模态场景：

| 知识库类型 | 多模态能力 | 说明 |
|-----------|-----------|------|
| 图片问答 | 图像理解 + 检索 | 仅支持 `multimodal-embedding-v1` 向量模型 |
| 音视频搜索 | 语音识别 + 视频帧提取 + 剧情解析 | 按时间轴结构化对齐 |
| 视觉理解文档搜索 | 富文本文档的图文并茂回复 | 自动切换为 `qwen3-vl-embedding` 向量模型 |

知识库创建时需选定类型且不可更改。多模态知识库的排序模型只能使用 `qwen3-vl-rerank`。

## 关键参数速查

| 场景 | 参数 / 配置 | 说明 |
|------|------------|------|
| 视觉理解 | 图片像素上限 1600 万 | [Token](token.md) = `h x w / (32 x 32) + 2` |
| 实时交互 | `session.turn_detection.type` | `server_vad` / `semantic_vad` / `null`（Manual） |
| 多模态向量 | `dimensions` | `qwen3-vl-embedding` 默认 2560 维 |
| 多模态排序 | `qwen3-vl-rerank` | 文本 100 条 / 图片 40 张 / 视频 4 个 |
| 视频生成 | [异步调用](async-invocation.md) | `X-DashScope-Async: enable`，轮询 task_id |
| 图像生成 | 模型选择 | 文字渲染用千问系列，通用生成用万相系列 |

## 开发者注意事项

- 多模态模型、Endpoint URL、[API Key](api-key.md) 必须属于同一地域，跨地域调用会失败。
- 知识库功能仅在华北2（北京）地域可用。
- 视频生成为异步接口，单次请求耗时通常 1-5 分钟，需通过 task_id 轮询结果。
- Token Plan 团队版支持多模态生成模型（图像生成），Coding Plan 仅支持文本生成模型。
- 实时多模态交互（Omni Realtime）通过 WebSocket 接入，北京与新加坡地域使用不同的接入地址。

## 关联主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [token plan guide](../guides/token-plan-guide.md)
- [model experience](../guides/model-experience.md)
- [knowledge base](../guides/knowledge-base.md)
- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [vector and sort](../api/vector-and-sort.md)


