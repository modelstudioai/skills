# [more](more.md) about models

本主题汇总阿里云百炼模型 API 之外的若干**周边能力与运维接口**：临时 API Key 派发、[异步任务](../concepts/async-task.md)管理（查询/批量查询/取消/事件通知）、DashScope SDK 连接复用、子[业务空间](../concepts/workspace.md)隔离调用，以及本地文件临时 URL 上传。这些能力面向需要在生产场景中安全地分发凭证、高并发地调度模型、并合理治理多[业务空间](../concepts/workspace.md)与文件输入的开发者。

## 临时 API Key

在浏览器、移动 App 等不可信环境中直接使用永久 API Key 会带来泄露风险。可由后端服务通过 `POST https://dashscope.aliyuncs.com/api/v1/tokens` 接口换取**临时 API Key**，默认有效期 60 秒，支持通过 `expire_in_seconds` 参数指定 \[1, 1800\] 秒 TTL。返回的 `token`（以 `st-` 开头）继承生成它的永久 Key 的全部权限（含模型、知识库访问限制），且**到期自动失效，不能手动删除**。详细字段、错误码与 curl 示例见 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。

> **注意**：北京、新加坡、弗吉尼亚三个地域的永久 API Key 互相独立，临时 Key 也必须在对应地域调用。

## [异步任务](../concepts/async-task.md)管理

文生图、文生视频、长语音识别等**长耗时任务**采用"先创建任务返回 task_id，再凭 task_id 获取结果"的异步调用模型。除模型自身的提交接口外，百炼额外提供一组**通用的[异步任务](../concepts/async-task.md)管理 API**：

| 接口 | 方法/路径 | 用途 |
| --- | --- | --- |
| 查询单个任务 | `GET /api/v1/tasks/{task_id}` | 拉取任务状态及结果 |
| 批量查询任务 | `GET /api/v1/tasks/` | 按 `start_time` / `end_time` / `model_name` / `status` / 分页条件批量查询 |
| 取消任务 | `POST /api/v1/tasks/{task_id}/cancel` | 仅支持 `PENDING` 状态的任务，其他状态返回 `UnsupportedOperation` |

任务状态枚举为 `PENDING`/`RUNNING`/`SUCCEEDED`/`FAILED`/`CANCELED`/`UNKNOWN`。三个接口共用 20 QPS 的账号级限流；查询返回结果**仅保留 24 小时**（具体以对应模型文档为准），过期会被自动清理。权限上只能查询/取消**同一阿里云主账号**下的任务（含其名下任何 API Key 提交的任务）。完整入参、出参字段与样例响应见 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。

## [异步任务](../concepts/async-task.md)完成通知（替代轮询）

高频轮询查询接口会同时消耗业务系统资源并触发 20 QPS 限流。百炼已将[异步任务](../concepts/async-task.md)接入**事件总线 EventBridge**：任务完成（无论成功失败）会生成 `dashscope:System:AsyncTaskFinish` 事件，可通过事件总线推送给两类目标，业务侧仅需 **一次** 拉取结果即可：

- **HTTP 回调 URL**：业务方提供一个支持公网或 VPC 的 `POST` 接口接收 JSON 事件。配置简单，适合大多数场景。
- **云消息队列 RocketMQ**：事件转发至 RocketMQ Topic，业务方通过 PushConsumer 消费。能保证消息不丢失、支持失败重试，适合**高可靠性**要求。

事件 Body 关键字段：`data.task_id`、`data.task_status`、`data.user_api_unique_key`（格式 `apikey:version:group:task:function-call:model`，可用于事件模式过滤特定模型，例如按 `{"suffix": ":paraformer-8k-v1"}` 过滤）、`data.region` 等。配置流程依次为：在事件总线控制台查询事件 → 创建事件规则（事件源 `acs.dashscope`、事件类型 `dashscope:System:AsyncTaskFinish`） → 选择 HTTP / RocketMQ 事件目标。同一规则可挂多个事件目标。完整步骤、Java RocketMQ SDK 消费样例与排查指引见 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。

> **注意**：事件规则的**地域必须与任务地域一致**（北京地域规则不会转发上海地域的事件）；接收不到事件时优先检查这一项。

## DashScope SDK 连接复用

高并发场景下频繁建立 TCP 连接会显著放大延迟与资源开销。DashScope 各 SDK 都支持复用连接，但配置方式按语言而异：

### Java SDK

内置 OkHttp 连接池，默认启用，建议根据并发量手动覆盖默认值：

| 参数 | 默认 | 单位 | 说明 |
| --- | ---: | --- | --- |
| `connectTimeout` | 120 | 秒 | 建立连接超时；低延迟场景应调小 |
| `readTimeout` | 300 | 秒 | 读超时 |
| `writeTimeout` | 60 | 秒 | 写超时 |
| `connectionIdleTimeout` | 300 | 秒 | 空闲连接保留时间；高并发可延长 |
| `connectionPoolSize` | 32 | 个 | 最大连接数 |
| `maximumAsyncRequests` | 32 | 个 | 全局并发请求数，必须 ≤ `connectionPoolSize` |
| `maximumAsyncRequestsPerHost` | 32 | 个 | 单 host 并发请求数，必须 ≤ `maximumAsyncRequests` |

通过 `Constants.connectionConfigurations = ConnectionConfigurations.builder()...build();` 设置（建议 SDK ≥ 2.12.0）。

### Python SDK

按调用方式选择：
- **异步**：传入 `aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=..., limit_per_host=...))` 给 `AioGeneration.call(..., session=session)`；
- **同步**：用 `requests.Session()` 传给 `Generation.call(..., session=session)`，推荐用 `with` 语句自动释放。

完整代码示例（含连接池参数、`base_http_api_url` 配置、API Key 环境变量读取）见 [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)。

## 子[业务空间](../concepts/workspace.md)的模型调用

百炼默认[业务空间](../concepts/workspace.md)的 API Key 权限较大（可调用所有模型）。当需要按 RAM 用户授权可用模型，或为不同业务/场景**独立账单**时，可在子[业务空间](../concepts/workspace.md)中创建 API Key 并按以下要点调用：

- **调用标准模型**（如 `qwen-plus`）：在子[业务空间](../concepts/workspace.md)内为该空间 [设置模型调用权限](https://help.aliyun.com/zh/model-studio/permission-management-overview#f642213a1f38l) 后再调用。
- **调用百炼调优后部署的模型**：无需额外授权，但**只能由该模型所在[业务空间](../concepts/workspace.md)的 API Key 调用**；且**仅支持 DashScope 协议**，不支持 OpenAI 兼容方式。
- **地域差异**：
  - 北京地域 OpenAI 兼容：`base_url = https://dashscope.aliyuncs.com/compatible-mode/v1`
  - 新加坡地域 OpenAI 兼容：`base_url = https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`（DashScope 协议同理替换 host）

调用代码与默认[业务空间](../concepts/workspace.md)几乎一致，**关键区别只是必须使用子[业务空间](../concepts/workspace.md)自己的 API Key**。Python/Java/Node.js/Go/C#/PHP/curl 完整示例见 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。

## 本地文件临时 URL（仅测试场景）

多模态、图像、视频、语音模型通常要求传入 URL 形式的输入文件。百炼提供**免费的临时存储**，可将本地文件上传换取 `oss://` 前缀的临时 URL，**有效期 48 小时**。可通过三种方式上传：

1. **代码上传**（Python / Java）：先调 `GET /api/v1/uploads?action=getPolicy&model=<model>` 获取 OSS 上传凭证，再用 multipart 表单 `POST` 到 `data.upload_host`，最后拼接 `oss:// + key` 得到 URL。
2. **命令行**：`dashscope oss.upload --model qwen-vl-plus --file cat.png`（需 Python SDK ≥ 1.24.0）。
3. **DashScope SDK**：直接把 `oss://...` 作为图片/视频参数传入，SDK 自动添加必要请求头。

使用临时 URL 时有**四条硬约束**：

- **文件与模型绑定**：上传时必须指定 `model`，后续调用必须用同一模型；
- **文件与主账号绑定**：上传与调用的 API Key 必须**同属一个阿里云主账号**；
- **48 小时有效期**：到期自动清理，无法续期；
- **HTTP 直接调用必须加请求头** `X-DashScope-OssResourceResolve: enable`，否则服务端无法解析 `oss://` 链接（DashScope SDK 自动处理；OpenAI SDK 不支持此能力）。

接口限流为按"主账号 + 模型"维度的 **100 QPS** 且不支持扩容。完整入参字段、错误码（`InvalidParameter.DataInspection`、`AccessDenied`、`Throttling.RateQuota`）及代码示例见 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

> **注意**：临时 URL 与上传凭证接口均**不适用于生产环境与压测**。生产请使用 [阿里云 OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss) 等长期稳定的存储服务。

## 错误码参考

上述所有接口在调用失败时返回的 `code` / `message` 取值，请统一查阅百炼[错误码](https://help.aliyun.com/zh/model-studio/error-code)页面；本主题中列出的接口特有错误码（如[异步任务](../concepts/async-task.md)的 `UnsupportedOperation`、临时 URL 的 `InvalidParameter.DataInspection` / `AccessDenied` / `Throttling.RateQuota`）已在各自源文档中标注语义和处置建议。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)









