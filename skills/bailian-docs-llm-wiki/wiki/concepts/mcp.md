# 模型上下文协议

模型上下文协议（Model Context Protocol，简称 MCP）是百炼平台用于标准化模型与外部工具/服务之间结构化交互的开放协议。它定义了一套统一的通信契约（包括能力发现、参数协商、调用执行与结果返回），使大模型无需硬编码即可理解、选择并安全调用符合协议的外部能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **Agent 应用中**：MCP 服务作为“可插拔工具”集成至智能体，模型根据用户意图自动判断是否调用、调用哪个服务及传入哪些参数（如用户问“北京今天天气如何”，模型自动触发 `weather` MCP 服务）。单个 Agent 最多可挂载 5 个 MCP 服务。
- **工作流（Workflow）中**：MCP 以显式节点形式存在，开发者需手动指定服务 ID（如 `amap_maps`）和输入参数（支持引用上游节点输出），实现确定性、可编排的工具链路。
- **Omni Realtime API 中**：通过 `tools` 字段声明 MCP 工具（`type: "mcp"`），与 Function Calling 并列作为工具调用方式；但二者不可与 `enable_search: true` 同时启用。
- **外部集成中**：支持通过 [MCP SDK](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md) 编程接入 Cherry Studio、Cursor 等 IDE 工具，或自建客户端对接百炼托管的 MCP 服务。
- **不适用场景**：MCP 服务**无法在直接调用千问基础 API（如 `dashscope.ChatCompletion.create`）时使用**，也不支持本地部署的 MCP Server 接入百炼云端环境。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `type` | string | 是 | MCP 服务类型，必须与接入路径严格匹配：<br>• `sse` → 对应 `/sse` 端点（推荐用于长连接、低延迟场景）<br>• `streamableHttp` → 对应 `/mcp` 端点（兼容 RESTful 风格）<br>• `stdio` → 仅限本地调试，不适用于百炼托管<br>配置错误将导致错误码 `11200058`。 |
| `deploymentMode` | string | 否 | 部署模式：<br>• `basic`（基础模式）：按调用时长计费（0.000156 元/秒），无部署费；<br>• `ultra`（极速模式）：额外收取部署费（0.000036 元/秒），适合高并发、亚秒级响应要求场景。 |
| `tool_whitelist`（治理层） | list[string] | 否 | 在 Agent 治理配置中，可限定该 Agent 实例仅允许调用指定 MCP 服务 ID（如 `["websearch", "firecrawl"]`），实现细粒度权限控制。 |

> ⚠️ 注意：  
> - 百炼托管的 MCP 服务运行于函数计算（FC），**无固定出口公网 IP**，访问云数据库等资源需配置 FC 白名单或 VPC 打通；  
> - 自定义 MCP Server 版本更新后**不会自动同步**，需手动重新部署；  
> - 私有 npm 仓库的 MCP 包暂不支持直接部署，建议发布至公共仓库或改用 SSE 连接方式。

## 面向开发者，简洁实用

- ✅ **快速上手**：优先选用官方预置 MCP 服务（如 `WebSearch`、`Amap Maps`），开通即用，无需开发。  
- ✅ **自定义接入三选一**：  
  &nbsp;&nbsp;① 脚本部署：`npx mcp-server-xxx` 或 `uvx mcp-server-xxx`（适合 Node.js/Python 工具）；  
  &nbsp;&nbsp;② AI 网关导入：将已有 RESTful API 封装为 MCP 标准接口；  
  &nbsp;&nbsp;③ OpenAPI 导入：一键拉取阿里云 OpenAPI，自动生成 MCP 服务（适合云资源操作）。  
- ✅ **调试技巧**：使用 `sse` 类型时，务必确保服务端返回 `Content-Type: text/event-stream` 和正确 `event:` 格式；可通过 `curl -N http://your-mcp-server/sse` 验证流式响应。  
- ❌ **避坑提醒**：不要尝试在 `dashscope.ChatCompletion.create()` 中传入 MCP 工具——该调用路径完全绕过百炼的 MCP 调度引擎，协议不生效。

## 关联主题页

- [agent store](../guides/agent-store.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [security api guide](../api/security-api-guide.md)
- [application support](../guides/application-support.md)
- [agent governance](../guides/agent-governance.md)


