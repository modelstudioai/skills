# model context protocol

[模型上下文协议](../concepts/mcp.md)（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化机制，用于在大模型与外部工具（如地图、搜索、数据库等）之间建立安全、可扩展的信息通道。它屏蔽了底层接口差异，使开发者无需为每个工具单独编写适配逻辑，即可在智能体或工作流中声明式接入多种能力。该协议基于 Anthropic 提出的开源标准 [MCP 官网](https://modelcontextprotocol.io/) 实现，并已升级为 Streamable HTTP 协议以支持更稳定的外部集成。

## 支持的模型/功能

MCP 服务**不直接绑定特定大模型**，而是通过百炼平台的智能体（Agent）和工作流（Workflow）两类应用承载调用能力：

- **智能体应用**：支持自动决策调用（基于对话上下文触发），最多可同时配置 5 个 MCP 服务；典型场景包括路径规划（Amap Maps）、逻辑推理（Sequential Thinking）、多工具协同（如天气查询 + 图表生成）[官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **工作流应用**：需手动指定 MCP 节点使用的具体工具（如 `maps_weather`），并显式连接输入/输出参数；适用于确定性编排任务，例如“自然语言解析 → 天气查询 → 结果总结”链路 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **外部调用**：支持通过 MCP SDK 或集成至 Cherry Studio/Cursor 等第三方客户端，使用 Streamable HTTP 协议（`/mcp` 端点）或 SSE（`/sse` 端点）进行调用 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

> **注意**：文档 4 明确指出“MCP 服务不能在调用千问 API 时直接接入”，而文档 5 的 FAQ 第 3 条却称“MCP 服务能否在调用千问 API 时接入？不可以”，二者一致；但需强调：MCP 仅在百炼平台内建应用（智能体/工作流）或通过 SDK 外部调用生效，**不支持作为参数透传至 `dashscope` [OpenAI 兼容接口](../concepts/openai-compatible-api.md)的 `tools` 字段中直接使用**。

## 关键参数

MCP 服务配置与调用涉及以下核心参数：

| 参数类别 | 参数名 | 说明 | 示例值 |
|---------|--------|------|--------|
| **服务元信息** | `服务名称` / `描述` | 仅用于控制台识别，不影响模型调用逻辑 | `"长期记忆"`, `"该服务使大模型能够记录个性化信息..."` |
| **部署配置** | `安装方式` | 决定启动方式：`npx`（Node.js）、`uvx`（Python）、`http`（远程 SSE/Streamable HTTP） | `"npx"` |
| | `部署方式` | `基础模式`（按调用时长计费，有冷启动延迟）或 `极速模式`（按部署+调用双计费，常驻内存） | `"基础模式：按次计费"` |
| | `MCP 服务配置` | JSON 格式，必须符合 `mcpServers` 结构，`type` 需与端点协议匹配 | `{ "memory": { "command": "npx", "args": ["@modelcontextprotocol/server-memory"] } }` |
| **调用参数** | `tool.name` | 工具唯一标识，由 MCP Server 声明，模型调用时必须精确匹配 | `"maps_weather"` |
| | `tool.inputSchema` | JSON Schema 描述输入参数结构，影响模型参数生成准确性 | `{"type": "object", "properties": {"city": {"type": "string"}}}` |

> **注意**：文档 5 的错误码 `11200058` 明确要求 `type`（如 `"sse"`）必须与接入路径（如 `/sse`）严格匹配，否则返回 `HTTP 405`；而文档 3 的配置模板未强调此约束，实际部署时须严格校验。

## 使用方式

### 1. 接入官方 MCP 服务
- 前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，选择服务（如 Amap Maps）→ **立即开通**；
- 在智能体/工作流编辑器中，从 MCP 服务列表添加，无需配置密钥（试用版已预置）；
- 敏感参数（如自定义 API Key）需通过 KMS 凭据加密管理 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。

### 2. 部署自定义 MCP 服务
支持三种方式：
- **脚本部署**：上传符合 MCP 协议的代码包（npm/PyPI），通过函数计算 FC 托管；
- **AI 网关导入**：将现有 RESTful API 封装为 MCP 工具；
- **OpenAPI 导入**：将阿里云产品（OSS/ECS）操作发布为 MCP 服务 [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)。

### 3. 外部 SDK 调用
- 使用 `mcp` Python SDK 连接 `streamablehttp_client`；
- 通过 `session.list_tools()` 获取工具列表，转换为 OpenAI `tools` 格式；
- 在 `chat.completions.create` 中启用 `tools`，并处理 `tool_calls` 循环调用 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 限制和注意事项

- **网络与权限限制**：  
  - MCP 服务运行于函数计算 FC，**无法访问用户本地资源（文件、硬件）或本地数据库**；  
  - 访问远程云资源（如 RDS）需配置 FC IP 白名单或 VPC 打通 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

- **协议与兼容性**：  
  - 百炼已全面升级至 **Streamable HTTP 协议**（`/mcp`），旧版 SSE（`/sse`）需手动重新开通以完成升级 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)；  
  - 自定义服务若使用 `npx`/`uvx` 部署，**版本更新后必须手动重新部署**，不会自动同步 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

- **调用与计费**：  
  - 智能体/工作流中调用 MCP 会增加模型输入 Token（返回结果作为上下文）和潜在输出 Token（更详细响应）；  
  - 云部署服务限流为 **15 QPS（主账号与 RAM 子账号共享）**，超出将返回 `HTTP 429` 错误码 `11200051`；  
  - 自定义服务计费分两档：基础模式（0.000156 元/秒，仅调用时计费）与极速模式（0.000156 元/秒调用 + 0.000036 元/秒部署）[模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)。

- **调试建议**：  
  - 模型无法调用 MCP 时，优先检查提示词是否明确工具名称与能力；  
  - 部署失败请按文档 5 的错误码表排查（如 `11200044` 表示连接拒绝，需验证下游服务可达性）；  
  - 生产环境建议启用 FC 日志服务，实时捕获启动与运行日志。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)


