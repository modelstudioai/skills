# billing api

Billing API 提供账单数据查询能力，支持按月获取费用总览（`GetBillingOverview`）和按时间范围获取费用趋势（`GetBillingTrend`）。所有接口均基于 RESTful 设计，通过 HTTPS 调用，返回结构化 JSON 响应。开发者可利用分组、筛选、多语言等参数灵活适配财务分析与成本监控场景。

## 支持的模型/功能

- `GetBillingOverview`：查询**单个月份**的账单总览，返回按指定维度聚合的 TopN 分组及金额占比，适用于月度成本概览与归因分析。  
- `GetBillingTrend`：查询**连续时间范围内**（支持 DAY/MONTH 粒度）的费用趋势，返回周期性明细（`resultByTime`）与分组汇总（`groupByTotal`），适用于成本波动监控与预测。  
两者的维度体系完全一致，均支持 `MAAS_TYPE`、`BASE_MODEL`、`API_KEY_ID`、`WORKSPACE_ID` 等 9 类标准维度，详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 的补充说明部分。该维度定义也同步适用于 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)，确保跨接口语义一致性。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `billMonth`（仅 `GetBillingOverview`） | string | 是 | 账单月份，格式 `YYYY-MM` | `"2026-08"` |
| `granularity`（仅 `GetBillingTrend`） | string | 是 | 时间粒度，取值 `DAY` 或 `MONTH` | `"DAY"` |
| `timePeriod.start` / `.end`（仅 `GetBillingTrend`） | string | 是 | 查询起止日期，格式 `YYYY-MM-DD` | `"2026-08-01"`, `"2026-08-31"` |
| `groupBy` | array<object> | 是 | 分组条件，**必须且仅含一个元素**；`code` 字段需从标准维度中选择 | `[{"code": "MAAS_TYPE"}]` |
| `filter.dimensions` | array<object> | 否 | 维度过滤器，支持 `IN`/`NOT` 逻辑；`values` 可传 `DIMENSION_FILTER_NULL_VALUE` 表示空值匹配 | `[{"code": "BASE_MODEL", "values": ["qwen-plus"], "selectType": "IN"}]` |
| `topNum` | integer | 否 | 返回分组数量（1–20），默认 `20`；超出部分在 `GetBillingTrend` 中合并为“其他” | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组，默认 `true` | `false` |
| `locale` | string | 否 | 返回语言，`zh-CN`（中文）或 `en-US`（英文），影响 `name` 字段展示 | `"zh-CN"` |

> **注意**：`GetBillingOverview` 和 `GetBillingTrend` 对 `filter.dimensions[].code` 和 `groupBy[].code` 的支持列表完全相同，但文档 1 和文档 2 的“补充说明”表格内容存在冗余重复，以 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 中的定义为准，其为权威来源。

## 使用方式

1. **认证**：所有请求需携带有效的 Bearer [Token](../concepts/token.md)（通过百炼平台 AccessKey 鉴权，具体流程见平台身份认证文档）。  
2. **构造请求**：
   - `GetBillingOverview`：`GET /modelstudio/billing/overview?billMonth=2026-08&groupBy[0].code=MAAS_TYPE&locale=zh-CN`  
   - `GetBillingTrend`：`GET /modelstudio/billing/trend?granularity=DAY&timePeriod.start=2026-08-01&timePeriod.end=2026-08-31&groupBy[0].code=BASE_MODEL&filter.dimensions[0].code=MAAS_TYPE&filter.dimensions[0].values[0]=inference`  
3. **解析响应**：
   - 共同字段：`requestId`、`code`、`success`、`data.currency`；
   - `GetBillingOverview` 主要使用 `data.groups`（TopN 分组列表）和 `data.totalAmount`；
   - `GetBillingTrend` 主要使用 `data.resultByTime`（时间序列）、`data.groupByTotal`（分组汇总）和 `data.costTotals`（全量合计）。

## 限制和注意事项

- **时间范围限制**：`GetBillingTrend` 的 `timePeriod.end` 不能晚于当前日期；`timePeriod.start` 与 `end` 间隔最长支持 90 天（`DAY` 粒度）或 24 个月（`MONTH` 粒度）。  
- **分组约束**：两个接口均强制要求 `groupBy` 数组长度为 1，不支持多维嵌套分组。  
- **空值处理**：`filter.dimensions[].values` 中传入 `DIMENSION_FILTER_NULL_VALUE` 可匹配数据库中 NULL 或空字符串字段，该行为在两接口中一致。  
- **币种差异**：响应中 `currency` 字段取决于账单实际结算币种（如 `USD` 或 `CNY`），**不支持请求时指定输出币种**，需由客户端自行处理汇率转换。  
- **精度说明**：所有金额字段（如 `amount`、`pretaxAmount`）均为字符串类型，保留两位小数，避免浮点精度丢失。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


