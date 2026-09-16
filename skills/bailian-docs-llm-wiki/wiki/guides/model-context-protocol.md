# model context protocol

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化接口协议，用于在大模型与外部工具（如地图、搜索、数据库等）之间建立安全、可扩展的信息通道。它屏蔽了工具接入的底层差异，使开发者无需为每个第三方服务单独开发适配层，即可在智能体或工作流中声明式调用能力。该协议基于 Anthropic 提出的开源标准实现，当前百炼平台已全面支持 Streamable HTTP 协议（替代旧版 SSE），并提供云部署、自定义部署和外部集成三种使用路径。

## 支持的模型/功能

MCP 服务本身不绑定特定大模型，但其调用行为依赖于百炼平台内嵌的推理模型能力。目前所有支持工具调用（function calling）的百炼内置模型均可驱动 MCP，包括 `qwen-max`、`qwen-plus` 及 `qwen-turbo` 等。实际可用性取决于应用类型：

- **智能体应用**：自动识别用户意图并动态选择已配置的 MCP 服务（最多同时启用 5 个），支持多轮工具调用与结果融合，例如路径规划、逻辑推理、多源数据聚合（如“用高德查天气 + QuickChart 绘图”）[官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **工作流应用**：需显式配置 MCP 节点，并手动指定所用工具（如 `maps_weather`）、输入参数映射与输出解析逻辑，适用于确定性、强流程控制的场景 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **外部调用**：通过 MCP SDK 或兼容 OpenAI 接口的客户端（如 Cherry Studio、Cursor）集成，支持 Streamable HTTP 协议直连，适用于第三方 IDE 或自有系统 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

> **注意**：文档 4 明确指出 MCP 服务“不能直接在调用千问 API 时接入”，而文档 5 的 FAQ 第 3 条却表述为“MCP 服务能否在调用千问 API 时接入？不可以”。二者一致，但需强调：MCP 是百炼平台级能力，**不开放给纯 API 调用链路**；若需类似能力，必须通过百炼智能体/工作流封装后暴露为 API。

## 关键参数

MCP 服务配置与调用涉及以下核心参数，分属不同层级：

| 参数类别 | 参数名 | 说明 | 示例值 |
|----------|--------|------|--------|
| **服务注册** | `service_name` | 服务唯一标识符，仅用于平台内区分，不影响模型调用逻辑 | `"long_term_memory"` |
| | `type` | 协议传输类型，决定端点路径与请求方式 | `"stdio"`（本地）、`"sse"`（`/sse`）、`"streamableHttp"`（`/mcp`） |
| | `url` / `command`+`args` | 远程服务地址 或 本地启动命令 | `"https://your-server/mcp"` / `"npx @modelcontextprotocol/server-memory"` |
| **工具调用** | `tool.name` | 工具在 MCP Server 中注册的名称，模型生成时必须严格匹配 | `"maps_weather"` |
| | `tool.inputSchema` | JSON Schema 描述输入参数结构，影响模型参数生成准确性 | `{"type": "object", "properties": {"city": {"type": "string"}}}` |
| **安全与认证** | `env` | 启动时注入的环境变量（如 API Key），敏感值建议通过 KMS 凭据加密 | `{"AMAP_MAPS_API_KEY": "xxx"}` |
| | `headers` | 外部调用时需携带的认证头 | `{"Authorization": "Bearer ${DASHSCOPE_API_KEY}"}` |

> **注意**：文档 3 的配置模板中 `type` 字段缺失（如 `"memory": { "command": ... }` 未声明 `type`），但文档 5 的错误码 11200058/11200059 明确要求 `type` 必须与端点路径严格匹配（`"sse"` → `/sse`，`"streamableHttp"` → `/mcp`）。实际部署时务必补全 `type`，否则将触发协议错误。

## 使用方式

### 1. 云部署（开箱即用）
- 前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，选择官方服务（如 Amap Maps、WebSearch），点击“立即开通”。
- 开通后，在智能体/工作流编辑器中直接添加，无需配置密钥（试用版）或填入 KMS 加密凭据（商业化版）[模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)。

### 2. 自定义部署（三类方式）
- **脚本部署**：适用于开源或自研 MCP Server（Node.js/Python）。上传 `npx`/`uvx` 启动配置至函数计算（FC），支持基础模式（按调用计费）与极速模式（常驻+调用双计费）[自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)。
- **AI 网关导入**：将现有 RESTful API 封装为 MCP 工具，通过 AI 网关统一管理鉴权与限流。
- **OpenAPI 导入**：一键将阿里云产品（OSS/ECS）的 OpenAPI 发布为 MCP 工具，需配置 RAM 角色与权限策略。

### 3. 外部集成
- **IDE 集成**：在 Cherry Studio 或 Cursor 中，通过“一键配置”自动注入 MCP Server 配置（含 URL、Token、类型）。
- **SDK 编程**：使用 `mcp` Python SDK 连接 Streamable HTTP 端点，调用 `list_tools()` 获取工具列表，并与 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)协同完成多轮工具调用循环 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 限制和注意事项

- **网络与资源限制**：
  - 所有云部署 MCP 服务运行于函数计算 FC，**无固定出口 IP**，访问云数据库等需配置 IP 白名单或 VPC 打通 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
  - **不支持访问本地资源**（文件、硬件、本地数据库），此类服务需本地部署 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
  - 联网搜索等付费服务有明确限流（如 15 QPS）和额度（2000 次/月），超限后停止服务 [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)。

- **协议与兼容性**：
  - 百炼已全面升级至 **Streamable HTTP 协议**（`/mcp` 端点），旧版 SSE（`/sse`）服务需重新开通以获得支持 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。
  - 自定义部署时，`npx`/`uvx` 方式部署的服务**版本更新后不会自动同步**，必须手动重新部署 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

- **调试与排错**：
  - 工具调用失败常见原因包括：提示词未明确指令、模型能力不足、参数 schema 不匹配。优先检查 `tool.name` 是否与 `list_tools()` 返回值完全一致。
  - 遇到连接类错误（如 `MCP_CONNECTION_REFUSED`, `MCP_SSL_ERROR`），应使用 `curl` 直连服务端点验证连通性与证书有效性 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)


