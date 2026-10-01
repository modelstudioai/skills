# model context protocol

[模型上下文协议](../concepts/mcp.md)（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化机制，用于在大语言模型与外部工具（如地图、爬虫、天气、数据库等）之间建立安全、可扩展的信息通道。它基于 Anthropic 提出的开源 MCP 标准 [MCP 官网](https://modelcontextprotocol.io/) 实现，无需为每个工具重复开发适配层。开发者可通过官方服务、自定义部署或外部 SDK 三种方式快速集成。

## 支持的模型/功能

MCP 协议本身不绑定特定模型，但其调用能力**仅在百炼平台的智能体（Agent）和工作流（Workflow）应用中可用**，不支持直接在调用千问 API（如 `qwen-max` 的 [OpenAI 兼容接口](../concepts/openai-compatibility.md)）时接入 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。  
当前支持的典型能力包括：
- **地理信息处理**：通过 Amap Maps MCP 服务实现路径规划、天气查询（`maps_weather` 工具）等；
- **网页内容获取**：通过 Firecrawl MCP 服务执行网页爬取；
- **逻辑推理增强**：通过 Sequential Thinking MCP 服务辅助多步推理；
- **图表生成**：结合 QuickChart MCP 服务将结构化数据转为可视化图表；
- **[长期记忆](../concepts/memory.md)管理**：通过 Knowledge Graph Memory 等自定义服务存储与检索用户上下文。

> **注意**：文档 5 中提到“支持通过 OpenAI SDK + MCP SDK 调用百炼联网搜索 MCP 服务”，但文档 3 明确指出“MCP 服务不能在调用千问 API 时接入”。实际可行的是：**SDK 调用的是百炼托管的 MCP Server（即 `mcp` 接口），而非直接让千问模型调用工具**；模型侧仍需运行在百炼智能体/工作流环境中才能触发工具调用。该差异已在[官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)中得到验证。

## 关键参数

MCP 服务配置与调用涉及以下核心参数：

| 参数类别 | 参数名 | 说明 | 示例值 |
|----------|--------|------|--------|
| **服务元信息** | `服务名称` / `描述` | 仅用于控制台识别，不影响模型调用逻辑 | `"杭州天气查询"` / `"调用高德API获取实时天气"` |
| **传输协议** | `type` | 必须与端点路径严格匹配：`"sse"` → `/sse`；`"streamableHttp"` → `/mcp` | `"streamableHttp"` |
| **部署配置** | `command` / `args` | `npx` 或 `uvx` 启动命令及参数，需与服务包兼容 | `"npx", ["-y", "@modelcontextprotocol/server-memory"]` |
| **环境变量** | `env` | 用于注入敏感凭据（如 `AMAP_MAPS_API_KEY`），**必须通过 KMS 加密** | `{"AMAP_MAPS_API_KEY": "kms://xxx"}` |
| **网络地址** | `url` | 远程服务地址，需确保函数计算 FC 可访问（注意 IP 白名单/VPC 配置） | `"https://my-server.example.com/sse"` |

所有参数均在 [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md) 的“使用脚本部署”章节中明确定义。

## 使用方式

### 1. 平台内集成（推荐）
- **智能体应用**：最多可同时添加 5 个 MCP 服务；模型根据对话自动判断是否调用及选择工具，无需显式指定 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **工作流应用**：每个 MCP 节点**只能绑定一个工具**（如 `maps_weather`），需手动配置输入参数（如从上游大模型节点提取城市名）并传递输出结果。

### 2. 外部调用
- **第三方应用集成**：支持一键配置至 Cherry Studio、Cursor 等工具，自动注入 `DASHSCOPE_API_KEY` 和服务 URL。
- **SDK 开发集成**：使用 `mcp` Python SDK（如 `streamablehttp_client`）连接百炼 MCP Server，再通过 [OpenAI 兼容接口](../concepts/openai-compatibility.md)驱动模型调用工具链 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 限制和注意事项

- **网络与权限**：MCP 服务托管于函数计算 FC，**无固定出口 IP**，访问云数据库等远程资源时需配置 IP 白名单或 VPC 打通 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)；**不支持访问本地文件、硬件或数据库**。
- **版本与更新**：通过 `npx`/`uvx` 部署的服务**不会自动同步上游包更新**，版本变更后需手动重新部署 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **Token 开销**：MCP 返回结果会作为上下文输入模型，**显著增加输入 Token 数量**；模型响应也可能因信息更丰富而变长，间接增加输出 Token [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **错误排查**：常见错误码（如 `11200044` 连接拒绝、`11200059` 404 路径错误）需结合 `curl` 测试、FC 日志及协议类型（`sse` vs `streamableHttp`）交叉验证 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **计费模式**：自定义服务分“基础模式”（按调用时长计费，有冷启动延迟）和“极速模式”（额外收取部署时长费，适合高频调用）；云部署服务按第三方 API 调用量计费，百炼不收中间费用 [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)


