# model context protocol

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化机制，用于在大模型与外部工具（如地图、搜索、天气等服务）之间建立安全、可扩展的信息通道。它屏蔽了底层接口差异，使开发者无需为每个工具单独编写适配逻辑，即可在智能体或工作流中声明式接入多种能力。该协议基于 Anthropic 提出的开源标准 [MCP 官网](https://modelcontextprotocol.io/) 实现，并已升级为 Streamable HTTP 协议以支持更稳定的外部集成。

## 支持的模型/功能

MCP 服务本身不绑定特定大模型，但其调用行为由百炼平台内运行的推理模型（如通义千问-Max、Qwen3 系列）驱动。当前支持以下两类使用场景：

- **平台内集成**：在[智能体应用](raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)和[工作流应用](raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)中直接配置并调用 MCP 服务。智能体支持自动决策调用（最多 5 个并发服务），工作流需手动指定工具并串联参数流。
- **外部调用**：通过 SDK、CLI 或第三方 IDE（如 Cherry Studio、Cursor）集成，支持 `streamableHttp`（推荐）和 `sse` 两种传输方式。详见[外部调用](raw/application-user-guide/model-context-protocol/mcp-external-calls.md)文档。

官方已预置 Amap Maps、WebSearch（联网搜索）、QuickChart、Sequential Thinking 等 MCP 服务；同时支持自定义部署，包括脚本托管（npx/uvx）、AI 网关封装 RESTful API、OpenAPI 云资源操作三种方式。

> **注意**：文档 4 明确指出“MCP 服务不能在调用千问 API 时直接接入”，而文档 2 中“外部调用 MCP 服务”章节未强调此限制。实际开发中，MCP 仅可在百炼平台创建的智能体/工作流应用中生效，**不可作为独立中间件注入到任意 OpenAI 兼容 API 调用链中**。

## 关键参数

| 参数 | 说明 | 示例值 | 来源 |
|------|------|--------|------|
| `DASHSCOPE_API_KEY` | 百炼通用鉴权凭证，用于所有 MCP 服务调用（含 One Key 服务） | `sk-xxx` | [官方 MCP 服务](raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md) |
| `mcp_url` | 外部调用地址，格式为 `https://dashscope.aliyuncs.com/api/v1/mcps/{service-name}/mcp` | `https://.../WebSearch/mcp` | [外部调用](raw/application-user-guide/model-context-protocol/mcp-external-calls.md) |
| `type`（配置项） | 自定义服务部署时指定通信协议类型 | `"stdio"`（本地）、`"sse/streamableHttp"`（远程） | [自定义 MCP 服务](raw/application-user-guide/model-context-protocol/custom-mcp.md) |
| `command` & `args` | npx/uvx 部署必需字段，定义启动命令及参数 | `"npx"`, `["-y", "@modelcontextprotocol/server-memory"]` | [自定义 MCP 服务](raw/application-user-guide/model-context-protocol/custom-mcp.md) |

## 使用方式

1. **开通服务**  
   - One Key 服务（如 Amap Maps）：首次调用自动生效，无需手动开通。  
   - 其他广场服务：需前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market) 点击“立即开通”。  
   - *升级提示*：旧版 SSE 服务需先“取消开通”再重新开通，以启用新版 Streamable HTTP 协议（见[外部调用](raw/application-user-guide/model-context-protocol/mcp-external-calls.md)）。

2. **平台内配置**  
   - **智能体**：在应用编辑页 → “MCP 服务” → 添加服务 → 保存后即可在对话中自动触发。  
   - **工作流**：拖入 MCP 节点 → 选择具体工具（如 `maps_weather`）→ 手动绑定输入参数（如引用上游节点输出）→ 连接下游节点处理结果。

3. **外部调用**  
   - CLI：`bl mcp list` 查看服务，`bl mcp call --target amap-maps.maps_route` 直接调用。  
   - SDK：使用 `mcp.client.streamable_http` 客户端连接 `mcp_url`，配合 OpenAI SDK 实现工具调用循环（见[外部调用](raw/application-user-guide/model-context-protocol/mcp-external-calls.md)示例代码）。

## 限制和注意事项

- **地域与网络**：自定义 MCP 服务托管于函数计算 FC，无固定出口 IP。若需访问云数据库等资源，必须配置 IP 白名单或 VPC 打通（见[常见问题](raw/application-user-guide/model-context-protocol/mcp-faq.md)）。
- **敏感数据**：云部署 MCP 服务默认使用 KMS 加密凭据（如 AMAP_MAPS_API_KEY），禁止明文配置。
- **[Token](../concepts/token.md) 消耗**：MCP 返回结果将作为上下文注入模型，**显著增加输入 [Token](../concepts/token.md) 数量**；模型响应也可能因信息更丰富而延长，间接增加输出 [Token](../concepts/token.md)。
- **版本管理**：通过 `npx/uvx` 部署的服务，版本更新后需手动重新部署，不会自动同步（见[常见问题](raw/application-user-guide/model-context-protocol/mcp-faq.md)）。
- **错误排查**：常见连接失败（如 `MCP_CONNECTION_REFUSED`、`MCP_INIT_TIMEOUT`）多因配置路径/协议不匹配（`sse` vs `/mcp`）、冷启动延迟或 FC 权限缺失，建议优先检查 [MCP 管理](https://bailian.console.aliyun.com/?tab=app#/mcp-manage) 中的部署状态与日志。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)


