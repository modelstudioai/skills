# support

百炼平台的 `support` 模块提供模型调用过程中的基础服务支持能力，包括模型可用性查询、错误诊断辅助、服务范围界定及售后响应机制。开发者可通过该模块快速确认所用模型是否在官方支持范围内，并获取与服务等级、协议约束和问题排查相关的权威信息。所有支持策略均以 [服务支持](../../raw/model-user-guide/support.md) 文档为基准。

## 支持的模型/功能

- 官方支持的模型列表详见 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md)，该列表按模型类型（如文本生成、多模态、嵌入）和上线状态（GA / Beta / Deprecated）分类，**每季度更新一次**。
- 支持的功能包括：模型健康状态查询（`/v1/models/{model_id}/health`）、错误码语义映射（如 `429` 对应配额超限而非模型不可用）、以及基础服务 SLA 查询（仅限 GA 模型）。
- > **注意**：[模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中标注为 `Beta` 的模型不提供 7×24 小时技术支持，其错误响应可能包含实验性字段，与 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 中定义的服务范围不一致。

## 关键参数

- `model_id`：必需，必须严格匹配 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中公布的 ID（区分大小写，含版本后缀如 `-v1`）。
- `timeout_ms`：可选，默认 30000（30 秒），若设为 `0` 则使用服务端默认超时；超过 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 承诺的 P99 延迟阈值时，不触发自动重试。
- `trace_id`：建议提供，用于关联日志与工单，格式需符合 RFC 7231，否则 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 中的诊断工具将无法准确定位。

## 使用方式

- 通过 HTTP GET 请求 `/v1/support/models/{model_id}` 可获取该模型当前支持状态、维护窗口及最近变更摘要。
- 错误响应体中若含 `support_link` 字段，其值为指向 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 对应章节的绝对 URL，开发者应优先查阅该链接内容再提工单。
- 所有支持接口均要求 `Authorization: Bearer <api_key>`，且 `api_key` 必须具备 `model:read` 权限，否则返回 `403 Forbidden` 并附带指向 [相关协议](../../raw/model-user-guide/support/related-agreements.md) 第 3.2 条的提示。

## 限制和注意事项

- 单账户每分钟最多调用支持接口 60 次，超出后返回 `429 Too Many Requests`，**不计入配额消耗**，但会触发风控临时限流（持续 5 分钟）。
- 不支持跨地域查询：请求必须发往与目标模型部署区域一致的 endpoint（如杭州模型需调用 `dashscope.aliyuncs.com` 而非 `dashscope.cn-shanghai.aliyuncs.com`）。
- > **注意**：[售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 中声明“模型输出质量不属支持范围”，但 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 第 4.7 条明确列出可申诉的典型质量缺陷场景（如系统性 token 截断、重复输出），二者存在解释差异，以 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 为准。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


