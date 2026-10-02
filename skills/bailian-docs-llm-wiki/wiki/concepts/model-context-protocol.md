# 模型上下文协议（MCP）

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化、安全、可扩展的工具接入协议，用于在大语言模型与外部能力（如地理服务、联网搜索、数据库、云产品 OpenAPI 等）之间建立统一通信通道。它基于开源 MCP 标准（modelcontextprotocol.io）实现，并升级为 **Streamable HTTP 协议**（`POST /mcp`），替代旧版 SSE，显著提升集成稳定性与生产就绪度。

## 在百炼平台的不同场景中，这个概念如何使用

MCP 不是独立运行的服务，而是贯穿百炼三大应用形态的**统一工具抽象层**，其使用方式因场景而异：

- **智能体（Agent 2.0）**：  
  MCP 工具作为“自主决策单元”被统一纳入规划链路。开发者在控制台添加最多 5 个 MCP 服务后，模型根据用户意图（如“查北京明天天气”）自动判断是否调用、调用哪个工具、传入哪些参数——全程无需硬编码或显式提示词指令。知识库、RAG 和 MCP 在 Agent 2.0 中共享同一工具调度框架。

- **工作流（Workflow）**：  
  MCP 以**专用工具节点**形式存在，每个节点绑定且仅绑定一个 MCP 服务（如 `web_search` 或 `oss_list_objects`）。需手动配置输入参数（常由前置“参数提取”节点提供）和输出参数映射（如将 `search_results[0].url` 传给后续“网页解析”节点），适用于确定性、多步骤的业务流程。

- **高代码应用（Rich Code）**：  
  开发者通过 `fastmcp.Client` SDK 在 Python 代码中主动调用 MCP 工具，完全掌控调用时机、重试逻辑与错误处理。控制台中配置的 MCP 工具仅用于环境变量注入（如加密后的 `AMAP_MAPS_API_KEY`）和元数据展示，不参与运行时调度。

- **Connector（统一连接器）**：  
  Connector 是 MCP 的企业级封装形态。当您在「Connector」模块授权钉钉、OSS、MySQL 等系统后，平台**自动生成符合 MCP 规范的工具定义**并注册到智能体/工作流中，无需编写任何适配代码。所有 App 连接均以 `connection_id` 为唯一标识，凭证统一管理，Schema 自动同步。

> ✅ 提示：无论哪种场景，MCP 工具返回的结果都会作为结构化上下文注入模型输入（增加 [Token](token.md) 消耗），因此建议在提示词中明确约束工具调用频次与结果摘要长度。

## 关键参数和配置

| 参数 | 说明 | 注意事项 |
|------|------|----------|
| `type` | 协议类型标识，**必须为 `"streamableHttp"`**（新版标准）；`"sse"` 已弃用，配置将导致 `11200058` 错误 | 生产环境务必检查服务端点与 `type` 严格匹配 |
| `url` | MCP 服务地址，官方服务由百炼托管（如 `https://mcp.aliyuncs.com/v1/mcp/amap-maps`）；自定义服务需确保公网可达或 VPC 内网互通 | 自定义服务部署地域推荐北京（降低延迟） |
| `name` | 工具名称，将出现在模型 `tools` 列表中，影响模型对能力的理解（如 `weather_query` 比 `tool_123` 更易识别） | 建议语义化命名，避免特殊字符 |
| `headers` | 认证头，**必须包含 `DASHSCOPE_API_KEY`**；部分服务需额外头（如 `AMAP_MAPS_API_KEY`） | 敏感 Key 必须通过 KMS 加密配置，禁止明文写入 |
| `command` / `args` / `env` | 仅用于函数计算（FC）部署的自定义服务：指定启动命令（`npx`/`uvx`）、参数及加密环境变量 | 上游包版本更新需手动重新部署，不自动同步 |

> ⚠️ 常见错误码速查：  
> - `11200051`：QPS 超限（如联网搜索限 15 QPS）  
> - `11200058`：`type` 与端点不匹配（如配置 `streamableHttp` 但请求 `/sse`）  
> - `11200059`：`url` 路径错误（如应为 `/mcp` 却写成 `/api/mcp`）

## 面向开发者，简洁实用

- **快速起步**：优先使用官方 MCP 服务（Amap Maps、WebSearch、Firecrawl 等），控制台一键启用，免部署、免鉴权配置。
- **自定义服务**：首选「AI 网关导入」方式封装现有 RESTful API，比从零实现 MCP Server 更快更稳；若需 `stdio` 类型，用 `uvx` 启动（比 `npx` 启动冷启动更快）。
- **调试技巧**：  
  - 在工作流中开启「节点日志」查看原始 MCP 请求/响应；  
  - 使用 `curl -X POST https://<your-mcp-url>/mcp -H "Authorization: Bearer <key>" -d '{"type":"listTools"}'` 手动探测服务可用性；  
  - 智能体调试时，在提示词末尾加一句：“请严格按以下工具列表调用，不要虚构工具名”，可减少幻觉调用。
- **性能优化**：  
  - 避免在单次调用中请求过多数据（如 `web_search` 返回 100 条结果），模型难以消化；建议用 `limit: 3` 控制返回条数；  
  - 对高频低延迟需求（如内部微服务），优先走「Connector + OpenAPI 导入」而非远程 HTTP 调用。

MCP 的本质是**让模型“会用工具”，而不是“懂工具实现”**。你只需关注：工具能做什么（Schema）、何时该用（提示词/工作流编排）、结果怎么用（参数映射）。其余通信、认证、重试、流控，均由百炼平台透明承载。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [overview](../guides/overview.md)
- [llm application](../guides/llm-application.md)
- [application support](../guides/application-support.md)


