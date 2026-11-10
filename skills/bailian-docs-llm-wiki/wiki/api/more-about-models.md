# [more](more.md) about models

本文档汇总了百炼平台模型调用相关的进阶能力与配置项，涵盖[异步任务](../concepts/asynchronous-task.md)管理、临时凭证生成、子空间调用、文件上传支持及连接复用等关键场景。开发者应结合具体业务需求选择合适的能力组合，并注意各功能的适用范围与约束条件。所有能力均通过标准 Model API 或配套 SDK 提供。

## 支持的模型/功能

当前支持以下扩展功能（均基于标准模型接口增强）：
- 生成临时 API Key，用于短期、受限的模型访问授权，适用于前端直连或第三方集成场景：[生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)  
- 管理长耗时模型调用的[异步任务](../concepts/asynchronous-task.md)生命周期（提交、查询、取消、结果拉取）：[管理异步任务](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)  
- 配置[异步任务](../concepts/asynchronous-task.md)完成后的 HTTP 回调通知，避免轮询：[配置异步任务回调](../../raw/model-api-reference/more-about-models/async-task-api.md)  
- 在子业务空间（Sub Workspace）中调用模型，需显式指定 `workspace_id` 和权限上下文：[子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)  
- 上传文件并获取带签名的临时 URL，供多模态模型（如 Qwen-VL）直接引用：[上传文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)  
- 通过 DashScope SDK 启用 HTTP/2 连接复用，显著降低高并发下的建连开销：[DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `workspace_id` | string | 否（子空间调用时必填） | 指定目标子业务空间 ID；主空间调用可省略 |
| `api_key` | string | 否（推荐使用临时 Key） | 若使用长期 Key，需确保其具备对应模型和子空间权限 |
| `callback_url` | string | 否（异步回调必需） | HTTPS 协议，需可公网访问；回调体格式见 [配置异步任务回调](../../raw/model-api-reference/more-about-models/async-task-api.md) |
| `enable_stream` | boolean | 否 | 仅同步接口支持；设为 `true` 时返回 SSE 流式响应 |
| `connection_pool_size` | integer | 否（SDK 专用） | DashScope SDK 中设置最大复用连接数，默认 10；详见 [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |

> **注意**：部分旧版文档中提及 `x-dashscope-workspace` 请求头用于子空间调用，但自 v2.3.0 起已统一要求通过 `workspace_id` 字段传参，请求头方式已被废弃，请以 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md) 中的最新示例为准。

## 使用方式

- **同步调用**：直接向 `/api/v1/services/aigc/text-generation/generation` 等标准路径发送 POST 请求，附加 `workspace_id`（如需）、`model`、`input` 等字段。  
- **异步调用**：将请求路径中的 `generation` 替换为 `async-generation`，响应中返回 `task_id`；后续通过 `/async-tasks/{task_id}` 查询状态或等待回调。  
- **临时 Key 集成**：先调用 `/api/v1/auth/clients/temporary-api-keys` 获取 `api_key` 和 `expires_at`，再将其用于后续模型请求（有效期通常 ≤ 1 小时）。  
- **文件上传流程**：先调用 `/api/v1/files/upload` 获取临时 URL 和 `file_id`，再在模型 `input` 中以 `{"image_url": "https://..."}` 形式引用该 URL。

## 限制和注意事项

- 临时 API Key 单次最多生成 10 个，且总有效期不可超过 24 小时；过期后需重新申请。  
- 异步任务默认最长保留 7 天，超时未拉取结果则自动清理；回调失败重试上限为 3 次，间隔 1s/5s/15s。  
- 子业务空间调用模型时，若 `workspace_id` 不存在或无权限，将返回 `403 Forbidden`，而非 `404`。  
- 上传文件的临时 URL 有效期为 1 小时，且仅限百炼平台内模型服务访问，不可用于客户端直下载。  
- 连接复用仅在 DashScope SDK 的 `SyncClient` 和 `AsyncClient` 中生效；原生 HTTP 客户端需自行实现连接池。  

> **注意**：[上传文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) 文档中示例使用的 `POST /v1/files` 路径已更新为 `POST /api/v1/files/upload`，旧路径将于下个大版本下线，请及时迁移。

## 来源文档

- [更多](../../raw/model-api-reference/more-about-models.md)


