# 函数调用

函数调用（Function Calling）是百炼平台中让大模型具备**主动识别用户意图、结构化生成工具请求、并交由运行时安全执行外部能力**的核心机制。它不是简单的 API 转发，而是由模型推理层、协议适配层与执行沙箱协同完成的端到端能力链路。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼三大 Agent 模式中承担不同角色，但底层语义一致：**将自然语言请求转化为结构化工具调用指令，并确保其被正确解析、授权、执行与结果注入上下文**。

- **Managed Agent**：完全托管式调用。开发者在控制台配置 MCP 工具或 Skill 后，模型自动决定是否调用、调用哪个工具及传入参数；运行时自动完成参数校验、权限检查、沙箱执行与结果格式化回填。无需编写调用逻辑，但不可干预中间过程。
  
- **Flow Agent**：可视化编排式调用。工具节点作为流程图中的一个标准组件，可手动连接输入/输出、设置失败重试或分支跳转；`tool_choice` 参数支持强制指定工具，适用于确定性调度场景（如“先查天气，再规划行程”）。

- **Sandbox**：代码级自主调用。开发者需在 `main.py` 中显式调用 `bailian.tool.call(tool_name, **kwargs)` 或直接构造符合 MCP 协议的 JSON 请求；可捕获异常、自定义重试、组合多个工具调用，也支持动态加载私有工具函数（需注册为 `bailian.tool.register()`）。

> ⚠️ 注意：所有模式下，函数调用均受统一安全策略约束——未在 `tools` 白名单中声明的工具不会被模型选择；未通过 Vault 注入凭证的敏感操作（如数据库写入）将被拦截；超时（默认 30 秒）或资源超限会立即终止并返回 `500 ToolExecutionTimeout`。

## 关键参数和配置

| 参数 | 作用 | 必填 | 说明 |
|------|------|------|------|
| `tools` | 工具白名单 | 否（但启用调用必填） | 字符串数组，如 `["weather_query", "db_search"]`；仅在此列表中的工具才可能被模型选择或 Flow 节点调用；Sandbox 模式下该参数仅用于权限声明，实际调用由代码控制。 |
| `tool_choice` | 调用策略 | 否 | 可选 `"auto"`（默认，由模型决策）、`"none"`（禁用调用）、或指定工具 ID（如 `"weather_query"`），强制触发单次调用。Flow Agent 和 Managed Agent 支持，Sandbox 不生效。 |
| `max_iterations` | 最大调用轮数 | 否 | 默认 `10`（Flow/Sandbox）或 `15`（Managed）；防止模型陷入“调用→失败→重试→再调用”死循环；超过后终止流程并返回 `400 TooManyToolCalls`。 |
| `enable_stream` | 流式响应支持 | 否 | 仅 Sandbox 和 Flow Agent 支持设为 `true`；启用后，工具执行日志与中间结果可实时推送（需配合 `bailian.stream` SDK 接口）。 |

> ✅ 提示：工具定义必须符合 [MCP v1.0 协议规范](https://modelcontextprotocol.io)，包括 `name`、`description`、`parameters`（JSON Schema 格式）三要素；百炼控制台创建 Skill 或上传 MCP YAML 文件时会自动校验。

## 面向开发者，简洁实用

- **调试建议**：首次集成务必开启 `debug: true` 并检查响应中的 `tool_calls` 字段——若为空数组，说明模型未识别出调用意图，请优化提示词中对工具能力的描述（例如明确写出“当用户问‘今天北京天气’时，必须调用 `weather_query` 工具”）。
- **错误处理**：工具执行失败时，Managed Agent 直接报错；Flow Agent 可配置「失败后跳转」节点；Sandbox 中请 `try/except bailian.ToolExecutionError` 并记录 `error.tool_name` 和 `error.detail` 用于定位。
- **性能优化**：避免在单次请求中声明大量工具（>20 个），会显著增加模型推理开销；高频调用场景建议复用 `bailian.Client` 实例（Python SDK）或启用 HTTP 连接池（Java SDK）。
- **安全底线**：所有工具函数必须在 Sandbox 环境内执行（即使 Managed Agent 也经由同构沙箱），禁止在 `main.py` 中直接执行 `os.system()`、`subprocess.Popen()` 等原生系统调用——此类行为会被运行时拦截并记为安全事件。

## 关联主题页

- [get started with agents](../guides/get-started-with-agents.md)
- [managed agents api](../api/managed-agents-api.md)
- [agent development](../guides/agent-development.md)
- [more about models](../api/more-about-models.md)


