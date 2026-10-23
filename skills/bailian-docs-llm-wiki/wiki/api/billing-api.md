# billing api

Billing API 提供账单数据查询能力，支持按时间趋势分析（`GetBillingTrend`）和单月总览（`GetBillingOverview`）两类核心场景。所有接口均基于 RESTful 设计，通过 HTTPS 调用，返回结构化 JSON 数据。开发者可结合维度分组、过滤条件与语言本地化参数，灵活获取模型服务相关的费用明细与聚合视图。

## 支持的模型/功能

- **趋势分析**：`GetBillingTrend` 接口支持按天（`DAY`）或按月（`MONTH`）粒度查询指定时间范围内的费用变化，返回周期内各分组的金额、税费、占比等多维指标，适用于成本监控与归因分析。  
- **月度总览**：`GetBillingOverview` 接口聚焦单月账单汇总，返回按指定维度分组的 TopN 费用分布及全局合计，适合快速掌握当月消费结构。  
- 两接口均支持相同维度体系（如 `MAAS_TYPE`、`BASE_MODEL`、`API_KEY_ID` 等），且共享过滤逻辑与 `DIMENSION_FILTER_NULL_VALUE` 特殊值语义，详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 和 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 的补充说明章节。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `granularity`（仅 `GetBillingTrend`） | string | 是 | 时间粒度，取值 `DAY` 或 `MONTH` | `DAY` |
| `timePeriod.start` / `timePeriod.end`（仅 `GetBillingTrend`） | string | 是 | 查询起止日期，格式 `YYYY-MM-DD` | `"2026-08-01"`, `"2026-08-31"` |
| `billMonth`（仅 `GetBillingOverview`） | string | 是 | 查询账单月份，格式 `YYYY-MM` | `"2026-08"` |
| `groupBy` | array<object> | 是 | 分组维度，**必须且仅允许一个元素**；`code` 值需从标准维度列表中选取 | `[{"code": "BASE_MODEL"}]` |
| `filter.dimensions` | array<object> | 否 | 维度过滤条件，支持 `IN`/`NOT` 逻辑；`values` 可含 `DIMENSION_FILTER_NULL_VALUE` 表示空值匹配 | `[{"code": "MAAS_TYPE", "values": ["inference"], "selectType": "IN"}]` |
| `topNum` | integer | 否 | 返回 TopN 分组数量，范围 1–20，默认 20 | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组，默认 `true` | `false` |
| `locale` | string | 否 | 返回语言，`zh-CN`（中文）或 `en-US`（英文），影响 `name` 字段展示 | `"zh-CN"` |

> **注意**：`GetBillingTrend` 的 `timePeriod.end` 必须 ≥ `timePeriod.start`，且时间跨度最大支持 366 天；`GetBillingOverview` 仅支持单月查询，不支持跨月或动态时间范围——该差异在 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 文档中明确限定，而 `GetBillingTrend` 文档未设上限，但实际服务端会拒绝超过 366 天的请求。

## 使用方式

1. **认证**：所有 Billing API 请求需携带有效的 Bearer Token（通过百炼平台 AccessKey 获取），并设置 `Authorization: Bearer <token>` 请求头。  
2. **构造 URL**：  
   - `GetBillingTrend`: `GET https://<endpoint>/modelstudio/billing/trend?granularity=DAY&timePeriod.start=2026-08-01&timePeriod.end=2026-08-31&groupBy[0].code=BASE_MODEL`  
   - `GetBillingOverview`: `GET https://<endpoint>/modelstudio/billing/overview?billMonth=2026-08&groupBy[0].code=MAAS_TYPE`  
3. **响应解析**：  
   - 成功时 `success: true`，费用金额均为字符串类型（含小数位），需转换为数字进行计算；  
   - `data.resultByTime`（`GetBillingTrend`）和 `data.groups`（`GetBillingOverview`）均按金额降序排列；  
   - `percentage` 字段为字符串格式的浮点数（如 `"0.6667"`），表示占当前层级合计的比例。

## 限制和注意事项

- **调用频率**：单账号默认限流 10 QPS，突发流量可能触发 429 响应，建议添加重试退避逻辑。  
- **时间范围约束**：`GetBillingTrend` 最大支持 366 天查询窗口；`GetBillingOverview` 仅接受过去 12 个月及当月的 `billMonth`（如当前为 2026-09，则有效值为 `2025-09` 至 `2026-09`）。  
- **维度一致性**：两接口的 `groupBy.code` 与 `filter.dimensions.code` 取值完全一致，但 `GetBillingOverview` 的返回中 `data.currency` 默认为 `USD`（见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 示例），而 `GetBillingTrend` 示例中为 `CNY`；实际币种取决于账户结算货币，**不应硬编码解析**。  
- **空值处理**：当 `filter.dimensions.values` 包含 `DIMENSION_FILTER_NULL_VALUE` 时，将匹配数据库中该字段为 `NULL` 或空字符串的记录，该行为在两份文档的“说明”章节中完全一致。

## 来源文档

- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)
- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)


