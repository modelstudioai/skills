# 多模态

多模态（Multimodal）指在同一模型或服务中同时处理文本、图像、音频、视频等多种类型数据的能力。在百炼平台上，多模态既体现为模型的输入/输出能力（如视觉理解、语音对话、图文视频生成），也体现为向量与检索层面的跨模态语义对齐。

## 在百炼平台中的典型场景

### 实时音视频交互（Omni-Realtime）

Qwen-Omni-Realtime 系列基于 WebSocket 提供低延迟的实时多模态对话，支持语音输入/输出、图像输入、语音活动检测（VAD）、工具调用与联网搜索，适用于语音助手、智能客服等场景。图像通过 `input_image_buffer.append`（JPG/JPEG，Base64 编码）随音频流一起输入，输出模态由 `modalities` 控制（`["text"]` 或 `["text","audio"]`）。

### 视觉理解

视觉理解模型支持图像分析、视频理解和 OCR。旗舰模型 `qwen3.7-plus` 支持 1M 上下文、最长约 2 小时视频；`qwen3.5-ocr` 专为文档、表格、手写内容优化。图像按 `h x w / (32 x 32) + 2` 计算 Token，单张最高约 1600 万像素。

### 图像生成与编辑

涵盖文生图、图像编辑、图像翻译、风格迁移等，主要模型族为千问（Qwen-Image）、万相（Wan/Wanx）、Z-Image 与可灵（Kling），通过 HTTP 或 [DashScope SDK](dashscope-sdk.md) 调用。图像编辑与图文混排本质上是文本 + 图像的多模态输入输出。

### 视频生成

文生视频、图生视频、参考生视频、视频编辑与人像动画均采用异步调用（创建任务 -> 轮询结果）。其中"参考生视频"（如 `wan2.7-r2v`）接受图片/视频/音频的多模态输入，可实现多角色互动与音色一致性；数字人（`wan2.2-s2v`）基于单图 + 音频生成说话/唱歌视频。

### 知识库（RAG）多模态检索

知识库支持文档搜索、图片问答、音视频搜索等多模态场景。图片问答类知识库使用 `multimodal-embedding-v1`（1024 维）向量模型；视觉理解场景自动切换为 `qwen3-vl-embedding`（qwen3 多模态向量）；多模态知识库的排序只能选 `qwen3-vl-rerank`。音视频解析会做语音识别、视频帧提取与剧情解析，并按时间轴结构化对齐。

### 多模态向量与排序

多模态向量模型（如 `qwen3-vl-embedding`）将文本、图像、视频映射到同一语义空间，支持以文搜图、以图搜视频等跨模态检索，可生成"独立向量"（逐项对比）或"融合向量"（综合理解）。排序侧的 `qwen3-vl-rerank` 支持对文本、图片、视频候选做统一重排（文本 100 条 / 图片 40 张 / 视频 4 段）。

## 关键参数与配置

- **输出模态（`modalities`）**：Omni-Realtime 中决定返回纯文本还是文本 + 音频，默认 `["text","audio"]`。
- **图像输入**：Realtime 通过 `input_image_buffer.append` 传入 Base64 编码的 JPG/JPEG；生成/理解类通过请求体中的图像 URL 或 Base64 传入。
- **视频参数**：视觉理解支持最长约 2 小时 / 2GB 视频；视频生成为异步任务，需轮询 `task_id`。
- **向量维度与类型**：多模态向量按模型固定或可选维度（如 `qwen3-vl-embedding` 默认 2560），并可选择独立或融合向量类型。
- **多模态重排**：`qwen3-vl-rerank` 的 `query` 支持文本和图片两种查询模态，`top_n` 控制返回数量。
- **知识库多模态解析**：创建知识库时选择解析方式（大模型文档解析 / Qwen VL 解析 / 音视频解析），部分配置（如 Meta 抽取、多轮对话改写）创建后不可更改。

## 开发者提示

- 实时语音图像交互优先走 WebSocket 的 Omni-Realtime API，非实时的视频生成走异步任务模式。
- 需要跨模态检索时，向量与重排要成对选用多模态模型（`qwen3-vl-embedding` + `qwen3-vl-rerank`），避免与纯文本模型混用导致语义空间不一致。
- 图片问答类知识库的向量模型（`multimodal-embedding-v1`）在创建时锁定，选型前需确认维度与场景匹配。

## 关联主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [knowledge base](../guides/knowledge-base.md)
- [model experience](../guides/model-experience.md)
- [vector and sort](../api/vector-and-sort.md)



