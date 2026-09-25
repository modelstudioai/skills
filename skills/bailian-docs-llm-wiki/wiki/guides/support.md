# support

百炼平台的 `support` 接口提供模型调用过程中的基础服务支持能力，包括错误诊断、请求追踪、响应元信息获取等，主要用于调试与可观测性场景。该能力不参与模型推理逻辑，仅在 API 层面增强请求生命周期管理。开发者需结合具体模型调用方式启用对应支持功能。

## 支持的模型/功能

- 所有通过百炼 API 调用的 [通义千问系列模型（Qwen）](../../raw/model-user-guide/support/model-studio-model-list.md) 均支持 `support` 相关元数据返回（如 `request_id`、`backend_latency`）；
- 部分模型（如 Qwen2.5-72B-Instruct）额外支持 `debug` 模式下的 token 级 trace 信息，详见 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 中“调试模式”章节；
- 不支持非百炼托管模型（如 BYOM 自定义部署模型）的 `support` 功能扩展，其元信息由用户自行实现。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `support_trace` | boolean | 否 | 启用后返回 `trace_id` 和各阶段耗时（`preprocess_ms`, `infer_ms`, `postprocess_ms`），默认 `false` |
| `support_debug` | boolean | 否 | 仅部分模型支持；启用后返回 token-level logprobs 和 attention map 摘要（需开通白名单），详见 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 第 3.2 条 |
| `support_timeout_ms` | integer | 否 | 全局超时阈值（毫秒），覆盖 `timeout` 参数，范围 100–60000 |

> **注意**：`support_debug` 在文档 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 中标注为“按需申请”，但 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 的示例中直接使用了该参数而未提示权限限制——实际调用前请确认账号已获 debug 权限，否则将返回 `403 Forbidden`。

## 使用方式

1. 在标准 `/v1/chat/completions` 请求中添加 `support_*` 参数（无需额外 endpoint）；
2. 响应头中固定包含 `X-Bailian-Request-ID` 和 `X-Bailian-Backend-Latency`；
3. 若启用 `support_trace=true`，响应体中新增 `support` 字段，结构如下：
   ```json
   "support": {
     "trace_id": "xxx",
     "stages": {
       "preprocess_ms": 12,
       "infer_ms": 345,
       "postprocess_ms": 8
     }
   }
   ```

## 限制和注意事项

- 单次请求最多启用 `support_trace` 或 `support_debug` 其中一项，同时设置将导致 `400 Bad Request`；
- `support_debug=true` 会显著增加响应体积与延迟（+200~800ms），**禁止在生产环境默认开启**；
- 所有 `support` 相关字段均不参与计费逻辑，但 trace 数据默认保留 7 天，超期自动清理；
- 若发现响应中缺失预期 `support` 字段，请检查模型是否在 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中明确标注“支持 support trace”。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


