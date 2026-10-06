# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的托管式智能体服务接口，用于创建、配置和运行具备[长期记忆](../concepts/memory.md)、工具调用、多步推理能力的自主 Agent。该 API 以 RESTful 形式提供，支持细粒度资源管理（如 Environment、Session、Memory Store 等），适用于构建客服助手、自动化工作流、数据分析师等生产级应用。详细设计与行为规范请参考 [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款 Qwen 系列大模型；不支持第三方模型或自定义模型权重。
- **核心功能**：
  - 多轮 Session 管理与事件流订阅（见 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)）
  - 基于 Vault 的敏感凭证安全存储与动态注入
  - 可插拔 Skill（如 HTTP 调用、数据库查询、文件解析）注册与编排
  - 持久化 Memory Store（支持向量+结构化混合检索）
  - 环境隔离（Environment）实现配置、技能、记忆的逻辑分组  
  > **注意**：[Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md) 文档中提及的“跨环境共享 Memory Store”功能尚未上线，实际调用将返回 `400 UnsupportedOperation`，请以 [Memory Store](../../raw/application-api-reference/managed-agents-api/memory-store-api.md) 文档的当前约束为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `agent_id` | string | 是 | Agent 实例唯一标识，由 `/agent` 接口创建后返回 |
| `session_id` | string | 否 | 显式指定会话 ID；若省略，API 自动创建新会话 |
| `stream` | boolean | 否 | 默认 `false`；设为 `true` 时返回 SSE 流式响应（仅限 `/session/{id}/chat`） |
| `tool_choice` | string \| object | 否 | 控制工具调用策略，可选 `"auto"`、`"none"` 或指定 [skill](../guides/skill.md) ID；详见 [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md) |
| `max_steps` | integer | 否 | 单次请求最大执行步数，默认 15，上限 50 |

## 使用方式

1. **初始化 Agent**：先调用 `POST /v1/agents` 创建 Agent 配置（含 model、[skill](../guides/skill.md)s、memory_store_id 等）；
2. **启动会话**：使用返回的 `agent_id` 调用 `POST /v1/sessions` 获取 `session_id`；
3. **交互**：向 `POST /v1/sessions/{session_id}/chat` 发送用户消息，支持携带 `files`（通过 `/files` 上传后引用 ID）；
4. **状态监听**：通过 `GET /v1/sessions/{id}/events` 或 Webhook（需提前配置 [Webhook](../../raw/application-api-reference/managed-agents-api/webhook-api.md)）接收事件（如 `tool_call_started`, `memory_updated`）。

## 限制和注意事项

- 单个 Agent 最多绑定 20 个 Skill；单个 Session 最大上下文长度为 32k tokens（含系统提示、历史、工具结果）；
- 文件上传（`/files`）单次最大 100MB，支持格式：`.txt`, `.pdf`, `.docx`, `.xlsx`, `.csv`, `.json`；
- Memory Store 写入延迟通常 < 500ms，但强一致性读（`/memory/{id}/query?consistency=strong`）可能增加 200–800ms 延迟；
- 所有资源（Agent、Session、File 等）默认保留 30 天，过期后自动清理；如需长期保留，请在创建时显式设置 `ttl_seconds`（最大 31536000，即 1 年）；
- **重要**：`/deployment` 接口当前仅支持 `status: "draft"` 和 `"active"` 两种状态，`"inactive"` 状态虽在 [Deployment](../../raw/application-api-reference/managed-agents-api/deployment-api.md) 文档中列出，但实际调用将被拒绝。

## 来源文档

- [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)


