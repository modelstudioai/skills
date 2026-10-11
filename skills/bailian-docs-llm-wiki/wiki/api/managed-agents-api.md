# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的托管式智能体服务接口，用于创建、配置和管理具备长期记忆、工具调用、多步推理能力的自主 Agent。该 API 以 RESTful 形式提供，支持细粒度的环境隔离、会话生命周期控制与安全凭证管理。开发者可通过组合 Agent、Environment、Session、Skill 等核心资源构建生产级自动化工作流。

## 支持的模型与功能

- **模型无关性**：Managed Agents 不绑定特定大模型，支持通过 `model_id` 参数指定任意已接入百炼平台的 LLM（如 Qwen-Max、Qwen-Plus），模型能力由底层 `Agent` 资源配置决定。
- **核心功能模块**：
  - `Agent`：定义行为逻辑、系统提示、默认技能集；
  - `Environment`：提供沙箱化执行上下文（含网络访问策略、文件系统挂载）；
  - `Session`：维护用户级对话状态与短期记忆；
  - `Memory Store`：持久化长期记忆（向量+结构化混合存储）；
  - `Skill`：封装可复用的工具函数（如 HTTP 请求、数据库查询）；
  - `Vault` 与 `Credential`：安全存储敏感凭据并按需注入运行时。

> **注意**：[原文标题](../../raw/application-api-reference/managed-agents-api.md) 中列出的 `Webhook` 和 `Deployment` 接口当前仅限企业版开通，免费版调用将返回 `403 Forbidden` —— 此限制未在 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 中明确说明，以本页为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `agent_id` | string | 是 | 通过 `/v1/agents` 创建后返回的唯一标识符 |
| `environment_id` | string | 否 | 指定运行环境；不传则使用默认环境（见 [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)） |
| `session_id` | string | 否 | 复用已有会话；首次调用建议留空由服务自动生成 |
| `input` | object | 是 | 用户输入内容，格式为 `{ "text": "..." }` 或 `{ "files": ["file_id_1", "..."] }` |
| `stream` | boolean | 否 | 设为 `true` 启用 SSE 流式响应（推荐用于长任务） |

## 使用方式

1. **初始化 Agent**：先调用 `POST /v1/agents` 创建 agent 实例（参考 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)）；
2. **启动会话**：调用 `POST /v1/sessions` 绑定 agent 与 environment（参考 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)）；
3. **发送请求**：对 `/v1/sessions/{session_id}/chat` 发起 `POST`，传入 `input` 及可选参数；
4. **处理响应**：非流式响应返回 JSON 对象；流式响应需按 `data:` 行解析事件（含 `message`, `tool_use`, `memory_update` 等类型）。

## 限制和注意事项

- 单次请求 `input.text` 长度上限为 32,768 字符；上传文件总大小不超过 100 MB（见 [File](../../raw/application-api-reference/managed-agents-api/files-api.md)）；
- `Memory Store` 的向量检索默认 Top-K=5，不可覆盖；如需调整，须通过 `POST /v1/memory_stores/{id}/search?top_k=10` 显式调用；
- 所有 Skill 调用均受 Environment 的网络策略约束：默认禁止外网访问，需在 Environment 配置中显式启用 `allow_external_network: true`；
- Session 生命周期默认 24 小时，超时后关联内存自动清理，但 `Memory Store` 中数据永久保留（除非手动删除）。

## 来源文档

- [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)


