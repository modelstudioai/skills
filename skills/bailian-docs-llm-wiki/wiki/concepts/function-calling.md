# 函数调用

函数调用（Function Calling）是百炼平台支持的一种结构化工具调度机制，允许大模型在推理过程中自主识别用户意图、生成符合规范的函数调用请求（含函数名与参数），并由平台安全执行外部工具或服务，最终将结果注入上下文继续生成。该能力无需开发者编写硬编码逻辑即可实现动态数据查询、业务系统集成与多步骤任务编排。

## 在百炼平台的不同场景中，这个概念如何使用

- **基础模型 API 调用**：在 `/v1/chat/completions` 请求中，通过 `tools` 字段声明可用函数（OpenAI 兼容格式），并设置 `tool_choice` 控制调用策略（如 `"auto"` 或指定函数名）。模型返回 `tool_calls` 数组，平台自动解析、校验并执行对应函数（如数据库查询、HTTP 请求），再将结果以 `tool_message` 形式回传给模型完成闭环。
  
- **Managed Agents（托管智能体）**：函数调用是 Agent 的核心执行单元。Agent 定义中声明的 `tools` 会自动注册为可调用函数；当 Agent 运行时，模型基于 `input_schema` 和会话上下文决定是否及如何调用这些函数，并支持异步等待、错误重试与状态透出（通过 `tool_called` Webhook 事件）。

- **数据连接（Data Connection）**：函数调用可直接绑定已配置的数据连接。例如，在 `tools` 中定义一个 `query_database` 函数，其内部实现调用 `DataConnectionClient.invoke()` 并传入 `connection_id` 和参数化 SQL，实现 RAG 检索或实时数据增强。

- **插件（Plug-in）系统**：插件本质是预注册的标准化函数。启用 `enable_plugins: true` 后，模型可将插件视为内置函数进行调用；插件元数据（OpenAPI 描述）即为函数签名，平台负责协议转换、鉴权与超时控制。

- **[Token](token.md) Plan 计费**：函数调用产生的 token 消耗（包括输入 [prompt](../guides/prompt.md)、tool call 请求、tool response 内容）全部纳入 [Token](token.md) Plan 抵扣范围，与普通文本生成同等计费，无需额外开通或配置。

- **模型兼容性**：当前仅 `qwen-max`、`qwen-plus`、`qwen-turbo` 及 `qwen2.5-*` 系列模型原生支持函数调用；`qwen-vl` 等多模态模型暂不支持（需使用 `qwen2.5-vl` 替代）。

## 关键参数和配置

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `tools` | array of objects | 必填。函数定义列表，每个对象包含 `type: "function"`、`function: { name, description, parameters }`（JSON Schema 格式） |
| `tool_choice` | string or object | 控制调用策略：<br>• `"none"`：禁用调用<br>• `"auto"`（默认）：由模型自主决策<br>• `{"type": "function", "function": {"name": "xxx"}}`：强制指定函数 |
| `tool_choice_mode` | string | （可选）高级策略，如 `"parallel"`（并发调用多个函数）、`"sequential"`（串行链式调用），需模型版本支持 |
| `tool_timeout_ms` | integer | 单次函数执行超时，默认 10000（10 秒），最大 30000；超时后返回 error message 并终止调用链 |
| `enable_plugins` | boolean | 若同时使用插件，必须设为 `true` 才激活函数调度器；否则 `tools` 字段被忽略 |

> ⚠️ 注意：`tools` 中的 `parameters` 必须为严格 JSON Schema（支持 `string`/`number`/`boolean`/`object`/`array`/`null`），不支持 OpenAPI 的 `x-aliyun-*` 扩展字段；平台将校验参数类型与必填项，非法调用直接拒绝。

## 面向开发者，简洁实用

- **快速验证**：用 `curl` 发起一次带 `tools` 的请求，观察响应中是否出现 `finish_reason: "tool_calls"` 和 `message.tool_calls` 字段；若无，检查模型是否支持、`tool_choice` 是否正确、`parameters` 是否符合 Schema。
- **调试技巧**：开启 `debug: true` 可在响应中获取 `tool_call_request` 原始内容与 `tool_call_result` 执行日志，便于定位参数拼接或权限问题。
- **错误处理**：捕获 `tool_calls` 中的 `error` 字段（如 `tool_not_authorized`、`function_not_found`），并在业务层降级为文本回答或提示用户重试。
- **性能优化**：单次最多并发 3 个函数调用；如需更高吞吐，请拆分为多个独立请求或使用 Managed Agents 的异步任务委派能力。
- **安全边界**：所有函数执行均在百炼服务端沙箱内完成，原始凭证（如数据库密码）不透出至模型上下文；但 `tools` 定义中避免硬编码敏感值（如 `api_key: "xxx"`），应通过数据连接或插件授权机制管理。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [managed agents](../guides/managed-agents.md)
- [data connection overview](../guides/data-connection-overview.md)
- [plug in](../guides/plug-in.md)
- [more about models](../api/more-about-models.md)
- [get started with models](../guides/get-started-with-models.md)


