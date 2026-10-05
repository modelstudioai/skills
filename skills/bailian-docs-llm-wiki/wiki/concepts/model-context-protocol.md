# 模型上下文协议（MCP）

模型上下文协议（Model Context Protocol, MCP）是百炼平台提供的标准化、安全、可扩展的工具集成机制，用于在大模型与外部能力（如地图、搜索、数据库、API 服务等）之间建立统一通信通道。它基于开源 MCP 标准（[modelcontextprotocol.io](https://modelcontextprotocol.io/)），并由百炼深度增强为 **Streamable HTTP 协议**，支持稳定流式调用、凭据安全注入与跨平台兼容。

## 在百炼平台的不同场景中，这个概念如何使用

MCP 不是独立运行的服务，而是作为“能力接入层”，必须嵌入百炼的托管运行环境中使用。其核心使用场景如下：

- **智能体（Agent）应用**：在创建或编辑智能体时，于「MCP 服务」模块添加已开通的 MCP 服务（如 `amap_weather`）。模型（如 `qwen-max`）将根据对话上下文自主决策是否调用、何时调用、调用哪个工具，并自动解析输入/输出结构。最多可同时启用 **5 个 MCP 服务**。
  
- **工作流（Workflow）应用**：拖入「MCP 节点」→ 选择具体工具（如 `web_search`）→ 显式配置输入参数（支持从上游节点引用变量，如 `{{llm_output.city}}`）→ 将输出结果传递给下游节点（如文本生成或条件判断）。每个 MCP 节点绑定**唯一工具实例**，不支持动态路由。

- **Managed Agents（托管智能体）**：在 Agent 配置中通过 `mcp_servers` 字段声明 MCP 服务列表。MCP 工具与内置工具（`bash`、`web_fetch` 等）同处于沙箱环境中，可被多步编排调用，并共享会话状态、文件系统和记忆库。

- **Qwen-Omni-Realtime API**：在实时语音会话中，通过 `session.update` 的 `tools` 数组声明 `type: "mcp"` 工具（如 `"tool": "amap_maps"`）。模型可在语音交互过程中触发 MCP 调用，结果以结构化事件（`tool_call.created` / `tool_call.output`）实时返回，支持与音频流同步响应。

> ⚠️ 注意：MCP **不可直接用于裸调用 DashScope 或 Qwen 原生 API**（如 `POST /api/v1/services/qwen-max`）。它必须依托百炼的智能体、工作流、Managed Agents 或 Omni-Realtime 等容器化运行时环境。

## 关键参数和配置

### 服务级参数（部署时设定）
| 参数 | 说明 | 必填 | 示例值 |
|------|------|------|--------|
| `type` | 协议类型，决定端点路径 | 是 | `"streamableHttp"`（对应 `/mcp`；**百炼仅支持此类型**） |
| `url` | MCP Server 公网可访问地址 | 是 | `https://my-mcp-service.example.com/mcp`（需有效 TLS 证书） |
| `command` / `args` | 仅脚本部署（如 `npx`）时使用 | 否 | `["npx", "@mcp/server-node", "--port=3000"]` |
| `env_vars` | 环境变量（用于注入密钥等） | 否 | `{"AMAP_MAPS_API_KEY": "${KMS_CREDENTIAL:amap_key}"}` |

### 调用级参数（运行时传递）
- **工具发现**：通过 `list_tools()` 自动获取工具名（`tool.name`）及输入 Schema（`tool.inputSchema`），无需硬编码。
- **认证头**：所有调用均需携带 `Authorization: Bearer <DASHSCOPE_API_KEY>`。
- **敏感参数**：API Key、Token 等必须通过 KMS 凭据加密后注入（格式 `${KMS_CREDENTIAL:xxx}`），**禁止明文配置**。
- **输入参数**：由上游模型或工作流节点生成，严格遵循 `inputSchema` 定义的 JSON Schema（类型、必填项、枚举值等）。

## 面向开发者，简洁实用

- ✅ **快速开通**：前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，一键开通官方服务（如高德地图、联网搜索）；试用版免配 Key。
- ✅ **自定义发布**：用 Python/Node.js 编写 MCP Server → 托管至函数计算（FC）→ 控制台「自定义 MCP 服务」导入 URL 即可。
- ✅ **调试三步法**：
  1. `curl -v <your_mcp_url>/mcp` 测试连通性与 TLS；
  2. 查看智能体/工作流日志中的 `mcp_call` 事件，确认请求 payload 是否符合 `inputSchema`；
  3. 若模型未触发调用，检查 System Prompt 是否明确声明工具能力（例如：“你可调用 `weather` 工具查询实时天气”）。
- ⚠️ **避坑提醒**：
  - 升级提示：旧版 SSE 服务需**取消再重新开通**，才能切换至 Streamable HTTP；
  - 网络限制：FC 托管的自定义服务无固定出口 IP，访问 RDS/VPC 内资源需配置白名单或 VPC 打通；
  - 计费注意：全局限流 15 QPS（主账号+子账号共享），超量将拒绝请求（HTTP 429）。

> 提示：MCP 是百炼实现“模型即服务编排中枢”的关键协议。相比插件（Plugin）机制，MCP 更强调**标准化协议层**与**跨平台互操作性**（支持 Cherry Studio、Cursor 等外部 IDE），而插件则更侧重百炼原生体验与快速上手。两者可共存，但自定义能力推荐优先走 MCP 路径。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [managed agents](../guides/managed-agents.md)
- [plug in](../guides/plug-in.md)
- [omni realtime api](../api/omni-realtime-api.md)


