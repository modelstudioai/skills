# 模型上下文协议

模型上下文协议（Model Context Protocol，简称 MCP）是百炼平台定义的标准化接口规范，用于实现大语言模型与外部工具服务之间的结构化、可发现、可调用的双向交互。它抽象了工具注册、元信息描述、参数校验与执行反馈等关键环节，使智能体无需硬编码适配即可动态感知并调用各类能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Managed Agent）与工作流（Flow Agent）集成**：MCP 服务作为“插件式能力”被添加至智能体或工作流配置中，模型在推理过程中根据上下文自动触发对应工具（如 `maps_weather`），参数由模型生成并经平台校验后透传，结果再注入后续上下文。
- **Agent Store 统一能力中心**：MCP 是 Agent Store 的核心协议标准，所有官方 MCP（如高德地图、联网搜索）、One Key MCP（开箱即用）及自定义 MCP 均需符合 MCP 规范才能被发现、列表展示和安全调用。
- **外部客户端对接**：开发者可通过兼容 MCP 的 SDK（如 `mcp.client.streamable_http`）或支持 OpenAI 工具调用格式的 IDE 插件（Qoder/Cursor），以标准 HTTP 或 SSE 协议直连 MCP 服务端点（如 `/mcp` 或 `/sse`），实现跨平台工具复用。
- **自定义 MCP 开发与部署**：开发者可基于 `STDIO`（函数计算运行 CLI）、`HTTP`、`SSE` 或 `OPENAPI` 四种接入模式实现 MCP Server，只需暴露符合 MCP Schema 的工具列表与调用接口，平台即自动完成注册、发现与生命周期管理。

## 关键参数和配置

- **`mcp_type`**（必填）：标识接入协议类型，取值为 `stdio`、`http`、`sse` 或 `openapi`。
- **`mcp_config`**（结构化对象，按类型填写）：
  - `http`：需提供 `url`（服务地址）、`headers`（含鉴权信息，如 `Authorization: Bearer xxx`）、`timeout_ms`（默认 10000）；
  - `openapi`：需提供 `api_list`（工具定义数组）及每个工具的 `input_params` JSON Schema；
  - `stdio`：需指定 `command`（如 `npx`）、`args`（如 `["@modelcontextprotocol/server-memory"]`）、`env`（环境变量）；
  - `sse`：需提供 `url` 及 `event_prefix`（可选，默认 `mcp.`）。
- **`deploymentMode`**（自定义 MCP）：控制性能与计费模式，取值 `basic`（基础）或 `pro`（极速），影响响应延迟与单价。
- **工具调用参数**：统一通过 `tool_params` 字段传递，其结构必须严格匹配该工具在 `GET /tools` 接口中返回的 `input_schema` 定义。

## 面向开发者，简洁实用

- ✅ **快速验证**：使用 CLI 命令 `bl mcp tools --server <code>` 查看工具列表及其输入 Schema；用 `bl mcp call --target <server>.<tool> --params '{"key":"value"}'` 直接调试。
- ✅ **安全第一**：敏感凭据（如 API Key、Bearer Token）仅允许配置在 `mcp_config.headers` 或 `env` 中，**严禁写入代码或日志**；响应体中的 `headers` 字段可能含敏感信息，需脱敏处理。
- ✅ **协议选型建议**：
  - 优先选用 `streamable_http`（即 `http` 类型 + `/mcp` endpoint），兼容性好、调试直观、支持超时与重试；
  - `stdio` 适合轻量脚本类工具（如本地 memory server），部署简单但无弹性伸缩；
  - `sse` 仅用于需长连接推送的特殊场景，客户端需主动维护连接。
- ⚠️ **注意限制**：MCP 服务运行于函数计算，**无固定出口 IP**，访问公网资源需配置白名单；**不支持访问本地网络、硬件设备或未打通 VPC 的私有数据库**。

## 关联主题页

- [overview](../api/overview.md)
- [agent store](../guides/agent-store.md)
- [agent billing](../guides/agent-billing.md)
- [managed agents api](../api/managed-agents-api.md)
- [flow agent api](../api/flow-agent-api.md)


