# 模型上下文协议（MCP）

模型上下文协议（Model Context Protocol，简称 MCP）是百炼平台定义的标准化工具接入与编排协议，用于将外部服务（如地图、搜索、天气、数据库等）以统一语义和结构暴露给大模型，使其能在推理过程中动态感知、发现、选择并调用合适工具，从而扩展模型能力边界。MCP 不是单一接口，而是一套涵盖服务注册、元信息描述、工具发现、参数校验、异步调用与结果解析的端到端协议体系。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）开发**：MCP 是 Agent 调用外部工具的核心载体。在 Managed Agent 的 YAML 配置或 Flow Agent 的工具节点中，开发者通过 `mcp_code` 引用已开通的 MCP 服务；模型根据 System Prompt 中的工具描述与用户请求，自主生成符合 MCP Schema 的调用指令，平台自动完成序列化、路由、认证与结果注入。
  
- **工作流（Workflow）编排**：每个 MCP 节点绑定一个具体 MCP 服务及其工具（如 `amap/weather`），需手动配置输入参数映射（如将上一节点输出的 `city_name` 映射为 `location` 字段）。MCP 节点执行失败时，错误信息（含 `data.isError: true` 及原始响应）会透传至下游，支持条件分支判断。

- **外部集成与 CLI/Sdk 调用**：通过百炼 MCP SDK（兼容 OpenAI Tools API）、CLI 工具（如 `bl mcp call --target amap.weather`）或第三方客户端（Qoder/Cursor），可绕过智能体直接调用 MCP 工具，适用于调试、自动化脚本或嵌入已有系统。

- **自定义能力扩展**：开发者可创建自定义 MCP，支持四种接入类型：
  - `STDIO`：本地进程（如 `npx @bailian/mcp-server`），适合轻量 Node.js/Python 工具；
  - `HTTP`：标准 RESTful 接口，要求返回符合 MCP Tool Schema 的 JSON；
  - `SSE`：服务端事件流，适用于长时任务（如爬取、渲染）的进度推送；
  - `OPENAPI`：自动解析 OpenAPI 3.0 文档，一键生成工具列表与调用逻辑。

> ⚠️ 注意：MCP **不可直接接入千问原生 API（如 `/v1/chat/completions`）调用链**；仅限在智能体应用、工作流应用中使用。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `mcp_type` | string | 是 | 接入类型，取值为 `stdio` / `http` / `sse` / `openapi`；必须与后端服务实际协议严格一致，否则触发 `11200058` 错误。 |
| `mcp_config` | object | 是 | 协议配置对象，结构因 `mcp_type` 而异：<br>• `http`/`sse`: 含 `url`（不含凭据、`#` 或 `\`）、`headers`（禁止 CR/LF）；<br>• `stdio`: 含 `command`（如 `npx`）、`args`（仅支持公共 npm/PyPI 包）；<br>• `openapi`: 含 `spec_url`（OpenAPI JSON/YAML 地址）或内联 `spec_content`。 |
| `server_type` | string | 是（API 创建时） | 后端部署形态，取值 `STDIO`/`HTTP`/`SSE`/`OPENAPI`，与 `mcp_type` 语义对齐但命名风格不同（全大写）。 |
| `type`（前端/CLI） | string | 是 | 前端 UI 或 CLI 中使用的协议标识，取值 `stdio`/`sse`/`streamableHttp`；注意 `streamableHttp` 对应后端 `HTTP` 类型，且端点路径必须为 `/mcp`。 |

- **敏感字段处理**：`mcp_config.headers`、`mcp_config.env` 等字段可能包含 API Key、Token 等密钥，**严禁明文填写**。生产环境必须使用 KMS 凭据加密，并在日志、监控、前端响应中主动过滤该字段。
- **状态管理**：自定义 MCP 修改配置前需先调用 `/disable`；官方 MCP 仅支持 `/activate`/`/deactivate`，无删除接口。
- **工具调用判据**：响应体中 `success: true` 仅表示 MCP API 调用成功；**必须检查 `data.isError` 字段（布尔值）及 `data.error_msg` 才能确认工具执行是否成功**。

## 面向开发者，简洁实用

- ✅ **快速上手**：从控制台「Agent Store」→「MCP 服务」开通高德地图、WebSearch 等官方服务，无需配置即可在智能体中调用。
- ✅ **调试技巧**：使用 `GET /{mcpCode}/tools` 查看工具列表及完整 Schema；用 `POST /{mcpCode}/tools/call` 手动构造请求测试；所有响应头含 `X-Request-Id`，用于问题定位。
- ✅ **安全红线**：`mcp_config.url` 和 `headers` 中禁止硬编码密钥；本地开发时用 `.env` + KMS 加密；线上环境禁用 `stdio` 的 `command` 明文命令。
- ✅ **排障重点**：若工具未被调用，检查 System Prompt 是否清晰描述工具名称与能力；若调用失败，优先查看 `data.isError` 和 `activate_fail_reason`（激活失败时）。
- ❌ **避坑提示**：MCP 服务运行在函数计算 FC，**无法访问本地文件、数据库或内网资源**；需访问云服务时，务必配置 FC 公网出口 IP 白名单或 VPC 打通。

## 关联主题页

- [overview](../api/overview.md)
- [overview 1e06e5e20b81f10d](../api/overview-1e06e5e20b81f10d.md)
- [agent store](../guides/agent-store.md)
- [agent development](../guides/agent-development.md)
- [agent governance](../guides/agent-governance.md)
- [application support](../guides/application-support.md)


