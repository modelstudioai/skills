# [more](more.md) about models

本文档面向开发者，系统梳理百炼平台模型调用的关键扩展能力，涵盖[异步任务](../concepts/asynchronous-task.md)管理、子业务空间隔离、临时资源获取与连接优化等核心场景。所有能力均基于标准 API Key 或其派生凭证（如临时 API Key）实现，不改变基础模型调用语义，但显著提升安全性、可维护性与生产稳定性。

## 支持的模型/功能

百炼平台支持的模型调用能力不仅限于同步推理，还覆盖以下关键扩展功能：

- **[异步任务](../concepts/asynchronous-task.md)处理**：适用于图像生成、视频合成、语音转写等长耗时任务。需通过 `POST /api/v1/tasks` 创建任务，再通过 `GET /api/v1/tasks/{task_id}` 查询结果。该机制由 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) 统一提供，支持查询、批量列表与取消（仅 `PENDING` 状态）。
- **事件驱动通知**：为避免轮询开销与限流风险，推荐通过事件总线接收任务完成通知。支持配置 HTTP 回调 URL 或 RocketMQ 消息队列，事件类型为 `dashscope:System:AsyncTaskFinish`，详情见 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。
- **子业务空间隔离调用**：支持在非默认业务空间中调用模型，用于权限管控与费用分账。调用时必须使用该子空间专属的 API Key，并按地域配置对应 `base_url`（如北京地域为 `https://dashscope.aliyuncs.com/compatible-mode/v1`），详见 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。
- **临时文件托管**：多模态模型（如 `qwen3-vl-plus`）需传入文件 URL 时，可通过 `/api/v1/uploads?action=getPolicy` 获取上传凭证，将本地文件上传至百炼托管 OSS 并获得 `oss://` 前缀的临时 URL（有效期 48 小时）。调用时须在 Header 中添加 `X-DashScope-OssResourceResolve: enable`，参见 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

> **注意**：文档 5 明确指出“文件上传与模型调用所使用的 API Key 必须属于同一个阿里云主账号”，而文档 4 中子业务空间的 API Key 也归属其主账号。二者逻辑一致，无矛盾；但需确保上传和调用均使用同一子空间的 API Key，而非混用默认空间与子空间密钥。

## 关键参数

| 参数 | 说明 | 取值范围/示例 | 来源 |
|------|------|----------------|------|
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒，默认 60 秒 | [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `task_id` | [异步任务](../concepts/asynchronous-task.md)唯一标识符 | UUID 格式字符串，如 `a8532587-xxxx-xxxx-xxxx-0c46b17950d1` | [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) |
| `model_name` | 文件上传时绑定的模型名 | 必须与后续模型调用的 `model` 字段完全一致，如 `qwen3-vl-plus` | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `connectionPoolSize` | Java SDK 连接池最大连接数 | 默认 32，高并发建议设为 256 | [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |
| `limit_per_host` | Python 异步 SDK 每主机连接数限制 | 默认 0（无限制），生产建议设为 30 | [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |

## 使用方式

- **临时凭证生成**：在不可信环境（如浏览器）中调用模型前，后端应调用 `POST https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800` 生成 `st-***` 格式临时 Key，其权限继承自发起请求的永久 API Key。
- **异步任务流程**：  
  1. 调用模型创建接口（如 `POST /api/v1/services/aigc/image-synthesis/generation`）获取 `task_id`；  
  2. 轮询 `GET /api/v1/tasks/{task_id}`（推荐间隔 ≥1s）或配置事件总线接收 `dashscope:System:AsyncTaskFinish` 事件；  
  3. 事件中解析 `task_id` 后，调用一次 `GET /api/v1/tasks/{task_id}` 获取最终结果。
- **子空间调用**：  
  - OpenAI 兼容模式：设置 `base_url` 为 `https://dashscope.aliyuncs.com/compatible-mode/v1`（北京）或 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`（新加坡），并使用子空间 API Key；  
  - DashScope 原生模式：北京地域无需额外配置 `base_url`，新加坡地域需显式设置 `dashscope.base_http_api_url`。
- **连接复用**：  
  - Java：通过 `Constants.connectionConfigurations` 配置连接池参数；  
  - Python 同步：传入 `requests.Session()` 实例至 `Generation.call(session=...)`；  
  - Python 异步：传入 `aiohttp.ClientSession(connector=...)` 至 `AioGeneration.call(session=...)`。

## 限制和注意事项

- **临时 API Key**：无法手动删除，到期自动失效；其权限严格继承自生成它的永久 Key，**不支持细粒度权限降级**。
- **异步任务查询**：单账号 QPS 限流为 20，任务数据保留期为 24 小时（以各任务文档为准），超时后 `GET /api/v1/tasks/{task_id}` 返回 `UNKNOWN` 状态。
- **临时文件**：  
  - 文件大小上限 1GB，且必须与调用模型名称严格匹配；  
  - **严禁用于生产环境**：48 小时有效期、100 QPS 限流且不可扩容，生产应使用阿里云 OSS 自建存储。
- **子业务空间**：调用标准模型（如 `qwen-plus`）前，需在控制台为该空间**显式授权模型调用权限**；调优部署的模型则无需授权，但仅限本空间 Key 调用。
- **连接复用**：Python 同步调用中若复用 `requests.Session`，务必在生命周期结束时调用 `session.close()`；Java 中 `connectionPoolSize` 应 ≤ `maximumAsyncRequests`，否则可能阻塞请求。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


