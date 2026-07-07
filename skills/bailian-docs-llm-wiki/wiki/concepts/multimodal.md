# 多模态

多模态（Multimodal）指模型同时处理和生成多种信息形态（文本、图像、音频、视频、3D 等）的能力。百炼平台围绕多模态提供了从理解、生成到检索排序的完整模型矩阵，开发者可按场景选择对应的模型和 API。

## 百炼平台的多模态能力谱

百炼平台的多模态能力覆盖以下维度：

| 维度 | 典型场景 | 代表模型 |
|------|----------|----------|
| 多模态理解 | 图像分析、视频理解、OCR | qwen3.7-plus、qwen3.6-flash、qwen3.5-ocr |
| 实时多模态交互 | 语音+视频实时对话 | qwen3.5-omni-realtime 系列 |
| 图像生成与编辑 | 文生图、图像编辑、文字渲染 | wan2.7-image-pro、qwen-image-2.0-pro、z-image-turbo |
| 视频生成与编辑 | 文生视频、图生视频、视频编辑 | happyhorse-1.1 系列、wan2.7 系列 |
| 3D 生成 | 文生 3D、图生 3D | Tripo/Tripo-H3.1、Tripo/Tripo-P1.0 |
| 多模态向量 | 跨模态检索（以文搜图、以图搜视频） | qwen3-vl-embedding |
| 多模态排序 | 图文视频混合 Rerank | qwen3-vl-rerank |

## 多模态理解

视觉理解模型接受图像或视频作为输入，与文本提示配合完成分析、问答、OCR 等任务。推荐从 qwen3.7-plus 开始——它支持 1M 上下文、最长 2 小时视频输入、每张图片最高 1600 万像素，同时具备 Function Calling 和结构化输出能力。图像 Token 计算公式为 `h x w / (32 x 32) + 2`。

## 实时多模态交互

Qwen-Omni-Realtime API 基于 WebSocket 长连接实现低延迟的语音、视频、图像实时对话。支持 VAD 自动检测与 Manual 手动控制两种交互模式，并可配合声音复刻、工具调用、联网搜索等能力。关键配置包括：

- **交互模式**：`turn_detection.type` 设为 `server_vad`（自动检测）或 `null`（手动控制）
- **VAD 灵敏度**：`threshold` 范围 [-1.0, 1.0]，默认 0.5
- **静音时长**：`silence_duration_ms` 范围 [200, 6000]，默认 800
- **静默超时**：`idle_timeout_ms` 范围 [5000, 30000]，超时后模型主动引导对话

## 多模态生成

### 图像生成

百炼提供千问（Qwen-Image）、万相（Wan/Wanx）、Z-Image 等多个图像生成模型系列。wan2.7-image-pro 支持文生图最高 4K 输出、文字渲染和角色一致性；z-image-turbo 速度快且成本低，适合只需生成不需编辑的场景；qwen-image-2.0-pro 支持负向提示词和多张变体。

### 视频生成

视频生成 API 覆盖文生视频、图生视频、参考生视频、视频编辑、数字人等场景，底层模型包括万相（Wan）、HappyHorse、Pixverse、Vidu、Kling 等。所有接口采用[异步调用](async-invocation.md)模式（创建任务 → 轮询获取），单次生成通常耗时 1-5 分钟。

### 3D 生成

基于 Tripo 模型实现文生 3D、单图生 3D 和多图生 3D，产出带 PBR 材质贴图的 GLB 模型。同样采用[异步调用](async-invocation.md)模式，仅限北京地域使用。

## 多模态检索与排序

多模态向量模型（qwen3-vl-embedding）将文本、图像和视频映射到同一语义空间，支持跨模态检索。向量类型分为独立向量（逐项对比）和融合向量（综合理解多模态内容）。

多模态排序模型（qwen3-vl-rerank）可对文本、图片、视频混合的候选文档进行相关性排序，最多支持 100 条文本、40 张图片或 4 段视频的单次排序请求，适用于 RAG 流程中的精排阶段。

## 调用方式差异

不同多模态能力的调用方式有所不同：

| 能力类型 | 调用方式 | 响应模式 |
|----------|----------|----------|
| 多模态理解（视觉） | [OpenAI 兼容接口](openai-compatible-interface.md) / [DashScope SDK](dashscope-sdk.md) | 同步流式 |
| 实时交互 | WebSocket 长连接 | 双向实时 |
| 图像/视频/3D 生成 | HTTP REST + 异步头 | 异步轮询 |
| 向量与排序 | [OpenAI 兼容接口](openai-compatible-interface.md) / [DashScope SDK](dashscope-sdk.md) | 同步 |

开发者在接入多模态能力时需注意：模型、Endpoint URL 与 API Key 必须属于同一地域，跨地域调用会失败。推荐使用[业务空间](workspace.md)专属域名（`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）以获得更好的性能与稳定性。

## 关联主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [model experience](../guides/model-experience.md)
- [video generation api](../api/video-generation-api.md)
- [image generation](../api/image-generation.md)
- [3d generation](../api/3d-generation.md)
- [vector and sort](../api/vector-and-sort.md)


