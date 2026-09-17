# support

百炼平台的 `support` 接口提供模型调用过程中的基础服务支持能力，包括错误诊断、请求追踪、响应元信息获取等，主要用于调试与可观测性场景。该能力不参与模型推理计算，但对排查超时、鉴权失败、配额不足等问题至关重要。开发者需结合具体模型文档和协议条款使用。

## 支持的模型/功能

`support` 接口本身不绑定特定模型，但其返回的诊断信息（如 `request_id`、`error_code`、`trace_id`）与所有百炼托管模型（含 Qwen 系列、Qwen-VL、Qwen-Audio 及第三方接入模型）完全兼容。完整支持的模型清单请参阅 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md)。此外，该接口可配合 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 中定义的服务等级，用于定位是否属于 SLA 覆盖范围内的问题。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `request_id` | string | 否 | 用于关联原始请求的唯一标识；若未提供，则返回最近一次失败请求的上下文摘要 |
| `include_trace` | boolean | 否 | 默认 `false`；设为 `true` 时返回完整链路追踪路径（需具备对应权限） |
| `level` | string | 否 | 可选 `debug` / `info` / `error`；控制返回日志粒度，`debug` 级别包含输入 token 分片详情 |

> **注意**：`include_trace` 参数在 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 中被描述为“始终启用”，但实际行为受账号角色策略限制，仅 `admin` 或 `observer` 角色可获取完整 trace；普通 `developer` 角色调用时将静默降级为 `info` 级别输出。

## 使用方式

通过 HTTP POST 请求调用 `/v1/support` 端点，需携带有效的 `Authorization: Bearer <api_key>` 头。示例请求体：
```json
{
  "request_id": "req-abc123",
  "include_trace": true,
  "level": "debug"
}
```
响应为 JSON 格式，包含 `status`、`diagnosis`、`suggestions` 字段。建议在客户端异常捕获逻辑中自动触发 `support` 查询，以提升问题复现效率。

## 限制和注意事项

- 单日调用频次上限为 100 次/项目（按 `project_id` 维度计费），超出后返回 `429 Too Many Requests`；
- `request_id` 仅保留最近 7 天的有效记录，过期请求将返回空诊断；
- 所有 `support` 返回数据均受 [相关协议](../../raw/model-user-guide/support/related-agreements.md) 约束，禁止用于训练或模型逆向工程；
- 若请求中 `request_id` 对应的原始调用发生在异步批处理任务中，`support` 将无法关联子任务日志，此时需改用批处理专用诊断接口（见 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中“批量推理”章节）。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


