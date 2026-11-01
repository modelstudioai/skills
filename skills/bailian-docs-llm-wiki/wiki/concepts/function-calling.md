# 函数调用

函数调用（Function Calling）是百炼平台中让大模型具备**主动识别用户意图、结构化生成工具请求、并交由系统执行外部操作**的核心能力。它不是简单的 API 封装，而是模型原生支持的推理阶段行为——模型在生成响应前，会自主决定是否调用函数、调用哪个函数、以及传入哪些参数，整个过程可被显式控制、可观测、可审计。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中并非孤立功能，而是贯穿多个开发范式与接口协议的统一抽象，具体体现为：

- **Managed Agent 与 Flow Agent 中**：作为「工具（Tool）」能力的基础。开发者在控制台或 API 中注册工具（如查天气、查订单、写数据库），模型在推理时自动触发 `tool_calls`，平台负责解析、执行、注入结果回上下文。此时函数调用由平台自动编排，开发者只需定义工具 schema 和实现逻辑。
  
- **Sandbox 模式中**：函数调用逻辑完全由开发者自主控制。你可在 `main.py` 中通过 `@tool` 装饰器声明函数，再调用 `llm.invoke(..., tools=[...])` 显式启用；也可跳过平台封装，直接构造符合 OpenAI 兼容格式的 `tools` 和 `tool_choice` 参数，调用底层模型接口。

- **Managed Agents API（`/agents/{id}/invoke`）中**：通过 `tool_choice` 字段精确控制行为：
  - `"auto"`（默认）：模型自主决定是否及如何调用；
  - `"none"`：禁用所有函数调用；
  - `{"type": "function", "name": "xxx"}`：强制调用指定函数（适用于确定性流程）。

- **[OpenAI 兼容接口](openai-compatible-interface.md)（如 Responses API、Chat Completions）中**：使用标准 `tools` + `tool_choice` 字段（JSON Schema 格式），百炼模型（如 `qwen3.8-max`、`qwen3.7-plus`）原生支持该协议。注意：仅 Responses API 和 Chat Completions 协议支持完整函数调用链路；Embedding/Vision 等协议不支持。

> ✅ 关键共识：无论在哪种场景，函数调用的输入（`tools`）必须是符合 [OpenAI Function Calling Schema](https://platform.openai.com/docs/guides/function-calling) 的 JSON Schema 描述；输出（`tool_calls`）始终是结构化数组，含 `id`、`function.name`、`function.arguments` 字段，便于程序解析与执行。

## 关键参数和配置

| 参数 | 位置 | 类型 | 说明 |
|------|------|------|------|
| `tools` | 请求体（`messages` 同级） | `array[object]` | 必填（启用调用时）。每个对象包含 `type: "function"`、`function.name`、`function.description`、`function.parameters`（JSON Schema）。参数名需为合法标识符（字母/数字/下划线），不可含空格或特殊字符。 |
| `tool_choice` | 请求体（`messages` 同级） | `string` 或 `object` | 控制策略：`"auto"`（默认）、`"none"`、或 `{"type": "function", "name": "xxx"}`。Flow Agent/Sandbox 中亦可通过节点/代码逻辑覆盖此值。 |
| `enable_context` | 请求体（部分模型需显式开启） | `boolean` | 部分模型（如早期 Qwen-Turbo）需设为 `true` 才能激活函数调用能力；Qwen-Max/Plus 默认启用。 |
| `response_format` | 请求体（高级控制） | `object` | 可选。设为 `{"type": "json_object"}` 强制模型输出 JSON，常用于避免函数调用后返回自然语言解释；但会抑制 `tool_calls` 字段（因非标准行为），慎用。 |

> ⚠️ 注意事项：
> - 单次请求最多触发 **5 次函数调用**（含嵌套），超限返回 `400 Bad Request`；
> - 函数参数 `arguments` 是字符串（JSON 序列化后），**务必用 `json.loads()` 解析，不可直接 `eval`**；
> - 若函数执行失败，需在 `tool_outputs` 中返回明确错误信息，模型可能重试或切换策略；
> - Sandbox 模式中，函数内部禁止访问沙箱受限网络（如内网地址），否则调用将中断。

## 面向开发者，简洁实用

- **快速验证**：用 `curl` 调用 Responses API，`tools` 至少包含一个带 `description` 和简单 `parameters` 的函数，观察响应中是否出现 `tool_calls` 数组；
- **调试技巧**：启用 `enable_tracing`（Flow/Sandbox）或检查响应头 `X-Bailian-Trace-ID`，在控制台追踪完整的调用-执行-注入链路；
- **错误处理**：永远假设 `tool_calls` 可能为空（模型未触发）、`arguments` 可能为无效 JSON、函数执行可能超时——你的胶水代码必须健壮；
- **性能提示**：函数调用本身不计费，但每次调用后的模型二次推理（处理 `tool_outputs`）会计费；减少不必要的调用轮次；
- **安全底线**：函数实现中涉及密钥、数据库连接等敏感操作，**必须通过 `Vault`/`Credential` 管理凭据，严禁硬编码或从 `os.environ` 直接读取明文密钥**。

函数调用是构建可靠 Agent 的基石。掌握它，你就掌握了让模型“动手做事”的开关。

## 关联主题页

- [agent context](../guides/agent-context.md)
- [agent development](../guides/agent-development.md)
- [managed agents api](../api/managed-agents-api.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


