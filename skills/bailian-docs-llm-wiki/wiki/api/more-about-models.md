# [more](more.md) about models

本文档面向开发者，汇总百炼平台模型调用的关键扩展能力，涵盖[异步任务](../concepts/asynchronous-task.md)管理、子业务空间隔离、文件上传与临时资源、连接复用优化及安全凭证机制。所有能力均基于标准模型 API 构建，不改变核心调用语义，但显著提升生产环境的可靠性、可维护性与性能。

## 支持的模型/功能

百炼平台支持多种模型类型（大语言模型、多模态、图像生成、视频生成、语音识别等）的异步调用模式，适用于处理耗时较长的任务。异步能力覆盖 `wanx2.1-t2i-turbo`、`wanx2.1-kf2v-plus`、`paraformer-16k-1` 等主流模型，具体支持列表请参考各模型的 API 文档。  
对于多模态输入（如图像、视频、音频），需先通过 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) 接口上传文件并获得 `oss://` 格式的临时 URL，该 URL 有效期为 48 小时，且**必须与后续调用的模型名称严格一致**。  
子业务空间（Sub Workspace）支持模型调用隔离，适用于权限管控与费用分账场景：标准模型（如 `qwen-plus`）需在子空间中显式授权后方可调用；而用户在百炼平台调优并部署的专属模型，则**仅限其所在子空间的 API Key 调用**，无需额外授权 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。

> **注意**：文档 5 明确指出“文件与模型绑定”，即上传时指定的 `model_name` 必须与后续模型请求中的 `model` 参数完全一致；而文档 4 中关于子空间调用的说明强调“调用在阿里云百炼调优并部署的模型，无需模型调用授权”，但该模型**仅能由其所在业务空间的 API Key 调用**——这与文档 5 的“文件与主账号绑定”要求（文件与模型调用所用 API Key 属于同一主账号）存在隐含耦合，开发者需确保子空间 API Key 与文件上传 API Key 同属一个主账号，否则文件解析将失败。

## 关键参数

- **临时 API Key TTL**：通过 `expire_in_seconds` 参数控制，范围 `[1, 1800]` 秒，默认 60 秒，用于浏览器或移动 App 等不可信环境的安全调用 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。  
- **[异步任务](../concepts/asynchronous-task.md)查询频率**：单账号限流 20 QPS，建议按任务类型设置合理轮询间隔（文本向量可高频，图像/视频生成应低频），避免触发限流。  
- **文件上传限流**：按“主账号 + 模型”维度限流 100 QPS，超出将直接失败，**严禁用于生产压测**。  
- **连接池参数（Java SDK）**：`connectionPoolSize`（默认 32）、`maximumAsyncRequests`（默认 32）等需根据并发量调整；Python SDK 通过 `httpx.Limits` 控制 `max_connections` 与 `max_keepalive_connections`。  
- **HTTP 回调必需 Header**：使用 `oss://` 临时 URL 调用模型时，**必须**在请求头中添加 `X-DashScope-OssResourceResolve: enable`，否则请求将被拒绝。

## 使用方式

- **[异步任务](../concepts/asynchronous-task.md)管理**：统一通过 `/api/v1/tasks/{task_id}`（单查）、`/api/v1/tasks`（批量查）、`/api/v1/tasks/{task_id}/cancel`（取消）三个接口操作，支持 Python SDK（`client.images.jobs.fetch/list/cancel`）、curl 及 CLI（当前仅 `video-synthesis` 子命令完整支持）。  
- **接收完成通知**：推荐配置事件总线（EventBridge）接收 `dashscope:System:AsyncTaskFinish` 事件，通过 HTTP 回调 URL 或 RocketMQ 消费，避免轮询限流与资源浪费 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。  
- **子空间模型调用**：  
  - DashScope 方式：构造 Client 时传入 `workspace` 和 `region`（如 `ap-southeast-1`），调用时使用子空间 API Key；  
  - OpenAI 兼容方式：北京地域使用通用域名 `https://dashscope.aliyuncs.com/compatible-mode/v1`，新加坡地域需替换为工作空间专属域名 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`。  
- **连接复用**：  
  - Java SDK：通过 `Constants.connectionConfigurations` 全局配置连接池；  
  - Python SDK：传入自定义 `httpx.Client` 或 `httpx.AsyncClient` 实例，推荐使用 `with` 语句管理生命周期 [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)。

## 限制和注意事项

- **临时资源时效性**：临时 API Key 过期后自动失效，无法手动删除；临时文件 URL 48 小时后自动清理，**均不可用于生产环境长期服务**，生产环境应使用 OSS 等持久化存储。  
- **地域与 API Key 绑定**：北京、新加坡、弗吉尼亚、中国香港等地域的 API Key **完全独立且不互通**，调用前必须确认地域匹配，否则返回 `InvalidApiKey` 错误 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。  
- **异步任务数据保留**：任务完成后通常保留 24 小时（以具体模型文档为准），超时后无法查询，需及时获取结果。  
- **文件使用约束**：上传文件不可查询、修改或下载，仅能作为 URL 参数在模型调用中使用；且 `oss://` URL 必须配合 `X-DashScope-OssResourceResolve: enable` Header 才能被正确解析。  
- **SDK 兼容性**：DashScope Python SDK 版本需 ≥ `2.0.1` 才支持 `client.files.upload`；Java SDK 建议 ≥ `2.12.0` 以获得完整连接池配置能力。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


