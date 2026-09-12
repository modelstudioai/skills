# plug in

插件（Plug-in）是百炼平台提供的扩展能力机制，允许模型调用外部工具或服务以增强其功能边界，例如访问实时数据、执行计算或与业务系统集成。插件通过标准化协议（如 OpenAPI 描述）注册并被大模型理解与调度，支持在推理过程中动态触发。该能力已在多个主流模型中集成，但具体行为受模型版本和部署配置影响。

## 支持的模型/功能

当前支持插件调用的模型包括：Qwen-Max、Qwen-Plus 和 Qwen-Turbo（v202409 及之后版本）。基础版 Qwen1.5 系列模型默认不启用插件能力，需显式配置 `enable_plugins: true` 并使用兼容的 tokenizer 与 [prompt](prompt.md) template。插件功能涵盖 HTTP 工具调用、异步任务回调、多步骤编排等，详细能力清单见 [插件概述](../../raw/application-user-guide/plug-in.md)。注意：部分旧版文档中提及的“Qwen-VL 支持图像插件”已过时，实际该模型未实现插件调度逻辑，> **注意**：请以 [官方和第三方插件](../../raw/application-user-guide/plug-in.md) 中最新列表为准。

## 关键参数

- `plugins`: 字符串数组，指定启用的插件 ID（如 `["weather-api", "db-query"]`），必须预先在控制台注册；
- `plugin_selection_strategy`: 可选值为 `"auto"`（默认，由模型自主选择）或 `"explicit"`（需在用户 query 中显式声明插件名）；
- `plugin_timeout_ms`: 单次插件调用超时，默认 10000（10 秒），最大支持 30000；
- `enable_plugins`: 布尔值，必须设为 `true` 才能激活插件调度器，否则忽略 `plugins` 字段。  
完整参数说明参见 [自定义插件](../../raw/application-user-guide/plug-in.md) 文档中的配置章节。

## 使用方式

1. 在百炼控制台「插件管理」中上传 OpenAPI 3.0 YAML 文件完成注册；
2. 创建应用或调用 API 时，在请求体中传入 `plugins` 和 `enable_plugins: true`；
3. 对于 `plugin_selection_strategy: "explicit"` 模式，用户输入需包含类似 `请调用天气插件查询北京今日温度` 的明确指令；
4. 插件返回结果将自动注入模型上下文，参与后续生成。调试建议开启 `debug: true` 查看插件调度日志。

## 限制和注意事项

- 单次请求最多启用 5 个插件，且总并发调用数不超过 3；
- 插件响应体大小上限为 2MB，超限将被截断并记录 warning；
- 不支持跨域 Cookie 或需要浏览器环境的前端插件（如支付 SDK）；
- 插件函数签名变更后，必须重新注册并更新应用绑定，否则调用失败；  
> **注意**：若发现插件返回 `403 Forbidden` 但权限配置无误，可能是模型服务侧缓存了旧版插件 schema，此时需强制刷新插件元数据——操作路径见 [插件概述](../../raw/application-user-guide/plug-in.md) 中的“刷新机制”小节。

## 来源文档

- [插件](../../raw/application-user-guide/plug-in.md)


