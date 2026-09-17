# billing api

Billing API 提供账单数据查询能力，支持按月获取费用总览（`GetBillingOverview`）和按时间范围获取费用趋势（`GetBillingTrend`）。所有接口均基于 RESTful 设计，通过 HTTPS 调用，返回结构化 JSON 响应。该 API 适用于开发者集成至内部财务看板、成本分析工具或自动化对账系统。

## 支持的模型/功能

Billing API 当前提供两个核心接口：

- `GetBillingOverview`：查询**单个月份**的账单总览，返回按指定维度聚合的 TopN 分组费用及全局合计（含税/不含税/币种）。适用于月度成本复盘与概览展示。  
- `GetBillingTrend`：查询**连续时间段内**（按天或按月粒度）的费用趋势，返回分周期、分组的明细费用序列，支持“其他”分组合并。适用于成本波动监控与归因分析。  

两接口均支持统一的维度体系（如 `MAAS_TYPE`、`BASE_MODEL`、`API_KEY_ID` 等）进行分组与过滤，具体维度定义详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 和 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 的补充说明章节。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `billMonth`（仅 `GetBillingOverview`） | string | 是 | 账单月份，格式 `YYYY-MM` | `2026-08` |
| `granularity`（仅 `GetBillingTrend`） | string | 是 | 时间粒度：`DAY` 或 `MONTH` | `DAY` |
| `timePeriod.start` / `timePeriod.end`（仅 `GetBillingTrend`） | string | 是 | 查询起止日期，格式 `YYYY-MM-DD`；`end` 可等于 `start` | `2026-08-01`, `2026-08-31` |
| `groupBy` | array<object> | 是 | 分组条件，**必须且仅能传入一个维度**；`code` 值需从文档定义的维度 Code 中选取 | `[{"code": "MAAS_TYPE"}]` |
| `filter.dimensions` | array<object> | 否 | 维度过滤器，支持多维组合；每个元素含 `code`、`values`（可含 `DIMENSION_FILTER_NULL_VALUE`）、`selectType`（`IN`/`NOT`） | `[{"code": "BASE_MODEL", "values": ["qwen-plus"], "selectType": "IN"}]` |
| `topNum` | integer | 否 | 返回分组数量，1–20，默认 20；超出部分在 `GetBillingTrend` 中合并为“其他” | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组，默认 `true` | `false` |
| `regionId` / `locale` | string | 否 | 地域 ID（如 `cn-beijing`）与返回语言（`zh-CN`/`en-US`），影响 `name` 字段本地化 | `zh-CN` |

> **注意**：两文档对 `filter.dimensions[].selectType` 的取值描述完全一致，但 `GetBillingTrend` 示例中未体现 `NOT` 用法；实际调用时请以 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 文档为准，`NOT` 为有效值。

## 使用方式

1. **认证**：所有请求需携带有效的 Bearer [Token](../concepts/token.md)（通过百炼平台 AccessKey 鉴权，具体流程参见平台通用鉴权文档）。
2. **Endpoint**：
   - `GET /modelstudio/billing/overview` → `GetBillingOverview`
   - `GET /modelstudio/billing/trend` → `GetBillingTrend`
3. **构造请求**：将参数作为 query string 附加（如 `?billMonth=2026-08&groupBy[0].code=MAAS_TYPE&filter.dimensions[0].code=BASE_MODEL&filter.dimensions[0].values=qwen-plus`），注意 URL 编码。
4. **解析响应**：
   - 共同字段：`requestId`（用于问题排查）、`success`、`data.currency`、`data.totalAmount`（`GetBillingOverview`）或 `data.costTotals.amount`（`GetBillingTrend`）。
   - `GetBillingOverview` 主要关注 `data.groups` 数组（TopN 分组）；
   - `GetBillingTrend` 主要关注 `data.resultByTime`（时间序列）和 `data.groupByTotal`（分组汇总）。

## 限制和注意事项

- **时间范围限制**：`GetBillingTrend` 的 `timePeriod` 最大跨度为 90 天（`DAY` 粒度）或 12 个月（`MONTH` 粒度）；超出将返回 400 错误。
- **分组约束**：`groupBy` 必须且只能包含一个维度对象，传入多个将被拒绝；维度 `code` 值**必须大写**（如 `MAAS_TYPE`，非 `maas_type`），否则返回空数据或错误。
- **空值处理**：`filter.dimensions[].values` 中传入 `DIMENSION_FILTER_NULL_VALUE` 可匹配 NULL 或空字符串字段，该行为在两篇文档中定义一致，详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 补充说明。
- **金额精度**：所有金额字段（`amount`、`pretaxAmount`、`taxAmount`）均为字符串类型，保留两位小数，**不可直接转为浮点数计算**，避免精度丢失。
- **地域与币种**：`regionId` 影响账单数据源地域，但不强制与 `locale` 一致；`currency` 由账单实际结算币种决定，可能为 `CNY` 或 `USD`，不可预设。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


