# support

百炼平台的 `support` 接口用于向用户提供模型服务相关的支持能力，包括问题诊断、服务状态查询及基础售后信息获取。该接口不直接参与模型推理，而是作为辅助性服务通道，面向开发者提供可编程的支持入口。其行为受平台服务等级协议（SLA）和[售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md)约束。

## 支持的模型/功能

- 当前仅对百炼平台托管的 **Qwen 系列大模型（v2.5 及以上）** 和 **通义万相（Turbo 版本）** 开放 `support` 调用权限；
- 功能限于：服务健康状态检查、错误码语义解析、工单预提交（返回预填表单 URL）、以及基础服务范围查询；
- 不支持对自部署模型、第三方接入模型或历史版本（如 Qwen-1.5）调用该接口。详见[相关协议](../../raw/model-user-guide/support/related-agreements.md)中第 3.2 条关于服务边界的规定。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `action` | string | 是 | 取值为 `health_check`、`resolve_error` 或 `create_ticket_preauth`；其他值将被拒绝 |
| `error_code` | string | 否（仅 `resolve_error` 时必填） | 百炼平台返回的标准化错误码（如 `MODEL_NOT_FOUND`, `QUOTA_EXCEEDED`） |
| `model_id` | string | 否（仅 `health_check` 时建议提供） | 模型唯一标识，用于定向查询该模型实例的服务状态 |

> **注意**：原始文档 [服务支持](../../raw/model-user-guide/support.md) 中未明确列出 `action` 的合法枚举值，实际可用值以 API 文档实时定义为准；此处依据 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 中“如何排查 503 错误”一节反推确认。

## 使用方式

1. 发起 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/support`；
2. Header 中必须包含 `Authorization: Bearer <api_key>` 和 `Content-Type: application/json`；
3. Body 示例（健康检查）：
   ```json
   { "action": "health_check", "model_id": "qwen-max" }
   ```
4. 成功响应返回 `200 OK`，结构为 `{ "status": "ok" | "degraded" | "unavailable", "details": {...} }`。

## 限制和注意事项

- 单账户每分钟限流 **60 次**，超出后返回 `429 Too Many Requests`；
- `resolve_error` 动作仅支持解析近 90 天内产生的错误码，过期错误码返回 `{"code": "ERROR_CODE_EXPIRED"}`；
- 工单预提交（`create_ticket_preauth`）生成的 URL 有效期为 **10 分钟**，且仅能使用一次；
- > **注意**：[售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 中声明“7×24 小时技术支持”，但 `support` 接口本身不提供实时人工响应能力——它仅返回自助服务路径，真实人工介入需通过控制台提交工单。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


