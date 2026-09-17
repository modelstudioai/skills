# [more](more.md) about models

阿里云百炼平台支持多种模型调用方式与高级功能，涵盖[异步任务](../concepts/asynchronous-task.md)管理、子业务空间隔离、文件上传、连接复用及临时密钥生成等核心能力。本文档面向开发者，系统梳理关键能力、参数、使用方法及限制，帮助您高效、安全地集成模型服务。

## 支持的模型/功能

百炼平台支持文本、[多模态](../concepts/multi-modal.md)、图像、视频、语音等全类型模型，其中**图像生成、视频生成、语音转写等长耗时模型默认采用异步调用机制**，需通过任务ID轮询或事件通知获取结果 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。  
对于[多模态](../concepts/multi-modal.md)模型（如 `qwen-vl-plus`），输入文件需先上传至百炼提供的临时OSS存储并获取 `oss://` 格式URL，该URL与模型强绑定且有效期仅48小时 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。  
此外，平台支持**子业务空间（Workspace）隔离调用**，可用于模型权限管控与费用分账，调用时必须使用对应空间的API Key，并按地域配置专属Base URL [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。

> **注意**：文档3中“DashScope方式调用子业务空间模型”示例代码在Java部分被截断（`System.out.println(JsonU`），实际应为`JsonUtils.toJsonString(result)`，请以[最新SDK文档](https://help.aliyun.com/zh/model-studio/install-sdk)为准。

## 关键参数

- **[异步任务](../concepts/asynchronous-task.md)查询限流**：所有任务管理接口（`fetch`/`list`/`cancel`）统一限流为 **20 QPS**（每秒每个主账号），超限将返回 `Throttling.RateQuota` 错误码。  
- **临时文件上传限流**：`/api/v1/uploads?action=getPolicy` 接口按“主账号+模型”维度限流 **100 QPS**，不可扩容，生产环境严禁使用 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。  
- **连接复用配置**：Java SDK默认启用连接池，关键参数包括 `connectionPoolSize`（默认32）、`maximumAsyncRequests`（默认32）；Python SDK需显式传入 `requests.Session` 或 `aiohttp.ClientSession` 实现复用 [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)。  
- **临时API Key有效期**：默认60秒，可通过 `expire_in_seconds` 参数设置TTL，范围为 **1–1800秒**，过期后自动失效且不可手动删除 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。

## 使用方式

- **[异步任务](../concepts/asynchronous-task.md)结果获取**：推荐优先使用**事件总线（EventBridge）回调**替代轮询，通过配置HTTP URL或RocketMQ接收 `dashscope:System:AsyncTaskFinish` 事件，实时获知任务状态，避免触发20 QPS限流 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。  
- **子业务空间调用**：OpenAI兼容模式需设置 `base_url` 为 `https://dashscope.aliyuncs.com/compatible-mode/v1`（北京）或 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`（新加坡）；DashScope原生SDK则需配置 `base_http_api_url` 或使用协议参数指定地域Endpoint。  
- **临时文件调用**：上传后获得的 `oss://` URL 必须在模型请求Header中显式添加 `X-DashScope-OssResourceResolve: enable`，否则调用失败。  
- **连接优化**：高并发场景下，Java SDK建议将 `connectionPoolSize` 和 `maximumAsyncRequests` 调整至256；Python同步调用推荐 `with requests.Session() as session:` 管理生命周期，异步调用需配置 `aiohttp.TCPConnector(limit=100, limit_per_host=30)`。

## 限制和注意事项

- **临时文件不可用于生产**：`oss://` URL有效期仅48小时，且上传接口限流严格，**生产环境必须使用阿里云OSS等自有稳定存储** [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。  
- **异步任务取消限制**：仅状态为 `PENDING` 的任务可取消，`RUNNING` 或已完成任务调用 `/cancel` 将返回 `UnsupportedOperation` 错误 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。  
- **子空间模型授权差异**：调用标准模型（如 `qwen-plus`）需在子空间中单独授权；但调优部署的模型**无需额外授权**，仅限其所在空间的API Key调用 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。  
- **临时API Key权限继承**：生成的临时Key完全继承父Key的全部权限（含模型/知识库访问策略），不支持细粒度权限降级。

## 来源文档

- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)


