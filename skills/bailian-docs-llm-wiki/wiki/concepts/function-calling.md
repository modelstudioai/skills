# 函数调用

函数调用（Function Calling）是大模型根据用户输入自动选择并调用外部工具或 API 的能力。在百炼平台中，函数调用是连接大模型与外部系统的核心机制，使模型能够突破自身局限，执行实时数据查询、精确计算、代码运行等操作。

## 调用方式

百炼平台提供多种函数调用的接入路径，开发者可根据场景选择：

- **OpenAI 兼容 Chat Completions 接口**：通过 `tools` 参数定义可用函数列表，模型返回 `tool_calls` 指示需要调用的函数及参数。适合从 OpenAI 生态迁移的项目。
- **OpenAI 兼容 Responses 接口**：内置联网搜索、代码解释器等工具，无需手动定义函数即可使用，同时支持自定义工具。
- **DashScope 原生接口**：百炼原生接口，提供最完整的函数调用功能集和参数支持。
- **Anthropic 兼容 Messages 接口**：支持思考和工具调用，适合使用 Anthropic 生态的开发者。

## 应用场景

### 插件体系

百炼的插件机制是函数调用的典型实现。插件下的每个工具对应一个可调用的函数：

- **智能体应用**：大模型根据用户输入和工具描述自动判断是否触发函数调用，单次最多组合调用 10 个工具。
- **工作流应用**：将工具作为流程节点，按编排顺序执行，函数调用由流程控制而非模型主动规划。
- **Assistant API**：通过 `tools` 参数显式指定工具 ID，编程式触发函数调用。

### MCP 服务

MCP（模型上下文协议）提供了标准化的函数调用协议。在智能体应用中，大模型根据对话上下文自动判断是否调用 MCP 服务中的工具；在工作流应用中，每个 MCP 节点手动指定一个工具并串联输入输出。

### 实时多模态交互

Qwen3.5-Omni-Realtime 系列模型在 WebSocket 实时交互中支持函数调用。通过 `session.update` 事件配置 `tools`，模型在语音对话过程中触发工具调用，客户端通过 `conversation.item.create` 回传函数执行结果，再发送 `response.create` 继续对话。

### 意图路由

`tongyi-intent-detect-v3` 意图理解模型可在百毫秒级内解析用户意图并选择目标函数，常用于路由层，替代"先让通用大模型识别意图"的高成本方案。

## 关键参数

| 参数 | 说明 |
|------|------|
| `tools` | 函数定义列表，包含函数名称、描述和参数 JSON Schema |
| `tool_choice` | 控制模型的函数调用行为：`auto`（模型自行决定）、`none`（禁止调用）、或指定具体函数 |
| `tool_calls` | 模型响应中返回的函数调用指令，包含函数名和序列化后的参数 |
| `biz_params` | 插件调用时传递业务透传参数或用户级鉴权信息 |

## 支持的模型

函数调用能力主要由以下模型支持：

- **通用文本模型**：qwen-max、qwen-plus、qwen-turbo 等千问系列均支持
- **视觉模型**：qwen-vl-max、qwen-vl-plus 支持在多模态场景下进行函数调用
- **实时模型**：qwen3.5-omni-plus-realtime、qwen3.5-omni-flash-realtime
- **意图模型**：tongyi-intent-detect-v3 专用于函数路由
- **界面交互模型**：GUI-Plus 通过工具调用模式执行 GUI 操作

## 开发建议

- 函数描述要清晰准确，模型依据描述判断何时调用，描述质量直接影响调用准确率。
- 若智能体调用效果不佳，可尝试更强的推理模型（如千问 3 系列）。
- MCP 服务调用会增加 Token 消耗——MCP 返回内容作为上下文传入模型，增加输入和输出 Token。
- 输入参数设置为"大模型识别"时由模型从用户输入中提取，设置为"业务透传"时需外部主动传入。
- 工具创建后需在线调试通过并发布，只有"已发布"状态的工具才能被调用。

## 关联主题页

- [plug in](../guides/plug-in.md)
- [model context protocol](../guides/model-context-protocol.md)
- [specialized model](../api/specialized-model.md)
- [more models](../api/more-models.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [qwen api reference](../api/qwen-api-reference.md)


