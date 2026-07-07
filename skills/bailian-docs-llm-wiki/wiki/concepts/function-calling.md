# 函数调用（Function Calling）

函数调用（Function Calling）是大模型与外部工具交互的核心机制：开发者在请求中声明可用的函数（工具）定义，模型根据用户输入自主判断是否需要调用某个函数，并输出结构化的调用参数，由应用侧执行后将结果回传模型以生成最终回答。

## 工作原理

函数调用的典型流程分为三步：

1. **声明工具**：开发者在 API 请求中通过 `tools` 字段传入函数名称、描述和参数 JSON Schema。
2. **模型决策**：模型分析用户输入与工具描述，判断是否需要调用工具。如需调用，模型输出 `tool_calls`（包含函数名与参数），而非直接生成文本回答。
3. **执行与回传**：应用侧根据 `tool_calls` 执行实际函数，将返回结果以 `tool` 角色消息追加到对话历史，再次请求模型生成最终回答。

模型本身不执行函数，仅负责决策和参数生成；实际执行完全在应用侧完成。

## 在百炼平台的使用场景

### OpenAI 兼容 Chat Completions 接口

通过标准 `tools` 和 `tool_choice` 字段定义函数，支持非流式与流式调用。开发者只需将 `api_key`、`base_url`、`model` 替换为百炼的值，即可复用现有 OpenAI function call 代码。支持的模型包括 Qwen 系列商业版与开源版、DeepSeek、Kimi、GLM 等。

### OpenAI 兼容 Responses 接口

Responses 接口在函数调用基础上进一步内置了联网搜索、代码解释器、网页内容提取等工具，开箱即用，无需自行定义。平台自动管理对话历史，简化了多轮工具调用的上下文维护。

### Anthropic 兼容 Messages 接口

兼容 Anthropic Messages API 的工具调用协议，支持 thinking 与 tool use，适合从 Anthropic 生态迁移的开发者。

### DashScope 原生接口

百炼原生接口提供最完整的参数支持，适合需要使用全部采样参数、插件或业务字段的场景。

### 插件系统

百炼插件本质上是对函数调用的平台级封装。每个插件包含一个或多个工具，在智能体应用中由模型自动判断是否调用。支持官方插件（如代码解释器、夸克搜索、计算器）、三方插件和自定义插件。单个智能体应用最多可添加 10 个工具。

### MCP 服务

模型上下文协议（MCP）为函数调用提供了标准化的工具接入通道。通过 MCP，智能体可接入海量第三方工具而无需逐一编写接口。单个智能体最多同时添加 5 个 MCP 服务。

### 实时[多模态](multimodal.md)交互

Qwen-Omni-Realtime API 在 WebSocket 长连接中支持函数调用。模型在实时语音对话过程中可触发工具调用，客户端执行后通过 `conversation.item.create` 回传结果，再发送 `response.create` 让模型继续生成响应。

### Managed Agents API

托管智能体运行时中，函数调用通过 Event 机制实现。用户消息、工具调用回执、函数执行结果等均以事件形式在会话中流转，支持 SSE 流式推送。

## 关键参数与配置

| 参数 | 说明 |
| --- | --- |
| `tools` | 工具定义数组，每个元素包含 `type`（通常为 `function`）、`function.name`、`function.description` 和 `function.parameters`（JSON Schema） |
| `tool_choice` | 控制模型的工具调用策略：`auto`（模型自主决定）、`none`（禁止调用）、或指定某个函数名（强制调用） |
| `tool_calls` | 模型返回的调用指令，包含 `id`、`function.name` 和 `function.arguments` |
| `parallel_tool_calls` | 是否允许模型在单次响应中并行调用多个函数 |

## 注意事项

- **Token 消耗**：工具定义和工具返回结果都会占用上下文窗口中的 Token，工具数量较多时需注意输入 Token 的增长。
- **模型兼容性**：不同模型对函数调用的支持程度不同，建议使用 Qwen-Plus、Qwen-Max 等较强的推理模型以获得更准确的调用决策。
- **描述质量**：函数名称和描述的清晰度直接影响模型的调用准确性，建议在描述中明确说明函数用途、参数含义和返回值格式。
- **接口差异**：Responses 接口内置工具开箱即用，Chat Completions 和其他接口需自行定义工具；从不同平台迁移时应先确认目标接口对 `tools` 参数的支持情况。

## 关联主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [plug in](../guides/plug-in.md)
- [model context protocol](../guides/model-context-protocol.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [managed agents api](../api/managed-agents-api.md)


