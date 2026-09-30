# [more](more.md) about models

本文档面向开发者，系统梳理百炼平台模型调用的关键扩展能力，涵盖临时凭证管理、异步任务处理、子空间隔离、文件上传、连接复用等核心机制。所有能力均基于标准 API Key 体系构建，需配合正确的地域、模型权限与网络配置使用。

## 支持的模型/功能

百炼平台支持同步与异步两类模型调用模式：
- **同步模型**（如 `qwen-plus`、`qwen-vl-plus`）：适用于文本生成、多模态理解等低延迟场景，直接返回结果。
- **异步模型**（如图像生成 `wanx2.1-t2i-turbo`、视频生成 `wanx2.1-kf2v-plus`、语音转写 `paraformer-16k-1`）：适用于耗时较长的任务，需通过任务 ID 轮询或事件通知获取结果。详情见 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。

> **注意**：文档 3 中提到的“任务完成事件”类型为 `dashscope:System:AsyncTaskFinish`，但文档 2 的响应示例中 `output.task_status` 字段值包含 `CANCELED` 和 `UNKNOWN`，而文档 3 的参数描述表中未列出 `CANCELED` 状态；实际开发应以文档 2 的状态枚举为准。

此外，部分模型（如微调后部署的专属模型）仅支持在所属子业务空间内调用，且不兼容 [OpenAI 兼容接口](../concepts/openai-compatibility.md)，详见 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。

## 关键参数

| 参数 | 说明 | 取值范围/示例 | 来源 |
|------|------|----------------|------|
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒，默认 60 秒 | [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `task_id` | 异步任务唯一标识符 | UUID 格式字符串，如 `a8532587-xxxx-xxxx-xxxx-0c46b17950d1` | [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) |
| `model_name` | 文件上传时绑定的模型名 | 必须与后续模型调用一致，如 `qwen-vl-plus` | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `X-DashScope-OssResourceResolve: enable` | 使用 `oss://` URL 时必需的请求头 | 固定字符串 | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |

## 使用方式

### 1. 安全调用（不可信环境）
在浏览器或移动 App 中，**禁止硬编码永久 API Key**。应由可信后端调用 `/api/v1/tokens` 接口生成临时 Key，并设置合理 TTL（建议 ≤ 180 秒），其权限继承自父 Key。参见 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。

### 2. 异步任务处理
- **轮询模式**：调用 `GET /api/v1/tasks/{task_id}` 查询状态，注意遵守 20 QPS 限流，避免高频查询；
- **事件驱动模式**：配置事件总线（EventBridge）接收 `dashscope:System:AsyncTaskFinish` 事件，支持 HTTP 回调或 RocketMQ 消费，规避轮询资源消耗与限流风险。详见 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。

### 3. 子空间模型调用
需使用**子业务空间专属 API Key**，并确保：
- 调用标准模型前已在该空间完成[模型调用权限配置](https://help.aliyun.com/zh/model-studio/permission-management-overview#f642213a1f38l)；
- 调用地址使用工作空间专属域名（如 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`）或通用兼容地址（`dashscope.aliyuncs.com/compatible-mode/v1`）；
- 不得混用默认空间与子空间的 Key 或域名。

### 4. 多模态文件输入
上传本地文件获取 `oss://` 前缀临时 URL（有效期 48 小时），调用时必须在 Header 中添加 `X-DashScope-OssResourceResolve: enable`。注意：文件与模型强绑定，且仅限同一主账号下使用。生产环境请使用 OSS 自有存储。参见 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

### 5. 连接复用优化
- **Java SDK**：通过 `Constants.connectionConfigurations` 配置连接池（如 `connectionPoolSize=256`）；
- **Python SDK**：同步调用传入 `requests.Session()`，异步调用传入 `aiohttp.ClientSession(connector=...)`；
- 所有配置均需在首次调用前完成，否则无效。

## 限制和注意事项

- **临时 Key 无法主动删除**：到期自动失效，无撤销接口；
- **异步任务保留期**：成功/失败任务默认保留 24 小时（具体以各模型文档为准），超时后无法查询；
- **文件上传限流严格**：按“主账号+模型”维度限 100 QPS，**禁止用于压测或生产高频场景**；
- **地域隔离**：北京、新加坡、弗吉尼亚、中国香港等地域的 API Key 与 Endpoint **完全独立**，不可混用；
- **子空间权限隔离**：子空间 API Key 无法调用默认空间模型，反之亦然；调优模型仅限本空间调用；
- **连接复用生效前提**：Python SDK 中 `session` 参数必须显式传入 `call()` 方法，否则不生效；
- **生产环境警示**：临时文件 URL（48 小时）、临时 API Key（≤30 分钟）均**不适用于生产环境长期服务**，应使用自有 OSS + 长效认证方案。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


