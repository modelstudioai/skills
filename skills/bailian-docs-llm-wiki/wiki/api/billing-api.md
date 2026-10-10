# billing api

Billing API 提供账单数据查询能力，支持按月获取费用总览（`GetBillingOverview`）和按时间范围获取费用趋势（`GetBillingTrend`）。所有接口均基于 RESTful 设计，通过 HTTPS 调用，返回结构化 JSON 响应。该 API 适用于开发者集成至内部财务看板、成本分析工具或自动化对账系统。

## 支持的模型/功能

- `GetBillingOverview`：查询**单个月份**的账单总览，返回按指定维度（如 `MAAS_TYPE`、`BASE_MODEL` 等）聚合的 TopN 分组及金额占比。详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)。
- `GetBillingTrend`：查询**连续时间范围内**（支持日/月粒度）的费用趋势，返回分周期明细（`resultByTime`）、分组汇总（`groupByTotal`）及整体费用合计（`costTotals`）。详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)。
- 两接口均支持多维度过滤（`filter.dimensions`）、语言本地化（`locale`）、零值过滤（`zeroFilter`）及地域限定（`regionId`），且共享同一套维度 Code 体系（如 `API_KEY_ID`、`WORKSPACE_ID`、`ARTICLE_CODE` 等）。

> **注意**：文档 1 中 `GetBillingOverview` 的 `data.groups.percentage` 字段描述为“分组金额占 TopN 金额合计的比例”，而文档 2 中 `GetBillingTrend` 的 `periodDetails.percentage` 明确为“占当前周期总金额的比例”。二者语义不同，不可混用计算逻辑；实际使用时请严格依据对应接口文档定义解析。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `billMonth`（仅 Overview） | string | 是 | 账单月份，格式 `YYYY-MM` | `"2026-08"` |
| `granularity`（仅 Trend） | string | 是 | 时间粒度：`DAY` 或 `MONTH` | `"DAY"` |
| `timePeriod.start` / `.end`（仅 Trend） | string | 是 | 查询起止日期，格式 `YYYY-MM-DD` | `"2026-08-01"`, `"2026-08-31"` |
| `groupBy` | array<object> | 是 | 分组维度，**必须且仅含 1 个元素**；`code` 值需从[维度 Code 表](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)中选取 | `[{"code": "BASE_MODEL"}]` |
| `filter.dimensions` | array<object> | 否 | 筛选条件，支持 `IN`/`NOT` 模式；`values` 可传 `DIMENSION_FILTER_NULL_VALUE` 匹配空值 | `[{"code": "MAAS_TYPE", "values": ["inference"], "selectType": "IN"}]` |
| `topNum` | integer | 否 | 返回分组数量（1–20），默认 20；超出部分在 Trend 中合并为“其他” | `10` |
| `locale` | string | 否 | 返回语言：`zh-CN`（中文）或 `en-US`（英文），影响 `name` 字段展示 | `"zh-CN"` |

## 使用方式

1. **认证**：所有请求需携带有效的 Bearer [Token](../concepts/token.md)（通过百炼平台 AccessKey 获取），并设置 `Authorization: Bearer <token>` 请求头。
2. **Endpoint**：
   - 总览：`GET https://<region>.modelstudio.aliyuncs.com/modelstudio/billing/overview`
   - 趋势：`GET https://<region>.modelstudio.aliyuncs.com/modelstudio/billing/trend`
3. **构造请求**：按需组合路径参数与 Query 参数（如 `billMonth=2026-08&groupBy=[{"code":"MAAS_TYPE"}]&locale=zh-CN`）。
4. **解析响应**：检查 `success` 字段为 `true` 且 `code` 为 `"200"`；金额字段（如 `amount`、`pretaxAmount`）均为字符串类型，需转为数值处理；币种由 `currency` 字段明确标识。

## 限制和注意事项

- 单次请求最多返回 20 个分组（`topNum` 上限），`GetBillingTrend` 中超出部分统一归入 `DIMENSION_GROUP_OTHERS_VALUE`。
- `GetBillingOverview` 仅支持查询已结算完成的账单月份，通常延迟 1–3 个工作日；`GetBillingTrend` 的 `timePeriod.end` 不得晚于当前日期。
- 两个接口的 `groupBy.code` 和 `filter.dimensions.code` 值集完全一致，但 `GetBillingTrend` 的 `resultByTime.periodDetails` 中 `key` 为空时使用 `DIMENSION_GROUP_OTHERS_VALUE`，而 `GetBillingOverview` 使用 `DIMENSION_FILTER_NULL_VALUE` —— 二者语义不同，不可互换。
- 所有金额字段（如 `totalAmount`, `amount`）均为**字符串格式的十进制数字**（含小数点），无千分位分隔符，需用高精度浮点或定点数解析，避免 JS `parseFloat` 精度丢失。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


