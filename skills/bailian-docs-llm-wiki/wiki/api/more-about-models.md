# [more](more.md) about models

本文档面向开发者，系统梳理百炼平台模型调用的关键扩展能力，涵盖[异步任务](../concepts/asynchronous-task.md)管理、子业务空间隔离、临时资源获取、连接优化及安全凭证机制。内容聚焦实际集成场景中的高频需求，如长耗时任务处理、多租户权限管控、多模态文件接入和高并发性能调优，不包含营销性描述。

## 支持的模型/功能

百炼平台支持同步与异步两类模型调用模式：
- **同步模型**：适用于文本生成（如 `qwen-plus`）、嵌入向量等低延迟任务，直接返回结果。
- **异步模型**：适用于图像生成（`wanx2.1-t2i-turbo`）、视频合成（`wanx2.1-kf2v-plus`）、语音转写（`paraformer-16k-1`）等长耗时任务，需通过任务 ID 轮询或事件通知获取结果 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。

所有模型均支持在**子业务空间**中独立调用，实现模型权限隔离与费用分账。标准模型（如 `qwen-plus`）需显式授权，而用户在百炼平台调优并部署的模型仅限其所在子空间调用 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。

多模态模型（如 `qwen3-vl-plus`）依赖外部文件输入，平台提供免费临时存储服务，上传后生成 `oss://` 格式 URL，有效期 48 小时 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

> **注意**：文档 5 明确指出“临时 URL 请勿用于生产环境”，而文档 4 中子空间调用示例未提及该限制，实际生产部署必须使用 OSS 等持久化存储，避免因 URL 过期导致服务中断。

## 关键参数

| 参数 | 说明 | 取值范围/示例 | 来源 |
|------|------|----------------|------|
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒，默认 60 秒 | [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `task_id` | [异步任务](../concepts/asynchronous-task.md)唯一标识符 | UUID 格式字符串，如 `a8532587-xxxx-xxxx-xxxx-0c46b17950d1` | [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) |
| `model_name` | 文件上传时绑定的模型名 | 必须与后续模型调用一致，如 `qwen3-vl-plus` | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `connectionPoolSize` | Java SDK 连接池最大连接数 | 默认 32，高并发建议调至 256 | [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |

## 使用方式

### 1. 安全凭证
在不可信环境（如浏览器、App）中调用模型时，**禁止硬编码永久 API Key**。应由可信后端调用 `/api/v1/tokens` 接口生成临时 Key，并设置合理 TTL（如 `expire_in_seconds=1800`），其权限继承自生成所用的永久 Key [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。

### 2. [异步任务](../concepts/asynchronous-task.md)处理
- **轮询模式**：调用 `GET /api/v1/tasks/{task_id}` 查询状态，QPS 限流 20，建议按任务类型设置查询间隔（文本向量可短，图像生成宜长）。
- **事件驱动模式**：配置事件总线（EventBridge）接收 `dashscope:System:AsyncTaskFinish` 事件，支持 HTTP 回调或 RocketMQ 消息队列，规避轮询限流 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。

### 3. 子空间调用
- **OpenAI 兼容方式**：设置 `base_url` 为 `https://dashscope.aliyuncs.com/compatible-mode/v1`（北京）或 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`（新加坡），使用子空间专属 API Key。
- **DashScope 原生方式**：北京地域无需额外配置；新加坡等地域需显式设置 `base_http_api_url` 为工作空间专属域名。

### 4. 连接优化
- **Java SDK**：通过 `Constants.connectionConfigurations` 配置连接池参数（如 `connectionPoolSize=256`, `connectTimeout=10`）。
- **Python SDK**：同步调用传入 `requests.Session()`，异步调用传入 `aiohttp.ClientSession(connector=TCPConnector(limit=100))`。

## 限制和注意事项

- **临时文件**：单文件 ≤1GB；上传限流 100 QPS（按主账号+模型维度）；文件与模型强绑定，且仅限同一主账号下使用；**过期后自动清理，严禁用于生产环境** [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。
- **异步任务**：任务结果默认保留 24 小时（以具体模型文档为准），超时后无法查询；仅 `PENDING` 状态任务可取消 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。
- **地域一致性**：临时 API Key 的生成地域、子空间调用的 Endpoint 地域、文件上传的地域必须与模型服务地域匹配（如北京地域 Key 不能调用新加坡模型），各文档中地域 URL 示例存在差异，需严格对照 [Base URL 总览](raw/model-user-guide/get-started-with-models/base-url.md) 使用。
- **SDK 版本依赖**：`Files.upload(purpose='inference')` 要求 Python SDK ≥ `1.27.3`；Java SDK 连接池配置要求 ≥ `2.12.0` [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


