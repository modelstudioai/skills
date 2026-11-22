# [more](more.md) about models

阿里云百炼平台提供多种模型调用机制与配套能力，涵盖[异步任务](../concepts/asynchronous-task.md)管理、子空间隔离、连接复用、文件上传、临时密钥等关键场景。本文档面向开发者，系统梳理核心功能、参数配置、使用方式及限制条件，帮助构建稳定高效的模型服务集成。

## 支持的模型/功能

百炼支持同步与异步两类模型调用模式：  
- **同步模型**（如 `qwen-plus` 文本生成）：直接返回结果，适用于低延迟、确定性响应场景；  
- **异步模型**（如图像生成 `wanx2.1-t2i-turbo`、视频生成 `wanx2.1-kf2v-plus`、语音转写 `paraformer-16k-1`）：需通过任务 ID 轮询或事件通知获取结果，适用于长耗时任务 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。  

此外，平台提供以下关键辅助功能：  
- **子业务空间模型调用**：支持在非默认工作空间中调用标准模型（如 `qwen-plus`）或专属调优模型，实现权限隔离与费用分账；  
- **临时文件 URL 上传**：为[多模态](../concepts/multi-modal.md)模型（如 `qwen3-vl-plus`）提供免费 OSS 临时存储，生成 48 小时有效 `oss://` URL；  
- **临时 API Key 生成**：用于浏览器、移动端等不可信环境，避免永久密钥泄露，有效期可设为 1–1800 秒 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)；  
- **HTTP 回调与 RocketMQ 事件通知**：替代轮询，通过事件总线推送 `dashscope:System:AsyncTaskFinish` 事件，提升实时性并规避 QPS 限流 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。

> **注意**：文档 6 中 DashScope SDK 的 `client.files.upload` 方法声明 `purpose` 参数仅支持 `fine_tune` 或 `inference`，**未要求指定 `model_name`**；但文档 6 同时明确强调“文件上传时必须指定模型名称，且该模型须与后续调用的模型一致”。二者存在逻辑矛盾——SDK 封装层隐藏了模型绑定，而底层协议仍强制校验。实际使用中，`purpose="inference"` 的上传行为隐式关联当前 API Key 所属空间的默认推理上下文，但跨模型复用仍被禁止。建议以 HTTP 接口为准，在上传凭证请求中显式传入 `model` 参数。

## 关键参数

| 参数 | 作用 | 典型值/范围 | 来源 |
|------|------|-------------|------|
| `task_id` | [异步任务](../concepts/asynchronous-task.md)唯一标识 | UUID 格式字符串（如 `a8532587-xxxx-xxxx-xxxx-0c46b17950d1`） | [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) |
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒 | [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `connectionPoolSize`（Java） / `max_connections`（Python） | 连接池最大连接数 | Java 默认 32，推荐高并发场景设为 256；Python 默认无限制，建议设为 100 | [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |
| `model_name`（上传时） | 绑定临时文件的模型名 | 如 `qwen3-vl-plus`, `wanx2.1-t2i-turbo` | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `X-DashScope-OssResourceResolve` | 使用 `oss://` URL 时必需的请求头 | 固定值 `enable` | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |

## 使用方式

### [异步任务](../concepts/asynchronous-task.md)管理
1. **提交任务**：调用对应模型的创建接口（如 `client.images.jobs.create`），获取 `task_id`；  
2. **查询结果**：  
   - 轮询：调用 `GET /api/v1/tasks/{task_id}`，建议按任务类型设置间隔（文本向量可短至 1s，图像/视频建议 ≥5s）；  
   - 事件驱动：配置事件总线规则，监听 `dashscope:System:AsyncTaskFinish` 事件，收到后调用一次查询接口即可；  
3. **批量操作**：使用 `GET /api/v1/tasks` 按 `start_time`/`end_time`/`status`/`model_name` 筛选任务列表；  
4. **取消任务**：仅对 `PENDING` 状态任务有效，调用 `POST /api/v1/tasks/{task_id}/cancel`。

### 子空间调用
- **OpenAI 兼容方式**：固定 `base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"`，但**必须使用子空间的 API Key**；  
- **DashScope 原生方式**：构造 Client 时显式传入 `workspace` 和 `region`（如 `ap-southeast-1`），无需修改 `base_url`。

### 连接复用
- **Java**：通过 `Constants.connectionConfigurations` 全局配置连接池参数；  
- **Python**：传入自定义 `httpx.Client` 或 `httpx.AsyncClient` 实例，推荐使用 `with` 语句确保资源释放。

### 临时文件与密钥
- **文件上传**：先调用 `/api/v1/uploads?action=getPolicy&model={model}` 获取凭证，再直传 OSS，返回 `oss://` URL；调用模型时需在 Header 添加 `X-DashScope-OssResourceResolve: enable`；  
- **临时密钥**：向 `/api/v1/tokens?expire_in_seconds=1800` 发起 POST，使用主账号的永久 API Key 鉴权，响应含 `token` 与 `expires_at`。

## 限制和注意事项

- **异步任务保留期**：成功/失败任务默认保留 **24 小时**，超时后无法查询，具体以各任务文档为准 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)；  
- **临时文件限制**：  
  - 单文件 ≤ 1 GB；  
  - 有效期严格为 **48 小时**，过期即失效；  
  - **严禁用于生产环境**，因存在 100 QPS 限流且不支持扩容，生产应使用阿里云 OSS；  
- **临时 API Key**：无法手动删除，到期自动失效；继承父密钥全部权限，包括模型访问控制；  
- **地域隔离**：北京、新加坡、弗吉尼亚、中国香港等地域的 API Key **完全独立**，不可混用；  
- **连接复用最佳实践**：Python 同步调用中若复用 `http_client`，务必显式调用 `close()`；Java 中 `maximumAsyncRequestsPerHost` 不得超过 `connectionPoolSize`，否则请求可能阻塞。

## 来源文档

- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)


