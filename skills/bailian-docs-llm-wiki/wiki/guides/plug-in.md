# plug in

插件（Plug-in）是百炼平台支持的外部能力扩展机制，允许模型在推理过程中动态调用函数、API 或其他服务，以增强其处理现实世界任务的能力。插件可由平台官方提供、第三方发布或用户自定义，需通过标准化协议（如 OpenAPI Schema）声明接口契约。当前仅适用于部分大语言模型，并依赖于模型自身对工具调用协议的理解与支持。

## 支持的模型/功能

- **支持模型**：`qwen-max`、`qwen-plus` 和 `qwen-turbo`（v202408 及之后版本）原生支持插件调用；`qwen2.5-72b-instruct` 等开源模型需通过 `tool_choice` + `tools` 参数显式启用，且实际效果取决于微调质量与工具描述清晰度。  
- **核心功能**：包括同步 HTTP API 调用、多步骤工具编排（需模型自主规划）、结果自动注入上下文等。不支持异步回调、长时任务轮询或二进制文件上传类操作。  
- 更多兼容性细节请参考 [插件概述](../../raw/application-user-guide/plug-in.md) 中的模型支持矩阵说明。

## 关键参数

调用插件需在请求体中显式传入以下字段：

- `tools`: 必填，数组格式，每个元素为符合 OpenAPI 3.0.3 的 JSON Schema 描述（含 `name`、`description`、`parameters`），[官方和第三方插件](../../raw/application-user-guide/plug-in.md) 提供了标准模板示例；  
- `tool_choice`: 可选，控制调用策略：`"auto"`（默认，由模型决策）、`"none"`（禁用）、或指定 `{"type": "function", "function": {"name": "xxx"}}` 强制调用；  
- `enable_thinking`: 非插件专属参数，但影响插件使用效果——若设为 `false`，模型将跳过规划步骤，可能导致 `tool_calls` 输出为空，详见 [自定义插件](../../raw/application-user-guide/plug-in.md) 的调试建议。

> **注意**：文档中提及“所有 Qwen 系列模型均支持插件”，但实测 `qwen-1.8b-chat` 在 v202406 版本中无法解析 `tools` 字段并返回 `invalid_parameter` 错误。该描述已过时，请以 [插件概述](../../raw/application-user-guide/plug-in.md) 中的最新兼容列表为准。

## 使用方式

1. **准备工具定义**：按 OpenAPI Schema 编写 JSON 描述，确保 `parameters` 中必填字段标记 `"required"`，且类型严格匹配（如 `integer` 不可写作 `int`）；  
2. **构造请求**：在 `/v1/chat/completions` 接口请求中嵌入 `tools` 与 `tool_choice`；  
3. **处理响应**：检查 `response.choices[0].message.tool_calls` 是否存在；若存在，执行对应函数并以 `tool_result` 格式发起下一轮请求（`messages` 追加 `role: "tool"` 消息）；  
4. **终止条件**：当 `finish_reason == "stop"` 且无 `tool_calls` 时，视为流程完成。

## 限制和注意事项

- 单次请求最多声明 20 个 `tools`，单次调用最多触发 5 次 `tool_calls`（防止无限循环）；  
- 插件调用不经过百炼平台鉴权代理，**所有凭证（如 API Key）必须由用户在客户端自行注入并加密管理**，平台不存储或透传敏感字段；  
- 响应超时统一为 15 秒（含网络+函数执行），超时后模型将中止调用并尝试生成兜底回复；  
- 自定义插件的错误日志仅返回至调用方 `tool_result` 的 `content` 字段，平台侧无独立监控入口，调试需依赖 [自定义插件](../../raw/application-user-guide/plug-in.md) 文档中的日志埋点建议。

## 来源文档

- [插件](../../raw/application-user-guide/plug-in.md)


