# model context protocol

[模型上下文协议](../concepts/mcp.md)（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化接口协议，用于在大语言模型与外部工具（如地图、搜索、数据库等）之间建立安全、可扩展的信息通道。它屏蔽了工具接入的底层差异，使开发者无需为每个第三方服务单独编写适配代码，即可在智能体或工作流中声明式调用能力。该协议基于 Anthropic 提出的开源标准 [MCP 官网](https://modelcontextprotocol.io/) 实现，并已升级为 Streamable HTTP 协议以支持更稳定的外部集成。

## 支持的模型/功能

MCP 服务**不直接绑定特定大模型**，而是通过百炼平台的智能体（Agent）和工作流（Workflow）两类应用载体提供能力：

- **智能体应用**：支持自动推理调用。大模型根据用户输入自然语言判断是否需调用 MCP 工具，并自动生成参数；单个智能体最多可同时配置 5 个 MCP 服务 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **工作流应用**：支持显式编排调用。每个 MCP 节点仅能绑定一个具体工具（如 `maps_weather`），需手动配置输入参数映射与输出参数传递，适合确定性任务链路 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。

当前支持的 MCP 服务分为两类：
- **官方云部署服务**：由百炼预置并托管，如 Amap Maps（地理信息）、WebSearch（联网搜索）、Firecrawl（网页爬取）、Sequential Thinking（逻辑推理）、QuickChart（图表生成）等，开通即用。
- **自定义服务**：支持三种部署方式：① 使用脚本（npx/uvx）部署开源或自研 MCP Server；② 通过 AI 网关将现有 RESTful API 封装为 MCP 工具；③ 通过 OpenAPI 开发者门户将阿里云产品（如 OSS、ECS）能力发布为 MCP 服务 [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)。

> **注意**：文档 4 明确指出“MCP 服务需集成在智能体或工作流应用中使用，不能直接在调用千问 API 时接入”，而文档 1 中“大模型应用：智能体应用”“大模型应用：工作流应用”的表述易被误解为模型本身原生支持 MCP。实际是百炼平台层封装了协议交互逻辑，模型仅作为协议消费者参与调用决策与结果处理。

## 关键参数

MCP 服务配置涉及两类关键参数：

### 服务级参数（部署时指定）
| 参数 | 说明 | 示例值 |
|------|------|--------|
| `type` | 通信协议类型，决定端点路径与请求方式 | `"stdio"`（本地进程）、`"sse"`（`/sse`）、`"streamableHttp"`（`/mcp`） |
| `command` / `url` | 启动命令或远程服务地址 | `"npx"` 或 `"https://your-server/mcp"` |
| `env` | 环境变量（如 API Key），敏感字段需通过 KMS 凭据加密 | `{"AMAP_MAPS_API_KEY": "xxx"}` |
| 部署模式 | 基础模式（按调用时长计费，有冷启动延迟）或极速模式（额外收取部署时长费，常驻内存） | 基础模式 |

### 工具级参数（运行时传递）
- 每个 MCP 工具定义明确的 `inputSchema`（JSON Schema 描述输入参数名、类型、是否必填）和 `outputSchema`。
- 在工作流中，必须通过节点配置将上游输出（如“信息提取/result”）**显式映射**到 MCP 工具的输入字段（如 `city: string`）[官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。

## 使用方式

### 平台内集成（推荐入门）
1. **开通服务**：前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，选择服务（如 Amap Maps）→ 点击“立即开通”。
2. **配置应用**：
   - *智能体*：创建后在“MCP 服务”模块添加，无需指定工具，模型自动选择；
   - *工作流*：拖入 MCP 节点 → 选择服务及具体工具（如 `maps_weather`）→ 在配置中设置输入参数来源（如引用上游节点输出）。
3. **测试验证**：发送符合工具能力的自然语言指令（如“查询杭州天气”），观察是否触发调用及返回结果。

### 外部调用（面向第三方集成）
- **一键配置**：支持 Cherry Studio、Cursor 等 IDE，通过控制台“外部调用”页点击“一键配置”自动注入服务元数据。
- **SDK 编程集成**：使用 `mcp` SDK 连接 Streamable HTTP 端点（如 `https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp`），配合 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)实现多轮工具调用循环 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 限制和注意事项

- **网络与权限限制**：
  - 自定义 MCP 服务运行于函数计算 FC，**无固定出口 IP**，访问云数据库等资源需配置 IP 白名单或 VPC 打通 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)；
  - **不支持访问用户本地资源**（如本地文件、硬件设备），此类服务需本地部署 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

- **协议与兼容性**：
  - 百炼已全面升级至 **Streamable HTTP 协议**（`/mcp` 端点），旧版 SSE（`/sse`）需手动取消再重新开通以完成升级 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)；
  - 配置中的 `type` 必须与端点路径严格匹配（`"sse"` → `/sse`，`"streamableHttp"` → `/mcp`），否则触发错误码 `11200058` [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

- **调用与计费**：
  - 智能体调用 MCP 会增加模型输入 [Token](../concepts/token.md)（工具返回内容计入上下文）和潜在输出 [Token](../concepts/token.md)（更详尽响应）；
  - 云部署服务中，联网搜索等存在 **2000 次/月免费额度**，超量后按 29 元/千次计费；自定义服务按调用时长（0.000156 元/秒）或部署时长（0.000036 元/秒）计费 [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)。

- **调试建议**：
  - 若调用失败，优先检查错误码（如 `11200044` 表示连接拒绝，`11200049` 表示鉴权失败），并使用 `curl` 直连服务端点验证；
  - 自定义服务部署失败时，需确认：① 本地可运行；② 无浏览器/本地依赖；③ 配置代码与安装方式（npx/uvx/http）一致；④ FC 权限与账号状态正常 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)


