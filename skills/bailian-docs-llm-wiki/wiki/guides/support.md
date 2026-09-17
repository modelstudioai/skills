# support

百炼平台的 `support` 接口提供模型调用过程中的基础服务支持能力，包括错误诊断、请求追踪、响应元信息返回等，主要用于调试与问题排查。该能力默认启用，无需额外配置，但部分高级功能需配合特定参数或模型版本使用。开发者应结合 [服务支持](../../raw/model-user-guide/support.md) 文档理解整体服务边界。

## 支持的模型/功能

- 所有在 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中标注为“已上线”且状态为“可用”的模型均支持基础 `support` 能力（如 `request_id` 返回、`x-bailian-trace-id` 头透传）。
- 高级支持功能（如详细错误分类码、token 级耗时分解）仅对 Qwen2.5-72B-Instruct、Qwen3-32B 及后续版本开放，旧版模型（如 Qwen1.5-7B）仅返回通用错误码。
- 流式响应中，`support` 相关元数据（如 `usage` 字段）仅在 `finish_reason == "stop"` 的 final chunk 中完整返回。

## 关键参数

| 参数名 | 类型 | 是否必需 | 说明 |
|--------|------|----------|------|
| `support_trace` | boolean | 否 | 启用后返回 `x-bailian-trace-id` 和 `x-bailian-request-id`，用于全链路追踪；默认 `false` |
| `support_debug` | boolean | 否 | 启用后在响应头中返回 `x-bailian-debug-info`（含模型加载耗时、KV cache 命中率等），仅限调试环境；生产环境禁用 |
| `support_timeout_ms` | integer | 否 | 设置支持层超时阈值（毫秒），范围 100–30000；超出将触发 `504 Gateway Timeout`，不影响模型实际执行 |

> **注意**：`support_debug` 在 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 中被明确列为“不适用于生产环境”，但 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 第 4.2 条误述为“可按需开启”。请以 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 为准。

## 使用方式

1. 发起标准 `/v1/chat/completions` 请求，在 `headers` 中添加 `X-Bailian-Support-Trace: true` 即可启用基础追踪；
2. 如需调试信息，额外添加 `X-Bailian-Support-Debug: true`（仅限非生产域名如 `dashscope.aliyuncs.com`）；
3. 解析响应头获取 `x-bailian-trace-id`，并结合 [相关协议](../../raw/model-user-guide/support/related-agreements.md) 中定义的日志保留策略进行问题定位；
4. 错误响应体中 `error.code` 字段遵循 [服务支持](../../raw/model-user-guide/support.md) 定义的统一编码规范（如 `SUPPORT_TIMEOUT`、`SUPPORT_INVALID_PARAM`）。

## 限制和注意事项

- `support_trace` 和 `support_debug` 不可同时设为 `true`，否则返回 `400 Bad Request` 并提示 `conflict_support_flags`；
- 启用 `support_debug` 将增加约 8–12ms 的额外处理延迟，且可能暴露内部部署细节，严禁在生产流量中使用；
- 所有 `support` 相关字段（含响应头与响应体）不参与计费统计，但其产生的日志存储受 [相关协议](../../raw/model-user-guide/support/related-agreements.md) 中约定的配额约束；
- 若请求中 `model` 参数指定为未在 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中登记的 ID，`support` 层将直接拦截并返回 `SUPPORT_MODEL_NOT_FOUND`，不转发至后端模型服务。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


