# [more](more.md) about models

本文档汇总了百炼平台模型调用中进阶功能与关键配置项，涵盖异步任务管理、临时凭证生成、子空间隔离调用等核心能力，适用于需要精细化控制模型服务生命周期与资源访问的开发者场景。所有功能均通过标准 REST API 或 DashScope SDK 提供支持，无需额外开通权限。详细实现细节请参考对应子文档。

## 支持的模型/功能

- 生成临时 API Key：用于短期、受限的模型访问授权，适用于前端直连或第三方集成场景，有效期可精确控制至秒级。[生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)  
- 管理异步任务：支持长耗时模型调用（如大文件解析、批量推理）的提交、查询、取消与结果拉取。[管理异步任务](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)  
- 配置异步任务回调：通过 `callback_url` 指定 HTTP 回调地址，服务端在任务完成时主动推送结果，降低轮询开销。[配置异步任务回调](../../raw/model-api-reference/more-about-models/async-task-api.md)  
- 子业务空间的模型调用：支持在多租户环境下按 `workspace_id` 隔离模型调用上下文与配额，确保资源与计费归属准确。[子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)  
- 上传文件获取临时 URL：上传文件后返回带签名的临时访问链接，供模型输入（如 `file://` 协议）直接引用，避免客户端重复上传。[上传文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)  
- DashScope SDK 连接复用配置：通过 `connection_pool_size` 和 `keep_alive_timeout` 控制 HTTP 连接池行为，提升高并发调用下的吞吐与稳定性。[DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `workspace_id` | string | 否（默认主空间） | 指定子业务空间 ID，影响模型可见性、配额归属与审计日志归属 |
| `callback_url` | string | 否 | 异步任务完成时触发的 HTTPS 回调地址，需支持 POST，响应超时 ≤ 10s |
| `expires_in` | integer | 否（默认 3600） | 临时 API Key 有效期（秒），最小值为 60，最大值为 86400 |
| `file_type` | string | 是（仅上传文件时） | 文件 MIME 类型，如 `application/pdf`、`image/png`，必须与实际内容一致 |

> **注意**：`workspace_id` 在 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md) 中要求以请求头 `X-DashScope-Workspace-ID` 传递，而部分旧版 SDK 示例仍使用 query 参数方式，后者已不推荐且可能被拒绝。

## 使用方式

1. **同步调用**：直接向 `/v1/services/aigc/text-generation/generation` 等标准 endpoint 发起 POST 请求，适用于低延迟、短耗时场景。  
2. **异步调用**：  
   - 先调用 `/v1/tasks` 提交任务（含 `model`, `input`, `parameters`），获取 `task_id`；  
   - 可选配置 `callback_url` 实现服务端通知；  
   - 通过 `GET /v1/tasks/{task_id}` 查询状态，或等待回调。  
3. **SDK 调用**：使用 DashScope Python/Java SDK 时，启用连接复用需显式设置 `ConnectionPoolConfig`；临时 Key 生成需调用 `dashscope.api_key.generate_temp_api_key()` 方法。详情见 [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)。

## 限制和注意事项

- 临时 API Key 不支持刷新，过期后需重新生成；单次调用最多生成 10 个并发有效 Key。  
- 异步任务最长保留 7 天，超时未拉取的结果将被自动清理；回调失败重试策略为指数退避（最多 3 次）。  
- 上传文件临时 URL 有效期为 1 小时，且仅限模型服务内部访问，不可用于客户端直下载。  
- 所有异步任务回调必须使用 HTTPS，且服务端证书需由可信 CA 签发；自签名证书将导致回调失败。  
> **注意**：[配置异步任务回调](../../raw/model-api-reference/more-about-models/async-task-api.md) 文档中提到的 `callback_method=GET` 已废弃，当前仅支持 `POST`，且请求体为 JSON 格式，与文档早期版本描述不一致，请以最新 API Schema 为准。

## 来源文档

- [更多](../../raw/model-api-reference/more-about-models.md)


