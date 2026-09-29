# 模型上下文协议

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台实现大语言模型与外部工具安全、标准化集成的核心通信规范。它定义了一套统一的接口契约，使模型能在推理过程中动态发现、调用并消费外部服务（如搜索、地图、数据库、API 等），而无需硬编码适配逻辑。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体应用（Agent）**：MCP 是智能体调用外部工具的事实标准。开发者在智能体配置中声明 `mcp_servers`，模型将基于对话上下文自主决策是否调用、调用哪个工具及传入何参数。例如添加 Amap Maps 后，用户说“查北京天气”，模型自动触发 `maps_weather` 工具，无需显式指令。单个智能体最多支持 5 个 MCP 服务。

- **工作流应用（Workflow）**：MCP 以独立节点形式接入画布，每个节点绑定一个 MCP 工具（如 `web_search`）。需手动配置输入参数来源（如引用上游节点输出），适合确定性编排场景。常配合前置大模型节点完成自然语言→结构化参数的转换。

- **Connector 数据连接**：百炼 Connector 将钉钉、语雀、OSS、MySQL 等企业系统自动封装为符合 MCP 规范的工具，开箱即用。授权后即生成标准 MCP 工具 ID（如 `dingtalk_docs_abc123`），直接供智能体或工作流调用，免去接口开发与协议适配。

- **Managed Agents 托管运行时**：MCP 服务作为 `tools` 的一部分挂载至 Agent 配置中，与内置工具（`bash`, `web_fetch` 等）统一管理，并支持独立审批策略（如 `always_ask`）。所有 MCP 调用均在隔离沙箱中执行，状态与事件历史可追溯。

- **插件（Plug-in）生态**：官方/三方/自定义插件需发布为 MCP 服务后，方可被智能体应用在图形化界面中添加；工作流中则作为 MCP 节点使用。插件能力（如 `quark_search`）通过 MCP 协议暴露工具元数据（schema）和执行端点，确保模型理解与调用一致性。

> ⚠️ 注意：MCP **不适用于** 直接调用千问 OpenAI 兼容 API（如 `/v1/chat/completions`），仅限百炼平台内智能体、工作流、Managed Agents 等托管应用上下文。

## 关键参数和配置

MCP 服务配置通过 `mcp_servers` 字段声明，核心参数如下：

| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `type` | string | ✅ | 协议类型，决定连接方式与端点路径。必须与服务实际暴露协议严格一致 | `"streamableHttp"`（推荐）、`"sse"`、`"stdio"` |
| `url` | string | ✅（远程） | 远程 MCP 服务 HTTP 地址（POST `/mcp`） | `"https://my-api.example.com/mcp"` |
| `command` | string | ✅（本地） | 本地启动命令（npx/uvx） | `"npx @modelcontextprotocol/server-memory"` |
| `env` | object | ❌ | 环境变量，用于传递敏感凭据（**必须经 KMS 加密**） | `{"AMAP_MAPS_API_KEY": "{{kms:xxx}}"}` |
| `inputSchema` | object | ✅ | 工具输入参数的 JSON Schema，直接影响模型参数生成准确性 | `{"type":"object","properties":{"query":{"type":"string"}}}` |

- **协议端点映射**：`"sse"` → GET `/sse`；`"streamableHttp"` → POST `/mcp`（当前默认，替代旧版 SSE）。
- **错误防护**：`type` 与服务实际协议不匹配将导致 `11200054`（协议错误）或 `11200058`（HTTP 方法不支持）。
- **命名规范**：自动生成的工具 ID（如 Connector 生成）须为小写字母、数字、下划线组合，长度 ≤ 64。

## 面向开发者，简洁实用

- ✅ **快速启用**：官方 MCP 服务（WebSearch、Firecrawl、QuickChart 等）开通即用；Connector 授权后自动注册，无需写代码。
- ✅ **灵活部署**：自定义服务支持三种方式——脚本一键启动（`npx`/`uvx`）、AI 网关封装 RESTful API、OpenAPI 导入阿里云产品能力。
- ✅ **安全合规**：所有敏感凭据必须通过 KMS 加密注入 `env`；自定义服务运行于函数计算 FC，无固定出口 IP，访问云资源需配置 VPC 或白名单。
- ⚠️ **避坑提示**：
  - 不要混用 `type: "sse"` 和 `/mcp` 端点，或 `type: "streamableHttp"` 和 `/sse` 端点；
  - 工作流中每个 MCP 节点只能绑定一个工具，多工具需拆分为多个节点；
  - 旧版数据连接器（pre-Connector）不兼容 MCP，必须迁移；
  - MCP 服务**不支持访问本地文件、硬件或用户设备**，纯云端执行。

如需调试，推荐使用百炼控制台的「MCP 服务测试」功能，或通过 `mcp.client.streamable_http` SDK 在本地验证请求/响应格式。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [overview](../guides/overview.md)
- [managed agents](../guides/managed-agents.md)
- [application call](../api/application-call.md)
- [plug in](../guides/plug-in.md)


