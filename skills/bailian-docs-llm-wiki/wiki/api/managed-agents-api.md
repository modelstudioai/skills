# managed agents api

Managed Agents API 是百炼平台提供的托管式智能体服务接口，用于创建、配置和运行具备[长期记忆](../concepts/long-term-memory.md)、工具调用、多步推理能力的 AI Agent。该 API 封装了环境管理、会话生命周期、文件与凭证安全存储、技能编排等核心能力，开发者无需自行维护底层基础设施。所有接口均需通过 OAuth 2.0 认证，并遵循统一的 RESTful 设计规范。

## 支持的模型与功能

- **模型支持**：当前仅支持 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款 Qwen 系列大模型作为 Agent 的推理引擎；其他模型（如 `qwen-vl` 或第三方模型）暂未开放接入。  
- **核心功能模块**包括：Agent 实例管理、隔离式 Environment 配置、Session 生命周期控制、结构化 Memory Store、基于 YAML 的 Skill 定义、加密 Vault 存储、细粒度 Credential 绑定，以及 Webhook 事件回调。完整能力清单详见 [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md) 的子目录导航。

## 关键参数

- `agent_id`（路径参数）：全局唯一标识符，由平台在创建时生成，不可自定义。  
- `session_id`（请求体或查询参数）：用于关联用户上下文，若未提供则自动创建新会话；重复使用同一 `session_id` 可延续 Memory Store 中的历史状态。  
- `tool_choice`（可选）：指定工具调用策略，取值为 `"auto"`（默认）、`"none"` 或具体工具名（如 `"web_search"`），详见 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md) 接口文档。  
- `memory_ttl_seconds`（可选）：Memory Store 条目的存活时间，默认 `3600` 秒（1 小时），最大支持 `86400` 秒（24 小时）。

## 使用方式

1. 通过 `POST /v1/agents` 创建 Agent 实例，传入 `name`、`description`、`model` 及初始 `skills` 列表；  
2. 调用 `POST /v1/agents/{agent_id}/sessions` 启动会话，获取 `session_id`；  
3. 使用 `POST /v1/agents/{agent_id}/sessions/{session_id}/chat` 发送用户消息，Agent 自动调度工具、检索 Memory 并流式返回响应；  
4. 所有资源操作（如上传文件、绑定凭证）均通过对应子资源接口完成，例如文件上传需调用 `/v1/agents/{agent_id}/files`。快速上手流程请参考 [Managed Agents Quickstart](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)。

## 限制和注意事项

- 单个 Agent 最多绑定 50 个 Skill，单次会话中 Memory Store 总容量上限为 10 MB；  
- Session 默认有效期为 24 小时，超时后关联的 Memory 和临时文件将被自动清理；  
- > **注意**：[Managed Agents API Overview](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 中提及的 “支持自定义 LLM adapter” 属于已下线功能，当前版本不支持外部模型接入，以 [Agent API](../../raw/application-api-reference/managed-agents-api/agent-api.md) 文档中 `model` 字段的枚举值为准；  
- Webhook 事件投递最多重试 3 次，失败后不再重发，建议业务侧实现幂等处理；  
- 所有敏感操作（如 `DELETE /vaults/{id}`）均需显式启用 `X-Bailian-Confirm: true` 请求头，否则返回 `400 Bad Request`。

## 来源文档

- [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md)


