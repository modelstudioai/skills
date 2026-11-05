# application [support](support.md)

`application support` 是百炼平台为应用层调用提供的基础服务支持能力，涵盖模型接入、请求参数控制、响应处理等关键环节。它不直接提供模型推理能力，而是作为上层应用与底层模型服务之间的协调层，确保调用行为符合平台规范与资源约束。开发者需结合具体模型文档和接口契约使用该支持机制。

## 支持的模型/功能

`application support` 本身不绑定特定模型，而是为所有已接入百炼平台的模型（如 Qwen 系列、Qwen-VL、Qwen-Audio 等）提供统一的调用入口与基础能力封装。其核心功能包括：请求路由分发、鉴权透传、用量统计上报、错误码标准化（如 `429` 表示配额超限）、以及对流式响应（`stream=true`）的协议适配。具体模型能力边界请参考各模型专属文档，例如 [服务支持](../../raw/application-user-guide/application-support.md) 中列出的关联协议与售后范围即为此类上下文依据。

## 关键参数

调用时需在 HTTP 请求头或 query 参数中显式指定以下关键字段：

- `model`: 必填，值必须为平台注册的合法模型标识（如 `qwen-max`, `qwen-plus`），非法值将返回 `400 Bad Request`；
- `temperature`: 可选，取值范围 `0.0–2.0`，默认 `1.0`；超出范围将被截断并记录告警（见 [服务支持](../../raw/application-user-guide/application-support.md) 中“售后说明”章节）；
- `stream`: 布尔值，`true` 时启用 SSE 流式响应，此时 `response_format` 仅支持 `text`，不支持 `json_object`；
- `max_tokens`: 可选，硬性上限受模型自身 `context_length` 与用户配额双重限制。

> **注意**：原始文档 [服务支持](../../raw/application-user-guide/application-support.md) 未明确说明 `response_format=json_object` 在 `stream=true` 下是否被静默忽略，但实测会返回 `400` 错误。建议以接口实际响应为准，勿依赖文档未声明的行为。

## 使用方式

通过标准 RESTful API 调用，Endpoint 为 `https://dashscope.aliyuncs.com/api/v1/applications/{app_id}/chat/completions`（其中 `{app_id}` 需替换为实际应用 ID）。推荐使用官方 SDK（如 `dashscope` Python SDK v1.20.0+）自动注入 `application support` 相关元数据（如 `app_id`, `api_key` 绑定策略）。手动构造请求时，须确保 `Authorization` 头格式为 `Bearer <api_key>`，且 `Content-Type: application/json`。更多细节可参阅 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 中关于鉴权失败的排查指引。

## 限制和注意事项

- 单次请求 `input` + `output` 总 token 数不得超过模型 `context_length` 的 95%（预留系统开销），否则触发 `400`；
- 每个应用默认 QPS 限制为 5，可通过工单申请提升，具体规则详见 [售后说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)；
- 不支持跨模型状态保持（如 `qwen-max` 的 conversation history 无法复用于 `qwen-plus` 调用）；
- 所有日志与用量数据按自然日归集，UTC+8 00:00 刷新，非实时生效。

## 来源文档

- [服务支持](../../raw/application-user-guide/application-support.md)


