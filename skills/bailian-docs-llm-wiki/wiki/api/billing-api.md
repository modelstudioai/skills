# billing api

Billing API 提供账单数据查询能力，支持按月获取费用总览（`GetBillingOverview`）和按时间范围获取费用趋势（`GetBillingTrend`）。所有接口均基于 RESTful 设计，通过 HTTPS 调用，返回结构化 JSON 数据。开发者可利用分组、筛选、多语言等参数灵活适配监控、对账与成本分析场景。

## 支持的模型/功能

Billing API 当前提供两个核心功能接口：

- `GetBillingOverview`：查询**单个月份**的账单总览，返回按指定维度聚合的 TopN 分组及金额占比，适用于月度成本概览与归因分析。详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)。
- `GetBillingTrend`：查询**连续时间范围内**（按天或按月粒度）的费用趋势，返回周期内各时段的分组明细与汇总，适用于成本波动监控与用量预测。详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)。

两个接口均支持相同的维度体系（如 `MAAS_TYPE`、`BASE_MODEL`、`API_KEY_ID` 等），且分组与筛选逻辑一致，便于统一集成。

> **注意**：两篇原始文档中 `filter.dimensions[].selectType` 的取值说明完全一致（仅支持 `IN`/`NOT`），但 `GetBillingTrend` 文档示例中未体现 `NOT` 用法，而 `GetBillingOverview` 文档明确列出该选项；建议以 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 中的定义为准，`NOT` 为有效且受支持的筛选类型。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `billMonth`（仅 `GetBillingOverview`） | string | 是 | 账单月份，格式 `YYYY-MM` | `"2026-08"` |
| `granularity`（仅 `GetBillingTrend`） | string | 是 | 时间粒度：`DAY` 或 `MONTH` | `"DAY"` |
| `timePeriod.start` / `.end`（仅 `GetBillingTrend`） | string | 是 | 查询起止日期，格式 `YYYY-MM-DD` | `"2026-08-01"`, `"2026-08-31"` |
| `groupBy` | array<object> | 是 | 分组条件，**必须且仅能传入一个维度**；`code` 值需从标准维度列表中选取 | `[{"code": "MAAS_TYPE"}]` |
| `filter.dimensions` | array<object> | 否 | 维度过滤条件，支持多维组合（如同时按 `BASE_MODEL` 和 `REGION_ID` 筛选） | `[{"code": "BASE_MODEL", "values": ["qwen-max"], "selectType": "IN"}]` |
| `topNum` | integer | 否 | 返回分组数量（1–20），默认 `20`；超出部分在 `GetBillingTrend` 中合并为“其他” | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组，默认 `true` | `false` |
| `locale` | string | 否 | 返回语言：`zh-CN`（中文）或 `en-US`（英文），影响 `name` 字段展示 | `"zh-CN"` |

所有维度 Code（如 `MAAS_TYPE`、`ARTICLE_CODE` 等）及其可选值，均以两篇文档共同的[补充说明](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)为准；其中 `DIMENSION_FILTER_NULL_VALUE` 可用于匹配空值，该行为在两篇文档中定义一致。

## 使用方式

1. **认证**：所有请求需携带有效的 `Authorization` header（如 Bearer [Token](../concepts/token.md)），具体鉴权方式参见平台通用认证文档。
2. **构造请求**：
   - `GetBillingOverview`：`GET /modelstudio/billing/overview?billMonth=2026-08&groupBy=[{"code":"MAAS_TYPE"}]&locale=zh-CN`
   - `GetBillingTrend`：`GET /modelstudio/billing/trend?granularity=DAY&timePeriod.start=2026-08-01&timePeriod.end=2026-08-31&groupBy=[{"code":"BASE_MODEL"}]`
3. **解析响应**：
   - 共同字段：`requestId`、`code`、`success`、`message`；
   - `GetBillingOverview` 主要关注 `data.groups`（TopN 分组列表）及 `data.totalAmount`；
   - `GetBillingTrend` 主要关注 `data.resultByTime`（时间序列）、`data.groupByTotal`（分组汇总）和 `data.costTotals`（全局合计）。

## 限制和注意事项

- **分组限制**：`groupBy` 数组长度**严格限定为 1**，不支持多维嵌套分组（如同时按 `MAAS_TYPE` 和 `BASE_MODEL` 分组）。
- **时间范围限制**：
  - `GetBillingTrend` 的 `timePeriod.end` 不能晚于当前日期，且跨度最大支持 90 天（`DAY` 粒度）或 12 个月（`MONTH` 粒度）；
  - `GetBillingOverview` 仅支持已生成账单的月份，通常延迟 1–3 个工作日。
- **空值处理**：`filter.dimensions[].values` 中传入 `DIMENSION_FILTER_NULL_VALUE` 可匹配 NULL 或空字符串字段，该机制在两篇文档中定义一致，无歧义。
- **金额精度**：所有金额字段（如 `amount`、`pretaxAmount`）均为**字符串类型**，保留两位小数，开发者需自行转换为数值进行计算，避免浮点误差。
- **地域与币种**：`regionId` 影响数据源地域，`currency` 字段由账单实际结算币种决定，不同 `regionId` 可能返回不同币种（如 `CNY` 或 `USD`），不可硬编码假设。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


