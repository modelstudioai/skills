# 异步处理

异步处理是百炼平台对耗时较长任务（如文档解析、视频生成、知识库同步等）采用的标准执行模式：客户端提交任务后立即获得唯一任务标识（如 `job_id`、`task_id` 或 `biz_id`），服务端后台执行，客户端通过轮询或事件通知方式获取最终结果，避免请求长时间阻塞。

## 在百炼平台的不同场景中，这个概念如何使用

- **RAG 知识库管理**：文档上传、切片、索引构建等操作均以异步任务形式执行。调用 `/v1/documents` 或 `/v1/sync_jobs` 后返回 `job_id`，需轮询 `/v1/sync_jobs/{job_id}` 查询状态（`PENDING`/`RUNNING`/`SUCCESS`/`FAILED`）。
- **视频生成 API**：所有视频类模型（HappyHorse、万相、爱诗、数字人等）强制启用异步模式，请求头必须携带 `X-DashScope-Async: enable`；提交后返回 `task_id`，24 小时内有效，需轮询 `/api/v1/tasks/{task_id}` 获取 `output.video_url`。
- **ParseX 文档与音视频处理**：无论是图文解析（PDF/Word）、音视频解析（ASR/分镜/摘要）还是字段抽取（Schema-based extraction），全部基于 `biz_id` 异步模型；提交 `/parse/submit` 或 `/extract/submit` 后，必须轮询 `/parse/result` 或 `/extract/result`，不可假设同步响应。
- **通用异步任务管理**：平台统一提供 `/api/v1/tasks/{task_id}` 接口支持跨服务任务状态查询；高并发场景推荐结合事件总线（EventBridge）订阅 `dashscope:System:AsyncTaskFinish` 事件，实现免轮询的事件驱动架构。
- **多模态模型调用**：图像生成、语音转写（如 `paraformer-16k-1`）等长耗时模型明确归类为“异步模型”，其调用流程与视频生成一致，需任务 ID + 结果拉取。

## 关键参数和配置

- **任务标识符（必需）**：  
  - `job_id`（RAG 同步任务）  
  - `task_id`（视频生成、通用异步任务）  
  - `biz_id`（ParseX 解析与抽取任务）  
  所有 ID 均为 UUID 格式字符串，是轮询和结果获取的唯一凭证，**必须持久化存储，不可丢弃**。

- **强制异步开关（部分接口必需）**：  
  - `X-DashScope-Async: enable`：视频生成 API 的硬性请求头，缺失将直接报错 `"current user api does not support synchronous calls"`。

- **轮询建议配置（面向开发者）**：  
  - 初始间隔：1–2 秒（文本/轻量任务）或 5–10 秒（视频/大文件解析）  
  - 指数退避：建议最大重试间隔 ≤30 秒，总超时 ≥ 任务预期最大耗时 × 1.5（如视频任务预期 5 分钟，总超时设为 480 秒）  
  - 错误码处理：收到 `409 ResultNotReady` 应继续轮询；`400 FileDownloadFailed` 等不可恢复错误应终止并告警。

- **生命周期约束（必须遵守）**：  
  - `task_id` / `job_id` / `biz_id` 有效期统一为 **24 小时**（视频生成、通用异步任务）或 **7 天**（ParseX 解析结果复用期）；超时后无法查询，数据被系统自动清理。  
  - 异步任务结果默认保留 **24 小时**（任务完成起计），超时后不可访问。

## 面向开发者，简洁实用

- ✅ **不要写同步等待循环**：所有异步接口均不支持 `stream=true` 或阻塞式响应，强行等待会超时失败。  
- ✅ **轮询是底线，事件是升级选项**：低频调用用轮询即可；高频或关键链路务必接入 EventBridge HTTP 回调或 RocketMQ，规避 QPS 限流与网络抖动风险。  
- ✅ **ID 是你的“订单号”**：`task_id` 等必须记录到业务日志或数据库，用于问题排查、重试追踪与用户进度展示。  
- ❌ **不要复用过期 ID**：24 小时后 `GET /api/v1/tasks/{task_id}` 将返回 `404`，需重新提交任务。  
- ❌ **不要在前端暴露永久 API Key**：异步任务常需较长时间运行，前端调用必须配合后端签发临时 Key（`expire_in_seconds ≤ 1800`），杜绝密钥泄露风险。

## 关联主题页

- [rag api](../api/rag-api.md)
- [video generation api](../api/video-generation-api.md)
- [getting started overview](../guides/getting-started-overview.md)
- [api overview](../api/api-overview.md)
- [more about models](../api/more-about-models.md)


