# plug in

插件（Plug-in）是百炼平台提供的扩展能力机制，允许用户在不修改模型本体的前提下，通过调用外部服务或本地逻辑增强大模型的工具调用、数据检索与业务集成能力。插件以标准化 Schema 描述，支持同步/异步执行，并可与[函数调用](../concepts/function-calling.md)（Function Calling）深度协同。其设计目标是提升模型在真实业务场景中的可控性与可扩展性。

## 支持的模型/功能

当前仅 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款 Qwen 系列模型原生支持插件调用；其他模型（如 `qwen2-72b`）暂不支持，调用将被静默忽略。插件功能涵盖：HTTP Webhook 调用、数据库查询封装、企业内部系统对接（如 OA、CRM）、以及基于 OpenAPI 规范的第三方服务集成。所有插件能力均需通过 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md) 中定义的 `plugin.json` Schema 进行声明。

## 关键参数

- `plugin_id`: 必填，插件唯一标识符，需在控制台插件管理中注册并启用；
- `arguments`: JSON 字符串，必须严格符合插件 Schema 中 `parameters` 定义的结构与类型约束；
- `timeout_ms`: 可选，默认 10000（10 秒），最大支持 30000（30 秒）；
- `enable_caching`: 可选布尔值，默认 `false`，仅对幂等性明确的插件生效。  
> **注意**：`enable_caching` 参数在 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md) 中被标记为“实验性”，而 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 文档未提及该字段——实际使用中应以控制台最新 API 文档为准，避免依赖缓存行为。

## 使用方式

1. 在控制台「插件管理」中上传或启用插件（需提供 `plugin.json` 及后端服务地址）；  
2. 在请求 payload 的 `tools` 字段中声明插件 ID（如 `"tools": [{"type": "plugin", "plugin_id": "weather-v2"}]`）；  
3. 模型返回 `tool_calls` 后，调用方需解析并执行对应插件逻辑，再将结果通过 `tool_results` 提交回续写请求。完整流程详见 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。

## 限制和注意事项

- 单次请求最多声明 5 个插件，且 `tool_calls` 总数不超过 10 次（含并发调用）；  
- 插件响应体必须为 UTF-8 编码 JSON，顶层字段 `content` 为字符串，`error` 字段（若存在）不可为空字符串；  
- 自定义插件的后端服务必须支持 HTTPS 且具备有效 TLS 证书，HTTP 回调地址不得为内网 IP 或 localhost；  
- 插件调用日志仅保留 7 天，调试建议结合 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 中推荐的本地 mock 工具链进行联调。

## 来源文档

- [插件](../../raw/application-user-guide/plug-in.md)


