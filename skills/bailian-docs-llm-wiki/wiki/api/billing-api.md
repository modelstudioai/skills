# billing api

Billing API 提供账单数据查询能力，支持按月获取费用总览（`GetBillingOverview`）和按时间范围获取费用趋势（`GetBillingTrend`）。所有接口均基于 RESTful 设计，通过 HTTPS 调用，返回结构化 JSON 数据。开发者可利用分组、筛选、多语言等参数灵活适配监控、对账与成本分析场景。

## 支持的模型/功能

- `GetBillingOverview`：查询**单个月份**的账单总览，返回按指定维度聚合的 TopN 分组及金额占比，适用于月度成本概览与归因分析。  
- `GetBillingTrend`：查询**连续时间段内**（按天或按月粒度）的费用趋势，返回各周期内分组明细与汇总，适用于成本波动监控与用量预测。  
两者的维度体系完全一致，均支持 `MAAS_TYPE`、`BASE_MODEL`、`API_KEY_ID`、`WORKSPACE_ID` 等 9 类标准维度，详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 的补充说明部分。> **注意**：文档中 `filter.dimensions[].values` 允许传入 `DIMENSION_FILTER_NULL_VALUE` 表示空值匹配，但该行为在实际调用中需以最新 SDK 或控制台调试结果为准；建议优先使用显式空字符串或 omit 字段替代。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `billMonth`（仅 `GetBillingOverview`） | string | 是 | 账单月份，格式 `YYYY-MM` | `2026-08` |
| `granularity`（仅 `GetBillingTrend`） | string | 是 | 时间粒度：`DAY` 或 `MONTH` | `DAY` |
| `timePeriod.start` / `.end`（仅 `GetBillingTrend`） | string | 是 | 查询起止日期，格式 `YYYY-MM-DD` | `2026-08-01`, `2026-08-31` |
| `groupBy` | array<object> | 是 | 分组条件，**必须且仅含 1 个元素**；`code` 值需从标准维度列表中选取 | `[{"code": "MAAS_TYPE"}]` |
| `filter.dimensions` | array<object> | 否 | 维度过滤器，支持多维组合；每个 `dimension` 包含 `code`、`values` 和 `selectType`（`IN`/`NOT`） | `[{"code":"BASE_MODEL","values":["qwen-max"],"selectType":"IN"}]` |
| `topNum` | integer | 否 | 返回分组数量（1–20），默认 20；超出部分在 `GetBillingTrend` 中合并为“其他” | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组，默认 `true` | `false` |
| `locale` | string | 否 | 返回语言：`zh-CN`（中文）或 `en-US`（英文），影响 `name` 字段展示 | `zh-CN` |

所有维度 Code（如 `MAAS_TYPE`、`ARTICLE_CODE`）**必须大写**，且 `filter.dimensions[].values` 支持特殊值 `DIMENSION_FILTER_NULL_VALUE` 表示匹配 NULL 或空字符串，该能力在 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 和 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 中定义一致。

## 使用方式

1. **认证**：使用平台统一的 AccessKey ID/Secret 签名鉴权（参考通用 API 鉴权文档）。
2. **构造请求**：
   - `GetBillingOverview`：`GET /modelstudio/billing/overview?billMonth=2026-08&groupBy[0].code=BASE_MODEL&locale=zh-CN`
   - `GetBillingTrend`：`GET /modelstudio/billing/trend?granularity=DAY&timePeriod.start=2026-08-01&timePeriod.end=2026-08-31&groupBy[0].code=MAAS_TYPE`
3. **解析响应**：
   - `GetBillingOverview` 主要关注 `data.groups`（TopN 分组）和 `data.totalAmount`（总额）；
   - `GetBillingTrend` 主要关注 `data.resultByTime`（时间序列明细）和 `data.groupByTotal`（分组汇总），注意 `periodDetails` 中 `percentage` 为**当前周期内占比**，非全局占比。

## 限制和注意事项

- **时间范围限制**：`GetBillingTrend` 的 `timePeriod.end` 不得晚于当前日期，且 `end - start` 最大跨度为 90 天（`granularity=DAY`）或 12 个月（`granularity=MONTH`）。
- **分组约束**：两个接口均强制要求 `groupBy` 数组长度为 1，不支持多维嵌套分组。
- **币种差异**：`GetBillingOverview` 示例返回 `USD`，而 `GetBillingTrend` 示例返回 `CNY`；实际币种由账户结算货币决定，**不可通过参数指定**，需以响应中 `currency` 字段为准。
- > **注意**：两篇原始文档中 `data.groups.amount`（`GetBillingOverview`）与 `data.resultByTime.periodDetails.amount`（`GetBillingTrend`）均为字符串类型，**必须按字符串解析并转换为浮点数进行计算**，避免直接 JSON 解析为整数导致精度丢失。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


