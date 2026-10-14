# billing api

billing api 提供账单数据的聚合查询能力，支持按月总览和时间趋势两种视角。开发者可通过 `GetBillingOverview` 获取指定月份的费用分组概览，或通过 `GetBillingTrend` 查询跨日/月的费用变化趋势，并支持多维度分组与筛选。所有接口均基于 RESTful 设计，返回结构化 JSON 数据，适用于成本分析、用量监控与财务对账等场景。

## 支持的模型/功能

当前 billing api 包含两个核心接口：

- `GetBillingOverview`：用于查询**单个月份**的账单总览，返回按指定维度（如 `MAAS_TYPE`、`BASE_MODEL`）聚合的 TopN 分组及金额占比。详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)。
- `GetBillingTrend`：用于查询**连续时间段内**（按天或按月粒度）的费用趋势，返回各周期内分组明细及累计汇总。详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)。

> **注意**：两文档中 `filter.dimensions[].selectType` 均仅列出 `IN` 和 `NOT` 两种取值，但实际调用中若传入 `EXCLUDE` 或空字符串将导致参数校验失败；该行为已在 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 的最新测试中确认，建议严格按文档取值。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `billMonth`（仅 `GetBillingOverview`） | string | 是 | 账单月份，格式 `YYYY-MM` | `"2026-08"` |
| `granularity`（仅 `GetBillingTrend`） | string | 是 | 时间粒度：`DAY` 或 `MONTH` | `"DAY"` |
| `timePeriod.start` / `.end`（仅 `GetBillingTrend`） | string | 是 | 查询起止日期，格式 `YYYY-MM-DD` | `"2026-08-01"`, `"2026-08-31"` |
| `groupBy` | array<object> | 是 | 分组维度，**必须且仅能含 1 个元素**；`code` 值需从标准维度列表中选取 | `[{"code": "MAAS_TYPE"}]` |
| `filter.dimensions` | array<object> | 否 | 筛选条件，支持多维组合；每个维度需指定 `code`、`values` 和 `selectType` | `[{"code": "BASE_MODEL", "values": ["qwen-max"], "selectType": "IN"}]` |
| `topNum` | integer | 否 | 返回分组数量，范围 `1–20`，默认 `20` | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 `0` 的分组，默认 `true` | `false` |
| `locale` | string | 否 | 返回语言，`zh-CN` 或 `en-US`，影响 `name` 字段展示 | `"zh-CN"` |

**支持的维度 Code（通用）**：`MAAS_TYPE`、`BASE_MODEL`、`API_KEY_ID`、`WORKSPACE_ID`、`FEE_TYPE`、`CHARGE_TYPE`、`BUSINESS_REGION`、`SERVICE_SITE`、`ARTICLE_CODE`。所有维度均支持传入 `DIMENSION_FILTER_NULL_VALUE` 表示匹配空值。

## 使用方式

1. **认证**：所有请求需携带有效的 `Authorization` header（如 Bearer [Token](../concepts/token.md)），具体鉴权方式参见平台统一认证文档。
2. **构造请求**：
   - `GetBillingOverview`：`GET /modelstudio/billing/overview?billMonth=2026-08&groupBy[0].code=MAAS_TYPE&locale=zh-CN`
   - `GetBillingTrend`：`GET /modelstudio/billing/trend?granularity=DAY&timePeriod.start=2026-08-01&timePeriod.end=2026-08-31&groupBy[0].code=BASE_MODEL`
3. **解析响应**：
   - 共同字段：`requestId`、`code`、`success`、`data.currency`
   - `GetBillingOverview` 主要关注 `data.groups`（TopN 分组列表）和 `data.totalAmount`
   - `GetBillingTrend` 主要关注 `data.resultByTime`（时间序列明细）和 `data.groupByTotal`（分组累计）

## 限制和注意事项

- **分组限制**：`groupBy` 数组长度**必须为 1**，不支持多维嵌套分组（如同时按 `MAAS_TYPE` 和 `BASE_MODEL` 分组）。
- **时间范围限制**：`GetBillingTrend` 的 `timePeriod.end` 与 `start` 间隔最长支持 **90 天**（`DAY` 粒度）或 **12 个月**（`MONTH` 粒度），超出将返回 `400` 错误。
- **空值处理**：当 `filter.dimensions[].values` 包含 `DIMENSION_FILTER_NULL_VALUE` 时，会匹配数据库中该字段为 `NULL` 或空字符串的记录；但 `groupBy.code` 不允许为 `NULL`。
- > **注意**：`GetBillingOverview` 文档中 `data.groups.percentage` 定义为“占 TopN 金额合计的比例”，而 `GetBillingTrend` 中 `periodDetails.percentage` 定义为“占**当前周期总金额**的比例”。二者语义不同，不可直接对比，使用时需严格依据各自文档上下文理解。该差异已在 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 和 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 中分别明确，无需额外兼容。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


