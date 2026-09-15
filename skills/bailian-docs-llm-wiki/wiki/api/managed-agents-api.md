# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的托管式智能体服务接口，用于创建、配置和运行具备自主决策与工具调用能力的 AI Agent。该 API 将环境管理、会话状态、技能编排、文件与凭证安全存储等能力封装为标准化资源，开发者可通过 RESTful 接口按需组合。整体设计遵循声明式原则，支持生产级部署与事件驱动集成。

## 支持的模型与功能

- 支持基于 Qwen 系列大模型（如 `qwen-max`、`qwen-plus`）构建的托管 Agent，模型选择通过 `model_id` 参数指定；
- 内置核心功能模块包括：Agent 生命周期管理、隔离式执行环境（Environment）、多轮会话与事件流（Session and Event）、结构化文件上传/引用（File）、可复用技能封装（Skill）、密钥与凭证安全存储（Credential）、加密数据保险库（Vault），以及 Webhook 事件回调；  
- 所有模块均通过独立 API 资源暴露，例如 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md) 用于定义行为逻辑，[Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md) 用于配置沙箱依赖与超时策略。

## 关键参数

- `model_id`（必填）：指定底层大模型 ID，当前仅支持百炼平台已纳管的 Qwen 模型，不支持自定义模型或外部模型端点；
- `skills`（数组）：引用已注册 Skill 的 ID 列表，Skill 必须预先通过 [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md) API 创建并发布；
- `environment_id`（可选）：绑定预配置的 Environment，若未指定则使用默认环境（CPU 限制 2C，内存 4GB，无 GPU）；
- `session_ttl_seconds`（可选，默认 3600）：控制 Session 自动过期时间，超出后历史上下文不可访问；
- `vault_ids`（可选）：关联 Vault ID 列表，用于在运行时安全注入敏感配置，Vault 内容仅在 Agent 执行期间解密加载。

## 使用方式

1. **前置准备**：通过 [Credential](../../raw/application-api-reference/managed-agents-api/credential-api.md) 和 [Vault](../../raw/application-api-reference/managed-agents-api/vault-api.md) API 注册凭据与密钥；通过 [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md) API 上传并发布工具函数；
2. **创建 Agent**：POST `/v1/agents`，传入 `model_id`、`skills`、`environment_id` 等参数，获取 `agent_id`；
3. **启动会话**：POST `/v1/agents/{agent_id}/sessions`，可携带初始 `input` 和 `files`（通过 [File](../../raw/application-api-reference/managed-agents-api/files-api.md) API 上传后获得 file_id）；
4. **流式交互**：使用 SSE 或轮询方式监听 `/v1/sessions/{session_id}/events` 获取 `agent_message`、`tool_call`、`tool_result` 等事件。

## 限制和注意事项

- 单次 Agent 执行最大耗时为 300 秒（受 Environment 配置约束），超时将强制终止且不触发重试；
- Session 最多保留 100 条消息（含用户输入与 Agent 输出），超出后自动截断最旧消息；
- > **注意**：原始文档中 [Deployment](../../raw/application-api-reference/managed-agents-api/deployment-api.md) 提到支持“灰度发布”，但当前 API 实际未开放 `deployment_strategy` 字段，该功能尚未上线，以实际 OpenAPI Schema 为准；
- 文件上传大小上限为 50MB（[File](../../raw/application-api-reference/managed-agents-api/files-api.md) 规定），且仅支持 `text/plain`、`application/json`、`application/pdf`、`text/csv` 四类 MIME 类型；
- Vault 中存储的密钥不可被 Agent 直接读取原始值，仅能通过 `{{vault.<key>}}` 模板语法在 Skill 参数或提示词中安全注入。

## 来源文档

- [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)


