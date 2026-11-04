# 异步调用

异步调用是百炼平台对长耗时任务（通常 >3 秒）的标准执行模式：客户端发起请求后立即返回任务标识符（如 `task_id` 或 `biz_id`），服务端后台执行任务，结果需通过轮询或事件通知方式获取。该模式解耦请求与响应，保障 API 网关稳定性，适用于图像生成、视频合成、3D 建模、语音转写、文档/音视频解析等计算密集型场景。

## 在百炼平台的不同场景中，这个概念如何使用

- **图像生成**：`wanx-virtualmodel`、`shoemodel-v1`、`creative-poster-generation-v1`、`wanx-x-painting` 等编辑与垂直工具类模型强制异步；调用 `POST /api/v1/services/aigc/multimodal-generation/generation` 创建任务，返回 `task_id`，24 小时内可轮询 `GET /api/v1/tasks/{task_id}` 查询状态与结果。
  
- **视频生成**：所有视频模型（HappyHorse、WanX、PixVerse、Vidu、Kling 等）**仅支持异步调用**，必须在请求头中显式设置 `X-DashScope-Async: enable`，否则报错；任务创建后通过 `task_id` 轮询，支持事件总线（EventBridge）回调接收完成通知。

- **3D 生成**：Tripo 全系列模型（文生3D、图生Splat、网格重拓扑、贴图生成、自动绑骨等）**仅限异步**，且目前仅华北2（北京）地域可用；同样依赖 `X-DashScope-Async: enable` 请求头和 `task_id` 生命周期管理。

- **语音与多模态处理**：语音转写模型（如 `paraformer-16k-1`）、图像理解类长流程任务（如多步编辑链）均归入异步任务体系，统一由 `/api/v1/tasks/{task_id}` 接口管理。

- **结构化解析（ParseX）**：文档与音视频解析、基于 Schema 的字段抽取全部采用异步范式，使用 `biz_id` 作为任务凭证；提交 `/parse/submit` 或 `/extract/submit` 后，通过 `/parse/result` 或 `/extract/result` 轮询，结果保留期为 30 天（复用场景要求 7 天内）。

> ✅ 统一特征：所有异步任务均返回唯一 ID、支持状态查询（`PENDING`/`RUNNING`/`SUCCEEDED`/`FAILED`/`CANCELED`）、支持取消（仅 `PENDING` 状态）、结果有效期明确（24 小时至 30 天不等）。

## 关键参数和配置

| 参数/配置项 | 位置 | 说明 | 注意事项 |
|-------------|------|------|----------|
| `X-DashScope-Async` | HTTP 请求头 | **强制启用异步模式的开关**，值必须为 `"enable"` | 缺失或值错误将导致 `400 Bad Request`（如视频 API 明确报 `"current user api does not support synchronous calls"`） |
| `task_id` / `biz_id` | 响应体 & 后续请求路径/体 | 任务全局唯一标识（UUID 格式），用于轮询、取消、结果获取 | 不可跨接口混用（如 `task_id` 不能用于 ParseX 的 `/parse/result`）；不可自行构造或猜测 |
| `status` 字段 | 轮询响应体（如 `data.status`） | 当前任务状态，典型值：`PENDING`, `RUNNING`, `SUCCEEDED`, `FAILED`, `CANCELED` | `SUCCEEDED` 表示主任务成功（子任务可能部分失败）；`FAILED` 时 `code` 和 `message` 提供具体错误原因 |
| 轮询间隔策略 | 客户端逻辑 | 建议采用指数退避（如 1s → 2s → 4s → 8s），避免高频轮询触发 QPS 限流（默认 20 QPS） | 对图像/视频等长任务，初始间隔建议 ≥2s；文本类可缩短至 500ms |
| 事件通知（EventBridge） | 平台侧配置 | 配置 HTTP 回调 URL 或 RocketMQ Topic，接收 `dashscope:System:AsyncTaskFinish` 事件 | 比轮询更高效、实时、免限流，**高并发或生产环境强烈推荐**；需自行实现幂等处理 |

## 面向开发者，简洁实用

- ✅ **必做三件事**：  
  1. 请求头加 `X-DashScope-Async: enable`（图像/视频/3D/ParseX 全部必需）；  
  2. 保存响应中的 `task_id` 或 `biz_id`；  
  3. 用该 ID 轮询或配置事件通知，**不要等待同步响应**。

- ⚠️ **常见踩坑点**：  
  - 忘记设 `X-DashScope-Async` → 直接报错，尤其视频 API 会明确拒绝；  
  - 混用 `task_id` 和 `biz_id` → 返回 `404 Not Found` 或 `InvalidParameter`；  
  - 轮询超时未处理 `ResultNotReady` → 导致任务“卡住”，应持续重试直至终态；  
  - 未校验 `status === 'SUCCEEDED'` 就直接读取 `output` 字段 → 可能为空或结构异常。

- 🚀 **最佳实践建议**：  
  - 生产环境优先配置 EventBridge HTTP 回调，降低客户端复杂度与资源消耗；  
  - 使用 SDK 封装的异步方法（如 Python SDK 的 `client.async_generate()`）自动处理轮询逻辑；  
  - 为每个异步任务添加业务上下文标签（如 `trace_id`），便于日志追踪与问题定位；  
  - 设置任务超时兜底（如轮询 5 分钟无终态则主动取消并告警）。

## 关联主题页

- [more about models](../api/more-about-models.md)
- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [api overview](../api/api-overview.md)


