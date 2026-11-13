# 异步任务

异步任务是百炼平台对耗时较长的 AI 操作（如图像/视频/3D 生成、文档与音视频解析等）所采用的标准执行模式：用户提交请求后立即获得 `task_id`，后续通过轮询或事件回调方式获取最终结果，避免长连接阻塞与超时风险。

## 在百炼平台的不同场景中，这个概念如何使用

异步任务是以下能力的默认且唯一支持的调用方式：

- **图像生成**：虽基础 `/v1/images/generations` 接口支持同步返回（适用于 Z-Image 等低延迟模型），但**所有图生图、局部重绘、风格迁移等创意工具类接口（`/v1/images/edits`）均强制异步**，响应中仅返回 `task_id`，需轮询 `GET /api/v1/tasks/{task_id}` 获取 `output`。
- **视频生成**：全部模型（HappyHorse、万相、可灵、Vidu、人像驱动等）**统一采用异步模式**。请求成功即返回 `task_id`，任务状态最长等待 5 分钟，超时置为 `failed`；结果通过 `output.video_url` 提供，有效期 24 小时。
- **3D 生成**：Tripo 全系列能力（文/图生 3D、后处理、动画绑定）**仅支持异步调用**，且必须显式设置请求头 `X-DashScope-Async: enable`；同步请求将被拒绝。任务创建后需轮询，建议首次延迟 10 秒，后续间隔 15–30 秒。
- **ParseX 解析与抽取**：文档解析（PDF/Word/音视频）、字段抽取（Schema-based extraction）**全部基于异步任务流**。提交后返回 `biz_id`（等效于 `task_id`），通过 `/parse/result` 或 `/extract/result` 轮询，状态为 `"success"` 时方可读取结构化输出。
- **其他长耗时模型**：包括多模态理解（如 `wanx2.1-kf2v-plus`）、语音识别（`paraformer-16k-1`）等，只要单次执行预期耗时 > 1s，平台即自动启用异步调度，开发者无需额外判断。

> ✅ 统一性提示：无论底层模型类型如何，所有异步任务均通过同一套任务管理接口操作：`GET /api/v1/tasks/{task_id}`（查询）、`GET /api/v1/tasks`（批量查询）、`POST /api/v1/tasks/{task_id}/cancel`（取消）。SDK 和 CLI 均已封装对应方法（如 Python SDK 的 `client.images.jobs.fetch()`）。

## 关键参数和配置

- **必填标识**：`task_id`（由初始 POST 请求返回）是所有异步操作的唯一凭证，有效期通常为 **24 小时**（部分模型如 ParseX 为 30 天，详见各文档）。
- **轮询控制**：
  - 建议间隔：文本类任务可设为 1–2 秒；图像/视频/3D 类任务推荐 **10–30 秒**，避免触发限流；
  - 限流阈值：单账号异步查询 QPS 上限为 **20**，超限返回 `429 Too Many Requests`；
  - 超时策略：任务总生命周期上限因模型而异（视频生成为 300 秒，3D 生成可达数分钟），超时后状态变为 `failed`，错误信息含具体原因。
- **回调替代方案（推荐生产环境使用）**：
  - 配置阿里云 **EventBridge** 订阅 `dashscope:System:AsyncTaskFinish` 事件，接收 JSON 格式完成通知；
  - 或在请求中指定 `callback_url`（需 HTTPS，支持 Basic Auth），平台将在任务完成后发起 POST 回调（含 `task_id`、`status`、`output` 等字段）。
- **强制头字段**：
  - 3D 生成：必须携带 `X-DashScope-Async: enable`；
  - 使用临时 OSS 文件时：必须携带 `X-DashScope-OssResourceResolve: enable`，否则请求被拒。

## 面向开发者，简洁实用

- ✅ **不要阻塞主线程**：永远假设异步任务不会即时返回结果；前端轮询请加 loading 状态，后端请用定时任务或消息队列解耦。
- ✅ **务必校验 `task_status`**：轮询响应中 `task_status` 字段必须为 `SUCCEEDED` 才可安全读取 `output`；`FAILED` 或 `CANCELED` 时检查 `error_code` 和 `error_message` 进行重试或告警。
- ✅ **及时获取结果**：任务完成后数据仅保留有限时间（通常 24 小时），请在轮询成功后立即下载或持久化 `url` 内容（如图片、视频、3D 模型文件）。
- ✅ **复用优于重跑**：ParseX 等服务支持复用已有解析结果（通过 `parsed_file_biz_id`），可显著降低延迟与成本；避免对同一文件重复提交解析任务。
- ⚠️ **地域与密钥强绑定**：华北2（北京）的 Tripo 任务只能用该地域 API Key 创建和查询；跨地域调用将直接失败，无重定向机制。

## 关联主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [api overview](../api/api-overview.md)
- [more about models](../api/more-about-models.md)


