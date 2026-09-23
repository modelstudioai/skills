# model context protocol

[模型上下文协议](../concepts/mcp.md)（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化接口协议，用于在大语言模型与外部工具（如地图、搜索、数据库等）之间建立安全、可扩展的信息通道。通过 MCP，开发者无需为每个工具单独开发适配层，即可在智能体或工作流中声明式接入官方或自定义工具服务。该协议基于 [MCP 官网](https://modelcontextprotocol.io/) 开源标准实现，当前百炼平台采用 Streamable HTTP 协议（替代旧版 SSE），并提供全托管部署与外部 SDK 集成能力。

## 支持的模型/功能

- **适用场景**：仅支持在百炼平台内的 **智能体应用** 和 **工作流应用** 中使用，不支持直接在调用千问 API（如 `qwen-max` [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)）时接入 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **官方服务**：已预置 Amap Maps（地理信息）、WebSearch（联网搜索）、Firecrawl（网页爬取）、Sequential Thinking（逻辑推理）、QuickChart（图表生成）等 MCP 服务，开通后即用 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **自定义服务**：支持三种部署方式：
  - **脚本部署**（npx/uvx）：适用于 Node.js/Python 编写的开源或自研 MCP 服务（如 `@modelcontextprotocol/server-memory`）；
  - **AI 网关导入**：将现有 RESTful API 封装为 MCP 工具；
  - **OpenAPI 导入**：将阿里云产品（如 OSS、ECS）操作能力发布为 MCP 服务 [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)。

> **注意**：文档 4 提到“MCP 服务已从旧版 SSE 协议升级为新版 Streamable HTTP 协议”，但文档 2 的示例截图及部分配置项（如 `type: "sse/streamableHttp"`）仍混用旧术语；实际部署时请严格按 `type` 字段与端点路径匹配：`"sse"` 对应 `/sse`（GET），`"streamableHttp"` 对应 `/mcp`（POST）[MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `type` | 传输协议类型，决定连接方式与端点路径 | `"stdio"`（本地）、`"sse"`、`"streamableHttp"` |
| `command` / `url` | 启动命令（npx/uvx）或远程服务地址 | `"npx"` / `"https://your-mcp-server/mcp"` |
| `env` | 环境变量，用于传递敏感凭据（如 API Key） | `{"AMAP_MAPS_API_KEY": "xxx"}` |
| `inputSchema` | 工具输入参数的 JSON Schema，影响模型参数生成准确性 | `{"type": "object", "properties": {"city": {"type": "string"}}}` |

- 所有敏感字段（如 API Key）必须通过 KMS 凭据加密，不可明文写入配置 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- 自定义服务配置中 `mcpServers` 字段需严格遵循 JSON 格式，且 `type` 必须与下游服务实际暴露的协议一致，否则触发 `11200054 - MCP_PROTOCOL_ERROR` 或 `11200058 - MCP_SERVER_HTTP_METHOD_NOT_ALLOWED` 错误 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 使用方式

### 在智能体中使用
- 最多可同时添加 **5 个 MCP 服务**；
- 模型根据对话自动判断是否调用及选择工具，无需显式指令；
- 示例：添加 Amap Maps 后，发送“从杭州萧山国际机场到西湖景区，提供三种公交方案”，模型将自动调用 `maps_route` 工具 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。

### 在工作流中使用
- 每个 MCP 节点**仅能绑定一个工具**（如 `maps_weather`），需手动指定输入参数来源（如引用上游节点输出）；
- 通常需前置大模型节点进行自然语言→结构化参数转换（如提取城市名），后置节点处理工具返回结果 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。

### 外部调用
- 支持集成至 Cherry Studio、Cursor 等第三方客户端，提供一键自动配置；
- 通过 MCP SDK（如 `mcp.client.streamable_http`）与 OpenAI SDK 组合调用，代码示例见 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 限制和注意事项

- **网络限制**：自定义 MCP 服务运行于函数计算 FC，**无固定出口 IP**，访问云数据库等资源需配置 IP 白名单或 VPC 打通 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **本地资源**：**不支持访问用户本地文件、硬件或数据库**；依赖本地环境的服务（如需读取本地 CSV）无法云端部署 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **版本更新**：通过 `npx/uvx` 部署的服务，下游包版本更新后**不会自动同步**，需手动重新部署 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **计费模式**：
  - 云部署服务：调用费用由第三方收取（如高德 API），百炼不收费；
  - 自定义服务：基础模式按调用时长计费（0.000156 元/秒），极速模式另收部署费（0.000036 元/秒） [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)。
- **[Token](../concepts/token.md) 影响**：MCP 返回内容会作为上下文注入模型输入，**显著增加输入 [Token](../concepts/token.md) 数量**；复杂工具链可能导致输出 [Token](../concepts/token.md) 间接增长 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)


