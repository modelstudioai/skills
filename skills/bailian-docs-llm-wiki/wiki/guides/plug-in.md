# plug in

插件（Plug-in）是百炼平台提供的扩展能力机制，允许用户在不修改模型底层逻辑的前提下，动态接入外部服务、工具或知识源，增强大模型的推理与执行能力。插件通过标准化协议与模型交互，支持同步调用与异步回调两种模式。其设计目标是解耦模型能力与业务逻辑，提升应用构建灵活性。

## 支持的模型/功能

当前仅 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款 Qwen 系列模型原生支持插件调用；其他模型（如 `qwen2-72b` 或第三方模型）暂不支持，调用将被静默忽略。插件可实现的功能包括：实时数据查询（如天气、股票）、系统操作（如发送邮件、创建日程）、知识增强（如检索私有文档库）等。详细插件能力清单见 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。

## 关键参数

启用插件需在请求中显式配置以下字段：
- `plugins`: JSON 数组，每个元素为 `{ "name": "plugin_id", "args": { ... } }`，`plugin_id` 必须已在控制台启用；
- `enable_plugins`: 布尔值，设为 `true` 才触发插件调度（即使 `plugins` 非空，此字段为 `false` 时仍禁用）；
- `plugin_timeout_ms`: 可选，单位毫秒，默认 `10000`（10 秒），超时后自动降级为无插件响应。  
参数语义与校验规则详见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。

## 使用方式

1. 在百炼控制台「插件管理」中启用所需插件（官方插件开箱即用，第三方插件需授权）；  
2. 构造 API 请求，在 `messages` 后追加 `plugins` 和 `enable_plugins` 字段；  
3. 发送请求，平台自动完成插件发现、参数校验、调用与结果注入。  
自定义插件的注册与调试流程请参考 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

## 限制和注意事项

- 单次请求最多指定 3 个插件；超过部分将被截断且不报错；  
- 插件调用链深度限制为 1 层（即插件不可再调用其他插件）；  
- 若插件返回非 JSON 格式响应或 HTTP 状态码非 `200`，平台将返回 `plugin_execution_failed` 错误；  
> **注意**：原始文档中 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md) 提到“支持插件嵌套调用”，但该描述已过时——自 v2.3.0 起，嵌套调用已被移除，实际行为以本节为准。  
- 插件输入参数 `args` 中的敏感字段（如 `api_key`）不会被日志记录，但需确保插件服务端自行做好鉴权。

## 来源文档

- [插件](../../raw/application-user-guide/plug-in.md)


