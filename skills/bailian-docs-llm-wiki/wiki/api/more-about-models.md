# [more](more.md) about models

本页汇总阿里云百炼模型调用过程中常用的配套 API 与 SDK 能力，涵盖临时 [API Key](../concepts/api-key.md)、异步任务管理与通知、子[业务空间](../concepts/workspace.md)调用、本地文件临时上传、SDK 连接复用等场景。这些能力围绕"安全、高效、可管控"地调用模型服务展开，是标准模型调用之外的关键补充。

## 临时 [API Key](../concepts/api-key.md)

在浏览器、移动 App 等不可信环境中直接持有永久 [API Key](../concepts/api-key.md) 存在泄露风险。可通过后端服务调用令牌接口生成临时 [API Key](../concepts/api-key.md)，将其下发到客户端使用，详见 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。

- 临时 [API Key](../concepts/api-key.md) 继承生成它的永久 [API Key](../concepts/api-key.md) 的全部权限（含模型、[知识库](../concepts/knowledge-base.md)的访问限制），无法进一步收窄权限。
- 默认有效期 60 秒，可通过 `expire_in_seconds` 参数设置，范围为 [1, 1800] 秒；到期自动失效，不能提前删除。

请求示例：

```
curl -X POST "https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

正常响应返回 `token`（生成的临时 Key，前缀 `st-`）与 `expires_at`（UNIX 时间戳，秒）。失败时返回 `code`/`message`/`request_id`，常见错误如 `InvalidApiKey`。

> **注意**：各地域（北京、新加坡、弗吉尼亚）的 [API Key](../concepts/api-key.md) 不互通，临时 Key 与生成它的永久 Key 必须属于同一地域。

## 异步任务管理

图像生成、视频生成等耗时模型采用异步机制：先创建任务拿到 `task_id`，再查询结果。阿里云百炼提供一组通用的异步任务接口，参见 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。三个接口的限流均为 20 QPS（按主账号 + 子账号维度计算）。

| 接口 | 方法与路径 | 用途 |
| --- | --- | --- |
| 查询单个任务 | `GET /api/v1/tasks/{task_id}` | 根据 task_id 查询状态与结果 |
| 批量查询 | `GET /api/v1/tasks/` | 按 time/status/model 等条件分页查询多个任务 |
| 取消任务 | `POST /api/v1/tasks/{task_id}/cancel` | 取消排队中的任务 |

任务状态包括 `PENDING`（排队）、`RUNNING`（处理中）、`SUCCEEDED`（成功）、`FAILED`（失败）、`CANCELED`（已取消）、`UNKNOWN`（不存在或未知）。批量查询的时间窗口跨度不能超过 24 小时；不传时间则默认查询最近 24 小时。

关键约束：

- 接口可查询/取消当前 [API Key](../concepts/api-key.md) 所属主账号下的所有任务（含该主账号下任意 [API Key](../concepts/api-key.md) 提交的任务），但无法跨主账号操作。
- 异步任务完成后通常保留 24 小时（以对应模型 API 文档为准），超时自动清理，届时无法再查询。
- 取消接口**仅支持 `PENDING` 状态**的任务，其他状态会返回 `UnsupportedOperation`（HTTP 400）。
- 含多个子任务的任务，只要有一个子任务成功，整体状态即为 `SUCCEEDED`，失败子任务的错误信息在 `output.results` 中单独展示；`task_metrics` 给出 `TOTAL`/`SUCCEEDED`/`FAILED` 统计。

## 异步任务完成通知（避免轮询）

频繁轮询结果接口会浪费资源并可能触发 20 QPS 限流。阿里云百炼已接入事件总线 EventBridge，任务完成（无论成功或失败）后主动上报"任务完成事件"，由事件总线推送到您配置的接收端，收到通知后只需查询一次即可拿到结果。详见 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。

事件关键信息：

- 事件源：`acs.dashscope`
- 事件类型：`dashscope:System:AsyncTaskFinish`
- 事件总线默认为 `default`（北京地域的云服务专用总线）
- 事件 `data` 中包含 `task_id`、`task_status`、`start_time`、`end_time`、`region`、`request_id`、`api_key_id`、`user_api_unique_key` 等字段

两种常见接收方案：

- **HTTP 回调 URL**：提供一个支持公网或 VPC 访问、接收 POST 请求的 HTTP 接口，事件总线直接推送。接入简单，适合大多数通用场景。
- **RocketMQ 消息队列**：事件总线将事件投递到 RocketMQ，业务方消费消息。支持消息无丢失与失败重试，适合对可靠性要求较高的场景。

在事件总线控制台需创建事件规则：事件模式指定 `source=acs.dashscope`、`type=dashscope:System:AsyncTaskFinish`，并可通过 `data.user_api_unique_key` 等字段做过滤（例如只转发某个模型的事件）。事件目标配置为 HTTP 或 RocketMQ。

> **注意**：通知方案不限流、实时性高、不占用业务系统资源，但接入比轮询复杂；轮询方案接入简单但受 20 QPS 限制且实时性低。高并发、大规模或对实时性要求高的任务建议用通知方案。

## 子[业务空间](../concepts/workspace.md)的模型调用

默认[业务空间](../concepts/workspace.md)的 API Key 可调用所有模型，权限过大且费用难以分账。可将 RAM 用户归入子[业务空间](../concepts/workspace.md)，仅授权必要模型，并要求使用该子空间的 API Key 调用，参见 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。

适用场景：

- **模型调用权限管控**：限制某类用户只能调用被授权的模型。
- **费用分账**：为不同业务/场景创建独立子空间，各自独立出账。

调用方式与默认空间基本一致，区别在于**必须使用该子[业务空间](../concepts/workspace.md)的 API Key**。支持 OpenAI 兼容与 DashScope 两种协议：

- **OpenAI 兼容**：北京地域 `base_url` 为 `https://dashscope.aliyuncs.com/compatible-mode/v1`；新加坡地域为 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`，需把 `WorkspaceId` 替换为真实[业务空间](../concepts/workspace.md) ID。
- **DashScope**：北京地域千问大语言模型 HTTP 地址为 `POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`；新加坡地域需在 SDK 中设置 `base_http_api_url = 'https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1'`。

准备工作要点：

1. 在子[业务空间](../concepts/workspace.md)创建 API Key 并配置到环境变量 `DASHSCOPE_API_KEY`。
2. 调用标准模型（如 `qwen-plus`）前，需为该子空间设置模型调用权限。
3. 在阿里云百炼调优并部署的模型**无需模型调用授权**，但只能由其所在[业务空间](../concepts/workspace.md)的 API Key 调用，且**仅支持 DashScope 协议**，不支持 OpenAI 兼容方式。

> **注意**：北京与新加坡地域的 API Key 不同，切换地域必须更换对应 Key；新加坡地域的 OpenAI 兼容与 DashScope 地址都需要把 `WorkspaceId` 替换为真实[业务空间](../concepts/workspace.md) ID。

## 上传本地文件获取临时 URL

调用[多模态](../concepts/multimodal.md)、图像、视频、音频模型时通常需要传入文件 URL。阿里云百炼提供**免费**临时存储空间，可上传本地文件得到以 `oss://` 为前缀的临时 URL，参见 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

使用流程：

1. 获取上传凭证：`GET https://dashscope.aliyuncs.com/api/v1/uploads?action=getPolicy&model={model_name}`，返回 `upload_host`、`upload_dir`、`OSSAccessKeyId`、`Signature`、`policy` 等 OSS 上传凭证。
2. 用凭证将文件 POST 到 `upload_host`，得到 `oss://{upload_dir}/{file_name}` 形式的临时 URL。
3. 调用模型时使用该 URL，并**必须在 HTTP 请求头显式添加** `X-DashScope-OssResourceResolve: enable`，否则接口报错。

也可用 DashScope 命令行工具一步完成：`dashscope oss.upload --model qwen-vl-plus --file cat.png`（推荐用环境变量传 Key，避免明文暴露）。

关键限制：

- **文件与模型绑定**：上传时必须指定模型名，且须与后续调用的模型一致，不同模型不能共享文件；不同模型对文件大小限制不同。
- **文件与主账号绑定**：上传与调用所用的 API Key 必须属于同一阿里云主账号，文件仅限该主账号及对应模型使用。
- **有效期 48 小时**：到期自动清理，文件不可查询、修改或下载，只能通过 URL 参数在模型调用时使用。
- **上传凭证接口限流 100 QPS**（按"主账号+模型"维度），且不支持扩容。

> **注意**：临时 URL 有效期仅 48 小时、上传限流 100 QPS 且不可扩容，**请勿用于生产环境**。生产环境建议使用阿里云 OSS 等稳定存储，确保文件长期可用并规避限流。

## SDK 连接复用配置

高并发场景下频繁建连会导致请求超时、资源消耗大。[DashScope SDK](../concepts/dashscope-sdk.md) 支持连接复用以降低开销，参见 [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)。

### Java SDK

内置连接池机制，默认启用。关键参数（通过 `ConnectionConfigurations` 配置到 `Constants.connectionConfigurations`）：

| 参数 | 含义 | 默认值 |
| --- | --- | --- |
| `connectTimeout` | 建立连接超时 | 120 秒 |
| `readTimeout` | 读取数据超时 | 300 秒 |
| `writeTimeout` | 写入数据超时 | 60 秒 |
| `connectionIdleTimeout` | 空闲连接超时 | 300 秒 |
| `connectionPoolSize` | 连接池最大连接数 | 32 |
| `maximumAsyncRequests` | 全局最大并发请求数 | 32 |
| `maximumAsyncRequestsPerHost` | 单主机最大并发请求数 | 32 |

建议：`maximumAsyncRequests` 需小于等于 `connectionPoolSize`，`maximumAsyncRequestsPerHost` 需小于等于 `maximumAsyncRequests`，否则可能出现请求阻塞。低延迟场景可缩短 `connectTimeout`；高并发场景适当增大 `connectionPoolSize` 与空闲超时。

### Python SDK

通过传入自定义 Session 实现连接复用：

- **异步（协程）**：用 `aiohttp.ClientSession` 配合 `aiohttp.TCPConnector`，参数 `limit`（总连接数，默认 100）、`limit_per_host`（单主机连接数，默认 0 不限制）、`ssl`（SSL 上下文）。
- **同步**：用 `requests.Session`，同一 Session 内多次请求复用底层 TCP 连接。

推荐用 `with` 语句或 `try/finally` 管理 Session 生命周期，确保连接正确释放；异步架构（asyncio、FastAPI 等）用[异步调用](../concepts/async-invocation.md)方式，传统同步架构用同步方式即可。

## 常见限制与注意事项汇总

- **限流**：异步任务接口 20 QPS；文件上传凭证接口 100 QPS（不可扩容）；临时 API Key 不可手动删除，靠 TTL 自动失效。
- **地域隔离**：北京、新加坡、弗吉尼亚的 API Key 不互通；新加坡地域调用地址需带 `WorkspaceId`。
- **权限继承**：临时 API Key 继承源 Key 全部权限；子业务空间 API Key 的可调模型由该空间授权范围决定；调优部署的模型无需授权但只能由所属空间 Key 调用。
- **数据保留**：异步任务结果通常保留 24 小时；临时文件 URL 保留 48 小时；超期均自动清理且不可恢复。
- **生产可用性**：临时文件存储仅供开发/测试，生产环境请用 OSS；通知方案（EventBridge + HTTP/MQ）比轮询更适合高并发场景。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)











