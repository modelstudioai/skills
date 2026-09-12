# billing api

billing api 是百炼平台提供的账单查询服务接口，用于获取模型调用产生的费用概览与趋势数据。开发者可通过该 API 实时监控资源消耗和成本分布，适用于财务对账、预算控制及用量分析等场景。所有接口均需通过阿里云统一身份认证（STS [Token](../concepts/token.md) 或 AccessKey）调用。

## 支持的模型/功能

billing api 不直接关联具体大模型（如 Qwen 系列），而是面向整个 Model Studio 计费体系提供通用账单能力，当前支持两类核心功能：
- `GetBillingOverview`：返回指定周期内（默认最近30天）的总费用、调用次数、[Token](../concepts/token.md) 消耗量等聚合指标；
- `GetBillingTrend`：按日/周/月粒度返回费用与用量的时间序列趋势，支持多维度分组（如按模型、项目、地域）。

> **注意**：原始文档中未明确说明是否支持按模型 ID 维度过滤，但 [查询账单概览](https://help.aliyun.com/zh/model-studio/api-modelstudio-2026-02-10-getbillingoverview) 接口实际支持 `model_id` 参数；该能力在 [原文标题](../../raw/model-api-reference/billing-api.md) 中未体现，建议以 OpenAPI 文档为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `StartTime` | string (ISO8601) | 是 | 查询起始时间，精度到秒，最多支持90天跨度 |
| `EndTime` | string (ISO8601) | 是 | 查询结束时间，需晚于 `StartTime` |
| `Granularity` | string | 否 | 趋势类接口专用，取值 `DAY` / `WEEK` / `MONTH`；默认 `DAY` |
| `GroupBy` | string | 否 | 分组维度，如 `model_id`, `project_id`, `region_id`；详见 [原文标题](../../raw/model-api-reference/billing-api.md) 中的官方示例 |

## 使用方式

1. 调用前确保已开通 Model Studio 服务并具备 `bss:Describe*` 权限；
2. 构造 HTTPS 请求，Endpoint 为 `https://modelstudio.aliyuncs.com`，Action 为 `GetBillingOverview` 或 `GetBillingTrend`；
3. 所有请求必须携带签名（Signature）和公共请求参数（如 `Version=2026-02-10`, `RegionId=cn-shanghai`）；
4. 响应体为 JSON，含 `Data` 字段（结构化账单数据）和 `RequestId`（用于问题排查）；完整字段定义请参考 [原文标题](../../raw/model-api-reference/billing-api.md)。

## 限制和注意事项

- 单次查询时间跨度不得超过90天；
- `GetBillingTrend` 最多返回365条趋势记录，超出部分自动截断；
- 账单数据存在约2小时延迟，非实时计费结果；
- 免费调用额度不计入账单 API 返回的 `TotalAmount`，仅反映已扣费金额；
- 若发现 `model_id` 过滤行为与 [原文标题](../../raw/model-api-reference/billing-api.md) 描述不一致，请优先以 [查询账单概览](https://help.aliyun.com/zh/model-studio/api-modelstudio-2026-02-10-getbillingoverview) 官方文档为准。

## 来源文档

- [账单](../../raw/model-api-reference/billing-api.md)


