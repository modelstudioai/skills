# [more](more.md) about models

本文档面向开发者，系统梳理百炼平台中与模型调用相关的进阶能力，涵盖模型访问控制、异步任务管理、文件上传、连接优化等核心场景。所有能力均基于 DashScope API 体系设计，适用于生产环境集成，但需注意各功能的适用范围与约束条件。

## 支持的模型/功能

百炼平台支持多种模型调用模式，包括同步推理（如文本生成）、[异步处理](../concepts/asynchronous-processing.md)（如文生图、文生视频）及多模态输入（如图像、音频、视频）。异步任务需通过独立接口管理生命周期，详见[异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)；多模态模型（如 `qwen-vl-plus`）要求输入文件必须通过临时存储服务获取 URL，不可直接上传二进制流；标准大语言模型（如 `qwen-plus`）既支持 DashScope 原生协议，也兼容 OpenAI 接口规范，但子业务空间调用时需严格匹配对应地域的 endpoint 和 API Key [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。

> **注意**：文档 5 中提到的 `Files.upload(purpose='inference')` 方法在 SDK 中实际不接受 `model` 参数，而上传凭证接口（`/api/v1/uploads?action=getPolicy`）强制要求传入 `model`。二者语义不一致，生产中应以凭证接口的 `model` 参数为准，确保上传文件与后续模型调用严格绑定。

## 关键参数

- **临时 API Key**：通过 `/api/v1/tokens` 接口生成，`expire_in_seconds` 范围为 `[1, 1800]` 秒，超时后自动失效且不可手动删除，详见[生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。
- **异步任务状态字段**：`task_status` 取值包括 `PENDING`、`RUNNING`、`SUCCEEDED`、`FAILED`、`CANCELED`、`UNKNOWN`；`contain_result` 控制事件体是否内嵌完整结果；`user_api_unique_key` 是模型调用五要素组成的唯一标识，可用于事件过滤。
- **文件上传参数**：`model_name` 必须与后续模型调用一致；临时 URL 有效期固定为 48 小时；HTTP 调用时必须显式添加请求头 `X-DashScope-OssResourceResolve: enable`。
- **连接复用参数**：Java SDK 默认启用连接池，关键可调参数包括 `connectionPoolSize`（默认 32）、`maximumAsyncRequests`（默认 32）；Python SDK 需显式传入 `requests.Session` 或 `aiohttp.ClientSession` 实例。

## 使用方式

- **安全调用**：在浏览器或移动端等不可信环境，应通过可信后端生成临时 API Key，避免永久密钥泄露。
- **异步任务通知**：推荐使用事件总线（EventBridge）配置 HTTP 回调或 RocketMQ 目标，替代轮询。回调事件类型为 `dashscope:System:AsyncTaskFinish`，其 `data.task_id` 和 `data.task_status` 是消费逻辑的核心字段，详见[通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。
- **文件上传**：优先使用 DashScope SDK 的 `Files.upload(purpose='inference')`（Python）或手动调用 `/api/v1/uploads?action=getPolicy` 获取 OSS 签名后直传；上传后获得 `oss://` 格式 URL，调用模型时需在 Header 中启用资源解析。
- **连接优化**：高并发场景下，Java 应调整 `ConnectionConfigurations`；Python 同步调用推荐 `with requests.Session()` 管理，异步调用推荐 `aiohttp.TCPConnector(limit=100)` 配置。

## 限制和注意事项

- **临时文件**：单文件上限 1 GB；上传限流为 100 QPS（按主账号+模型维度）；文件仅限同一主账号下使用，且 48 小时后自动清理；**严禁用于生产环境或压测**，生产应使用 OSS 自建存储。
- **异步任务查询**：`/api/v1/tasks/{task_id}` 和 `/api/v1/tasks` 接口均限流 20 QPS；任务数据保留期通常为 24 小时（以具体模型文档为准）；仅支持取消 `PENDING` 状态任务。
- **子业务空间**：调用标准模型前需在控制台显式授权该空间对目标模型的访问权限；调优部署的模型仅能被其所在空间的 API Key 调用，且不支持 OpenAI 兼容方式。
- **连接复用**：Python 同步调用若复用 `requests.Session`，需确保其生命周期覆盖全部请求；异步调用中 `aiohttp.ClientSession` 必须配合 `async with` 使用，否则连接可能泄漏。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


