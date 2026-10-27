# billing api

billing api 提供账单数据查询能力，支持按时间趋势分析和月度总览两种核心场景。开发者可通过标准 RESTful 接口获取分组聚合、维度筛选后的费用明细，适用于成本监控、用量分析与财务对账等生产需求。所有接口均需通过百炼平台认证鉴权，并遵循统一的错误码与分页规范。

## 支持的模型/功能

- `GetBillingTrend`：查询指定时间范围内（支持 DAY/MONTH 粒度）的账单趋势，返回按周期拆分的费用分布及 TopN 分组汇总，适用于趋势分析与波动诊断。详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)。
- `GetBillingOverview`：查询指定月份（YYYY-MM 格式）的账单总览，返回当月费用合计与按单一维度分组的 TopN 占比，适用于月度结算与资源归因。详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)。

> **注意**：两接口均要求 `groupBy` 参数必须且仅能传入一个维度对象，但 `GetBillingOverview` 的返回结构中 `data.groups` 不包含税费拆分字段（如 `pretaxAmount`/`taxAmount`），而 `GetBillingTrend` 在 `data.groupByTotal` 和 `data.resultByTime.periodDetails` 中均提供完整税项字段。实际开发中若需精确税务分析，应优先使用 `GetBillingTrend`。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `granularity`（仅 `GetBillingTrend`） | string | 是 | 时间粒度，取值 `DAY` 或 `MONTH` | `DAY` |
| `billMonth`（仅 `GetBillingOverview`） | string | 是 | 账单月份，格式 `YYYY-MM` | `2026-08` |
| `timePeriod.start` / `timePeriod.end`（仅 `GetBillingTrend`） | string | 是 | 查询起止日期，格式 `YYYY-MM-DD` | `2026-08-01`, `2026-08-31` |
| `groupBy[].code` | string | 是 | 分组维度 Code，大小写敏感，建议全大写 | `BASE_MODEL`, `MAAS_TYPE` |
| `filter.dimensions` | array<object> | 否 | 维度过滤条件，支持 `IN`/`NOT` 逻辑 | `[{"code": "BASE_MODEL", "values": ["qwen-plus"], "selectType": "IN"}]` |
| `topNum` | integer | 否 | 返回 TopN 分组数，范围 1–20，默认 20 | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组，默认 `true` | `false` |
| `locale` | string | 否 | 返回语言，`zh-CN` 或 `en-US`，影响 `name` 字段展示 | `zh-CN` |

所有维度 Code（如 `BASE_MODEL`, `API_KEY_ID`, `FEE_TYPE` 等）及其可选值详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 补充说明章节。

## 使用方式

1. **构造请求 URL**  
   - `GetBillingTrend`: `GET /modelstudio/billing/trend?granularity=DAY&timePeriod.start=2026-08-01&timePeriod.end=2026-08-31&groupBy[0].code=BASE_MODEL`  
   - `GetBillingOverview`: `GET /modelstudio/billing/overview?billMonth=2026-08&groupBy[0].code=MAAS_TYPE`

2. **设置请求头**  
   - `Authorization: Bearer <access_token>`  
   - `Content-Type: application/json`

3. **解析响应**  
   - 成功时 `success === true`，费用金额均为字符串类型（含小数位），需按业务需要转为数值处理。  
   - `currency` 字段标识币种（如 `CNY`, `USD`），不同接口默认值可能不同，不可硬编码假设。

## 限制和注意事项

- 时间范围限制：`GetBillingTrend` 最大支持 90 天跨度；`GetBillingOverview` 仅支持单月查询，不支持跨月。
- 维度一致性：`groupBy[].code` 与 `filter.dimensions[].code` 必须属于同一维度集合，且大小写需严格匹配文档定义（如 `MAAS_TYPE` 不可写作 `maas_type`）。
- 空值处理：所有维度过滤均支持 `DIMENSION_FILTER_NULL_VALUE` 字符串作为 `values` 元素，用于匹配 NULL 或空字符串字段。
- 币种差异：`GetBillingTrend` 示例返回 `CNY`，而 `GetBillingOverview` 示例返回 `USD`；实际币种取决于账户结算配置，**不可依赖示例值**，必须解析响应中的 `currency` 字段。
- 分组数量：`topNum` 超出实际分组数时，返回全部分组；若设为 1 且存在大量低价值分组，可能掩盖长尾分布，建议结合 `zeroFilter=false` 调试。

## 来源文档

- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)
- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)


