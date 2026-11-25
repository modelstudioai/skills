# managed agents api

Managed Agents API 是百炼平台提供的用于创建、配置和管理托管智能体（Managed Agent）的 RESTful 接口集合，支持从环境初始化、会话生命周期控制到技能编排、文件与记忆存储等全链路能力。该 API 采用标准 OAuth2 认证，所有资源均遵循 REST 设计规范，并通过统一错误码体系提供可预测的响应行为。开发者可通过 [原文标题](../../raw/application-api-reference/managed-agents-api.md) 查阅完整子模块索引。

## 支持的模型与功能

Managed Agents API **不直接绑定特定大模型**，而是通过 `agent` 资源中的 `model_id` 字段指定底层推理模型（如 `qwen-max`、`qwen-plus` 等），具体可用模型列表以 [原文标题](../../raw/application-api-reference/managed-agents-api.md) 中 `/agent` 接口文档为准。核心功能覆盖：
- Agent 生命周期管理（创建、更新、删除、发布）
- Environment 隔离配置（网络策略、资源限制、依赖注入）
- Session 与 Event 驱动交互（支持长连接 SSE 和短轮询）
- 文件上传/引用（支持 Base64 内联与对象存储 URI）
- Memory Store 的结构化记忆读写（键值 + 元数据过滤）
- Skill 组合调用（内置 HTTP、SQL、Python 执行器，支持自定义 Skill 注册）

> **注意**：部分旧版文档（如 `managed-agents-api-overview.md`）提及“默认使用 qwen-turbo”，但该描述已过时；实际模型由 `model_id` 显式指定，且必须在创建 Agent 时传入，参见 [原文标题](../../raw/application-api-reference/managed-agents-api.md) 中 `/agent` 接口定义。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_id` | string | 是 | 百炼平台已上线的模型 ID，例如 `qwen-max`；不可为空或留空字符串 |
| `environment_id` | string | 否 | 关联的 Environment ID；未指定则使用默认环境 |
| `session_id` | string | 否（仅 `/session` 接口） | 用于复用上下文的会话标识符，长度 ≤ 64 字符，仅含字母、数字、下划线、短横线 |
| `enable_memory` | boolean | 否 | 默认 `false`；设为 `true` 后自动启用 Memory Store 并关联当前 Agent |
| `webhook_url` | string | 否 | 事件回调地址，需为 HTTPS 协议，且须提前在 Vault 中注册可信域名 |

## 使用方式

1. **认证**：使用 `Authorization: Bearer <access_token>` 请求头，Token 通过 OAuth2 Client Credentials 流程获取（详见 [原文标题](../../raw/application-api-reference/managed-agents-api.md) 中 `/authentication` 文档）  
2. **创建 Agent**：`POST /v1/agents`，请求体包含 `name`、`model_id`、`description` 等字段  
3. **启动会话**：`POST /v1/agents/{agent_id}/sessions`，可选传入 `initial_context` 或 `file_ids`  
4. **流式调用**：对 `/v1/sessions/{session_id}/messages` 使用 `Accept: text/event-stream` 头，接收 SSE 响应  

所有接口均返回标准 JSON 响应，含 `request_id` 用于问题排查。

## 限制和注意事项

- 单个 Agent 最多关联 100 个 Skill；单次会话最多携带 10 个文件（总大小 ≤ 50MB）  
- Memory Store 单条记录最大 1MB，Key 长度 ≤ 128 字符，Value 长度 ≤ 10MB  
- Webhook 回调超时为 10 秒，失败后重试 2 次（间隔 1s），超过阈值将丢弃事件  
- `model_id` 必须与当前 Region 支持的模型严格匹配，不支持跨 Region 模型别名（如 `qwen-max-cn` 与 `qwen-max-us` 视为不同模型）  
- Agent 创建后需显式调用 `/deploy` 接口发布才可被会话调用；未部署状态下的调用将返回 `400 Bad Request`（错误码 `AGENT_NOT_DEPLOYED`）

## 来源文档

- [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md)


