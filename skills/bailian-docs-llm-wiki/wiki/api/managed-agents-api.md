# managed agents api

Managed Agents API 是百炼平台提供的托管式智能体服务接口，用于创建、配置和管理具备长期记忆、工具调用、多步推理能力的自主运行 Agent。该 API 封装了环境隔离、会话生命周期、文件与凭证管理等底层复杂性，开发者可通过 RESTful 接口快速集成。其设计目标是降低构建生产级 Agent 应用的工程门槛，同时保障安全与可观测性。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款 Qwen 系列大模型；其他模型（如 `qwen2.5-*`）暂未开放给 Managed Agents 使用，相关限制详见 [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md)。
- **核心功能**：包括 Agent 实例生命周期管理（创建/更新/删除）、带状态的会话（Session）控制、结构化 Memory Store 持久化、沙箱化 Environment 配置、Skill 注册与编排、Vault 安全凭证注入，以及 Webhook 事件回调。完整能力矩阵可参考 [概览](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 关键参数

- `agent_id`（路径参数）：全局唯一标识符，由平台在创建时生成，不可自定义。
- `session_id`（请求头或 query 参数）：用于关联上下文，若未提供则自动新建会话；重复使用同一 `session_id` 可恢复历史 memory 与执行状态。
- `input`（JSON body）：必须为字符串类型（非对象），Agent 将其作为初始用户消息解析；若需传递结构化数据，请先序列化为 JSON 字符串。
- `tools`（可选数组）：指定启用的 Skill ID 列表，仅限已通过 [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md) 接口注册并绑定到该 Agent 的技能。

## 使用方式

1. **认证**：所有请求需携带 `Authorization: Bearer <access_token>`，Token 通过 OAuth2 流程获取，具体流程见 [认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-authentication.md)。
2. **发起调用**：向 `POST /v1/agents/{agent_id}/chat` 发送请求，Body 示例：
   ```json
   { "input": "请分析附件中的销售报表", "files": ["file_abc123"] }
   ```
3. **处理响应**：返回流式 SSE 或完整 JSON，含 `event` 类型字段（如 `"message"`、`"tool_use"`、`"error"`），需按 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md) 规范解析。

## 限制和注意事项

- 单次请求最大 `input` 长度为 32768 字符；上传文件单个不超过 100 MB，总大小不超过 500 MB/会话。
- Memory Store 默认保留最近 100 条交互记录，超出部分自动截断；如需定制容量，须在创建 Agent 时通过 `memory_config.max_entries` 指定（最高 1000）。
- > **注意**：原始文档中 [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md) 提到支持自定义 Docker 镜像，但该功能已于 v2.3.0 版本下线，当前仅允许使用平台预置的 `python3.11-sandbox` 和 `node18-sandbox` 运行时；最新约束以 [Deployment](../../raw/application-api-reference/managed-agents-api/deployment-api.md) 中的 `runtime` 字段说明为准。
- 文件上传后默认 7 天过期，且仅在所属会话内可被引用；跨会话复用需显式调用 `/files/{file_id}/copy`。

## 来源文档

- [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md)


