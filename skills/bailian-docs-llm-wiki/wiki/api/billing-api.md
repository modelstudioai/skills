# billing api

Billing API 提供账单数据查询能力，支持按月获取费用总览（`GetBillingOverview`）和按时间序列获取费用趋势（`GetBillingTrend`）。所有接口均基于 RESTful 设计，通过 HTTPS 调用，返回结构化 JSON 数据。开发者可结合分组（`groupBy`）、筛选（`filter`）和语言（`locale`）等参数灵活定制查询结果，适用于成本分析、用量监控与财务对账等场景。

## 支持的模型/功能

Billing API 当前提供两个核心接口：

- `GetBillingOverview`：查询**单个月份**的账单总览，返回按指定维度聚合的 TopN 分组金额及占比，适用于月度成本概览与归因分析。详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)。
- `GetBillingTrend`：查询**指定时间范围**（支持 DAY 或 MONTH 粒度）的账单趋势，返回分周期、分组的费用明细及汇总，适用于用量波动监测与趋势预测。详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)。

两个接口支持的维度 Code 完全一致（如 `MAAS_TYPE`、`BASE_MODEL`、`API_KEY_ID` 等），且均支持 `DIMENSION_FILTER_NULL_VALUE` 作为空值匹配标识。> **注意**：文档 1 和文档 2 中 `filter.dimensions.selectType` 的示例值均写为 `IN`，但未明确说明是否支持 `NOT` 的实际行为；建议在生产环境验证 `NOT` 类型筛选的语义一致性，避免因逻辑歧义导致漏查。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `billMonth`（仅 `GetBillingOverview`） | string | 是 | 账单月份，格式 `YYYY-MM` | `"2026-08"` |
| `granularity`（仅 `GetBillingTrend`） | string | 是 | 时间粒度，取值 `DAY` 或 `MONTH` | `"DAY"` |
| `timePeriod.start` / `.end`（仅 `GetBillingTrend`） | string | 是 | 查询起止日期，格式 `YYYY-MM-DD` | `"2026-08-01"`, `"2026-08-31"` |
| `groupBy` | array<object> | 是 | 分组条件，**必须且仅能传入一个维度**；`code` 字段需从标准维度列表中选择 | `[{"code": "MAAS_TYPE"}]` |
| `filter` | object | 否 | 维度过滤器，支持多维组合筛选 | `{"dimensions": [{"code": "BASE_MODEL", "values": ["qwen-max"], "selectType": "IN"}]}` |
| `topNum` | integer | 否 | 返回分组数量，范围 1–20，默认 20 | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组，默认 `true` | `false` |
| `regionId` | string | 否 | 地域 ID，用于限定账单数据范围 | `"cn-beijing"` |
| `locale` | string | 否 | 返回语言，`zh-CN`（中文）或 `en-US`（英文），影响 `name` 字段展示 | `"zh-CN"` |

> **注意**：两篇原始文档均明确要求 `groupBy` 数组长度必须为 1，但未说明传入多个元素时的错误码或降级行为；实际调用中应严格遵守单维度约束，否则可能触发 400 错误。该限制在 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 和 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 中保持一致。

## 使用方式

1. **认证**：所有 Billing API 请求需携带有效的 `Authorization` 头（如 Bearer Token），具体鉴权方式参见平台统一认证文档。
2. **构造请求**：
   - `GetBillingOverview`：`GET /modelstudio/billing/overview?billMonth=2026-08&groupBy[0].code=MAAS_TYPE&locale=zh-CN`
   - `GetBillingTrend`：`GET /modelstudio/billing/trend?granularity=DAY&timePeriod.start=2026-08-01&timePeriod.end=2026-08-31&groupBy[0].code=BASE_MODEL&filter.dimensions[0].code=MAAS_TYPE&filter.dimensions[0].values[]=inference`
3. **解析响应**：
   - `GetBillingOverview` 的核心数据位于 `data.groups`，按金额降序排列；
   - `GetBillingTrend` 的核心数据位于 `data.resultByTime`（时间序列）和 `data.groupByTotal`（全局分组汇总）。

## 限制和注意事项

- **时间范围限制**：`GetBillingTrend` 的 `timePeriod.end` 不能晚于当前日期；`timePeriod.start` 与 `end` 间隔最长支持 90 天（`DAY` 粒度）或 12 个月（`MONTH` 粒度）。
- **币种差异**：`GetBillingOverview` 示例返回 `USD`，而 `GetBillingTrend` 示例返回 `CNY`；实际币种取决于账户结算设置，**不支持跨币种强制转换**。
- **空值处理**：所有维度字段（如 `BASE_MODEL`）若原始账单数据为空，其值将映射为 `DIMENSION_FILTER_NULL_VALUE`，需在 `filter.dimensions.values` 中显式传入该字符串以匹配空值。
- **分组合并逻辑**：当 `topNum < 实际分组数` 时，`GetBillingTrend` 会将非 TopN 分组合并为 `DIMENSION_GROUP_OTHERS_VALUE`，而 `GetBillingOverview` 仅返回 TopN，无“其他”分组。
- **地域与站点一致性**：`regionId` 与 `SERVICE_SITE`、`BUSINESS_REGION` 等维度存在隐含关联，例如 `regionId=cn-beijing` 通常对应 `SERVICE_SITE=asia-pacific-china`；跨地域混用可能导致数据为空，建议优先使用 `regionId` 控制范围。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


