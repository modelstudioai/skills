# model context protocol

model context protocol（MCP）是百炼平台提供的标准化上下文交互协议，用于在大模型调用中动态注入结构化外部数据（如数据库查询结果、实时日志、知识库片段等），从而增强模型推理的准确性与上下文相关性。它通过统一的 JSON-RPC 2.0 接口规范定义服务契约，支持同步/异步调用模式。该协议已在多个百炼内置工具链和插件系统中落地应用，详见 [MCP 简介](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)。

## 支持的模型与功能

- **支持模型**：当前仅 `qwen-max`、`qwen-plus` 和 `qwen-turbo`（v202409 及以上版本）原生支持 MCP 上下文注入；其他模型需通过 `tools` 字段显式声明 `mcp://` 类型工具才能触发协议解析。
- **核心功能**：
  - 上下文片段按需加载（on-demand context fetching）
  - 多源上下文并行获取与自动去重合并
  - 基于 `context_id` 的缓存生命周期控制（TTL 可配）
  - 错误降级：当 MCP 服务不可用时，自动跳过该上下文项，不中断主推理流程  
  更多能力边界说明请参阅 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `mcp_url` | string | 是 | 符合 `mcp://<host>:<port>/<path>` 格式的标准服务地址；支持 HTTPS 回退（如 `mcp+https://...`） |
| `context_id` | string | 否 | 用于缓存键和日志追踪；若未提供，平台自动生成 UUID |
| `timeout_ms` | integer | 否 | 单次请求超时，默认 `3000`（ms），上限 `10000` |
| `retry_count` | integer | 否 | 服务失败时重试次数，默认 `1`，最大 `2` |

> **注意**：原始文档中 [自定义MCP服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md) 提到 `retry_count` 默认为 `0`，但实测 v202409+ 版本 SDK 已统一为 `1`，以提升弱网环境鲁棒性，请以运行时行为为准。

## 使用方式

1. 在请求 payload 的 `messages` 中任一 `user` 消息内添加 `context` 字段：
   ```json
   {
     "role": "user",
     "content": "请基于最新销售数据回答问题",
     "context": {
       "mcp_url": "mcp://sales-api.internal/v1/recent-orders",
       "context_id": "sales_q3_2024",
       "timeout_ms": 5000
     }
   }
   ```
2. 若需并发加载多个上下文，可在同一消息中使用 `context_list` 数组（优先级高于单个 `context`）；
3. 客户端必须确保 `mcp_url` 对应的服务已注册至百炼 MCP 目录（或配置白名单），否则请求将被拒绝 —— 具体接入步骤见 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 限制和注意事项

- 单次请求最多允许 5 个独立 MCP 上下文项（`context` + `context_list` 合计）；
- 每个上下文返回内容总大小限制为 128 KB（解压后），超出部分将被截断并记录警告；
- MCP 服务响应必须符合 [JSON-RPC 2.0 规范](https://www.jsonrpc.org/specification)，且 `result` 字段须为字符串或对象（不支持数组）；
- 不支持跨域凭证传递（如 cookies、Authorization header），所有认证需通过 `mcp_url` 查询参数或服务端预置密钥完成；
- 调试建议：启用 `debug: true` 请求头可获取完整上下文加载链路日志（含耗时、状态码、原始响应）。  
  遇到非预期行为时，请首先核对 [常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md) 中的典型场景。

## 来源文档

- [MCP](../../raw/application-user-guide/model-context-protocol.md)


