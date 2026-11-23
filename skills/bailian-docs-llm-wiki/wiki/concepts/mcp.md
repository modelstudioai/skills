# 模型调用协议

模型调用协议（Model Calling Protocol，简称 MCP）是百炼平台定义的一套标准化工具接入规范，用于将任意后端服务（如 API、函数、本地脚本）封装为大模型可识别、可发现、可安全调用的结构化能力单元。它不改变模型本身，而是构建在模型推理层之上的统一工具交互契约，使智能体能以声明式方式调用外部能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体与工作流编排**：在 Managed Agent 或 Flow Agent 中添加 MCP 服务后，模型可在生成过程中自动触发 `tool_calls`，平台依据协议解析参数、转发请求、处理响应并注入上下文。例如用户问“北京今天天气如何”，模型自动调用 `amap-maps.weather` 工具，无需硬编码集成。
- **CLI 与 SDK 直接调用**：开发者可通过 `bl mcp call --target amap-maps.weather` 命令或 Python SDK 的 `MCPClient` 类，绕过智能体直接调用已注册的 MCP 服务，适用于自动化脚本、测试或轻量级集成。
- **自定义工具接入**：开发者可基于四种部署类型实现符合 MCP 协议的服务：
  - `STDIO`：通过函数计算（FC）运行 CLI 工具（如 `npx`/`uvx`），标准输入输出通信；
  - `HTTP`：提供兼容 OpenAPI 规范的 REST 接口，支持同步响应；
  - `SSE`：提供 Server-Sent Events 流式接口，适用于长时任务或进度反馈；
  - `OPENAPI`：复用现有 OpenAPI 3.0 文档，平台自动解析 schema 并生成调用逻辑。
- **Agent Store 能力中心**：所有官方 MCP（如高德地图、Firecrawl、WebSearch）和用户自建 MCP 均在 Agent Store 统一注册、管理、启停与计费，形成即插即用的能力市场。

> ⚠️ 注意：MCP 服务**仅限智能体/工作流内部调用或通过 MCP 专用 API（`/api/v1/mcp/servers/...`）显式调用**，不可在纯 `qwen-*` 模型 API（如 `/v1/chat/completions`）中直接使用。

## 关键参数和配置

- **核心标识**：
  - `mcp_code`：MCP 唯一编码（如 `amap-maps`），创建后生成，用于所有 API 路径（如 `/api/v1/mcp/servers/{mcpCode}`）和 CLI 参数（`--target {mcpCode}.tool_name`）。
  - `tool_name`：工具名（如 `weather`, `geocode`），必须与 MCP 服务返回的 `tools` 列表中定义一致，调用时必填。

- **协议配置字段（`mcp_config`）**：
  - `mcp_type`：必需，取值为 `STDIO` / `HTTP` / `SSE` / `OPENAPI`，决定后续配置结构。
  - `endpoint`（HTTP/SSE/OPENAPI）：服务地址，支持 HTTPS URL；SSE 必须以 `/sse` 结尾。
  - `command`（STDIO）：执行命令（如 `npx @amap/maps-cli weather`），支持环境变量占位符（如 `$AMAP_API_KEY`）。
  - `headers`：请求头（如 `{"Authorization": "Bearer ${apiKey}"}`），敏感字段在响应中自动脱敏。
  - `inputSchema`：JSON Schema 定义工具输入参数结构，直接影响模型参数生成准确性。

- **调用控制参数**：
  - `timeout_ms`：单次调用超时毫秒数（默认 30000，最大 60000）。
  - `max_retries`：失败重试次数（默认 0，最大 3）。
  - `enable_streaming`（SSE/HTTP）：是否启用流式响应（需服务端支持）。

- **认证与安全**：
  - 所有 MCP 调用共享 `DASHSCOPE_API_KEY` 认证，无需为每个服务单独申请密钥。
  - 敏感凭据（如第三方 API Key）**必须通过 KMS 加密后注入 `mcp_config.headers` 或环境变量**，严禁明文配置。

## 面向开发者，简洁实用

- ✅ **快速验证**：用 `bl mcp list` 查看可用服务，`bl mcp tools --target amap-maps` 查看工具列表，`bl mcp call --target amap-maps.weather --params '{"city":"北京"}'` 直接调试。
- ✅ **自建第一步**：选择 `STDIO` 类型 → 编写一个接收 JSON 输入、输出 JSON 响应的 CLI 脚本 → 用 `bl mcp create --type STDIO --command "node weather.js"` 注册。
- ✅ **调试关键**：关注响应中的 `isError` 字段（`true` 表示工具执行失败，非网络错误）和 `x-request-id` 头（用于日志追踪）。
- ❌ **避免踩坑**：
  - 不要依赖 `server_status_text` 字符串做状态判断，应检查 `server_status` 枚举值（如 `ACTIVE`, `INACTIVE`）；
  - 自定义 MCP 更新代码后，必须重新部署（`bl mcp update` + `bl mcp enable`），不会自动热更新；
  - `inputSchema` 中缺失 `required` 字段或类型错误，会导致模型传参失败，调用前务必用 `bl mcp tools` 校验 schema。

## 关联主题页

- [overview](../api/overview.md)
- [overview 1e06e5e20b81f10d](../api/overview-1e06e5e20b81f10d.md)
- [agent store](../guides/agent-store.md)
- [capabilities](../guides/capabilities.md)
- [agent development](../guides/agent-development.md)


