# 函数调用

函数调用（Function Calling）是百炼平台中模型主动识别用户意图、生成结构化工具请求并交由外部系统执行的关键能力。它使大模型不仅能生成文本，还能安全、可控地与现实世界交互，完成计算、查询、操作等具体任务。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中并非单一接口功能，而是贯穿多个能力层的横切机制，按使用方式可分为三类：

- **模型原生函数调用**：适用于 `qwen3.8-max`、`qwen3.7-plus` 等支持 OpenAI 兼容协议的通用模型。开发者通过 `tools` 参数声明可用函数（JSON Schema 描述），模型在推理过程中自动判断是否需要调用、选择哪个函数、并生成符合 Schema 的 `function_call` 请求体。典型用于 `web_search`、`code_interpreter`、自定义 MCP 工具等场景。

- **Agent 中的工具调用**：在 Managed Agent 和 Flow Agent 中，“函数调用”被抽象为更高阶的“工具调用（Tool Invocation）”。开发者无需手动构造 `tools` 数组，而是通过控制台配置或 API 的 `tools` 字段（Managed）或 `nodes` 节点（Flow）声明可用能力包（如 `mcp://calculator`、`connector://crm`）。Agent 运行时自动编排 LLM 与工具的协同，包括多轮调用、错误重试、结果注入上下文等。

- **专用模型的轻量函数生成**：`tongyi-intent-detect-v3` 等意图理解模型专为低延迟、高精度函数触发设计。它不返回自然语言，而是直接输出标准化的意图标签（如 `"intent:book_flight"`）或结构化函数参数（如 `{"flight_date": "2025-04-10", "from": "PEK"}`），适用于对话路由、前端指令解析等对响应速度和确定性要求极高的场景。

> ⚠️ 注意：`qwen-deep-research`、GUI-Plus 等专用模型虽支持工具（如 `computer_use`），但其调用逻辑由模型内部两阶段流程（反问 → 执行）驱动，不暴露标准 `function_call` 字段，不属于本文定义的“函数调用”范畴。

## 关键参数和配置

| 参数/配置项 | 说明 | 使用位置 | 示例值 |
|-------------|------|----------|--------|
| `tools` | JSON Schema 数组，定义可调用函数的名称、描述、参数类型与约束 | OpenAI 兼容 API（Chat/Responses）、Managed Agent API | `[{"type":"function","function":{"name":"get_weather","description":"获取指定城市天气","parameters":{"type":"object","properties":{"city":{"type":"string"}}}}}]` |
| `tool_choice` | 控制模型行为：`"auto"`（默认，由模型决定）、`"none"`（禁用）、或指定 `{"type":"function","function":{"name":"xxx"}}` | OpenAI 兼容 API | `"auto"` 或 `{"type":"function","function":{"name":"get_weather"}}` |
| `enable_thinking` | GUI-Plus 等混合模型特有，启用后返回 `reasoning_content` 辅助调试调用逻辑 | GUI-Plus 模型调用 | `true` |
| `extra_body` | Python SDK 中传递非标准参数（如 `top_k`, `vl_high_resolution_images`）的字典入口 | Python SDK 调用所有模型 | `{"enable_thinking": true}` |
| `tools`（Agent） | Managed Agent API 中声明工具 URI 列表，格式为 `["mcp://xxx", "connector://yyy"]` | Managed Agent `/agents/{id}/invoke` | `["mcp://calculator", "connector://salesforce"]` |

- **Schema 编写建议**：参数名避免下划线（部分模型兼容性差），必填字段明确标注 `"required": ["param1", "param2"]`，字符串参数建议加 `"maxLength"` 限制以提升鲁棒性。
- **调试技巧**：开启 `stream=true` 可观察模型思考过程；若函数未被触发，检查 `system message` 是否包含足够强的指令（如 `"You MUST call a function if the user asks for calculation."`）。

## 面向开发者，简洁实用

- ✅ **首选 OpenAI 兼容协议**：90% 的函数调用场景推荐使用 `/compatible-mode/v1/chat/completions` 接口，文档成熟、SDK 支持好、调试直观。
- ✅ **生产环境务必校验 `function_call`**：模型可能返回空 `function_call` 或无效参数，调用前需做 `if response.choices[0].message.tool_calls:` 判断，并用 `jsonschema.validate()` 校验参数。
- ✅ **Agent 开发更关注“能力编排”而非“函数细节”**：在 Flow Agent 中，把函数封装为节点后，重点应放在输入映射、条件分支与错误处理上，而非反复调试 Schema。
- ❌ **避免在 `qwen-deep-research` 等专用模型上强行套用 `tools`**：该模型不遵循标准函数调用协议，强行传入 `tools` 将被忽略或报错。
- 🚀 **性能提示**：函数调用会增加单次请求延迟（通常 +300~800ms），高频调用场景建议启用 `previous_response_id`（Responses API）或 Agent 的 `enable_memory` 复用上下文，减少重复推理。

## 关联主题页

- [get started with agents](../guides/get-started-with-agents.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [more about models](../api/more-about-models.md)
- [more models](../api/more-models.md)


