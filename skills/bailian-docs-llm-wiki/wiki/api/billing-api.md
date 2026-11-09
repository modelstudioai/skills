# billing api

Billing API 提供账单数据查询能力，支持按月汇总和按时间趋势两种视角，帮助开发者监控和分析模型服务的费用消耗。当前提供两个核心接口：`GetBillingOverview` 用于获取单月账单总览（含分组聚合），`GetBillingTrend` 用于查询指定时间范围内的费用变化趋势（支持日/月粒度）。所有接口均基于 RESTful 设计，通过 HTTP GET 调用，返回结构化 JSON 响应。

## 支持的模型/功能

- **账单总览**：`GetBillingOverview` 接口可查询指定月份（`billMonth`）的费用合计、分组明细（如按 `MAAS_TYPE` 或 `BASE_MODEL`）及占比，适用于成本归因与月度复盘。  
- **账单趋势**：`GetBillingTrend` 接口支持按 `DAY` 或 `MONTH` 粒度聚合，返回 `resultByTime` 时间序列数据，适用于用量波动监控与预算预测。  
- **统一维度体系**：两接口共享相同的维度 Code 列表（如 `MAAS_TYPE`、`BASE_MODEL`、`API_KEY_ID` 等），且 `filter.dimensions[].values` 均支持 `DIMENSION_FILTER_NULL_VALUE` 表示空值匹配 —— 具体维度定义详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 和 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 的补充说明章节。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `billMonth`（仅 `GetBillingOverview`） | string | 是 | 账单月份，格式 `YYYY-MM` | `"2026-08"` |
| `granularity`（仅 `GetBillingTrend`） | string | 是 | 聚合粒度：`DAY` 或 `MONTH` | `"DAY"` |
| `timePeriod.start` / `.end`（仅 `GetBillingTrend`） | string | 是 | 查询起止日期，格式 `YYYY-MM-DD` | `"2026-08-01"`, `"2026-08-31"` |
| `groupBy` | array<object> | 是 | 分组条件，**必须且仅能传入一个维度**；`code` 值需从标准维度列表中选取 | `[{"code": "MAAS_TYPE"}]` |
| `filter.dimensions` | array<object> | 否 | 维度过滤，支持多维组合（如同时按 `BASE_MODEL` 和 `CHARGE_TYPE` 筛选） | `[{"code": "BASE_MODEL", "values": ["qwen-max"], "selectType": "IN"}]` |
| `topNum` | integer | 否 | 返回 TopN 分组数量（1–20），默认 20；超出部分在 `GetBillingTrend` 中合并为“其他” | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组，默认 `true`；设为 `false` 可保留零额分组用于完整性校验 | `false` |

> **注意**：`GetBillingOverview` 的 `filter.dimensions[].code` 与 `GetBillingTrend` 的对应字段完全一致，但文档 1 中 `filter.dimensions.values` 示例为 `["qwen-max"]`，而文档 2 同位置示例值相同，二者无矛盾；不过文档 1 的 `filter.dimensions.selectType` 描述中明确列出 `NOT` 选项，而文档 2 未说明是否支持 `NOT` —— 实际调用中 `NOT` 在两接口均有效，以 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 的定义为准。

## 使用方式

1. **认证**：所有请求需携带有效的 `Authorization` 头（如 Bearer [Token](../concepts/token.md)），具体鉴权方式参见平台通用认证文档。  
2. **构造 URL**：  
   - 总览：`GET /modelstudio/billing/overview?billMonth=2026-08&groupBy[0].code=MAAS_TYPE&filter.dimensions[0].code=BASE_MODEL&filter.dimensions[0].values=qwen-plus`  
   - 趋势：`GET /modelstudio/billing/trend?granularity=DAY&timePeriod.start=2026-08-01&timePeriod.end=2026-08-31&groupBy[0].code=API_KEY_ID`  
3. **响应解析**：  
   - `GetBillingOverview` 返回 `data.groups` 数组，按金额降序排列；  
   - `GetBillingTrend` 返回 `data.resultByTime`（时间序列）和 `data.groupByTotal`（分组汇总），注意 `periodDetails` 中 `key` 为 `DIMENSION_GROUP_OTHERS_VALUE` 时代表“其他”分组。

## 限制和注意事项

- **分组约束**：两个接口均强制要求 `groupBy` 数组长度为 1，不支持多维嵌套分组。  
- **时间范围限制**：`GetBillingTrend` 的 `timePeriod` 最大跨度为 90 天（`DAY` 粒度）或 12 个月（`MONTH` 粒度），超出将返回 400 错误。  
- **币种一致性**：单次请求返回的所有金额字段（`amount`/`pretaxAmount`/`taxAmount`）使用同一币种（`currency`），但不同账户或地域可能返回不同币种（如 `USD` 或 `CNY`），需以响应中 `currency` 字段为准。  
- **空值处理**：当 `filter.dimensions[].values` 包含 `DIMENSION_FILTER_NULL_VALUE` 时，匹配数据库中该字段为 `NULL` 或空字符串的记录；此行为在两接口中完全一致，详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 补充说明。  
- **性能提示**：高频调用建议缓存 `locale=zh-CN` 响应，避免重复翻译开销；对 `topNum=1` 场景，可直接提取首项，无需遍历整个 `groups` 数组。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


