# 函数调用

函数调用（Function Calling）是百炼平台中模型主动识别用户意图、并按需触发外部能力（如数据查询、API 调用、业务逻辑执行等）的核心机制。它通过结构化工具定义与标准化调用协议，使大模型从“纯文本生成器”升级为可操作现实世界的智能代理。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中并非单一功能模块，而是贯穿多个关键能力的横切能力，具体体现为以下四类典型场景：

- **插件（Plug-in）调用**：面向开发者直接集成外部服务。通过在 `/v1/chat/completions` 请求中传入 `tools`（OpenAPI Schema 描述）和 `tool_choice`，由支持函数调用的模型（如 `qwen-max`、`qwen-plus`）自主决策是否及如何调用指定工具，并返回 `tool_calls` 结构化指令。适用于 HTTP API、自建服务等轻量级扩展。

- **MCP（Model Context Protocol）调用**：作为百炼官方推荐的标准化上下文交互协议，MCP 在插件能力基础上增强安全性与可控性。除 `tools` 和 `tool_choice` 外，支持可选的 `tool_config`（用于配置超时、重试、鉴权策略），并强制要求工具端点符合 HTTPS 与跨域规范，适用于生产环境中的高可靠工具编排。

- **数据连接（Data Connection）集成**：在 RAG 检索节点、Agent 工作流的 Data Source 节点或自定义函数节点中，函数调用被隐式封装为“安全数据访问动作”。开发者只需配置 `connection_id` 和参数化 `query`（如 `SELECT * FROM users WHERE id = {{input.user_id}}`），平台自动将该请求作为受控函数执行，禁止写操作，保障数据安全。

- **Skill 与应用内函数节点**：Skill 可绑定预定义函数逻辑（如格式转换、规则校验），并在低代码工作流中以“自定义函数节点”形式被调用；Agent 工作流亦支持拖拽函数节点，输入经 Schema 校验后透传至后端服务。此类调用由平台统一调度，不暴露原始 `tool_calls`，适合封装确定性业务逻辑。

> ⚠️ 注意：所有函数调用均**不经过百炼平台代理鉴权**（插件/MCP 场景下凭证需客户端自行注入），但数据连接类调用全程在服务端沙箱内执行，凭据由 KMS 加密托管。

## 关键参数和配置

函数调用的行为由以下核心参数控制，不同场景下存在共性与差异：

| 参数名 | 所属场景 | 是否必填 | 说明 |
|--------|----------|----------|------|
| `tools` | 插件、MCP | 是 | 工具定义数组，每个元素为 OpenAI-style function schema（含 `name`、`description`、`parameters` JSON Schema）。单次最多 20 个。 |
| `tool_choice` | 插件、MCP | 否（默认 `"auto"`） | 控制调用策略：`"auto"`（模型决策）、`"none"`（禁用）、或指定 `{"type": "function", "function": {"name": "xxx"}}` 强制调用。 |
| `connection_id` + `query` | 数据连接 | `connection_id` 必填 | 数据连接专属参数：`connection_id` 为平台分配的唯一标识；`query` 支持 SQL 或 OSS 路径，可嵌入 `{{input.xxx}}` 占位符。 |
| `tool_config` | MCP | 否 | 运行时策略配置对象，支持 `timeout_ms`（默认 15000）、`max_retries` 等字段（具体以 [MCP 外部调用文档](https://help.aliyun.com/zh/model-studio/mcp-external-calls) 为准）。 |
| `enable_thinking` | 插件（全局请求级） | 否（默认 `true`） | 若设为 `false`，模型跳过规划步骤，可能导致 `tool_calls` 为空——调试时建议保持启用。 |

## 面向开发者，简洁实用

- ✅ **快速起步**：优先使用 MCP 协议（`/v1/chat/completions` + `tools`），兼容性好、文档完善、生产就绪。
- ✅ **安全读取数据**：敏感数据源接入首选「数据连接」，避免硬编码凭据，利用 `{{input.xxx}}` 实现动态参数注入。
- ✅ **复用业务逻辑**：确定性处理（如日期解析、JSON 格式化）封装为 Skill 或工作流函数节点，降低模型幻觉风险。
- ⚠️ **避坑提示**：
  - 流式响应（`stream: true`）下无法解析 `tool_calls`，必须等待完整响应；
  - 工具 `parameters` 中必填字段务必在 JSON Schema 的 `"required"` 数组中显式声明；
  - 自定义工具返回错误时，仅通过 `tool_message.content` 传递，需在客户端主动解析并处理；
  - 所有函数调用链深度上限为 5 层（含嵌套调用），避免无限循环。

函数调用不是终点，而是模型与真实世界建立可信协作的起点——请始终以最小权限、明确契约、可观测日志为设计前提。

## 关联主题页

- [data connection overview](../guides/data-connection-overview.md)
- [skill](../guides/skill.md)
- [plug in](../guides/plug-in.md)
- [model context protocol](../guides/model-context-protocol.md)
- [bailian application calling](../guides/bailian-application-calling.md)
- [application permission management](../guides/application-permission-management.md)


