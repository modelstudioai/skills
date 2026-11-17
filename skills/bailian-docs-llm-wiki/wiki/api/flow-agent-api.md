# flow agent api

Flow Agent API 是百炼平台提供的核心能力接口，用于在应用中集成基于流程编排的智能体（Agent）调用能力。它支持将多个组件（如 LLM 调用、工具执行、条件分支等）按图结构串联，实现复杂任务的自动化执行。该 API 与百炼统一认证体系和应用生命周期管理深度集成，适用于构建对话式工作流、自动化客服、数据处理流水线等场景。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 等 Qwen 系列模型；不支持第三方模型或自定义模型直接接入 Flow Agent 执行节点。  
- **核心功能**：包括流程触发（`/v1/flows/run`）、异步状态轮询（`/v1/flows/runs/{run_id}`）、输入变量注入、节点级日志与 trace 查看。[长期记忆](../concepts/long-term-memory.md)能力已迁移至新版 [应用上下文管理](../../raw/application-api-reference/application-context.md)，旧版 [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md) 文档已过时，**请勿使用**。  
- **扩展能力**：支持通过 `tool_calls` 集成百炼内置工具（如搜索、数据库查询），也支持注册自定义 HTTP 工具（需符合 [应用组件 API 规范](../../raw/_short/api-bailian-2023-12-29-dir-others-b9c3a16db11771f5.md)）。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `flow_id` | string | 是 | 在控制台创建并发布的 Flow 唯一标识，非应用 ID 或版本 ID |
| `inputs` | object | 否 | JSON 对象，键名需与 Flow 编辑器中定义的「输入变量」名称严格一致；值将透传至首节点 |
| `stream` | boolean | 否 | 默认 `false`；设为 `true` 时返回 Server-Sent Events 流式响应（仅支持部分 Flow 类型） |
| `trace_id` | string | 否 | 用于链路追踪的自定义 ID，建议与上游系统保持一致 |

> **注意**：`inputs` 中若包含嵌套对象或数组，需确保其 schema 与 Flow 设计时声明的类型兼容，否则将触发 `400 Bad Request` 错误（详见 [错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)）。

## 使用方式

1. **认证**：所有请求需携带 `Authorization: Bearer <access_token>`，[Token](../concepts/token.md) 通过 [应用凭证管理](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md) 获取，有效期 2 小时。  
2. **发起调用**：向 `POST https://dashscope.aliyuncs.com/api/v1/flows/run` 发送 JSON 请求体。  
3. **获取结果**：同步模式下直接返回 `outputs` 字段；异步模式需轮询 `/v1/flows/runs/{run_id}` 直到 `status` 变为 `success` 或 `failed`。  
4. **调试建议**：首次集成时，推荐先在控制台使用「测试运行」功能验证 Flow 行为，再对接 API；调试日志可通过 `X-DashScope-Trace-ID` 头关联查看。

## 限制和注意事项

- 单次 Flow 运行最大超时时间为 300 秒（5 分钟），超时后自动终止并返回 `status: timeout`。  
- 每个 Flow 实例每秒最多接受 10 次并发调用（QPS 限流），超出将返回 `429 Too Many Requests`。  
- 不支持在 Flow 内部动态修改节点拓扑结构（如运行时增删节点），所有流程逻辑必须预先在控制台发布。  
- Prompt 模板不可通过 API 动态覆盖，必须在 Flow 编辑器中配置并发布新版本；相关规范见 [Prompt 模板](../../raw/_short/api-bailian-2023-12-29-dir-prompt-engineering-11ee962a5f5d5d1e.md)。  
- 当前不支持跨应用共享 Flow 实例，`flow_id` 作用域限定于创建该 Flow 的应用内。

## 来源文档

- [Flow Agent API](../../raw/application-api-reference/flow-agent-api.md)


