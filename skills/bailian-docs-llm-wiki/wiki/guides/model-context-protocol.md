# model context protocol

model context protocol（MCP）是百炼平台定义的一套标准化接口协议，用于在大模型推理过程中动态注入上下文数据（如知识库片段、实时API响应、用户会话状态等），从而增强模型对特定任务的理解与生成能力。它不依赖模型内置能力，而是通过统一的上下文协商机制实现外部数据与模型输入的协同。该协议已在多个官方服务和插件中落地验证，详见 [MCP 简介](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)。

## 支持的模型与功能

- **支持模型**：当前仅限百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三类模型（v2024.06 及以上版本），其他模型暂不支持 MCP 上下文注入。
- **核心功能**：
  - 上下文发现（Context Discovery）：自动识别请求中需补充的实体或意图，并触发对应 MCP 服务；
  - 上下文协商（Context Negotiation）：模型与 MCP 服务间按协议交换 schema、约束条件与超时策略；
  - 动态上下文注入：将服务返回的结构化数据（JSON Schema 定义）安全拼入 [prompt](prompt.md) 的指定位置。

> **注意**：原始文档中 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md) 列出的 `qwen-vl-plus` 曾标注为支持，但实测 v2024.07 版本已移除该模型的 MCP 能力，以控制台实际可用模型列表为准。

## 关键参数

调用启用 MCP 的模型时，需在 `messages` 或 `tools` 字段外显式声明以下参数：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `mcp_enabled` | boolean | 是 | 启用 MCP 协商流程；设为 `false` 或省略则跳过全部上下文注入 |
| `mcp_services` | array of string | 否 | 指定允许调用的 MCP 服务 ID 列表（如 `["kb-search", "user-profile"]`）；为空时使用默认服务集 |
| `mcp_timeout_ms` | integer | 否 | 单个 MCP 服务调用超时毫秒数，默认 `3000`，范围 `100–10000` |

完整参数示例见 [自定义MCP服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md) 中的请求体定义。

## 使用方式

1. **启用协议**：在 `/v1/chat/completions` 请求中设置 `mcp_enabled: true`；
2. **声明服务**：通过 `mcp_services` 明确白名单（推荐），避免非预期服务调用；
3. **构造消息**：在 `messages` 中使用 `role: "system"` 或 `role: "user"` 的 content 内嵌占位符（如 `{context: kb-search}`），MCP 服务将按 schema 自动填充；
4. **处理响应**：模型输出中可能包含 `mcp_context_used: [...]` 字段，列出本次实际注入的上下文项及其来源。

详细调用链路与错误码说明参见 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 限制和注意事项

- 单次请求最多触发 **3 个独立 MCP 服务调用**，超出部分被静默忽略；
- 上下文注入总长度（含 JSON 序列化后）不得超过 **8192 字符**，否则触发截断并记录警告；
- MCP 服务返回的字段若未在模型 schema 中声明，将被丢弃（非报错）；
- 不支持在流式响应（`stream: true`）中动态注入上下文——所有 MCP 调用均在首 token 生成前完成；
- 开发者须自行保障自定义 MCP 服务的鉴权与数据脱敏，平台不代理敏感字段过滤。

请务必参考 [常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md) 获取典型故障排查指引。

## 来源文档

- [MCP](../../raw/application-user-guide/model-context-protocol.md)


