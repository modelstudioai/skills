# support

百炼平台的 `support` 接口提供模型调用过程中的基础服务支持能力，包括错误诊断、请求追踪、响应元信息返回等，用于辅助开发者快速定位问题和优化集成逻辑。该能力默认启用，无需额外配置，但部分高级功能依赖特定模型或参数控制。所有行为均遵循 [相关协议](raw/model-user-guide/support/related-agreements.md) 中的服务条款。

## 支持的模型/功能

- 当前仅 **Qwen 系列（Qwen1.5、Qwen2、Qwen2.5）及 Qwen-VL** 支持完整的 `support` 元数据返回（如 `request_id`、`backend_latency`、`model_version`）；其他模型可能仅返回基础错误码。
- 错误分类与建议修复动作由统一错误引擎驱动，覆盖 4xx/5xx 响应及超时、限流、鉴权失败等场景，详情见 [售后说明](raw/model-user-guide/support/after-sales-service-scope.md)。
- 模型列表持续更新，最新支持情况请以 [模型列表](raw/model-user-guide/support/model-studio-model-list.md) 为准。

## 关键参数

| 参数名 | 类型 | 是否必需 | 说明 |
|--------|------|----------|------|
| `enable_support_trace` | boolean | 否 | 设为 `true` 时在响应头中返回 `X-Bailian-Trace-ID`，用于全链路日志关联；默认 `false` |
| `support_level` | string | 否 | 可选 `basic`（默认）、`detailed`；`detailed` 将在响应体 `support_info` 字段中返回后端延迟、节点信息等调试数据 |
| `support_timeout_ms` | integer | 否 | 仅当 `support_level=detailed` 时生效，指定支持模块自身超时阈值（单位 ms），范围 100–5000 |

> **注意**：`support_timeout_ms` 在 [常见问题](raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 中被错误描述为“影响模型推理总耗时”，实际仅约束支持模块内部诊断逻辑，不影响主推理流程。

## 使用方式

1. 在标准 `/v1/chat/completions` 或 `/v1/models/{model}/invoke` 请求中，于 `body` 添加 `support` 对象：
   ```json
   {
     "messages": [...],
     "support": {
       "enable_support_trace": true,
       "support_level": "detailed"
     }
   }
   ```
2. 成功响应中，`support_info` 字段（`detailed` 模式下）包含 `backend_latency_ms`、`backend_region`、`model_commit_id` 等字段；
3. 所有 `support` 相关字段均通过响应头 `X-Bailian-Support-*` 透出，例如 `X-Bailian-Support-Request-ID`。

## 限制和注意事项

- `support_level=detailed` 会轻微增加响应延迟（通常 <15ms），生产环境建议仅在问题排查期启用；
- `enable_support_trace=true` 时，Trace ID 有效期为 7 天，日志需通过百炼控制台「运维中心 → 日志查询」检索；
- 不支持在流式响应（`stream=true`）中返回 `support_info` 字段，此时仅响应头携带基础支持信息；
- [售后说明](raw/model-user-guide/support/after-sales-service-scope.md) 明确指出：`support` 接口本身不构成 SLA 保障项，其输出仅供参考，不可作为服务可用性判定依据。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


