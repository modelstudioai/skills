# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的托管式智能体服务接口，用于构建、部署和管理具备长期记忆、多工具调用与环境感知能力的 AI 应用。它将 Agent 生命周期（如环境配置、会话管理、技能编排、文件与凭证管理）抽象为标准化 REST 接口，开发者无需自行维护底层运行时。该 API 与百炼模型服务深度集成，支持异步流式响应与事件驱动架构，详见 [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)。

## 支持的模型与功能

- **模型兼容性**：当前仅支持百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 系列大模型；不支持自定义模型或第三方模型接入。
- **核心功能模块**：
  - `Agent`：定义智能体行为逻辑、系统提示与默认技能集；
  - `Environment`：隔离运行上下文（如 [sandbox](../guides/sandbox.md)、network policy、tool access scope）；
  - `Session`：管理用户级会话状态与事件生命周期（`session.created`、`event.step_completed` 等）；
  - `Memory Store`：提供向量+结构化混合存储，支持跨会话记忆检索；
  - `Skill` 与 `Vault`：分别封装可复用的功能单元（如查天气、调用数据库）与加密凭证仓库；
  - `Webhook`：用于接收异步事件回调（如任务完成、错误告警），其签名验证机制在 [Webhook](../../raw/application-api-reference/managed-agents-api/webhook-api.md) 中明确定义。

> **注意**：原始文档中 [Deployment](../../raw/application-api-reference/managed-agents-api/deployment-api.md) 提到支持“灰度发布策略”，但实际 API 当前仅接受 `active` / `inactive` 两种状态，灰度字段已被忽略——该描述已过时，请以 OpenAPI Schema 为准。

## 关键参数

所有 POST 请求需携带 `Authorization: Bearer <token>` 及 `Content-Type: application/json`。通用关键参数包括：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `agent_id` | string | 是（除 `/agents` 创建外） | Agent 唯一标识，由平台分配或用户指定（需全局唯一） |
| `session_id` | string | 否（首次调用可省略） | 会话 ID；若未提供，API 自动创建新会话并返回 `session_id` |
| `stream` | boolean | 否，默认 `false` | 设为 `true` 时启用 Server-Sent Events (SSE) 流式响应，适用于长任务场景 |
| `max_steps` | integer | 否，默认 `15` | 单次会话中 Agent 最大自主推理步数，防止无限循环 |

完整参数定义请参考 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md) 与 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md) 文档。

## 使用方式

1. **初始化 Agent**：调用 `POST /v1/agents` 创建 Agent 实例，传入 `model`、`system_prompt`、`skills` 列表等；
2. **启动会话**：调用 `POST /v1/sessions`（或直接在 `POST /v1/agents/{id}/run` 中隐式创建），附带用户输入 `input`；
3. **流式交互（推荐）**：设置 `stream=true`，按 SSE 格式解析 `data:` 行，处理 `message`、`step`、`tool_call` 等事件类型；
4. **文件与记忆操作**：通过 `/files` 上传上下文材料，再于 `session.run` 请求中引用 `file_ids`；使用 `/memory` 接口显式写入或查询长期记忆。

快速上手示例见 [Quick Start](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)。

## 限制和注意事项

- **速率限制**：单个 `agent_id` 默认限流 5 QPS（突发允许 10 QPS/3s），超出返回 `429 Too Many Requests`；
- **会话超时**：空闲会话 30 分钟自动销毁，`session_id` 失效；活跃会话最长存活 24 小时；
- **文件限制**：单文件 ≤ 100 MB，总容量按项目配额计费；不支持 `.exe`、`.bin` 等可执行格式；
- **安全约束**：`Environment` 中禁用 `root` 权限、`hostNetwork` 及任意端口绑定；所有 `Skill` 调用必须经 `Vault` 解密凭证后执行；
- **调试建议**：开启 `debug: true`（仅开发环境）可在响应中返回 `trace_id` 和中间步骤日志，便于排查 [Memory Store](../../raw/application-api-reference/managed-agents-api/memory-store-api.md) 检索偏差或技能调用失败问题。

## 来源文档

- [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)


