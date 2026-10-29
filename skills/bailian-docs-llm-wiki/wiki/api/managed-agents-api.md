# managed agents api

Managed Agents API 是百炼平台提供的用于构建、部署和管理可编程智能体（Agent）的 RESTful 接口集合，支持环境隔离、会话状态管理、技能编排、文件与记忆存储等核心能力。该 API 采用标准 HTTP 协议，需通过 Bearer [Token](../concepts/token.md) 认证，适用于需要细粒度控制 Agent 生命周期与运行时行为的开发者场景。完整功能覆盖从开发调试到生产部署的全链路需求。

## 支持的模型与功能

Managed Agents API **不直接调用大模型**，而是提供对 Agent 运行时基础设施的编排能力；底层模型由用户在 `Agent` 配置中指定（如 `qwen-max`、`qwen-plus` 等），并受 [Managed Agent API 概览](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 中定义的模型兼容性约束。支持的核心功能包括：  
- Agent 实例的创建、更新与生命周期管理（含 `status` 查询与强制终止）  
- 独立 `Environment` 隔离（支持多租户、多版本配置）  
- 基于 `Session` 的有状态交互与事件流订阅（`event_type=agent_step`, `agent_finish`）  
- `Memory Store` 提供结构化记忆持久化（键值对 + TTL）  
- `Skill` 注册与动态绑定（支持 HTTP Webhook 和内置工具）  
- `Vault` 与 `Credential` 安全管理敏感凭证  

> **注意**：文档中提及的 `qwen-turbo` 在最新版平台中已下线，实际可用模型请以 [Managed Agent API 概览](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 的 `supported_models` 字段为准，避免使用已废弃标识符。

## 关键参数

所有写操作（如 `POST /v1/agents`）必须包含以下标头：  
- `Authorization: Bearer <access_token>`（参见 [认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-authentication.md)）  
- `Content-Type: application/json`  

关键请求体字段示例：  
- `agent.runtime.model`: 必填，指定基础模型 ID（如 `"qwen-plus"`）  
- `environment.id`: 可选，显式绑定环境；未指定则使用默认环境  
- `session.ttl_seconds`: 控制会话自动过期时间（默认 3600，最大 86400）  
- `memory_store.enabled`: 布尔值，启用后自动挂载内存存储实例  

## 使用方式

1. **快速验证**：参考 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md) 中的 `curl` 示例，完成 Agent 创建 → Session 启动 → 消息发送三步流程  
2. **生产集成**：建议使用官方 SDK（Python/Node.js），自动处理重试、鉴权与事件解析  
3. **事件驱动开发**：通过 `POST /v1/webhooks` 注册回调地址，监听 `agent_step` 事件实现自定义日志或审计  

## 限制和注意事项

- 单个账户最多创建 100 个 Agent 实例，单个 Environment 最多承载 50 个并发 Session  
- `File` API 仅支持上传 `< 100MB` 的文本类文件（`.txt`, `.json`, `.csv`, `.pdf`），且 PDF 解析依赖异步 OCR，延迟约 2–10 秒  
- 所有 `Credential` 存储内容均经 KMS 加密，但 `vault` 中的明文字段（如 `description`）不加密，请勿存放敏感信息  
- `Deployment` 接口仅支持蓝绿发布模式，回滚需显式调用 `/v1/deployments/{id}/rollback`，不可自动触发  

> **注意**：`Session` 的 `max_steps` 默认为 50，但部分旧版文档误标为 100；实际生效值以 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md) 中 `limits.max_steps` 的最新定义为准。

## 来源文档

- [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md)


