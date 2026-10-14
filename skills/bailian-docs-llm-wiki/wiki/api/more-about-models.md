# [more](more.md) about models

阿里云百炼平台支持多种模型调用模式，包括同步与异步执行、子业务空间隔离、临时凭证安全访问等。本文档面向开发者，系统梳理模型调用的核心能力、关键参数配置、使用方式及常见限制，帮助您高效、稳定地集成模型服务。

## 支持的模型/功能

百炼平台支持文本生成、多模态理解（VL）、语音识别（ASR）、图像生成（T2I）、视频生成（T2V）等多类模型。其中，**图像生成、视频生成、长音频转写等耗时较长的任务均采用[异步调用](../concepts/asynchronous-invocation.md)机制**，需通过任务 ID 查询结果或取消任务 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。异步任务还支持通过事件总线（EventBridge）主动推送完成通知，避免轮询带来的资源浪费和限流风险 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。

此外，平台支持在**子业务空间（Sub Workspace）中独立调用模型**，适用于权限隔离与费用分账场景；也支持为不可信前端环境生成**临时 API Key**，提升调用安全性 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。

> **注意**：文档 5 中提到 `Files.upload` 方法的 `purpose` 参数取值为 `fine_tune` 或 `inference`，但明确说明“**无 `model` 参数**”；而文档 5 的其他部分（如 Python 示例函数 `upload_file_and_get_url`）及文档 1、2 均强调文件上传必须指定 `model_name` 且与后续调用模型严格一致。该矛盾表明 SDK 封装层（`Files.upload`）已解耦模型绑定逻辑，但底层存储策略仍依赖模型上下文——实际使用中，**必须确保上传用途（`purpose=inference`）与目标模型语义一致，否则可能导致调用失败**。

## 关键参数

- **异步任务查询频率**：单账号（含子账号）限流 20 QPS，建议按任务类型设置合理轮询间隔（如 T2I 建议 ≥5s，T2V 建议 ≥30s）。
- **临时文件 URL**：有效期固定为 48 小时，上传限流为 100 QPS（按“主账号+模型”维度），且必须在请求头中显式添加 `X-DashScope-OssResourceResolve: enable` 才能解析 `oss://` URL。
- **临时 API Key TTL**：有效期范围为 1–1800 秒（默认 60 秒），不可手动撤销，到期自动失效。
- **连接复用配置**：
  - Java SDK：默认启用连接池，关键参数包括 `connectionPoolSize`（默认 32）、`maximumAsyncRequests`（默认 32）及各类超时时间（`connectTimeout` 默认 120s）。
  - Python SDK：需显式传入 `requests.Session`（同步）或 `aiohttp.ClientSession`（异步），推荐使用 `with` 语句管理生命周期。

## 使用方式

### 异步任务管理
- **创建任务**：调用对应模型的 `create` 接口（如 `ImageSynthesis.async_invoke`），获取 `task_id`。
- **查询结果**：使用 `fetch(task_id)`（Python SDK）或 `GET /api/v1/tasks/{task_id}`（HTTP）。
- **批量查询**：使用 `list()` 或 `GET /api/v1/tasks`，支持按 `start_time`/`end_time`/`status`/`model_name` 等条件筛选。
- **取消任务**：仅支持状态为 `PENDING` 的任务，调用 `cancel(task_id)` 或 `POST /api/v1/tasks/{task_id}/cancel`。

### 子业务空间调用
- 必须使用该子空间专属的 API Key；
- OpenAI 兼容方式需配置 `base_url`（北京地域为 `https://dashscope.aliyuncs.com/compatible-mode/v1`）；
- DashScope 原生方式在北京地域无需额外配置 `base_url`，但在新加坡等地域需显式设置 `base_http_api_url`。

### 文件与凭证
- 上传本地文件前，先调用 `GET /api/v1/uploads?action=getPolicy&model={model_name}` 获取上传策略；
- 临时 API Key 通过 `POST /api/v1/tokens?expire_in_seconds=1800` 生成，需用永久 API Key 鉴权。

### 连接优化
- Java：通过 `Constants.connectionConfigurations` 全局配置连接池参数；
- Python：同步调用传入 `requests.Session()`，[异步调用](../concepts/asynchronous-invocation.md)传入 `aiohttp.ClientSession()`，并配置 `TCPConnector` 参数。

## 限制和注意事项

- **异步任务保留期**：任务完成后通常保留 24 小时（具体以各模型文档为准），超时后无法查询 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。
- **临时文件限制**：文件大小 ≤1GB；仅限同一主账号下使用；不支持生产环境长期存储，**高并发或压测场景严禁使用**，应改用 OSS [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。
- **子空间模型权限**：调用标准模型（如 `qwen-plus`）需提前在子空间中授权；调优部署的模型则无需额外授权，但仅限本空间 API Key 调用。
- **SDK 兼容性**：`dashscope CLI` 当前仅 `video-synthesis` 子命令完整支持 `fetch`/`list`/`cancel`，其他模型任务管理需依赖 Python SDK 或 HTTP 直连 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。

## 来源文档

- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


