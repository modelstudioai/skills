# 函数调用

函数调用（Function Calling）是大模型与外部工具交互的核心机制，允许模型在对话过程中根据用户意图自主决定调用预定义的函数或工具，获取实时数据或执行特定操作后再生成最终回复。

## 基本原理

函数调用的典型流程为：

1. 开发者在请求中定义一组可用工具（函数名称、描述、参数 schema）。
2. 模型根据用户输入判断是否需要调用工具，若需要则输出结构化的函数名与参数。
3. 客户端执行实际的函数调用，将返回结果回传给模型。
4. 模型结合工具返回结果生成最终回复。

这一机制使大模型能够突破自身在实时信息获取、精确计算、外部系统操作等方面的局限。

## 在百炼平台的使用场景

### 通过 API 接口调用

百炼提供多种兼容接口，均支持函数调用能力：

| 接口 | 函数调用方式 |
| --- | --- |
| OpenAI 兼容 Chat Completions | 通过 `tools` 参数定义工具列表，模型返回 `tool_calls` 结构 |
| OpenAI 兼容 Responses | 内置联网搜索、代码解释器、网页内容提取等工具，开箱即用；也支持自定义工具 |
| Anthropic 兼容 Messages | 兼容 Anthropic 工具调用协议，支持思考模式与工具调用 |
| DashScope 原生 | 功能集最完整，参数支持最丰富 |

其中 Responses 接口内置的联网搜索、代码解释器等为平台托管工具，无需开发者自行实现函数逻辑；其他接口需按各自协议自行定义工具。

### 在实时[多模态](multimodal.md)交互中使用

Qwen-Omni-Realtime API 支持在 WebSocket 实时会话中使用函数调用。当模型判断需要调用工具时，服务端会在响应中输出工具调用请求，客户端完成实际调用后，通过 `conversation.item.create` 事件将结果回传，再发送 `response.create` 触发模型继续生成。这种机制使语音对话场景也能接入外部数据源和服务。

### 在智能体应用中使用

百炼智能体应用将函数调用作为核心能力之一：

- **Agent 2.0**：将知识库、MCP 服务、插件等统一为工具，由模型自主规划调用顺序，支持完整的"规划-执行-反思"链路。通过 ReAct 最大轮次参数（1-50）限制单次会话中工具调用的最大次数。
- **Agent 1.0**：先检索知识库，再决策是否调用插件工具，适用于流程固定的简单任务。

### 在工作流应用中使用

工作流中的插件节点和 MCP 节点本质上也是函数调用，区别在于调用顺序由用户编排的流程决定，而非由模型自主规划。

### 通过插件体系使用

百炼插件是函数调用在平台层的封装。每个插件包含一个或多个工具（API），模型根据工具名称和描述自动判断是否调用。官方插件包括 Python 代码解释器、计算器、夸克搜索、图片生成等，均可在智能体中直接关联使用。

### 通过 MCP 协议使用

模型上下文协议（MCP）为函数调用提供了标准化的传输层。百炼支持官方 MCP 服务和自定义 MCP 服务，单个智能体最多可同时接入 5 个 MCP 服务，工作流中每个 MCP 节点使用一个工具。

## 关键参数与配置

### API 层面

- **`tools`**：工具定义数组，每个工具包含 `type`（固定为 `function`）、`function.name`、`function.description` 和 `function.parameters`（JSON Schema 格式）。
- **`tool_choice`**：控制模型的工具调用策略，可选 `auto`（模型自主决定）、`none`（禁止调用）或指定特定函数名。
- **`parallel_tool_calls`**：是否允许模型在一次回复中并行调用多个工具。

### 应用层面

- **ReAct 最大轮次**：智能体应用中限制单次会话的工具调用次数上限（1-50），超出后自动生成最终回复。
- **工具数量限制**：每个智能体应用最多添加 10 个插件工具，最多 5 个 MCP 服务。

## 支持的模型

函数调用能力对模型有一定要求，目前支持的主要模型包括：

- Qwen 系列：qwen-max、qwen-plus、qwen-turbo 及其变体
- Qwen3 系列：qwen3-max、qwen3.7-max、qwen3.7-plus 等
- Qwen-VL 系列：qwen-vl-max、qwen-vl-plus
- Qwen-Omni-Realtime 系列：支持实时语音场景下的工具调用
- 部分三方直供模型（DeepSeek、Kimi、GLM、MiniMax 等）

建议选用具备强工具调用能力的模型（如千问-Max 系列）以获得更好的调用准确性。

## 注意事项

- 函数调用会增加 [Token](token.md) 消耗：工具定义和工具返回内容均计入输入 [Token](token.md)。
- 调用准确性依赖工具描述的质量，建议在描述中明确工具的功能、适用场景和参数含义。
- 不同接口的工具调用能力存在差异，Responses 接口内置工具最丰富，DashScope 原生接口参数支持最全。
- 自定义插件有超时限制（旧版智能体为 5 秒），需确保工具响应速度。

## 关联主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [plug in](../guides/plug-in.md)
- [llm application](../guides/llm-application.md)
- [model context protocol](../guides/model-context-protocol.md)


