# [more](more.md) about models

本文档面向开发者，汇总百炼平台模型调用的关键技术要点，涵盖模型访问控制、异步任务管理、多业务空间隔离、连接优化及文件处理等核心能力。所有功能均需配合有效的 API Key 使用，且不同地域（北京/新加坡/弗吉尼亚/中国香港）的 API Key 与 Endpoint 不可混用。

## 支持的模型/功能

百炼平台支持同步与异步两类模型调用模式：
- **同步模型**：如 `qwen-plus`、`qwen-vl-plus` 等文本与多模态大模型，直接返回结果；
- **异步模型**：如图像生成（`wanx2.1-t2i-turbo`）、视频生成（`wanx2.1-kf2v-plus`）、语音转写（`paraformer-8k-v1`）等耗时较长的任务，需通过任务 ID 轮询或事件通知获取结果。  
异步任务统一由 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) 提供标准化接口（`fetch`/`list`/`cancel`），支持跨模型、跨地域查询，且 SDK 封装已覆盖 `ImageSynthesis`、`VideoSynthesis`、`Transcription` 等类。

对于多业务场景，平台支持**子业务空间（Sub Workspace）** 隔离：标准模型（如 `qwen-plus`）需在子空间中显式授权后方可调用；而用户在该空间内调优部署的私有模型，则仅限本空间 API Key 访问，无需额外授权。详情见 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。

> **注意**：文档 4 中明确指出“调用在阿里云百炼[调优](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)并部署的模型，**无需模型调用授权**”，但文档 6 的 `Files.upload` 示例中 `purpose='fine_tune'` 用于微调训练文件上传，与模型调用权限无直接关联——二者属于不同功能域，不构成矛盾。

## 关键参数

| 参数 | 说明 | 典型值/范围 | 来源 |
|------|------|-------------|------|
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒（默认 60 秒） | [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `task_id` | 异步任务唯一标识符 | UUID 格式字符串（如 `a8532587-xxxx-xxxx-xxxx-0c46b17950d1`） | [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) |
| `model_name` | 文件上传时绑定的模型名，决定 URL 可用性 | 如 `qwen-vl-plus`、`wanx2.1-t2i-turbo` | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `connectionPoolSize` | Java SDK 连接池最大连接数 | 默认 `32`，高并发建议设为 `256` | [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |

## 使用方式

### 1. 安全调用（不可信环境）
在浏览器或移动 App 等前端场景，**禁止硬编码永久 API Key**。应通过后端服务调用 `/api/v1/tokens` 接口生成临时 Key，并设置合理 TTL（如 `expire_in_seconds=300`）。临时 Key 继承源 Key 的全部权限，且到期自动失效，不可手动删除。

### 2. 异步任务处理
避免高频轮询（≤20 QPS 限流），推荐两种方案：
- **轮询模式**：使用 `fetch(task_id)` 查询单任务，或 `list(status='SUCCEEDED', page_size=10)` 批量筛选；
- **事件驱动模式**：通过 [事件总线 EventBridge](../../raw/model-api-reference/more-about-models/async-task-api.md) 配置 HTTP 回调或 RocketMQ，接收 `dashscope:System:AsyncTaskFinish` 事件后按需查询结果，实现零轮询、高实时性。

### 3. 子空间模型调用
- **OpenAI 兼容方式**：设置 `base_url` 为 `https://dashscope.aliyuncs.com/compatible-mode/v1`（北京）或 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`（新加坡），并使用子空间专属 API Key；
- **DashScope 原生方式**：Java/Python SDK 需显式配置 `base_url` 指向子空间域名（如 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1`）。

### 4. 连接复用优化
- **Java SDK**：通过 `Constants.connectionConfigurations` 配置连接池参数（如 `connectionPoolSize=256`, `readTimeout=300`）；
- **Python SDK**：同步调用传入 `requests.Session()`，异步调用传入 `aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=100))`。

### 5. 多模态文件处理
上传本地文件获取 `oss://` 开头的临时 URL（有效期 48 小时），**必须满足**：
- 上传时指定 `model_name`，且后续模型调用必须使用同一模型；
- HTTP 请求头需添加 `X-DashScope-OssResourceResolve: enable`；
- 生产环境禁用此机制，应改用 OSS 等持久化存储。

## 限制和注意事项

- **临时文件服务**：上传限流为 100 QPS（按主账号+模型维度），且文件不可下载/修改，**严禁用于生产环境、压测及高并发场景**。详见 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。
- **异步任务保留期**：任务完成后数据默认保留 24 小时（具体以各模型文档为准），超时后自动清理，`list` 接口将无法查到历史记录。
- **地域隔离**：API Key 与 Endpoint 严格绑定地域（北京/新加坡/弗吉尼亚/中国香港），混用将导致 `InvalidApiKey` 错误。例如，新加坡地域的 Key 必须搭配 `ap-southeast-1` 的 URL。
- **权限继承风险**：临时 API Key 完全继承生成它的永久 Key 的权限（含知识库访问限制），请确保源 Key 权限最小化。
- **取消任务限制**：仅状态为 `PENDING` 的异步任务可被取消，`RUNNING` 或 `SUCCEEDED` 状态调用 `cancel` 接口将返回 `UnsupportedOperation` 错误码。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)


