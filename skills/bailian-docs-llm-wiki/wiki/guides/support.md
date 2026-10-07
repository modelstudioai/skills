# support

百炼平台的 `support` 接口提供模型调用过程中的基础服务支持能力，包括错误诊断、请求追踪、响应元信息返回等，主要用于调试与问题排查。该能力默认启用，无需额外配置，但部分高级功能需配合特定参数或模型版本使用。开发者应结合 [服务支持](../../raw/model-user-guide/support.md) 文档理解整体支持范围。

## 支持的模型/功能

- 所有在 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中标注为“已上线”且状态为“可用”的模型均支持基础 `support` 能力（如 `request_id` 返回、HTTP 状态码语义化）；
- 高级支持功能（如详细错误分类码、token 级耗时分析、推理链路日志标识）仅对 Qwen2.5-72B-Instruct、Qwen3-32B 和 Qwen3-235B-A22B 等指定大模型版本开放；
- 流式响应（`stream=true`）下，`support` 会附加 `x-bailian-trace-id` 和 `x-bailian-request-id` 响应头，便于全链路追踪。

## 关键参数

| 参数名 | 类型 | 是否必需 | 说明 |
|--------|------|----------|------|
| `support.trace` | boolean | 否 | 设为 `true` 时强制启用全链路追踪（默认由平台策略自动控制）；详见 [服务支持](../../raw/model-user-guide/support.md) |
| `support.debug` | string | 否 | 可选值：`"minimal"`（默认）、`"full"`；设为 `"full"` 将在响应 `x-bailian-debug-info` 头中返回 token 分析与缓存命中详情 |
| `support.timeout_ms` | integer | 否 | 覆盖全局超时设置，单位毫秒；仅对支持该字段的模型生效（参见 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中的“支持参数”列） |

> **注意**：`support.debug=full` 在 v3.2.0+ SDK 中才被完整支持；旧版 SDK 或直接 HTTP 调用可能忽略该参数，建议同步查阅 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 中关于调试支持的时效性说明。

## 使用方式

1. 发起标准 `/v1/chat/completions` 请求，在 `headers` 中添加 `X-DashScope-Support: true`（推荐，兼容性最佳）；
2. 或在 `body` 中显式传入 `support` 对象（JSON 格式），例如：
   ```json
   {
     "model": "qwen3-32b",
     "messages": [{"role": "user", "content": "Hello"}],
     "support": {
       "trace": true,
       "debug": "full"
     }
   }
   ```
3. 成功响应中检查 `x-bailian-request-id`、`x-bailian-trace-id` 及（当启用 debug 时）`x-bailian-debug-info` 头字段。

## 限制和注意事项

- 单次请求中 `support.debug="full"` 最多返回前 100 个 token 的详细分析，超出部分不填充；
- `support.trace=true` 会轻微增加首 token 延迟（约 5–15ms），生产环境建议仅在问题复现时启用；
- 不支持在 `/v1/embeddings` 或 `/v1/rerank` 等非 chat 接口上使用 `support` 参数；
- 若响应中缺失 `x-bailian-*` 头，表明当前模型未接入新版支持框架，请核对模型是否在 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中明确标注“支持 support v2”。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


