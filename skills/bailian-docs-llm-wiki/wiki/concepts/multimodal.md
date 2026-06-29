# 多模态

多模态指模型能够同时接收、理解或生成多种数据形态（文本、图像、音频、视频、3D 等）的能力。在百炼平台中，多模态既体现为"输入多模态"（一张图或一段视频加文本提问），也体现为"输出多模态"（生成图像、视频、3D 资产、语音），并通过统一的 DashScope HTTP / WebSocket 接口与 API Key 鉴权对外提供。

## 平台中的多模态场景

百炼把多模态能力按"理解"与"生成"两条主线组织：

- **多模态理解（输入侧）**：视觉理解模型（如 `qwen3.7-plus`、`qwen3.6-flash`、`qwen-vl-ocr`）接收图像或视频并输出文本回答，支持 OCR、视频理解、最长 2 小时视频；多模态向量模型（`qwen3-vl-embedding`、`multimodal-embedding-v1`）把文本、图片、视频统一编码为向量用于语义检索；跨模态排序模型（`qwen3-vl-rerank`）对图文混合召回结果做精排。
- **多模态生成（输出侧）**：图像生成（千问 `qwen-image-2.0-pro`、万相 `wan2.7-image-pro`、`z-image-turbo` 等）、视频生成（`happyhorse-1.1` 系列、`wan2.7` 系列、PixVerse、Vidu、可灵等）、3D 生成（`Tripo/Tripo-H3.1`、`Tripo/Tripo-P1.0`）、语音合成与语音转语音（`cosyvoice-v3.5-plus`、`qwen3.5-omni-plus-realtime`）。
- **全模态实时交互**：Qwen-Omni-Realtime 系列（`qwen3.5-omni-plus-realtime` / `qwen3.5-omni-flash-realtime` / `qwen3-omni-flash-realtime` / `qwen-omni-turbo-realtime`）通过 WebSocket 长连接实现语音、视频、图像的低延迟对话，支持 VAD 自动检测与 Manual 手动控制两种交互模式，并叠加声音复刻、Function Calling、联网搜索等能力。

## 调用方式

| 形态 | 协议 | 典型接口 |
| --- | --- | --- |
| 同步多模态理解 / 文生图 | HTTP | `POST /api/v1/services/aigc/multimodal-generation/generation`、OpenAI 兼容 `/compatible-mode/v1/chat/completions` |
| 异步生成（图像/视频/3D） | HTTP | 创建任务 `POST /api/v1/services/aigc/...` 获取 `task_id`，再 `GET /api/v1/tasks/{task_id}` 轮询 |
| 实时全模态对话 | WebSocket | `wss://dashscope.aliyuncs.com/api-ws/v1/realtime`（北京）|
| 多模态向量 / 排序 | HTTP | `POST /api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`、`/compatible-api/v1/reranks` |

## 关键参数与配置

- **鉴权与地域**：统一使用 API Key，通过 `Authorization: Bearer $DASHSCOPE_API_KEY` 传递。模型、Endpoint URL、API Key 必须属于同一地域，跨地域调用会鉴权失败；3D 生成（Tripo）仅限华北2（北京）。北京/新加坡建议迁移到业务空间专属域名以获得更好性能。
- **异步任务头**：图像、视频、3D 等耗时生成接口必须带 `X-DashScope-Async: enable`，否则报错 `current user api does not support synchronous calls`。`task_id` 有效期 24 小时，请勿重复创建任务，轮询即可；产物下载链接通常有效期 2 小时。
- **多模态消息**：视觉理解通过多模态消息接口传入图片 URL 或 Base64；单张图片上限 1600 万像素，Token 计算公式 `h × w / (32 × 32) + 2`，分辨率越高消耗越大。
- **实时会话配置**：通过 `session.update` 设置 `turn_detection`（`server_vad` / `semantic_vad` / `null`）、音色、`threshold`、`silence_duration_ms`、`idle_timeout_ms` 等；声音复刻时 `target_model` 必须与后续 Omni 调用指定的模型一致。
- **向量维度**：`text-embedding-v4` 支持自定义 `dimensions`（64–2048），`multimodal-embedding-v1` 等多模态向量模型用于跨模态检索。

## 使用建议

需要"看图/看视频回答问题"选视觉理解模型；需要"从文本/图像生成视觉内容"走异步生成任务并轮询；需要"实时语音+视觉对话"用 Qwen-Omni-Realtime 的 WebSocket 接口；需要"图文统一检索"用多模态向量 + 跨模态排序。所有路径共用同一套 API Key 与 DashScope 域名，差别仅在接口路径、协议（HTTP/WebSocket）和调用模式（同步/异步）。

## 关联主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [model experience](../guides/model-experience.md)
- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [vector and sort](../api/vector-and-sort.md)


