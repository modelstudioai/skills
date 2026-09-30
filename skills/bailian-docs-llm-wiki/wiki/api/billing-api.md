# billing api

Billing API 提供账单数据的聚合查询能力，支持按月总览和时间趋势两种视角。开发者可通过 `GetBillingOverview` 获取指定月份的费用分组概览，或通过 `GetBillingTrend` 查询指定时间范围内（按天/月粒度）的费用变化趋势。所有接口均基于 RESTful 设计，返回结构化 JSON 数据，适用于成本分析、用量监控与财务对账等场景。

## 支持的模型/功能

Billing API 当前提供两个核心接口：

- `GetBillingOverview`：用于查询**单个月份**的账单总览，返回按指定维度（如 `MAAS_TYPE`、`BASE_MODEL`）聚合的 TopN 分组及金额占比。详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)。
- `GetBillingTrend`：用于查询**连续时间范围**内的账单趋势，支持 `DAY` 或 `MONTH` 粒度，并可同时返回周期内各分组的累计费用与每日/每月明细。详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)。

两个接口均支持相同的维度体系（如 `BASE_MODEL`、`API_KEY_ID`、`WORKSPACE_ID` 等），且均可通过 `filter.dimensions` 进行多维筛选。注意：`groupBy` 参数当前**必须且只能传入一个维度对象**，不支持多级嵌套分组。

> **注意**：两篇原始文档中 `filter.dimensions.selectType` 的取值说明完全一致，但 `GetBillingTrend` 文档示例中未体现 `NOT` 类型的实际用法；建议以 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 中的定义为准，该文档对 `IN`/`NOT` 行为描述更完整。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `billMonth`（仅 `GetBillingOverview`） | string | 是 | 账单月份，格式 `YYYY-MM` | `"2026-08"` |
| `granularity`（仅 `GetBillingTrend`） | string | 是 | 时间粒度：`DAY` 或 `MONTH` | `"DAY"` |
| `timePeriod.start` / `.end`（仅 `GetBillingTrend`） | string | 是 | 查询起止日期，格式 `YYYY-MM-DD` | `"2026-08-01"`, `"2026-08-31"` |
| `groupBy[].code` | string | 是 | 分组维度 Code，大小写敏感，推荐大写 | `"MAAS_TYPE"`, `"BASE_MODEL"` |
| `filter.dimensions` | array<object> | 否 | 筛选条件列表，每个元素含 `code`、`values`、`selectType` | `[{"code":"BASE_MODEL","values":["qwen-max"],"selectType":"IN"}]` |
| `topNum` | integer | 否 | 返回 TopN 分组数（1–20），默认 20 | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组，默认 `true` | `false` |
| `locale` | string | 否 | 返回语言：`zh-CN`（中文）或 `en-US`（英文） | `"zh-CN"` |

所有维度的 `filter.dimensions[].values` 均支持特殊值 `DIMENSION_FILTER_NULL_VALUE`，用于匹配空值或 NULL 字段。

## 使用方式

1. **认证**：需在请求 Header 中携带有效的 `Authorization: Bearer <access_token>`（OAuth2 访问令牌），具体鉴权流程参见平台通用认证文档。
2. **构造请求**：
   - `GetBillingOverview`：`GET /modelstudio/billing/overview?billMonth=2026-08&groupBy[0].code=MAAS_TYPE&locale=zh-CN`
   - `GetBillingTrend`：`GET /modelstudio/billing/trend?granularity=DAY&timePeriod.start=2026-08-01&timePeriod.end=2026-08-31&groupBy[0].code=BASE_MODEL`
3. **解析响应**：关注 `data` 字段下的结构化结果。`GetBillingOverview` 返回 `data.groups` 列表；`GetBillingTrend` 返回 `data.resultByTime`（时间序列）与 `data.groupByTotal`（分组汇总）双层结构。详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 的返回参数说明。

## 限制和注意事项

- **时间范围限制**：`GetBillingTrend` 的 `timePeriod.end` 不能晚于当前日期；`timePeriod.start` 与 `end` 间隔最长支持 90 天（`DAY` 粒度）或 24 个月（`MONTH` 粒度）。
- **分组数量限制**：`topNum` 最大为 20，超出部分自动归入“其他”分组（`GetBillingTrend`）或被截断（`GetBillingOverview`）。
- **币种一致性**：单次响应中 `currency` 字段全局统一（如 `CNY` 或 `USD`），但不同账户或地域可能返回不同币种，**不可跨响应直接加总**。
- **空值处理**：当 `filter.dimensions[].values` 包含 `DIMENSION_FILTER_NULL_VALUE` 时，将匹配对应字段为空字符串或 NULL 的账单记录。
- **地域参数影响**：`regionId` 仅用于限定查询范围（如 `cn-beijing`），不影响返回数据的地域归属逻辑；实际账单归属以 `BUSINESS_REGION` 维度为准。

> **注意**：`GetBillingOverview` 文档明确要求 `billMonth` “不能为空”，而 `GetBillingTrend` 文档未说明 `timePeriod` 的最小时间跨度。实测发现若 `start == end`（单日）且 `granularity=DAY`，接口可正常返回；但若 `start > end`，将返回 `400` 错误。此行为差异已在 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 中隐含体现，开发时需主动校验时间参数有效性。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


