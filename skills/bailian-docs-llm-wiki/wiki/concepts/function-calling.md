# 函数调用

函数调用（Function Calling）是百炼平台支持的一种结构化工具编排能力，允许大模型在推理过程中主动识别用户意图、生成符合预定义 Schema 的函数调用请求，并将结果交由外部系统执行。该机制是构建可靠 Agent 的核心基础设施，实现了 LLM 与真实世界 API、数据库、业务逻辑的安全解耦。

## 在百炼平台的不同场景中，这个概念如何使用

- **Agent 开发**：在 Managed Agent 和 Flow Agent 中，函数调用通过「工具注册」实现——开发者上传 OpenAPI Spec 或 JSON Schema 定义的工具，平台自动注入模型上下文；模型根据 `system` 提示和用户输入，输出 `tool_calls` 结构，平台负责路由、执行、注入结果并继续推理。Sandbox Agent 则由开发者在 Python 代码中手动解析 `tool_calls` 并调用对应函数。
  
- **API 直接调用**：通过 OpenAI 兼容 `/v1/chat/completions` 接口启用函数调用，需在请求中传入 `tools`（数组，每个元素含 `function.name`、`function.description` 和严格符合 JSON Schema 规范的 `function.parameters`）及 `tool_choice`（可选 `"auto"`、`"none"` 或指定 `{"type": "function", "function": {"name": "xxx"}}`）。模型返回 `finish_reason: "tool_calls"` 且响应体含 `message.tool_calls` 字段。

- **专用模型增强**：`tongyi-intent-detect-v3`（意图理解模型）专为函数调用优化，支持毫秒级意图识别与高精度参数提取，在对话路由、客服工单分派等低延迟场景中替代通用模型，显著提升调用准确率与响应速度。

- **CLI 限制说明**：当前 `bailian-cli`（v2.3+）**不支持函数调用功能**，所有 `--input` 请求均以纯文本生成模式处理。如需使用函数调用，请改用 SDK（Python/Java）或直接调用 REST API。

- **框架集成**：LangChain 的 `BailianLLM` 封装类原生支持 `tools` 参数，调用 `invoke()` 时自动处理 `tool_calls` 解析与回调；OpenAI SDK 用户只需配置百炼兼容 endpoint，即可复用 `openai.ChatCompletion.create(..., tools=...)` 语法（注意：不支持 `stream=True` 与 `tools` 同时启用）。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `tools` | array | 是（启用函数调用时） | 工具定义列表，每个工具必须包含：<br>• `function.name`（字符串，仅字母数字下划线，长度 ≤ 64）<br>• `function.description`（字符串，用于模型理解用途）<br>• `function.parameters`（JSON Schema object，**不支持 `null`、`anyOf`、`oneOf`、`not` 等复杂关键字**；必需字段需显式声明 `"required": ["field1", "field2"]`） |
| `tool_choice` | string / object | 否 | 控制调用策略：<br>• `"auto"`（默认）：模型自主决定是否调用及调用哪个工具<br>• `"none"`：禁止任何函数调用，强制文本输出<br>• `{"type": "function", "function": {"name": "xxx"}}`：强制调用指定函数（适用于确定性流程） |
| `response_format` | object | 否（但推荐显式设置） | 若需模型返回结构化 JSON，设为 `{"type": "json_object"}`；注意：仅部分模型（如 `qwen-plus`）稳定支持，且与 `tools` 同时使用时，模型优先满足工具调用格式而非 JSON 输出格式 |

> ⚠️ 重要限制：  
> - **流式响应（`stream=true`）与函数调用互斥**：同时设置将返回 HTTP 400 错误。  
> - **工具参数 Schema 必须为 object 类型**：`"parameters": null` 或 `"parameters": {}` 均非法；空参数应写为 `"parameters": {"type": "object", "properties": {}, "required": []}`。  
> - **地域与模型约束**：`tongyi-intent-detect-v3` 仅支持华北2（北京）地域；Qwen 系列通用模型需 `qwen-plus` 及以上版本才能稳定支持多工具选择。

## 面向开发者，简洁实用

- ✅ **快速验证**：用 `curl` 调用 `/v1/chat/completions`，先测试单工具（如天气查询），确认 `tool_calls` 返回结构正确后再扩展。
- ✅ **调试技巧**：开启 `enable_tracing=true`（Agent 场景）或在请求头加 `X-DashScope-Trace: enable`（API 场景），可在控制台可观测性中查看完整工具调用链路与参数填充过程。
- ✅ **错误处理**：当模型返回无效 `tool_calls`（如参数类型错误、缺失必填字段），平台不会自动重试；建议在客户端捕获 `finish_reason: "tool_calls"` 后，先校验参数再执行，失败时回传 `tool_result` 并附带错误信息供模型修正。
- ❌ **避免踩坑**：不要在 `system` 消息中要求“只返回 JSON”，这会干扰函数调用协议；应依赖 `tools` 定义本身驱动行为。

## 关联主题页

- [getting started](../guides/getting-started.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [more models](../api/more-models.md)
- [agent development](../guides/agent-development.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


