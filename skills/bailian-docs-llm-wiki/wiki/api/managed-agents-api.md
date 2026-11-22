# managed agents api

Managed Agents API 是百炼平台提供的托管式智能体服务接口，用于创建、配置和管理具备[长期记忆](../concepts/long-term-memory.md)、工具调用、多轮会话与环境隔离能力的 AI Agent。该 API 以 RESTful 形式提供，支持细粒度资源控制（如 Environment、Session、Memory Store）和可扩展能力（如 Skill、Vault、Webhook）。开发者可通过它构建生产级自动化工作流，无需自行维护底层推理与状态管理逻辑。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 系统模型；自定义模型暂不支持接入 Managed Agents —— 此限制在 [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md) 的概览章节中明确说明。
- **核心功能**：
  - 多会话生命周期管理（Session + Event）
  - 持久化记忆存储（Memory Store，支持向量+结构化混合索引）
  - 安全凭证与密钥管理（Credential + Vault）
  - 可插拔技能注册与编排（Skill API）
  - 文件上传与上下文注入（Files API）
  - 部署与扩缩容控制（Deployment API）

> **注意**：原始文档中 [Environment API](../../raw/application-api-reference/managed-agents-api/environment-api.md) 描述其支持“跨区域网络策略”，但该能力尚未在 v1.2.0 生产环境开放，实际调用将返回 `400 UnsupportedFeature`；请以 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md) 中的环境配置示例为准。

## 关键参数

所有 POST/PUT 请求需在请求体中包含以下必需字段（JSON 格式）：

| 参数 | 类型 | 说明 |
|------|------|------|
| `agent_id` | string | Agent 唯一标识，由 `/agent` 接口创建后返回，不可修改 |
| `session_id` | string | 会话 ID，首次调用 `/session` 时生成；后续消息必须复用同一 session_id 以维持上下文 |
| `input` | object | 用户输入内容，格式为 `{ "text": "..." }` 或 `{ "files": ["file_id_1", "..."] }` |
| `enable_memory` | boolean | 默认 `true`；设为 `false` 时禁用 Memory Store 写入（仅读取已有记忆） |

其他可选参数（如 `tool_choice`、`max_steps`）详见 [Agent API](../../raw/application-api-reference/managed-agents-api/agent-api.md) 文档。

## 使用方式

1. **认证**：使用 Bearer [Token](../concepts/token.md)，通过 `Authorization: Bearer <api_key>` 传入；API Key 需具备 `managed_agents:full_access` 权限（参见 [认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-authentication.md)）  
2. **典型流程**：
   - 调用 `/agent` 创建 agent（获取 `agent_id`）
   - 调用 `/environment` 配置运行环境（如设置 Vault 访问策略）
   - 调用 `/session` 初始化会话（获取 `session_id`）
   - 调用 `/session/{session_id}/chat` 发送用户消息（自动触发 Skill 调用与 Memory 更新）
3. 所有端点均遵循统一错误响应格式，详见 [错误码](../../raw/application-api-reference/managed-agents-api/managed-agents-api-errors.md)

## 限制和注意事项

- 单次 `chat` 请求最大输入长度为 32768 token（含 system prompt + history + input），超限将返回 `400 PayloadTooLarge`
- Memory Store 单条记忆最大 size 为 8KB，超出部分会被截断（非报错）；批量写入上限为 100 条/请求
- Session 生命周期默认 24 小时，过期后 `session_id` 不可复用，需新建会话
- Webhook 事件（如 `session.completed`）仅保证至少一次投递，业务侧需实现幂等处理  
- 文件上传后有效期为 7 天，且仅在关联的 Session 中有效；独立调用 `/files` 接口上传的文件不会自动进入 Memory Store，需显式调用 `/memory/store` 注入

> **注意**：[Usage API](../../raw/application-api-reference/managed-agents-api/usage-api.md) 文档中列出的 `total_tokens_used` 字段，在 v1.2.x 版本中存在统计延迟（约 5–10 分钟），实时用量应通过 `/usage/current` 获取，而非 `/usage/historical`。

## 来源文档

- [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md)


