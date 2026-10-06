# billing api

Billing API 提供账单数据查询能力，支持按月汇总和按时间趋势两种视角，帮助开发者监控和分析模型服务的费用分布。当前开放两个核心接口：`GetBillingOverview` 用于获取单月账单总览（含分组聚合与筛选），`GetBillingTrend` 用于查询指定时间范围内（日/月粒度）的费用变化趋势。所有接口均基于 RESTful 设计，需通过 HTTPS 调用，并依赖平台身份认证。

## 支持的模型/功能

- **账单总览**：通过 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 获取指定月份（`billMonth`）的费用合计、分组明细（如按 `MAAS_TYPE` 或 `BASE_MODEL`）及占比。
- **账单趋势**：通过 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 查询连续时间段（`timePeriod.start` 至 `timePeriod.end`）内的费用变化，支持 `DAY` 或 `MONTH` 粒度聚合，并返回各周期内分组详情（`resultByTime.periodDetails`）。
- **通用维度能力**：两个接口均支持相同维度 Code（如 `MAAS_TYPE`、`BASE_MODEL`、`API_KEY_ID` 等）用于 `groupBy` 和 `filter.dimensions`，且 `filter.dimensions.values` 均可传 `DIMENSION_FILTER_NULL_VALUE` 表示空值匹配。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `billMonth`（仅 Overview） | string | 是 | 账单月份，格式 `YYYY-MM` | `"2026-08"` |
| `granularity`（仅 Trend） | string | 是 | 时间粒度，取值 `DAY` 或 `MONTH` | `"DAY"` |
| `timePeriod`（仅 Trend） | object | 是 | 含 `start`（`YYYY-MM-DD`）和 `end`（`YYYY-MM-DD`） | `{"start":"2026-08-01","end":"2026-08-31"}` |
| `groupBy` | array<object> | 是 | 分组条件，**必须且仅能传 1 个维度**；`code` 值需从[维度 Code 表](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)中选取 | `[{"code": "BASE_MODEL"}]` |
| `filter.dimensions` | array<object> | 否 | 维度过滤，支持多维组合；每个元素含 `code`、`values`（字符串数组）、`selectType`（`IN`/`NOT`） | `[{"code":"MAAS_TYPE","values":["inference"],"selectType":"IN"}]` |
| `topNum` | integer | 否 | 返回 TopN 分组数，范围 1–20，默认 20；超出部分在 Trend 中合并为“其他” | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组，默认 `true` | `false` |
| `locale` | string | 否 | 返回语言，`zh-CN`（中文）或 `en-US`（英文），影响 `name` 字段展示 | `"zh-CN"` |

> **注意**：`regionId` 参数在两篇文档中均列为可选，但实际调用时若账户启用了多地域资源隔离，**必须显式传入目标地域 ID（如 `cn-beijing`）**，否则可能返回空数据或非预期地域账单 —— 此行为未在 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 文档中明确强调，需开发者主动适配。

## 使用方式

1. **认证**：使用平台标准 AccessKey 签名或 Bearer [Token](../concepts/token.md) 认证（详见 [API 认证机制](../../raw/auth/api-authentication.md)）。
2. **构造请求**：
   - 总览：`GET /modelstudio/billing/overview?billMonth=2026-08&groupBy=[{"code":"MAAS_TYPE"}]&locale=zh-CN`
   - 趋势：`GET /modelstudio/billing/trend?granularity=DAY&timePeriod.start=2026-08-01&timePeriod.end=2026-08-31&groupBy=[{"code":"BASE_MODEL"}]`
3. **解析响应**：
   - `data.groups`（Overview）或 `data.resultByTime`（Trend）为费用主体数据，金额字段（`amount`、`pretaxAmount`、`taxAmount`）均为**字符串类型**，需转为数值处理。
   - `currency` 字段标识币种，不同账户可能返回 `CNY` 或 `USD`，不可硬编码假设。

## 限制和注意事项

- **时间范围限制**：`GetBillingTrend` 的 `timePeriod.end` 不能晚于当前日期，且跨度最长支持 90 天（`DAY` 粒度）或 12 个月（`MONTH` 粒度）；`GetBillingOverview` 仅支持已结算完成的月份（通常延迟 1–3 天）。
- **分组约束**：`groupBy` 必须且只能包含一个维度对象，传入多个将导致 400 错误；`filter.dimensions` 可多维，但各维度 `code` 不得重复。
- **空值处理**：当 `filter.dimensions.values` 包含 `DIMENSION_FILTER_NULL_VALUE` 时，匹配数据库中该字段为 `NULL` 或空字符串的记录 —— 此逻辑在两篇文档中一致，但 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 的补充说明位置更靠前，建议优先参考。
- **性能提示**：高频调用（>5 次/秒）或大范围 `topNum`（如 20）+ 多维 `filter` 组合可能导致响应延迟，生产环境建议添加客户端缓存（如 `Cache-Control: max-age=300`）。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


