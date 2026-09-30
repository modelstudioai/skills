# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的托管式智能体服务接口，用于创建、配置和运行具备[长期记忆](../concepts/memory.md)、工具调用、多步推理能力的 AI Agent。该 API 封装了环境管理、会话生命周期、文件与凭证存储、技能编排等底层复杂性，开发者可通过 RESTful 接口快速集成。详细设计与行为语义请参考 [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三类大模型作为 Agent 的推理引擎；不支持自定义模型或外部模型接入。
- **核心功能**：
  - 基于 Session 的有状态交互（含事件流式响应）
  - 内置 Memory Store 实现跨会话记忆持久化
  - 文件上传/引用（支持 PDF、TXT、CSV 等格式，解析由平台自动完成）
  - Vault + Credential 联合管理敏感凭据（如 API Key、数据库连接串）
  - 技能（Skill）注册与组合调用，支持 HTTP Webhook 类型技能
  - 环境隔离（Environment）用于区分开发、测试、生产部署上下文

> **注意**：[Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md) 文档中提及的 `model: custom-llm-v1` 参数值已在 v2.3.0 版本后废弃，实际调用将返回 400 错误；请以 [Deployment](../../raw/application-api-reference/managed-agents-api/deployment-api.md) 中声明的模型列表为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `agent_id` | string | 是 | Agent 唯一标识，由 `/v1/agents` 创建后返回 |
| `session_id` | string | 否 | 复用已有会话；首次调用可省略，平台自动生成 |
| `input` | object | 是 | 用户输入内容，结构为 `{ "text": "..." }` 或 `{ "files": ["file_id_1", "..."] }` |
| `stream` | boolean | 否 | 默认 `false`；设为 `true` 时启用 Server-Sent Events (SSE) 流式响应 |
| `memory_store_id` | string | 否 | 指定关联的 Memory Store，否则使用 Agent 默认存储 |

所有请求需携带 `Authorization: Bearer <api_key>` 及 `Content-Type: application/json`。更多字段细节见 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)。

## 使用方式

1. **创建 Agent**：调用 `POST /v1/agents`，传入基础配置（名称、描述、默认模型、[skill](../guides/skill.md)s 列表等）  
2. **启动会话**：`POST /v1/agents/{agent_id}/sessions`，可选指定 `environment_id` 和 `memory_store_id`  
3. **发送消息**：`POST /v1/sessions/{session_id}/messages`，支持单次多文件+文本混合输入  
4. **查询状态/历史**：`GET /v1/sessions/{session_id}` 或 `GET /v1/sessions/{session_id}/messages`  

完整端到端流程示例参见 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)。

## 限制和注意事项

- 单次请求 `input.text` 长度上限为 32768 字符；单个文件大小上限为 50 MB（PDF 解析后文本长度计入总上下文）  
- 每个 Agent 最多绑定 10 个 Skill；每个 Skill 最多配置 5 个 Webhook endpoint  
- Session 默认 TTL 为 24 小时，超时后自动清理内存与临时文件；如需延长，请在创建时显式设置 `ttl_seconds`（最大 604800，即 7 天）  
- 所有文件上传均通过 `/v1/files` 接口预处理，直接在 `input.files` 中引用 file_id；未预上传的 file_id 将导致 404 错误 —— 此行为与 [File](../../raw/application-api-reference/managed-agents-api/files-api.md) 文档一致。

## 来源文档

- [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)


