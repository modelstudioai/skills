# billing api

Billing API 提供账单数据的查询能力，支持按月获取费用总览（`GetBillingOverview`）和按时间范围获取费用趋势（`GetBillingTrend`）。所有接口均基于 RESTful 设计，使用 HTTPS 协议，返回结构化 JSON 响应。开发者可通过维度分组、条件筛选和多语言支持灵活适配财务分析与成本监控场景。

## 支持的模型/功能

- `GetBillingOverview`：查询**单个月份**的账单总览，返回按指定维度聚合的 TopN 分组及金额占比，适用于月度成本概览与归因分析。详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)。
- `GetBillingTrend`：查询**连续时间范围内**（支持 DAY/MONTH 粒度）的账单趋势，返回分周期费用明细、分组汇总及“其他”合并项，适用于成本波动追踪与用量预测。详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)。

> **注意**：两接口均要求 `groupBy` 必填且仅支持单维度（如 `MAAS_TYPE` 或 `BASE_MODEL`），不支持多维嵌套分组；文档中未提及任何实时账单或秒级粒度能力，当前 API 仅面向已结算的账单数据。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `billMonth`（仅 `GetBillingOverview`） | string | 是 | 账单月份，格式 `YYYY-MM` | `2026-08` |
| `granularity`（仅 `GetBillingTrend`） | string | 是 | 时间粒度：`DAY` 或 `MONTH` | `DAY` |
| `timePeriod.start` / `.end`（仅 `GetBillingTrend`） | string | 是 | 查询起止日期，格式 `YYYY-MM-DD`；`end` 可等于 `start` | `2026-08-01`, `2026-08-31` |
| `groupBy[].code` | string | 是 | 分组维度 Code，统一建议大写；两接口支持完全相同的维度列表（如 `MAAS_TYPE`, `BASE_MODEL`, `API_KEY_ID` 等） | `BASE_MODEL` |
| `filter.dimensions[]` | array<object> | 否 | 维度过滤条件，支持 `IN`/`NOT` 逻辑；各维度 `values` 均可传 `DIMENSION_FILTER_NULL_VALUE` 表示匹配空值 | `[{"code": "BASE_MODEL", "values": ["qwen-plus"], "selectType": "IN"}]` |
| `topNum` | integer | 否 | 返回 TopN 分组数（1–20），默认 20；超出部分在 `GetBillingTrend` 中合并为“其他”，`GetBillingOverview` 中直接截断 | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组，默认 `true` | `false` |
| `locale` | string | 否 | 返回语言：`zh-CN`（中文）或 `en-US`（英文），影响 `name` 字段展示 | `zh-CN` |

## 使用方式

1. **认证**：所有请求需携带有效的 Bearer [Token](../concepts/token.md)（通过百炼平台 AccessKey/SecretKey 获取，具体鉴权流程见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 文档头部说明）。
2. **构造请求**：
   - `GetBillingOverview`：`GET /modelstudio/billing/overview?billMonth=2026-08&groupBy[0].code=MAAS_TYPE&locale=zh-CN`
   - `GetBillingTrend`：`GET /modelstudio/billing/trend?granularity=DAY&timePeriod.start=2026-08-01&timePeriod.end=2026-08-31&groupBy[0].code=BASE_MODEL`
3. **解析响应**：
   - 共同字段：`requestId`, `code`, `success`, `message`；
   - `GetBillingOverview` 主要数据在 `data.groups`（分组列表）和 `data.totalAmount`（总额）；
   - `GetBillingTrend` 主要数据在 `data.resultByTime`（时间序列）、`data.groupByTotal`（分组汇总）和 `data.costTotals`（总计）。

## 限制和注意事项

- **时间范围限制**：`GetBillingTrend` 的 `timePeriod.end` 不能晚于当前日期，且 `end - start` 最大跨度为 90 天（`granularity=DAY`）或 24 个月（`granularity=MONTH`）；`GetBillingOverview` 仅支持已生成账单的月份，通常延迟 1–3 个工作日。
- **维度一致性**：两接口对 `groupBy.code` 和 `filter.dimensions.code` 的取值集合、含义及 `values` 可选范围完全一致，详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 补充说明章节。
- **金额精度**：所有金额字段（如 `amount`, `pretaxAmount`）均为字符串类型，保留两位小数，**不可直接用浮点数解析**，须按字符串处理后转 decimal 避免精度丢失。
- > **注意**：`GetBillingOverview` 响应中 `data.groups.percentage` 是“占 TopN 分组金额合计”的比例，而非占全量账单的比例；而 `GetBillingTrend` 的 `periodDetails.percentage` 是“占该周期总金额”的比例——二者统计基准不同，不可混用。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


