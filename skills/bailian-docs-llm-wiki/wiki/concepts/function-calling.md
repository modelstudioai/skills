# 函数调用（Function Calling / 工具调用）

函数调用（Function Calling，又称工具调用）是指大模型在生成回复的过程中，根据用户输入和工具描述自主判断是否需要调用外部工具（函数/API），并生成结构化的调用参数；应用执行工具后，将结果回传给模型，由模型合并结果生成最终答案。它是弥补大模型在实时信息获取、精确计算、图像处理、外部系统操作等原生局限的核心机制。

## 在百炼平台的使用场景

函数调用贯穿百炼的多种应用与接口，不同场景下的调用形态和控制粒度有所差异：

### [OpenAI 兼容接口](openai-compatible-interface.md)（Chat Completions / Responses）

- **Chat Completions** 标准对话接口支持 `function call`，模型可返回工具调用请求，适用于通用对话中的工具触发。
- **Responses** 接口是 Chat Completions 的演进版，内置联网搜索等工具，简化了上下文与工具管理，适合智能体场景。
- 迁移自 OpenAI 应用时，通常只需修改 `base_url`、`api_key`、`model` 三个参数即可复用原有的 function call 代码。

### 智能体应用（Agent）

- **新版智能体（Agent 2.0）**：将知识库、MCP、插件等能力统一抽象为工具，由智能体自主规划调用顺序，支持完整的「规划-执行-反思」链路。推荐使用具备强工具调用能力的模型（如千问-Max / 千问 3 系列）。通过「ReAct 最大轮次」（取值 1-50）限制单次会话中的工具调用次数。
- **旧版智能体（Agent 1.0）**：通过知识库（RAG）和插件扩展能力，先检索再决策是否调用工具；自定义插件有 5 秒超时限制。

### 工作流应用（Workflow）

在工作流中，插件 / MCP 以**节点**形式出现，按用户编排的顺序执行，需手动指定输入参数并把输出传递到下一节点，而非由模型主动规划调用。

### 插件（Plug-in）

插件是工具集合，一个插件可含多个工具（每个工具有唯一的工具 ID，如 `calculator`、`code_interpreter`、`quark_search`）。在智能体应用 / Assistant API 中，模型依据工具名称与描述判断是否调用；通过 API 调用时需正确传递工具 ID。单个智能体应用最多添加 10 个工具。

### MCP（Model Context Protocol）

MCP 是大模型与外部工具之间的统一信息通道，让智能体和工作流无需为每个工具单独编写接口即可接入海量第三方工具。单个智能体最多同时添加 5 个 MCP 服务。调用准确性高度依赖提示词，建议在提示词中写明工具名称与能力。

### Managed Agents（托管运行时）

平台在服务端托管会话状态与沙箱，智能体可自主调用内置工具（`bash`、`read`、`write`、`edit`、`glob`、`grep`、`download_file` 等 7 个内置工具）、MCP 服务和 Skill。工具调用过程与结果通过会话级 SSE 事件流实时推送，事件历史持久化，支持中断与续接。

### 实时[多模态](multimodal.md)（Omni-Realtime API）

基于 WebSocket 的实时音视频对话接口同样支持工具调用：模型通过服务端事件 `response.function_call_arguments.done` 返回工具调用参数，客户端执行工具后通过 `conversation.item.create` 事件回传结果。

## 关键参数与配置

| 场景 | 关键配置 | 说明 |
| --- | --- | --- |
| Chat Completions | `tools` / `function` | 声明可调用的工具及其参数 schema |
| 新版智能体 | ReAct 最大轮次（1-50） | 限制单次会话工具调用最大次数 |
| 智能体应用 | 工具数上限 10 | 应用会根据输入选择调用一个或多个工具 |
| MCP（智能体） | MCP 服务数上限 5 | 模型自动判断是否调用 |
| Managed Agents | `resources` 挂载 + SSE 事件流 | 沙箱路径约定 `/mnt/session/uploads` |
| Omni-Realtime | `session.update` 配置工具；`response.function_call_arguments.done` / `conversation.item.create` | 通过事件回传调用结果 |
| Managed Agents API | `POST /sessions/{session_id}/events` | 注入函数结果、工具审批等事件 |

## 面向开发者的实用建议

- **选强工具模型**：优先选用工具调用能力强的模型（千问-Max、千问 3 系列），弱模型易漏调或错调。
- **写清工具描述与提示词**：模型依据工具名称和描述决策，描述越明确，调用越准；MCP / 插件尤其依赖提示词中明确指令。
- **注意 Token 消耗**：工具返回内容会作为上下文回传模型，增加输入（并可能间接增加输出）Token。
- **控制调用轮次**：通过 ReAct 最大轮次等参数避免工具调用死循环。
- **区分自主调用与编排**：智能体 / Assistant API 由模型自主规划调用，工作流则由用户显式编排节点顺序。

## 关联主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [managed agents api](../api/managed-agents-api.md)
- [llm application](../guides/llm-application.md)
- [plug in](../guides/plug-in.md)
- [model context protocol](../guides/model-context-protocol.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [managed agents](../guides/managed-agents.md)


