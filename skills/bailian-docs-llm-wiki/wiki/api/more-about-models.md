# [more](more.md) about models

本文档面向开发者，汇总百炼平台模型调用的关键扩展能力：包括临时凭证管理、[异步任务](../concepts/asynchronous-task.md)处理、子业务空间隔离、连接复用优化及多模态文件上传等核心机制。这些能力共同支撑高并发、高安全、可治理的生产级模型服务集成。

## 支持的模型/功能

百炼平台支持多种模型调用模式与配套功能：
- **标准模型与调优模型**：标准模型（如 `qwen-plus`）需在子业务空间中[显式授权](raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)后方可调用；而调优并部署的模型仅限其所属业务空间的 API Key 调用，无需额外授权。
- **[异步任务](../concepts/asynchronous-task.md)模型**：图像生成、视频合成、语音转写等长耗时模型采用异步机制，需通过任务 ID 查询结果或取消任务。相关接口统一收口于 `/api/v1/tasks`，支持查询、批量列表和取消操作 [异步任务管理 API](raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。
- **事件驱动通知**：为避免轮询，可通过事件总线配置 HTTP 回调 URL 或 RocketMQ 接收 `dashscope:System:AsyncTaskFinish` 事件，实现任务完成后的主动推送 [通过HTTP回调URL或MQ接收异步任务完成通知](raw/model-api-reference/more-about-models/async-task-api.md)。
- **多模态文件支持**：调用 VL、图像、音视频模型时，可上传本地文件获取 `oss://` 开头的临时 URL（有效期 48 小时），该 URL 与模型强绑定且仅限同一主账号使用 [上传本地文件获取临时URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

> **注意**：文档 4 中“调用在阿里云百炼[调优](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)并部署的模型，**无需模型调用授权**”与文档 6 中“文件上传时必须指定模型名称，且该模型须与后续调用的**模型一致**”存在隐含冲突——调优模型无公开模型名，其 `model` 参数实际为部署时指定的服务名（如 `my-qwen3-vl-finetuned`），而非标准模型名。开发者需以部署服务名为准传入 `model` 字段。

## 关键参数

| 参数 | 说明 | 典型值/范围 | 来源 |
|------|------|-------------|------|
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒，默认 60 秒 | [生成临时API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `task_id` | [异步任务](../concepts/asynchronous-task.md)唯一标识符 | UUID 格式字符串，如 `a8532587-xxxx-xxxx-xxxx-0c46b17950d1` | [异步任务管理 API](raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) |
| `contain_result` | 事件通知是否内嵌结果数据 | `true` / `false`，默认 `false` | [通过HTTP回调URL或MQ接收异步任务完成通知](raw/model-api-reference/more-about-models/async-task-api.md) |
| `model_name` | 文件上传时指定的模型名（用于权限与存储策略绑定） | 必须与后续模型调用的 `model` 参数完全一致，如 `qwen3-vl-plus` | [上传本地文件获取临时URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `connectionPoolSize` | Java SDK 连接池最大连接数 | 默认 32，建议根据并发量调整（如 256） | [DashScope SDK连接复用配置](raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |

## 使用方式

### 临时凭证
在不可信环境（如浏览器、App）中调用模型时，应由可信后端调用 `/api/v1/tokens` 接口生成临时 API Key（`st-***`），并设置合理 TTL（推荐 ≤ 180 秒）。临时 Key 继承父 Key 的全部权限，但无法手动删除，到期自动失效。

### 异步任务
1. 提交任务（如 `client.images.jobs.create(...)`）获取 `task_id`；
2. 轮询 `GET /api/v1/tasks/{task_id}`（建议间隔 ≥ 1s，避免触发 20 QPS 限流）或配置事件总线接收推送；
3. 若任务处于 `PENDING` 状态，可调用 `POST /api/v1/tasks/{task_id}/cancel` 取消。

### 子业务空间
调用子空间模型时：
- **必须使用该子空间生成的 API Key**；
- **必须匹配地域域名**：北京用 `dashscope.aliyuncs.com` 或 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，新加坡用 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`；
- OpenAI 兼容模式下，`base_url` 需指向 `compatible-mode/v1`；DashScope 原生模式下，SDK 需显式传入 `workspace` 和 `region`。

### 连接复用
- **Java SDK**：通过 `Constants.connectionConfigurations` 设置连接池参数（如 `connectionPoolSize`, `readTimeout`）；
- **Python SDK**：构造 `Client` 或 `AsyncClient` 时传入复用的 `httpx.Client` / `httpx.AsyncClient` 实例，并配置 `limits`。

### 多模态文件
1. 调用 `GET /api/v1/uploads?action=getPolicy&model={model_name}` 获取上传策略；
2. 按策略向 OSS `upload_host` 发起表单上传，获得 `oss://...` URL；
3. 在模型请求中传入该 URL，并**必须添加 Header**：`X-DashScope-OssResourceResolve: enable`。

## 限制和注意事项

- **临时 API Key**：继承父 Key 所有权限，包括知识库访问；各地域 API Key 不互通，调用时需确保 Endpoint 与 Key 地域一致 [生成临时API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。
- **异步任务保留期**：任务完成后通常保留 24 小时，超时后数据被自动清理，无法再查询 [异步任务管理 API](raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。
- **文件上传限流**：凭证接口按“主账号+模型”维度限流 100 QPS，**明确不适用于生产环境与压测场景**；生产环境务必使用 OSS 等自有存储 [上传本地文件获取临时URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)。
- **地域一致性**：子业务空间调用、文件上传、临时 Key 生成均需严格匹配地域（北京/新加坡/弗吉尼亚/中国香港），跨地域调用将失败。
- **安全性**：临时 URL 有效期仅 48 小时，且与模型强绑定；切勿在客户端硬编码或日志中泄露 `oss://` URL 或 API Key。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)


