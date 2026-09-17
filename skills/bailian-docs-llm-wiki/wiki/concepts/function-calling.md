# 函数调用

函数调用（Function Calling）是百炼平台支持的一种关键能力，允许大语言模型在推理过程中自主识别用户意图、生成结构化工具调用请求，并将结果交由外部系统执行，最终融合返回自然语言响应。它不是简单的 API 封装，而是模型原生具备的语义理解与动作规划能力，是构建可执行智能体（Agent）、自动化工作流和生产级 RAG 应用的核心机制。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中并非独立服务，而是深度集成于多个核心能力模块，其触发、定义、执行与响应流程因场景而异：

- **智能体（Agent）应用**：在新版/旧版智能体中，函数调用作为「工具调用（tool_calling）」阶段自动发生。模型根据 `system` 提示词中声明的工具列表（`tools`）及当前对话上下文，输出符合 OpenAI Function Calling Schema 的 JSON 结构（含 `function.name` 和 `function.arguments`）。平台自动解析、路由并调用开发者配置的后端函数（如知识库检索、数据库查询、第三方 API），再将结果注入后续生成阶段。该过程对开发者透明，仅需在控制台或 API 中声明工具即可。

- **知识问答（RAG Agent）**：在 `/api/v2/apps/knowledge/chat` 接口中，函数调用体现为内置工具链（如 `semantic_search`、`execute_sql`、`obtain_file`）的自动调度。模型无需显式定义 `tools`，而是基于知识库元数据和用户问题动态选择并调用合适工具，实现多跳推理与证据整合。开发者通过知识库配置和 agent_options 控制工具可用性，不直接编写函数定义。

- **实时语音交互（Omni Realtime API）**：在 WebSocket 会话中，通过 `session.update` 事件传入 `tools` 数组启用函数调用。模型在语音或文本输入后，可主动触发工具（如查天气、订会议室），客户端需监听 `response.function_call` 事件、执行本地逻辑、并通过 `function_call.result` 事件回传结果。此模式要求全双工、低延迟处理，适用于语音助手等强交互场景。

- **标准模型 API（`/v1/chat/completions`）**：当使用支持 `function-calling` 能力的模型（如 `qwen-max`、`qwen-plus`、`qwen3.5-omni-plus-realtime`）时，开发者需在请求 `messages` 外显式传入 `tools` 参数（OpenAI 格式）及可选 `tool_choice`（`auto`/`required`/`{"type":"function","function":{"name":"xxx"}}`）。模型返回 `finish_reason: "tool_calls"`，响应体中包含 `message.tool_calls` 字段，开发者需自行解析、调用、拼接并发起下一轮请求（若需继续生成）。

- **工作流（Workflow）**：函数调用以「节点」形式显式编排。开发者在控制台拖拽「函数调用」节点，配置目标函数 URL、认证方式、输入映射（Jinja2 模板）和错误重试策略。模型本身不参与决策，而是由工作流引擎根据上一节点输出（如 LLM 生成的 JSON 参数）驱动函数执行。此模式强调确定性与可观测性，适合需要人工审核或复杂错误处理的业务流程。

## 关键参数和配置

| 参数 | 位置 | 类型 | 说明 | 是否必需 |
|------|------|------|------|----------|
| `tools` | 请求体（`/v1/chat/completions`、Omni `session.update`、Agent `parameters.tools`） | array | 工具定义数组，每个元素为 OpenAI Function Calling Schema 对象，含 `function.name`、`description`、`parameters`（JSON Schema） | 启用函数调用时必需 |
| `tool_choice` | 请求体（仅 `/v1/chat/completions`） | string / object | 控制模型行为：`"auto"`（默认，由模型决定）、`"none"`（禁用）、`"required"`（必须调用）、或指定具体函数名的对象 | 否（但推荐显式设置以提升可控性） |
| `parameters.tools` | 知识问答/智能体请求体 `parameters` 内 | array | 同 `tools`，用于覆盖应用级默认工具集 | 否（应用内已配置则可省略） |
| `function_call.result` | Omni Realtime API 客户端事件 | object | 客户端执行完工具后，通过此事件回传结果，格式为 `{ "tool_call_id": "...", "result": ... }` | 工具调用后必需 |
| `X-DashScope-SSE: enable` | HTTP Header（流式场景） | string | 启用 Server-Sent Events 流式响应，函数调用相关事件（如 `tool_calling`）通过 `event: tool_calling` 帧推送 | 流式调用时必需 |

> **注意**：所有工具参数（`parameters` 字段）必须严格遵循 JSON Schema 规范，平台不校验运行时值合法性；`function.name` 必须与后端函数标识完全一致（区分大小写）；`tool_call_id` 由平台生成，客户端回传时必须原样复用，否则视为无效响应。

## 面向开发者，简洁实用

- **快速验证**：用 `qwen-plus` 模型 + 最小 `tools` 定义（一个带 `name` 和 `description` 的空参函数）调用 `/v1/chat/completions`，观察响应中是否出现 `tool_calls` 字段。
- **错误容错**：流式响应中 `delta.content` 可能为空（尤其在 `tool_calling` 帧），务必检查 `delta.tool_calls`；非流式响应需判断 `finish_reason === "tool_calls"` 再解析 `message.tool_calls`。
- **安全边界**：函数调用不自动执行，所有 `tool_calls` 输出均为模型建议，必须由你（开发者）完成鉴权、参数校验、网络调用与结果清洗，严禁直接 `eval()` 或反射执行。
- **调试技巧**：在 `system` 消息中加入明确指令，如“你只能调用以下工具，禁止自行编造工具名”，可显著降低幻觉调用率。
- **性能提示**：函数调用会增加端到端延迟，单次请求中避免定义过多工具（建议 ≤10 个），高频场景优先考虑预计算或缓存结果。

## 关联主题页

- [start using](../guides/start-using.md)
- [more about models](../api/more-about-models.md)
- [knowledge](../api/knowledge.md)
- [application call](../api/application-call.md)
- [omni realtime api](../api/omni-realtime-api.md)


