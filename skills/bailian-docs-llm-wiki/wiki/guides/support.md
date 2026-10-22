# support

`support` 是百炼平台为开发者提供的模型服务支持能力入口，用于查询当前可用的模型、了解服务边界、获取售后保障及合规协议。该能力不直接提供推理接口，而是作为元信息枢纽，帮助用户快速定位技术文档、服务条款与问题排查路径。所有支持信息均以官方发布文档为准，建议定期查阅更新。

## 支持的模型/功能

- 当前支持的模型列表详见 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md)，涵盖通义千问系列（Qwen1、Qwen2、Qwen3）、Qwen-VL、Qwen-Audio 等开源与闭源模型，按训练阶段、输入模态和商用许可分类。
- 功能层面，`support` 提供模型能力说明、调用方式概览、输出格式约定及典型使用场景示例，但**不包含实时模型状态监控或自动故障诊断**。
- 售后服务范围（如 SLA、工单响应时效、问题分级标准）请参考 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md)。

## 关键参数

`support` 接口本身无运行时参数；其返回内容由后台静态配置驱动，依赖以下元数据字段：
- `model_id`：模型唯一标识符，与 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中定义一致；
- `support_level`：取值为 `"basic"` / `"premium"` / `"enterprise"`，对应不同售后响应等级，具体定义见 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md)；
- `eula_url`：指向最新版《用户协议》或《模型许可协议》的链接，来源为 [相关协议](../../raw/model-user-guide/support/related-agreements.md)。

> **注意**：原始文档中 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 提到“Qwen2-7B 支持[流式输出](../concepts/streaming-output.md)”，但 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 当前版本（v20240815）未标注该能力，建议以模型实际 API 文档为准，此处视为待同步信息。

## 使用方式

- 开发者无需调用 HTTP 接口，所有支持信息通过 Web 控制台「模型详情页 → 支持」Tab 或 CLI 命令 `bailian model describe --model-id <id>` 获取；
- 控制台展示内容动态拉取自 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 与 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 的结构化摘要；
- 如需程序化集成，可解析 `https://dash.aliyun.com/api/v1/models/<model-id>/support`（需认证），响应格式为 JSON，字段语义与上述关键参数一致。

## 限制和注意事项

- 不支持按地域、部署方式（公有云/专有云/VPC）筛选模型支持状态；
- 所有协议类内容（如版权归属、商用限制）以 [相关协议](../../raw/model-user-guide/support/related-agreements.md) 最终文本为准，控制台摘要不构成法律承诺；
- 模型下线通知提前 30 天通过站内信推送，但 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 中未明确下线模型的技术支持终止时间，建议在迁移计划中预留缓冲期。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


