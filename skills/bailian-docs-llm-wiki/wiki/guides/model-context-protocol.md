# model context protocol

Model Context Protocol（MCP）是百炼平台提供的标准化上下文交互协议，用于在大模型应用中解耦模型推理与外部工具/数据源的调用逻辑。它通过定义统一的请求/响应结构和生命周期语义，支持开发者以声明式方式集成检索、数据库、API 等上下文服务。该协议已在多个官方 SDK 和运行时中实现 [MCP 简介](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)。

## 支持的模型与功能

- **模型支持**：当前仅 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款 Qwen 系列模型原生支持 MCP；其他模型（如 `qwen-vl` 或第三方模型）暂不支持上下文注入能力。
- **核心功能**：
  - 工具发现（tool discovery）与动态注册
  - 上下文片段按需加载（on-demand context fetching）
  - 多轮会话中上下文状态保持（stateful context session）
  - 错误回退与降级策略（fallback to no-context when MCP service unavailable）

> **注意**：[官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md) 文档中提及的 `qwen-14b-chat` 支持已过时——该模型自 v2.3.0 起已移除 MCP 兼容层，请以控制台模型能力列表为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `mcp_server_url` | string | 是 | MCP 服务端地址，须为 HTTPS，且需通过百炼平台白名单校验 |
| `tools` | array[object] | 否 | 工具描述列表，结构需符合 [MCP 简介](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md) 中定义的 Tool Schema |
| `context_timeout_ms` | integer | 否 | 上下文获取超时，默认 5000ms，最小值 100ms，最大值 30000ms |

## 使用方式

1. 在 `ChatCompletion` 请求的 `extra_parameters` 字段中启用 MCP：
   ```json
   {
     "model": "qwen-plus",
     "messages": [...],
     "extra_parameters": {
       "mcp_enabled": true,
       "mcp_server_url": "https://your-mcp-service.example.com/v1",
       "tools": [...]
     }
   }
   ```
2. 确保 MCP 服务遵循 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md) 规范，提供 `/tools`（发现）和 `/context`（获取）两个标准端点；
3. 客户端无需手动解析上下文响应——百炼运行时自动注入并参与 [prompt](prompt.md) 构建。

## 限制和注意事项

- 单次请求最多允许 5 个工具注册，总上下文 token 数上限为 2048（超出部分将被截断）；
- MCP 服务响应必须在 `context_timeout_ms` 内返回，超时后请求将降级为无上下文模式，**不抛出错误**；
- 自定义 MCP 服务需自行保障鉴权与速率限制，百炼平台不代理或缓存其响应 —— 详见 [自定义MCP服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)；
- 不支持嵌套 MCP 调用（即 MCP 服务内部不可再发起 MCP 请求）。

## 来源文档

- [MCP](../../raw/application-user-guide/model-context-protocol.md)


