# billing api

billing api 提供账单数据查询能力，支持按时间趋势分析和月度总览两种核心场景。开发者可通过标准 RESTful 接口获取分组聚合、维度筛选后的费用明细，适用于成本监控、资源归因与财务对账等生产需求。所有接口均需通过百炼平台 API Key 进行身份认证，并遵循统一的错误码与分页规范。

## 支持的模型/功能

- `GetBillingTrend`：查询指定时间范围内（支持 DAY/MONTH 粒度）的账单趋势，返回按周期拆分的费用分布及 TopN 分组汇总，适用于趋势分析与波动诊断。详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)。
- `GetBillingOverview`：查询单个月份（格式 `YYYY-MM`）的账单总览，返回该月费用合计、TopN 分组金额及占比，适用于月度结算与概览报表。详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)。

> **注意**：两接口均要求 `groupBy` 参数必须且仅能传入一个维度对象，但 `GetBillingOverview` 的返回结构中 `data.groups` 不包含 `pretaxAmount` 和 `taxAmount` 字段，而 `GetBillingTrend` 在 `data.groupByTotal` 和 `data.resultByTime.periodDetails` 中均提供完整税额拆分。实际开发中若需精确税务分析，应优先使用 `GetBillingTrend`。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `granularity`（仅 `GetBillingTrend`） | string | 是 | 时间粒度，取值 `DAY` 或 `MONTH` | `DAY` |
| `billMonth`（仅 `GetBillingOverview`） | string | 是 | 账单月份，格式 `YYYY-MM` | `2026-08` |
| `timePeriod.start` / `timePeriod.end`（仅 `GetBillingTrend`） | string | 是 | 查询起止日期，格式 `YYYY-MM-DD`，最大跨度 366 天 | `2026-08-01`, `2026-08-31` |
| `groupBy[].code` | string | 是 | 分组维度 Code，大小写敏感，建议全大写。支持 `MAAS_TYPE`, `BASE_MODEL`, `API_KEY_ID`, `WORKSPACE_ID`, `FEE_TYPE`, `CHARGE_TYPE`, `BUSINESS_REGION`, `SERVICE_SITE`, `ARTICLE_CODE` | `BASE_MODEL` |
| `filter.dimensions` | array<object> | 否 | 维度过滤条件，每个元素含 `code`, `values`, `selectType`；`values` 可含 `DIMENSION_FILTER_NULL_VALUE` 表示匹配空值 | `[{"code":"BASE_MODEL","values":["qwen-plus"],"selectType":"IN"}]` |
| `topNum` | integer | 否 | 返回 TopN 分组数量，范围 1–20，默认 20 | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组，默认 `true` | `false` |
| `locale` | string | 否 | 返回语言，`zh-CN`（中文）或 `en-US`（英文），影响 `name` 字段展示 | `zh-CN` |

## 使用方式

1. **认证**：在请求 Header 中携带 `Authorization: Bearer <API_KEY>`。
2. **构造请求**：
   - `GetBillingTrend`：`GET /modelstudio/billing/trend?granularity=DAY&timePeriod.start=2026-08-01&timePeriod.end=2026-08-31&groupBy[0].code=BASE_MODEL`
   - `GetBillingOverview`：`GET /modelstudio/billing/overview?billMonth=2026-08&groupBy[0].code=MAAS_TYPE`
3. **解析响应**：检查 `success` 字段为 `true` 且 `code` 为 `"200"`；费用金额均为字符串类型（含小数），需按业务逻辑转为数值处理；币种由 `currency` 字段明确标识（如 `CNY`, `USD`）。
4. **错误处理**：常见错误包括 `400 Bad Request`（参数校验失败）、`401 Unauthorized`（认证失败）、`403 Forbidden`（权限不足）。详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 和 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 的错误码说明。

## 限制和注意事项

- 时间范围限制：`GetBillingTrend` 最大支持 366 天跨度，超出将返回 `400` 错误。
- 维度一致性：`groupBy[].code` 与 `filter.dimensions[].code` 必须从同一维度集合中选取，不支持跨维度组合（如同时按 `BASE_MODEL` 分组、按 `WORKSPACE_ID` 过滤）。
- 空值处理：所有维度字段均可传 `DIMENSION_FILTER_NULL_VALUE` 表示匹配 NULL 或空字符串，但 `groupBy[].code` 本身不可为空。
- 币种差异：`GetBillingTrend` 默认返回 `CNY`，`GetBillingOverview` 示例中为 `USD`，实际币种取决于账户结算配置，**不可硬编码假设**。
- 数据延迟：账单数据通常有最多 24 小时延迟，非实时更新。

## 来源文档

- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)
- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)


