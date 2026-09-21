# [more](more.md) about models

本文档汇总了百炼平台模型调用相关的进阶能力与配置项，涵盖异步任务管理、安全凭证生成、子空间隔离调用等关键场景。适用于需要精细化控制模型请求生命周期、提升调用效率或满足多租户隔离需求的开发者。所有功能均通过标准 Model API 或 DashScope SDK 提供支持。

## 支持的模型/功能

当前支持以下扩展能力（不依赖具体模型类型，适用于所有已接入的 LLM、Embedding、Multimodal 等模型）：
- 生成临时 API Key，实现细粒度权限控制与短期凭证分发：[生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)  
- 异步任务提交与状态轮询，适用于长耗时推理（如大文件解析、批量生成）：[管理异步任务](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)  
- 配置 HTTP 回调地址，由服务端主动推送异步任务完成事件：[配置异步任务回调](../../raw/model-api-reference/more-about-models/async-task-api.md)  
- 在子业务空间（sub-workspace）内独立调用模型，实现资源与配额隔离：[子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)  
- 上传文件并获取带签名的临时访问 URL，用于多模态模型输入（如图像、PDF）：[上传文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)  

> **注意**：[DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) 中描述的 `connection_pool_size` 参数在 v3.12.0+ SDK 中已默认启用连接复用，旧版文档中需手动配置的说明已过时，请以 [管理异步任务](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) 中的 SDK 初始化示例为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `task_group_id` | string | 否 | 异步任务分组标识，用于批量查询与清理；建议按业务维度设置 |
| `callback_url` | string | 否（启用回调时必填） | HTTPS 地址，需支持 POST，接收 JSON 格式回调事件；详见 [配置异步任务回调](../../raw/model-api-reference/more-about-models/async-task-api.md) |
| `workspace_id` | string | 否（子空间调用时必填） | 子业务空间 ID，必须与请求 Header 中 `X-DashScope-Workspace` 一致 |
| `expires_in` | integer | 否（临时 Key 场景） | 临时 API Key 有效期（秒），范围 60–86400，默认 3600 |

## 使用方式

1. **异步调用流程**：发送 `POST /api/v1/services/aigc/text-generation/generation`（含 `"async": true`）→ 获取 `task_id` → 轮询 `GET /api/v1/tasks/{task_id}` 或监听回调  
2. **子空间调用**：在请求 Header 中显式添加 `X-DashScope-Workspace: <workspace_id>`，且模型名称前缀需为 `workspace/<workspace_id>/`（如 `workspace/ws-abc123/qwen-max`）  
3. **临时文件接入**：先调用文件上传接口获取 `file_url`，再将该 URL 作为 `input.file_url` 字段传入多模态模型请求  

## 限制和注意事项

- 单个异步任务最大执行时长为 10 分钟（超时自动终止），超时后无法续跑；如需更长处理时间，请拆分为多个子任务  
- 临时 API Key 不可刷新，过期后需重新生成；不支持撤销，仅能等待自然失效  
- 子业务空间调用要求调用方具备该 workspace 的 `model:invoke` 权限，否则返回 `403 Forbidden`  
- 所有回调请求均携带 `X-DashScope-Signature` 签名头，**必须校验**以防范伪造（签名算法见 [配置异步任务回调](../../raw/model-api-reference/more-about-models/async-task-api.md)）

## 来源文档

- [更多](../../raw/model-api-reference/more-about-models.md)


