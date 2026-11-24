# flow agent api

Flow Agent API 是百炼平台提供的用于调用流程化智能体（Flow Agent）的核心接口，支持将预定义的多步骤工作流（含条件分支、工具调用、记忆管理等）以 HTTP 方式集成到业务系统中。该 API 采用 RESTful 设计，兼容标准 OAuth2 认证与结构化请求/响应格式。适用于需要可控执行逻辑、可审计调用链路及与企业已有系统深度集成的场景。

## 支持的模型与功能

- 当前仅支持百炼平台托管的 Flow Agent 实例（即通过控制台「智能体编排」创建并发布的流程），不支持直接调用基础大模型或自定义 LLM 接口。
- 支持的功能包括：同步执行（`/v1/flow_agent/run`）、异步执行与结果轮询（`/v1/flow_agent/run_async`）、输入变量注入、运行时上下文覆盖、以及基于 [Prompt 模板](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-prompt-engineering.md) 的动态提示工程。
- [长期记忆](../concepts/long-term-memory.md)能力已迁移至统一向量知识库接口，原 [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md) 文档中的 `/memory/*` 路由已废弃，实际应使用 `knowledge_base_id` 参数关联知识库实例。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `agent_id` | string | 是 | Flow Agent 的唯一标识（非应用 ID），可在控制台「智能体详情」页获取。注意该字段与 [概览](../../raw/application-api-reference/flow-agent-api/flow-agent-api-overview.md) 中描述的 `application_id` 不同，勿混淆。 |
| `inputs` | object | 否 | JSON 对象，键为流程中定义的输入变量名，值为对应字符串或结构化数据（如 `{"query": "北京天气", "user_id": "u123"}`）。 |
| `stream` | boolean | 否 | 默认 `false`；设为 `true` 时启用 Server-Sent Events (SSE) 流式响应，适用于长流程实时反馈。 |
| `timeout` | integer | 否 | 单位秒，最大值 300；超时后服务终止执行并返回 `504 Gateway Timeout`。 |

> **注意**：`agent_id` 字段在 [认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md) 文档中曾被误标为 `app_id`，该表述已过时，请以控制台实际展示和本节为准。

## 使用方式

1. **认证**：使用 `Authorization: Bearer <access_token>` 请求头，`access_token` 需通过百炼平台 OAuth2 接口获取（参见 [认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md)）；
2. **发起调用**：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/flow_agent/run \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
           "agent_id": "agt-xxx",
           "inputs": {"query": "总结会议纪要"},
           "stream": false
         }'
   ```
3. **错误处理**：所有错误均遵循统一错误码规范，详见 [错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)。

## 限制和注意事项

- 单次请求 `inputs` 总大小上限为 1MB；单个输入字段值长度建议不超过 10KB，避免触发内部截断。
- 同步接口（`/run`）最大执行时长为 120 秒；超出需改用 `/run_async` 并配合轮询机制。
- Flow Agent 内部若调用外部工具（如 HTTP 工具节点），其超时与重试策略由 Agent 配置决定，API 层不可覆盖。
- 所有调用日志默认保留 7 天，如需长期审计，请自行记录 `request_id` 并关联 [应用调用](../../raw/application-api-reference/flow-agent-api/application-call.md) 文档中定义的回调或日志导出路径。

## 来源文档

- [Flow Agent API](../../raw/application-api-reference/flow-agent-api.md)


