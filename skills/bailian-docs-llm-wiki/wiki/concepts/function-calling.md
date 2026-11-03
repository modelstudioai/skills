# 函数调用

函数调用（Function Calling）是百炼平台中模型主动识别用户意图并结构化生成工具执行指令的能力，表现为模型在响应中输出标准 JSON 格式的 `tool_calls` 数组，包含目标工具名（`function.name`）和参数（`function.arguments`），而非自由文本。该机制是构建可靠智能体（Agent）、实现可控工具编排与业务系统集成的核心基础。

## 在百炼平台的不同场景中，这个概念如何使用

- **意图理解专用模型（`tongyi-intent-detect-v3`）**：在 `INTENT_MODE` 下，模型直接输出符合预定义工具 Schema 的函数调用，例如 `{"name": "alarm_set", "arguments": {"time": "07:30", "label": "晨会提醒"}}`，无需额外解析即可对接下游服务。  
- **插件（Plug-in）调用**：当请求中传入 `tools` 数组（含 `type: "plugin"` 的插件定义）时，支持插件的模型（如 `qwen-max`、`qwen-plus`）可自主决定是否调用、调用哪个插件，并以 `tool_calls` 形式返回结构化指令；开发者需按 `id` 和 `arguments` 发起插件 HTTP 请求，再将结果作为 `tool_message` 提交回模型。  
- **Agent 开发（Managed / Flow / Sandbox）**：Managed Agent 和 Flow Agent 内置工具调用流程，自动处理 `tool_calls` → 执行 → `tool_message` → 最终回复的闭环；Sandbox 则由开发者完全控制——需手动解析响应中的 `tool_calls` 字段，调用对应工具，并构造合规的 `tool_message` 重新提交。  
- **[OpenAI 兼容接口](openai-compatible-api.md)（Responses API / Chat Completions）**：所有支持函数调用的模型（包括 `qwen3.8-max`、`qwen3-vl-plus` 等）均可通过 OpenAI SDK 的 `tools` + `tool_choice` 参数启用该能力；`Responses API` 尤其推荐用于智能体场景，因其内置上下文管理与工具调用状态追踪。

## 关键参数和配置

- `tools`（必需）：`array` 类型，每个元素为工具定义对象，必须包含 `type`（`"function"` 或 `"plugin"`）、`function.name`（字符串）及 `function.parameters`（JSON Schema 对象，描述参数名、类型、是否必填等）。  
- `tool_choice`（可选）：控制模型行为，取值包括：  
  - `"auto"`（默认）：模型自主判断是否调用及调用哪个工具；  
  - `"required"`：强制模型必须调用至少一个工具；  
  - `{"type": "function", "name": "xxx"}` 或 `{"type": "plugin", "id": "xxx"}`：指定唯一工具，模型必须调用该工具（若无法满足则报错）。  
- `response_format`（可选）：设为 `{"type": "json_object"}` 可增强结构化输出稳定性，但不替代 `tools` 机制；函数调用本身始终以 `tool_calls` 字段返回，与 `content` 并存。  
- 注意：`tools` 总大小不可超过 2MB；工具名（`function.name`）须与注册/声明时完全一致（区分大小写）；`function.arguments` 必须是合法 JSON 字符串（非对象），由模型生成后需由开发者 `json.loads()` 解析。

## 面向开发者，简洁实用

- ✅ **务必校验响应结构**：检查 `response.choices[0].message.tool_calls` 是否存在且非空，而非依赖 `content` 字段。  
- ✅ **严格按 Schema 解析参数**：`function.arguments` 是字符串，需 `json.loads()`；若解析失败，说明模型输出格式异常，应记录日志并降级处理（如重试或返回错误）。  
- ✅ **工具执行后必须构造 `tool_message`**：格式为 `{"role": "tool", "content": "<stringified result>", "tool_call_id": "<id from tool_calls>"}`；`content` 应为字符串（即使结果是 JSON，也需 `json.dumps()`），不可为原始对象。  
- ⚠️ **不支持函数调用的模型不会返回 `tool_calls`**：如 `qwen-deep-research`、`qwen-mt-plus` 等专用模型无此能力，强行传 `tools` 将被忽略。调用前请确认模型文档明确标注“支持 Function Calling”或“支持工具调用”。  
- ⚠️ **避免嵌套调用陷阱**：单次响应最多返回 10 个 `tool_calls`；若需多步工具协同，请在 `tool_message` 中明确提示模型继续推理，而非在代码中循环调用。

## 关联主题页

- [more models](../api/more-models.md)
- [plug in](../guides/plug-in.md)
- [agent development](../guides/agent-development.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


