# model context protocol

Model Context Protocol（MCP）是百炼平台提供的标准化上下文交互协议，用于在大模型应用中安全、可控地接入外部工具、数据源或业务系统。它通过定义统一的请求/响应结构与生命周期语义，使模型能以结构化方式调用外部能力，同时保障上下文隔离与权限收敛。该协议已在百炼控制台和 SDK 中深度集成，开发者可快速启用或自建符合规范的服务。

## 支持的模型与功能

MCP 当前支持所有百炼平台托管的 LLM 模型（包括 Qwen 系列、Qwen2 系列及第三方接入模型），但**仅在 `chat` 类型会话中生效**，不适用于 `completion` 或 `embedding` 场景。核心功能包括：工具发现（`list_tools`）、上下文感知工具调用（`call_tool`）、多轮状态保持（通过 `session_id` 绑定上下文），以及服务端自动注入的元信息（如 `tool_id`、`execution_id`）。详细能力边界请参阅 [MCP 简介](https://help.aliyun.com/zh/model-studio/mcp-introduction) —— 该文档明确指出 MCP 不替代传统 API 网关，而是聚焦于“模型驱动的上下文敏感调用”。

## 关键参数

调用 MCP 服务时需在请求体中显式传递以下字段（均为必填）：

- `tool_id`: 字符串，注册时分配的唯一工具标识（非 URL 路径）；
- `input`: 对象，结构由工具 schema 定义，**不支持嵌套过深（最大深度为 5）**；
- `session_id`: 字符串，用于跨轮次上下文关联，长度限制 64 字符；
- `trace_id`: 可选字符串，用于全链路追踪（建议与调用方 trace 一致）。

注意：`input` 中若含二进制内容（如 base64 图片），必须在 schema 中声明 `"type": "string", "format": "binary"`，否则服务端将拒绝解析。此约束在 [自定义MCP服务](https://help.aliyun.com/zh/model-studio/custom-mcp) 文档中有明确定义，但 [外部调用](https://help.aliyun.com/zh/model-studio/mcp-external-calls) 文档未强调，实际实现应以 [自定义MCP服务](https://help.aliyun.com/zh/model-studio/custom-mcp) 为准。

## 使用方式

1. **启用 MCP**：在百炼控制台「应用配置 → 高级设置」中开启「启用 Model Context Protocol」开关；  
2. **注册工具**：通过控制台或 OpenAPI 提交工具描述（JSON Schema 格式），指定 `tool_id` 与 endpoint；  
3. **发起调用**：在 `messages` 中插入 `{"role": "tool", "content": "...", "tool_call_id": "..."}` 类型消息，或使用 SDK 的 `client.chat(..., tools=[...])` 方法；  
4. **处理响应**：模型返回 `tool_calls` 数组后，客户端需按 `tool_call_id` 并行调用对应 MCP 服务，并将结果以 `{"role": "tool", ...}` 形式回传。完整流程示例见 [外部调用](https://help.aliyun.com/zh/model-studio/mcp-external-calls)。

> **注意**：SDK v3.12.0+ 默认启用 MCP 自动重试（最多 2 次），但若服务返回 HTTP 400，SDK 不重试且直接抛出异常；而 [MCP 简介](https://help.aliyun.com/zh/model-studio/mcp-introduction) 中描述的“失败自动降级为普通文本”属于旧版行为，已废弃，请以当前 SDK 行为为准。

## 限制和注意事项

- 单次 `call_tool` 请求 payload 上限为 2 MB，响应上限为 1 MB；  
- 工具执行超时默认为 15 秒，不可配置（[官方 MCP 服务](https://help.aliyun.com/zh/model-studio/official-and-third-party-mcp) 明确说明）；  
- 同一 `session_id` 下并发调用同一 `tool_id` 的请求，服务端不保证执行顺序；  
- 所有 MCP 流量经百炼网关鉴权，**禁止绕过平台直接访问工具 endpoint**，否则将触发风控拦截；  
- 错误码 `MCP_TOOL_NOT_FOUND` 表示 `tool_id` 未注册或已下线，而非网络错误——该语义定义见 [常见问题](https://help.aliyun.com/zh/model-studio/mcp-faq)。

## 来源文档

- [MCP](../../raw/application-user-guide/model-context-protocol.md)



