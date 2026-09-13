# model context protocol

Model Context Protocol（MCP）是百炼平台提供的标准化上下文交互协议，用于在大模型应用中安全、可控地接入外部工具与数据源。它通过定义统一的请求/响应结构和生命周期语义，使 LLM 能够按需调用函数、检索知识或执行操作，同时保障上下文隔离与权限收敛。该协议已在百炼控制台、SDK 及 Agent 框架中深度集成。

## 支持的模型与功能

MCP 当前支持所有百炼平台托管的 `qwen-max`、`qwen-plus`、`qwen-turbo` 等 Qwen 系列模型（含 v1/v2 接口），以及通过 [自定义MCP服务](https://help.aliyun.com/zh/model-studio/custom-mcp) 接入的第三方模型。核心功能包括：  
- 工具调用（tool calling）与多轮上下文绑定  
- 动态工具发现（通过 `/tools` 端点返回 OpenAPI 格式描述）  
- 上下文感知的参数注入（如 `user_id`、`session_id` 等运行时上下文字段）  
- 与百炼 Agent Runtime 的原生协同，支持自动 fallback 与错误重试逻辑  

> **注意**：部分旧版文档称 MCP 仅支持 `qwen-max`，但实际已扩展至全部 Qwen 公共模型——请以 [官方 MCP 服务](https://help.aliyun.com/zh/model-studio/official-and-third-party-mcp) 的最新说明为准。

## 关键参数

MCP 请求需在 `messages` 中携带特殊 `tool_calls` 字段，并在 `tools` 数组中声明可用工具。关键参数如下：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `tools[].function.name` | string | 是 | 工具唯一标识符，须与 MCP 服务注册名一致 |
| `tools[].function.description` | string | 是 | 工具功能描述，供模型理解调用意图 |
| `tools[].function.parameters` | JSON Schema | 否 | OpenAPI 3.0 兼容的参数定义，影响模型生成参数值的准确性 |
| `tool_choice` | `"auto"` / `"required"` / `{"type": "function", "name": "xxx"}` | 否 | 控制调用策略；默认为 `"auto"`，详见 [MCP 简介](https://help.aliyun.com/zh/model-studio/mcp-introduction) |

## 使用方式

1. **启用 MCP**：在百炼控制台创建应用时，于「模型配置」页勾选「启用 Model Context Protocol」；  
2. **注册工具**：通过控制台「工具管理」上传 OpenAPI YAML/JSON，或调用 `POST /v1/mcp/tools` 接口注册（需携带 `Authorization: Bearer <token>`）；  
3. **发起推理请求**：在 `/v1/chat/completions` 请求体中传入 `tools` 和 `tool_choice`，模型将返回 `tool_calls`；  
4. **执行与回调**：客户端解析 `tool_calls`，调用对应 MCP 服务端点（如 `POST https://mcp.example.com/execute`），并将结果以 `tool_responses` 形式追加到后续请求的 `messages` 中。  

完整流程示例见 [外部调用](https://help.aliyun.com/zh/model-studio/mcp-external-calls) 文档。

## 限制和注意事项

- 单次请求最多声明 50 个工具，单次响应最多触发 5 次 `tool_calls`；  
- 工具响应体必须为 JSON，且顶层字段 `content` 或 `result` 将被自动注入上下文（其他字段被忽略）；  
- MCP 服务端点必须支持 HTTPS、CORS（`Access-Control-Allow-Origin: *`），且响应头需包含 `Content-Type: application/json`；  
- 若使用自建 MCP 服务，请确保其符合 [MCP 协议规范](../../raw/application-user-guide/model-context-protocol.md)，否则可能触发 `invalid_tool_response` 错误；  
- 调试时建议开启 `debug: true` 参数，可在响应中获取 `mcp_trace` 字段查看工具调度链路——该能力在 [常见问题](https://help.aliyun.com/zh/model-studio/mcp-faq) 中有详细说明。

## 来源文档

- [MCP](../../raw/application-user-guide/model-context-protocol.md)


