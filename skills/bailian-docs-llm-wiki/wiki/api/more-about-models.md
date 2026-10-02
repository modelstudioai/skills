# [more](more.md) about models

本文档面向开发者，系统梳理百炼平台模型调用的关键扩展能力，涵盖临时凭证管理、异步任务处理、子空间隔离、文件上传、连接复用等核心机制。所有能力均基于标准 API Key 体系构建，需配合正确的地域、模型权限与网络配置使用。

## 支持的模型/功能

百炼平台支持同步与异步两类模型调用模式：
- **同步模型**（如 `qwen-plus`、`qwen-vl-plus`）：适用于文本生成、多模态理解等毫秒级响应场景，直接返回结果。
- **异步模型**（如图像生成 `wanx2.1-t2i-turbo`、视频生成 `wanx2.1-kf2v-plus`、语音转写 `paraformer-16k-1`）：适用于耗时较长的任务，需通过任务 ID 轮询或事件通知获取结果。详情见 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。

此外，平台支持在**子业务空间**中调用标准模型（如 `qwen-plus`）或专属调优模型，实现权限隔离与费用分账。调用子空间模型时，必须使用该空间生成的 API Key，并按地域配置对应 Base URL（如北京地域为 `https://dashscope.aliyuncs.com/compatible-mode/v1`）。[子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md) 文档详细说明了 OpenAI 兼容与 DashScope 原生两种调用方式。

> **注意**：文档 4 明确指出“调用在阿里云百炼[调优](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)并部署的模型，**无需模型调用授权**”，但文档 2 的异步任务接口描述中未区分标准模型与调优模型的权限逻辑。实际开发中，请以子空间模型调用权限配置为准，调优模型仅限其所属空间 API Key 调用。

## 关键参数

| 参数 | 作用 | 取值范围/说明 | 来源 |
|------|------|----------------|------|
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒，默认 60 秒 | [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `task_id` | 异步任务唯一标识 | UUID 格式字符串，由创建任务接口返回 | [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) |
| `model_name` | 文件上传绑定模型名 | 必须与后续模型调用的 `model` 参数完全一致（如 `qwen-vl-plus`） | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `X-DashScope-OssResourceResolve: enable` | 使用 `oss://` URL 时必需的请求头 | 固定字符串，缺失将导致模型调用失败 | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |

## 使用方式

### 1. 安全调用（不可信环境）
在浏览器或移动 App 等前端环境中，**禁止硬编码永久 API Key**。应通过可信后端服务调用 `/api/v1/tokens` 接口生成临时 API Key，并设置合理 TTL（如 `expire_in_seconds=300`）。临时 Key 继承父 Key 的全部权限，且到期自动失效，无法手动删除。

### 2. 异步任务处理
- **轮询模式**：调用 `GET /api/v1/tasks/{task_id}` 查询状态，建议按任务类型设置间隔（文本向量可 1s，图像生成建议 5–10s），避免触发 20 QPS 限流。
- **事件驱动模式**：配置事件总线（EventBridge）接收 `dashscope:System:AsyncTaskFinish` 事件，支持 HTTP 回调或 RocketMQ 消费。此方式规避轮询限流，适合高并发场景，详见 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。

### 3. 多模态文件输入
调用图像、视频等模型前，需先上传本地文件获取 `oss://` 开头的临时 URL：
- 调用 `GET /api/v1/uploads?action=getPolicy&model={model_name}` 获取上传策略；
- 使用策略参数直传至 OSS；
- 在模型请求中传入该 URL，并**必须添加请求头 `X-DashScope-OssResourceResolve: enable`**。

### 4. 连接优化
- **Java SDK**：通过 `Constants.connectionConfigurations` 配置连接池（如 `connectionPoolSize=256`、`connectTimeout=10`）；
- **Python SDK**：同步调用传入 `requests.Session()`，异步调用传入 `aiohttp.ClientSession(connector=TCPConnector(...))`，复用底层 TCP 连接。

## 限制和注意事项

- **临时文件**：`oss://` URL 有效期严格为 **48 小时**，超时后文件被自动清理；上传限流为 **100 QPS（按主账号+模型维度）**，**严禁用于生产环境或压测**；生产环境请使用阿里云 OSS 自建存储。
- **临时 API Key**：各地域（北京/新加坡/弗吉尼亚/香港）的 API Key **不互通**，生成临时 Key 的 Endpoint 必须与目标地域一致。
- **异步任务生命周期**：任务完成后默认保留 **24 小时**，超时后数据被系统清理，无法再查询。
- **子空间模型权限**：调用标准模型（如 `qwen-plus`）前，必须在子空间控制台显式开启该模型的调用权限；调优模型则无需额外授权，但仅限本空间 API Key 调用。
- **连接复用**：Python 同步调用中若复用 `requests.Session`，需确保其生命周期覆盖所有请求，并在结束时调用 `session.close()`；异步调用中 `aiohttp.ClientSession` 必须用 `async with` 管理，否则连接泄漏。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


