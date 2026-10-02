# model context protocol

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化接口协议，用于在大语言模型与外部工具（如地理服务、网页爬取、天气查询等）之间建立安全、可扩展的信息通道。它屏蔽了底层通信细节，使开发者无需为每个工具单独开发适配逻辑，即可在智能体或工作流中声明式接入多种能力。该协议基于 Anthropic 提出的开源标准 [MCP 官网](https://modelcontextprotocol.io/) 实现，并已升级为 Streamable HTTP 协议以支持更稳定的外部集成。

## 支持的模型/功能

MCP 协议本身不绑定特定模型，但其能力需通过百炼平台的**智能体应用**和**工作流应用**触发与编排。当前支持以下两类服务接入方式：

- **官方 MCP 服务**：由阿里云百炼预部署并托管的服务，开箱即用，包括 Amap Maps（地理信息）、WebSearch（联网搜索）、Firecrawl（网页爬取）、Sequential Thinking（逻辑推理）、QuickChart（图表生成）等。其中 Amap Maps 服务限时免费，联网搜索服务提供 2000 次/月免费额度 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **自定义 MCP 服务**：支持三种部署路径：
  - *使用脚本部署*：通过函数计算（FC）托管符合 MCP 协议的 `stdio` 类型服务（如 Node.js 的 `npx` 或 Python 的 `uvx` 启动）；
  - *从 AI 网关导入*：将现有 RESTful API 封装为 MCP 工具；
  - *从阿里云 OpenAPI 导入*：将 OSS、ECS 等云产品 OpenAPI 快速发布为 MCP 服务 [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)。

> **注意**：文档 4 明确指出 MCP 服务已从旧版 SSE 协议升级为新版 Streamable HTTP 协议；而文档 2 中部分截图及描述仍沿用 SSE 术语（如“服务器发送事件 (sse)”），实际生产环境应以 `/mcp` 端点和 `streamableHttp` 类型为准 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 关键参数

MCP 服务配置与调用涉及以下核心参数：

- **服务类型标识**：`type` 字段必须与接入端点严格匹配——`"sse"` 对应 `GET /sse`，`"streamableHttp"` 对应 `POST /mcp`；配置错误将导致 `11200058`（METHOD_NOT_ALLOWED）或 `11200059`（NOT_FOUND）错误 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **命令与参数**：`command`（如 `"npx"`）、`args`（如 `["-y", "@modelcontextprotocol/server-memory"]`）和 `env`（敏感环境变量需通过 KMS 凭据加密）。
- **网络配置**：`url`（远程服务地址）、`deployment region`（部署地域，推荐北京以降低延迟）。
- **认证凭证**：外部调用需设置 `DASHSCOPE_API_KEY`；部分服务（如商业化 Amap Maps）需额外传入 `AMAP_MAPS_API_KEY`，且须确保其权限充足、余额/额度未耗尽。

## 使用方式

### 平台内集成（智能体/工作流）
- **智能体应用**：最多可同时添加 5 个 MCP 服务；模型根据对话自动判断是否调用及选择工具，无需显式指定参数（如发送“从杭州萧山国际机场到西湖景区”即可触发 Amap Maps 路径规划）。
- **工作流应用**：每个 MCP 节点仅能绑定一个工具（如 `maps_weather`），需手动配置输入参数（常通过前置大模型节点提取城市名）和输出参数传递链路。

### 外部调用
- **第三方 IDE 集成**：支持 Cherry Studio、Cursor 等工具的一键自动配置，或手动导入 JSON 配置（含 `name`、`type`、`url`、`headers`）。
- **SDK 编程集成**：推荐使用 `mcp` SDK + `openai` SDK 组合，通过 `streamablehttp_client` 连接 `/mcp` 端点，获取工具列表后转为 OpenAI `tools` 格式，驱动多轮工具调用循环。

## 限制和注意事项

- **协议兼容性**：仅支持标准 MCP 协议实现的服务；非标准或依赖本地资源（如文件系统、硬件）的 MCP Server 无法在百炼函数计算环境中部署 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **网络与安全**：
  - 自定义服务若需访问远程数据库，须配置 FC 出口 IP 白名单或 VPC 打通；
  - 不支持访问用户本地资源（如本地数据库）；
  - 敏感凭据（如 API Key）必须通过 KMS 加密管理。
- **计费与限流**：
  - 官方服务中，联网搜索限流 15 QPS（主账号与 RAM 子账号共享），超限返回 `11200051` 错误；
  - 自定义服务分“基础模式”（按调用时长计费，0.000156 元/秒）和“极速模式”（另收部署费 0.000036 元/秒），冷启动延迟仅存在于基础模式。
- **模型交互影响**：MCP 返回结果会作为上下文注入模型输入，直接增加输入 [Token](../concepts/token.md)；同时可能因信息更丰富而间接增加输出 [Token](../concepts/token.md) [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **版本更新**：通过 `npx`/`uvx` 部署的服务，上游包版本更新后需手动重新部署，不会自动同步。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)


