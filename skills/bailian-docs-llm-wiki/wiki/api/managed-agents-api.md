# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的托管式智能体服务接口，用于创建、配置和运行具备长期记忆、工具调用、多步推理能力的自主 Agent。该 API 将底层模型调度、状态管理、环境隔离与安全凭证等复杂性封装为声明式资源（如 `Agent`、`Environment`、`Memory Store`），开发者可通过 RESTful 接口组合构建生产级 AI 应用。所有操作均需通过 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 中描述的 Bearer [Token](../concepts/token.md) 进行身份验证。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三类大模型作为 Agent 的推理引擎；不支持 BYOM（Bring Your Own Model）或外部模型端点。  
- **核心功能模块**包括：  
  - `Agent`：定义行为逻辑、提示词模板、技能绑定与执行策略；  
  - `Environment`：隔离运行时上下文（如 sandboxed Python 执行环境）；  
  - `Memory Store`：持久化会话记忆与长期知识，支持向量检索；  
  - `Skill`：封装可复用的工具能力（如 HTTP 调用、数据库查询），其注册与调用流程详见 [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md) 文档；  
  - `Vault` 与 `Credential`：用于安全存储和动态注入敏感凭据，避免硬编码。  

> **注意**：原始文档中 [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md) 描述支持自定义 Docker 镜像，但该能力已在 v2.3 版本中下线，实际仅支持平台预置的 `python311-sandbox` 和 `node18-sandbox` 环境镜像，请以 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md) 中的示例为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model_id` | string | 是 | 必须为 `qwen-max` / `qwen-plus` / `qwen-turbo` 之一，不接受别名或版本后缀（如 `qwen-max-202406`） |
| `memory_store_id` | string | 否 | 若未指定，系统自动创建临时 Memory Store；若指定，需确保已通过 [Memory Store](../../raw/application-api-reference/managed-agents-api/memory-store-api.md) API 创建并处于 `active` 状态 |
| `skills` | array[string] | 否 | 技能 ID 列表，每个 ID 必须已在当前项目中注册（参见 [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)） |
| `max_steps` | integer | 否 | 默认 15，取值范围 1–50；超过此步数将强制终止执行并返回 `stopped_by_max_steps` |

## 使用方式

1. **初始化 Agent**：`POST /v1/agents`，传入 `model_id`、`name`、`description` 及可选的 `memory_store_id` 和 `skills`；  
2. **启动会话**：`POST /v1/sessions`，指定 `agent_id`，获取 `session_id`；  
3. **发送用户消息**：`POST /v1/sessions/{session_id}/messages`，携带 `content` 字段（纯文本或结构化 JSON）；  
4. **流式响应**：设置 `Accept: text/event-stream` 头，接收 SSE 格式事件（含 `step_started`、`tool_call`、`message` 等类型）。  
完整交互流程与错误码说明请参考 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)。

## 限制和注意事项

- 单个 Agent 实例最大并发会话数为 100；超出将返回 `429 Too Many Requests`；  
- 文件上传（如通过 [File](../../raw/application-api-reference/managed-agents-api/files-api.md) API）单文件上限 100 MB，且仅在 `Environment` 中可被 `Skill` 访问；  
- `Credential` 绑定后不可修改，如需更新密钥，必须删除重建并重新关联 `Skill` 或 `Agent`；  
- 所有 API 均遵循平台统一配额策略，具体限流阈值请查阅 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 来源文档

- [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)


