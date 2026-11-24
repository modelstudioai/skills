# billing api

Billing API 提供账单数据的查询能力，支持按月汇总和按时间趋势两种视角，帮助开发者获取模型调用、训练等 MaaS 服务的费用分布与变化。当前开放两个核心接口：`GetBillingOverview` 用于获取单月账单总览，`GetBillingTrend` 用于查询指定时间范围内（按日或按月）的费用趋势。所有接口均基于 RESTful 设计，通过 HTTP GET 调用，返回结构化 JSON 数据。

## 支持的模型/功能

- **账单总览**：`GetBillingOverview` 接口提供指定月份的费用聚合结果，支持按单一维度（如 `MAAS_TYPE`、`BASE_MODEL` 等）分组，并返回 TopN 分组金额及占比。详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)。
- **账单趋势**：`GetBillingTrend` 接口支持按 `DAY` 或 `MONTH` 粒度统计费用变化，返回周期内各时间段的费用明细、分组汇总及“其他”合并项，适用于成本监控与归因分析。详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)。
- **通用维度能力**：两接口共享同一套维度体系（如 `MAAS_TYPE`、`BASE_MODEL`、`API_KEY_ID`、`WORKSPACE_ID` 等），且均支持 `DIMENSION_FILTER_NULL_VALUE` 表示空值匹配 —— 此能力在两篇原始文档中定义一致，详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 的补充说明章节。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `billMonth`（仅 `GetBillingOverview`） | string | 是 | 账单月份，格式 `YYYY-MM` | `2026-08` |
| `granularity`（仅 `GetBillingTrend`） | string | 是 | 时间粒度：`DAY` 或 `MONTH` | `DAY` |
| `timePeriod.start` / `.end`（仅 `GetBillingTrend`） | string | 是 | 查询起止日期，格式 `YYYY-MM-DD` | `2026-08-01`, `2026-08-31` |
| `groupBy` | array<object> | 是 | 分组条件，**必须且仅允许 1 个元素**；`code` 值需从标准维度列表中选取 | `[{"code": "MAAS_TYPE"}]` |
| `filter.dimensions` | array<object> | 否 | 维度过滤器，每个元素含 `code`、`values`、`selectType` | `[{"code": "BASE_MODEL", "values": ["qwen-max"], "selectType": "IN"}]` |
| `topNum` | integer | 否 | 返回分组数量，范围 `1–20`，默认 `20`；超出部分在 `GetBillingTrend` 中合并为“其他” | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组，默认 `true` | `false` |
| `locale` | string | 否 | 返回语言，`zh-CN`（中文）或 `en-US`（英文），影响 `name` 字段展示 | `zh-CN` |

> **注意**：`GetBillingOverview` 的 `filter.dimensions[].values` 支持 `DIMENSION_FILTER_NULL_VALUE`，但其返回体中 `data.groups.key` 对应空值时固定返回字符串 `DIMENSION_FILTER_NULL_VALUE`；而 `GetBillingTrend` 在 `resultByTime.periodDetails.key` 中对非 TopN 分组使用 `DIMENSION_GROUP_OTHERS_VALUE` —— 二者语义不同，不可混用，开发时需严格依据各自文档处理空值与“其他”标识。

## 使用方式

1. **认证**：所有 Billing API 请求需携带有效的 Bearer [Token](../concepts/token.md)（通过百炼平台 AccessKey 获取），并设置 `Authorization: Bearer <token>` 请求头。
2. **构造请求**：
   - `GetBillingOverview`：`GET /modelstudio/billing/overview?billMonth=2026-08&groupBy[0].code=MAAS_TYPE&locale=zh-CN`
   - `GetBillingTrend`：`GET /modelstudio/billing/trend?granularity=DAY&timePeriod.start=2026-08-01&timePeriod.end=2026-08-31&groupBy[0].code=BASE_MODEL`
3. **解析响应**：
   - 共同校验 `success === true` 和 `code === "200"`；
   - 金额字段（如 `amount`、`pretaxAmount`）均为**字符串类型**，需转换为数值后参与计算；
   - 多币种场景下，`currency` 字段可能为 `CNY` 或 `USD`，不可假设统一币种。

## 限制和注意事项

- **调用频率限制**：单账号默认 QPS 为 5，突发请求可能触发限流（HTTP 429），建议添加重试退避逻辑。
- **时间范围约束**：
  - `GetBillingOverview`：`billMonth` 仅支持近 12 个月（含当月）的历史账单，不支持未来月份；
  - `GetBillingTrend`：`timePeriod` 最大跨度为 90 天（`DAY` 粒度）或 12 个月（`MONTH` 粒度）。
- **分组与筛选一致性**：`groupBy[].code` 与 `filter.dimensions[].code` 必须属于同一维度集合，且大小写敏感（文档明确要求“建议统一使用大写”），传入小写 code（如 `maas_type`）将导致 400 错误。
- **空值处理差异**：`GetBillingOverview` 返回的 `data.groups.key` 为空时恒为 `DIMENSION_FILTER_NULL_VALUE`；而 `GetBillingTrend` 的 `resultByTime.periodDetails.key` 中，TopN 之外的分组统一为 `DIMENSION_GROUP_OTHERS_VALUE` —— 此处行为不一致，开发时需分别适配，详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 与 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 的返回参数定义。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


