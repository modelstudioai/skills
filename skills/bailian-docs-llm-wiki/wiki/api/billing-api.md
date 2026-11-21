# billing api

Billing API 提供账单数据的查询能力，支持按月汇总和按时间趋势两种视角，帮助开发者获取模型调用、训练等 MaaS 服务的费用分布与变化。当前开放两个核心接口：`GetBillingOverview` 用于获取单月账单总览，`GetBillingTrend` 用于查询指定时间范围内（按日或按月）的费用趋势。所有接口均基于 RESTful 设计，通过 HTTP GET 调用，返回结构化 JSON 数据。

## 支持的模型/功能

- **账单总览**：`GetBillingOverview` 接口提供指定月份的费用聚合结果，支持按单一维度（如 `MAAS_TYPE`、`BASE_MODEL` 等）分组，并返回 TopN 分组金额及占比。详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)。
- **账单趋势**：`GetBillingTrend` 接口支持按 `DAY` 或 `MONTH` 粒度统计多周期费用，返回每个周期内各分组的明细及“其他”合并项，适用于监控费用波动。详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)。
- **通用维度能力**：两接口共享同一套维度体系（如 `BASE_MODEL`、`API_KEY_ID`、`WORKSPACE_ID` 等），且均支持 `DIMENSION_FILTER_NULL_VALUE` 特殊值匹配空/NULL 字段，该能力在两篇原始文档中定义一致，详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 的补充说明章节。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `billMonth`（仅 `GetBillingOverview`） | string | 是 | 账单月份，格式 `YYYY-MM` | `2026-08` |
| `granularity`（仅 `GetBillingTrend`） | string | 是 | 时间粒度：`DAY` 或 `MONTH` | `DAY` |
| `timePeriod.start` / `.end`（仅 `GetBillingTrend`） | string | 是 | 查询起止日期，格式 `YYYY-MM-DD` | `2026-08-01`, `2026-08-31` |
| `groupBy` | array<object> | 是 | 分组条件，**必须且仅能传入一个维度**；`code` 值需从标准维度列表中选取 | `[{"code": "MAAS_TYPE"}]` |
| `filter.dimensions` | array<object> | 否 | 维度过滤条件，支持 `IN`/`NOT` 操作；`values` 可含 `DIMENSION_FILTER_NULL_VALUE` | `[{"code":"BASE_MODEL","values":["qwen-plus"],"selectType":"IN"}]` |
| `topNum` | integer | 否 | 返回分组数量，范围 `1–20`，默认 `20`；超出部分在 `GetBillingTrend` 中归入“其他” | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组，默认 `true` | `false` |
| `locale` | string | 否 | 返回语言，`zh-CN` 或 `en-US`，影响 `name` 字段展示 | `zh-CN` |

> **注意**：`GetBillingOverview` 的 `filter.dimensions[].code` 和 `GetBillingTrend` 的对应字段虽定义相同，但文档 1 中 `filter.dimensions` 的描述为“否”，而文档 2 中未明确其必填性；实际调用中二者均为可选，行为一致，以 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 的说明为准。

## 使用方式

1. **认证**：所有请求需携带有效的 `Authorization` Header（如 Bearer Token），具体鉴权方式参见平台统一认证文档。
2. **构造 URL**：
   - 总览：`GET https://<endpoint>/modelstudio/billing/overview?billMonth=2026-08&groupBy[0].code=BASE_MODEL&locale=zh-CN`
   - 趋势：`GET https://<endpoint>/modelstudio/billing/trend?granularity=DAY&timePeriod.start=2026-08-01&timePeriod.end=2026-08-31&groupBy[0].code=MAAS_TYPE`
3. **响应解析**：
   - 成功时 `success: true`，费用金额字段（如 `amount`, `pretaxAmount`）均为**字符串类型**，需转为浮点数处理；
   - `data.groups`（总览）和 `data.resultByTime.periodDetails`（趋势）中的 `percentage` 为小数形式（如 `0.10` 表示 10%），非百分比字符串。

## 限制和注意事项

- **时间范围限制**：`GetBillingTrend` 的 `timePeriod.end` 不能晚于当前日期；`timePeriod.start` 与 `end` 间隔最长支持 90 天（`DAY` 粒度）或 12 个月（`MONTH` 粒度）。
- **分组约束**：`groupBy` 数组长度严格为 1，传入多个元素将返回参数错误；不支持多维嵌套分组。
- **币种差异**：`GetBillingOverview` 示例返回 `USD`，`GetBillingTrend` 示例返回 `CNY`，实际币种取决于账户结算货币，**不可假设固定值**。
- **空值处理**：当 `filter.dimensions.values` 包含 `DIMENSION_FILTER_NULL_VALUE` 时，匹配数据库中该字段为 NULL 或空字符串的记录，该语义在两篇文档中完全一致，是可靠的行为保证。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


