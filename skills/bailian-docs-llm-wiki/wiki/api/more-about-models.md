# [more](more.md) about models

本文档汇总了百炼平台模型调用相关的进阶能力与配置项，涵盖异步任务管理、临时凭证生成、子空间调用、文件上传支持及连接复用等关键场景。开发者应结合具体业务需求选择合适的功能组合，并注意各功能的适用范围与约束条件。所有功能均通过标准 Model API 或 DashScope SDK 提供支持。

## 支持的模型/功能

当前支持以下扩展能力（均基于标准模型接口增强）：
- 生成临时 API Key，用于短期、受限的模型访问授权，适用于前端直连或第三方集成场景：[生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)  
- 管理长耗时任务（如大文件解析、批量推理），支持查询状态、取消与结果拉取：[管理异步任务](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)  
- 配置 HTTP 回调地址，由服务端在异步任务完成后主动推送结果：[配置异步任务回调](../../raw/model-api-reference/more-about-models/async-task-api.md)  
- 在子业务空间（Sub-Workspace）中调用模型，需显式指定 `workspace_id` 且权限独立：[子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)  
- 上传文件后获取带签名的临时 URL，供模型输入（如 `file://` 协议引用）：[上传文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)  
- 启用 DashScope SDK 的连接复用（HTTP/1.1 keep-alive 或 HTTP/2 multiplexing），降低建连开销：[DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `workspace_id` | string | 否（子空间调用时必填） | 指定目标子业务空间 ID；主空间调用时不可传，否则返回 403 |
| `enable_stream` | boolean | 否 | 仅同步接口支持；设为 `true` 时启用流式响应（SSE） |
| `callback_url` | string | 否（异步任务回调必需） | HTTPS 地址，需可被百炼服务端公网访问；参见 [配置异步任务回调](../../raw/model-api-reference/more-about-models/async-task-api.md) |
| `timeout` | integer | 否 | 单位秒，默认 60；异步任务最大支持 86400（24 小时） |
| `connection_pool_size` | integer | 否（SDK 专用） | DashScope SDK 中连接池大小，默认 10；详见 [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |

> **注意**：`workspace_id` 在同步调用中传入将导致鉴权失败；该行为与 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md) 文档一致，但部分旧版 SDK 示例代码未明确禁止，需以本页为准。

## 使用方式

- **同步调用扩展功能**：在请求体中添加对应字段（如 `callback_url` 会自动转为异步模式），无需额外路径变更。  
- **异步任务发起**：使用 `POST /api/v1/tasks`（非 `/api/v1/models/{model}/invoke`），响应含 `task_id`，后续通过 `GET /api/v1/tasks/{task_id}` 查询。  
- **SDK 调用**：启用连接复用需显式配置 `ConnectionPoolSize`（Python SDK）或 `maxConnectionsPerRoute`（Java SDK），参考 [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)。  
- **临时文件引用**：先调用文件上传接口获取 `temp_url`，再在模型请求中以 `{"file": "temp_url"}` 形式传入（部分多模态模型支持）。

## 限制和注意事项

- 异步任务最长保留 7 天，超时后 `task_id` 不可查；结果只保留一次，需及时拉取。  
- 临时 API Key 有效期最短 300 秒，最长 86400 秒，且不支持刷新；密钥泄露后无法主动吊销，仅能等待过期。  
- 子业务空间调用需确保当前 AK/SK 具备该 `workspace_id` 的 `ModelInvoke` 权限，否则返回 `403 Forbidden`。  
- 所有回调请求均携带 `X-DashScope-Signature` HTTP Header，用于校验来源真实性（签名算法见 [配置异步任务回调](../../raw/model-api-reference/more-about-models/async-task-api.md)）。  
- 连接复用配置仅对 SDK 生效，直接调用 HTTP 接口无此优化；若服务端未开启 HTTP/2 支持，复用效果受限。

## 来源文档

- [更多](../../raw/model-api-reference/more-about-models.md)


