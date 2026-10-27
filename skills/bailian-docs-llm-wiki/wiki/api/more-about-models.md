# [more](more.md) about models

本文档面向开发者，系统梳理百炼平台模型调用的进阶能力与关键约束。涵盖模型访问控制、异步任务管理、多模态文件处理、连接优化及事件通知等核心场景，帮助您构建稳定、高效、可扩展的模型集成方案。

## 支持的模型/功能

百炼平台支持多种模型调用模式与配套功能：

- **标准模型与自定义模型**：可通过默认业务空间或子业务空间调用[标准模型](raw/model-user-guide/get-started-with-models/models.md)（如 `qwen-plus`），也可调用在百炼中[调优并部署的模型](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)，后者仅限其所属业务空间的 API Key 调用。
- **异步任务模型**：图像生成、视频合成、语音转写等长耗时任务采用异步机制，需通过[异步任务管理 API](raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) 创建、查询与取消任务。
- **多模态输入支持**：调用视觉语言（VL）、OCR、音频等模型时，需上传本地文件并获取临时 URL；该功能由[上传本地文件获取临时URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md) 文档详细说明。
- **事件驱动通知**：为避免轮询开销，可配置 HTTP 回调或 RocketMQ 接收异步任务完成事件，详见[通过HTTP回调URL或MQ接收异步任务完成通知](raw/model-api-reference/more-about-models/async-task-api.md)。

> **注意**：文档 4 明确指出“文件上传时必须指定模型名称，且该模型须与后续调用的**模型一致**”，而文档 3 中子业务空间调用示例未强调此绑定关系。实际开发中，上传文件时指定的 `model_name` 必须与最终调用模型的名称完全一致，否则模型服务将拒绝请求。

## 关键参数

以下参数在模型调用链路中具有全局影响：

- **`expire_in_seconds`**：用于生成临时 API Key，取值范围 `[1, 1800]` 秒，默认 60 秒。该参数在[生成临时API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md) 中定义，适用于浏览器、App 等不可信环境。
- **`task_id`**：异步任务唯一标识，是查询、批量列表、取消操作的核心入参，所有异步任务接口均依赖此字段。
- **`X-DashScope-OssResourceResolve: enable`**：使用 `oss://` 形式临时 URL 调用模型时，**必须**在 HTTP 请求头中显式添加此 Header，否则请求将失败（见[上传本地文件获取临时URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)）。
- **连接池参数**（Java/Python SDK）：如 `connectionPoolSize`、`max_connections`、`keepalive_expiry` 等，直接影响高并发下的稳定性与延迟，需根据业务负载合理配置（见[DashScope SDK连接复用配置](raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)）。

## 使用方式

### 1. 安全调用（临时凭证）
在前端或移动端等不可信环境，禁止硬编码永久 API Key。应由后端服务调用 `/api/v1/tokens` 接口生成短期有效的临时 Key，并将其透传至客户端使用。

### 2. 子业务空间调用
需满足三要素：
- 使用该子空间创建的 API Key；
- 若调用标准模型，需在该空间[设置模型调用权限](https://help.aliyun.com/zh/model-studio/permission-management-overview#f642213a1f38l)；
- 正确配置地域专属域名（如 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`）或 OpenAI 兼容 `base_url`。

### 3. 多模态文件处理
- 调用 `POST /api/v1/uploads?action=getPolicy&model={model_name}` 获取上传策略；
- 使用策略向 OSS 上传文件，获得 `oss://...` 格式 URL；
- 在模型请求中传入该 URL，并确保 Header 包含 `X-DashScope-OssResourceResolve: enable`。

### 4. 异步任务全流程
- 提交任务 → 获取 `task_id`；
- （可选）配置事件总线规则，订阅 `dashscope:System:AsyncTaskFinish` 事件；
- 收到通知后，调用 `GET /api/v1/tasks/{task_id}` 查询结果；
- 或按需轮询（建议间隔 ≥1s，避免触发 20 QPS 限流）。

## 限制和注意事项

- **临时文件有效期严格为 48 小时**，且不可续期。文档 4 明确警告：“**请勿用于生产环境**”，生产环境应使用阿里云 OSS 等长期存储方案。
- **临时 API Key 无法手动删除**，仅能等待自动过期（见[生成临时API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)）。
- **异步任务数据保留期为 24 小时**（见[异步任务管理 API](raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)），超时后 `GET /api/v1/tasks/{task_id}` 将返回 `UNKNOWN` 状态。
- **文件上传限流为 100 QPS（按主账号+模型维度）**，且不支持扩容，高并发上传场景需自行实现队列与重试逻辑。
- **连接复用配置需匹配服务端承载能力**：Java SDK 的 `connectionPoolSize` 与 Python SDK 的 `max_connections` 均不宜盲目设高，否则可能触发服务端限流或资源争抢。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)


