# [more](more.md) about models

本文档面向开发者，汇总百炼平台中与模型调用深度相关的进阶能力，涵盖临时凭证管理、异步任务处理、多业务空间隔离、文件上传与连接复用等核心机制。这些功能不改变基础模型接口语义，但显著影响生产环境的可靠性、安全性和性能表现。

## 支持的模型/功能

百炼平台支持多种模型调用模式，具体能力取决于模型类型：
- **同步模型**（如 `qwen-plus` 文本生成）：直接返回结果，适用于低延迟交互场景；
- **异步模型**（如图像生成 `wanx2.1-t2i-turbo`、视频生成 `wanx2.1-kf2v-plus`、语音转写 `paraformer-16k-1`）：需通过任务 ID 轮询或事件通知获取结果，详见 [异步任务管理 API](raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)；
- **多模态模型**（如 `qwen-vl-plus`）：支持本地文件输入，需先上传获取临时 URL，该 URL 与模型强绑定，不可跨模型复用，详见 [上传本地文件获取临时URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)；
- **子业务空间模型**：支持在非默认空间中调用标准模型（如 `qwen-plus`）或专属调优模型，实现权限隔离与费用分账，详见 [子业务空间的模型调用](raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。

> **注意**：文档 4 中明确指出“调用在阿里云百炼[调优](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)后的模型，仅支持通过 DashScope 调用，不支持通过 OpenAI 兼容方式调用”，但文档 4 的 OpenAI 兼容示例代码中却对 `qwen-plus`（标准模型）使用了该方式——此为正确用法；而对调优模型禁用 OpenAI 兼容方式是强制约束，开发者须严格区分模型类型。

## 关键参数

| 参数 | 作用 | 取值范围/说明 | 来源 |
|------|------|----------------|------|
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒，默认 60 秒 | [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `task_id` | 异步任务唯一标识 | UUID 格式字符串，由创建任务接口返回 | [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) |
| `model_name` | 文件上传时必需的模型标识 | 必须与后续模型调用的 `model` 参数完全一致，例如 `qwen-vl-plus` | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `X-DashScope-OssResourceResolve: enable` | 使用 `oss://` URL 时必需的请求头 | 固定字符串，缺失将导致模型调用失败 | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `connectionPoolSize` / `limit` | Java/Python SDK 连接池大小 | Java 默认 32，Python `aiohttp` 默认 100；高并发建议调大 | [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |

## 使用方式

### 1. 安全调用（不可信环境）
在浏览器或移动 App 等前端场景中，**禁止硬编码永久 API Key**。应由后端服务调用 `/api/v1/tokens` 接口生成临时 Key，并设置合理 TTL（如 `expire_in_seconds=300`），避免权限泄露风险。

### 2. 异步任务处理
- **轮询模式**：调用 `GET /api/v1/tasks/{task_id}` 查询状态，建议按任务类型设置间隔（文本类 1–2s，图像类 3–5s，视频类 ≥10s），避免触发 20 QPS 限流；
- **事件驱动模式**：配置事件总线（EventBridge）接收 `dashscope:System:AsyncTaskFinish` 事件，支持 HTTP 回调或 RocketMQ 消费，彻底规避轮询开销，详见 [通过HTTP回调URL或MQ接收异步任务完成通知](raw/model-api-reference/more-about-models/async-task-api.md)；
- **批量管理**：使用 `GET /api/v1/tasks` 按时间、状态、模型名等条件批量查询任务，适用于运维监控场景。

### 3. 多业务空间调用
- 子空间调用标准模型（如 `qwen-plus`）：必须使用该空间的 API Key，并显式配置 `base_url`（如北京地域为 `https://dashscope.aliyuncs.com/compatible-mode/v1`）；
- 子空间调用调优模型：**仅支持 DashScope 原生 SDK**，且无需额外授权，但必须使用工作空间专属域名（如 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）。

### 4. 文件上传与引用
- 上传前确认模型支持的文件类型与大小限制（如 `qwen-vl-plus` 支持 ≤1GB 图片）；
- 上传后获得 `oss://` URL，**必须在模型调用请求头中添加 `X-DashScope-OssResourceResolve: enable`**；
- 生产环境严禁依赖此临时存储，应使用 OSS 等持久化方案。

### 5. 连接优化
- **Java**：通过 `Constants.connectionConfigurations` 配置连接池参数，重点调整 `connectionPoolSize` 和 `maximumAsyncRequests`；
- **Python 同步**：复用 `requests.Session()` 实例；
- **Python 异步**：传入配置了 `aiohttp.TCPConnector(limit=100)` 的 `ClientSession`。

## 限制和注意事项

- **临时 Key 无法撤销**：生成后只能等待过期，[生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) 明确说明“不能手动删除”；
- **文件有效期严格为 48 小时**：超时后 URL 失效，且文件被自动清理，不可恢复；
- **文件上传限流严重**：按“主账号+模型”维度限 100 QPS，**明确禁止用于生产环境、高并发及压测场景**，详见 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)；
- **异步任务保留期为 24 小时**：超时后 `GET /api/v1/tasks/{task_id}` 将返回 `UNKNOWN`，历史数据不可查；
- **取消任务仅限 PENDING 状态**：`RUNNING` 或 `SUCCEEDED` 等状态调用 `/cancel` 接口会返回 `UnsupportedOperation` 错误；
- **地域一致性要求**：API Key、WorkspaceId、Endpoint 必须属于同一地域（北京/新加坡/弗吉尼亚/中国香港），跨地域调用将失败。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


