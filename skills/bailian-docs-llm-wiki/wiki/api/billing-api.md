# billing api

Billing API 提供账单数据查询能力，支持按月获取费用总览（`GetBillingOverview`）和按时间范围获取费用趋势（`GetBillingTrend`）。所有接口均基于 RESTful 设计，通过 HTTPS 调用，返回结构化 JSON 数据。开发者可结合分组、筛选与多语言支持，灵活适配控制台展示或成本分析场景。

## 支持的模型/功能

Billing API 当前提供两个核心能力：
- `GetBillingOverview`：查询**单个月份**的账单总览，返回按指定维度聚合的 TopN 分组及金额占比，适用于月度成本概览与归因分析。详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)。
- `GetBillingTrend`：查询**连续时间段内**（按天或按月粒度）的费用趋势，返回各周期内分组明细及累计汇总，适用于成本波动监控与用量预测。详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)。

> **注意**：两接口均仅支持单维度分组（`groupBy` 数组长度必须为 1），且不支持嵌套或多维交叉分析；文档中未提及任何实时账单或预估费用能力，所有数据均为已出账的结算数据。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `billMonth`（仅 `GetBillingOverview`） | string | 是 | 账单月份，格式 `YYYY-MM` | `2026-08` |
| `granularity`（仅 `GetBillingTrend`） | string | 是 | 时间粒度，取值 `DAY` 或 `MONTH` | `DAY` |
| `timePeriod.start` / `.end`（仅 `GetBillingTrend`） | string | 是 | 查询起止日期，格式 `YYYY-MM-DD`；`start` ≤ `end`，最大跨度 90 天 | `2026-08-01`, `2026-08-31` |
| `groupBy[].code` | string | 是 | 分组维度 Code，统一使用大写；两接口支持完全相同的维度列表 | `MAAS_TYPE`, `BASE_MODEL`, `API_KEY_ID` 等（见下文补充说明） |
| `filter.dimensions` | array<object> | 否 | 维度过滤条件，支持 `IN`/`NOT` 语义；`values` 中可传 `DIMENSION_FILTER_NULL_VALUE` 匹配空值 | `[{"code": "BASE_MODEL", "values": ["qwen-plus"], "selectType": "IN"}]` |
| `topNum` | integer | 否 | 返回 TopN 分组数（1–20），默认 20；超出部分在 `GetBillingTrend` 中合并为“其他” | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组，默认 `true` | `false` |
| `regionId` / `locale` | string | 否 | 地域 ID（如 `cn-beijing`）和返回语言（`zh-CN`/`en-US`） | `cn-beijing`, `zh-CN` |

**补充说明（通用）**：  
`groupBy[].code` 和 `filter.dimensions[].code` 均支持以下维度 Code（大小写敏感，建议全大写）：  
`MAAS_TYPE`, `BASE_MODEL`, `API_KEY_ID`, `WORKSPACE_ID`, `FEE_TYPE`, `CHARGE_TYPE`, `BUSINESS_REGION`, `SERVICE_SITE`, `ARTICLE_CODE`。  
各维度 `filter.dimensions[].values` 可传实际账单值（如 `"qwen-plus"`）或特殊标记 `DIMENSION_FILTER_NULL_VALUE`（表示 NULL/空字符串），该行为在 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 和 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 中定义一致。

## 使用方式

1. **认证**：所有请求需携带有效的 Bearer Token（通过百炼平台 AccessKey 鉴权，具体签权流程参见平台通用鉴权文档）。
2. **构造请求**：
   - `GetBillingOverview`：`GET /modelstudio/billing/overview?billMonth=2026-08&groupBy[0].code=MAAS_TYPE&locale=zh-CN`
   - `GetBillingTrend`：`GET /modelstudio/billing/trend?granularity=DAY&timePeriod.start=2026-08-01&timePeriod.end=2026-08-31&groupBy[0].code=BASE_MODEL`
3. **解析响应**：
   - 共同字段：`requestId`, `code`, `success`, `message`, `data`。
   - `GetBillingOverview` 主要关注 `data.groups`（TopN 分组列表）和 `data.totalAmount`（总额）。
   - `GetBillingTrend` 主要关注 `data.resultByTime`（时间序列明细）、`data.groupByTotal`（分组累计）和 `data.costTotals`（整体合计）。

## 限制和注意事项

- **时间范围限制**：`GetBillingTrend` 的 `timePeriod.end` 不得晚于当前日期，且 `end - start` 最大为 90 天；`GetBillingOverview` 的 `billMonth` 仅支持近 12 个月已出账数据（历史月份以平台实际账单生成为准）。
- **分组与筛选约束**：`groupBy` 必须且只能包含一个元素；`filter.dimensions` 中每个维度的 `values` 数组长度上限为 50。
- **金额精度**：所有金额字段（如 `amount`, `pretaxAmount`）均为字符串类型，保留两位小数，单位由 `currency` 字段声明（如 `"USD"`, `"CNY"`），**不可直接进行浮点运算**，需先转换为整数（单位：分）或使用高精度库处理。
- **空值处理**：当 `filter.dimensions[].values` 包含 `DIMENSION_FILTER_NULL_VALUE` 时，匹配对应字段为 NULL 或空字符串的账单记录；该机制在两接口中行为一致，但需注意 `GetBillingTrend` 的 `resultByTime.periodDetails` 中可能返回 `DIMENSION_GROUP_OTHERS_VALUE` 表示“其他”分组。
- > **注意**：`GetBillingOverview` 返回的 `data.groups.percentage` 是“占 TopN 金额合计的比例”，而非占总金额的比例；而 `GetBillingTrend` 中 `periodDetails.percentage` 是“占当前周期总金额的比例”。二者计算基准不同，不可混用。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


