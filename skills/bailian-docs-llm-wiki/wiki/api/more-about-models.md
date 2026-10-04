# [more](more.md) about models

本文档面向开发者，汇总百炼平台模型调用的核心扩展能力，涵盖安全凭证管理、异步任务处理、文件上传、子空间隔离及连接优化等关键实践。所有功能均基于 DashScope API 与 SDK 实现，需配合有效的 API Key 使用。

## 支持的模型/功能

百炼平台支持同步与异步两类模型调用模式：
- **同步模型**：适用于文本生成（如 `qwen-plus`）、[向量嵌入](../concepts/embedding.md)等低延迟场景，直接返回结果。
- **异步模型**：适用于图像生成（如 `wanx2.1-t2i-turbo`）、视频生成（如 `wanx2.1-kf2v-plus`）、语音转写（如 `paraformer-8k-v1`）等长耗时任务，需通过任务 ID 轮询或事件通知获取结果。  
  异步任务统一由 [异步任务管理 API](raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) 提供查询、批量状态获取和取消能力，且支持通过事件总线接收完成通知，避免轮询资源浪费 —— 详见 [通过HTTP回调URL或MQ接收异步任务完成通知](raw/model-api-reference/more-about-models/async-task-api.md)。

多模态模型（如 `qwen-vl-plus`）需传入文件 URL，平台提供免费临时存储服务，支持上传本地图片、音频、视频并获取 `oss://` 格式临时 URL（有效期 48 小时），该 URL 与指定模型强绑定，调用时必须携带请求头 `X-DashScope-OssResourceResolve: enable` —— 具体流程见 [上传本地文件获取临时URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

> **注意**：文档 4 明确要求临时 URL 必须在 HTTP 请求头中显式添加 `X-DashScope-OssResourceResolve: enable`；而文档 5 中子业务空间调用示例未体现该头，实际调用多模态模型时仍需补全，否则将报错。

## 关键参数

| 参数 | 说明 | 示例值 | 来源 |
|------|------|--------|------|
| `task_id` | 异步任务唯一标识，用于查询、取消操作 | `a8532587-xxxx-xxxx-xxxx-0c46b17950d1` | [异步任务管理 API](raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) |
| `expire_in_seconds` | 临时 API Key 有效期，范围 `[1, 1800]` 秒 | `1800` | [生成临时API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `model_name` | 文件上传时必需指定，决定临时 URL 的模型上下文与权限校验 | `qwen-vl-plus` | [上传本地文件获取临时URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `base_url` | 子业务空间调用必需，区分地域与协议（如 `compatible-mode/v1` 或 `maas.aliyuncs.com/api/v1`） | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1` | [子业务空间的模型调用](raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md) |

## 使用方式

### 安全凭证
- **生产环境推荐使用永久 API Key**，通过环境变量 `DASHSCOPE_API_KEY` 配置。  
- **不可信客户端（如浏览器、App）必须使用临时 API Key**：后端调用 `/api/v1/tokens?expire_in_seconds=1800` 接口生成，继承源 Key 权限，不可手动删除，过期自动失效 —— 参考 [生成临时API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。

### 异步任务处理
- **轮询方案**：调用 `/api/v1/tasks/{task_id}` 查询单任务（20 QPS 限流），或 `/api/v1/tasks` 批量查询（支持按 `start_time`/`end_time`/`status`/`model_name` 过滤）。  
- **事件驱动方案（推荐）**：配置事件总线规则，监听 `dashscope:System:AsyncTaskFinish` 事件，通过 HTTP 回调或 RocketMQ 消费，实时获知任务完成状态 —— 详见 [通过HTTP回调URL或MQ接收异步任务完成通知](raw/model-api-reference/more-about-models/async-task-api.md)。

### 连接优化
- **Java SDK**：通过 `Constants.connectionConfigurations` 配置连接池参数（如 `connectionPoolSize=256`, `connectTimeout=10`），默认启用复用。  
- **Python SDK**：同步调用传入 `requests.Session()`，异步调用传入 `aiohttp.ClientSession(connector=TCPConnector(...))` —— 具体配置见 [DashScope SDK连接复用配置](raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)。

## 限制和注意事项

- **临时文件**：单文件 ≤ 1 GB；仅限同一主账号下使用；48 小时后自动清理；**严禁用于生产环境或高并发压测**（上传接口限流 100 QPS，不支持扩容），生产环境请使用 OSS。  
- **临时 API Key**：有效期最长 1800 秒（30 分钟）；各地域 Endpoint 不同（北京/新加坡/弗吉尼亚/中国香港），需匹配对应地域的 API Key 和 URL。  
- **子业务空间**：调用标准模型（如 `qwen-plus`）前，必须在控制台为该空间[设置模型调用权限](https://help.aliyun.com/zh/model-studio/permission-management-overview#f642213a1f38l)；调优部署的模型仅限本空间 API Key 调用，且不支持 OpenAI 兼容方式。  
- **异步任务取消**：仅支持取消 `PENDING` 状态任务，`RUNNING` 或已完成任务无法取消；任务数据保留约 24 小时，超时后无法查询。  
- **地域一致性**：API Key、WorkspaceId、Endpoint 地域三者必须严格一致（如新加坡地域 Key 不能用于北京 Endpoint），否则返回 `InvalidApiKey` 错误。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


