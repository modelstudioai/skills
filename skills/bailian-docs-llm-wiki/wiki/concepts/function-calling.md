# 函数调用

函数调用（Function Calling）是百炼平台支持的一种结构化工具协同机制，允许大模型在推理过程中主动识别用户意图、生成符合预定义 Schema 的函数调用请求（而非仅输出自然语言），从而安全、可控地触发外部能力（如查询数据库、调用 API、执行计算等）。该能力由模型原生支持，无需额外解析或正则匹配。

## 在百炼平台的不同场景中，这个概念如何使用

- **基础模型 API 调用**：当使用支持函数调用的模型（如 `qwen-max`、`qwen-plus` 等标注了 function calling 能力的版本）时，开发者需在请求中通过 `input.functions` 字段声明可用函数列表（含名称、描述、JSON Schema 参数定义），并在 `input.messages` 中传入用户消息。模型将返回 `function_call` 字段（含 `name` 和 `arguments` 字符串），而非普通文本响应；你需自行解析 `arguments` 并执行对应函数，再将结果以 `tool_message` 形式回传给模型继续推理。

- **Flow Agent 流程编排**：在 Flow Agent 的 YAML 定义中，可通过 `type: function` 节点直接集成函数调用逻辑。平台自动处理 Schema 注册、调用触发、参数校验与错误重试。你只需提供函数实现（Python 函数或 HTTP 接口配置），无需手动解析/序列化 `function_call`。该节点天然支持上下文传递和异步等待，适用于需多步工具协同的复杂工作流。

- **Sandbox 沙箱环境**：在 Sandbox 中，你可完全自主实现函数调用闭环：使用 `bailian.llm.invoke()` 调用支持 function calling 的模型 → 检查响应中的 `function_call` → 执行本地 Python 函数或发起外部请求 → 构造 `tool_message` → 再次调用模型完成终局回答。此方式提供最高控制粒度，适合需自定义鉴权、熔断、日志审计或私有协议集成的场景。

> ⚠️ 注意：Managed Agent 当前不支持函数调用能力，其内置工具（如知识库检索）由平台封装调用，不可扩展自定义函数。

## 关键参数和配置

- `input.functions`（模型 API）：必填数组，每个元素为对象，包含：
  - `name`（string，必需）：函数唯一标识符，模型生成时将精确匹配此名称；
  - `description`（string，必需）：函数功能描述，供模型理解调用意图；
  - `parameters`（object，必需）：符合 JSON Schema Draft 07 的参数定义，用于约束 `arguments` 结构（如 `type`, `properties`, `required`, `enum` 等）。

- `input.function_call`（模型 API）：可选字符串或对象，用于控制调用行为：
  - `"auto"`（默认）：模型自主决定是否调用及调用哪个函数；
  - `"none"`：禁止函数调用，强制模型返回自然语言；
  - `{"name": "xxx"}`：强制模型仅调用指定函数（适用于确定性任务）。

- `functions`（Flow Agent YAML）：在 `type: function` 节点中声明，格式同上，但支持引用已注册的全局函数库或内联定义。

- `timeout`（所有场景）：函数执行超时时间（秒），建议设为 30–120，避免阻塞整个推理链路。

- `enable_tracing`（Flow Agent / Sandbox）：启用后可在响应中查看完整的函数调用轨迹（包括输入参数、执行耗时、原始 `arguments` 和返回值），便于调试与可观测性。

面向开发者提示：  
✅ 始终对 `arguments` 字符串做 JSON 解析容错（可能含非法转义或格式错误）；  
✅ 函数实现必须幂等，因平台可能重试失败调用；  
✅ 避免在 `description` 或 `parameters.description` 中泄露敏感逻辑或内部实现细节；  
✅ 生产环境务必设置 `timeout` 和 `max_retries`，防止下游服务异常导致 Agent 卡死。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [agent development](../guides/agent-development.md)
- [flow agent api](../api/flow-agent-api.md)


