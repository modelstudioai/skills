# 函数调用

函数调用（Function Calling）是大语言模型与外部工具交互的核心机制，允许模型在对话过程中识别用户意图并自动选择、调用预先定义的函数，从而扩展模型能力至实时数据查询、业务系统操作等场景。

## 工作原理

函数调用的基本流程为：开发者在请求中定义可用工具（函数）的名称、描述和参数 schema，模型根据用户输入判断是否需要调用工具，若需要则返回函数名和参数，由客户端执行后将结果回传模型继续生成最终回答。

## 在百炼平台中的使用场景

### 文本对话接口

通过 OpenAI 兼容 Chat Completions 接口，在请求中定义 `tools` 列表即可启用函数调用。模型会根据对话上下文自动判断是否需要调用工具，并输出结构化的调用参数。百炼的 Qwen3 系列通用模型（qwen3.7-max、qwen3.7-plus、qwen3.6-flash 等）均支持此能力。

### Responses API

Responses API 作为 Chat Completions 的演进版本，除了支持自定义函数调用外，还内置了联网搜索、代码解释器、网页抓取等工具，开箱即用无需额外定义。

### 实时多模态交互

Qwen-Omni-Realtime API 在 WebSocket 实时对话中同样支持函数调用。通过 `session.update` 事件配置工具列表，模型在语音对话过程中触发工具调用时会发送 `response.function_call_arguments.done` 事件，客户端执行完毕后通过 `conversation.item.create` 事件回传结果。Qwen3.5-Omni-Realtime 系列支持此能力。

### 意图理解模型

`tongyi-intent-detect-v3` 模型可同时输出用户意图分类和函数调用信息，适用于需要同时做意图路由和工具调度的场景。

## 关键参数和配置

| 参数 | 说明 |
| --- | --- |
| `tools` | 工具定义数组，每个元素包含 `type`（固定为 `function`）和 `function` 对象 |
| `tools[].function.name` | 函数名称，模型调用时会引用此标识 |
| `tools[].function.description` | 函数描述，帮助模型判断何时应调用该工具 |
| `tools[].function.parameters` | 函数参数的 JSON Schema 定义，模型据此生成结构化参数 |
| `tool_choice` | 工具选择策略：`auto`（模型自行判断）、`none`（禁止调用）、或指定具体函数名 |

## 支持的模型

百炼平台上支持函数调用的主要模型包括：

- **Qwen3 系列**：qwen3.7-max、qwen3.7-plus、qwen3.6-flash 等通用模型
- **DeepSeek 系列**：deepseek-v4-pro、deepseek-v4-flash
- **视觉模型**：qwen3.7-plus（视觉）、qwen3.6-flash（视觉）、qwen3.5-omni-plus
- **实时模型**：qwen3.5-omni-plus-realtime、qwen3.5-omni-flash-realtime
- **专用模型**：tongyi-intent-detect-v3（意图+函数调用）

## 最佳实践

- 函数描述应清晰准确，避免歧义，帮助模型正确判断调用时机
- 参数 schema 应使用 `required` 字段标注必填参数，并为可选参数提供合理默认值
- 对于复杂业务流程，可定义多个函数让模型按需组合调用
- 生产环境中建议对模型返回的函数参数做校验，防止非法输入
- 如需使用内置工具（联网搜索、代码解释器等），优先考虑 Responses API 以简化开发

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [model experience](../guides/model-experience.md)
- [more models](../api/more-models.md)


