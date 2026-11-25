# managed agents api

Managed Agents API 是百炼平台提供的托管式智能体服务接口，用于创建、配置和运行具备长期记忆、[工具调用](../concepts/tool-calling.md)、多步推理能力的 AI Agent。该 API 将底层模型调度、状态管理、技能编排等复杂逻辑封装为标准化资源操作（如 `Agent`、`Environment`、`Session`），开发者可通过 RESTful 接口快速集成。所有核心能力均基于百炼统一认证与配额体系，详见 [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md)。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款 Qwen 系列模型；其他模型（如 `qwen2.5-*`）暂未开放 Agent 模式推理通道，具体以 [Agent API](../../raw/application-api-reference/managed-agents-api/agent-api.md) 文档为准。
- **核心功能**：
  - 多轮 Session 管理（含事件流式返回）
  - 内置 Memory Store 实现跨会话上下文持久化
  - Vault + Credential 组合实现安全凭证注入
  - Skills 插件机制支持自定义工具注册与调用
  - Webhook 回调支持异步任务结果通知

> **注意**：原始文档中 [Environment API](../../raw/application-api-reference/managed-agents-api/environment-api.md) 提到支持“自定义 Docker 镜像部署”，但该能力已于 v2.3 版本下线；实际仅支持平台预置的沙箱环境，最新约束请以 [Deployment API](../../raw/application-api-reference/managed-agents-api/deployment-api.md) 为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `agent_id` | string | 是 | 通过 `/v1/agents` 创建后返回的唯一标识 |
| `session_id` | string | 否 | 复用已有会话时传入；不传则新建会话（自动绑定 Memory Store） |
| `input` | object | 是 | 用户输入，结构为 `{ "text": "..." }`，暂不支持多模态输入 |
| `stream` | boolean | 否 | `true` 时启用 SSE 流式响应，默认 `false` |
| `tools` | array | 否 | 显式指定本次调用可使用的 Skill ID 列表，未声明则使用 Agent 默认技能集 |

## 使用方式

1. **前置准备**：完成 [认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-authentication.md)，获取 `Authorization: Bearer <api_key>`；
2. **创建 Agent**：调用 `POST /v1/agents`，配置 `model`, `skills`, `memory_store_id` 等字段；
3. **发起推理**：`POST /v1/agents/{agent_id}/sessions`，传入 `input` 及可选参数；
4. **处理响应**：同步模式返回完整 JSON；流式模式需按 `event: message` + `data: {...}` 解析 SSE。

示例请求路径：  
`POST https://dashscope.aliyuncs.com/api/v1/agents/{agent_id}/sessions`

## 限制和注意事项

- 单次 `input.text` 长度上限为 8192 字符；
- Session 生命周期默认 24 小时，超时后关联 Memory Store 条目仍保留（受 Vault TTL 约束）；
- 同一 `agent_id` 并发 `sessions` 数不得超过 100（企业版可申请提升）；
- 文件上传必须先调用 `/v1/files` 获取 `file_id`，再在 `input` 中引用，不可直传二进制；
- 所有 API 均遵循 [错误码规范](../../raw/application-api-reference/managed-agents-api/managed-agents-api-errors.md)，常见 `429 Too Many Requests` 表示超出速率限制，需检查 `X-RateLimit-Remaining` 响应头。

## 来源文档

- [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md)


