# managed agents api

Managed Agents API 是百炼平台提供的托管式智能体服务接口，用于创建、配置和管理具备[长期记忆](../concepts/long-term-memory.md)、工具调用、多轮会话能力的 AI Agent。该 API 将底层模型调度、环境隔离、状态持久化等复杂逻辑封装为标准化资源操作（如 `Agent`、`Environment`、`Session`），开发者可通过 RESTful 接口快速构建生产级智能体应用。所有功能均需通过 [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md) 主文档索引访问子模块。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款 Qwen 系列大模型；不支持第三方模型或自定义模型权重接入。
- **核心功能模块**：
  - `Agent`：定义智能体行为逻辑、技能组合与默认配置；
  - `Environment`：隔离运行时依赖（如工具集、系统提示词、memory store 绑定）；
  - `Session`：管理用户级多轮对话上下文与事件流；
  - `Memory Store`：提供结构化[长期记忆](../concepts/long-term-memory.md)存储（支持向量检索与键值查询）；
  - `Skill`：封装可复用的原子能力（如 HTTP 调用、数据库查询、文件解析），通过 [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md) 接口注册与编排；
  - `Vault` 与 `Credential`：安全托管敏感凭证，供 Skill 在运行时按需访问。

> **注意**：原始文档中 `Environment` 模块描述其“支持任意 LLM provider”，但实际 API 实现仅接受 `qwen-*` 模型标识符；该不一致已在内部工单 #MA-204 中标记为文档过时，以 [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md) 当前接口契约为准。

## 关键参数

所有 POST/PUT 请求需在 JSON body 中包含以下必需字段（部分资源有额外约束）：

| 参数 | 类型 | 说明 |
|------|------|------|
| `name` | string | 资源唯一标识名（仅限字母、数字、连字符，长度 ≤ 64） |
| `description` | string | 可选，不超过 512 字符 |
| `config` | object | 模块特定配置对象，例如 `Agent.config.model` 必须为 `qwen-max` 等受支持值 |
| `environment_id` | string | 创建 `Agent` 或 `Session` 时必填，引用已存在的 Environment ID |

认证凭据必须通过 `Authorization: Bearer <api_key>` 传递，密钥需具备 `managed_agents:full_access` 权限；详细要求见 [认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-authentication.md) 文档。

## 使用方式

1. **初始化环境**：先调用 `/environments` 创建 `Environment`，指定 `skills` 列表与 `memory_store_id`；
2. **部署智能体**：调用 `/agents` 创建 `Agent`，绑定上一步的 `environment_id`；
3. **启动会话**：对目标 `Agent` 发起 `POST /agents/{agent_id}/sessions`，获取 `session_id`；
4. **交互消息**：向 `/sessions/{session_id}/messages` 发送 `user` 角色消息，服务端自动处理 tool call、memory 写入与流式响应。

完整流程示例参见 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)。所有资源均支持标准 CRUD 操作，事件驱动行为（如 skill 执行完成、session timeout）可通过 [Webhook](../../raw/application-api-reference/managed-agents-api/webhook-api.md) 订阅。

## 限制和注意事项

- 单个 `Session` 最长存活时间为 7 天，超时后 `memory` 数据仍保留但不可继续交互；
- `File` 上传大小上限为 100 MB，仅支持 `pdf`, `txt`, `csv`, `xlsx`, `docx` 格式（详见 [File](../../raw/application-api-reference/managed-agents-api/files-api.md)）；
- 同一 `Environment` 下最多关联 50 个 `Skill`；单次 `Session` 中 tool call 深度限制为 8 层嵌套；
- `Credential` 的 secret 值仅在创建时返回一次，后续无法读取，务必妥善保存；
- 错误响应遵循统一格式，常见错误码及含义请查阅 [错误码](../../raw/application-api-reference/managed-agents-api/managed-agents-api-errors.md)。

## 来源文档

- [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md)


