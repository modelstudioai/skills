# more about models

本文档面向开发者，系统梳理百炼平台模型调用的关键扩展能力，涵盖异步任务管理、子业务空间隔离、临时凭证与文件上传、连接复用等核心机制。这些能力不改变基础模型接口语义，但显著提升生产环境下的安全性、可观测性与资源效率。

## 支持的模型/功能

百炼平台支持多种模型调用模式，适配不同场景需求：

- **标准模型（如 `qwen-plus`）**：可通过 [DashScope SDK](raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md) 或 OpenAI 兼容方式调用，需在子业务空间中显式授权模型调用权限。
- **多模态/生成类模型（如 `wanx2.1-t2i-turbo`, `paraformer-8k-v2`）**：默认采用异步任务机制，需通过任务 ID 查询结果或配置事件通知；部分模型（如文生图、文生视频）在 [异步任务管理 API](raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) 中提供完整生命周期控制。
- **微调后模型**：仅限其所属子业务空间的 API Key 调用，不支持 OpenAI 兼容方式，详见 [子业务空间的模型调用](raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。

> **注意**：文档 4 明确指出“调用在阿里云百炼[调优](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)并部署的模型，**无需模型调用授权**”，但文档 5 的文件上传限制强调“文件上传时必须指定模型名称，且该模型须与后续调用的**模型一致**”。二者逻辑一致——微调模型虽免授权，但仍受严格模型绑定约束，不可混用临时文件。

## 关键参数

| 参数 | 说明 | 取值范围/示例 | 来源 |
|------|------|----------------|------|
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒，默认 60 秒 | [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `task_id` | 异步任务唯一标识符 | UUID 格式字符串，如 `a8532587-xxxx-xxxx-xxxx-0c46b17950d1` | [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) |
| `model_name` | 文件上传时绑定的模型名 | 必须与后续模型调用完全一致，如 `qwen3-vl-plus` | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `X-DashScope-OssResourceResolve: enable` | 使用 `oss://` URL 时必需的请求头 | 固定字符串 | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |

## 使用方式

### 1. 安全调用（前端/不可信环境）
在浏览器或移动 App 中，**禁止硬编码永久 API Key**。应由可信后端服务调用 `/api/v1/tokens` 接口生成临时 Key，并设置合理 TTL（建议 ≤ 180 秒），避免权限泄露。

### 2. 异步任务处理
对图像生成、语音转写等长耗时任务：
- **轮询方案**：调用 `GET /api/v1/tasks/{task_id}` 查询状态，注意遵守 20 QPS 限流，按任务类型设置合理间隔（文本类可短至 1s，图像类建议 ≥ 3s）；
- **事件驱动方案**：通过 [事件总线配置 HTTP 回调或 RocketMQ](raw/model-api-reference/more-about-models/async-task-api.md)，接收 `dashscope:System:AsyncTaskFinish` 事件后仅一次查询结果，规避轮询开销与限流风险。

### 3. 子业务空间隔离
为实现权限管控或分账，需：
- 在子空间创建独立 API Key；
- 对标准模型显式授权（微调模型自动继承）；
- 调用时使用对应空间的 API Key，并按地域选择正确 Base URL（如北京地域用 `https://dashscope.aliyuncs.com/compatible-mode/v1`）。

### 4. 多模态文件输入
上传本地文件获取临时 URL：
- 调用 `GET /api/v1/uploads?action=getPolicy&model={model_name}` 获取上传策略；
- 使用策略参数直传 OSS，获得 `oss://` URL；
- **关键**：模型调用请求头必须包含 `X-DashScope-OssResourceResolve: enable`，否则解析失败。

### 5. 连接复用优化
高并发场景下：
- **Java SDK**：通过 `Constants.connectionConfigurations` 配置连接池（如 `connectionPoolSize=256`, `maximumAsyncRequests=256`）；
- **Python SDK**：同步调用传入 `requests.Session()`，异步调用传入 `aiohttp.ClientSession(connector=TCPConnector(...))`。

## 限制和注意事项

- **临时凭证时效性**：临时 API Key 与临时文件 URL 均为短期凭证（TTL ≤ 1800 秒 / 有效期 48 小时），**严禁用于生产环境长期服务**。生产环境应使用阿里云 OSS 等持久化存储 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。
- **地域与 API Key 绑定**：各 Region（北京/新加坡/弗吉尼亚/中国香港）的 API Key **完全独立且不可互换**，调用前务必确认 Key 与 Endpoint 地域匹配 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。
- **异步任务数据保留**：任务完成后数据默认保留 24 小时（具体以对应模型文档为准），超时后自动清理，需及时查询 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。
- **文件上传限流**：`/api/v1/uploads` 接口按“主账号+模型”维度限流 100 QPS，超出即失败，不支持扩容，**禁止用于压测或高并发场景** [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。
- **模型绑定强约束**：上传文件时指定的 `model_name` 必须与后续模型调用的 `model` 参数**完全一致（含版本号）**，否则调用将失败。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


