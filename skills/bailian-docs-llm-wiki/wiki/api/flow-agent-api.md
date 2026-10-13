# flow agent api

Flow Agent API 是百炼平台提供的用于调用流程化智能体（Flow Agent）的核心接口，支持将预定义的多步骤工作流（含条件分支、工具调用、记忆管理等）以 HTTP 方式集成到业务系统中。该 API 采用 RESTful 设计，兼容标准 OAuth2 认证与结构化请求/响应格式。适用于需要可控执行逻辑、可审计调用链路及与企业已有系统深度集成的场景。

## 支持的模型与功能

- 当前仅支持百炼平台托管的 Flow Agent 实例（即通过控制台或 SDK 创建并发布的 `flow` 类型应用），不支持直接调用基础大模型（如 Qwen 系列）或非流程类 Agent。
- 核心能力包括：同步/异步任务触发、输入变量注入、运行时上下文传递、结构化输出解析（JSON Schema 可选）、以及基于 [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md) 的会话状态延续（注意：该机制已被新式向量记忆替代，详见 [概览](../../raw/application-api-reference/flow-agent-api/flow-agent-api-overview.md)）。
- > **注意**：原始文档中 [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md) 描述的记忆机制已废弃，新项目应使用 `memory_id` + 向量库方式实现持久化上下文，具体参见最新 [概览](../../raw/application-api-reference/flow-agent-api/flow-agent-api-overview.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | Flow Agent 应用唯一 ID，可在控制台「应用管理」中获取 |
| `inputs` | object | 否 | JSON 对象，键为流程中定义的 input 变量名，值为对应字符串或结构化数据（需符合 Prompt 模板约束） |
| `stream` | boolean | 否 | 默认 `false`；设为 `true` 时启用 SSE 流式响应（仅限同步调用） |
| `timeout` | integer | 否 | 单位秒，最大 300；超时后返回 `504 Gateway Timeout` |
| `memory_id` | string | 否 | 用于关联[长期记忆](../concepts/long-term-memory.md)的唯一标识符（推荐使用 UUID v4），替代已废弃的旧式记忆参数 |

## 使用方式

1. **认证**：使用 Bearer Token 进行身份验证，Token 需通过 [认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md) 文档所述方式获取（推荐使用 `client_credentials` 模式）；
2. **请求示例**（POST `/v1/agents/{app_id}/invoke`）：
   ```http
   POST /v1/agents/app-abc123/invoke HTTP/1.1
   Authorization: Bearer <access_token>
   Content-Type: application/json

   {
     "inputs": { "query": "今天北京天气如何？" },
     "stream": false,
     "memory_id": "mem-9f8e7d6c5b4a"
   }
   ```
3. **响应结构**：成功时返回 `200 OK`，主体为包含 `output`（流程最终结果）、`trace_id`（用于日志追踪）和 `status`（`success`/`failed`）的对象；错误码详见 [错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)。

## 限制和注意事项

- 单次请求 `inputs` 总大小上限为 1MB；单个 input 字段值长度建议不超过 10,000 字符；
- 异步调用（`/invoke-async`）返回 `task_id`，需轮询 `/tasks/{task_id}` 获取结果，最长保留 24 小时；
- 所有调用均受配额限制（QPS/日调用量），超出将返回 `429 Too Many Requests`；
- > **注意**：[Prompt 模板](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-prompt-engineering.md) 中定义的变量占位符语法（如 `{{query}}`）必须与 `inputs` 中的 key 完全一致，否则流程可能跳过该节点或报错；该约束在 [应用调用](../../raw/application-api-reference/flow-agent-api/application-call.md) 文档中有明确说明，但未在模板文档中强调，开发者需交叉核对。

## 来源文档

- [Flow Agent API](../../raw/application-api-reference/flow-agent-api.md)


