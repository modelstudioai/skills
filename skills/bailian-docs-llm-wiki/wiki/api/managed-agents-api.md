# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的托管式智能体服务接口，用于创建、配置和运行具备长期记忆、工具调用、多步推理能力的自主 Agent。该 API 以 RESTful 形式提供，支持细粒度的生命周期管理（如 Environment、Session、Memory Store）和安全资源隔离（如 Vault、Credential）。开发者可通过组合基础模块快速构建生产级 AI 应用，无需自行维护底层执行环境。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 系统级 Agent 模型；自定义模型暂不支持作为 Managed Agent 的推理引擎。  
- **核心功能模块**包括：Agent 定义与部署、运行时 Environment 配置、Session 生命周期管理、结构化 Memory Store、文件上传与引用、Skill 编排、密钥 Vault 与 Credential 绑定、Webhook 事件回调等。完整能力清单见 [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)。  
- 所有模块均通过统一认证与权限体系控制访问，具体权限策略参见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 关键参数

- `agent_id`：必填，由 `/v1/agents` 创建后返回的唯一标识，用于后续所有资源关联。  
- `session_id`：可选但强烈建议显式指定，用于跨请求保持上下文一致性；若未提供，系统将自动生成临时 session，其 memory 不持久化。  
- `memory_store_id`：若启用长期记忆，需提前通过 `/v1/memory-stores` 创建并在此处引用；注意该 ID 必须与 Agent 所属 workspace 权限一致。  
- `tool_choice`：支持 `"auto"`（默认）、`"none"` 或显式指定 Skill ID 列表；`"auto"` 行为依赖模型能力，实际调用前请验证 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md) 文档中对应模型的 tool [support](../guides/support.md) 声明。

## 使用方式

1. **初始化 Agent**：先调用 `POST /v1/agents` 创建 Agent 实例，传入 `model`, `instructions`, `skills` 等配置；响应中获取 `agent_id`。  
2. **准备运行时环境**：可选调用 `/v1/environments` 创建隔离环境（如设置网络策略或 CPU 限制），再在 Session 创建时通过 `environment_id` 关联。  
3. **启动交互**：调用 `POST /v1/sessions/{session_id}/messages` 发送用户消息；系统自动调度模型、调用 Skill、读写 Memory Store 并返回结构化响应（含 `event_type: "message", "tool_use", "memory_update"` 等）。  
4. **事件监听**：如需异步处理结果，可配置 Webhook（见 [Webhook](../../raw/application-api-reference/managed-agents-api/webhook-api.md)），接收 `session.completed` 或 `tool_error` 等事件。

> **注意**：文档中提及的 `/v1/files` 接口支持直接上传文件供 Agent 引用，但实测发现 `file_id` 在 `messages` 请求中必须通过 `content` 字段以 `{"type": "file_id", "id": "xxx"}` 格式嵌入，而非作为独立参数传递——该细节与 [File](../../raw/application-api-reference/managed-agents-api/files-api.md) 中示例代码存在偏差，以实际 API 行为为准。

## 限制和注意事项

- 单个 Session 最大持续时间为 24 小时；超时后 `session_id` 失效，需新建 Session。  
- Memory Store 单条记录最大 1MB，总容量受 workspace 配额限制；高频写入场景建议批量合并更新。  
- Skill 调用链深度限制为 5 层（含主 Agent 自身），超出将触发 `tool_depth_exceeded` 错误。  
- 所有 API 均要求 `X-DashScope-Source: managed-agents` 请求头，缺失将返回 `401 Unauthorized`；该要求在 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md) 中有明确说明，但部分旧版 SDK 示例遗漏，需手动补全。

## 来源文档

- [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)


