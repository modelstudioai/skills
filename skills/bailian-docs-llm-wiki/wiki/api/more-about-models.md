# [more](more.md) about models

本文档面向开发者，系统介绍百炼平台模型调用的核心机制与高级能力，涵盖模型访问控制、[异步任务](../concepts/asynchronous-task.md)管理、文件上传、连接优化及多业务空间支持等关键场景。所有功能均基于 DashScope API 与 SDK 实现，适用于生产环境集成。

## 支持的模型/功能

百炼平台支持多种模型调用模式：同步调用（如文本生成）、异步调用（如文生图、文生视频）及[多模态](../concepts/multimodal.md)推理（需上传文件）。异步模型包括 `wanx2.1-t2i-turbo`、`wanx2.1-kf2v-plus` 等图像/视频生成模型；[多模态](../concepts/multimodal.md)模型（如 `qwen-vl-plus`）需配合临时文件 URL 使用。标准大语言模型（如 `qwen-plus`）既支持同步也支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用。  
> **注意**：文档中提及的 `paraformer-8k-v1` 和 `paraformer-16k-1` 均为语音识别模型，但其在[通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)中的事件结构示例与[异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)中 `user_api_unique_key` 字段格式一致，表明模型标识体系已统一；而 `qwen-vl-plus` 在[上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)中作为必需的 `model_name` 参数，验证了文件与模型强绑定的设计原则。

## 关键参数

- **临时 API Key**：通过 `POST /api/v1/tokens?expire_in_seconds=1800` 生成，TTL 范围为 `[1, 1800]` 秒，继承源 API Key 的全部权限（含模型/知识库访问限制）[生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。  
- **文件上传参数**：`model_name` 必须与后续模型调用一致；`X-DashScope-OssResourceResolve: enable` 请求头为 OSS URL 调用必需项。  
- **连接复用参数**：Java SDK 可配置 `connectionPoolSize`（默认 32）、`maximumAsyncRequests`（默认 32）等；Python SDK 通过 `aiohttp.TCPConnector` 或 `requests.Session` 控制 `limit` 与 `limit_per_host` [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)。  
- **子业务空间参数**：调用非默认空间模型时，必须使用该空间专属 API Key，并按地域配置 `base_url`（如北京：`https://dashscope.aliyuncs.com/compatible-mode/v1`；新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`）[子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。

## 使用方式

- **[异步任务](../concepts/asynchronous-task.md)**：先调用模型创建接口获取 `task_id`，再通过 `/api/v1/tasks/{task_id}` 查询结果（20 QPS 限流），或配置事件总线接收 `dashscope:System:AsyncTaskFinish` 事件实现免轮询 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。  
- **文件上传**：调用 `GET /api/v1/uploads?action=getPolicy&model={model_name}` 获取上传凭证，再 POST 至 OSS Host 完成上传，返回 `oss://` 格式 URL（48 小时有效期）[上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。  
- **连接优化**：Java SDK 直接配置 `Constants.connectionConfigurations`；Python SDK 在 `call()` 时传入自定义 `session`（同步）或 `aiohttp.ClientSession`（异步）[DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)。  
- **子空间调用**：OpenAI 兼容方式需设置 `base_url` 并使用子空间 API Key；DashScope 原生方式需显式配置 `base_http_api_url`（新加坡等地域需填入 `{WorkspaceId}`）[子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。

## 限制和注意事项

- **临时 API Key**：不可手动删除，到期自动失效；不同地域 API Key 不互通，调用时需匹配对应 Endpoint。  
- **[异步任务](../concepts/asynchronous-task.md)查询**：单任务查询接口限流 20 QPS；任务数据保留约 24 小时，超时后无法查询；仅 `PENDING` 状态任务可取消 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。  
- **临时文件**：单文件 ≤ 1 GB；与主账号及指定模型强绑定；48 小时有效期，**严禁用于生产环境**；上传凭证接口限流 100 QPS 且不可扩容 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。  
- **连接复用**：Java SDK `maximumAsyncRequestsPerHost` 需 ≤ `maximumAsyncRequests`；Python 同步调用推荐 `with requests.Session()` 确保资源释放。  
- **子业务空间**：调用标准模型前需在控制台授权；调优部署的模型仅限本空间 API Key 调用，不支持 OpenAI 兼容方式 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)


