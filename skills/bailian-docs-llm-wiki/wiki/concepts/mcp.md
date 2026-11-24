# 模型上下文协议（MCP）

模型上下文协议（Model Context Protocol，简称 MCP）是百炼平台统一抽象和接入外部工具服务的核心协议标准。它将天气、地图、数据库、知识库等异构能力封装为语义清晰、结构一致、可被大模型自动发现与调用的标准化工具，使智能体无需硬编码即可动态扩展上下文感知与执行能力。

## 在百炼平台的不同场景中，这个概念如何使用

MCP 不是独立运行的服务，而是贯穿智能体全生命周期的**能力接入层协议**，在以下关键场景中发挥核心作用：

- **智能体（Managed / Flow Agent）中自动调用**：当用户提问（如“杭州今天气温多少？”），模型基于自然语言理解自动匹配已启用的 `weather` MCP 工具，并通过 `/tools/call` 接口发起调用；结果返回后由模型整合生成最终回复。最多可同时绑定 5 个 MCP 服务。
  
- **工作流（Flow Agent）中显式编排**：每个 MCP 节点严格绑定一个具体工具（如 `amap-maps.maps_weather`），需前置节点提取参数（城市名）、后置节点解析结果，实现确定性、可调试的工具链路。

- **CLI 与 SDK 外部直调**：开发者可通过 `bl mcp call --target weather.get_current --city "杭州"` 命令或 Python SDK 直接调用 MCP 工具，用于测试、集成或构建轻量级自动化脚本。

- **Agent Store 统一管理**：所有 MCP 服务（无论官方 One Key 或自定义）均在「Agent Store」集中展示、开通、配置与启停，形成可复用、可共享的能力市场。

> ⚠️ 注意：MCP **不能**在直接调用千问基础 API（如 `/v1/chat/completions`）时使用；仅限集成于百炼平台内的智能体应用或工作流应用中生效。

## 关键参数和配置

| 类别 | 参数/字段 | 说明 | 约束与示例 |
|--------|-----------|------|------------|
| **协议类型（必填）** | `mcp_type` | 决定服务部署与通信方式 | 支持 `STDIO`（npx/uvx 启动）、`HTTP`（普通 REST）、`SSE`（Server-Sent Events）、`OPENAPI`（OpenAPI 3.x 规范自动转换） |
| **服务标识** | `server_name`、`mcpCode` | 全局唯一编码，用于 API 路径与工具调用 | `mcpCode` 由平台生成，不可修改；`server_name` 可更新（不触发重部署） |
| **配置对象** | `mcp_config` | 根据 `mcp_type` 动态结构化 | • `HTTP`: 必含 `url`，可选 `headers`<br>• `OPENAPI`: 必含 `api_list`（工具列表 JSON Schema）<br>• `STDIO`: 必含 `command`（如 `"npx"`）与 `args`（如 `["@modelcontextprotocol/server-memory"]`） |
| **认证与安全** | `Authorization: Bearer <key>` | 所有 MCP 接口均需百炼 API Key 鉴权 | 使用 `DASHSCOPE_API_KEY`，通过请求头传递；敏感字段（如 `mcp_config.headers`）原样返回，禁止日志留存 |
| **工具推荐** | `topN`（查询参数） | 用于 `/tools/recommend` 接口，指定返回推荐工具数量 | 默认 `3`，最大 `10` |
| **分页控制** | `pageNo`, `pageSize` | 适用于 `/servers/list` 等列表接口 | `pageNo ≥ 1`，`pageSize ∈ [1, 100]`，且 `pageNo × pageSize ≤ 10000` |

## 面向开发者，简洁实用

- ✅ **快速上手**：One Key MCP（如联网搜索、Amap Maps）开箱即用，控制台点击开通 → 智能体中勾选 → 模型自动调用。
- ✅ **自定义灵活**：用 `npx @modelcontextprotocol/server-*` 一行启动本地 MCP 服务，或通过 AI 网关封装任意 HTTP API，5 分钟完成接入。
- ✅ **调试可靠**：所有工具调用返回统一结构，务必检查 `data.isError` 字段（即使 HTTP 状态码为 200，也可能执行失败）。
- ✅ **安全可控**：`mcp_config` 中的密钥类字段（如 `headers.Authorization`）不会被平台脱敏，**请确保调用环境可信，禁止打印/落库完整响应**。
- ✅ **状态明确**：区分 `OFFICIAL`（平台托管，仅支持 `activate/deactivate`）与 `CUSTOMER`（用户自建，支持 `enable/disable/update/delete`）；修改配置前必须先 `disable`，否则返回 `400 OperationNotSupported`。

> 📌 提示：开发自定义 MCP 时，优先选用 `SSE` 或 `OPENAPI` 类型——它们无需函数计算部署、无出口 IP 限制，更适合访问私有内网服务。

## 关联主题页

- [overview](../api/overview.md)
- [overview 1e06e5e20b81f10d](../api/overview-1e06e5e20b81f10d.md)
- [agent store](../guides/agent-store.md)
- [capabilities](../guides/capabilities.md)
- [agent development](../guides/agent-development.md)


