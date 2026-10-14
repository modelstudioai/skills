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

1. **快速验证**：参考 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md) 中的 cURL 示例，完成 Agent 创建 → Session 启动 → 发送消息三步流程  
2. **生产集成**：建议使用官方 SDK（Python/Node.js）封装 `Session` 生命周期与 `Event` 流解析逻辑，避免手动处理 SSE 连接重试  
3. **调试技巧**：启用 `debug: true` 参数可返回 `agent_step` 事件中的中间推理链（仅限非生产环境）

## 限制和注意事项

- 单个 `Session` 最长存活 24 小时，超时后自动清理关联 `Memory Store` 条目  
- `File` API 上传单文件上限为 100 MB，且仅支持 `text/plain`, `application/json`, `application/pdf`, `text/csv` 四类 MIME 类型  
- `Deployment` API 不支持灰度发布，每次 `deploy` 为全量覆盖；回滚需调用历史 `deployment_id` 重新部署  
- 所有 API 均遵循 429 限流策略：默认 100 QPS / 租户，突发流量需预申请配额  

> **注意**：`Webhook` API 的 `timeout_ms` 最小值已从 5000ms 调整为 3000ms（v2.4+），旧文档中未同步更新；详见 [Webhook API](../../raw/application-api-reference/managed-agents-api/webhook-api.md) 的 `request_config` 字段说明。

## 来源文档

- [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md)


