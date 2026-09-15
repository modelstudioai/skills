# [more](more.md) about models

本文档汇总了百炼平台模型服务的进阶能力与管理接口，涵盖模型调用扩展功能、权限与配额控制、异步任务处理及 SDK 高级配置等核心场景。面向需要精细化管控模型访问、集成文件处理或构建高并发服务的开发者。所有功能均通过 REST API 或 DashScope SDK 提供支持。

## 支持的模型/功能

- 模型元数据查询：支持通过 [查询模型列表](../../raw/model-api-reference/more-about-models/list-models.md) 获取当前可用模型及其版本、输入/输出格式等基础信息  
- 权限与配额管理：可细粒度查看和更新子业务空间下的模型调用权限（[查询模型授权](../../raw/model-api-reference/more-about-models/list-model-permissions.md)、[更新模型授权](../../raw/model-api-reference/more-about-models/update-model-permissions.md)）及速率限制（[查询模型限流](../../raw/model-api-reference/more-about-models/list-quotas.md)、[更新模型限流](../../raw/model-api-reference/more-about-models/update-model-rate-limits.md)）  
- 异步任务支持：适用于长耗时推理（如视频理解、大文档摘要），含任务提交、状态轮询与回调配置（[管理异步任务](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)、[配置异步任务回调](../../raw/model-api-reference/more-about-models/async-task-api.md)）  
- 文件协同能力：支持上传文件并获取临时可访问 URL，用于多模态模型输入（[上传文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)）  
- 安全凭证管理：支持按需生成短期有效的临时 API Key，降低密钥泄露风险（[生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)）  
- 连接优化：DashScope SDK 支持连接复用与超时重试策略配置，提升高并发调用稳定性（[DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)）

## 关键参数

- `workspace_id`：必需，指定主工作空间或子业务空间 ID；子空间调用需配合 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md) 文档确认路径与鉴权逻辑  
- `model`：必需，模型标识符（如 `qwen-max`），必须与 [查询模型列表](../../raw/model-api-reference/more-about-models/list-models.md) 返回的 `model_name` 严格一致  
- `async`：布尔值，启用异步模式时设为 `true`，此时响应体返回 `task_id` 而非直接结果  
- `callback_url`：异步回调地址，需为 HTTPS 协议且可通过公网访问；其签名验证机制详见 [配置异步任务回调](../../raw/model-api-reference/more-about-models/async-task-api.md)  
- `file_url`：多模态请求中引用的临时文件地址，须由 [上传文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) 接口生成，有效期默认 1 小时  

## 使用方式

1. **同步调用**：直接向 `/api/v1/services/aigc/text-generation/generation` 等标准端点发送 POST 请求，传入 `model`、`input` 等字段  
2. **异步调用**：在请求体中设置 `"async": true`，收到 `task_id` 后，轮询 `/api/v1/tasks/{task_id}` 或配置 `callback_url` 接收推送  
3. **子空间调用**：在请求 Header 中添加 `X-DashScope-Workspace: <sub_workspace_id>`，并确保已通过 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md) 完成模型授权  
4. **SDK 集成**：使用 DashScope Python/Java SDK 时，通过 `dashscope.Config(..., connection_pool_size=10)` 等参数启用连接复用（参考 [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)）

## 限制和注意事项

- 临时 API Key 有效期最长为 24 小时，且不继承主密钥的全部权限；生成后无法续期，需重新调用 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)  
- 异步任务状态保留时间为 7 天，超时后 `task_id` 不再可查；回调失败重试策略为指数退避（最多 3 次），需确保 `callback_url` 服务具备幂等性  
- > **注意**：[查询模型限流](../../raw/model-api-reference/more-about-models/list-quotas.md) 返回的 `max_requests_per_minute` 是账户级硬限流，而子业务空间的 `update-model-rate-limits` 接口仅能设置软限流（即配额分配上限），实际触发限流仍以账户级为准  
- > **注意**：[子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md) 文档中提及的 `X-DashScope-Sub-Workspace` Header 已于 v2.3.0 版本废弃，当前统一使用 `X-DashScope-Workspace`，旧文档未及时更新，请以本页说明为准  
- 文件临时 URL 仅支持百炼平台内生文件服务，不支持外部 URL 直接传入；上传后需等待 `status: "success"` 才可安全用于模型请求

## 来源文档

- [更多](../../raw/model-api-reference/more-about-models.md)


