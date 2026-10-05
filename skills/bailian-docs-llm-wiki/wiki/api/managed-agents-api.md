# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的托管式智能体服务接口，用于创建、配置和运行具备[长期记忆](../concepts/memory.md)、工具调用、多步推理能力的 AI Agent。该 API 以 RESTful 形式提供，支持细粒度的生命周期管理与环境隔离，适用于构建客服助手、自动化工作流、数据分析师等生产级应用。所有资源均通过统一的 `https://dashscope.aliyuncs.com/api/v1/agents` 基路径访问。

## 支持的模型与功能

- **模型支持**：当前仅支持 `qwen-max` 和 `qwen-plus` 作为底层推理模型；`qwen-turbo` 因上下文长度与工具调用能力限制，**不支持**用于 Managed Agents（详见 [Agent](raw/application-api-reference/managed-agents-api/agent-api.md) 文档）。
- **核心功能**：
  - 多轮 Session 管理与事件流订阅（[Session and Event](raw/application-api-reference/managed-agents-api/session-api.md)）
  - 持久化 Memory Store（支持向量检索与结构化元数据过滤）
  - 文件上传与内容解析（PDF/DOCX/CSV 等，见 [File](raw/application-api-reference/managed-agents-api/files-api.md)）
  - 技能（Skill）编排与 Vault 加密凭证注入（[Skill](raw/application-api-reference/managed-agents-api/skills-api.md)、[Vault](raw/application-api-reference/managed-agents-api/vault-api.md)）

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model_id` | string | 是 | 必须为 `qwen-max` 或 `qwen-plus`；其他模型将返回 `400 Bad Request` |
| `environment_id` | string | 否 | 指定运行环境；未指定时使用默认环境（[Environment](raw/application-api-reference/managed-agents-api/environment-api.md)） |
| `memory_store_id` | string | 否 | 绑定已有 Memory Store；若为空则自动创建临时 store（不持久化） |
| `enable_streaming` | boolean | 否 | 默认 `false`；设为 `true` 时响应为 SSE 流，需处理 `event: token` 格式 |

> **注意**：`system_prompt` 字段在 [Agent](raw/application-api-reference/managed-agents-api/agent-api.md) 中定义为可选，但实际调用中若未提供，系统将回退至平台默认提示词，可能导致行为不可控——建议始终显式传入。

## 使用方式

1. **创建 Agent**：`POST /agents`，传入 `model_id`、`name`、`description` 及可选 `skills` 列表；
2. **启动会话**：`POST /agents/{agent_id}/sessions`，获取 `session_id`；
3. **发送消息**：`POST /agents/{agent_id}/sessions/{session_id}/messages`，支持 `files` 数组上传（见 [File](raw/application-api-reference/managed-agents-api/files-api.md)）；
4. **监听事件**（可选）：对 `/sessions/{session_id}/events` 建立长连接，接收 `tool_call`、`memory_update` 等事件。

完整流程示例参见 [快速开始](raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)。

## 限制和注意事项

- 单次请求最大输入 tokens：`qwen-max` 为 32768，`qwen-plus` 为 65536；超出将被截断并返回警告头 `X-Warning: input_truncated`；
- Memory Store 单条记录最大 size 为 1MB，超限写入失败；
- Webhook 事件投递最多重试 3 次，间隔指数退避；需确保 endpoint 返回 `2xx`，否则视为失败（[Webhook](raw/application-api-reference/managed-agents-api/webhook-api.md)）；
- 所有资源（Agent、Session、File 等）均受项目级配额约束，详情见 [API 总览与认证](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 来源文档

- [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)


