# 函数调用

函数调用（Function Calling）是百炼平台支持的一种关键能力，允许大模型在推理过程中自主识别用户意图、生成结构化工具调用请求，并将外部系统（如计算器、搜索、代码执行器等）的返回结果整合进最终响应。该能力是构建智能体（Agent）、自动化工作流和复杂业务应用的基础机制。

## 在百炼平台的不同场景中，这个概念如何使用

- **标准模型 API 调用**：通过 `/v1/chat/completions` 接口，在 `messages` 中声明 `tools` 数组（含 `function.name`、`description` 和 `parameters` JSON Schema），并设置 `tool_choice` 控制调用策略（如 `"auto"` 或指定 `{"type": "function", "function": {"name": "calculator"}}`）。支持模型包括 `qwen-max`、`qwen-plus`、`qwen3.8-max`、`qwen3.7-plus` 等主流商业版模型。

- **插件（Plugin）集成场景**：函数调用是插件能力的底层协议载体。官方插件（如 `calculator`、`quark_search`）、三方插件及自定义插件，均需以 `tool_id` 作为 `function.name` 注册到 `tools` 列表中；大模型据此生成符合契约的参数对象，平台自动路由并执行。

- **Assistant API 与开发工具**：在 Assistant API 模式下，`tools` 是必配字段；主流客户端（如 Cursor、Dify、Cherry Studio）和 CLI 工具（如 Kilo CLI）均原生支持 OpenAI 兼容的 `tools` 格式，可直接复用百炼的函数调用能力，无需额外适配。

- **多模态与高级协议**：OpenAI 兼容的 Chat API 和 Responses API 均支持函数调用；Anthropic 兼容 Messages API 当前**不支持**函数调用；DashScope 原生 API 需通过 `tools` + `tool_choice` 字段显式启用（非默认行为），且仅限支持该能力的模型版本。

> ⚠️ 注意：并非所有模型都支持函数调用。请以控制台模型详情页或 [模型兼容性列表](https://bailian.console.aliyun.com/model/market) 为准；`qwen-turbo`、`qwen2.5-vl` 等轻量或视觉专用模型默认不支持。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `tools` | array | 是（启用函数调用时） | 工具定义列表，每个元素为 `{ "type": "function", "function": { "name": "tool_id", "description": "...", "parameters": { ... } } }`；`parameters` 必须为合法 JSON Schema（支持 `string`/`number`/`object`/`array`/`boolean`/`null`），`required` 字段建议明确列出。 |
| `tool_choice` | string or object | 否 | 控制调用策略：<br>• `"none"`：禁用函数调用；<br>• `"auto"`（默认）：由模型自主决定是否调用及调用哪个；<br>• `{"type": "function", "function": {"name": "xxx"}}`：强制调用指定工具。 |
| `response_format` | object | 否（推荐配合使用） | 若需模型返回严格 JSON 结构（如工具参数），可设为 `{"type": "json_object"}`，提升参数提取准确率（需模型支持 JSON 模式）。 |

- **工具参数约束**：  
  - `name`（即 `tool_id`）必须与插件市场或自定义插件发布的 ID 完全一致（区分大小写）；  
  - `parameters` 中若含 `object` 类型，其所有子属性**不可为空**，否则发布/调用失败（错误码 130022）；  
  - 建议为复杂参数提供 `examples` 字段（非标准 OpenAI 字段，但百炼解析器支持），显著提升泛化准确率。

- **调试建议**：  
  - 开启 `stream: false` 获取完整响应，检查 `choices[0].message.tool_calls` 字段是否存在；  
  - 若未触发调用，优先检查 `tools` 是否有效注册、`messages` 中用户输入是否含明确工具需求（如“计算 123*456”、“搜索最新 AI 新闻”）；  
  - 使用控制台「API 调试」功能实时查看模型生成的 `tool_calls` 内容与参数填充质量。

面向开发者，请始终以最小可行工具集开始验证（例如仅配置 `calculator`），再逐步扩展至多工具协同场景。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [plug in](../guides/plug-in.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)


