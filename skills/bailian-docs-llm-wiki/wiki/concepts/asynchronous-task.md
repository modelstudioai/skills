# 异步任务模式

异步任务模式是百炼平台对计算密集型、耗时较长的模型服务（如视频生成、3D建模、音视频/文档解析等）所采用的标准调用范式：客户端提交任务后立即返回唯一任务标识（`task_id` 或 `biz_id`），结果需通过轮询或事件回调方式异步获取，而非阻塞等待。

## 在百炼平台的不同场景中，这个概念如何使用

- **视频生成（Video Generation）**：所有视频类 API（HappyHorse、万相、PixVerse、Kling 等）强制启用异步模式。必须在请求头中显式设置 `X-DashScope-Async: enable`，否则返回错误；创建任务后获得 `task_id`，通过 `GET /api/v1/tasks/{task_id}` 轮询状态，典型耗时 1–5 分钟。

- **3D 生成（3D Generation）**：Tripo 全系列能力（文生/图生 3D 网格、Gaussian Splatting、网格分割、自动绑骨等）均仅支持异步调用，且**严格限定为华北2（北京）地域**；同样依赖 `X-DashScope-Async: enable` 请求头和 `task_id` 轮询机制。

- **ParseX 文档与音视频解析（API Overview）**：文档解析、音视频处理、结构化字段抽取三类能力统一采用 `biz_id` 作为任务标识符，通过 `/parse/submit` 或 `/extract/submit` 提交，再以 `biz_id` 查询 `/parse/result` 或 `/extract/result`；不支持同步返回，且结果保留策略差异化（解析结果保留 30 天，字段抽取复用窗口仅 7 天）。

- **通用异步模型服务（More about Models）**：平台明确区分同步模型（如 `qwen-plus`）与异步模型（如 `wanx2.1-kf2v-plus`、`paraformer-16k-1`）。异步任务支持全生命周期管理：创建、查询（分页/过滤）、取消（仅 `PENDING` 状态）、事件通知（HTTP 回调或 RocketMQ），并提供 SDK 连接复用与限流适配建议。

## 关键参数和配置

- **强制请求头**：
  - `X-DashScope-Async: enable`：所有异步模型调用必需，缺失将报错 `current user api does not support synchronous calls`。
  - `Authorization: Bearer <API_KEY>`：标准鉴权，API Key 必须与 Endpoint 地域一致（如北京 Key 不能调用新加坡 Endpoint）。

- **任务标识符**：
  - `task_id`：视频生成、3D 生成、通用异步模型使用，UUID 格式，有效期 24 小时。
  - `biz_id`：ParseX 解析与抽取服务使用，字符串格式，有效期依业务类型而定（解析 30 天，抽取复用 7 天）。

- **轮询与事件配置**：
  - 轮询推荐间隔：文本类任务可设 1–2 秒，图像/视频/3D 类建议 5–30 秒，避免触发 QPS 限流（查询接口限流 20 QPS）。
  - 事件驱动：配置 HTTP 回调 URL 或 RocketMQ Topic，监听 `dashscope:System:AsyncTaskFinish` 事件，收到后单次查询结果，更高效可靠。

- **地域与 Endpoint 绑定**：
  - 模型、API Key、Endpoint URL 必须同属一个地域（如 `cn-beijing`、`ap-southeast-1`），跨地域调用必然失败。
  - 推荐使用业务空间专属域名：`https://{WorkspaceId}.{region}.maas.aliyuncs.com`。

- **SDK 注意事项**：
  - Java：通过 `Constants.connectionConfigurations` 配置连接池（默认 32，高并发建议 256）与超时。
  - Python：构造 `AsyncClient` 时显式传入 `httpx.AsyncClient(max_connections=100)`，避免默认无限制导致资源耗尽。

面向开发者，请始终以“提交 → 等待 → 查询”为基本心智模型，勿尝试同步等待；合理利用事件通知降低轮询开销，并严格校验地域、时效性与权限隔离约束。

## 关联主题页

- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [api overview](../api/api-overview.md)
- [more about models](../api/more-about-models.md)


