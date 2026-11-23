# billing api

Billing API 提供账单数据查询能力，支持按月获取费用总览（`GetBillingOverview`）和按时间范围获取费用趋势（`GetBillingTrend`）。所有接口均基于 RESTful 设计，通过 HTTPS 调用，返回结构化 JSON 响应。该 API 适用于开发者集成至内部财务看板、成本分析工具或自动化对账系统。

## 支持的模型/功能

Billing API 当前提供两个核心接口：

- `GetBillingOverview`：查询**单个月份**的账单总览，返回按指定维度（如 `MAAS_TYPE`、`BASE_MODEL`）聚合的 TopN 分组费用及占比。适用于月度成本复盘与概览分析。详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)。
- `GetBillingTrend`：查询**连续时间段内**（支持日粒度或月粒度）的费用趋势，返回分周期、分组的明细金额与税费拆分。适用于成本波动监控与归因分析。详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)。

> **注意**：两文档均声明 `groupBy` 必须且只能传入一个维度，但未明确禁止嵌套多层分组；实际调用时若传入多个 `groupBy` 元素，将被服务端拒绝（HTTP 400），此行为已在 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 的线上环境验证。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `billMonth`（仅 `GetBillingOverview`） | string | 是 | 账单月份，格式 `YYYY-MM` | `"2026-08"` |
| `granularity`（仅 `GetBillingTrend`） | string | 是 | 时间粒度，取值 `DAY` 或 `MONTH` | `"DAY"` |
| `timePeriod.start` / `.end`（仅 `GetBillingTrend`） | string | 是 | 查询起止日期，格式 `YYYY-MM-DD`，最大跨度 90 天 | `"2026-08-01"`, `"2026-08-31"` |
| `groupBy[].code` | string | 是 | 分组维度 Code，统一使用大写；支持 `MAAS_TYPE`、`BASE_MODEL`、`API_KEY_ID`、`WORKSPACE_ID`、`FEE_TYPE`、`CHARGE_TYPE`、`BUSINESS_REGION`、`SERVICE_SITE`、`ARTICLE_CODE` | `"BASE_MODEL"` |
| `filter.dimensions` | array | 否 | 维度过滤条件，每个元素含 `code`、`values`、`selectType` | `[{"code":"BASE_MODEL","values":["qwen-plus"],"selectType":"IN"}]` |
| `topNum` | integer | 否 | 返回 TopN 分组数量（1–20），默认 20；超出部分在 `GetBillingTrend` 中合并为“其他” | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组，默认 `true` | `false` |
| `locale` | string | 否 | 返回语言，`zh-CN`（中文）或 `en-US`（英文），影响 `name` 字段展示 | `"zh-CN"` |

## 使用方式

1. **认证**：所有请求需携带有效的 Bearer Token（通过百炼平台 AccessKey 签名生成，具体参见平台通用鉴权文档）。
2. **Endpoint**：
   - `GET /modelstudio/billing/overview` → `GetBillingOverview`
   - `GET /modelstudio/billing/trend` → `GetBillingTrend`
3. **构造请求**：将参数作为 query string 传递（如 `?billMonth=2026-08&groupBy[0].code=MAAS_TYPE&locale=zh-CN`）。
4. **解析响应**：
   - 共同字段：`requestId`（用于问题排查）、`success`、`code`、`message`；
   - `GetBillingOverview` 主要关注 `data.groups`（分组列表）与 `data.totalAmount`（总额）；
   - `GetBillingTrend` 主要关注 `data.resultByTime`（时间序列明细）与 `data.groupByTotal`（分组汇总）。

## 限制和注意事项

- **时间范围限制**：
  - `GetBillingOverview`：仅支持查询已出账的自然月，不支持未来月份或非整月区间；
  - `GetBillingTrend`：`timePeriod.end` 与 `start` 间隔不得超过 90 天，且 `end` 不得晚于当前日期（T-1 日数据可查）。
- **维度值一致性**：`filter.dimensions[].values` 中传入 `DIMENSION_FILTER_NULL_VALUE` 可匹配 NULL 或空字符串，但该值**不可与其他具体值混用在同一 `values` 数组中**（否则返回 400）。
- **币种差异**：`GetBillingOverview` 示例返回 `USD`，而 `GetBillingTrend` 示例返回 `CNY`；实际币种取决于账户结算主体，**不支持跨币种强制转换**，需以 `data.currency` 字段为准。
- **空值处理**：当 `groupBy.code` 对应维度在某条账单记录中为空时，其 `key` 字段返回 `DIMENSION_FILTER_NULL_VALUE`（而非空字符串），前端需做兼容处理。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


