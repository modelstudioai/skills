# billing api

Billing API 提供账单数据查询能力，支持按月汇总和按时间趋势两种视角，帮助开发者监控和分析模型服务的费用分布。当前开放两个核心接口：`GetBillingOverview` 用于获取单月账单总览（含分组聚合），`GetBillingTrend` 用于查询指定时间范围内的费用变化趋势（支持日/月粒度）。所有接口均基于 RESTful 设计，需通过 HTTPS 调用，并依赖平台身份认证。

## 支持的模型/功能

- **账单总览**：通过 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 获取指定月份（`billMonth`）的费用汇总、分组 TopN 及占比，适用于月度成本复盘。
- **账单趋势**：通过 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 查询连续时间段（`timePeriod.start` 至 `timePeriod.end`）的费用变化，支持 `DAY` 或 `MONTH` 粒度，适用于用量波动分析与预算预警。
- **统一维度体系**：两接口共享相同的维度 Code（如 `MAAS_TYPE`、`BASE_MODEL`、`API_KEY_ID` 等）和过滤逻辑，确保分析口径一致；详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 补充说明部分。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `billMonth`（仅 Overview） | string | 是 | 账单月份，格式 `YYYY-MM` | `"2026-08"` |
| `granularity`（仅 Trend） | string | 是 | 时间粒度，取值 `DAY` 或 `MONTH` | `"DAY"` |
| `timePeriod`（仅 Trend） | object | 是 | 含 `start`（`YYYY-MM-DD`）和 `end`（`YYYY-MM-DD`） | `{"start":"2026-08-01","end":"2026-08-31"}` |
| `groupBy` | array<object> | 是 | 分组条件，**必须且仅能传 1 个维度**；`code` 值需从标准维度列表中选取 | `[{"code": "MAAS_TYPE"}]` |
| `filter.dimensions` | array<object> | 否 | 维度过滤，支持 `IN`/`NOT` 语义；`values` 中可使用 `DIMENSION_FILTER_NULL_VALUE` 匹配空值 | `[{"code":"BASE_MODEL","values":["qwen-plus"],"selectType":"IN"}]` |
| `topNum` | integer | 否 | 返回分组数量，1–20，默认 20；超出部分在 Trend 接口中合并为“其他” | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组，默认 `true` | `false` |
| `locale` | string | 否 | 返回语言，`zh-CN`（中文）或 `en-US`（英文），影响 `name` 字段展示 | `"zh-CN"` |

> **注意**：`regionId` 参数在两份文档中均列为可选，但实际调用时若账户跨地域部署账单数据，**必须显式指定 `regionId`**，否则可能返回空结果或不完整数据 —— 此行为未在 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 文档中明确强调，需开发者自行验证。

## 使用方式

1. **认证**：所有请求需携带有效的 Bearer [Token](../concepts/token.md)（通过百炼平台 AccessKey 鉴权）。
2. **构造 URL**：
   - 总览：`GET https://<endpoint>/modelstudio/billing/overview?billMonth=2026-08&groupBy[0].code=MAAS_TYPE`
   - 趋势：`GET https://<endpoint>/modelstudio/billing/trend?granularity=DAY&timePeriod.start=2026-08-01&timePeriod.end=2026-08-31&groupBy[0].code=BASE_MODEL`
3. **响应解析**：
   - `data.groups`（Overview）或 `data.resultByTime`（Trend）为关键业务数据数组，按金额降序排列；
   - 金额字段（如 `amount`、`pretaxAmount`）均为**字符串类型**，需转为数值后参与计算；
   - `currency` 字段标识币种，不同账户可能返回 `USD` 或 `CNY`，不可硬编码假设。

## 限制和注意事项

- **时间范围限制**：`GetBillingTrend` 的 `timePeriod.end` 不能晚于当前日期，且跨度最长支持 90 天；`GetBillingOverview` 的 `billMonth` 仅支持近 12 个月（以当前月为基准）。
- **分组约束**：`groupBy` 严格限定为单维度，传入多个元素将导致 `400 Bad Request`；维度 `code` 值**必须大写**（如 `MAAS_TYPE`），小写将被忽略。
- **空值处理**：当 `filter.dimensions.values` 包含 `DIMENSION_FILTER_NULL_VALUE` 时，匹配数据库中该字段为 `NULL` 或空字符串的记录 —— 此机制在两份文档中定义一致，但 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 的示例未体现，建议在测试中覆盖空值场景。
- **性能提示**：高 `topNum`（如 20）或宽时间范围（如 90 天 `DAY`）可能增加响应延迟，生产环境建议结合 `filter` 缩小数据集。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


