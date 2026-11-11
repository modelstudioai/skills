# 异步任务模式

异步任务模式是百炼平台对计算密集型、耗时较长的模型服务（如视频生成、3D建模、音视频/文档解析等）所采用的标准调用范式：客户端提交任务后立即返回任务标识符，服务端后台执行并持久化结果，客户端通过轮询或事件通知方式获取最终输出。

## 在百炼平台的不同场景中，这个概念如何使用

- **视频生成**：所有视频类 API（文生视频、图生视频、数字人、口型替换等）强制启用异步模式，需在请求头中显式设置 `X-DashScope-Async: enable`；调用返回 `task_id`，后续通过 `/api/v1/tasks/{task_id}` 查询状态与结果，典型耗时 1–5 分钟。
- **ParseX 文档与音视频解析**：统一采用 `biz_id` 作为任务唯一标识，提交 `/parse/submit` 或 `/extract/submit` 后，轮询 `/parse/result` 或 `/extract/result` 获取结构化输出；结果默认保留 30 天，支持复用（7 天内同类型解析结果可直接用于字段抽取）。
- **3D 生成（Tripo）**：全部接口仅支持华北2（北京）地域，必须携带 `X-DashScope-Async: enable`；任务创建后返回 `task_id`，通过标准 `/api/v1/tasks/{task_id}` 接口轮询，建议首次延迟 10 秒、后续间隔 15–30 秒。
- **其他计算密集型模型**：包括高分辨率图像生成、长文本语音转写（如 `paraformer-8k-v2`）、多图输入的复杂推理等，默认启用异步机制；是否启用由模型能力决定，不依赖用户选择——若接口文档未明确声明“同步支持”，即视为仅支持异步。

> ✅ 统一行为：所有异步任务均**不可取消**（除 `PENDING` 状态外），结果保留期以各服务文档为准（通常为 24–30 小时），超期后查询返回空或过期错误。

## 关键参数和配置

- **强制请求头**：  
  `X-DashScope-Async: enable` —— 缺失将直接报错 `"current user api does not support synchronous calls"`。该头是异步模式的开关凭证，与模型类型强绑定，不可省略或设为 `disable`。

- **任务标识符**：  
  - 视频/3D/通用模型：返回 `task_id`（字符串），用于 `/api/v1/tasks/{task_id}` 查询；  
  - ParseX 解析与抽取：返回 `biz_id`（字符串），用于 `/parse/result?biz_id=...` 或 `/extract/result?biz_id=...` 查询。

- **轮询建议策略**（面向开发者）：  
  | 任务类型         | 首次查询延迟 | 后续轮询间隔 | 状态检查字段       |  
  |------------------|--------------|----------------|--------------------|  
  | 文本/轻量推理     | 1–2 秒       | 1–3 秒         | `data.status == "success"` |  
  | 图像生成          | 3–5 秒       | 5–10 秒        | `data.status in ["success", "failed"]` |  
  | 视频/3D/音视频解析 | 10 秒        | 15–30 秒       | `data.status`（值为 `success` / `failed` / `processing`） |  
  > ⚠️ 避免高频轮询：单 IP 或 API Key 下轮询 QPS 超过 20 可能触发限流；推荐优先使用 [HTTP 回调或 EventBridge 事件通知](../../raw/model-api-reference/more-about-models/async-task-api.md) 替代轮询。

- **结果保留与清理**：  
  - 通用异步任务：结果默认保留 **24 小时**（以 `/api/v1/tasks/{task_id}` 返回的 `created_at` 时间戳起算）；  
  - ParseX 解析结果：保留 **30 天**，抽取复用窗口为 **7 天**；  
  - 所有结果超期后无法恢复，不提供手动清理接口。

## 面向开发者，简洁实用

- ✅ **必做三件事**：  
  1. 请求头务必包含 `X-DashScope-Async: enable`；  
  2. 检查响应体中的 `task_id` 或 `biz_id`，并安全存储；  
  3. 使用标准任务查询接口轮询（或配置回调），**不要尝试重放原始请求体**（会创建新任务）。

- ❌ **常见错误规避**：  
  - 混用旧版路径（如 `/api/v1/services/aigc/image2video/video-synthesis`）与新版异步头 —— 路径与协议需严格匹配模型文档；  
  - 对 `failed` 状态任务重复轮询 —— 应记录错误码（如 `FileSizeExceeded`, `ServiceQuotaExhausted`）并针对性修复；  
  - 在前端直传临时 API Key + 异步轮询 —— 临时密钥有效期短、限流严，**仅限调试，严禁生产使用**。

- 🚀 **进阶建议**：  
  - 生产环境优先接入 [EventBridge 事件总线](../../raw/model-api-reference/more-about-models/async-task-api.md)，订阅 `dashscope:System:AsyncTaskFinish` 事件，实现零轮询、低延迟结果消费；  
  - SDK 用户请复用 HTTP 客户端连接池（Python：传入 `httpx.AsyncClient`；Java：配置 `connectionPoolSize`），避免每轮询新建连接。

## 关联主题页

- [video generation api](../api/video-generation-api.md)
- [api overview](../api/api-overview.md)
- [3d generation](../api/3d-generation.md)
- [more about models](../api/more-about-models.md)


