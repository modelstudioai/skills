# 函数调用

函数调用（Function Calling）是百炼平台中大模型主动识别用户意图、生成结构化工具调用请求，并交由外部系统执行的关键能力。它使模型能脱离纯文本生成，安全、可控地接入真实业务系统（如数据库、API、计算器、搜索服务等），是构建生产级 AI Agent 的核心机制。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中并非单一接口能力，而是贯穿多个模型与协议的**统一语义能力**，具体体现为以下四类典型场景：

- **OpenAI 兼容 `chat/completions` 接口**：通过 `tools` 数组声明可用函数（含 `name`、`description`、`parameters` JSON Schema），模型在 `tool_calls` 字段中返回结构化调用请求；开发者需解析并执行后，将结果以 `tool_message` 形式回传继续对话。
- **Omni Realtime 实时语音 API**：在 `session.update` 配置中传入 `tools`（支持标准 Function Calling 和 MCP 协议），模型可在语音交互流中动态触发工具，但需注意：`tools` 与 `enable_search` 互斥，不可同时启用。
- **意图识别专用模型（如 `tongyi-intent-detect-v3`）**：在 `INTENT_MODE` 下，模型直接输出 `<intent>` 标签包裹的函数名与参数 JSON，无需 `tool_calls` 封装，适合轻量级路由与快速决策场景。
- **应用编排中的插件调用（Application Support）**：在低代码应用中配置插件节点后，模型自动理解插件能力并生成调用逻辑；自定义插件需符合 OpenAPI 3.0 规范，平台仅透传 `Authorization` Header，其余请求头不支持自定义。

> ⚠️ 注意：函数调用能力**依赖模型本身支持**。例如 `qwen3-audio`（仅 DashScope 协议）和 `qwen-deep-research` 不支持函数调用；而 `qwen3.8-omni-flash-realtime`、`qwen3.7-plus`、`tongyi-intent-detect-v3` 等明确支持，调用前请确认模型文档说明。

## 关键参数和配置

| 参数 | 类型 | 说明 | 所属场景 |
|------|------|------|----------|
| `tools` | `array` | 必填。函数定义列表，每个元素包含 `type`（`function` 或 `mcp`）、`function.name`、`description`、`parameters`（JSON Schema） | [OpenAI 兼容接口](openai-compatible-api.md)、Omni Realtime |
| `tool_choice` | `string` / `object` | 控制调用策略：`"auto"`（默认，由模型决定）、`"none"`（禁用）、`{"type": "function", "function": {"name": "xxx"}}`（强制指定） | [OpenAI 兼容接口](openai-compatible-api.md) |
| `reasoning.effort` | `string` | 在 `OpenAI兼容-Responses` 接口中，设为 `"high"` 可提升工具调用准确性（尤其复杂参数组合） | Responses 接口 |
| `INTENT_MODE` | — | 在 `tongyi-intent-detect-v3` 的 `system` message 中声明，触发意图+参数直出模式，响应格式为 `<intent>{"name":"xxx","args":{...}}</intent>` | 意图识别模型 |
| `extra_body.tools` | `array` | 使用 OpenAI SDK 调用非标模型（如 `farui-plus`）时，需将 `tools` 放入 `extra_body` 透传 | 更多模型（More Models） |

- 所有函数调用均要求 `parameters` 使用严格 JSON Schema 定义（支持 `string`、`number`、`boolean`、`object`、`array` 及嵌套），模型据此生成合法参数；建议避免过度复杂 schema，优先使用 `required` 字段明确必填项。
- 工具执行结果必须以正确格式（如 OpenAI 的 `tool_message` 或意图模型的 `<intent>` 块）回传，否则会导致上下文断裂或循环调用。

## 面向开发者，简洁实用

- ✅ **推荐实践**：优先使用 `qwen3.7-plus` 或 `qwen3.8-max` 等通用强模型进行函数调用；对高确定性任务（如客服意图识别），选用 `tongyi-intent-detect-v3` + `INTENT_MODE` 可降低解析开销、提升首响速度。
- ✅ **调试技巧**：开启 `stream=False` 获取完整响应，检查 `tool_calls` 或 `<intent>` 内容是否符合预期；若调用失败，先验证 `parameters` Schema 是否与实际传参一致（如 `number` vs `"number"` 字符串）。
- ❌ **避坑提示**：不要在同一个请求中混用 `tools` 和 `enable_search`（Omni Realtime）；不要为不支持函数调用的模型（如 `qwen3-audio`）配置 `tools`，将被静默忽略；自定义插件注册后，须在控制台完成鉴权测试再上线。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [more models](../api/more-models.md)
- [application support](../guides/application-support.md)


