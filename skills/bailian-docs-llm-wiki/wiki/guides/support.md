# support

`support` 是百炼平台为模型调用和管理提供的基础服务支持能力，涵盖模型可用性、功能边界、参数配置及售后保障等维度。开发者可通过该服务确认所选模型是否受支持、了解调用限制，并获取故障响应与服务范围说明。所有支持信息均以官方文档为准，建议结合具体模型文档交叉验证。

## 支持的模型/功能

当前支持的模型列表详见 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md)，该文档按模型类型（如大语言模型、多模态模型）、部署形态（API / SDK / 控制台）及地域可用性分类维护。功能支持范围包括同步推理、流式响应、批量调用及部分模型的微调后服务接入。注意：部分新上线模型可能尚未同步至该列表，需同时参考对应模型的独立文档，例如 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 中提及的“Qwen-VL-Plus 在杭州地域暂未开放 API 调用”即属此类临时限制。

> **注意**：[模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中标注“已下线”的模型，其 SDK 接口仍可能短暂返回 200，但实际不执行推理；此行为与 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 中“服务不可用即视为故障”的定义存在不一致，建议以控制台实时状态为准。

## 关键参数

调用支持相关接口（如 `/v1/models` 或控制台健康检查端点）时，关键参数包括：
- `region_id`：必需，指定服务地域（如 `cn-hangzhou`），影响模型可用性；
- `with_details`：布尔值，设为 `true` 可返回模型版本、计费模式及 SLA 承诺；
- `status_filter`：可选，支持 `active` / `deprecated` / `offline` 过滤。

参数语义与约束详见 [相关协议](../../raw/model-user-guide/support/related-agreements.md) 的附录 B “API 元数据规范”。

## 使用方式

- **查询支持模型**：调用 `GET /v1/models?region_id=cn-hangzhou` 获取当前地域可用模型清单；
- **验证服务状态**：向任意模型 endpoint 发送空 body 的 `HEAD` 请求，响应头 `X-Service-Status: ok` 表示服务就绪；
- **获取支持策略**：查阅 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 明确故障响应时效（P1 级 30 分钟）、补偿规则及免责情形。

## 限制和注意事项

- 单账号默认最多并发调用 50 个不同模型实例，超出需提工单申请配额；
- 模型服务地域隔离严格，跨 region 调用将返回 `404 Not Found`（而非重定向），请勿依赖 DNS 或网关自动路由；
- [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 中“如何切换免费试用额度”一节已过时：自 2024 年 7 月起，试用额度统一通过「资源包」管理，原控制台开关入口已下线。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


