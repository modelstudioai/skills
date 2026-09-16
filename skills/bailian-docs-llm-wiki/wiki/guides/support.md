# support

百炼平台的 `support` 接口提供模型调用过程中的基础服务支持能力，包括错误诊断、请求追踪、响应元信息返回等，主要用于调试与问题排查。该能力默认启用，无需额外配置，但部分高级功能需配合特定参数或模型版本使用。开发者应结合 [服务支持](../../raw/model-user-guide/support.md) 文档理解整体支持范围。

## 支持的模型/功能

- 所有在 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中标注为“已上线”且状态为“可用”的模型均支持基础错误码返回与 request_id 透传；
- 部分模型（如 qwen-max、qwen-plus）支持增强型诊断信息，包括 token 使用详情、推理阶段耗时分解、缓存命中状态等；
- 不支持对非百炼托管模型（如 BYOM 自定义后端）启用自动重试、熔断或自动降级等服务治理功能。

## 关键参数

| 参数名 | 类型 | 是否必需 | 说明 |
|--------|------|----------|------|
| `request_id` | string | 否 | 用于链路追踪，若未提供则由服务端自动生成并返回于响应头 `X-Request-ID` 中；建议客户端显式传入以对齐日志体系 |
| `debug` | boolean | 否 | 设为 `true` 时返回完整推理中间状态（仅限测试环境，生产环境强制忽略）；详见 [服务支持](../../raw/model-user-guide/support.md) 中的调试策略说明 |
| `trace_enabled` | boolean | 否 | 启用全链路追踪（需已接入阿里云 SLS），返回 `trace_id` 字段；该参数在 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 中明确列为付费支持项 |

> **注意**：原始文档 [服务支持](../../raw/model-user-guide/support.md) 中提及 `debug=true` 在生产环境“可能生效”，但实际行为已统一为强制忽略——此为文档过时，以当前 API 实际响应为准。

## 使用方式

1. 发起标准 `/v1/chat/completions` 或 `/v1/embeddings` 请求时，在请求体或 query 参数中添加上述支持的参数；
2. 检查响应头中的 `X-Request-ID` 和（当 `trace_enabled=true` 时）响应体中的 `trace_id`，用于问题定位；
3. 解析响应体中 `usage` 字段（含 `prompt_tokens`, `completion_tokens`, `total_tokens`, `cache_hit_tokens`）以评估成本与缓存效率；
4. 若收到非 2xx 响应，参考 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 中的错误码映射表进行归因。

## 限制和注意事项

- 单次请求的 `request_id` 长度不得超过 64 字符，且仅允许字母、数字、连字符（`-`）和下划线（`_`），否则将被拒绝；
- `debug=true` 仅在百炼控制台开启“调试模式”的项目中生效，普通 API Key 调用始终无效；
- 增强诊断信息（如缓存命中详情）不适用于流式响应（`stream=true`），此时仅返回聚合后的 `usage`；
- 所有支持能力均受 [相关协议](../../raw/model-user-guide/support/related-agreements.md) 约束，特别是数据留存与审计日志条款。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


