# [more](more.md) about models

百炼平台提供多种高级模型调用能力，涵盖[异步任务](../concepts/asynchronous-task.md)管理、子业务空间隔离、临时凭证与文件上传、连接复用优化等核心场景。本文面向开发者，系统梳理模型服务的扩展功能、关键参数、使用方式及实践约束，帮助构建稳定、高效、可管控的 AI 应用。

## 支持的模型/功能

百炼支持同步与异步两类模型调用模式：
- **同步模型**：如 `qwen-plus`、`qwen3-vl-plus` 等文本/多模态大模型，适用于低延迟、确定性响应场景。
- **异步模型**：明确标注为异步的模型（如图像生成 `wanx2.1-t2i-turbo`、视频合成 `wanx2.1-kf2v-plus`、语音转写 `paraformer-16k-1`），需通过任务 ID 轮询或事件通知获取结果。详情见 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。

此外，平台支持：
- **子业务空间模型调用**：实现模型权限隔离与费用分账，适用于多租户或跨团队协作场景；
- **临时文件上传与 URL 生成**：为多模态输入提供免 OSS 配置的临时存储，但仅限 48 小时有效；
- **临时 API Key 生成**：在不可信前端环境（如浏览器、App）中安全调用模型，避免永久密钥泄露。

> **注意**：文档 5 中强调“文件上传时必须指定模型名称，且该模型须与后续调用的**模型一致**”，而文档 3 指出“调用在阿里云百炼[调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)并部署的模型，**无需模型调用授权**”。二者逻辑一致——模型绑定是资源隔离前提，但授权要求因模型类型（标准 vs 微调）而异。

## 关键参数

| 参数 | 说明 | 典型取值/范围 | 来源 |
|------|------|----------------|------|
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒（默认 60） | [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `task_id` | [异步任务](../concepts/asynchronous-task.md)唯一标识符 | UUID 格式字符串（如 `a8532587-...-0c46b17950d1`） | [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) |
| `model_name` | 文件上传时必需的模型标识 | 如 `qwen3-vl-plus`、`wanx2.1-t2i-turbo` | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `connectionPoolSize` / `max_connections` | Java/Python SDK 连接池大小 | Java 默认 32；Python 建议设为 100+（高并发） | [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |
| `contain_result` | HTTP 回调事件中是否内嵌结果 | `true` 或 `false`（影响是否需二次查询） | [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md) |

## 使用方式

### 1. [异步任务](../concepts/asynchronous-task.md)管理
- **创建任务**：调用对应模型的异步接口（如 `/api/v1/services/aigc/image-synthesis/jobs`），获取 `task_id`；
- **查询状态**：使用 `GET /api/v1/tasks/{task_id}`（单查）或 `GET /api/v1/tasks`（批量）；
- **取消任务**：仅支持取消 `PENDING` 状态任务，调用 `POST /api/v1/tasks/{task_id}/cancel`；
- **避免轮询**：推荐配置 [事件总线回调](../../raw/model-api-reference/more-about-models/async-task-api.md)（HTTP 或 RocketMQ），由平台主动推送 `dashscope:System:AsyncTaskFinish` 事件。

### 2. 子业务空间调用
- **API Key 绑定**：必须使用子空间生成的 API Key，且该 Key 需已获得目标模型调用权限（标准模型）或已部署模型（微调模型）；
- **Endpoint 选择**：
  - DashScope 方式：显式指定 `workspace` 和 `region`（如 `ap-southeast-1`）；
  - OpenAI 兼容方式：北京地域统一用 `https://dashscope.aliyuncs.com/compatible-mode/v1`；新加坡地域需替换为 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`。

### 3. 临时文件与凭证
- **上传流程**：先调用 `GET /api/v1/uploads?action=getPolicy&model={model_name}` 获取策略，再按 OSS 表单上传，返回 `oss://` URL；
- **调用约束**：模型请求中传入该 URL 时，**必须**在 Header 中添加 `X-DashScope-OssResourceResolve: enable`；
- **SDK 简化**：Python SDK `client.files.upload(file_path, purpose="inference")` 自动处理策略与上传。

### 4. 连接复用
- **Java**：通过 `Constants.connectionConfigurations` 全局配置连接池参数（如 `connectionPoolSize=256`）；
- **Python**：构造 `Client` 或 `AsyncClient` 时传入自定义 `httpx.Client` / `httpx.AsyncClient` 实例，并设置 `limits`。

## 限制和注意事项

- **临时 API Key**：继承生成者 API Key 的全部权限，**无法提前删除**，到期自动失效；各地域 API Key 不互通 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。
- **临时文件**：48 小时有效期、1GB 单文件上限、严格绑定模型与主账号；**禁止用于生产环境**，高并发场景请使用 OSS [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。
- **异步任务保留期**：任务完成后通常保留 24 小时（具体以模型文档为准），超时后数据被自动清理，查询将返回 `UNKNOWN` 状态。
- **限流策略**：
  - 任务查询/取消接口：20 QPS（按主账号计）；
  - 文件上传凭证接口：100 QPS（按“主账号 + 模型”维度）；
  - 所有接口均受通用配额约束，详见控制台配额管理。
- **地域一致性**：API Key、Workspace、Endpoint 必须属同一地域（北京/新加坡/弗吉尼亚/中国香港），混用将导致 `InvalidApiKey` 错误。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


