# flow agent api

Flow Agent API 是百炼平台提供的用于调用流程型智能体（Flow Agent）的核心接口，支持将预定义的多步骤工作流封装为可编程服务。该 API 适用于需要结构化任务编排、状态保持与外部系统集成的场景，如客服工单处理、数据清洗流水线等。开发者可通过 HTTP 请求直接触发流程执行，并获取结构化输出与中间状态。

## 支持的模型/功能

- 当前仅支持基于百炼自研的 `flow-agent-v1` 模型类型，不兼容通用大语言模型（如 `qwen-max`）或旧版 `bailian-2023-12-29` 系列模型。  
- 支持的功能包括：流程启动、异步轮询状态、中断/重试控制、带上下文的多轮交互（需启用 `enable_session`）、以及通过 `memory_id` 关联[长期记忆](../concepts/long-term-memory.md)（见 [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md)）。  
- > **注意**：[Prompt 模板](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-prompt-engineering.md) 文档中描述的 `template_id` 参数在 v1.2+ 版本已废弃，实际应使用 `flow_id` 指向部署后的流程实例；请以 [概览](../../raw/application-api-reference/flow-agent-api/flow-agent-api-overview.md) 中的最新接口定义为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `flow_id` | string | 是 | 百炼控制台部署后生成的唯一流程 ID，非原始 Prompt ID 或模板 ID |
| `input` | object | 是 | 用户输入数据，结构需严格匹配流程定义中的 input schema |
| `enable_session` | boolean | 否 | 默认 `false`；设为 `true` 时启用会话上下文与状态持久化 |
| `memory_id` | string | 否 | 用于绑定[长期记忆](../concepts/long-term-memory.md)的唯一标识符；若未提供，则使用默认匿名记忆空间 |
| `timeout` | integer | 否 | 单位秒，最大值 300；超时后返回 `504 Gateway Timeout` |

## 使用方式

1. **认证**：使用 Bearer Token 方式，在 `Authorization` Header 中传入 `Bearer <access_token>`；Token 需通过 [认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md) 流程获取。  
2. **发起调用**：向 `POST /v1/flows/{flow_id}/run` 发送请求，Body 为 JSON 格式，包含 `input` 及可选参数。  
3. **处理响应**：同步模式下直接返回 `status: "success"` 或 `"failed"`；异步模式需解析 `task_id` 并轮询 `/v1/tasks/{task_id}` 获取最终结果（详见 [应用调用](../../raw/application-api-reference/flow-agent-api/application-call.md)）。

## 限制和注意事项

- 单次 `input` 大小上限为 1MB；总请求（含 headers + body）不得超过 1.5MB。  
- 同一 `memory_id` 下并发执行超过 5 个流程实例将触发限流（HTTP 429），建议按业务粒度合理划分 `memory_id`。  
- 错误响应格式统一遵循标准错误结构，具体码值及含义参见 [错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)。  
- > **注意**：[长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md) 文档中描述的 `memory_ttl` 参数已不再生效，当前所有记忆默认 TTL 为 7 天且不可配置。

## 来源文档

- [Flow Agent API](../../raw/application-api-reference/flow-agent-api.md)


