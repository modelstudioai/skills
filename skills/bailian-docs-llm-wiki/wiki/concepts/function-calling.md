# 函数调用

函数调用（Function Calling）是大模型根据用户输入和预定义的工具描述，自主决定是否调用外部函数并生成结构化调用参数的能力。它是百炼平台实现工具调用、智能体编排和插件集成的底层机制。

## 在百炼平台中的使用场景

### API 直接调用

通过 Chat Completions 接口调用时，开发者在请求的 `tools` 参数中声明可用函数（名称、描述、参数 JSON Schema），模型根据对话上下文判断是否需要调用，并在响应中返回函数名和参数。开发者执行函数后将结果追加到消息列表，再次请求模型生成最终回复，支持多轮工具调用。

各接口对函数调用的支持情况：

- **OpenAI 兼容 Chat Completions**：通过 `tools` 参数支持，兼容 OpenAI SDK 的 function calling 字段约定。
- **Anthropic 兼容 Messages**：以 tool use 形式支持，字段遵循 Anthropic 协议。
- **DashScope 原生接口**：参数支持最完整，适合需要精细控制调用行为的场景。
- **OpenAI 兼容 Responses**：除自定义函数外，还内置联网搜索、代码解释器等平台工具，自动管理调用流程。

### 智能体应用与工作流

在百炼应用层面，函数调用是智能体（Agent）的核心运行机制：

- **智能体应用（Agent 2.0）**：知识库、MCP 工具、插件、内置工具均统一为工具，由模型基于函数调用能力自主规划调用顺序。系统提示词中应明确提及工具名称及使用时机以引导调用。ReAct 最大轮次（1-50）限制单次会话中工具调用的最大次数。
- **工作流应用**：插件作为工作流节点按预定义流程执行，不依赖模型主动规划，属于确定性调用。
- **Assistant API**：通过工具 ID 调用插件，底层同样基于模型的函数调用判断。

### Managed Agents API

在托管智能体运行时中，函数调用由平台沙箱执行。Session 内的 Event 记录包含工具调用回执，开发者可通过 `POST /sessions/{session_id}/events` 注入函数执行结果，平台驱动"规划-执行-反思"循环直至任务完成。

### 插件调用

百炼插件（官方、三方、自定义）本质上是函数的集合。模型根据用户输入、工具名称和工具描述判断是否调用；需要调用时选择合适工具，应用内部完成调用后将结果与用户内容合并再次输入模型生成最终回复。每个智能体应用最多添加 10 个工具。

## 支持函数调用的模型

- **文本生成**：Qwen3 及以上通用模型均支持 Function Calling，推荐 `qwen3.7-plus` 起步（完整 Function Calling 与内置工具支持）。
- **视觉理解**：Qwen3.7/3.6/3.5 及 Qwen-VL 系列支持。
- **语音实时对话**：`qwen-audio-3.0-realtime-plus` 支持 Function Calling。
- **意图理解**：`tongyi-intent-detect-v3` 可同时输出意图与函数调用信息。
- **GUI 交互**：`gui-plus` 通过 `computer_use` 工具定义实现界面操作调用。

插件场景目前支持 qwen-turbo、qwen-plus、qwen-max、qwen-vl-max、qwen-vl-plus。

## 关键参数与配置

| 参数 | 位置 | 说明 |
| --- | --- | --- |
| `tools` | 请求体 | 函数声明数组，每个元素包含函数名称、描述和参数 Schema |
| `tool_choice` | 请求体 | 控制调用策略（自动/强制/指定函数），具体取值以接口文档为准 |
| `tool_calls` | 响应体 | 模型返回的调用请求，含函数名和 JSON 格式参数 |
| `role: "tool"` | messages | 将函数执行结果回传模型的消息角色 |
| ReAct 最大轮次 | 智能体应用配置 | 限制单次会话工具调用次数（1-50） |
| 工具 ID | 插件/Assistant API | 调用插件工具时的唯一标识（如 `calculator`） |

## 开发建议

- 函数描述应清晰准确，模型依赖描述判断调用时机；参数 Schema 越严格，生成的调用参数越可靠。
- 多步任务推荐选用工具调用能力强的模型（如千问-Max 系列），并在提示词中引导工具使用。
- 开启思考模式（`enable_thinking`）有助于提升智能体的工具规划与反思效果。
- 跨接口迁移时注意字段映射差异：DashScope 参数最全，OpenAI/Anthropic 兼容接口以对应生态约定为准。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [more models](../api/more-models.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [plug in](../guides/plug-in.md)
- [model experience](../guides/model-experience.md)
- [managed agents api](../api/managed-agents-api.md)
- [llm application](../guides/llm-application.md)



