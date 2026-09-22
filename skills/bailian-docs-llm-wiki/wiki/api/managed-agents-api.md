# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的托管式智能体服务接口，用于创建、配置和运行具备[长期记忆](../concepts/memory.md)、工具调用、多步推理能力的 AI Agent。该 API 将底层基础设施（如环境隔离、状态持久化、技能注册）抽象为标准 REST 接口，开发者可聚焦于业务逻辑而非运维细节。所有资源均通过统一的 `https://dashscope.aliyuncs.com/ma` 基础路径访问。

## 支持的模型与功能

- **模型支持**：当前仅支持 `qwen-max` 和 `qwen-plus` 作为 Agent 的核心推理模型；其他 Qwen 系列模型（如 `qwen-turbo`）暂不支持 Agent 模式，详见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。
- **核心功能**：
  - 多轮会话管理（含自动 session 生命周期控制）
  - 内置 Memory Store（支持向量检索与结构化记忆）
  - 文件上传与内容解析（PDF/DOCX/TXT/CSV 等，最大 100MB）
  - 技能（Skill）注册与编排（支持 HTTP Webhook、内置函数、自定义 Python 脚本）
  - 凭据安全存储（Vault + Credential 绑定）

> **注意**：原始文档中 [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md) 提到支持自定义 Docker 镜像，但该能力已于 v2.3 版本下线；实际仅支持平台预置的沙箱环境，最新约束请以 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md) 中的运行时说明为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 固定为 `qwen-max` 或 `qwen-plus`，不支持别名或版本后缀 |
| `instructions` | string | 否 | Agent 的系统提示词，长度 ≤ 4096 字符；若为空则使用模型默认行为 |
| `tools` | array | 否 | 工具列表，每个元素为 `{ "type": "webhook" \| "function" \| "retrieval", ... }`；`retrieval` 类型需关联已上传的 File ID 或 Memory Store ID |
| `memory_store_id` | string | 否 | 指定复用的 Memory Store，否则自动创建新实例 |
| `session_ttl_seconds` | integer | 否 | 会话过期时间，默认 3600（1 小时），范围 60–86400 |

## 使用方式

1. **创建 Agent**：`POST /v1/agents`，传入 `model`、`instructions`、`tools` 等参数，返回 `agent_id`；
2. **启动会话**：`POST /v1/sessions`，指定 `agent_id`，获取 `session_id`；
3. **发送消息**：`POST /v1/sessions/{session_id}/messages`，支持流式响应（`stream=true`）；
4. **管理依赖**：通过 `/v1/files`、`/v1/memory-stores`、`/v1/skills` 等子资源提前准备所需资产。

完整流程示例见 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)，包括 cURL 和 Python SDK 调用片段。

## 限制和注意事项

- 单次请求最大 token 数：输入 + 输出总和 ≤ 32768（`qwen-max`）或 16384（`qwen-plus`）；
- 单个 Agent 最多绑定 50 个 Skill，单个 Session 最多调用 100 次工具；
- Memory Store 默认保留最近 1000 条交互记录，超出部分按 LRU 自动淘汰；
- 所有文件上传必须先调用 `/v1/files` 创建 File 对象，再在 `tools.retrieval` 中引用其 `file_id` —— 直接传入本地路径将失败；
- Agent 不支持跨区域部署，`agent_id` 仅在其创建时指定的 Region 内有效。

> **注意**：[Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md) 文档中描述的 `event_type: "tool_call"` 回调格式，与当前 v2.5 API 实际返回字段存在差异（新增 `tool_use_id` 字段且 `name` 改为 `tool_name`），请以 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md) 文档中的响应 Schema 为准。

## 来源文档

- [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)


