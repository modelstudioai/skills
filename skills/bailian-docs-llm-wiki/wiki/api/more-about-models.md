# [more](more.md) about models

本文档面向开发者，系统介绍百炼平台模型调用的进阶能力与关键约束，涵盖异步任务管理、子业务空间调用、连接复用、临时文件上传、临时API Key生成等核心机制。所有功能均需配合有效的 API Key 使用，且不同地域（北京/新加坡/弗吉尼亚/中国香港）的 API Key 与 Endpoint 不互通。

## 支持的模型/功能

百炼平台支持同步与异步两类模型调用模式：
- **同步模型**：如 `qwen-plus`、`qwen3-vl-plus` 等文本/多模态大模型，请求即响应，适用于低延迟场景。
- **异步模型**：如图像生成（`wanx2.1-t2i-turbo`）、视频合成（`wanx2.1-kf2v-plus`）、语音转写（`paraformer-16k-1`）等长耗时任务，需通过任务 ID 轮询或事件通知获取结果。详情见 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。

此外，平台提供以下辅助能力：
- **子业务空间模型调用**：支持为不同业务线或用户组创建独立空间，实现模型权限隔离与费用分账，调用时需使用对应空间的 API Key 和专属 Endpoint。
- **临时文件上传**：为多模态模型提供免费 OSS 临时存储，上传后返回 `oss://` 格式 URL（有效期 48 小时），调用时需在 Header 中添加 `X-DashScope-OssResourceResolve: enable`。该功能不适用于生产环境，高并发场景请使用 [阿里云OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss)。详情见 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。
- **临时API Key生成**：适用于浏览器、移动 App 等不可信环境，由后端服务基于永久 API Key 动态签发，继承其全部权限（含模型/知识库访问限制），TTL 可设为 1–1800 秒。详情见 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。

> **注意**：文档 6 中称“DashScope SDK 的 `client.files.upload` 无 `model` 参数”，但文档 6 同时明确要求“文件上传时必须指定模型名称，且该模型须与后续调用的模型一致”。SDK 封装虽隐藏了显式 `model` 字段，但底层仍强制校验模型一致性，实际使用中必须确保 `purpose='inference'` 对应的模型上下文与后续推理请求严格匹配，否则调用将失败。

## 关键参数

| 参数 | 说明 | 典型值/范围 | 注意事项 |
|------|------|-------------|----------|
| `expire_in_seconds` | 临时API Key有效期 | `[1, 1800]` 秒 | 默认 60 秒；超时后自动失效，不可手动删除 |
| `task_id` | 异步任务唯一标识 | UUID 格式字符串 | 用于查询状态（`GET /api/v1/tasks/{task_id}`）或取消（`POST /api/v1/tasks/{task_id}/cancel`） |
| `status` | 异步任务状态 | `PENDING`, `RUNNING`, `SUCCEEDED`, `FAILED`, `CANCELED`, `UNKNOWN` | 仅 `PENDING` 状态可取消；`SUCCEEDED` 表示至少一个子任务成功 |
| `page_size` / `page_no` | 批量查询任务分页参数 | `page_size` 默认 10，最大建议 50 | 避免过大 `page_size` 导致响应延迟 |
| `connectionPoolSize` (Java) / `max_connections` (Python) | HTTP 连接池大小 | Java 默认 32；Python 建议 100 | 高并发场景需调优，过高易触发服务端限流 |
| `model_name` | 临时文件绑定模型名 | 如 `qwen3-vl-plus` | 必须与后续模型调用的 `model` 参数完全一致，否则报错 |

## 使用方式

### 异步任务结果获取
- **轮询方式**：调用 `GET /api/v1/tasks/{task_id}` 查询单个任务，或 `GET /api/v1/tasks` 批量查询。QPS 限流为 20，建议按任务类型设置合理间隔（文本向量可短，图像/视频宜长）。
- **事件通知方式**：配置事件总线（EventBridge）接收 `dashscope:System:AsyncTaskFinish` 事件，目标支持 HTTP 回调或 RocketMQ。相比轮询，该方式不限流、实时性高、资源消耗低，推荐用于高并发或实时性敏感场景。详情见 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。

### 子业务空间调用
- **DashScope SDK 方式**：构造 `Client` 时传入 `workspace` 和 `region`（如 `ap-southeast-1`），并使用该空间的 API Key。
- **OpenAI 兼容方式**：北京地域使用通用域名 `https://dashscope.aliyuncs.com/compatible-mode/v1`；新加坡等地域必须使用工作空间专属域名 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`。

### 连接复用配置
- **Java SDK**：通过 `Constants.connectionConfigurations` 设置连接池参数（如 `connectionPoolSize`, `readTimeout`）。
- **Python SDK**：传入自定义 `httpx.Client` 或 `httpx.AsyncClient` 实例，并配置 `limits`。推荐使用 `with` 语句管理生命周期。

### 临时文件上传
1. 调用 `GET /api/v1/uploads?action=getPolicy&model={model_name}` 获取上传凭证；
2. 使用凭证将文件 POST 到 OSS Host，获得 `oss://` URL；
3. 在模型调用请求 Header 中添加 `X-DashScope-OssResourceResolve: enable`；
4. 在请求 Body 中使用该 URL（如 `"image_url": "oss://..."`）。

## 限制和注意事项

- **地域隔离**：北京、新加坡、弗吉尼亚、中国香港四地的 API Key 与 Endpoint 完全独立，不可混用。[生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) 文档已强调“各地域的API Key 不同”。
- **临时资源时效性**：
  - 临时API Key：最长 1800 秒，到期自动失效。
  - 临时文件 URL：固定 48 小时，过期后无法访问。
  - 异步任务历史数据：通常保留 24 小时（以具体任务文档为准），超时后自动清理。
- **权限与安全**：
  - 临时API Key 继承签发 Key 的全部权限，包括对特定模型/知识库的访问控制。
  - 文件上传与模型调用必须使用同一阿里云主账号下的 API Key。
  - 子业务空间中调用标准模型（如 `qwen-plus`）前，需单独授权；而调优部署的模型则无需额外授权，但仅限本空间调用。
- **生产环境警示**：
  - 临时文件上传接口 QPS 限流 100，且不支持扩容，**严禁用于生产环境、高并发及压测场景**。
  - 临时API Key 和临时文件 URL 均为开发/测试用途，生产环境应使用长期有效的 API Key 和稳定存储（如 OSS）。
- **限流策略**：
  - 异步任务查询接口：20 QPS（账号级）。
  - 文件上传凭证接口：100 QPS（主账号+模型维度）。
  - 所有接口均受通用 API 调用配额约束，详见控制台配额管理。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)


