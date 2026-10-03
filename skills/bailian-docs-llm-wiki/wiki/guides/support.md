# support

百炼平台的 `support` 模块提供模型调用过程中的基础服务保障能力，包括模型可用性说明、售后响应机制及合规协议支持。开发者可通过该模块确认所选模型是否在官方支持范围内，并了解服务边界与响应时效。所有支持策略均以 [服务支持](../../raw/model-user-guide/support.md) 文档为权威依据。

## 支持的模型/功能

- 当前支持的模型列表详见 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md)，该列表按模型类型（如文本生成、多模态、Embedding）和上线状态（GA / Beta）分类，每日自动同步生产环境实际可用模型。
- 功能层面，`support` 覆盖模型调用异常诊断、配额超限告警、基础错误码解释（如 `429`, `503`），但**不包含**模型微调过程中的训练失败归因或私有化部署的硬件兼容性排查。
- 所有已上线模型均默认启用基础服务支持；Beta 模型的支持范围参见 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 中的分级定义。

## 关键参数

- `support_level`：请求头中可选字段，取值为 `"basic"`（默认）或 `"premium"`，仅对开通企业版且完成实名认证的账号生效，影响 SLA 响应时长（详见 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md)）。
- `trace_id`：强烈建议在每次调用中透传唯一 trace ID，用于故障定界；缺失时将降低问题复现与日志关联效率。
- 无专用 API endpoint，支持能力通过统一 `/v1/chat/completions` 等主接口隐式承载，不需额外鉴权或路由切换。

## 使用方式

- 开发者无需主动调用独立 `support` 接口，所有支持能力内嵌于标准模型调用链路中：
  - 错误响应体中自动携带 `support_ticket_id`（当 HTTP 状态码 ≥ 400 且非客户端参数错误时）；
  - 控制台「调用监控」页可基于 `trace_id` 或 `support_ticket_id` 查看完整服务侧诊断日志；
  - 如需人工介入，须凭 `support_ticket_id` 在工单系统提交，系统自动关联原始请求上下文。

## 限制和注意事项

- 单个 `support_ticket_id` 仅保留 30 天，超期后无法检索原始诊断数据。
- 免费试用账号仅享 `basic` 支持等级，响应时效为 5 个工作日；企业版账号需显式设置 `support_level=premium` 并确保账户状态有效。
> **注意**：[模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中标注为 “Beta” 的模型，其 `premium` 支持等级在部分区域（如金融云）暂未开通，实际服务能力以控制台实时提示为准，与 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 中的全局描述存在临时性差异。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


