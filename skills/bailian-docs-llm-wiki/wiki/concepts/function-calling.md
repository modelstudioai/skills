# 函数调用（Function Calling）

函数调用（Function Calling）是指大模型在推理过程中，根据用户输入、工具名称与工具描述判断是否需要调用外部工具（函数/API），并生成结构化的调用参数，再将工具返回结果并入上下文以生成最终回复的能力。它是弥补大模型在实时信息获取、精确计算、外部系统操作等原生局限的核心机制。

## 在百炼平台的使用场景

百炼平台在多个层面暴露和使用函数调用能力：

- **文本生成模型**：所有通用文本模型（如 `qwen3.7-plus`、`qwen3.6-flash`、`qwen3.7-max`）均支持 Function Calling。此外平台还提供免复杂配置的内置工具（联网搜索、代码解释器、网页抓取），开箱即用。
- **API 接口层**：函数调用通过不同接口协议暴露，字段约定各有差异：
  - **OpenAI 兼容 Chat Completions**：以 OpenAI 的 `tools` / `tool_calls` 字段约定描述工具与调用结果，迁移成本最低。
  - **OpenAI 兼容 Responses**：内置联网搜索、代码解释器、网页内容提取等工具，并自动管理对话历史，无需手动维护上下文。
  - **Anthropic 兼容 Messages**：以 tool use 形式支持工具调用，适合 Anthropic 生态应用。
  - **DashScope 原生接口**：功能与参数最完整，是使用平台全部工具能力时的首选。
- **实时多模态（Qwen-Omni-Realtime）**：基于 WebSocket 的实时 API 同样支持工具调用（Function Calling）。模型触发调用后通过 `response.function_call_arguments.done` 服务端事件返回调用参数，客户端执行工具后再用 `conversation.item.create` 事件将结果回传给模型。
- **应用构建（智能体 / 工作流）**：
  - **智能体应用（Agent）/ Assistant API**：模型根据输入、工具名称与描述自主判断是否调用，动态选择并规划调用顺序；新版智能体（Agent 2.0）把知识库、MCP、插件统一为“工具”交由模型自主编排。
  - **工作流应用**：工具作为编排节点按预定义流程执行，调用顺序由用户编排而非模型规划。
- **插件（Plug-in）**：调用插件的本质就是通过函数调用触发插件下的工具（如 `code_interpreter`、`calculator`、`quark_search` 等）。模型依据工具描述决定调用哪个工具。

## 关键参数与配置

- **工具定义**：需为每个工具提供名称、功能描述与参数 Schema。工具描述质量直接影响模型判断是否/如何调用。
- **模型能力要求**：应选用具备强工具调用能力的模型。插件调用目前支持 `qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max`、`qwen-vl-plus` 等；智能体推荐千问-Max 系列。
- **思考模式**：可通过 `enable_thinking` 开启（Responses API 用 `reasoning.effort` 控制），配合工具调用完成“规划-执行-反思”链路。
- **ReAct 最大轮次**：智能体中取值 1-50，限制单次会话内工具调用的最大次数。
- **实时 API 事件**：VAD/Manual 模式下通过 `session.update` 配置工具；调用参数由 `response.function_call_arguments.done` 返回，结果经 `conversation.item.create` 回传。
- **调用约束**：每个智能体应用最多可添加 10 个工具；旧版智能体的自定义插件有 5 秒超时限制。

## 开发者实践建议

- 迁移已有 OpenAI/Anthropic 应用时，优先选用对应生态的兼容接口，注意核对不同接口的工具字段映射差异。
- 需要联网搜索、代码解释器等内置工具时，使用 Responses 接口而非普通 Chat Completions。
- 需要最完整的工具能力与参数控制时，使用 DashScope 原生接口。
- 编写清晰、无歧义的工具描述，是提升模型正确触发函数调用的关键。

## 关联主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [model experience](../guides/model-experience.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [llm application](../guides/llm-application.md)
- [plug in](../guides/plug-in.md)


