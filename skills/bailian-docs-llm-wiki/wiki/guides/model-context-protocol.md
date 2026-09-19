# model context protocol

[模型上下文协议](../concepts/mcp.md)（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化机制，用于在大模型与外部工具（如地图、搜索、图表生成等）之间建立安全、可扩展的信息通道。它屏蔽了底层接口差异，使开发者无需为每个工具单独编写适配逻辑，即可在智能体或工作流中声明式接入多种能力。该协议基于 Anthropic 提出的开源标准 [MCP 官网](https://modelcontextprotocol.io/) 实现，并针对百炼平台进行了工程化增强和托管支持。

## 支持的模型/功能

MCP 本身不绑定特定大模型，而是作为**工具调用层协议**，由百炼平台的智能体（Agent）和工作流（Workflow）应用统一承载。当前支持以下两类使用场景：

- **智能体应用**：大模型根据对话上下文自动判断是否调用、调用哪个 MCP 工具及传入参数，支持单次调用多个工具（最多 5 个），适用于自然语言驱动的动态任务（如“规划从杭州机场到西湖的三种公交方案”）。详情见[官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **工作流应用**：需显式配置 MCP 节点，每个节点仅绑定一个工具（如 `maps_weather`），输入参数需通过前置大模型节点解析（如提取城市名），输出参数需手动传递至后续节点，适用于结构化、确定性的业务流程。

支持的 MCP 服务分为两类：
- **官方 MCP 服务**：由百炼预部署并托管，包括 Amap Maps（地理信息）、WebSearch（联网搜索）、Firecrawl（网页爬取）、Sequential Thinking（逻辑推理）、QuickChart（图表生成）等，开通即用。
- **自定义 MCP 服务**：支持三种部署方式：① 使用脚本部署（npx/uvx 托管本地 MCP Server）；② 从 AI 网关导入（将现有 RESTful API 封装为 MCP 工具）；③ 从阿里云 OpenAPI 导入（将 OSS/ECS 等云产品能力暴露为工具）。详见[自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)。

> **注意**：文档 4 中提到“百炼 MCP 服务已从旧版 SSE 协议升级为新版 Streamable HTTP 协议”，但文档 2 和文档 3 的配置示例仍混用 `sse` 和 `streamableHttp` 类型。实际部署时，必须严格匹配端点路径：`type: "sse"` 对应 `/sse` 端点（GET），`type: "streamableHttp"` 对应 `/mcp` 端点（POST），否则将触发错误码 `11200058` 或 `11200059`（见[文档 5](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)）。

## 关键参数

MCP 服务配置的核心参数取决于部署方式，通用关键项如下：

| 参数 | 说明 | 示例值 | 来源 |
|------|------|--------|------|
| `type` | 通信协议类型 | `"stdio"`, `"sse"`, `"streamableHttp"` | [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md) |
| `command` / `url` | 启动命令或服务地址 | `"npx"`, `"https://your-server/mcp"` | [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md) |
| `env` | 环境变量（用于密钥、配置） | `{"AMAP_MAPS_API_KEY": "xxx"}` | [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md) |
| `deploymentMode` | 部署模式 | `"basic"`（按次计费）或 `"ultra"`（极速模式） | [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md) |
| `region` | 部署地域 | `"cn-beijing"` | [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md) |

> **注意**：敏感环境变量（如 API Key）必须通过 KMS 凭据加密，直接明文写入配置存在安全风险（见[官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)）。

## 使用方式

### 1. 开通服务
- **官方服务**：前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，点击服务卡片 → “立即开通” → “确认开通”。试用服务（如 Amap Maps）无需填写 API Key。
- **自定义服务**：前往 [MCP 管理](https://bailian.console.aliyun.com/?tab=app#/mcp-manage)，选择部署方式（脚本/AI 网关/OpenAPI）→ 填写配置 → 提交部署。

### 2. 在应用中集成
- **智能体**：创建智能体 → “添加 MCP 服务” → 从已开通列表中勾选（最多 5 个）→ 保存后即可在对话中自动触发。
- **工作流**：创建工作流 → 拖入 MCP 节点 → 选择已开通的服务及具体工具（如 `maps_weather`）→ 配置输入参数（支持引用上游节点输出）→ 连接至下游节点。

### 3. 外部调用
支持两种集成方式：
- **第三方应用**：在 MCP 服务详情页的“外部调用”界面，一键配置至 Cherry Studio 或 Cursor（自动注入 DASHSCOPE_API_KEY 和服务元数据）。
- **自有项目**：使用 MCP SDK（如 `mcp.client.streamable_http`）连接百炼 MCP endpoint（如 `https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp`），配合 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)实现工具调用循环。参考代码见[外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 限制和注意事项

- **平台限制**：MCP 服务**仅可在百炼智能体或工作流应用中使用**，无法直接接入千问 API 的裸调用（见[文档 5](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)）。
- **网络限制**：自定义 MCP 服务托管于函数计算 FC，无固定出口 IP，若需访问云数据库等资源，必须配置 IP 白名单或 VPC 打通（见[文档 5](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)）。
- **本地资源限制**：不支持访问用户本地文件、硬件或数据库（见[文档 5](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)）。
- **版本与更新**：通过 npx/uvx 部署的服务，其 npm/PyPI 包版本更新后**不会自动同步**，需手动重新部署（见[文档 5](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)）。
- **[Token](../concepts/token.md) 影响**：MCP 返回结果会作为上下文注入模型输入，显著增加输入 [Token](../concepts/token.md)；同时可能因信息更丰富而延长输出，间接增加输出 [Token](../concepts/token.md)（见[文档 5](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)）。
- **错误排查**：常见连接失败（如 `11200044`）、超时（`11200045`/`11200046`）、鉴权失败（`11200049`）等问题，需结合 `curl` 测试、FC 日志及下游服务文档定位（见[文档 5](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)）。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)


