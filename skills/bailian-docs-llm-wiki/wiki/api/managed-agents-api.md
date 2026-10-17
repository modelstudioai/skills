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

> **注意**：原始文档中 `skills-api.md` 描述的“本地 Python 函数注册”能力已在 v2.3 版本中移除，当前仅支持 Webhook 类型 Skill；请以 [Skill API](../../raw/application-api-reference/managed-agents-api/skills-api.md) 的最新修订版为准。

## 关键参数

所有 POST/PUT 请求需包含以下必需 Header：  
- `Authorization: Bearer <token>`（参见 [认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-authentication.md)）  
- `Content-Type: application/json`  

关键请求体字段示例（以创建 Agent 为例）：  
```json
{
  "name": "customer-support-agent",
  "model": "qwen-plus",
  "environment_id": "env-prod-789",
  "skills": ["skill-ticket-create", "skill-kb-search"],
  "memory_store": { "ttl_seconds": 3600 }
}
```
其中 `environment_id` 必须已存在（通过 `/environments` 创建），`skills` 列表中的 ID 需提前在 `/skills` 中注册。

## 使用方式

1. **快速验证**：参考 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md) 文档，使用 `curl` 或 Postman 调用 `/agents` 创建首个 Agent 并发起会话  
2. **集成开发**：调用 `/sessions` 创建会话后，向 `POST /sessions/{session_id}/messages` 发送用户消息，接收流式响应（SSE）或轮询 `GET /sessions/{session_id}` 获取状态  
3. **生产部署**：通过 `/deployments` 创建灰度/全量部署，结合 `/webhooks` 配置事件回调（如 `agent_finish` 后触发 CRM 更新）  

所有资源路径均遵循 `/v1/{resource}` 格式（如 `/v1/agents`, `/v1/files`），版本号不可省略。

## 限制和注意事项

- 单个 Agent 最多绑定 20 个 Skill；单次会话最大上下文长度为 32K tokens（含系统提示、历史消息、Memory 内容）  
- `Memory Store` 键名仅支持 ASCII 字母、数字及 `-` `_` `.`，长度 ≤ 128 字符；值大小上限 1MB  
- 文件上传（`/files`）仅支持 `multipart/form-data`，单文件 ≤ 50MB，且仅在 `session` 生命周期内有效（除非显式调用 `/files/{file_id}/pin`）  
- 所有 API 均有速率限制：默认 100 QPS / 租户，突发容量 500；超出将返回 `429 Too Many Requests`（详见 [错误码](../../raw/application-api-reference/managed-agents-api/managed-agents-api-errors.md)）  
- `Credential` 的 `secret_value` 仅在创建时返回一次，后续无法读取，务必妥善保存

## 来源文档

- [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md)


