# 函数调用

函数调用（Function Calling）是百炼平台中大模型主动识别用户意图、生成结构化工具调用指令，并交由平台执行外部操作的核心能力。它不是简单的 API 转发，而是模型在推理过程中基于上下文动态选择工具、填充参数、处理返回结果并决定是否继续调用的闭环机制。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台并非单一接口功能，而是贯穿多个能力层的统一语义抽象，具体体现为以下四类场景：

- **Managed Agents（托管智能体）**：Agent 在 `Session` 中自动触发工具调用。当模型输出符合 `Skill` 定义的 JSON Schema 时，平台自动解析、校验参数、调用对应技能（如数据库查询、HTTP 请求），并将结果注入后续上下文。调用过程受 `max_iterations` 限制，且失败可通过 `Webhook` 实时通知。

- **Sandbox（沙箱环境）**：用于调试函数调用逻辑本身。通过 `POST /v1/sandbox/instances/{id}/chat/completions` 发起请求时，若传入 `tools`（OpenAI 兼容格式）或 `plugins` 参数，模型将尝试生成符合 schema 的调用指令；沙箱支持流式返回原始 `tool_calls` 字段，便于验证参数生成准确性与格式合规性。

- **Plug-in（插件）与 Application Support（应用支持）**：以插件形式封装函数调用能力。启用 `enable_plugins=true` 后，模型可调用控制台已开通的官方或自定义插件（如“天气查询”“二维码生成”）。所有插件调用均遵循统一协议——输入经 `args` 透传，仅支持 `Authorization` header，响应需为合法 JSON，否则视为执行失败。

- **Model Context Protocol（MCP）**：提供标准化、可扩展的函数调用基础设施。MCP 将各类外部服务（地图、搜索、私有知识库等）抽象为 `tool`，通过 `tool.name` 和 `inputSchema` 声明式注册。在智能体或工作流中启用 MCP 后，模型可跨服务组合调用（如“查天气 + 绘图”），平台负责协议适配、认证透传（`headers`/`env`）与错误降级。

> ⚠️ 注意：纯千问 API（如 `/v1/chat/completions`）**不支持原生函数调用**；必须通过 Managed Agents、Sandbox、Plug-in 或 MCP 等平台级封装才能启用该能力。

## 关键参数和配置

函数调用行为由以下关键参数协同控制，开发者需按场景显式配置：

| 参数名 | 所属场景 | 类型 | 必填 | 说明 |
|--------|----------|------|------|------|
| `tools` | Sandbox、MCP（部分模式） | array | 否 | OpenAI 兼容格式：`[{ "type": "function", "function": { "name": "...", "parameters": {...} } }]`。模型据此生成 `tool_calls`。 |
| `plugins` | Plug-in、Application Support | array | 否 | 百炼专有格式：`[{ "name": "plugin_id", "args": {...} }]`。需配合 `enable_plugins=true` 使用。 |
| `skills` | Managed Agents | array | 是（若需工具能力） | Agent 创建时绑定：每个元素含 `id`（指向 Skill 资源）及可选 `config`，定义工具元信息与运行时配置。 |
| `enable_plugins` | Plug-in | boolean | 是（启用插件时） | 显式开关，即使 `plugins` 非空，此字段为 `false` 时仍禁用调用。 |
| `tool.name` / `inputSchema` | MCP | string / object | 是（注册 MCP 服务时） | 工具唯一标识与参数约束 Schema，直接影响模型能否正确生成调用指令。 |
| `plugin_timeout_ms` / `timeout` | Plug-in / Sandbox | integer | 否 | 插件或沙箱实例超时时间（毫秒/秒），超时后自动降级，避免阻塞推理流。 |

> ✅ 最佳实践：始终为工具定义清晰的 `inputSchema`（JSON Schema draft-07 子集），避免使用 `anyOf`/`not`；敏感参数（如 `api_key`）应通过 `env` 或 KMS 凭据注入，**切勿写入 `args` 明文传递**。

## 面向开发者，简洁实用

- **调试优先**：用 Sandbox 快速验证模型能否生成合法 `tool_calls`，再迁移到 Managed Agents 生产环境。
- **统一 Schema**：无论使用 Plug-in、MCP 还是自定义 Skill，确保 `inputSchema` 严格匹配后端接口，这是调用成功率的关键。
- **错误必捕获**：监听 `tool.error`（Webhook）、`plugin_execution_failed`（错误码）或 MCP 协议错误（如 11200058），及时降级或重试。
- **安全红线**：所有凭证必须通过 `Vault`/`Credential` 或 `env` 注入；API 调用仅支持 `Authorization` header，其他头字段会被丢弃。
- **性能意识**：单次请求最多 3 个插件 / 20 个 Skill / 5 个 MCP 服务；嵌套调用不支持，需在工具内部实现复合逻辑。

## 关联主题页

- [managed agents api](../api/managed-agents-api.md)
- [sandbox](../guides/sandbox.md)
- [plug in](../guides/plug-in.md)
- [application support](../guides/application-support.md)
- [model context protocol](../guides/model-context-protocol.md)


