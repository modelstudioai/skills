# model context protocol

model context protocol（MCP）是百炼平台提供的标准化上下文交互协议，用于在大模型应用中安全、可控地接入外部工具与数据源。它通过定义统一的请求/响应结构和生命周期管理机制，使模型能按需调用函数、检索知识或执行操作，同时保障上下文隔离与权限收敛。该协议已在百炼控制台、SDK 及 API 层面深度集成。

## 支持的模型与功能

MCP 当前支持所有百炼平台托管的 `qwen-max`、`qwen-plus`、`qwen-turbo` 等 Qwen 系列模型（含 v1/v2 版本），以及通过 [自定义MCP服务](https://help.aliyun.com/zh/model-studio/custom-mcp) 接入的第三方模型。核心功能包括：工具发现（tool discovery）、上下文感知的[函数调用](../concepts/function-calling.md)（context-aware tool calling）、多轮会话中的状态保持（stateful session context），以及基于角色的工具访问控制。详细能力边界请参见 [MCP 简介](https://help.aliyun.com/zh/model-studio/mcp-introduction)。

## 关键参数

调用 MCP 时需在 `messages` 中显式声明 `tool_choice` 和 `tools` 字段，并在 `tools` 中提供符合 OpenAI-style function schema 的工具定义。关键字段包括：

- `tools`: 工具列表，每个工具必须包含 `type: "function"`、`function.name`、`function.description` 和 `function.parameters`（JSON Schema 格式）  
- `tool_choice`: 可选 `"auto"`、`"none"` 或 `{"type": "function", "function": {"name": "xxx"}}`  
- `tool_config`: （可选）用于指定超时、重试、鉴权等运行时策略，详见 [外部调用](https://help.aliyun.com/zh/model-studio/mcp-external-calls)  

> **注意**：`tool_config` 在 [raw/application-user-guide/model-context-protocol.md](../../raw/application-user-guide/model-context-protocol.md) 中未定义具体字段，实际可用参数以 SDK 文档和 [外部调用](https://help.aliyun.com/zh/model-studio/mcp-external-calls) 为准。

## 使用方式

1. 在请求 payload 中构造 `tools` 数组并注入工具定义；  
2. 设置 `tool_choice` 控制调用策略；  
3. 发送请求至 `/v1/chat/completions`（需 `model` 参数为支持 MCP 的模型）；  
4. 解析响应中的 `tool_calls` 字段，同步或异步执行对应工具逻辑；  
5. 将工具执行结果以 `tool_message` 形式拼入下一轮 `messages` 并继续请求。  
完整示例见 [官方 MCP 服务](https://help.aliyun.com/zh/model-studio/official-and-third-party-mcp) 及 [raw/application-user-guide/model-context-protocol.md](../../raw/application-user-guide/model-context-protocol.md)。

## 限制和注意事项

- 单次请求最多声明 20 个工具，单个工具 `parameters` Schema 深度不得超过 8 层；  
- 工具调用链深度限制为 5 层（即最多嵌套 5 次 `tool_message` → 新 `tool_call`）；  
- 不支持在流式响应（`stream: true`）中解析 `tool_calls`，必须等待完整响应；  
- 所有工具端点必须启用 HTTPS 且响应头包含 `Access-Control-Allow-Origin: *`（浏览器场景）或通过百炼网关代理（服务端场景）。  
常见兼容性问题与调试建议汇总于 [常见问题](https://help.aliyun.com/zh/model-studio/mcp-faq)，亦可对照 [raw/application-user-guide/model-context-protocol.md](../../raw/application-user-guide/model-context-protocol.md) 进行快速核验。

## 来源文档

- [MCP](../../raw/application-user-guide/model-context-protocol.md)


