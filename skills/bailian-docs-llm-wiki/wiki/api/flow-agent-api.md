# flow agent api

Flow Agent API 是百炼平台提供的用于调用流程型智能体（Flow Agent）的核心接口，支持将预定义的多步骤工作流封装为可编程服务。该 API 适用于需要结构化任务编排、状态保持与外部系统集成的场景，如客服工单处理、数据清洗流水线等。开发者可通过 HTTP 请求发起调用，并接收结构化的 JSON 响应。

## 支持的模型/功能

- 当前仅支持基于百炼自研的 `flow-agent-v1` 模型类型，不兼容通用大语言模型（如 `qwen-max`）直接作为 Flow Agent 调用目标；  
- 支持的功能包括：流程启动、多轮会话保持、节点级上下文注入、外部工具调用（需在 Flow 编辑器中预先配置）、以及基于 Prompt 模板的动态提示工程；  
- [长期记忆](../concepts/long-term-memory.md)能力已由新版向量存储机制替代，旧版 [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md) 文档中的 REST 接口已废弃，实际开发请参考 [Prompt 模板](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-prompt-engineering.md) 中的 `memory_context` 字段规范。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | Flow 应用在百炼控制台生成的唯一 ID，非模型 ID；需在 [应用调用](../../raw/application-api-reference/flow-agent-api/application-call.md) 文档中确认其获取方式 |
| `input` | object | 是 | 用户输入数据，结构需严格匹配 Flow 定义中首个节点的 `input_schema`；字段缺失或类型错误将导致 400 错误 |
| `session_id` | string | 否 | 用于维持多轮对话状态；若未提供，系统将自动生成新会话；同一 `session_id` 下的连续请求共享流程执行上下文 |
| `stream` | boolean | 否 | 默认 `false`；设为 `true` 时返回 SSE 流式响应，适用于长流程实时反馈场景 |

> **注意**：`input` 参数的 schema 校验逻辑在 v2.3.0 后升级为强约束模式，与早期 [概览](../../raw/application-api-reference/flow-agent-api/flow-agent-api-overview.md) 文档中“允许宽松传入”的描述存在不一致，请以实际 API 返回的 422 错误及 `validation_errors` 字段为准。

## 使用方式

1. 使用 API Key 进行认证（详见 [认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md)）；  
2. 构造 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/agents/{app_id}/invoke`；  
3. 设置 `Content-Type: application/json`，并在 body 中按上述关键参数格式组织 payload；  
4. 解析响应：成功时返回 `status: "success"` 及 `output` 对象；失败时依据 [错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md) 进行诊断。

## 限制和注意事项

- 单次请求最大 `input` 大小为 256 KB，超限将返回 `413 Payload Too Large`；  
- `session_id` 生命周期默认为 24 小时，过期后关联上下文自动清理；  
- 不支持跨 `app_id` 共享 session 或 memory，每个 Flow 应用的状态完全隔离；  
- 若流程中包含异步工具调用（如 HTTP 请求、数据库查询），整体超时时间默认为 60 秒，不可配置；  
- 所有调试日志与 trace 信息仅保留 7 天，生产环境建议自行集成 OpenTelemetry 上报。

## 来源文档

- [Flow Agent API](../../raw/application-api-reference/flow-agent-api.md)


