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
- `session_ttl_seconds`（可选，默认 3600）：控制 Session 自动过期时间，最小值为 60 秒；
- `vault_ids`（可选）：关联 Vault ID 列表，用于在运行时安全注入敏感配置，需确保当前 API Key 具备对应 Vault 的 `read` 权限。

## 使用方式

1. **初始化 Agent**：向 `/v1/agents` 发送 `POST` 请求，传入 `name`、`model_id`、`skills` 等字段，获取返回的 `agent_id`；
2. **启动会话**：调用 `/v1/agents/{agent_id}/sessions` 创建新 Session，可携带初始 `input` 和 `files`（通过 File API 上传后获得的 `file_id`）；
3. **流式交互**：使用 SSE 或轮询方式监听 `/v1/sessions/{session_id}/events` 获取 `message`、`tool_call`、`tool_result` 等事件；
4. 所有资源操作均需在请求头中携带 `Authorization: Bearer <api_key>`，且 API Key 需具备对应资源的操作权限（如 `agents:create`、`vaults:read`）。

## 限制和注意事项

- 单个 Agent 最多绑定 10 个 Skill，单次 Session 最多上传 50 个文件（总大小 ≤ 100MB）；
- Environment 不支持运行任意 shell 命令或持久化写入磁盘，所有工具调用必须通过 Skill 显式声明并经平台审核；
- > **注意**：原始文档中 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 提到“支持 OAuth2 授权码模式”，但当前生产环境仅支持 API Key 认证，OAuth2 尚未上线，实际接入请以 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md) 中的 Key 配置为准；
- Vault 中存储的密钥在 Agent 运行时以环境变量形式注入，**不会**出现在日志或事件响应体中，但需确保 Skill 代码未主动打印敏感字段；
- Deployment 和 Webhook 功能目前仅限企业版客户开通，免费版调用 `/v1/deployments` 或 `/v1/webhooks` 将返回 `403 Forbidden`。

## 来源文档

- [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)


