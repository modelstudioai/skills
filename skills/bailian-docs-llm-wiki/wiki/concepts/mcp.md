# 模型上下文协议（MCP）

模型上下文协议（MCP，Model Context Protocol）是百炼平台定义的标准化工具集成协议，用于将外部服务（如 API、云资源、自建系统）以统一语义和接口规范注入大模型上下文，使其在推理过程中可被自动识别、参数化调用并融合结果。MCP 不是模型能力本身，而是平台层提供的**工具接入标准与运行时桥接机制**，仅在智能体（Agent）或工作流（Workflow）应用内部生效，不可直接用于千问 API 的裸调用。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）中**：MCP 服务作为“工具”注册后，由大模型根据用户意图自动选择并调用（如“查北京天气”触发 `maps_weather`）。开发者在控制台「应用配置 → MCP 服务」中最多添加 5 个，无需修改提示词或代码逻辑；Sandbox Agent 可通过 `self.tools` 动态注册 MCP 工具。
  
- **工作流（Workflow）中**：MCP 以独立节点形式存在，需手动拖入画布、指定目标工具名（如 `websearch`）及输入参数（常由前置 LLM 节点提取结构化参数），实现确定性、可编排的工具链路。

- **Agent Store 管理中**：MCP 是 `agent store` 的两大核心能力之一（另一为 Skill），支持两类部署形态：
  - **官方 MCP 服务**：开箱即用，如 Amap Maps、WebSearch、Firecrawl，开通即生效；
  - **自定义 MCP 服务**：支持三种接入方式——脚本部署（`npx`/`uvx` 托管至函数计算 FC）、AI 网关导入（封装现有 RESTful API）、阿里云 OpenAPI 导入（操作 OSS/ECS 等资源）。

- **外部系统集成中**：可通过 CLI（`bl mcp call --target maps.weather`）或 SDK（如 `mcp.client.streamable_http`）从第三方客户端（Qoder/Cursor）或自有项目调用已部署的 MCP 服务，实现跨平台能力复用。

> ⚠️ 注意：MCP 服务**不能在调用 `/v1/chat/completions` 千问原生 API 时直接接入**；必须嵌入 Agent 或 Workflow 应用上下文中使用。

## 关键参数和配置

| 参数 | 类型 | 说明 | 必填 |
|------|------|------|------|
| `type` | string | 协议类型，必须与端点严格匹配：`"sse"` 对应 `/sse` 端点（事件流），`"streamableHttp"` 对应 `/mcp` 端点（HTTP JSON-RPC 风格）；不匹配将返回错误码 `11200058`。 | 是 |
| `deployment_mode` | string | 仅云部署服务支持：`"basic"`（按调用时长计费，有冷启动）或 `"ultra"`（常驻在线，额外部署费）。 | 否，默认 `basic` |
| `name` | string | MCP 服务唯一标识符（如 `websearch`），全平台内唯一，用于工具调用路由。 | 是 |
| `description` | string | 工具功能描述，直接影响大模型是否准确识别调用意图，建议包含支持操作、输入约束与典型用例。 | 是 |
| `parameters` | object | OpenAPI 3.0 兼容的 JSON Schema，定义工具所需参数（名称、类型、是否必需、示例等），用于参数提取与校验。 | 是 |

自定义 MCP 服务还需提供符合 [MCP Schema](https://help.aliyun.com/zh/bailian/developer-reference/mcp-schema) 的完整配置 JSON，例如 `npx` 启动需指定 `"command": "npx"` 和有效包名（如 `"package": "@mcp/websearch"`）。

## 面向开发者，简洁实用

- ✅ **快速上手**：优先选用官方 MCP 服务（如 WebSearch），控制台一键开通，5 分钟内完成接入；调试可用 CLI `bl mcp call` 直接测试端点。
- ✅ **自定义开发**：推荐使用 `npx` 方式部署轻量 MCP 服务（如封装内部 HTTP 接口），无需运维服务器；确保服务响应符合 [MCP 规范](https://help.aliyun.com/zh/bailian/developer-reference/mcp-spec)，尤其注意 `type` 与端点路径一致性。
- ✅ **生产注意**：自定义 MCP 无法访问本地资源；函数计算 FC 出口 IP 不固定，访问云数据库需配白名单或 VPC；所有 MCP 返回内容计入输入 Token，影响计费与长度限制。
- ❌ **避免踩坑**：不要尝试将 MCP 配置到千问 API 的 `tools` 字段中——该字段仅接受百炼平台纳管的工具定义，MCP 必须先在 Agent/Workflow 中注册生效。

## 关联主题页

- [agent store](../guides/agent-store.md)
- [agent development](../guides/agent-development.md)
- [get started with agents](../guides/get-started-with-agents.md)
- [agent governance](../guides/agent-governance.md)


