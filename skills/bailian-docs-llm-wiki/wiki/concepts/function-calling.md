# 函数调用

函数调用（Function Calling）是百炼平台中模型主动发起外部工具执行的核心机制，指大模型在推理过程中，根据用户意图和上下文，自主生成结构化工具调用请求（`tool_calls`），交由运行时环境解析、调度并执行对应函数（如搜索、代码解释、文件操作、插件服务等），再将结果注入后续推理循环。该能力使模型从纯文本生成跃迁为可操作、可扩展的智能体。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台并非单一接口能力，而是贯穿多个技术栈的统一语义层，具体体现为：

- **Managed Agents（托管智能体）**：模型在沙箱内自主触发内置工具（如 `bash`、`web_search`、`read`）或扩展能力（MCP 服务、Skills）。调用由平台自动解析 `tool_calls`、执行沙箱命令/HTTP 请求，并将结果以 `tool_results` 形式回传续写。开发者无需手动处理调用链，只需在 `tools.configs[]` 中声明启用并配置权限策略（如 `always_allow`）。

- **Qwen API（模型直调）**：通过 OpenAI 兼容 Responses API 或 Anthropic Messages API 的 `tools` 字段注册函数 Schema，模型返回 `tool_calls` 后，**调用方必须自行解析、执行并构造 `tool_results` 提交续写请求**。DashScope 原生 API 同理，但需严格遵循其 `function_calling` 参数格式。此模式适用于需完全掌控执行逻辑的高代码场景。

- **Omni Realtime API（实时多模态）**：支持 `type=function` 的工具声明，与 `enable_search` 互斥。模型在语音/文本混合会话中实时生成函数调用，服务端通过 WebSocket 事件流推送 `tool_calls`，客户端需同步执行并回传 `tool_results` 以维持低延迟交互。

- **Plug-in（插件）**：插件本质是函数调用的一种标准化实现。当模型选择 `type=plugin` 工具时，即触发插件函数调用；`plugin_id` 和 `arguments` 构成函数签名，调用方需按 `plugin.json` Schema 校验参数并发起 HTTPS 请求。

- **Application Call（应用调用）**：新版智能体应用（Agent 2.0）在 `application call` 接口中原生支持函数调用语义——若应用内部启用了工具（如内置工具、MCP 或插件），则调用方收到的响应中可能包含 `tool_calls`，需按相同协议处理 `tool_results` 续写；旧版智能体与工作流则不直接暴露函数调用接口，工具能力被封装在节点逻辑中。

## 关键参数和配置

函数调用的生效依赖以下关键参数，需在请求 payload 或 Agent 配置中显式设置：

- `tools`: 必填数组，声明可用函数列表。每个元素为对象，含：
  - `type`: `"function"`（自定义函数）、`"plugin"`（插件）、`"mcp"`（MCP 服务）或内置工具类型（如 `"web_search"`）；
  - `function`: 当 `type="function"` 时必填，含 `name`（函数名）、`description`（功能描述）、`parameters`（JSON Schema 定义参数结构）；
  - `plugin_id`: 当 `type="plugin"` 时必填；
  - `mcp_server_url`: 当 `type="mcp"` 时必填。

- `tool_choice`: 可选，控制模型调用行为：
  - `"auto"`（默认）：模型自主决定是否及何时调用；
  - `"none"`：禁止调用；
  - `{"type": "function", "function": {"name": "xxx"}}`：强制调用指定函数（仅部分 API 支持）。

- `tool_results`: 非请求参数，而是**调用方必须构造的续写输入字段**，用于提交函数执行结果。格式为数组，每个元素含 `tool_call_id`（匹配原始 `tool_calls[i].id`）和 `content`（字符串或 JSON 对象形式的结果）。

> ⚠️ 注意：`tools` 必须在请求中显式声明，仅在 Agent 配置中启用工具（如 `default_config.enabled: true`）**不会生效**；函数调用能力受模型限制（如 `qwen3.5-flash` 支持基础调用，`qwen3.8-max` 支持多步深度调用），请查阅各模型文档确认支持范围。

## 面向开发者，简洁实用

- **不要等待“自动执行”**：百炼平台中，除 Managed Agents 外，所有 API 的函数调用均需**你来执行**——模型只负责“说要调什么”，你必须解析 `tool_calls`、调用真实服务、校验结果、再发 `tool_results` 续写。
- **Schema 是契约**：`parameters` 的 JSON Schema 必须与后端函数实际入参严格一致，否则 `arguments` 解析失败将导致调用中断。
- **ID 必须匹配**：`tool_results[i].tool_call_id` 必须精确等于 `tool_calls[i].id`（大小写、符号全匹配），否则服务端无法关联结果。
- **错误处理有规范**：若函数执行失败，`tool_results[i].content` 应返回清晰错误信息（如 `{"error": "API rate limit exceeded"}`），避免空字符串或非 JSON 内容。
- **并发安全**：单次响应最多含 10 个 `tool_calls`，建议并发执行时控制超时（推荐 `timeout_ms: 10000`）并做好重试降级。

## 关联主题页

- [agent development](../guides/agent-development.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [plug in](../guides/plug-in.md)
- [application call](../api/application-call.md)


