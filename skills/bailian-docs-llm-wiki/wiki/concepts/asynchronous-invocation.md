# 异步调用

异步调用是一种非阻塞式 API 调用模式：客户端发起请求后立即获得任务标识（`task_id`），不等待模型执行完成，而是通过后续轮询或回调机制获取最终结果。该模式适用于耗时较长、资源密集型的生成任务（如高清图像编辑、视频合成、复杂[多模态](multimodal.md)推理），可避免连接超时、提升系统吞吐与稳定性。

## 在百炼平台的不同场景中，这个概念如何使用

- **图像生成（Image Generation）**：  
  适用于 `wan2.5-i2i-preview`、`kling/*`、`vidu/*` 及所有创意工具类模型（如 `wanx-poster-generation-v1`、`virtualmodel-v2`、`image-erase-completion`）。调用流程为两步：  
  ① `POST /api/v1/services/aigc/multimodal-generation/generation` 提交请求，返回 `task_id`；  
  ② 定期 `GET /api/v1/tasks/{task_id}` 查询状态，直至 `status == "SUCCESS"` 并获取 `output.image_url`。任务 URL 有效期为 24 小时。

- **视频生成（Video Generation）**：  
  **全部视频模型强制使用异步调用**（无同步选项）。必须在 HTTP 请求头中显式设置 `X-DashScope-Async: enable`，否则返回错误 `"current user api does not support synchronous calls"`。流程同上：先创建任务（`POST /api/v1/services/aigc/video-generation/video-synthesis`），再轮询 `/api/v1/tasks/{task_id}` 获取 `output.video_url`。

- **大语言模型（Qwen 系列）**：  
  当前 Qwen 文本/[多模态](multimodal.md)模型默认采用**同步调用**（含流式 `stream=true`）。但若启用需长时间运行的内置工具链（如深度联网搜索 + 代码解释器组合），或未来支持长上下文重排、批量文档解析等高延迟能力时，平台可能提供异步变体接口（具体以各模型 API 文档为准）。目前不推荐对标准 `qwen3.*` 文本生成使用异步模式。

> ✅ 共性原则：异步任务均强绑定地域（Workspace、API Key、Endpoint 必须同属一个 region），且 `task_id` 仅在创建地域内有效。

## 关键参数和配置

- **必需请求头（视频生成强制）**：  
  `X-DashScope-Async: enable` —— 缺失将直接报错，不可省略。

- **通用响应字段（所有异步接口）**：  
  - `task_id`（string）：全局唯一任务标识，用于后续查询；  
  - `status`（string）：取值包括 `"QUEUED"`、`"RUNNING"`、`"SUCCESS"`、`"FAILED"`、`"EXPIRED"`；  
  - `created_at` / `updated_at`（ISO8601 时间戳）：用于监控任务生命周期；  
  - `output`（object）：成功时包含结果 URL（如 `image_url`、`video_url`）及元数据（如 `width`、`height`、`duration`）；失败时含 `error.code` 与 `error.message`。

- **轮询建议配置**：  
  - 初始间隔：1–2 秒（任务刚提交时状态变化快）；  
  - 指数退避：后续间隔按 `min(30, interval × 1.5)` 递增，上限建议 30 秒；  
  - 超时保护：总等待时间不超过 23 小时（预留 1 小时容错），避免无限轮询。

- **注意事项**：  
  - 不要重复提交相同参数的任务（无幂等性保障）；  
  - 任务查询接口不计费，但频繁轮询（如 <500ms 间隔）可能触发限流；  
  - 异步任务不支持 `stream=true`，如需实时进度反馈，请关注 `status` 变化及 `output.progress` 字段（部分模型支持）。

面向开发者：优先选用异步模式处理 >5 秒预期耗时的生成任务；始终校验 `status` 再解析 `output`；将 `task_id` 存入业务数据库，便于重试与审计。

## 关联主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [qwen api reference](../api/qwen-api-reference.md)


