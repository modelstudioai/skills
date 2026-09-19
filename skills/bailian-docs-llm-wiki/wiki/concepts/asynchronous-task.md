# 异步任务

异步任务是百炼平台中处理高耗时、长周期模型推理任务的核心执行模式：调用方提交请求后立即获得 `task_id`，无需等待模型计算完成，而是通过轮询或事件回调方式获取最终结果。该模式显著提升客户端响应性与服务端资源利用率，适用于视频生成、3D建模、大文件翻译等典型场景。

## 在百炼平台的不同场景中，这个概念如何使用

- **视频生成**：所有视频类 API（如 HappyHorse、万相3.0、爱诗、EMO、LivePortrait）均强制采用异步模式，任务创建后需轮询 `/api/v1/tasks/{task_id}` 查询状态，典型耗时 1–5 分钟；跨地域调用（Endpoint、API Key、Workspace ID 不一致）将直接失败。
  
- **3D生成**：Tripo 系列模型（`Tripo/Tripo-H3.1`、`Tripo/Tripo-P1.0`）仅支持异步调用，必须在华北2（北京）地域执行，`task_id` 有效期为 24 小时，结果 URL（如 `pbr_model_url`）有效期仅 2 小时，需及时下载。

- **[多模态](multimodal.md)翻译（Qwen-MT-Uni）**：对 PDF/DOCX/PPTX/XLSX/长音频（3秒–60分钟）等大体积输入，必须启用异步模式；小文本、短图等低延迟场景可选同步调用，但异步仍是推荐默认路径，以统一错误处理与重试逻辑。

- **图像生成**：万相 V2.5 及以下、可灵（Kling）、Vidu、Z-Image Turbo、所有创意工具（如 facechain、wordart、aitryon-plus）均**不支持同步调用**，必须走异步流程；千问图像模型（`qwen-image-3.0-pro`）虽支持同步，但在批量生成或多图编辑等复杂请求下，仍建议主动启用异步以保障稳定性。

- **通用异步管理**：平台提供统一的异步任务生命周期接口 `/api/v1/tasks/{task_id}`（支持查询、取消），并支持通过事件总线订阅 `dashscope:System:AsyncTaskFinish` 事件实现免轮询回调（需配置 HTTP 回调 URL 或 MQ 消费端）。

## 关键参数和配置

- **必需请求头**：  
  `X-DashScope-Async: enable` —— 缺失将返回错误 `"current user api does not support synchronous calls"`。该头是触发异步流程的唯一开关，不可省略或设为其他值。

- **必需请求体字段**：  
  `model`: 字符串，精确匹配模型名（区分大小写与斜杠，如 `happyhorse-t2v`、`Tripo/Tripo-P1.0`、`qwen-mt-uni`）；  
  `input`: 结构依模型而异（如 `{"prompt": "..."}`、`{"fileUrl": "https://..."}`、`{"image_url": "...", "audio_url": "..."}`），三者互斥且不可为空。

- **可选但强推荐的配置**：  
  - 轮询间隔 ≥15 秒（避免触发 20 QPS 限流）；  
  - 任务查询前校验 `task_id` 有效性（长度、格式）；  
  - 对结果 URL（如 `video_url`、`pbr_model_url`、`rendered_image_url`）做一次 HEAD 请求验证可访问性，并在 2 小时内完成下载；  
  - 生产环境务必配置异步回调（HTTP 或 MQ），避免轮询带来的连接开销与状态延迟。

- **地域与密钥约束**：  
  所有异步任务严格绑定地域——`Endpoint URL`、`API Key`、`Workspace ID` 必须同属一个地域（如华北2/北京）。混用将导致 401 或 403 错误，无降级或自动路由机制。

## 面向开发者，简洁实用

- ✅ **记住一句话**：异步 = 提交 → 拿 `task_id` → 查结果（轮询或回调）→ 下载输出。  
- ✅ **必做三件事**：  
  1. 请求头加 `X-DashScope-Async: enable`；  
  2. 用对地域 Endpoint 和对应 API Key；  
  3. 24 小时内查任务、2 小时内取结果。  
- ❌ **避免踩坑**：  
  - 不要尝试同步调用明确标注“仅异步”的模型（如 Tripo、EMO、Kling）；  
  - 不要跨地域混用密钥与 Endpoint；  
  - 不要高频轮询（<15 秒间隔）或忽略 `task_id` 过期；  
  - 不要假设结果 URL 永久有效——它只是临时凭证。  
- 🚀 **进阶建议**：  
  使用 DashScope SDK 的 `wait_for_task()` 封装（Python/Java 均支持），或接入事件总线实现零轮询交付；对批量任务，用 `task_id` 数组 + 并发查询（控制 QPS ≤20）提升吞吐。

## 关联主题页

- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [qwen mt translation models](../api/qwen-mt-translation-models.md)
- [more about models](../api/more-about-models.md)
- [image generation](../api/image-generation.md)


