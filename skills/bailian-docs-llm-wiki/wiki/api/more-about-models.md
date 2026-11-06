# [more](more.md) about models

阿里云百炼平台提供多种模型调用机制与配套能力，涵盖同步/[异步任务](../concepts/asynchronous-task.md)管理、安全凭证控制、多业务空间隔离、连接性能优化及文件资源处理等核心场景。本文面向开发者，系统梳理关键能力、参数约束、使用方式及实践限制，帮助构建稳定高效的模型服务集成方案。

## 支持的模型/功能

百炼支持文本生成（如 `qwen-plus`）、多模态理解（如 `qwen3-vl-plus`）、图像生成（如 `wanx2.1-t2i-turbo`）、视频生成、语音识别（如 `paraformer-8k-v2`）等多类模型。其中，**图像生成、视频生成、语音转写等长耗时任务统一采用异步调用模式**，需通过任务 ID 查询结果或配置事件通知；而文本生成等低延迟任务默认支持同步调用。  
对于多模态模型（如 VL 模型），输入文件需先上传至百炼临时存储并获取 `oss://` 格式 URL，且该 URL 必须与后续调用的模型名称严格一致——[上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) 明确要求“文件与模型绑定”。  
此外，平台支持子业务空间（Sub-workspace）隔离调用，适用于权限管控与费用分账场景：子空间中部署的调优模型仅能由该空间 API Key 调用；而标准模型（如 `qwen-plus`）则需额外配置模型调用权限——详见 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。

> **注意**：文档 4 中称“调用在阿里云百炼[调优](https://help.aliyun.com/zh/model-studio/model-training-overview)并部署的模型，**无需模型调用授权**”，但文档 4 同一节又明确指出“使用子业务空间的API Key调用[标准模型]（例如`qwen-plus`）前，需为该空间[设置模型调用权限](https://help.aliyun.com/zh/model-studio/permission-management-overview#f642213a1f38l)”。此处逻辑无矛盾：调优模型自动继承空间权限，标准模型需显式授权。但需注意，文档 4 的 OpenAI 兼容调用示例中，北京地域使用通用域名 `dashscope.aliyuncs.com`，而新加坡地域使用工作空间专属域名 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`，**实际调用必须确保 API Key 地域与 endpoint 地域一致**，否则将因认证失败报错。

## 关键参数

- **[异步任务](../concepts/asynchronous-task.md)状态查询频率**：所有[异步任务](../concepts/asynchronous-task.md)接口（`/api/v1/tasks/{task_id}`、`/api/v1/tasks`、`/api/v1/tasks/{task_id}/cancel`）均受 **20 QPS 限流**约束（按主账号维度），建议根据任务类型设置合理轮询间隔（如图像生成建议 ≥5s），避免触发限流——参见 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。  
- **临时 API Key 有效期（TTL）**：通过 `/api/v1/tokens` 接口生成，默认 60 秒，可设为 `[1, 1800]` 秒内任意值，超时后自动失效且不可手动删除——见 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。  
- **文件上传凭证限流**：`/api/v1/uploads?action=getPolicy` 接口按“主账号+模型”维度限流 **100 QPS**，超出即失败；且临时文件 URL 有效期固定为 **48 小时**，过期后无法使用——该限制在 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) 中被多次强调。  
- **HTTP 客户端连接复用参数**：Java SDK 默认启用连接池，关键可调参数包括 `connectionPoolSize`（默认 32）、`maximumAsyncRequests`（默认 32）；Python SDK 需传入 `httpx.Client` 或 `httpx.AsyncClient` 并配置 `limits`，如 `max_connections=100`——详见 [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)。

## 使用方式

- **异步任务管理**：推荐优先采用 **事件总线（EventBridge）回调机制**替代轮询，以规避限流、降低资源消耗并提升实时性。支持 HTTP 回调 URL 或 RocketMQ 两种事件目标，事件类型为 `dashscope:System:AsyncTaskFinish`，事件体中包含 `task_id` 和 `task_status` 等关键字段——[通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md) 提供了完整配置流程。  
- **子业务空间调用**：必须使用该空间专属 API Key，并根据模型类型选择调用方式：  
  - 标准模型（如 `qwen-plus`）：支持 DashScope SDK（需指定 `workspace` 和 `region`）或 OpenAI 兼容模式（需配置 `base_url` 为对应地域 endpoint）；  
  - 调优模型：**仅支持 DashScope SDK 调用**，不支持 OpenAI 兼容模式。  
- **文件上传与引用**：调用多模态模型前，需先调用 `/api/v1/uploads?action=getPolicy` 获取上传策略，再将文件 POST 至 OSS Host，最终获得 `oss://` URL；模型请求时需在 Header 中添加 `X-DashScope-OssResourceResolve: enable`，且 URL 中的模型标识必须与上传时指定的 `model` 参数一致。  
- **连接性能优化**：高并发场景下，Java SDK 应调整 `ConnectionConfigurations`；Python SDK 应复用 `httpx.Client` 实例或 `httpx.AsyncClient`，避免每次请求重建连接。

## 限制和注意事项

- **临时文件功能非生产就绪**：`oss://` 临时 URL 有效期仅 48 小时，且上传接口限流 100 QPS 不可扩容，[上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) 明确警示“**请勿用于生产环境、高并发及压测场景**”，生产环境应使用阿里云 OSS 等长期可靠存储。  
- **异步任务数据保留策略**：任务完成后数据默认保留 **24 小时**（具体以各任务文档为准），超时后系统自动清理，`fetch` 或 `list` 接口将无法查到历史任务——此策略在 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) 中有明确说明。  
- **取消任务的严格限制**：`/api/v1/tasks/{task_id}/cancel` 接口**仅支持取消状态为 `PENDING` 的任务**（排队中未开始处理），对 `RUNNING` 或已完成状态的任务调用将直接返回 `UnsupportedOperation` 错误。  
- **地域与 API Key 强绑定**：北京、新加坡、弗吉尼亚、中国香港等地域的 API Key **完全独立且不可混用**，调用时 endpoint 必须与 API Key 所属地域匹配，否则认证失败。文档 2 和文档 4 均强调此点，但文档 6 的 Python SDK 示例中 `client.files.upload` 方法签名缺少 `model` 参数，与文档 6 前文“文件与模型绑定”要求存在潜在冲突——实际使用时需确保上传与调用模型严格一致，SDK 封装可能隐式处理，但逻辑约束不变。

## 来源文档

- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)


