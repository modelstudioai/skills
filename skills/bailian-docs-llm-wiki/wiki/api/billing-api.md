# billing api

Billing API 提供账单数据查询能力，支持按月汇总和按时间趋势两种视角，帮助开发者监控和分析模型服务的费用分布。当前开放两个核心接口：`GetBillingOverview` 用于获取单月账单总览（含分组聚合），`GetBillingTrend` 用于查询指定时间范围内按天或按月的费用变化趋势。所有接口均基于 RESTful 设计，需通过 HTTPS 调用，并受统一鉴权与配额控制。

## 支持的模型/功能

- **账单总览**：通过 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 获取指定月份（`billMonth`）的费用合计、税费、分组明细（如按 `MAAS_TYPE` 或 `BASE_MODEL` 聚合）。
- **账单趋势**：通过 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 查询连续时间段（`timePeriod.start` 至 `timePeriod.end`）内的费用走势，支持 `DAY` 或 `MONTH` 粒度，并返回各周期内分组费用详情。
- 两接口均支持多维度筛选（`filter.dimensions`）、语言本地化（`locale`）、地域限定（`regionId`）及空值匹配（使用 `DIMENSION_FILTER_NULL_VALUE`）。

> **注意**：文档 1 中 `GetBillingOverview` 的 `filter.dimensions.selectType` 仅列出 `IN` 和 `NOT`，但实际调用中若传入 `NOT` 且 `values` 为空数组，行为未明确定义；建议优先使用 `IN` 配合显式值列表，该限制在 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 文档中亦未补充说明，需以实测为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `billMonth`（仅 Overview） | string | 是 | 账单月份，格式 `YYYY-MM` | `"2026-08"` |
| `granularity`（仅 Trend） | string | 是 | 时间粒度：`DAY` 或 `MONTH` | `"DAY"` |
| `timePeriod`（仅 Trend） | object | 是 | 含 `start`（`YYYY-MM-DD`）和 `end`（`YYYY-MM-DD`） | `{"start":"2026-08-01","end":"2026-08-31"}` |
| `groupBy` | array<object> | 是 | 分组维度，**必须且仅能传 1 个**；`code` 值见下表 | `[{"code":"MAAS_TYPE"}]` |
| `filter.dimensions` | array<object> | 否 | 筛选条件，每个元素含 `code`、`values`、`selectType` | `[{"code":"BASE_MODEL","values":["qwen-plus"],"selectType":"IN"}]` |
| `topNum` | integer | 否 | 返回 TopN 分组数（1–20，默认 20） | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组（默认 `true`） | `false` |

**支持的维度 Code（通用）**：  
`MAAS_TYPE`, `BASE_MODEL`, `API_KEY_ID`, `WORKSPACE_ID`, `FEE_TYPE`, `CHARGE_TYPE`, `BUSINESS_REGION`, `SERVICE_SITE`, `ARTICLE_CODE`。所有维度均支持 `DIMENSION_FILTER_NULL_VALUE` 表示匹配空值。

## 使用方式

1. **认证**：请求需携带有效的 `Authorization` 头（如 Bearer [Token](../concepts/token.md)），具体鉴权方式参见平台通用认证文档。
2. **构造请求**：
   - 总览：`GET /modelstudio/billing/overview?billMonth=2026-08&groupBy[0].code=MAAS_TYPE&locale=zh-CN`
   - 趋势：`GET /modelstudio/billing/trend?granularity=DAY&timePeriod.start=2026-08-01&timePeriod.end=2026-08-31&groupBy[0].code=BASE_MODEL`
3. **响应解析**：
   - 成功时 `success: true`，费用金额均为字符串类型（含两位小数），需转为数值处理；
   - `data.groups`（Overview）和 `data.resultByTime`（Trend）按金额降序排列，`percentage` 为相对占比（非百分比整数）。

## 限制和注意事项

- **时间范围限制**：`GetBillingTrend` 的 `timePeriod.end` 不能晚于当前日期，且 `end - start` 最大跨度为 90 天（`DAY` 粒度）或 24 个月（`MONTH` 粒度）。
- **分组约束**：两接口均强制要求 `groupBy` 数组长度为 1，传入多个元素将返回参数错误；`filter.dimensions` 中同一 `code` 不可重复出现。
- **币种差异**：`GetBillingOverview` 示例返回 `USD`，而 `GetBillingTrend` 示例返回 `CNY`；实际币种由账户结算货币决定，接口不支持跨币种转换。
- **空值处理**：当 `filter.dimensions.values` 包含 `DIMENSION_FILTER_NULL_VALUE` 时，匹配数据库中该字段为 `NULL` 或空字符串的记录，此行为在两篇原始文档中定义一致。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


