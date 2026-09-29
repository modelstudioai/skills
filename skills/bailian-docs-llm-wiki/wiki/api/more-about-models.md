# [more](more.md) about models

本文档面向开发者，系统梳理百炼平台模型调用的关键技术要点，涵盖异步任务管理、临时凭证、文件上传、子空间隔离及连接优化等核心能力。所有功能均基于统一的 API Key 体系和地域化 Endpoint 架构，适用于生产环境高并发、多租户、多模态等典型场景。

## 支持的模型/功能

百炼平台支持同步与异步两类模型调用模式，具体取决于模型类型和任务耗时：

- **同步模型**：如 `qwen-plus`、`qwen-vl-plus` 等文本/多模态生成模型，直接返回结果，适用于低延迟交互场景。
- **异步模型**：如图像生成（`wanx2.1-t2i-turbo`）、视频生成（`wanx2.1-kf2v-plus`）、语音转写（`paraformer-16k-1`）等长耗时任务，需通过任务 ID 轮询或事件通知获取结果。详细支持列表见 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。
- **子业务空间模型**：支持在非默认工作空间中调用标准模型（如 `qwen-plus`）或专属调优模型，实现权限隔离与费用分账，详见 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。

> **注意**：文档 4 中明确指出“调用在阿里云百炼[调优](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)并部署的模型，**无需模型调用授权**”，但文档 5 的“文件与模型绑定”限制强调“文件上传时必须指定模型名称，且该模型须与后续调用的**模型一致**”。二者逻辑一致——调优模型仅限其所在空间调用，且输入文件必须严格匹配该模型，不存在跨模型复用文件的可能。

## 关键参数

| 参数 | 说明 | 典型值/范围 | 来源 |
|------|------|-------------|------|
| `task_id` | 异步任务唯一标识，用于查询、取消任务 | UUID 格式字符串 | [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) |
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒（默认 60 秒） | [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `model_name` | 文件上传时必需的模型标识，决定存储策略与访问权限 | 如 `qwen-vl-plus`, `wanx2.1-t2i-turbo` | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `connectionPoolSize` | Java SDK 连接池最大连接数 | 默认 32，建议按并发量调整至 64–256 | [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |

## 使用方式

### 异步任务管理
对图像、视频、语音等长耗时任务，推荐两种结果获取方式：
- **轮询模式**：调用 `/api/v1/tasks/{task_id}` 查询单任务，或 `/api/v1/tasks` 批量查询。注意遵守 20 QPS 限流，避免高频请求触发限流。
- **事件驱动模式**：通过 [事件总线 EventBridge](https://help.aliyun.com/zh/eventbridge/product-overview/what-is-eventbridge) 配置 HTTP 回调或 RocketMQ 目标，接收 `dashscope:System:AsyncTaskFinish` 事件后按需拉取结果，规避轮询资源消耗与限流风险。详见 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。

### 临时凭证与文件上传
- 生成临时 API Key 用于前端/移动端等不可信环境，调用 `POST https://dashscope.aliyuncs.com/api/v1/tokens`，凭永久 Key 签发，有效期可设（最长 30 分钟）。
- 多模态模型输入文件需先上传获取 `oss://` 前缀临时 URL（有效期 48 小时），上传时必须指定 `model_name`，且调用模型时需在 Header 中添加 `X-DashScope-OssResourceResolve: enable`。

### 子空间调用
调用子业务空间模型时：
- 必须使用该空间创建的 API Key；
- OpenAI 兼容方式需设置 `base_url` 为 `https://dashscope.aliyuncs.com/compatible-mode/v1`（北京）或 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`（新加坡）；
- DashScope 原生方式需显式配置 `base_http_api_url` 或 SDK 初始化参数指向对应地域工作空间 Endpoint。

### 连接复用优化
- **Java SDK**：通过 `Constants.connectionConfigurations` 配置连接池参数（如 `connectionPoolSize`, `readTimeout`），默认启用。
- **Python SDK**：同步调用传入 `requests.Session`，异步调用传入 `aiohttp.ClientSession`，显式控制连接生命周期与并发上限。

## 限制和注意事项

- **异步任务保留期**：任务结果默认保留 24 小时（以对应任务 API 文档为准），超时后自动清理，查询前请确认时效性。
- **临时文件限制**：上传限流为 100 QPS（按主账号+模型维度），文件大小 ≤ 1 GB，有效期 48 小时；**严禁用于生产环境或压测场景**，生产环境应使用 OSS 等持久化存储。
- **临时 API Key 安全性**：继承签发 Key 的全部权限，且无法手动删除，仅靠 TTL 自动失效，务必严格管控签发方权限。
- **子空间模型权限**：调用标准模型需单独授权，而调优模型仅限本空间调用且无需额外授权，权限模型存在差异。
- **SDK 版本兼容性**：Python SDK 文件上传需 ≥ `1.27.3`，Java SDK 连接配置需 ≥ `2.12.0`，旧版本不支持关键特性。

## 来源文档

- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


