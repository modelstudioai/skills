# 模型上下文协议

模型上下文协议（Model Context Protocol, MCP）是百炼平台提供的标准化、安全、可扩展的工具调用接口协议，用于在大语言模型与外部能力（如地图、搜索、数据库、自定义 API 等）之间建立统一通信通道。它基于开源 [MCP 标准](https://modelcontextprotocol.io/) 实现，并深度适配百炼运行时，屏蔽底层接入差异，使模型能以声明式方式自主发现、规划并调用工具。

## 在百炼平台的不同场景中如何使用

- **智能体（Agent 2.0）**：MCP 服务作为“可规划工具”自动注册到模型上下文。模型根据对话意图自主决定是否调用、调用哪个工具（如 `maps_route` 或 `WebSearch.search`），无需显式编码逻辑。最多可同时挂载 5 个 MCP 服务，配置后即生效。
- **工作流（Workflow）**：MCP 以独立节点形式存在，需手动选择具体工具（如 `firecrawl.crawl_url`），并显式绑定输入变量（如 `query: {{input.query}}`）。适用于确定性、强编排需求的流程。
- **高代码应用（Rich Code）**：通过 Python SDK（如 `fastmcp.Client` 或 `mcp.client.streamable_http`）编程调用，支持多轮会话、流式响应和错误重试，适合深度定制场景。
- **实时多模态 API（Omni-Realtime）**：在 `tools` 参数中以 `type=mcp` 声明，配合 `server_url` 和 `authorization` 配置，实现语音交互中同步触发外部工具（如边听边查天气）。
- **Managed Agents**：通过 `mcp_servers` 字段挂载，与内置工具（`bash`, `web_search` 等）统一纳入沙箱执行调度，支持跨工具状态传递与中断续接。

> ✅ 提示：所有存量 MCP 服务必须完成**协议升级**（控制台取消后重新开通），否则外部调用将失败——新版强制使用 Streamable HTTP 协议（`/mcp` 端点），旧版 SSE 已停用。

## 关键参数和配置

| 参数 | 说明 | 必填 | 注意事项 |
|------|------|------|----------|
| `type` | 协议类型，决定端点与方法 | 是 | 必须为 `"streamableHttp"`（对应 `POST /mcp`）；设为 `"sse"` 将导致 `11200058` 错误 |
| `server_url` | MCP 服务地址（百炼托管或自定义部署） | 是 | 官方服务由平台自动填充；自定义服务需确保公网可达且支持 HTTPS |
| `authorization` | 百炼通用鉴权凭证 | 是 | 固定使用 `DASHSCOPE_API_KEY`，格式：`Bearer <your_api_key>` |
| `tool_name` | 工具标识符（如 `WebSearch.search`） | 调用时必填 | 必须与 `list_tools()` 返回的 `name` 完全一致，区分大小写 |
| `input` | 工具调用参数对象 | 是 | 字段名与类型须严格匹配 `inputSchema`，否则返回 `11200060` 错误 |
| `timeout_ms` | 调用超时（毫秒） | 否 | 默认 30000，建议设为 15000–60000，避免阻塞模型推理 |

- **敏感参数保护**：如 `AMAP_MAPS_API_KEY` 等密钥类参数，必须通过百炼 KMS 凭据加密，禁止明文写入配置。
- **限流策略**：按主账号+RAM 子账号共享 QPS 限额（如 WebSearch 为 15 QPS），非单服务实例级限制。

## 面向开发者的实用建议

- ✅ **快速验证**：用 CLI 一行调试  
  ```bash
  bl mcp call --target WebSearch.search --args '{"query":"MCP协议最新特性"}'
  ```
- ✅ **SDK 推荐**：Python 开发优先使用 `mcp.client.streamable_http` 客户端，兼容 OpenAI 工具调用风格，支持自动重连与流式解析。
- ✅ **错误排查**：遇到 `112000xx` 错误码，直接查 [MCP 常见问题](raw/application-user-guide/model-context-protocol/mcp-faq.md) 对应条目，90% 问题源于 `type` 配置错误、参数 schema 不匹配或未完成协议升级。
- ⚠️ **网络注意**：自定义 MCP 服务运行于函数计算（FC），**无固定出口 IP**，访问云数据库等资源需配置白名单或 VPC 打通；**无法访问本地文件或设备**。
- ⚠️ **计费提醒**：官方 MCP 服务（如 WebSearch）按调用量计费（29 元/千次）；自定义服务按调用时长计费（基础模式 0.000156 元/秒），高频场景建议启用“极速模式”。

> 💡 最佳实践：新项目一律使用 `streamableHttp` 类型 + `/mcp` 端点；已有服务务必执行“取消→重开通”操作完成升级；第三方客户端（Cursor/Cherry Studio）请通过 MCP 广场一键导出 JSON 配置，避免手动拼接 URL。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [managed agents](../guides/managed-agents.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [llm application](../guides/llm-application.md)
- [application support](../guides/application-support.md)


