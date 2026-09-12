# model context protocol

Model Context Protocol（MCP）是百炼平台提供的标准化上下文交互协议，用于在大模型应用中安全、可控地接入外部工具与数据源。它定义了模型请求上下文时的统一接口规范、参数结构和响应格式，支持同步/异步调用模式。开发者可通过官方服务或自定义服务实现上下文增强能力，详见 [MCP 简介](https://help.aliyun.com/zh/model-studio/mcp-introduction)。

## 支持的模型与功能

- 当前仅支持 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三类推理模型启用 MCP 上下文注入（`tools` 字段需显式声明）；
- 支持两类上下文来源：  
  - 官方 MCP 服务（如搜索、知识库、数据库查询等预置能力）；  
  - 自定义 MCP 服务（需符合 [自定义MCP服务](https://help.aliyun.com/zh/model-studio/custom-mcp) 规范并完成鉴权注册）；  
- 不支持在流式响应（`stream: true`）中动态触发 MCP 工具调用，该限制已在 [外部调用](https://help.aliyun.com/zh/model-studio/mcp-external-calls) 文档中明确说明。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `tools` | array | 是 | 工具描述列表，每个元素含 `type`（固定为 `"mcp"`）、`name`（服务标识符）、`description`（功能说明）及可选 `parameters`（JSON Schema 格式）； |
| `tool_choice` | string / object | 否 | 控制调用策略：`"auto"`（默认）、`"none"` 或 `{ "type": "mcp", "name": "xxx" }`； |
| `context` | object | 否 | 透传给 MCP 服务的上下文元数据，如 `{"user_id": "u123", "session_id": "s456"}`，字段需与服务端约定一致； |

> **注意**：`context` 参数在 [MCP 简介](https://help.aliyun.com/zh/model-studio/mcp-introduction) 中被描述为“可选且自由扩展”，但实际调用中若服务端校验严格，缺失必要字段将导致 400 错误——请以 [自定义MCP服务](https://help.aliyun.com/zh/model-studio/custom-mcp) 的服务契约为准。

## 使用方式

1. 在请求 payload 中声明 `tools` 数组，例如：
   ```json
   {
     "model": "qwen-plus",
     "messages": [...],
     "tools": [{
       "type": "mcp",
       "name": "web_search",
       "description": "实时网络搜索",
       "parameters": { "type": "object", "properties": { "query": { "type": "string" } } }
     }]
   }
   ```
2. 发起标准 `/v1/chat/completions` 请求（HTTP POST）；
3. 模型返回 `tool_calls` 后，平台自动调用对应 MCP 服务，并将结果注入后续上下文；  
完整流程示例见 [外部调用](https://help.aliyun.com/zh/model-studio/mcp-external-calls)。

## 限制和注意事项

- 单次请求最多声明 5 个 `tools`，超出部分将被静默截断；
- MCP 服务响应超时阈值为 15 秒，超时后视为调用失败，不重试；
- 所有 MCP 调用均经过百炼网关鉴权与审计，**禁止在 `tools` 或 `context` 中传递敏感凭证（如 API Key、[Token](../concepts/token.md)）**，应通过服务端配置完成授权；
- 自定义 MCP 服务必须使用 HTTPS 且支持 `application/json` 请求体，否则无法通过 [官方 MCP 服务](https://help.aliyun.com/zh/model-studio/official-and-third-party-mcp) 的连通性检测。

## 来源文档

- [MCP](../../raw/application-user-guide/model-context-protocol.md)


