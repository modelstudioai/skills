# billing api

Billing API 提供账单数据的查询能力，支持按月获取费用总览（`GetBillingOverview`）和按时间范围获取费用趋势（`GetBillingTrend`）。所有接口均基于 RESTful 设计，使用 HTTPS 协议，需通过 API Key 进行身份认证。返回数据包含金额、税费、币种及多维度分组信息，适用于成本分析、用量监控与财务对账等场景。

## 支持的模型/功能

Billing API 当前提供两个核心功能接口：

- `GetBillingOverview`：查询**单个月份**的账单总览，返回按指定维度聚合后的 TopN 分组费用（如按 `MAAS_TYPE` 或 `BASE_MODEL` 分组），适用于月度成本概览分析。详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)。
- `GetBillingTrend`：查询**连续时间范围内**（支持 DAY/MONTH 粒度）的费用趋势，返回按时间序列组织的分组费用明细，支持“其他”分组合并，适用于用量波动监测与归因分析。详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)。

两个接口均支持相同的维度体系（如 `MAAS_TYPE`、`BASE_MODEL`、`API_KEY_ID` 等）进行分组与过滤，且维度 Code 建议统一使用大写形式。完整维度列表及取值说明请参考 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 文档中的“补充说明”章节。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `billMonth`（仅 `GetBillingOverview`） | string | 是 | 账单月份，格式 `YYYY-MM` | `2026-08` |
| `granularity`（仅 `GetBillingTrend`） | string | 是 | 时间粒度：`DAY` 或 `MONTH` | `DAY` |
| `timePeriod.start` / `.end`（仅 `GetBillingTrend`） | string | 是 | 查询起止日期，格式 `YYYY-MM-DD`；`end` 需 ≥ `start` | `2026-08-01`, `2026-08-31` |
| `groupBy` | array<object> | 是 | 分组条件，**必须且仅能传入一个元素**；`groupBy.code` 为维度 Code | `[{"code": "MAAS_TYPE"}]` |
| `filter.dimensions` | array<object> | 否 | 维度过滤条件，每个元素含 `code`、`values`（数组）、`selectType`（`IN`/`NOT`） | `[{"code":"BASE_MODEL","values":["qwen-max"],"selectType":"IN"}]` |
| `topNum` | integer | 否 | 返回分组数量，范围 1–20，默认 20；超出部分在 `GetBillingTrend` 中合并为“其他” | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组，默认 `true` | `false` |
| `regionId` | string | 否 | 地域 ID，用于限定账单数据范围 | `cn-beijing` |
| `locale` | string | 否 | 返回语言：`zh-CN`（中文）或 `en-US`（英文），影响 `name` 字段展示 | `zh-CN` |

> **注意**：两篇原始文档对 `filter.dimensions.selectType` 的可选值描述完全一致（仅 `IN`/`NOT`），但 `GetBillingOverview` 文档中示例值误写为 `IN`（带多余空格），而 `GetBillingTrend` 文档示例正确为 `IN`（无空格）。实际调用应使用无空格的 `IN` 或 `NOT`。

## 使用方式

1. **认证**：在 HTTP Header 中携带 `Authorization: Bearer <API_KEY>`。
2. **请求路径**：
   - 总览：`GET /modelstudio/billing/overview`
   - 趋势：`GET /modelstudio/billing/trend`
3. **构造查询参数**：将上述关键参数作为 Query String 传递（如 `?billMonth=2026-08&groupBy=[{"code":"MAAS_TYPE"}]&locale=zh-CN`）。
4. **解析响应**：
   - 共同字段：`requestId`、`code`、`success`、`data.currency`；
   - `GetBillingOverview` 主要关注 `data.groups`（TopN 分组）和 `data.totalAmount`；
   - `GetBillingTrend` 主要关注 `data.resultByTime`（时间序列明细）和 `data.groupByTotal`（分组汇总）。

## 限制和注意事项

- **时间范围限制**：`GetBillingTrend` 的 `timePeriod.end` 不能晚于当前日期；`timePeriod.start` 到 `end` 的跨度最大支持 90 天（`granularity=DAY`）或 12 个月（`granularity=MONTH`）。
- **分组约束**：`groupBy` 数组长度**必须为 1**，不支持多维嵌套分组；若需交叉分析，需客户端自行聚合。
- **空值处理**：所有维度的 `filter.dimensions.values` 可传特殊字符串 `DIMENSION_FILTER_NULL_VALUE` 表示匹配 NULL 或空字符串，该行为在两篇文档中定义一致。
- **金额精度**：所有金额字段（如 `amount`、`pretaxAmount`）均为字符串类型，保留两位小数，**不可直接转为浮点数参与计算**，避免精度丢失。
- **地域与币种**：`regionId` 影响账单数据源，但 `currency` 由账单实际记账币种决定，可能与用户所在地域不一致（例如国际站账单可能返回 `USD`）。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


