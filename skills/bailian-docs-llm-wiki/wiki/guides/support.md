# support

`support` 是百炼平台为开发者提供的模型服务支持能力入口，用于查询当前可用的模型列表、了解服务范围、获取售后保障及合规协议等关键信息。该能力不直接参与推理调用，而是作为服务元数据与支持策略的统一出口。所有支持信息均以平台最新控制台和文档为准。

## 支持的模型/功能

- 当前支持的模型列表详见 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md)，涵盖通义千问系列（Qwen）、语音、[多模态](../concepts/multi-modal.md)等全类型模型。
- 支持按场景（如文本生成、代码补全、图像理解）和服务形态（API、SDK、Web 控制台）分类检索模型能力。
- 除模型本身外，还提供配套的调试工具、用量监控、错误码说明等辅助功能，具体参见 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。

## 关键参数

- `model_id`：必需，用于唯一标识模型（如 `qwen-max`, `qwen-plus`），必须与 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中公布的 ID 完全一致。
- `region_id`：可选，指定服务地域（如 `cn-beijing`），影响 SLA 和数据驻留策略；未指定时默认使用账号所属主地域。
- `support_level`：仅限企业版客户调用，用于查询专属支持等级（L1–L3），需配合工单系统使用。

## 使用方式

- 控制台路径：进入「模型服务」→「支持中心」→「模型能力概览」，可实时筛选、导出模型清单。
- API 查询：调用 `GET /v1/support/models`（需携带有效 AccessKey），返回 JSON 格式模型元数据，字段含义与 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 文档严格对齐。
- 工单提交：通过控制台右上角「帮助与支持」入口提交技术咨询或售后请求，响应时效依 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 执行。

## 限制和注意事项

- 模型列表每小时自动同步一次，控制台显示可能有最多 60 分钟延迟；若发现 API 返回与 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 文档不一致，请以文档为准并刷新缓存。
- 免费试用模型不享受 SLA 保障，其可用性、性能指标及故障响应不适用 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 中定义的服务等级。
> **注意**：原始文档中 [相关协议](../../raw/model-user-guide/support/related-agreements.md) 提到“模型调用即视为接受全部服务条款”，但最新《百炼平台服务协议（2024 版）》第 3.2 条明确限定该条款仅适用于已开通付费服务的账号——请开发者务必确认自身账户状态，避免误读法律效力。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


