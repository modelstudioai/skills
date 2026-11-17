# [more](more.md) about models

本文档面向开发者，系统介绍百炼平台模型调用的核心能力与工程实践要点，涵盖模型访问控制、[异步任务](../concepts/asynchronous-task.md)处理、文件上传、连接优化等关键环节。所有功能均基于 DashScope 服务层统一提供，适用于标准模型、微调模型及多模态任务。

## 支持的模型/功能

百炼支持多种模型调用模式：  
- **标准模型**（如 `qwen-plus`、`qwen3-vl-plus`）可通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或原生 DashScope SDK 调用，但需在子业务空间中[设置模型调用权限](raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)；  
- **微调模型**仅支持通过其所属业务空间的 API Key 调用，且不支持 OpenAI 兼容方式；  
- **多模态任务**（文生图、文生视频、语音转写等）默认采用异步机制，需配合[异步任务管理 API](raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) 或事件总线回调使用；  
- **临时文件上传**专为多模态输入设计，生成 `oss://` 前缀的临时 URL（有效期 48 小时），上传时必须指定目标模型名称，且文件与模型强绑定。

> **注意**：文档 4 中明确要求“文件上传时必须指定模型名称，且该模型须与后续调用的**模型一致**”，而文档 3 的 OpenAI 兼容调用示例未体现此约束。实际开发中，若使用 `qwen3-vl-plus` 模型上传图片，则后续请求的 `model` 参数必须严格匹配，不可混用 `qwen-plus` 等其他模型。

## 关键参数

| 参数 | 说明 | 示例值 | 来源 |
|------|------|--------|------|
| `DASHSCOPE_API_KEY` | 主账号或子业务空间的 API Key，用于身份认证 | `sk-xxx` | [配置API Key 到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables) |
| `WorkspaceId` | 业务空间唯一标识，用于构造地域专属 Endpoint | `wsp-abc123` | [获取业务空间 ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h) |
| `expire_in_seconds` | 临时 API Key 有效期，范围 `[1, 1800]` 秒 | `1800` | [生成临时API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `X-DashScope-OssResourceResolve: enable` | 使用 `oss://` URL 时必需的请求头 | 启用 OSS 资源解析 | [上传本地文件获取临时URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md) |

## 使用方式

### 1. 安全调用（前端/移动端）
在不可信环境（如浏览器、App）中，**禁止硬编码永久 API Key**。应由后端服务调用 `/api/v1/tokens` 接口生成临时 Key，并设置合理 TTL（推荐 ≤ 300 秒）。临时 Key 继承父 Key 的全部权限，包括模型访问限制。

### 2. [异步任务](../concepts/asynchronous-task.md)处理
- **轮询方案**：直接调用 `/api/v1/tasks/{task_id}`（限流 20 QPS），适用于低并发场景；  
- **事件驱动方案**：通过[事件总线配置 HTTP 回调或 RocketMQ](raw/model-api-reference/more-about-models/async-task-api.md)，任务完成后主动推送 `dashscope:System:AsyncTaskFinish` 事件，避免轮询资源消耗；  
- **批量管理**：使用 `/api/v1/tasks` 批量查询状态，支持按 `start_time`/`end_time`/`status`/`model_name` 筛选。

### 3. 多模态文件上传
调用 `POST https://dashscope.aliyuncs.com/api/v1/uploads?action=getPolicy&model={model_name}` 获取上传策略，再将文件 POST 至 OSS Host。生成的 `oss://` URL 必须在模型请求中显式传入，并添加请求头 `X-DashScope-OssResourceResolve: enable`。

### 4. 连接复用优化
- **Java SDK**：通过 `Constants.connectionConfigurations` 配置连接池（如 `connectionPoolSize=256`）；  
- **Python SDK**：传入自定义 `httpx.Client` 或 `httpx.AsyncClient`，设置 `limits=httpx.Limits(max_connections=100)`。

## 限制和注意事项

- **临时 Key 生命周期**：无法手动删除，到期自动失效，且不支持刷新；  
- **文件上传限流**：凭证接口按“主账号+模型”维度限流 100 QPS，**严禁用于生产环境或压测**，生产环境应使用 OSS 直传；  
- **地域隔离**：北京、新加坡、弗吉尼亚、中国香港四地 API Key 互不通用，Endpoint 和 `WorkspaceId` 必须匹配；  
- **[异步任务](../concepts/asynchronous-task.md)保留期**：任务结果默认保留 24 小时，超时后数据被清理，需及时拉取；  
- **子空间模型授权**：调用标准模型前，必须在子业务空间中[设置模型调用权限](https://help.aliyun.com/zh/model-studio/permission-management-overview#f642213a1f38l)，否则返回 `Forbidden` 错误；  
- **SDK 版本要求**：DashScope Python SDK ≥ `2.0.1`（文件上传）、Java SDK ≥ `2.12.0`（连接池配置），旧版本不支持关键特性。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)


