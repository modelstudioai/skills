# 函数调用

函数调用（Function Calling）是大模型根据用户意图自动选择并调用外部工具（API、代码、数据库等），再将工具返回结果纳入上下文继续生成回复的能力。它是构建智能体、[工作流](workflow.md)和多工具协同场景的核心机制，使大模型能够突破自身在获取实时信息、精确计算和操作外部系统上的局限。

## 在百炼平台的使用方式

百炼平台在多个层次提供函数调用能力，开发者可按集成形态和接口协议选择：

### 1. 通过模型 API 直接定义工具

在 OpenAI 兼容 Chat Completions 接口中，通过请求体的 `tools` 字段按 OpenAI function call 协议自定义工具 schema，模型在响应中返回 `tool_calls`，调用方执行后回传结果，模型继续生成。DashScope 原生接口对参数支持最完整，适合需要最全采样参数或业务字段的场景。Anthropic 兼容 Messages 接口同样支持思考（thinking）与工具调用。

> 仅 OpenAI 兼容 Responses 接口内置联网搜索、代码解释器、网页内容提取等工具，开箱即用；Chat Completions 与 Messages 接口如需这些能力，需自行定义工具或通过协议接入。

### 2. 通过插件调用

百炼插件本质上是「工具集合」，一个插件下可包含多个工具。模型根据用户输入、工具名称与工具描述判断是否调用、调用哪个工具，应用内部完成调用后将结果与用户内容合并再次输入模型。插件支持智能体应用、[工作流](workflow.md)应用与 Assistant API 三种调用形态，每个智能体最多可添加 10 个工具。

### 3. 通过 MCP 服务

模型上下文协议（MCP）提供统一的标准协议接入外部工具。智能体根据输入对话自动判断是否调用 MCP 服务，单个智能体最多同时添加 5 个 MCP 服务。[工作流](workflow.md)中每个 MCP 节点只能使用一个工具，需手动指定输入参数并把输出传递到下一个节点。MCP 服务不能在直接调用千问 API 时接入，只能在智能体或工作流应用中使用。

### 4. 在实时多模态与托管智能体中

Qwen-Omni-Realtime API 通过 WebSocket 长连接支持工具调用（Function Calling），与语音、视频、图像交互融合。Managed Agents API 由平台托管会话、沙箱与工具执行，开发者通过 Agent、Environment、Skill、Session 等资源管理工具调用生命周期，无需自建调度与执行基础设施。

## 关键参数与配置

- **`tools` / `tool_choice`**：在 Chat Completions 与 Messages 接口中定义可用工具及调用策略（`auto`、`required`、指定函数名等）。
- **`model`**：不同模型对工具调用的兼容性有差异，Qwen 系列中 `qwen-turbo` / `qwen-plus` / `qwen-max` / `qwen-vl-max` / `qwen-vl-plus` 均支持插件调用；最新兼容性以控制台实际执行结果为准。
- **工具 ID**：通过 API 调用插件工具时需正确传递工具 ID（如 `calculator`、`code_interpreter`），可在插件详情页「插件工具」下获取。
- **MCP 配置**：`mcpServers` 结构中 `type`（`stdio` / `streamable-http`）、`command`/`args`、`url`、`env` 等决定服务部署与连接方式。
- **提示词**：模型需明确指令才能准确调用工具，建议在提示词中写明工具名称与能力；若仍无效可更换更强的推理模型（如千问 3 系列）。

## 限制和注意事项

- **功能完整度差异**：兼容接口为保证协议一致性，可能不暴露百炼原生的全部参数；如需最全工具相关参数建议改用 DashScope 原生接口。
- **对话历史管理**：仅 Responses 接口自动维护历史，迁移到其他接口时需自行管理上下文长度，避免超出模型[上下文窗口](context-window.md)。
- **Token 消耗增加**：调用工具会将工具返回内容作为上下文传入模型，导致输入 Token 增加，并可能间接增加输出 Token，需关注计费与限流。
- **调用准确性依赖提示词**：模型需明确指令才能准确调用工具，建议在提示词中写明工具名称与能力；若仍无效可更换更强的推理模型。
- **网络与本地资源**：MCP 服务托管在函数计算 FC，无固定出口公网 IP，无法访问用户本地数据库；Python 代码解释器不支持对外访问网络及上传本地文件。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [model context protocol](../guides/model-context-protocol.md)
- [plug in](../guides/plug-in.md)
- [managed agents api](../api/managed-agents-api.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


