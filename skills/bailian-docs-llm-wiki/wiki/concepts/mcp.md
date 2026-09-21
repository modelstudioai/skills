# 模型上下文协议

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台实现大模型与外部能力安全、标准化集成的核心通信机制。它定义了一套统一的工具发现、调用与响应规范，使大模型能在推理过程中按需、可验证地调用地图、数据库、知识库、SaaS 应用等外部服务，而无需硬编码适配逻辑。

## 在百炼平台的不同场景中，这个概念如何使用

MCP 不是独立运行的服务，而是贯穿百炼多个能力层的**协议层基础设施**，其使用方式因场景而异：

- **智能体（Agent）应用**：在编辑器中直接添加已开通的 MCP 服务（如 Amap Maps、[长期记忆](memory.md)），模型基于对话上下文自动决策是否调用、调用哪个工具及传入参数。最多支持同时配置 5 个 MCP 服务，适用于动态、多跳的自主任务（如“规划从杭州到上海的路线并查沿途天气”）。

- **工作流（Workflow）应用**：以显式节点形式接入 MCP 工具（如 `maps_weather`），需手动连接输入字段（如 `city`）与上游输出，并配置失败重试策略。适用于确定性、可审计的编排链路（如“用户提问 → 解析城市名 → 调用天气 MCP → 生成摘要”）。

- **Connector（数据连接中枢）**：所有第三方系统（OSS、Salesforce、钉钉、语雀等）和平台托管资源（文件、表格）均通过 MCP 协议暴露为标准化工具。创建连接器后，系统自动生成符合 MCP 规范的工具列表（如 `search_file`、`get_table_schema`），供智能体或工作流直接调用。

- **知识库（Knowledge Base）**：知识检索能力可通过 MCP Server 形式对外提供（如供 Qoder、Claude Code 等客户端调用）。此时知识库不作为 RAG 后端被动响应，而是作为主动可发现、可调用的 MCP 工具，支持 `search_knowledge` 等语义化操作。

- **外部 SDK 集成**：开发者可使用官方 `mcp` Python SDK 连接百炼 MCP 服务端点（`/mcp` 或 `/sse`），调用 `list_tools()` 获取工具元信息，并将结果转换为 OpenAI 兼容的 `tools` 格式，嵌入自有 LLM 调用流程中，实现跨平台能力复用。

> ⚠️ 注意：MCP **不支持**在直接调用千问 API（如 `dashscope` [OpenAI 兼容接口](openai-compatible-api.md)）时，通过 `tools` 参数透传使用。它仅在百炼原生应用（智能体/工作流）或通过 MCP SDK 外部调用两种模式下生效。

## 关键参数和配置

MCP 的配置与调用围绕三个核心层级展开，开发者需重点关注以下参数：

| 层级 | 参数 | 说明 | 示例值 |
|------|------|------|--------|
| **服务注册** | `type` | 协议类型，必须与接入路径严格匹配：`sse` → `/sse`，`streamablehttp` → `/mcp` | `"sse"` |
| | `mcpServers`（JSON） | 控制台部署配置主体，声明服务名称、启动命令与参数 | `{ "weather": { "command": "npx", "args": ["@mcp/server-weather"] } }` |
| **工具调用** | `tool.name` | 工具唯一标识符，由 MCP Server 声明，模型调用时必须精确匹配 | `"maps_weather"` |
| | `tool.inputSchema` | JSON Schema 描述输入参数结构，直接影响模型生成参数的准确性与合法性 | `{"type":"object","properties":{"city":{"type":"string"}}}` |
| **客户端连接** | `url` | MCP 服务端点地址（Streamable HTTP 或 SSE） | `https://xxx.cn-beijing.maas.aliyuncs.com/api/v2/connector/mcp` |
| | `headers.Authorization` | 认证头，固定为 `Bearer ${DASHSCOPE_API_KEY}` | `Bearer sk-xxx` |

> ✅ 实践提示：部署自定义 MCP 服务时，务必校验 `type` 与端点路径的一致性，否则将返回 `HTTP 405 Method Not Allowed`（错误码 `11200058`）。

## 面向开发者，简洁实用

- **快速上手**：优先使用 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market) 中的官方服务（如“[长期记忆](memory.md)”“Amap Maps”），开通即用，免密钥配置。
- **调试技巧**：在智能体 Playground 中开启「工具调用日志」，实时查看模型生成的 `tool_calls` 及实际返回结果，快速定位 schema 不匹配或参数缺失问题。
- **安全红线**：MCP 服务运行于函数计算（FC），**无法访问本地文件、硬件或未授权的远程数据库**；敏感凭证（API Key、OAuth Token）必须通过 KMS 加密管理，禁止硬编码。
- **性能选择**：对低延迟要求高的场景（如实时对话），选用“极速模式”（常驻内存）；对成本敏感且调用量低的场景，选“基础模式”（按次计费+冷启动）。
- **扩展建议**：若需将自有 RESTful API 接入 MCP，推荐使用百炼 AI 网关的「API 封装」功能，自动注入认证、限流与协议转换逻辑，无需修改业务代码。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [overview](../guides/overview.md)
- [knowledge base](../guides/knowledge-base.md)
- [application component api reference](../api/application-component-api-reference.md)
- [rag api](../api/rag-api.md)


