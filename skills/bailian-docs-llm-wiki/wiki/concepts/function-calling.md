# 函数调用

函数调用（Function Calling）是百炼平台中大模型主动识别用户意图、自主决策并触发外部工具执行的关键能力。它将自然语言请求转化为结构化函数调用请求，由模型生成符合规范的 `tool_calls`，再由平台调度执行、注入结果，最终生成自然语言响应，实现“规划—调用—推理—合成”的闭环。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台并非单一接口能力，而是贯穿多个核心服务的统一语义机制，具体体现为：

- **Managed Agents（托管智能体）**：Agent 运行时，模型根据 `skills` 列表中注册的工具描述，自主决定是否调用及构造参数；调用事件以 `tool_call` 类型出现在 `/sessions/{id}/events` 流中，开发者需监听并同步回传 `tool_result` 事件完成闭环。
- **Plug-in（插件）**：插件即标准化的函数封装单元。无论是官方 `calculator`、三方 `quark_search`，还是自定义 HTTP 工具，均通过 `tools` 字段声明，由模型按需触发；参数来源支持“大模型识别”（从对话中抽取）或“业务透传”（通过 `biz_params` 显式传入）。
- **Omni Realtime API（实时多模态）**：在 WebSocket 会话中，通过 `session.update` 的 `tools` 参数启用函数调用；模型触发后，服务端推送 `tool.call` 事件，客户端必须在规定超时内返回 `tool.result`，否则会话中断；注意：`enable_search` 与 `tools` 互斥，不可同时启用。
- **Application Call（应用调用）**：新版智能体/工作流应用调用时，可在 `tools`（Responses API）或 `biz_params.user_defined_params`（DashScope API）中声明可用函数；RAG 检索、[长期记忆](long-term-memory.md)等高级能力虽非传统函数，但其调用逻辑同样遵循“声明—触发—注入”范式，由平台自动编排。
- **Qwen 原生 API（模型直连）**：仅 Responses API 和 Anthropic Messages 接口完整支持函数调用（含 `tool_choice`、`tool_calls`、`tool_result` 全生命周期）；OpenAI 兼容的 Chat Completions 接口**不支持**函数调用，切勿混用。

> ✅ 统一行为：所有场景下，模型仅生成调用请求（不含执行），执行、鉴权、错误处理均由百炼平台完成；开发者只需关注工具定义、事件监听与结果回传。

## 关键参数和配置

| 参数 | 位置 | 类型 | 说明 | 必填性 |
|------|------|------|------|--------|
| `tools` | 请求体（`tools` 字段） | `array` of `object` | 工具定义列表，每个对象含 `name`（全局唯一ID）、`description`（功能说明）、`parameters`（JSON Schema 描述输入结构） | 是（启用调用时） |
| `tool_choice` | 请求体 | `string` 或 `object` | 控制调用策略：`"auto"`（默认，模型自主决策）、`"none"`（禁用）、`{"type": "function", "function": {"name": "xxx"}}`（强制指定） | 否（默认 auto） |
| `name` | `tools[i]` 内 | `string` | 工具唯一标识符，如 `"code_interpreter"`、`"github_search"`；长度 ≤20 字符 | 是 |
| `parameters` | `tools[i]` 内 | `object` (JSON Schema) | 定义输入参数名、类型、是否必需、描述；`Object` 类型子属性**不可为空**，需显式展开 | 是（若工具需参数） |
| `biz_params` / `user_defined_params` | 请求体（DashScope）或 `extra_body`（Responses） | `object` | 用于透传业务上下文参数，可被模型在 `tool_calls` 中引用，或直接注入到工具请求体/Query/Header 中 | 否（按需） |
| `tool_result` | 回传事件/请求体 | `object` | 包含 `tool_call_id`（匹配原始调用）和 `content`（字符串或 JSON 对象）；内容将被模型用于生成最终响应 | 是（响应调用事件时） |

> ⚠️ 注意事项：
> - 所有工具参数**必须填写完整描述**，缺失将导致发布失败（错误码 `130040`）；
> - GET 类工具**不支持 `Object` 类型输入参数**（错误码 `130022`）；
> - 自定义工具鉴权（Header/Query/Bearer）需在插件配置中预设，不可在运行时动态覆盖；
> - 单次会话中，模型最多发起 5 次函数调用（受模型与环境限制，超限将终止流程）。

## 面向开发者，简洁实用

- **定义工具，而非写胶水代码**：专注描述“做什么”（`description`）和“要什么”（`parameters` Schema），平台自动处理序列化、HTTP 调用、超时重试与错误注入。
- **监听事件，而非轮询状态**：在 Managed Agents 和 Omni Realtime 中，使用 SSE 或 WebSocket 监听 `tool_call` 事件，立即响应 `tool_result`，避免阻塞。
- **复用优先，避免重复造轮子**：优先选用官方插件（如 `code_interpreter`、`text_to_image`），它们已预置安全沙箱与性能优化；自定义工具应遵循 MCP 规范，便于跨应用复用。
- **调试技巧**：开启 `enable_thinking`（新版智能体）或使用 Anthropic Messages 接口，可查看模型生成 `tool_calls` 的推理过程，快速定位描述歧义或参数缺失问题。
- **生产就绪检查项**：确认工具 `name` 全局唯一、`parameters` Schema 无空嵌套、`biz_params` 透传路径与提示词中模板语法（如 `{{biz_params.xxx}}`）严格一致。

## 关联主题页

- [managed agents api](../api/managed-agents-api.md)
- [plug in](../guides/plug-in.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [application call](../api/application-call.md)
- [qwen api reference](../api/qwen-api-reference.md)


