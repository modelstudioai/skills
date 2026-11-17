# billing api

Billing API 提供账单数据查询能力，支持按月获取费用总览（`GetBillingOverview`）和按时间范围获取费用趋势（`GetBillingTrend`）。所有接口均基于 RESTful 设计，通过 HTTPS 调用，返回结构化 JSON 数据。开发者可利用分组、筛选、多语言等参数灵活定制查询结果，适用于成本分析、用量监控与财务对账等场景。

## 支持的模型/功能

Billing API 当前提供两个核心能力：

- `GetBillingOverview`：查询**单个月份**的账单总览，返回按指定维度聚合的 TopN 分组及金额占比，适用于月度成本快照分析。详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)。
- `GetBillingTrend`：查询**连续时间范围**（支持 DAY 或 MONTH 粒度）的账单趋势，返回分周期费用明细及分组汇总，适用于用量波动监测与趋势归因。详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)。

> **注意**：两文档均声明 `groupBy` 必须且只能传入一个维度，但未明确禁止嵌套或复合分组；实际调用中若传入多个 `groupBy` 元素，将被服务端拒绝（返回 400 错误），该行为与文档描述一致，无需额外兼容。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `billMonth`（仅 `GetBillingOverview`） | string | 是 | 账单月份，格式 `YYYY-MM` | `2026-08` |
| `granularity`（仅 `GetBillingTrend`） | string | 是 | 时间粒度：`DAY` 或 `MONTH` | `DAY` |
| `timePeriod.start` / `.end`（仅 `GetBillingTrend`） | string | 是 | 查询起止日期，格式 `YYYY-MM-DD` | `2026-08-01`, `2026-08-31` |
| `groupBy[].code` | string | 是 | 分组维度 Code，**必须且仅一个**。支持值：`MAAS_TYPE`, `BASE_MODEL`, `API_KEY_ID`, `WORKSPACE_ID`, `FEE_TYPE`, `CHARGE_TYPE`, `BUSINESS_REGION`, `SERVICE_SITE`, `ARTICLE_CODE` | `BASE_MODEL` |
| `filter.dimensions` | array<object> | 否 | 维度过滤条件，结构同 `groupBy`，支持 `IN`/`NOT` 语义 | `[{"code": "BASE_MODEL", "values": ["qwen-plus"], "selectType": "IN"}]` |
| `topNum` | integer | 否 | 返回 TopN 分组数（1–20），默认 20；超出部分在 `GetBillingTrend` 中合并为“其他” | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组，默认 `true` | `false` |
| `locale` | string | 否 | 返回语言：`zh-CN`（中文）或 `en-US`（英文），影响 `name` 字段展示 | `zh-CN` |

> **注意**：`filter.dimensions[].values` 可传特殊值 `DIMENSION_FILTER_NULL_VALUE` 表示匹配 NULL 或空字符串字段，该能力在两篇原始文档中定义完全一致，已在 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 和 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 中明确说明。

## 使用方式

1. **认证**：所有请求需携带有效的 Bearer [Token](../concepts/token.md)（通过百炼平台 AccessKey 获取），并设置 `Authorization: Bearer <token>` 请求头。
2. **Endpoint**：
   - `GET /modelstudio/billing/overview`（`GetBillingOverview`）
   - `GET /modelstudio/billing/trend`（`GetBillingTrend`）
3. **构造请求**：按需拼接查询参数（如 `?billMonth=2026-08&groupBy[0].code=MAAS_TYPE&locale=zh-CN`），**不支持 POST body 传参**。
4. **解析响应**：
   - 共同字段：`requestId`, `code`, `success`, `message`, `data`
   - `GetBillingOverview` 主要关注 `data.groups[]`（分组列表）和 `data.totalAmount`
   - `GetBillingTrend` 主要关注 `data.resultByTime[]`（时间序列）、`data.groupByTotal[]`（分组汇总）和 `data.costTotals`

## 限制和注意事项

- **时间范围限制**：`GetBillingTrend` 的 `timePeriod.end` 不能晚于当前日期；`timePeriod.start` 到 `end` 最大跨度为 90 天（`granularity=DAY`）或 24 个月（`granularity=MONTH`）。
- **分组约束**：`groupBy` 严格限定为单维度，传入多个元素将导致请求失败；`filter.dimensions` 同理，不支持跨维度联合筛选（如同时按 `BASE_MODEL` 和 `REGION_ID` 筛选）。
- **金额精度**：所有金额字段（如 `amount`, `pretaxAmount`）均为字符串类型，保留两位小数，**不可直接转 number 运算**，避免浮点误差。
- **空值处理**：当分组值为空时，`key` 字段返回 `DIMENSION_FILTER_NULL_VALUE`，`name` 字段返回 `-`（`locale=zh-CN`）或 `-`（`locale=en-US`），需在前端做显式判断。
- **地域与站点**：`regionId` 和 `SERVICE_SITE` 参数作用于数据过滤范围，但文档未说明其是否影响计费币种；实践中 `currency` 字段由账单实际结算币种决定，与 `regionId` 无强绑定关系。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


