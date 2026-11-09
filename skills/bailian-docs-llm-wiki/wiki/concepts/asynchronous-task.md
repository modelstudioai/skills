# 异步任务

异步任务是百炼平台中一类需“提交后等待执行、再主动查询或接收通知”的模型调用模式，适用于计算耗时长、I/O密集型或结果生成不可即时返回的场景（如图像/视频/3D生成、音视频解析、结构化抽取等）。与同步调用直接返回结果不同，异步任务返回唯一 `task_id`，开发者需通过该 ID 轮询状态或配置事件回调获取最终输出。

## 在百炼平台的不同场景中，这个概念如何使用

- **图像生成**：`wanx2.1-t2i-turbo`、`kling`、`vidu-image` 等模型均以异步方式运行。调用 `/v1/images/generations` 时需在请求头中显式设置 `X-DashScope-Async: enable`，成功响应中返回 `task_id`，后续通过 `GET /api/v1/tasks/{task_id}` 查询结果。
  
- **视频生成**：所有视频模型（`wan3.0`、`pixverse`、`vidu`、`kling` 等）强制采用异步范式。必须携带 `X-DashScope-Async: enable` 请求头，任务创建后获得 `task_id`，轮询间隔建议 ≥5 秒；`task_id` 有效期为 24 小时。

- **3D 生成**：Tripo 全系列能力（文生/图生 3D、Gaussian Splat、网格分割、贴图、重拓扑等）仅支持异步调用，且**当前仅限华北2（北京）地域**。同样依赖 `X-DashScope-Async: enable` 头与 `task_id` 轮询机制。

- **文档与音视频解析（ParseX）**：所有解析与字段抽取任务均为异步，但使用 `biz_id`（而非 `task_id`）作为任务标识符。`parse/submit` 与 `extract/submit` 返回各自独立的 `biz_id`，须分别调用对应 `result` 接口查询，不可混用。

- **跨业务空间调用**：子空间中的异步任务（如子空间部署的 `wanx` 图像模型）必须使用该子空间专属 API Key，并确保 Endpoint 域名与工作空间 ID、地域严格匹配（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），否则将因权限或路由失败导致任务无法创建或状态不可查。

> ✅ **最佳实践**：优先采用**事件通知**替代轮询。配置事件总线监听 `dashscope:System:AsyncTaskFinish` 事件，仅在 `task_status === "SUCCEEDED"` 时拉取结果，可规避轮询限流（默认 20 QPS）、降低延迟并提升系统可靠性。HTTP 回调适合快速验证，RocketMQ 更适合高可用生产环境。

## 关键参数和配置

| 参数 | 类型 | 说明 | 注意事项 |
|------|------|------|----------|
| `task_id` / `biz_id` | string (UUID) | 异步任务唯一标识符，由 `submit` 接口返回 | `task_id` 用于模型类异步（图像/视频/3D），`biz_id` 用于 ParseX 类异步；二者隔离，不可通用 |
| `X-DashScope-Async` | header | 必选请求头，值固定为 `enable` | **绝大多数新模型强制要求**；缺失将导致 400 错误（Legacy 模型如 wan2.1 除外） |
| `expire_in_seconds` | integer | 临时 API Key 有效期（秒） | 范围 `[1, 1800]`，默认 60 秒；异步任务若超时未完成，需确保 Key 在轮询期间仍有效 |
| `model_name` | string | 文件上传时绑定的目标模型名（如 `qwen3-vl-plus`） | 用于多模态输入预校验，上传后获得的 OSS URL 仅对该模型有效 |

- **轮询注意事项**：
  - 建议最小间隔 ≥5 秒（视频/3D 类任务建议 ≥10 秒）；
  - `task_id` / `biz_id` 有效期统一为 **24 小时**（ParseX 解析结果保留期为 30 天，但任务 ID 本身仍 24 小时失效）；
  - 状态字段常见值：`"QUEUED"` → `"RUNNING"` → `"SUCCEEDED"` / `"FAILED"` / `"CANCELLED"`。

- **错误重试策略**：
  - `ResultNotReady`（HTTP 409）：必须重试，使用原 ID；
  - `FileDownloadTimeout`（HTTP 400）：可重试；
  - `FileDownloadFailed` / `NotExistBizId` / `InvalidTaskId`：不可重试，需检查输入参数或网络可达性。

## 面向开发者，简洁实用

- ✅ **立即上手**：只需两步——  
  1. 发送带 `X-DashScope-Async: enable` 的 POST 请求，拿到 `task_id`；  
  2. 用该 ID 调用 `GET /api/v1/tasks/{task_id}`，检查 `status` 字段。  

- ⚠️ **避坑提醒**：  
  - 不要硬编码 `task_id` 或复用过期 ID；  
  - 不要在同一请求中混用 `model_name` 与实际调用模型；  
  - OpenAI 兼容方式调用异步模型时，**必须使用工作空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），通用域名可能导致权限错配；  
  - 临时文件 URL（OSS 直链）通常仅 1 小时有效，异步任务结果中的 `output.url` 同理，需及时下载或转存。

- 🚀 **进阶推荐**：  
  - 生产环境务必接入事件总线，订阅 `dashscope:System:AsyncTaskFinish`；  
  - 结合 SDK 的连接池配置（如 Java 的 `connectionPoolSize=256`）提升并发任务提交效率；  
  - 对接 RocketMQ 时，消费端需幂等处理（同一 `task_id` 可能重复投递）。

## 关联主题页

- [more about models](../api/more-about-models.md)
- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [api overview](../api/api-overview.md)
- [3d generation](../api/3d-generation.md)


