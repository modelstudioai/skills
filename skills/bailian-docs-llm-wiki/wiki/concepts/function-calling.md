# 函数调用

函数调用（Function Calling）是百炼平台中大模型主动识别用户意图、生成结构化工具调用指令的核心能力。它允许模型在推理过程中，根据对话上下文和预定义的工具 Schema，自主决定是否调用外部函数，并准确填充参数，从而实现规划-执行闭环。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中并非统一接口能力，而是按服务形态分层实现：

- **Agent 服务（`/v1/agents`）**：为最标准的函数调用场景。模型（仅 `qwen-plus` / `qwen-max`）基于 `tools` 数组中的 OpenAPI Schema 自动选择工具、生成参数并返回 `tool_calls`。开发者需同步执行工具后，将结果作为 `tool_message` 提交下一轮，形成多步交互循环。

- **意图理解模型（`tongyi-intent-detect-v3`）**：在 `INTENT_MODE` 下支持“意图 + 函数调用”联合输出。此时模型不仅返回意图标签（如 `alarm_set`），还会生成符合该意图语义的标准化函数调用结构（含 `name` 和 `arguments`），适用于轻量级、确定性高的垂直任务编排。

- **GUI 界面交互模型（`gui-plus`）**：支持多模态输入下的工具调用，可结合截图/控件坐标等视觉信息，生成如 `click_element`, `input_text` 等桌面自动化函数调用，用于真实环境的 GUI 操作代理。

- **Sandbox/Flow Agent**：不直接暴露函数调用原语，但可通过内置工具节点（如 WebSearch、数据库查询）或自定义 Python 脚本间接实现等效逻辑；函数调用决策由开发者代码控制，而非模型自动触发。

> ⚠️ 注意：`qwen-deep-research` 和 OCR 类模型（如 `qwen3.5-ocr`）**不支持函数调用**——前者专注研究流程编排，后者专注图像文本提取，二者均无工具调度能力。

## 关键参数和配置

| 参数 | 说明 | 使用位置 | 备注 |
|------|------|----------|------|
| `tools` | 工具定义数组，每个元素为 OpenAPI 3.0 兼容的 JSON Schema，必须包含 `function.name`、`function.description` 和 `function.parameters`（合法 JSON Schema 对象） | Agent 接口（`/v1/agents`）、应用配置中的插件接入 | `parameters` 不可为字符串，否则触发 `400 InvalidToolSchema` |
| `tool_choice` | 控制模型调用行为 | Agent 接口 | 可选 `"auto"`（默认）、`"none"` 或 `{ "type": "function", "function": { "name": "xxx" } }`；设为具体函数名时强制调用，绕过模型自主选择 |
| `enable_thinking` | 启用后，`gui-plus-2026-02-26` 将在 `reasoning_content` 字段中返回调用前的推理链，便于调试调用逻辑 | `gui-plus` 模型调用（通过 `extra_body` 传入） | 非必需，但强烈建议开发阶段开启 |
| `messages` 中的 `tool_message` | 工具执行结果必须以 `role: "tool"` 的消息格式提交，且 `content` 必须为 JSON 字符串（非对象），含 `tool_call_id` 与 `content` 字段 | Agent 多轮调用中第二轮及以后 | 格式错误将导致 `TOOL_EXECUTION_FAILED` 错误 |

## 面向开发者，简洁实用

- ✅ **必做**：所有 `tools` 的 `parameters` 必须是有效 JSON Schema（推荐用 [JSON Schema Validator](https://jsonschemalint.com/) 验证），避免因字段类型/必填项定义不清导致调用失败。  
- ✅ **调试技巧**：首次集成时，固定 `tool_choice` 为某具体函数名，验证参数生成准确性；再切换回 `"auto"` 观察模型决策合理性。  
- ✅ **错误处理**：当收到 `finish_reason: "tool_calls"` 时，务必检查 `message.tool_calls` 是否为空数组（可能模型未识别到可用工具），再解析调用项。  
- ❌ **禁止**：在 `tools` 中混用不同协议的工具（如同时传入 REST API 和本地 Python 函数 Schema）；Agent 服务仅支持标准 HTTP 工具调用。  
- 📌 **性能提示**：函数调用会显著增加端到端延迟，单次 Agent 请求最大支持 8 层嵌套调用，建议将复杂逻辑封装为单个幂等工具，而非拆分为多步细粒度调用。

## 关联主题页

- [more models](../api/more-models.md)
- [get started with agents](../guides/get-started-with-agents.md)
- [agent development](../guides/agent-development.md)
- [application support](../guides/application-support.md)


