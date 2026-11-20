# billing api

Billing API 提供账单数据的查询能力，支持按月汇总和按时间趋势两种视角，帮助开发者监控和分析模型服务的费用分布。当前开放两个核心接口：`GetBillingOverview` 用于获取指定月份的分组账单总览，`GetBillingTrend` 用于查询指定时间范围内（按日或按月粒度）的费用变化趋势。所有接口均基于 RESTful 设计，通过 HTTP GET 调用，返回结构化 JSON 响应。

## 支持的模型/功能

- **账单总览**：`GetBillingOverview` 接口提供单月账单的维度聚合视图，适用于快速掌握当月费用构成（如按 MaaS 类型、基础模型或 API Key ID 分组）。详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)。
- **账单趋势**：`GetBillingTrend` 接口支持自定义时间范围（起止日期）与聚合粒度（`DAY` 或 `MONTH`），返回分组维度下的周期性费用序列，适用于成本归因与波动分析。详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)。
- **通用维度能力**：两个接口均支持相同的维度 Code（如 `MAAS_TYPE`、`BASE_MODEL`、`API_KEY_ID` 等）进行分组（`groupBy`）和过滤（`filter.dimensions`），且均支持 `DIMENSION_FILTER_NULL_VALUE` 表示空值匹配。

> **注意**：两篇原始文档中 `filter.dimensions.selectType` 的取值说明完全一致，但 `GetBillingTrend` 文档未明确列出 `NOT` 的具体语义（如是否支持多值 `NOT IN`）。实际使用时请以 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 中的定义为准，并在测试中验证 `NOT` 行为。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `billMonth`（仅 `GetBillingOverview`） | string | 是 | 账单月份，格式 `YYYY-MM` | `"2026-08"` |
| `granularity`（仅 `GetBillingTrend`） | string | 是 | 时间粒度，取值 `DAY` 或 `MONTH` | `"DAY"` |
| `timePeriod.start` / `.end`（仅 `GetBillingTrend`） | string | 是 | 查询起止日期，格式 `YYYY-MM-DD` | `"2026-08-01"`, `"2026-08-31"` |
| `groupBy` | array<object> | 是 | 分组条件，**必须且仅能传入一个对象**；`groupBy.code` 为维度 Code | `[{"code": "MAAS_TYPE"}]` |
| `filter.dimensions` | array<object> | 否 | 维度过滤列表，每个元素含 `code`、`values`（string 数组）、`selectType`（`IN`/`NOT`） | `[{"code": "BASE_MODEL", "values": ["qwen-max"], "selectType": "IN"}]` |
| `topNum` | integer | 否 | 返回 TopN 分组数量，范围 1–20，默认 20 | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组，默认 `true` | `false` |
| `regionId` | string | 否 | 地域 ID，影响数据范围 | `"cn-beijing"` |
| `locale` | string | 否 | 返回语言，`zh-CN` 或 `en-US`，影响 `name` 字段展示 | `"zh-CN"` |

## 使用方式

1. **认证**：所有 Billing API 请求需携带有效的 `Authorization` 请求头（如 Bearer Token），具体鉴权方式参见平台统一认证文档。
2. **构造请求**：
   - `GetBillingOverview`：`GET /modelstudio/billing/overview?billMonth=2026-08&groupBy=[{"code":"MAAS_TYPE"}]&locale=zh-CN`
   - `GetBillingTrend`：`GET /modelstudio/billing/trend?granularity=DAY&timePeriod.start=2026-08-01&timePeriod.end=2026-08-31&groupBy=[{"code":"BASE_MODEL"}]`
   > **注意**：`groupBy` 和 `filter.dimensions` 为 JSON 对象数组，需进行 URL 编码（如 `%5B%7B%22code%22%3A%22MAAS_TYPE%22%7D%5D`），建议使用 SDK 或标准 HTTP 客户端自动处理。
3. **解析响应**：关注 `success` 字段判断调用结果；费用金额字段（如 `amount`、`pretaxAmount`）均为字符串类型，需转换为数值后参与计算；币种由 `currency` 字段标识，不同账单周期可能返回不同币种（如 `USD` 或 `CNY`）。

## 限制和注意事项

- **分组约束**：两个接口均强制要求 `groupBy` 数组长度为 1，不支持多维度嵌套分组（如同时按 `MAAS_TYPE` 和 `BASE_MODEL` 分组）。
- **时间范围限制**：`GetBillingTrend` 的 `timePeriod.end` 不能晚于当前日期，且最大跨度为 90 天（`DAY` 粒度）或 12 个月（`MONTH` 粒度）；超出将返回错误。
- **空值处理**：`filter.dimensions.values` 中传入 `DIMENSION_FILTER_NULL_VALUE` 可匹配数据库中为 NULL 或空字符串的记录，该行为在两篇文档中定义一致，可安全使用。
- **金额精度**：所有金额字段（`amount`、`pretaxAmount`、`taxAmount`）为字符串，保留小数点后两位，**不可直接用浮点数解析**，避免精度丢失；建议使用高精度 Decimal 类型或字符串运算。
- **地域隔离**：若未显式传入 `regionId`，接口默认返回用户主地域账单数据；跨地域账单需显式指定 `regionId`，否则可能遗漏数据。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


