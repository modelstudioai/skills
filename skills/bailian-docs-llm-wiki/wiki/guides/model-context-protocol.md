# model context protocol

[模型上下文协议](../concepts/mcp.md)（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化接口协议，用于在大模型与外部工具（如地图、搜索、数据库等）之间建立安全、可扩展的信息通道。它屏蔽了底层通信细节，使开发者无需为每个工具单独开发适配逻辑，即可在智能体或工作流中声明式接入多种能力。该协议基于 Anthropic 提出的开源标准 [MCP 官网](https://modelcontextprotocol.io/) 实现，并已升级为 Streamable HTTP 协议以支持更稳定的外部集成。

## 支持的模型/功能

MCP 服务本身不绑定特定大模型，但其调用行为依赖于百炼平台内应用所配置的推理模型能力。当前仅支持在以下两类应用中使用：

- **智能体应用**：模型根据自然语言对话自动判断是否调用、调用哪个 MCP 工具及传入参数（如 `maps_route` 或 `web_search`），支持最多同时配置 5 个 MCP 服务 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **工作流应用**：需手动指定 MCP 节点使用的具体工具（如 `maps_weather`），并显式连接输入/输出参数；每个 MCP 节点仅能绑定一个工具 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。

> **注意**：MCP 服务**不能直接接入千问 API 的原始调用链路**。文档 5 明确指出：“MCP 服务能否在调用千问 API 时接入？不可以。阿里云百炼 MCP 服务需集成在**智能体**或**工作流**应用中使用，不能直接在调用千问 API 时接入。” 因此，若需 MCP 能力，必须通过百炼应用框架而非裸 API 调用。

支持的服务类型包括：
- **官方云部署服务**：如 Amap Maps（地理信息）、Firecrawl（网页爬取）、WebSearch（联网搜索）等，开通即用 [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)。
- **自定义服务**：支持三种部署方式：① 使用脚本（npx/uvx）托管开源或自研 MCP Server；② 通过 AI 网关将现有 RESTful API 封装为 MCP；③ 通过 OpenAPI 开发者门户将阿里云产品（如 OSS、ECS）操作发布为 MCP 工具 [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)。

## 关键参数

MCP 配置涉及服务端与客户端两层关键参数：

- **服务端配置（部署时设置）**：
  - `type`：协议类型，必须与接入路径严格匹配——`"sse"` 对应 `/sse` 端点，`"streamableHttp"` 对应 `/mcp` 端点；配置错误将导致 `11200058`（METHOD_NOT_ALLOWED）或 `11200059`（NOT_FOUND）错误 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
  - `command` / `args`：如 `"npx"` + `["@modelcontextprotocol/server-memory"]`，用于启动 Node.js 服务。
  - `url`：远程服务地址，需确保网络可达且 TLS 证书有效（否则触发 `11200048` SSL_ERROR）。
  - `env`：敏感环境变量（如 `AMAP_MAPS_API_KEY`）须通过 KMS 凭据加密，不可明文写入配置。

- **客户端调用参数（运行时生成）**：
  - 工具调用由模型生成 `tool_calls`，包含 `name`（工具名）、`arguments`（JSON 字符串格式参数）。
  - 外部 SDK 调用需显式构造 `headers`（含 `Authorization: Bearer ${DASHSCOPE_API_KEY}`）和 `mcp_url`（如 `https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp`）[外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 使用方式

### 平台内集成（推荐）
1. **开通服务**：前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，选择服务（如 Amap Maps）→ 点击“立即开通”。
2. **配置应用**：
   - *智能体*：创建后在「MCP 服务」模块添加，最多 5 个；模型自动调度。
   - *工作流*：拖入「MCP 节点」→ 选择工具 → 通过「引用」绑定上游节点输出（如 `信息提取/result`）作为输入 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
3. **测试验证**：使用典型 query（如“查询杭州天气”）观察是否触发工具调用及结果流转。

### 外部调用（第三方集成）
- **一键配置**：支持 Cherry Studio、Cursor 等 IDE，通过控制台「外部调用」页点击「一键配置」自动注入 API Key 和服务元数据 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。
- **SDK 编码**：使用 `mcp` Python SDK 连接 `streamablehttp_client`，配合 [OpenAI 兼容接口](../concepts/openai-compatibility.md)实现多轮工具调用循环（详见文档 4 中完整代码示例）。

## 限制和注意事项

- **网络与权限限制**：
  - 自定义 MCP 服务运行于函数计算 FC，**无固定出口 IP**，访问云数据库等资源需配置 IP 白名单或 VPC 打通 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
  - **不支持访问本地资源**（如本地文件、硬件设备），此类服务应在本地部署 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

- **协议与兼容性**：
  - 百炼已全面升级至 **Streamable HTTP 协议**（`/mcp` 端点），旧版 SSE（`/sse`）用户需重新开通以升级 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。
  - 自定义服务若使用 `npx/uvx` 部署，**版本更新后需手动重新部署**，不会自动同步 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

- **计费与限流**：
  - 云部署服务（如 WebSearch）有免费额度（2000 次/月），超量后按 29 元/千次计费；限流 15 QPS，主账号与 RAM 子账号共享 [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)。
  - 自定义服务分「基础模式」（按调用时长计费，0.000156 元/秒）和「极速模式」（另加部署费 0.000036 元/秒），冷启动延迟敏感场景建议启用极速模式 [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)。

- **调试要点**：
  - 模型无法调用 MCP 的首要原因是提示词未明确指令（如未提及工具名或能力），需优化 System Prompt 或更换更强模型 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
  - 遇到连接失败（如 `11200044`）优先执行 `curl <服务地址>` 测试连通性，并检查下游服务日志 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)


