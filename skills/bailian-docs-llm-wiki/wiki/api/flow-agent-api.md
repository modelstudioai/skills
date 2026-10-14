# flow agent api

Flow Agent API 是百炼平台提供的用于调用流程型智能体（Flow Agent）的核心接口，支持将预定义的多步骤工作流封装为可编程服务。该 API 适用于需要编排工具调用、条件分支、循环或状态管理的复杂任务场景。开发者可通过 HTTP 请求发起调用，并接收结构化响应与执行轨迹。

## 支持的模型/功能

- 当前仅支持基于百炼自研的 `flow-agent-v1` 模型架构，不兼容通用大语言模型（如 `qwen-max`）直接作为 Flow Agent 后端 [Flow Agent API](../../raw/application-api-reference/flow-agent-api.md)。
- 支持的功能包括：多节点流程执行、内置工具自动选择、用户上下文注入、节点级超时控制、以及执行日志流式返回。
- **注意**：文档中提及的“长期记忆（旧）”模块 [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md) 已于 v2.3.0 版本起废弃，实际调用中将被忽略；请改用统一的 `memory_id` 参数配合新版记忆服务。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | Flow Agent 应用唯一标识，需在控制台创建后获取 |
| `inputs` | object | 是 | 用户输入数据，键值对形式，将注入流程首节点上下文 |
| `stream` | boolean | 否 | 默认 `false`；设为 `true` 时以 SSE 流式返回各节点执行结果 |
| `timeout` | integer | 否 | 全局超时（秒），范围 5–300，默认 60 |
| `memory_id` | string | 否 | 关联长期记忆实例 ID，用于跨会话状态复用 [Prompt 模板](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-prompt-engineering.md) 中定义的记忆上下文 |

## 使用方式

1. 使用平台颁发的 `API Key` 进行 Bearer [Token](../concepts/token.md) 认证（详见 [认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md)）；
2. 向 `POST /v1/flow_agent/applications/{app_id}/call` 发起请求；
3. 响应体包含 `output`（最终结果）、`trace`（执行路径快照）和 `status`（`success`/`failed`/`timeout`）字段。

示例请求头：
```http
Authorization: Bearer <your_api_key>
Content-Type: application/json
```

## 限制和注意事项

- 单次调用最大输入长度为 32KB，超出将返回 `400 Bad Request`；
- `stream=true` 时，连接空闲超时为 90 秒，期间无事件将自动断连；
- 节点内工具调用失败默认触发重试（最多 2 次），不可禁用；
- **注意**：错误码定义分散在多个子页中，但 [错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md) 主页未同步更新 v2.2+ 新增的 `FLOW_EXECUTION_CANCELLED` 状态码，实际响应中可能出现该码，建议按 HTTP 状态码 + `code` 字段双重判断。

## 来源文档

- [Flow Agent API](../../raw/application-api-reference/flow-agent-api.md)


