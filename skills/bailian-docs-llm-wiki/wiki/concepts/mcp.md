# 模型上下文协议

模型上下文协议（Model Context Protocol，简称 MCP）是百炼平台定义的标准化工具通信协议，用于在大模型推理过程中安全、可靠、可发现地调用外部服务与能力。它抽象了工具接入的底层传输细节（如 HTTP、SSE、STDIO），统一建模工具元信息、输入输出 Schema、调用生命周期与错误语义，使大模型能基于自然语言意图自动选择、参数化并执行工具。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Managed Agent）集成**：MCP 服务作为 `tools` 显式挂载到 Agent 配置中，Agent 运行时根据用户输入动态触发 MCP [工具调用](tool-calling.md)，并将结果注入上下文供后续 LLM 推理使用。  
- **工作流（Flow Agent）编排**：在 Flow 节点中以「MCP 工具节点」形式存在，需手动指定 `server_code.tool_name` 及参数映射规则；工具执行结果可被下游 LLM 或条件节点直接引用。  
- **Agent Store 统一管理**：所有官方 MCP（如天气、地图、联网搜索）和自定义 MCP 均注册于 Agent Store，通过 `/mcp/servers/list` 发现，通过 `/tools/call` 执行，实现“一处注册、多处复用”。  
- **外部 IDE/编辑器集成（Qoder、Cursor 等）**：开发者通过 MCP SDK（如 `streamablehttp_client`）连接百炼提供的 `mcp_url`，复用同一套协议与认证机制，实现本地开发环境与平台能力的无缝对接。  
- **自定义工具开发**：开发者只需按 `mcp_type`（`HTTP`/`SSE`/`STDIO`/`OPENAPI`）实现对应协议端点，并提交符合规范的 `mcp_config`，即可被平台识别为标准 MCP 服务，无需改造业务逻辑。

## 关键参数和配置

- **`mcp_type`**（必填）：声明服务通信类型，取值为 `HTTP`、`SSE`、`STDIO` 或 `OPENAPI`；决定 `mcp_config` 的结构约束与运行时调度方式。  
- **`mcp_config`**（必填，结构依赖 `mcp_type`）：
  - `HTTP`：需含 `url`（字符串）、可选 `headers`（对象，支持密钥透传）；
  - `SSE`：需含 `url`，且客户端必须监听 `/sse` 路径；
  - `STDIO`：需含 `command`（字符串，如 `python mcp_server.py`），由函数计算托管执行；
  - `OPENAPI`：需提供 `api_list` 数组，每个 API 含 `path`、`method`、`input_params`（OpenAPI 3.0 兼容 schema）。  
- **`type`（客户端配置）**：在 CLI 或 SDK 中声明客户端期望的通信模式，必须与服务端暴露的路径严格匹配（如 `type: "sse"` 对应服务端 `/sse` 端点），不一致将导致 `11200058` 错误。  
- **`mcp_url`**（运行时地址）：格式为 `https://dashscope.aliyuncs.com/api/v1/mcps/{ServiceCode}/mcp`（Streamable HTTP）或 `/sse`（SSE），由平台自动生成，不可自定义。  
- **认证凭证**：全程使用 `DASHSCOPE_API_KEY`（Bearer [Token](token.md)），无额外 OAuth 或 API Key 透传；敏感字段（如 `mcp_config.headers.Authorization`）由调用方自行维护，平台不解析、不审计。

## 面向开发者，简洁实用

- ✅ **快速验证**：用 `bl mcp tools --server weather` 查看工具列表，再用 `bl mcp call --target weather.get_current_weather --city 北京` 直接调试。  
- ✅ **零侵入接入**：已有 RESTful 服务？用 `OPENAPI` 类型导入 OpenAPI 3.0 YAML 即可生成 MCP；本地脚本？选 `STDIO` 类型，一行命令部署。  
- ✅ **安全第一**：`mcp_config` 中的 `headers`、`auth` 等字段**禁止记录日志、禁止前端展示**；所有传输必须 HTTPS，敏感配置建议通过 Vault 注入。  
- ⚠️ **注意一致性**：`mcp_type`（服务端声明）与客户端 `type`（SDK/CLI 配置）必须匹配；`OPENAPI` 类型的 `inputSchema` 字段名保持 camelCase，不转 snake_case。  
- 🚫 **不支持裸调用**：MCP 协议仅在百炼平台内生效（智能体、工作流、Agent Store），不可用于直接调用 `dashscope` SDK 的独立 Python 脚本。

## 关联主题页

- [overview 1e06e5e20b81f10d](../api/overview-1e06e5e20b81f10d.md)
- [overview](../api/overview.md)
- [agent store](../guides/agent-store.md)
- [managed agents api](../api/managed-agents-api.md)
- [flow agent api](../api/flow-agent-api.md)


