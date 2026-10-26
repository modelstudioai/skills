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

所有写操作（如 `POST /v1/agents`）需在请求体中包含以下必需字段：  
- `name`: 字符串，长度 1–64，仅限字母、数字、下划线、短横线  
- `environment_id`: 关联的 Environment ID（必须已存在）  
- `model`: 指定模型 ID（例如 `"qwen-max"`），必须属于当前项目已开通的模型列表  
- `prompt_template`: Jinja2 格式字符串，支持 `{{ input }}`、`{{ memory.key }}` 等上下文变量  

读操作（如 `GET /v1/sessions/{session_id}`）支持通用查询参数：  
- `include_events=true`：返回关联的 `Event` 列表（默认 `false`）  
- `limit=50`：限制返回事件数（最大 200）  
- `offset=0`：分页偏移量  

详细参数说明见 [Agent API](../../raw/application-api-reference/managed-agents-api/agent-api.md) 与 [Session API](../../raw/application-api-reference/managed-agents-api/session-api.md)。

## 使用方式

1. **认证**：在 `Authorization` Header 中传入 `Bearer <access_token>`，[Token](../concepts/token.md) 通过 [认证文档](../../raw/application-api-reference/managed-agents-api/managed-agents-api-authentication.md) 获取  
2. **快速启动**：参考 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md) 中的 cURL 示例，完成 Agent 创建 → Session 启动 → 流式响应消费全流程  
3. **生产集成**：建议使用官方 SDK（Python/Node.js），自动处理重试、事件解析与错误码映射；避免手动拼接 `webhook_url` 或硬编码 `memory_store_id`

## 限制和注意事项

- 单个 Agent 最多绑定 20 个 Skill；单个 Session 最大存活时长为 24 小时（超时后 `memory` 自动清理）  
- `File` API 上传单文件上限 100 MB，且仅支持 `text/plain`, `application/json`, `application/pdf`, `image/*` 四类 MIME 类型  
- 所有 `POST /v1/webhooks` 创建的回调地址必须支持 HTTPS 且响应时间 < 3s，否则触发重试（最多 3 次）并标记为 `failed`  
- `Deployment` API 当前仅支持蓝绿发布模式，不支持金丝雀；回滚需显式调用 `POST /v1/deployments/{id}/rollback`  
- 错误响应统一遵循 [错误码规范](../../raw/application-api-reference/managed-agents-api/managed-agents-api-errors.md)，常见 `429 Too Many Requests` 表示超出环境级 QPS 限额（默认 10 QPS）

## 来源文档

- [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md)


