# model context protocol

model context protocol（MCP）是百炼平台提供的标准化上下文交互协议，用于在大模型应用中安全、可控地接入外部工具与数据源。它定义了模型与外部服务之间结构化通信的接口规范，支持同步/异步调用、参数校验、权限控制和错误回传。开发者可通过官方 MCP 服务或自定义 MCP 服务快速集成业务能力。

## 支持的模型与功能

MCP 当前支持所有百炼平台托管的推理模型（包括 Qwen 系列、Qwen2 系列及第三方兼容模型），但**不适用于训练任务或微调流程**。核心功能包括：  
- 工具发现（`list_tools`）与元信息获取  
- 上下文感知的工具调用（`invoke`）与结果流式返回  
- 多轮会话状态透传（通过 `session_id` 和 `context` 字段）  
- 安全沙箱执行（仅限官方 MCP 服务）  

> **注意**：[原文标题](../../raw/application-user-guide/model-context-protocol.md) 中提及的“第三方 MCP 服务”需自行保障调用链路 TLS 加密与输入输出校验，该要求在 [原文标题](../../raw/application-user-guide/model-context-protocol.md) 的「外部调用」章节有明确说明，但未在「自定义MCP服务」章节强调，建议以「外部调用」为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `tool_id` | string | 是 | 工具唯一标识，由 MCP 服务注册时分配或自定义命名 |
| `input` | object | 是 | 结构化输入，字段由工具 schema 定义，**不支持任意 JSON Schema，仅支持 OpenAPI 3.0 兼容子集** |
| `session_id` | string | 否 | 用于关联多轮调用，长度 ≤ 64 字符，仅 ASCII 字母/数字/-/_ |
| `context` | object | 否 | 可选上下文对象，最大嵌套深度 3 层，总大小 ≤ 16 KB |

完整参数约束详见 [原文标题](../../raw/application-user-guide/model-context-protocol.md) 的「官方 MCP 服务」文档。

## 使用方式

1. **启用 MCP**：在应用配置中开启 `enable_mcp: true`；  
2. **声明工具**：在 `tools` 列表中指定 `tool_id` 和 `mcp_server_url`（官方服务可省略）；  
3. **触发调用**：模型输出符合 MCP 规范的 `tool_call` 指令后，平台自动路由并注入 `context`；  
4. **处理响应**：MCP 服务须返回标准格式 `{ "result": ..., "error": null }` 或 `{ "error": { "code": "...", "message": "..." } }`。

## 限制和注意事项

- 单次 MCP 调用超时为 30 秒（官方服务）或 15 秒（自定义服务），不可配置；  
- 自定义 MCP 服务必须提供 `/health` 健康检查端点，且响应头需含 `X-MCP-Version: 1.0`；  
- 不支持跨域直接浏览器调用（CORS 需显式配置），仅限服务端间通信；  
- `input` 中禁止包含敏感字段如 `password`、`api_key` —— 应通过平台凭证管理机制注入。  

请严格遵循 [原文标题](../../raw/application-user-guide/model-context-protocol.md) 中「常见问题」章节关于错误码分类（如 `TOOL_NOT_FOUND`, `INPUT_VALIDATION_FAILED`）的定义，确保客户端健壮性。

## 来源文档

- [MCP](../../raw/application-user-guide/model-context-protocol.md)


