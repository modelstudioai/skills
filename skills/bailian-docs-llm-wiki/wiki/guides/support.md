# support

百炼平台的 `support` 接口提供模型调用过程中的基础服务支持能力，包括错误诊断、请求追踪、响应元信息获取等，主要用于调试与可观测性场景。该能力不参与模型推理计算，但对排查超时、鉴权失败、配额不足等问题至关重要。开发者需结合具体模型文档和协议条款使用。

## 支持的模型/功能

`support` 接口本身不绑定特定模型，但其返回的诊断信息（如 `request_id`、`error_code`、`trace_id`）与所有百炼托管模型（含 Qwen 系列、Qwen-VL、Qwen-Audio 及第三方接入模型）完全兼容。完整支持的模型清单请参阅 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md)。此外，该接口可配合 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 中定义的服务等级，用于定位是否属于 SLA 覆盖范围内的问题。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `request_id` | string | 否 | 用于关联原始请求的唯一标识；若未提供，则返回最近一次失败请求的上下文摘要 |
| `include_trace` | boolean | 否 | 默认 `false`；设为 `true` 时返回完整链路追踪路径（需具备对应权限） |
| `level` | string | 否 | 可选 `debug` / `info` / `error`；控制返回日志粒度，仅对已记录的请求生效 |

> **注意**：`include_trace` 参数在 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 中被误标为“始终启用”，实际行为受账号权限及调用上下文限制，以当前接口文档为准。

## 使用方式

通过 HTTP POST 请求调用 `/v1/support/diagnose` 端点，Header 中需携带有效的 `Authorization: Bearer <api_key>` 和 `Content-Type: application/json`。示例请求体：
```json
{
  "request_id": "req-abc123",
  "include_trace": true,
  "level": "debug"
}
```
响应为 JSON 格式，包含 `status`、`diagnosis`、`suggestion` 字段。详细字段定义与状态码含义见 [相关协议](../../raw/model-user-guide/support/related-agreements.md) 的附录 B。

## 限制和注意事项

- 单账号每分钟最多调用 60 次 `support` 接口，超出后返回 `429 Too Many Requests`；
- `request_id` 仅保留最近 7 天内有效请求记录，过期 ID 将返回空诊断；
- 不支持跨项目（project_id）查询，`request_id` 必须属于当前认证账号下的同项目请求；
- 该接口不替代模型自身的健康检查机制，如需确认服务可用性，请直接调用目标模型的 `/health` 端点（若提供）。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


