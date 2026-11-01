# managed agents api

Managed Agents API 是百炼平台提供的用于构建、部署和管理可编程智能体（Agent）的 RESTful 接口集合，支持从环境配置、会话生命周期、技能编排到凭证与内存存储的全栈控制。该 API 适用于需要深度定制 Agent 行为、集成外部系统或实现企业级工作流编排的开发者场景。所有接口均需通过标准认证流程访问，详见 [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md)。

## 支持的模型与功能

- **核心能力**：支持基于 LLM 的自主决策 Agent 实例化（`Agent` 资源），配合 `Environment` 隔离运行上下文，通过 `Session` 管理多轮交互状态，并利用 `Memory Store` 持久化对话历史与任务上下文。
- **扩展能力**：可通过 `Skill` 注册自定义工具函数，使用 `Vault` 和 `Credential` 安全管理密钥与外部服务凭据，借助 `Webhook` 实现事件驱动回调；`Deployment` 接口支持灰度发布与版本回滚。
- 所有子模块（如 `Files API`、`Skills API`）均在 [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md) 的导航目录中明确定义，建议按需查阅对应子文档。

## 关键参数

- `agent_id`（路径参数）：Agent 实例唯一标识，由 `/agents` 创建接口返回，后续所有资源操作（如 `/sessions`, `/environments`）均需显式指定。
- `session_id`（请求头或路径）：部分端点（如 `/sessions/{session_id}/events`）要求携带有效 `session_id`，且需在 `X-Bailian-Session-ID` 中重复声明以确保一致性。
- `tool_choice`（请求体）：在 `POST /agents/{agent_id}/invoke` 中控制工具调用策略，可选 `"auto"`、`"none"` 或指定 `{"type": "function", "name": "xxx"}`；该字段行为与 [Agent API](../../raw/application-api-reference/managed-agents-api/agent-api.md) 文档严格一致。
- `memory_store_id`（可选）：若启用[长期记忆](../concepts/long-term-memory.md)，需在 `Environment` 创建时绑定已存在的 `Memory Store` ID，否则默认使用会话级临时内存。

## 使用方式

1. **认证**：使用平台颁发的 `API Key`，通过 `Authorization: Bearer <api_key>` 请求头完成认证；[认证说明](../../raw/application-api-reference/managed-agents-api/managed-agents-api-authentication.md) 提供了密钥生成与作用域配置细节。
2. **快速启动**：参考 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md) 文档，依次调用 `POST /agents` → `POST /environments` → `POST /sessions` 即可完成最小可用 Agent 流程。
3. **调试建议**：首次调用失败时，优先检查 `X-Bailian-Trace-ID` 响应头并结合 [错误码](../../raw/application-api-reference/managed-agents-api/managed-agents-api-errors.md) 文档定位问题；生产环境应监听 `webhook` 事件而非轮询 `GET /sessions/{id}/events`。

## 限制和注意事项

- 单个 `Environment` 最多关联 10 个 `Skill`，单次 `invoke` 请求最多触发 5 次工具调用（含嵌套），超出将返回 `400 Bad Request`。
- `Memory Store` 的 TTL 默认为 7 天，不可修改；若需更长保留期，须改用外部数据库并通过 `Skill` 自行实现读写逻辑。
- > **注意**：`/files` 接口当前仅支持 `multipart/form-data` 上传，但 [文件 API](../../raw/application-api-reference/managed-agents-api/files-api.md) 中示例仍包含已废弃的 `base64` 字段说明，实际请求中请忽略该字段，以最新 OpenAPI Schema 为准。

## 来源文档

- [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md)


