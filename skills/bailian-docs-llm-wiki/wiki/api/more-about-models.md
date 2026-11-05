# [more](more.md) about models

阿里云百炼平台提供多种模型调用机制与配套能力，覆盖同步/异步任务、多业务空间隔离、文件上传、连接优化等关键场景。本文面向开发者，系统梳理模型使用的核心技术要点，包括支持的模型类型与功能边界、关键参数配置、主流调用方式，以及必须注意的限制与兼容性问题。

## 支持的模型/功能

百炼支持的模型按调用行为分为两类：  
- **同步模型**：如 `qwen-plus`、`qwen3-vl-plus` 等文本/多模态生成模型，请求后直接返回结果；  
- **异步模型**：如图像生成（`wanx2.1-t2i-turbo`）、视频生成（`wanx2.1-kf2v-plus`）、语音转写（`paraformer-16k-1`）等长耗时任务，需通过任务 ID 轮询或事件通知获取结果。  

异步任务统一由通用任务管理接口支撑，支持查询、批量列表、取消（仅限 `PENDING` 状态），详见 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。  
此外，平台支持通过事件总线（EventBridge）主动推送任务完成事件，避免轮询限流，适用于高并发、实时性要求高的生产场景，具体实现见 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。

## 关键参数

- **`task_id`**：异步任务唯一标识，用于 `fetch`、`list`、`cancel` 操作，生命周期默认 24 小时（以对应任务文档为准）。  
- **`model_name`**：必需参数，用于文件上传绑定（[上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)）、权限控制及事件过滤（如 `user_api_unique_key` 字段后缀）。  
- **`workspace_id` 与 `region`**：子业务空间调用必需，不同地域（北京、新加坡等）Endpoint 和 API Key 不互通，SDK 需显式传入。  
- **连接复用参数**：Java SDK 通过 `ConnectionConfigurations` 配置 `connectionPoolSize`、`maximumAsyncRequests` 等；Python SDK 通过 `httpx.Client` 或 `httpx.AsyncClient` 的 `limits` 参数控制 `max_connections` 和 `max_keepalive_connections`。  

> **注意**：文档 5 中 `client.files.upload` 的 `purpose` 参数取值为 `inference`（非 `model`），而上传凭证接口（`/api/v1/uploads?action=getPolicy`）明确要求 `model` 参数，二者语义不一致，实际使用中须严格按接口契约传参，不可混用。

## 使用方式

### 1. 子业务空间调用  
需使用该空间专属 API Key，并按地域选择 Endpoint：  
- **DashScope SDK**：构造 `Client` 时传入 `workspace` 和 `region`（如 `ap-southeast-1`）；  
- **OpenAI 兼容模式**：设置 `base_url` 为 `https://dashscope.aliyuncs.com/compatible-mode/v1`（北京）或 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`（新加坡），详见 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。  

### 2. 本地文件上传  
调用多模态模型前，需先上传文件获取 `oss://` 开头的临时 URL（有效期 48 小时），且请求头必须携带 `X-DashScope-OssResourceResolve: enable`。SDK 封装了 `client.files.upload(file_path, purpose="inference")`，但底层仍依赖 `model_name` 绑定（见文档 5 示例代码中 `get_upload_policy` 调用）。  

### 3. 连接复用配置  
- **Java**：全局配置 `Constants.connectionConfigurations`；  
- **Python**：传入自定义 `http_client` 实例（推荐 `with httpx.Client() as client:` 确保资源释放）。  

## 限制和注意事项

- **异步任务限流**：`/api/v1/tasks/{task_id}`、`/api/v1/tasks`、`/api/v1/tasks/{task_id}/cancel` 接口均为 **20 QPS/账号**，高频轮询易触发限流，建议结合任务类型设置合理间隔（如图像生成用 2–5 秒，文本向量用 100–500ms）。  
- **临时文件限制**：上传凭证接口限流 **100 QPS/主账号+模型**，且文件仅限同主账号、同模型使用，**严禁用于生产环境或压测**；生产环境应使用 OSS 自建存储。  
- **临时 API Key**：通过 `/api/v1/tokens` 生成，TTL 范围 1–1800 秒，继承源 API Key 全部权限，到期自动失效，不可手动删除。  
- **地域隔离**：北京、新加坡、弗吉尼亚、中国香港等地域的 API Key、Endpoint、账单完全独立，跨地域调用需分别配置。  
- **CLI 功能缺失**：`dashscope CLI` 当前仅 `video-synthesis` 子命令支持 `fetch`/`list`/`cancel`，其他异步任务（如图像、ASR）需用 SDK 或 curl，详见 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。

## 来源文档

- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


