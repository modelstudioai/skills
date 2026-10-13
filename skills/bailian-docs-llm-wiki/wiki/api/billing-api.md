# billing api

Billing API 提供账单数据的查询能力，支持按月汇总和按时间趋势两种视角，帮助开发者获取模型调用、训练等 MaaS 服务的费用分布与变化。当前开放两个核心接口：`GetBillingOverview` 用于获取单月账单总览，`GetBillingTrend` 用于查询指定时间范围内（按日或按月）的费用趋势。所有接口均基于 RESTful 设计，通过 HTTP GET 调用，返回结构化 JSON 数据。

## 支持的模型/功能

- **账单总览**：`GetBillingOverview` 接口提供指定月份的费用聚合结果，支持按单一维度（如 `MAAS_TYPE`、`BASE_MODEL` 等）分组，并返回 TopN 分组金额及占比。详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)。
- **账单趋势**：`GetBillingTrend` 接口支持按 `DAY` 或 `MONTH` 粒度统计多周期费用，返回每个周期内各分组的明细及“其他”合并项，适用于监控费用波动。详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)。
- **通用维度能力**：两接口共享同一套维度体系（如 `BASE_MODEL`、`API_KEY_ID`、`WORKSPACE_ID` 等），且均支持 `DIMENSION_FILTER_NULL_VALUE` 特殊值匹配空/NULL 字段，该能力在两篇原始文档中定义一致，详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 的补充说明部分。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `billMonth`（仅 `GetBillingOverview`） | string | 是 | 账单月份，格式 `YYYY-MM` | `2026-08` |
| `granularity`（仅 `GetBillingTrend`） | string | 是 | 时间粒度：`DAY` 或 `MONTH` | `DAY` |
| `timePeriod.start` / `.end`（仅 `GetBillingTrend`） | string | 是 | 查询起止日期，格式 `YYYY-MM-DD` | `2026-08-01`, `2026-08-31` |
| `groupBy` | array<object> | 是 | 分组条件，**必须且仅能含一个元素**；`code` 值需从标准维度列表中选取 | `[{"code": "MAAS_TYPE"}]` |
| `filter.dimensions` | array<object> | 否 | 维度过滤器，支持多维组合（如同时按 `BASE_MODEL` 和 `CHARGE_TYPE` 过滤） | `[{"code":"BASE_MODEL","values":["qwen-plus"],"selectType":"IN"}]` |
| `topNum` | integer | 否 | 返回分组数量，范围 1–20，默认 20；超出部分在 `GetBillingTrend` 中归入“其他” | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组，默认 `true` | `false` |

> **注意**：`GetBillingOverview` 文档中 `filter.dimensions.selectType` 示例值为 `IN`，而 `GetBillingTrend` 文档中同字段示例值也为 `IN`，二者一致；但两文档均未明确说明 `NOT` 类型是否支持多值数组（如 `["qwen-max", "qwen-plus"]`）。实际使用时建议单值测试，复杂逻辑请参考 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 的 filter 行为验证。

## 使用方式

- **认证**：所有 Billing API 请求需携带有效的 Bearer Token（通过百炼平台 AccessKey 获取），并设置 `Content-Type: application/json`。
- **Endpoint**：
  - `GET /modelstudio/billing/overview`（`GetBillingOverview`）
  - `GET /modelstudio/billing/trend`（`GetBillingTrend`）
- **典型调用链路**：
  1. 先用 `GetBillingOverview` 快速定位高消费维度（如发现 `MAAS_TYPE=inference` 占比异常高）；
  2. 再用 `GetBillingTrend` 指定该维度（`groupBy=[{"code":"BASE_MODEL"}]`）+ 时间范围，下钻分析具体模型的日/月费用趋势；
  3. 结合 `filter` 精确筛选（如限定 `WORKSPACE_ID` 或特定 `API_KEY_ID`）进行归属分析。

## 限制和注意事项

- **分组约束**：`groupBy` 数组长度**严格限制为 1**，不支持多维嵌套分组（如同时按 `BASE_MODEL` 和 `CHARGE_TYPE` 分组）。
- **时间范围限制**：`GetBillingTrend` 的 `timePeriod.end` 不能晚于当前日期，且跨度最长支持 90 天（`DAY` 粒度）或 12 个月（`MONTH` 粒度）；超出将返回 `400` 错误。
- **空值处理**：当 `filter.dimensions.values` 包含 `DIMENSION_FILTER_NULL_VALUE` 时，匹配对应字段为 NULL 或空字符串的数据——该行为在两篇文档中定义完全一致，可安全复用。
- **币种差异**：`GetBillingOverview` 示例返回 `USD`，`GetBillingTrend` 示例返回 `CNY`，实际币种取决于账户结算货币，**不支持跨币种请求参数控制**。
- **locale 影响**：`locale=zh-CN` 仅影响 `name` 字段的本地化展示（如 `MAAS_TYPE=inference` → `"模型调用"`），不影响 `key` 或筛选逻辑。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


