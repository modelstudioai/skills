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

1. **初始化环境**：先调用 `/environments` 创建隔离环境（含模型配置、系统提示词模板）  
2. **注册技能**：向 `/skills` 提交 Webhook URL 或内置工具定义  
3. **创建 Agent**：POST `/agents`，关联环境与技能  
4. **启动会话**：POST `/sessions` 获取 `session_id`，再向 `/sessions/{id}/messages` 发送用户输入  
5. **监听事件（可选）**：通过 `/webhooks` 配置事件回调，或轮询 `/sessions/{id}/events`  

详细步骤见 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)，各子资源的完整接口定义参见对应文档（如 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)）。

## 限制和注意事项

- 单个 Agent 最多绑定 20 个 Skill；单个 Environment 下最多运行 100 个 Agent 实例  
- `Memory Store` 单条记录最大 1MB，Key 长度上限 256 字符  
- Session 事件流默认保留 24 小时，超时后不可查询（可通过 `keep_alive` 参数延长）  
- 所有[文件上传](../concepts/file-upload.md)（`/files`）必须经 `vault_id` 关联权限上下文，未授权 vault 将拒绝写入  
- 错误响应统一遵循 [错误码规范](../../raw/application-api-reference/managed-agents-api/managed-agents-api-errors.md)，常见如 `AGENT_ENV_NOT_FOUND (400)`、`SKILL_EXECUTION_TIMEOUT (504)`

## 来源文档

- [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md)


