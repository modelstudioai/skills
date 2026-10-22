# managed agents api

Managed Agents API 是百炼平台提供的用于构建、部署和管理可编程智能体（Agent）的 RESTful 接口集合，支持环境隔离、会话状态管理、技能编排、文件与记忆存储等核心能力。该 API 采用标准 HTTP 协议，需通过 Bearer [Token](../concepts/token.md) 认证，适用于需要细粒度控制 Agent 生命周期与运行时行为的开发者场景。完整功能覆盖从开发调试到生产部署的全链路需求。

## 支持的模型与功能

Managed Agents API **不直接调用大模型**，而是提供对 Agent 运行时基础设施的编排能力；实际模型推理由 Agent 内部配置的 `model_id`（如 `qwen-max`、`qwen-plus`）在执行时动态触发。当前支持的功能模块包括：Agent 定义与部署、隔离式 Environment 管理、Session 生命周期控制、Event 驱动的异步交互、File 上传与引用、Memory Store 键值存储、Skill 组合复用、Vault 安全凭证托管、Credential 动态注入，以及 Webhook 事件回调。详细接口说明见 [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md) 的子章节导航。

## 关键参数

- `agent_id`：必填，全局唯一标识符，由创建 Agent 时返回，用于后续所有资源操作。
- `session_id`：会话级上下文标识，首次调用 `/v1/agents/{agent_id}/sessions` 时生成；同一 session 内的请求共享 memory 和 event history。
- `input`：JSON 对象，作为用户输入传入 Agent，结构由 Agent 的 input schema 定义（参见 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md) 文档）。
- `stream`：布尔值，默认 `false`；设为 `true` 时启用 Server-Sent Events (SSE) 流式响应，适用于长任务或实时反馈场景。
- `timeout`：整数，单位秒，最大支持 300 秒；超时后会话自动终止，相关 memory 可能被清理（具体行为请参考 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)）。

## 使用方式

1. **认证**：在 HTTP Header 中携带 `Authorization: Bearer <access_token>`，token 通过 [认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-authentication.md) 流程获取；
2. **创建 Agent**：`POST /v1/agents` 提交 YAML 或 JSON 格式的 Agent 定义（含 skills、memory config、model binding 等）；
3. **启动会话**：`POST /v1/agents/{agent_id}/sessions` 获取 `session_id`；
4. **发起交互**：`POST /v1/agents/{agent_id}/sessions/{session_id}/chat` 传入 `input`，根据 `stream` 参数选择同步或流式响应；
5. 其他资源（如 File、Memory Store、Webhook）均通过独立 endpoint 操作，全部路径统一以 `/v1/` 为前缀。

> **注意**：原始文档中 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md) 所示的 `curl -X POST ... --data-binary @agent.yaml` 示例未明确要求 `Content-Type: application/yaml`，但实测必须显式设置，否则返回 415 错误；此为文档过时项，请以实际 API 响应为准。

## 限制和注意事项

- 单个 Agent 最多绑定 20 个 Skill；超出将导致 `400 Bad Request`；
- Session 默认 TTL 为 60 分钟，无新请求则自动失效；memory store 数据在 session 过期后不可恢复；
- 文件上传大小上限为 100 MB，且仅支持 `text/*`, `application/json`, `application/pdf`, `image/*` 类型；
- Vault 中存储的凭证无法被跨 Agent 共享，每个 Agent 必须独立绑定 Credential 资源；
- 所有 API 均遵循百炼平台通用限流策略（默认 10 QPS / project），高并发场景需合理设计重试与降级逻辑。  
  更多错误码含义详见 [错误码](../../raw/application-api-reference/managed-agents-api/managed-agents-api-errors.md)。

## 来源文档

- [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md)


