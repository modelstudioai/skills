# 函数调用

函数调用（Function Calling）是百炼平台中模型主动识别用户意图、并按预定义 Schema 触发外部工具或服务的能力。它使大模型不仅能生成文本，还能在推理过程中动态决定是否需要查询数据库、调用 API、执行计算或与业务系统交互，从而构建可扩展、可落地的智能体（Agent）应用。

## 在百炼平台的不同场景中如何使用

函数调用能力在百炼平台中主要应用于两类实时交互型 API：

- **Omni Realtime API**：面向语音助手、会议实时摘要等低延迟多模态场景。通过 `session.update` 事件中的 `tools` 数组声明支持的函数列表，模型在流式响应过程中可输出 `type=function` 的 `tool_use` 事件，携带函数名与参数。开发者需监听该事件并同步执行对应逻辑，再将结果通过 `tool_result` 事件回传给模型继续推理。

- **Realtime API（音频/视觉专用）**：适用于 `qwen-audio-20241015`、`qwen-vl-20241015` 等模型。同样通过 `tools` 字段注册函数，但要求所有函数 schema 严格遵循 OpenAI 兼容格式（含 `name`、`description`、`parameters`），且不支持嵌套对象以外的复杂类型（如 `anyOf`、`oneOf`）。模型触发后，服务端以 `tool_use` 事件推送调用请求，客户端须在 5 秒内返回 `tool_result`，否则会话中断。

> ⚠️ 注意：函数调用**不支持**在标准 Model Experience（`/v1/models/{model}/invoke`）REST API 中使用；也不与联网搜索（`enable_search: true`）共存——二者互斥，启用任一功能时另一项将被忽略。

## 关键参数和配置

| 参数 | 位置 | 类型 | 说明 |
|------|------|------|------|
| `tools` | `session.update` 消息体 | `array` | 必填。函数定义列表，每个元素为 `{ "type": "function", "function": { "name": "...", "description": "...", "parameters": { ... } } }`。`parameters` 需为 JSON Schema object，推荐使用 `required` 字段明确必填字段。 |
| `tool_choice` | `session.update`（可选） | `string` 或 `object` | 控制调用策略：`"auto"`（默认，由模型自主判断）、`"none"`（禁用）、或 `{ "type": "function", "function": { "name": "xxx" } }`（强制指定函数）。 |
| `max_tool_calls` | `session.update`（可选） | `integer` | 单次响应中允许触发的最大函数调用次数，默认为 `1`，最大支持 `5`。 |

- 所有函数名（`name`）必须为合法 Python 标识符（仅含字母、数字、下划线，不以数字开头），长度 ≤ 64 字符；
- `parameters` 中避免使用 `null` 默认值；建议为字符串字段设置 `minLength: 1`，数值字段设置 `minimum`/`maximum` 以提升模型理解准确性；
- 工具执行结果需通过 `tool_result` 事件回传，其 `tool_call_id` 必须与原始 `tool_use` 中的 ID 完全一致，且 `content` 字段应为字符串（JSON 序列化后的结果亦可，但需确保模型能解析）。

## 面向开发者：简洁实用提示

- ✅ **快速验证**：在控制台「模型体验」中选择 `qwen3.8-omni-flash-realtime`，开启 WebSocket 调试，粘贴含 `tools` 的 `session.update` 示例，观察 `tool_use` 事件是否如期触发；
- ✅ **错误排查**：若未触发调用，检查 `tools` 是否在首次 `session.update` 中完整发送、`name` 是否拼写正确、`parameters` 是否为有效 JSON Schema；
- ❌ **禁止行为**：不要在 `input.text` 或 `input.audio` 中“提示模型调用函数”（如“请调用天气API”）——函数调用由模型自主决策，显式指令反而干扰判断；
- 📦 **生产建议**：将工具执行逻辑封装为幂等接口，并在 `tool_result` 中返回结构化 JSON（如 `{ "status": "success", "data": {...} }`），便于模型后续提取关键信息生成自然语言回复。

## 关联主题页

- [model experience](../guides/model-experience.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)


