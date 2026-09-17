# model context protocol

model context protocol（MCP）是百炼平台提供的标准化上下文交互协议，用于在大模型调用过程中动态注入结构化外部数据（如数据库查询结果、实时日志、知识库片段等），从而增强模型推理的准确性与上下文相关性。它通过统一的 JSON-RPC 2.0 接口规范实现模型与外部服务的解耦通信，支持同步/异步两种调用模式。该协议已在多个官方模型和[插件](../concepts/plugin.md)场景中落地验证，详见 [MCP 简介](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)。

## 支持的模型与功能

- **内置支持模型**：`qwen-max`, `qwen-plus`, `qwen-turbo`（v202408 及以上版本）原生支持 MCP 上下文注入；`qwen-vl` 和 `qwen-audio` 暂不支持[多模态](../concepts/multi-modal.md)上下文扩展。
- **核心功能**：
  - 上下文片段按优先级自动拼接至 system [prompt](prompt.md) 或独立 context 字段；
  - 支持多源并行调用（最多 5 个 MCP 服务并发）；
  - 提供 `mcp/tools` 工具发现接口，供模型运行时动态加载可用能力；
  - 与百炼工作流（Workflow）深度集成，可在节点级配置 MCP 调用策略。

> **注意**：文档 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md) 中列出的部分第三方服务（如 `mcp://weather-api`）已因接口变更于 2024.07 下线，实际可用服务请以控制台「MCP 服务市场」实时列表为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `mcp_context` | object | 否 | 主上下文对象，含 `tools`, `sources`, `timeout_ms` 字段 |
| `tools` | array | 否 | 工具描述数组，每个元素为 `{name, description, parameters}`，遵循 OpenAPI 3.0 子集 |
| `sources` | array | 否 | 上下文数据源列表，每个元素为 `{uri, method, params, priority}`，`uri` 格式为 `mcp://<service>/<endpoint>` |
| `timeout_ms` | number | 否 | 单次 MCP 调用超时，默认 `3000`（ms），最大 `10000` |

完整参数定义与示例见 [自定义MCP服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)。

## 使用方式

1. **启用协议**：在 `ChatCompletion` 请求的 `extra_parameters` 中传入 `mcp_context` 对象（非 `messages` 内容）；
2. **服务注册**：通过控制台或 API 注册 MCP 服务端点（需提供符合 [MCP 规范](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md) 的 JSON-RPC 2.0 实现）；
3. **调试验证**：使用 `mcp validate --uri mcp://your-service/ping` CLI 命令校验服务连通性与响应格式。

## 限制和注意事项

- 单次请求最多携带 10 个 `sources`，总响应体大小（所有 source 合并后）不得超过 64KB；
- `mcp_context` 中的 `tools` 仅在模型明确声明支持工具调用（如 `enable_tools: true`）时生效；
- 不支持嵌套 MCP 调用（即 MCP 服务内部不可再发起 `mcp://` 请求）；
- 所有 `sources` 默认按 `priority` 降序合并，同优先级按字典序排序 —— 此行为与 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md) 文档中旧版“按声明顺序”描述存在差异，请以当前运行时逻辑为准。

## 来源文档

- [MCP](../../raw/application-user-guide/model-context-protocol.md)


