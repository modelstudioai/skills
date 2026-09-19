# support

`support` 是百炼平台为模型调用和服务稳定性提供的基础支持能力，涵盖模型兼容性、服务保障范围、售后响应机制等关键维度。开发者可通过该能力了解所用模型的服务等级、可用功能边界及问题反馈路径。所有支持策略均以 [服务支持](../../raw/model-user-guide/support.md) 为准。

## 支持的模型/功能

- 当前支持的模型列表详见 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md)，该文档按模型类型（如文本生成、[多模态](../concepts/multimodal.md)、嵌入）和上线状态（GA / Beta）分类维护。
- 功能层面，`support` 覆盖 API 调用、流式响应、[异步任务](../concepts/asynchronous-task.md)提交等核心交互方式；但不包含私有化部署场景下的本地运维支持，后者需参考 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 中明确界定的服务范围。
- > **注意**：[模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中标注为 “Beta” 的模型，其 `support` 级别低于 GA 模型，例如不承诺 SLA，且故障响应时效延长至 4 小时（GA 模型为 30 分钟）。

## 关键参数

- `support_level`：枚举值，取值为 `"ga"`、`"beta"` 或 `"deprecated"`，直接关联模型在 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中的状态字段。
- `response_time_sla`：仅对 `support_level = "ga"` 的模型生效，定义 P95 延迟上限（单位：秒），具体数值见各模型详情页。
- `fallback_enabled`：布尔值，表示当主服务不可用时是否自动切换至备用节点（默认 `true`，仅 GA 模型支持）。

## 使用方式

- 在调用模型 API 时，无需显式传入 `support` 相关参数；平台根据所选模型 ID 自动匹配对应支持策略。
- 开发者可通过 `/v1/models/{model_id}` 接口获取模型元信息，其中 `support_level` 和 `response_time_sla` 字段即来自 [服务支持](../../raw/model-user-guide/support.md) 的统一配置。
- 问题上报必须通过控制台「工单系统」提交，并在标题中注明模型 ID 与 `support_level`，以便路由至对应支持队列。

## 限制和注意事项

- `support` 不覆盖模型微调训练过程中的调试支持，该部分归属 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 中的“开发调试”章节。
- 所有 `support_level = "deprecated"` 的模型自下线公告发布起 30 天内仅提供只读访问与错误咨询，不再接受新工单（参见 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md)）。
- > **注意**：[相关协议](../../raw/model-user-guide/support/related-agreements.md) 中关于数据隐私的条款优先级高于本页描述，若发生冲突，以协议原文为准。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


