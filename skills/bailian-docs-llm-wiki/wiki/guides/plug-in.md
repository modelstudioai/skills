# plug in

插件（Plug-in）是百炼平台提供的扩展能力机制，允许用户在不修改模型底层逻辑的前提下，动态接入外部工具、API 或业务系统，实现[函数调用](../concepts/function-calling.md)（Function Calling）、数据检索、服务编排等增强功能。插件以标准化 schema 描述能力，并通过平台统一调度与权限管控。当前插件能力深度集成于推理请求链路，支持同步/异步调用模式。

## 支持的模型/功能

- **模型支持**：仅限 `qwen-plus`、`qwen-max` 及后续标注为“支持插件调用”的大模型版本；`qwen-turbo` 和 `qwen-14b-chat` 等轻量模型**不支持**插件调用。  
- **功能类型**：  
  - 官方插件（如 `weather`, `web_search`, `calendar`）由百炼预置并维护，详见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)；  
  - 自定义插件需按 OpenAPI 3.0 规范定义 schema，并通过控制台注册，具体要求见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)；  
  - 所有插件均支持 `tool_choice` 显式控制是否启用，且可参与多轮 tool calling 迭代。

> **注意**：[插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md) 中提及“所有 Qwen 系列模型默认支持插件”，该描述已过时，实际以模型文档中标注的 `plugin_support: true` 字段为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `tools` | array | 是 | 插件定义列表，每个元素为符合 OpenAPI 3.0 的 tool schema 对象（含 `name`, `description`, `parameters`） |
| `tool_choice` | string / object | 否 | 可选 `"auto"`（默认）、`"none"` 或 `{ "type": "function", "function": { "name": "xxx" } }`；控制模型是否及如何选择插件 |
| `tool_config` | object | 否 | 高级配置，如 `{"parallel": true}` 启用并行调用（仅部分模型支持） |

## 使用方式

1. **准备插件 schema**：参考 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 编写 JSON Schema，确保 `parameters` 中各字段含 `type` 和 `description`；  
2. **发起请求**：在 `/v1/chat/completions` 请求体中传入 `tools` 和（可选）`tool_choice`；  
3. **处理响应**：当模型返回 `finish_reason: "tool_calls"` 时，解析 `message.tool_calls` 数组，按 `function.name` 和 `function.arguments` 调用对应服务；  
4. **追加调用结果**：将执行结果以 `role: "tool"` 消息格式回传，继续下一轮请求。

## 限制和注意事项

- 单次请求最多声明 20 个 `tools`；单次调用最多触发 5 次 `tool_calls`（含嵌套）；  
- 插件调用超时默认为 10 秒，不可配置；失败后模型不会自动重试，需应用层处理；  
- `tools` 中的 `name` 必须全小写、仅含字母数字和下划线，且不能与平台保留字（如 `get_current_time`）冲突；  
- 插件返回内容受模型上下文长度限制，长响应可能被截断——建议服务端主动压缩或分页；  
- 所有插件调用日志默认记录，但敏感字段（如 `Authorization` header）会被脱敏，详情参见 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。

## 来源文档

- [插件](../../raw/application-user-guide/plug-in.md)


