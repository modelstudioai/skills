# plug in

插件（Plug-in）是百炼平台提供的扩展能力机制，允许用户在不修改模型本体的前提下，通过标准化接口调用外部服务或执行特定逻辑，从而增强大模型的工具调用、数据检索和业务集成能力。插件支持声明式定义与运行时动态加载，适用于[函数调用](../concepts/function-calling.md)（Function Calling）、RAG 增强、API 封装等场景。其设计遵循 OpenAI Function Calling 规范并做了平台适配。

## 支持的模型/功能

- **模型支持**：当前仅 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款 Qwen 系列模型原生支持插件调用；其他模型（如 `qwen2.5-7b` 或第三方模型）暂不支持，调用将被静默忽略。  
- **功能类型**：支持官方插件（如天气、翻译、知识库检索）、第三方插件（需通过 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md) 注册接入）及自定义插件（需按 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 规范实现 schema 与 endpoint）。  
- > **注意**：[插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md) 中提及“所有 32B+ 模型均支持插件”，该描述已过时，以本节为准。

## 关键参数

- `plugins`: JSON 数组，每个元素为 `{ "name": "xxx", "description": "...", "parameters": { ... } }`，必须与插件注册时的 schema 严格一致；  
- `enable_plugins`: 布尔值，默认 `false`，显式设为 `true` 才启用插件解析与调用；  
- `plugin_timeout_ms`: 整数，单位毫秒，默认 `10000`（10 秒），超时后终止插件请求并回退至纯文本响应；  
- 插件调用结果通过 `tool_calls` 字段返回，格式与 OpenAI 兼容，详见 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。

## 使用方式

1. **注册插件**：在控制台「插件管理」中上传 OpenAPI 3.0 Schema 文件，或通过 API 注册；第三方插件需先完成鉴权配置。  
2. **发起请求**：在 `/v1/chat/completions` 请求体中设置 `"enable_plugins": true`，并在 `messages` 中提供含工具意图的用户输入（如“查上海今天天气”）；  
3. **处理响应**：若模型返回 `tool_calls`，需按 `name` 和 `arguments` 调用对应插件 endpoint，并将结果以 `tool_message` 形式再次提交给模型完成终局推理。

## 限制和注意事项

- 单次请求最多触发 **3 个插件调用**，且总耗时（含网络延迟）不得超过 `plugin_timeout_ms`；  
- 插件 endpoint 必须支持 HTTPS、返回 JSON 格式，且响应头需包含 `Content-Type: application/json`；  
- 自定义插件的 `parameters` 定义中禁止使用 `$ref` 引用外部 schema，否则注册失败——该约束在 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 中有明确说明；  
- > **注意**：[官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md) 文档中示例使用的 `api_key` 透传方式已被弃用，现统一通过平台托管凭证（`credential_id`）进行安全调用。

## 来源文档

- [插件](../../raw/application-user-guide/plug-in.md)


