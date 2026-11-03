# plug in

插件（Plug-in）是百炼平台提供的扩展能力机制，允许用户在不修改模型本体的前提下，通过调用外部服务或本地逻辑增强大模型的工具调用、数据检索与业务集成能力。插件以标准化 Schema 描述，支持同步/异步执行，并可与[函数调用](../concepts/function-calling.md)（Function Calling）流程深度协同。其设计目标是提升模型在真实业务场景中的可控性与可扩展性。

## 支持的模型/功能

当前仅 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款 Qwen 系列模型原生支持插件调用能力；其他模型（如 `qwen2-72b` 或第三方模型）暂不支持，调用将被静默忽略。插件功能涵盖 HTTP API 调用、数据库查询封装、内部系统对接（如审批流、CRM）及轻量计算任务。详细支持列表见 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。

## 关键参数

插件调用需在请求中显式声明 `tools` 字段（类型为 `array`），每个元素包含 `type: "plugin"`、`plugin_id`（平台分配的唯一标识）及可选 `parameters`（JSON 对象）。`tool_choice` 控制调用策略：`"auto"`（默认，由模型决策）、`"required"`（强制调用至少一个插件）或指定 `{"type": "plugin", "id": "xxx"}`。参数校验严格遵循插件注册时定义的 OpenAPI 3.0 Schema，详见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。

## 使用方式

1. 在控制台「插件管理」中启用或上传插件（需提供合法 endpoint、认证方式及 schema）；  
2. 构造 LLM 请求，在 `messages` 后追加 `tools` 数组并设置 `tool_choice`；  
3. 解析响应中 `tool_calls` 字段，按 `id` 和 `function.arguments` 发起插件调用；  
4. 将插件返回结果以 `tool_message` 形式再次提交，供模型生成最终回复。完整流程示例参见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

## 限制和注意事项

- 单次请求最多声明 20 个插件，且 `tools` 总大小不得超过 2MB；  
- 插件 endpoint 必须支持 HTTPS，超时阈值固定为 15 秒，不可配置；  
- > **注意**：文档 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md) 中提及“支持 WebSocket 插件类型”，但该特性尚未上线，实际调用会返回 `400 Unsupported tool type` 错误，请勿依赖；  
- 插件调用日志默认保留 7 天，敏感字段（如 `Authorization` header、`parameters` 中的 `password` 字段）自动脱敏；  
- 自定义插件的 `parameters` 若含嵌套对象，需确保 JSON Schema 中 `additionalProperties: false` 显式声明，否则可能触发校验失败——此要求在 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 中有明确说明，但 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md) 的示例未体现，建议以自定义插件文档为准。

## 来源文档

- [插件](../../raw/application-user-guide/plug-in.md)


