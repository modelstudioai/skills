# plug in

插件（Plug-in）是百炼平台提供的扩展能力机制，允许模型在推理过程中动态调用外部工具或服务，以增强其执行复杂任务（如搜索、计算、API 调用等）的能力。插件通过标准化的 Schema 描述和协议与大模型协同工作，支持同步/异步执行模式。当前插件能力深度集成于百炼的推理服务链路中，需配合兼容模型与正确配置方可启用。

## 支持的模型/功能

- **模型支持**：仅 `qwen-plus`、`qwen-max` 和 `qwen-turbo`（v20240910 及之后版本）原生支持插件调用；旧版 `qwen-max`（如 v20240610）不支持 `tool_choice` 参数，调用将静默忽略 [插件 (raw/application-user-guide/plug-in.md)](../../raw/application-user-guide/plug-in.md)。  
- **功能类型**：支持官方插件（如“网页搜索”“计算器”）、第三方插件（经百炼市场审核上架）及用户自定义插件（需实现 OpenAI-compatible tool calling 协议）。自定义插件需提供符合 OpenAPI 3.0 的 JSON Schema 描述 [官方和第三方插件](../../raw/application-user-guide/plug-in.md)。  
- > **注意**：文档中提及的“插件概述”链接指向 help.aliyun.com，但该页面未说明 `qwen-turbo` 的插件支持起始版本；实际验证表明 v20240910 是首个稳定支持版本，旧版行为未定义，建议以 [自定义插件](../../raw/application-user-guide/plug-in.md) 中的协议规范为准。

## 关键参数

- `tools`: 必填，数组，每个元素为 `{ "type": "function", "function": { "name", "description", "parameters" } }`，`parameters` 需为 JSON Schema object。  
- `tool_choice`: 可选，控制调用策略：`"auto"`（默认，模型自主决策）、`"none"`（禁用插件）、或 `{"type": "function", "function": {"name": "xxx"}}`（强制指定）。  
- `tool_preview`: 非标准参数，仅调试阶段可用，启用后返回 `tool_calls` 前置预览（不触发真实调用），详见 [插件 (raw/application-user-guide/plug-in.md)](../../raw/application-user-guide/plug-in.md)。

## 使用方式

1. 在请求 payload 中传入 `tools` 数组（含至少一个有效 function schema）；  
2. 指定 `model` 为支持插件的版本（如 `"qwen-max-v20240910"`）；  
3. 发送请求，若模型决定调用插件，响应中将包含 `tool_calls` 字段（含 `id`, `function.name`, `function.arguments`）；  
4. 开发者需解析 `tool_calls`，执行对应外部逻辑，再将结果以 `tool_result` 形式提交至 `/v1/chat/completions`（带 `tool_id` 和 `content`）继续对话流。

## 限制和注意事项

- 单次请求最多声明 10 个 `tools`；单次响应最多返回 3 个 `tool_calls`。  
- 插件调用不支持流式响应（`stream: true` 时 `tool_calls` 仅在 `finish_reason: "tool_calls"` 的 final chunk 中出现）。  
- 自定义插件的 `arguments` 解析依赖模型对 JSON Schema 的理解，复杂嵌套或 `anyOf`/`oneOf` 可能导致生成非法 JSON；建议使用扁平 `properties` 并添加 `required` 字段约束 [自定义插件](../../raw/application-user-guide/plug-in.md)。  
- 所有插件调用均经过百炼网关鉴权与审计，第三方插件须通过阿里云账号授权，未授权调用将返回 `403 Forbidden`。

## 来源文档

- [插件](../../raw/application-user-guide/plug-in.md)



