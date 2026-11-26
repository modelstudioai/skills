# 模型上下文协议

模型上下文协议（Model Context Protocol，简称 MCP）是百炼平台定义的标准化服务接入与交互规范，用于将外部能力（如 HTTP API、本地进程、事件流服务等）以结构化、可发现、可编排的方式注入大模型推理上下文，实现工具调用、上下文增强与多步协同的统一抽象。

## 在百炼平台的不同场景中，这个概念如何使用

- **Agent 编排场景**：MCP 是 Agent 2.0 的核心能力载体。开发者通过 `agent.yaml` 中 `tools: [store://<mcp_id>]` 声明 MCP 工具，Agent 运行时自动完成工具发现、参数校验、调用路由与结果结构化解析，无需硬编码集成逻辑。
- **智能体开发场景**：在 Flow Agent 或 Sandbox Agent 中，MCP 作为“外部动作节点”被调用；其工具列表（`GET /{mcpCode}/tools`）和推荐接口（`POST /tools/recommend`）支持自然语言驱动的动态工具选择，提升多轮对话中的意图理解与动作泛化能力。
- **能力注册中心（Agent Store）场景**：MCP 作为一类标准能力类型（`type: "mcp"`）注册到 Agent Store，需提供 `endpoint` 和符合 OpenAPI 3.0 或 JSON Schema 的 `schema`，供全平台统一发现、权限管控与可观测性治理。
- **服务管理场景**：MCP 支持四种接入类型（`STDIO`/`HTTP`/`SSE`/`OPENAPI`），开发者可通过 MCP API 全生命周期管理自定义服务（创建、启用、更新、删除），并开通官方 MCP（如高德地图）直接复用。
- **可观测与治理场景**：MCP 调用天然纳入 [agent governance](../guides/agent-governance.md) 的 Trace 链路，支持工具级 QPM、成功率、耗时监控；其调用输入/输出也参与安全策略检测（如敏感数据外泄拦截）与评测集回流（用于轨迹准确性评估）。

## 关键参数和配置

- **协议标识**：每个 MCP 由唯一 `mcp_code` 标识，用于构造所有操作路径（如 `/api/v1/mcp/servers/{mcpCode}/tools/call`）。
- **接入类型配置（`mcp_config`）**：
  - `STDIO`：`command`（启动命令）、`args`（参数数组）、`env`（环境变量映射）；
  - `HTTP` / `SSE`：`url`（HTTPS 地址）、`headers`（下游请求头，**可能含敏感凭据，禁止日志透出**）；
  - `OPENAPI`：`api_list` 数组，每项含 `name`、`path`、`method`、`input_params`（JSON Schema 描述）等字段。
- **工具调用参数**：
  - 请求体必须包含 `tool_name` 和 `tool_input`（按 `inputSchema` 校验）；
  - 响应体固定含 `isError: boolean` 字段（`success: true` 仅表示 HTTP 成功，业务失败需检查此字段）。
- **推荐与发现参数**：
  - `GET /{mcpCode}/tools`：返回全部工具元信息（名称、描述、参数 Schema）；
  - `POST /tools/recommend`：支持 `topN`（默认 3）和 `query`（自然语言描述）参数，语义匹配最适配工具。

> ⚠️ 注意：`mcp_config.headers` 和工具调用响应中的敏感字段，必须在可信环境处理，严禁写入日志、前端或不可信存储。

## 关联主题页

- [overview](../api/overview.md)
- [overview 1e06e5e20b81f10d](../api/overview-1e06e5e20b81f10d.md)
- [agent store](../guides/agent-store.md)
- [agent development](../guides/agent-development.md)
- [agent legacy](../guides/agent-legacy.md)
- [agent governance](../guides/agent-governance.md)


