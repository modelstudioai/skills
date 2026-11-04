# billing api

Billing API 提供账单数据查询能力，支持按月获取费用总览（`GetBillingOverview`）和按时间范围获取费用趋势（`GetBillingTrend`）。所有接口均基于 RESTful 设计，通过 HTTPS 调用，返回结构化 JSON 数据。开发者可利用分组、筛选、多语言等参数灵活适配监控、对账与成本分析场景。

## 支持的模型/功能

Billing API 当前提供两个核心接口：
- `GetBillingOverview`：查询**单个月份**的账单总览，返回按指定维度聚合的 TopN 分组及金额占比，适用于月度成本概览与归因分析。详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)。
- `GetBillingTrend`：查询**连续时间段内**（按天或按月粒度）的费用趋势，返回各周期内分组明细及“其他”汇总，适用于成本波动监控与用量预测。详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)。

> **注意**：两接口均仅支持单维度分组（`groupBy` 数组长度必须为 1），不支持多维交叉聚合；且 `filter.dimensions` 中同一 `code` 仅允许出现一次，重复将被忽略。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `billMonth`（仅 `GetBillingOverview`） | string | 是 | 账单月份，格式 `YYYY-MM` | `2026-08` |
| `granularity`（仅 `GetBillingTrend`） | string | 是 | 时间粒度，取值 `DAY` 或 `MONTH` | `DAY` |
| `timePeriod.start` / `.end`（仅 `GetBillingTrend`） | string | 是 | 查询起止日期，格式 `YYYY-MM-DD` | `2026-08-01`, `2026-08-31` |
| `groupBy[].code` | string | 是 | 分组维度 Code，**必须且仅能传一个**。支持值包括：`MAAS_TYPE`, `BASE_MODEL`, `API_KEY_ID`, `WORKSPACE_ID`, `FEE_TYPE`, `CHARGE_TYPE`, `BUSINESS_REGION`, `SERVICE_SITE`, `ARTICLE_CODE` | `BASE_MODEL` |
| `filter.dimensions` | array<object> | 否 | 筛选条件，每个元素含 `code`、`values`（字符串数组）、`selectType`（`IN`/`NOT`） | `[{"code":"BASE_MODEL","values":["qwen-plus"],"selectType":"IN"}]` |
| `topNum` | integer | 否 | 返回分组数量，1–20，默认 20；超出部分在 `GetBillingTrend` 中合并为“其他”，`GetBillingOverview` 中直接截断 | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组，默认 `true` | `false` |
| `locale` | string | 否 | 返回语言，`zh-CN`（中文）或 `en-US`（英文），影响 `name` 字段展示 | `zh-CN` |

> **注意**：`filter.dimensions[].values` 可传特殊值 `DIMENSION_FILTER_NULL_VALUE` 表示匹配 NULL 或空字符串字段，该行为在两接口中一致，详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 补充说明。

## 使用方式

1. **认证**：所有请求需携带有效的 Bearer Token（通过百炼平台 AccessKey/SecretKey 获取并签发）。
2. **构造 URL**：
   - `GetBillingOverview`: `GET https://<endpoint>/modelstudio/billing/overview?billMonth=2026-08&groupBy[0].code=MAAS_TYPE`
   - `GetBillingTrend`: `GET https://<endpoint>/modelstudio/billing/trend?granularity=DAY&timePeriod.start=2026-08-01&timePeriod.end=2026-08-31&groupBy[0].code=BASE_MODEL`
3. **设置 Header**：`Content-Type: application/json`, `Authorization: Bearer <token>`。
4. **解析响应**：检查 `success` 字段及 `code` 值；金额字段（如 `amount`, `pretaxAmount`）均为字符串类型，需自行转换为数值进行计算。

## 限制和注意事项

- **时间范围限制**：`GetBillingTrend` 的 `timePeriod.end` 不能晚于当前日期；`timePeriod.start` 与 `end` 间隔最长支持 90 天（`DAY` 粒度）或 12 个月（`MONTH` 粒度）。
- **币种一致性**：单次响应中 `currency` 字段全局统一（如 `CNY` 或 `USD`），但不同账户或地域可能返回不同币种，**不可跨响应直接加总**。
- **空值处理**：当 `groupBy[].code` 对应字段为空时，`key` 返回 `DIMENSION_FILTER_NULL_VALUE`，`name` 返回 `-`（`locale=zh-CN`）或 `-`（`en-US`），该逻辑两接口一致。
- **精度提示**：所有金额字段为字符串，保留小数点后两位，**禁止使用浮点数直接解析**，应使用高精度 Decimal 类型或字符串运算避免精度丢失。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


