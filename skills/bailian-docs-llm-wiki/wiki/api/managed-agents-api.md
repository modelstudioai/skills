# managed agents api

Managed Agents API 是百炼平台提供的用于构建、部署和管理智能体（Agent）的 RESTful 接口集合，支持从环境配置、会话生命周期、技能编排到凭证与内存存储的全栈控制。该 API 采用标准 HTTP 协议，需通过 Bearer [Token](../concepts/token.md) 认证，适用于需要细粒度控制 Agent 行为的中高级开发者场景。详细设计原则与架构约束请参阅 [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md)。

## 支持的模型与功能

Managed Agents API **不直接调用大模型**，而是提供对 Agent 运行时基础设施的编排能力。其核心功能模块包括：
- `Agent`：定义 Agent 的行为逻辑、工具绑定与执行策略；
- `Environment`：隔离运行上下文（如 sandbox、prod），支持多版本并行部署；
- `Session` 和 `Event`：管理用户会话状态与事件驱动流程（如 `session.created`、`tool_executed`）；
- `Memory Store`：持久化短期记忆（如对话历史）与长期知识（需配合 Vault）；
- `Skill` 与 `Credential`：封装可复用的能力单元及安全凭据，支持 RBAC 级别授权。

所有模块均在 [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md) 的子页面中分项定义，例如 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md) 和 [Memory Store](../../raw/application-api-reference/managed-agents-api/memory-store-api.md)。

## 关键参数

请求必须携带以下通用头部：
- `Authorization: Bearer <token>`（认证方式详见 [Managed Agents API](../../raw/application-api-reference/managed-agents-api.md) 中的 [认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-authentication.md) 小节）；
- `X-App-ID: <app_id>`：标识所属应用，用于配额与审计；
- `Content-Type: application/json`（仅 `POST`/`PUT` 请求）。

部分端点要求必填路径参数（如 `/v1/agents/{agent_id}/sessions` 中的 `agent_id`）或查询参数（如 `?environment=staging`）。所有参数语义与示例均在对应子文档中明确定义，例如 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md) 明确了 `session_id` 的生成规则与幂等性保障。

> **注意**：原始文档中 `Environment` 接口的 `region` 字段在 v2.3+ 版本已弃用，实际应使用 `location`；该变更未同步更新至 [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md) 页面，开发者请以 OpenAPI Schema 为准。

## 使用方式

1. **初始化**：调用 `/v1/agents` 创建 Agent 实例，传入 `skills`、`memory_store_id` 等配置；
2. **启动会话**：向 `/v1/agents/{id}/sessions` 发送 `POST`，获取 `session_id`；
3. **交互**：向 `/v1/sessions/{session_id}/messages` 发送用户消息，接收结构化响应（含 `tool_calls`、`memory_updates` 等字段）；
4. **监控与调试**：通过 `/v1/sessions/{id}/events` 流式拉取事件日志，或调用 `/v1/deployments/{id}/logs` 查看部署级日志。

完整端到端流程见 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)，其中包含 cURL 与 Python SDK 示例。

## 限制和注意事项

- 单次 `messages` 请求最大输入长度为 32768 字符，超长内容需预处理切分；
- `Memory Store` 写入单条记录上限为 8KB，且 TTL 最小值为 300 秒；
- 所有 Webhook 回调必须在 5 秒内返回 `2xx`，否则视为失败并触发重试（最多 3 次）；
- Agent 配置变更（如更新 `skills`）需重新部署（`/v1/deployments`），**不支持热更新**；
- 错误响应统一遵循 [错误码](../../raw/application-api-reference/managed-agents-api/managed-agents-api-errors.md) 规范，常见如 `AGENT_NOT_FOUND (404)`、`SESSION_EXPIRED (410)`。

请始终参考 [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md) 主页获取最新目录结构与版本兼容性说明。

## 来源文档

- [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md)


