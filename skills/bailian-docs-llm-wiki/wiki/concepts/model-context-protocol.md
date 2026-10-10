# 模型上下文协议（MCP）

模型上下文协议（Model Context Protocol, MCP）是百炼平台统一的**工具接入与能力编排标准协议**，用于将外部服务（如地图、搜索、数据库、SaaS 应用等）以声明式、安全可控的方式注入大模型推理上下文。它不是模型本身的能力，而是平台提供的标准化“工具网关”——屏蔽底层接口差异，统一描述、发现、调用和鉴权逻辑，使模型能在自然语言驱动下自主选择并执行真实世界操作。

## 在百炼平台的不同场景中，这个概念如何使用

MCP 是百炼平台工具生态的底层协议层，贯穿三大应用范式，但**调用入口和控制粒度不同**：

- **智能体（Agent）**：在 Agent 2.0 中，MCP 服务与知识库、内置工具（`bash`/`write`）同等视为“可规划工具”。开启后，模型根据用户请求自动决策是否调用、调用哪个服务、传入哪些参数，全程无需人工编排。最多支持 5 个并发 MCP 调用。
- **工作流（Workflow）**：通过可视化 `MCP 节点` 显式接入。需手动选择已开通的服务（如 `amap-maps.maps_route`），绑定上游节点输出作为输入参数，并指定结果字段映射到下游。适合确定性流程与多步骤串联。
- **Managed Agents（托管智能体）**：在 `mcp_servers` 配置项中声明 MCP 服务地址（支持官方市场服务或自定义 HTTP 网关），并在 `tools` 列表中显式启用。工具调用发生在隔离沙箱内，结果可写入文件系统或触发后续 `tool_call_output` 事件。
- **Connector（数据连接器）**：所有已创建的业务系统连接（OSS、MySQL、语雀、钉钉等）均被自动封装为符合 MCP 规范的工具集，并聚合暴露在统一 MCP 地址下（`https://${workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/connector/mcp`）。客户端只需配置一次即可发现并调用全部连接器工具。
- **高代码应用（Rich Code）**：开发者可在 Python 项目中直接集成 `mcp.client.streamable_http` 客户端，连接任意 MCP 服务 URL（包括 Connector 或自定义部署服务），实现细粒度工具调用与结果处理。

> ⚠️ 注意：MCP **不可直接用于调用千问 OpenAI 兼容 API（如 `/v1/chat/completions`）**。它仅在百炼平台内建应用（智能体/工作流/Managed Agents）或通过百炼 SDK/CLI/Connector 客户端调用时生效，不能作为中间件注入第三方 LLM 请求链。

## 关键参数和配置

| 参数 | 说明 | 典型值/约束 | 使用位置 |
|------|------|-------------|----------|
| `DASHSCOPE_API_KEY` | 百炼平台通用鉴权凭证，所有 MCP 调用必需 | `sk-xxx`（需在控制台生成） | 所有场景（HTTP Header `Authorization: Bearer ${key}`） |
| `mcp_url` | MCP 服务访问地址 | `https://dashscope.aliyuncs.com/api/v1/mcps/amap-maps/mcp`（官方服务）<br>`https://${workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/connector/mcp`（Connector） | 外部调用、Managed Agents、高代码应用 |
| `type`（自定义服务） | 自定义 MCP 服务的通信协议类型 | `"streamableHttp"`（推荐）、`"sse"`（旧版）、`"stdio"`（本地调试） | 自定义 MCP 部署配置（`mcp.json` 或 CLI） |
| `command` & `args` | npx/uvx 启动命令（仅自定义服务） | `"npx"`, `["@modelcontextprotocol/server-memory"]` | 自定义 MCP 服务部署脚本 |
| `workspaceId` | Connector 专属业务空间标识 | `llm-xxxxxxxxxxxx`（控制台获取） | Connector 场景必填，用于路由和权限隔离 |

## 面向开发者，简洁实用

- ✅ **快速上手**：开通 One Key 服务（如 WebSearch）后，直接在智能体编辑页 → “MCP 服务” → 添加即可生效；Connector 连接后，工具自动就绪。
- ✅ **调试优先**：用 CLI 快速验证：`bl mcp list` 查服务列表，`bl mcp call --target web-search.search --query "杭州天气"` 直接调用。
- ✅ **安全第一**：敏感凭证（如 `AMAP_MAPS_API_KEY`）必须通过 KMS 加密或 Vault 注入，禁止明文写入代码或配置文件。
- ✅ **性能注意**：MCP 返回内容会作为上下文输入模型，显著增加 token 消耗；建议对长响应做服务端截断或摘要。
- ✅ **协议选型**：对外集成首选 `streamableHttp`（基于 HTTP/2 流式响应，稳定性优于 SSE）；避免使用已淘汰的 `stdio` 或 `sse`（旧版需重新开通才能升级）。
- ✅ **错误处理**：MCP 调用失败不会触发模型重试，需在应用层捕获 `4xx/5xx` 响应并降级（如返回“暂无法获取信息”）。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [overview](../guides/overview.md)
- [plug in](../guides/plug-in.md)
- [llm application](../guides/llm-application.md)
- [managed agents](../guides/managed-agents.md)


