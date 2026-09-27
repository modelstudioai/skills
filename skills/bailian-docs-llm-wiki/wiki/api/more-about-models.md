# [more](more.md) about models

本文档面向开发者，系统梳理百炼平台模型调用的关键扩展能力，涵盖临时凭证、异步任务管理、子空间隔离、文件上传、连接复用等核心机制。所有能力均基于标准 API Key 体系构建，需配合正确的地域 Endpoint 和权限配置使用。

## 支持的模型/功能

百炼平台支持同步与异步两类模型调用模式：  
- **同步模型**（如 `qwen-plus`、`qwen-vl-plus`）适用于低延迟文本生成、多模态理解等场景，直接返回结果；  
- **异步模型**（如图像生成 `wanx2.1-t2i-turbo`、视频生成 `wanx2.1-kf2v-plus`、语音转写 `paraformer-16k-1`）适用于耗时较长的任务，需通过任务 ID 轮询或事件通知获取结果。  
- 所有模型均可在[默认业务空间](raw/model-user-guide/get-started-with-models/models.md)或[子业务空间](raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)中调用，子空间支持细粒度权限管控与分账。  
- 多模态模型（如 VL、OCR、ASR）调用时需传入文件，平台提供[上传本地文件获取临时URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)能力，支持 OSS 临时存储（48 小时有效期）。

> **注意**：文档 5 明确指出“文件上传时必须指定模型名称，且该模型须与后续调用的**模型一致**”，而文档 4 的子空间调用示例中未强调此约束。实际开发中，上传文件时使用的 `model_name` 必须与最终调用模型的名称完全一致（含版本后缀），否则模型服务将拒绝请求。

## 关键参数

| 参数 | 说明 | 典型取值 | 来源 |
|------|------|----------|------|
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒，默认 60 秒 | [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `task_id` | 异步任务唯一标识符 | UUID 格式字符串（如 `a8532587-xxxx-xxxx-xxxx-0c46b17950d1`） | [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) |
| `X-DashScope-OssResourceResolve: enable` | 使用 `oss://` URL 时必需的请求头 | 固定字符串 | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `connectionPoolSize` | Java SDK 连接池最大连接数 | 默认 32，高并发建议设为 256 | [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |

## 使用方式

### 1. 安全调用（不可信环境）
在浏览器或移动 App 中调用模型时，**禁止硬编码永久 API Key**。应由可信后端调用 `/api/v1/tokens` 接口生成临时 Key，并设置合理 TTL（如 `expire_in_seconds=1800`），详见 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。

### 2. 异步任务管理
对图像/视频/语音类模型，推荐两种结果获取方式：  
- **轮询**：调用 `GET /api/v1/tasks/{task_id}` 查询状态，注意遵守 20 QPS 限流，避免高频查询；  
- **事件驱动**：通过[事件总线配置 HTTP 回调或 RocketMQ](../../raw/model-api-reference/more-about-models/async-task-api.md)，任务完成后自动推送事件，业务系统解析 `task_id` 后仅需一次查询即可获取结果，规避轮询资源消耗与限流风险。

### 3. 子空间模型调用
- 使用子空间 API Key 调用标准模型（如 `qwen-plus`）前，**必须在控制台为其显式授权该模型**；  
- 调用子空间内微调部署的模型时，**无需额外授权，但仅限该空间 API Key 访问**；  
- OpenAI 兼容模式下，北京地域使用通用域名 `https://dashscope.aliyuncs.com/compatible-mode/v1`，新加坡等地域需替换为工作空间专属域名（如 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`）。

### 4. 连接复用优化
- **Java SDK**：通过 `Constants.connectionConfigurations` 配置连接池参数（如 `connectionPoolSize=256`, `connectTimeout=10`）；  
- **Python SDK**：同步调用传入 `requests.Session()`，异步调用传入 `aiohttp.ClientSession(connector=TCPConnector(...))`，显著降低 TCP 建连开销。

## 限制和注意事项

- **临时文件**：`oss://` URL 有效期严格为 48 小时，过期后无法访问；上传接口限流为 100 QPS（按主账号+模型维度），**严禁用于生产环境或压测**，生产环境请使用阿里云 OSS 自建存储；  
- **临时 API Key**：继承生成者 API Key 的全部权限（含知识库访问），且**无法手动删除**，仅能等待自动过期；  
- **异步任务生命周期**：任务结果默认保留 24 小时（以各模型文档为准），超时后数据被自动清理，`list` 接口将无法查到；  
- **地域一致性**：API Key、Endpoint、文件上传、任务查询必须使用同一地域（如北京、新加坡），跨地域调用将失败；  
- **子空间权限**：子空间 API Key 调用标准模型前，若未在控制台完成模型授权，将返回 `Forbidden` 错误，而非 `InvalidApiKey`。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


