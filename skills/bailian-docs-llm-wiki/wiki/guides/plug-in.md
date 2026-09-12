# plug in

插件（Plug-in）是百炼平台支持的外部能力扩展机制，允许模型在推理过程中动态调用函数、API 或工具，以增强其对现实世界任务的处理能力。插件可由平台官方提供、第三方发布或用户自定义，需通过标准化协议（如 OpenAPI Schema）描述接口契约。当前仅适用于部分支持工具调用（tool calling）能力的大模型。

## 支持的模型/功能

- **模型支持**：仅 `qwen-max`、`qwen-plus` 和 `qwen-turbo`（v20240910 及之后版本）原生支持插件调用；其他模型（如 `qwen2-72b`）即使配置 `tools` 参数也不会触发实际调用，返回空 `tool_calls` 字段。  
- **功能类型**：支持同步 HTTP API 调用（含鉴权、参数校验、错误重试），暂不支持异步任务、流式响应或 WebSocket 接口。  
- 官方插件覆盖搜索、天气、翻译、数据库查询等场景，详情见 [插件概述](../../raw/application-user-guide/plug-in.md)；第三方与自定义插件能力详见 [官方和第三方插件](../../raw/application-user-guide/plug-in.md) 与 [自定义插件](../../raw/application-user-guide/plug-in.md)。

## 关键参数

- `tools`: 必填，为 JSON Schema 数组，每个元素需包含 `type: "function"`、`function.name`、`function.description` 及 `function.parameters`（遵循 OpenAPI 3.0.3 subset）。  
- `tool_choice`: 可选，取值 `"auto"`（默认）、`"none"` 或 `{ "type": "function", "function": { "name": "xxx" } }`；设为 `"none"` 时强制禁用插件调用。  
- `enable_thinking`: 若启用（`true`），模型可能在 `thinking` 字段中解释调用逻辑，但该字段不参与 token 计费，且 [自定义插件](../../raw/application-user-guide/plug-in.md) 文档明确指出其输出不可靠，不应作为业务判断依据。

## 使用方式

1. 在请求 payload 中传入 `tools` 和（可选）`tool_choice`；  
2. 模型返回 `finish_reason: "tool_calls"` 时，解析 `message.tool_calls` 获取调用列表；  
3. 同步执行对应函数，构造 `{"role": "tool", "tool_call_id": "...", "content": "..."}` 格式的 tool message；  
4. 将 tool message 与原始 messages 拼接后再次请求模型，完成多轮工具交互。  
> **注意**：[插件概述](../../raw/application-user-guide/plug-in.md) 中提及的“自动重试失败调用”功能在 v202410 版本中已被移除，实际需由客户端实现重试逻辑。

## 限制和注意事项

- 单次请求最多声明 20 个 `tools`，单次响应最多触发 5 次 `tool_calls`；  
- 插件调用超时固定为 10 秒，超时后返回 `{"error": "tool_timeout"}`，不重试；  
- 所有插件 endpoint 必须使用 HTTPS，且域名需在百炼控制台白名单中备案（自定义插件必填）；  
- `tools` 参数中的 `parameters` 不支持 `nullable: true` 或 `oneOf` 等复杂联合类型，否则导致 schema 解析失败——此限制未在 [官方和第三方插件](../../raw/application-user-guide/plug-in.md) 中明确说明，但实测验证存在。

## 来源文档

- [插件](../../raw/application-user-guide/plug-in.md)


