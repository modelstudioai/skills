# 函数调用

函数调用（Function Calling）是百炼平台支持的一种结构化工具协同能力，允许大语言模型在推理过程中主动识别用户意图、生成符合规范的工具调用请求（含函数名与参数），并将结果交由外部系统执行，从而扩展模型的能力边界。该机制不依赖客户端硬编码逻辑判断，而是由模型原生理解并生成标准化的调用指令。

## 在百炼平台的不同场景中如何使用

函数调用能力在百炼平台中并非全局默认启用，其可用性取决于所选服务类型与接口协议：

- **模型 API 层（DashScope 原生接口）**：  
  通过 `input.tools` 字段声明可用函数列表（JSON Schema 格式），并在 `parameters.tool_choice` 中指定调用策略（`auto` / `none` / 具体函数名）。模型返回结构化 `tool_calls` 字段，包含 `name` 和 `arguments`，开发者需自行解析、执行并注入结果后继续对话。

- **Qwen 系列模型（Anthropic 兼容 Messages 接口）**：  
  使用 `tools` 数组 + `tool_choice` 参数，响应中以 `content` 内嵌 `{"type": "tool_use", "name": "...", "input": {...}}` 形式输出调用请求，语义清晰、易于解析，推荐用于需要强结构化工具交互的场景。

- **Agent 服务层（Managed Agent / Flow Agent）**：  
  工具以 MCP 协议注册后，自动纳入 Agent 的可调用能力集；通过 `tool_choice: auto` 启用自动决策，或显式指定 `tool_choice: "weather_query"` 触发特定工具。Agent 运行时自动完成调用、结果注入与多轮编排，无需开发者手动处理中间状态。

- **[OpenAI 兼容接口](openai-compatible-interface.md)（Chat Completions）**：  
  **不原生支持函数调用**。若需类似能力，必须由客户端自行封装：例如将工具描述拼入 system prompt，再解析模型返回的 JSON-like 文本并做正则/Schema 校验——该方式稳定性低、易出错，不推荐生产使用。

> ✅ 最佳实践：优先选用 DashScope 原生接口或 Anthropic 兼容 Messages 接口进行函数调用开发；Agent 场景下直接配置 `tools` 并启用 `enable_tool_calling`（部分 SDK 封装为布尔开关）即可开箱即用。

## 关键参数和配置

| 参数 | 类型 | 说明 | 是否必需 | 备注 |
|------|------|------|----------|------|
| `tools` | array | 工具定义列表，每个元素为 `{ "name": string, "description": string, "parameters": JSON Schema }` | 是（启用函数调用时） | Schema 必须为合法 JSON Schema v7 子集，支持 `string`/`number`/`boolean`/`object`/`array` 及 `required` 字段 |
| `tool_choice` | string \| object | 调用策略：`"auto"`（模型自主决策）、`"none"`（禁用）、`{"type": "function", "function": {"name": "xxx"}}`（强制指定） | 否（默认 `"auto"`） | 部分 Agent 模式下也支持 `"required"`（必须调用至少一个工具） |
| `enable_search` | boolean | （仅 DashScope 接口）是否启用内置搜索增强（非函数调用，但常与工具协同） | 否 | 与 `tools` 独立，可同时开启 |

> ⚠️ 注意事项：
> - 所有工具名（`name`）必须为 ASCII 字符，长度 ≤ 64，且不能与保留关键字（如 `system`、`user`）冲突；
> - `parameters` 中的 `default` 值不会被模型自动填充，未提供的必填字段将导致调用失败；
> - 若模型返回无效 JSON 或参数类型不符，API 将返回 `400 Bad Request` 并附带校验错误详情，建议在客户端做 `try/catch` + 重试降级（如 fallback 到文本回答）。

## 面向开发者：快速上手提示

- **调试技巧**：首次集成时，在 `messages` 中加入明确指令（如“请调用天气查询工具获取北京当前温度”），并设置 `tool_choice: "auto"`，观察返回中是否出现 `tool_calls` 字段；
- **安全边界**：函数调用本身不执行代码，仅生成请求；实际执行必须由你控制的服务端完成，务必对 `arguments` 做白名单校验与输入消毒；
- **性能优化**：避免在 `tools` 中声明大量低频工具（>10 个），会显著增加模型推理开销；高频工具建议前置，低频工具按需动态注入；
- **错误恢复**：当工具执行失败时，将错误信息以 `role: tool` 消息形式回传（格式：`{"name": "...", "content": "error: ..."}"`），模型可据此重试或改写响应。

函数调用是构建可靠 AI 应用的关键桥梁——它让模型从“回答者”变为“协作者”。合理设计工具 Schema、精准控制 `tool_choice`、并做好执行层兜底，即可实现安全、可控、可扩展的智能体交互。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [get started with agents](../guides/get-started-with-agents.md)
- [agent development](../guides/agent-development.md)


