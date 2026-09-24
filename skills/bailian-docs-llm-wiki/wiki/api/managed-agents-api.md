# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的托管式智能体服务接口，用于创建、配置和运行具备长期[记忆](../concepts/memory.md)、工具调用、多步推理能力的 AI Agent。该 API 将底层基础设施（如环境隔离、状态持久化、凭证管理）抽象为标准化资源，开发者可聚焦于 Agent 行为逻辑设计。所有核心能力均通过 RESTful 接口暴露，并支持细粒度权限控制。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款大模型；其他模型（如 `qwen2.5-*` 系列）暂未接入 Managed Agents 运行时，调用将返回 `400 UnsupportedModel` 错误。  
- **核心功能模块**包括：Agent 定义与执行、沙箱化 Environment 配置、Session 生命周期管理、结构化 Memory Store、文件上传与引用、Skill 编排、Vault 加密凭证存储、Deployment 版本发布及 Webhook 事件回调。完整能力清单详见 [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)。

## 关键参数

- `agent_id`（路径参数）：全局唯一标识符，由平台生成或用户指定（需符合 `^[a-z0-9]([a-z0-9\-]{0,61}[a-z0-9])?$` 正则）。
- `session_id`（请求头或 body）：用于关联会话上下文；若未提供，系统自动创建新会话；同一 `session_id` 下的多次调用共享 Memory Store 与 Environment 状态。
- `tools`（body 字段）：JSON 数组，声明启用的 Skill 列表，格式为 `{"type": "retrieval", "name": "doc_search"}`；不支持自定义工具函数注册，仅限平台预置 Skill，详情见 [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)。
- `memory_store`（body 可选）：指定 Memory Store ID；若未指定，使用 Agent 默认 Memory Store；跨 Agent 共享 Memory Store 需显式授权，否则返回 `403 Forbidden`。

## 使用方式

1. **初始化 Agent**：`POST /v1/agents` 创建 Agent 实例，传入 `model`, `instructions`, `tools` 等字段；响应中返回 `agent_id`。  
2. **启动会话**：`POST /v1/agents/{agent_id}/sessions` 创建会话，可携带初始 `input` 和 `files`（需先通过 [File](../../raw/application-api-reference/managed-agents-api/files-api.md) 接口上传）。  
3. **流式执行**：`POST /v1/agents/{agent_id}/sessions/{session_id}/run` 发起推理，设置 `Accept: text/event-stream` 获取 SSE 流；每步输出含 `event: step_completed`、`event: tool_call` 等类型。  
4. **状态查询**：`GET /v1/agents/{agent_id}/sessions/{session_id}` 获取会话快照，含 `memory_store_usage` 和 `tool_calls_history`。

> **注意**：文档 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 中提及的 `X-Bailian-Region` 请求头已废弃，实际认证仅依赖 `Authorization: Bearer <token>` 和 `Content-Type: application/json`；请以 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md) 中的 curl 示例为准。

## 限制和注意事项

- 单次 `run` 请求最大 token 输入限制为 32768（含 system [prompt](../guides/prompt.md) + history + input），超限返回 `413 Payload Too Large`。  
- Session 默认 TTL 为 24 小时，过期后 `memory_store` 数据仍保留 7 天，但不可再关联新会话；如需长期状态，须主动调用 `PATCH /v1/memory-stores/{id}` 更新 TTL。  
- Environment 沙箱内禁止访问公网（除白名单 Skill 所需的 API Endpoint 外），且不支持 `fork()` 或子进程创建；违反将导致 `500 Internal Error` 并终止会话。  
- Vault 中存储的凭证仅在 Skill 执行时解密注入环境变量，不会出现在任何日志或 API 响应中；但若 Agent 代码中显式 `print(os.environ['SECRET_KEY'])`，该值可能被[流式输出](../concepts/streaming-output.md)泄露——务必在 [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md) 配置中启用 `mask_in_logs: true`。

## 来源文档

- [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)


