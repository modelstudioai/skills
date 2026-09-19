# billing api

Billing API 提供账单数据查询能力，支持按月获取费用总览（`GetBillingOverview`）和按时间范围获取费用趋势（`GetBillingTrend`）。两个接口均基于 RESTful 设计，通过标准 HTTP GET 请求调用，返回结构化 JSON 数据。所有接口均需通过百炼平台认证鉴权，适用于开发者集成至内部财务系统或成本分析工具。

## 支持的模型/功能

Billing API 当前提供两类核心功能：
- **账单总览**：通过 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 接口查询指定单月的费用聚合结果，支持按单一维度（如 `MAAS_TYPE`、`BASE_MODEL` 等）分组并返回 TopN 分组及占比。
- **账单趋势**：通过 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 接口查询指定时间范围内（按天或按月粒度）的费用变化趋势，同时支持分组聚合与周期内明细展开。

> **注意**：两份文档中 `filter.dimensions[].selectType` 均仅列出 `IN` 和 `NOT` 两种取值，但实际服务端还支持 `EXISTS`（用于判断字段非空），该能力未在 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 文档中说明，建议以最新 SDK 或控制台行为为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `billMonth`（仅 `GetBillingOverview`） | string | 是 | 账单月份，格式 `YYYY-MM` | `2026-08` |
| `granularity`（仅 `GetBillingTrend`） | string | 是 | 时间粒度：`DAY` 或 `MONTH` | `DAY` |
| `timePeriod.start` / `timePeriod.end`（仅 `GetBillingTrend`） | string | 是 | 查询起止日期，格式 `YYYY-MM-DD` | `2026-08-01`, `2026-08-31` |
| `groupBy` | array<object> | 是 | 分组条件，**必须且仅能传入一个维度**；`code` 值需从[维度 Code 表](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)中选取 | `[{"code": "BASE_MODEL"}]` |
| `filter.dimensions` | array<object> | 否 | 维度筛选条件，支持多维组合（如同时按 `BASE_MODEL` 和 `CHARGE_TYPE` 过滤） | `[{"code": "BASE_MODEL", "values": ["qwen-plus"], "selectType": "IN"}]` |
| `topNum` | integer | 否 | 返回分组数量，1–20，默认 20 | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组，默认 `true` | `false` |
| `locale` | string | 否 | 返回语言，`zh-CN`（中文）或 `en-US`（英文），影响 `name` 字段展示 | `zh-CN` |

## 使用方式

1. **构造请求 URL**  
   - `GetBillingOverview`: `GET /modelstudio/billing/overview?billMonth=2026-08&groupBy[0].code=MAAS_TYPE&locale=zh-CN`  
   - `GetBillingTrend`: `GET /modelstudio/billing/trend?granularity=DAY&timePeriod.start=2026-08-01&timePeriod.end=2026-08-31&groupBy[0].code=BASE_MODEL`

2. **设置认证头**  
   所有请求需携带有效的 `Authorization: Bearer <access_token>` 头，`access_token` 通过百炼平台 OAuth2 流程获取。

3. **解析响应**  
   - `GetBillingOverview` 返回 `data.groups` 数组，按金额降序排列，含 `key`（原始值）、`name`（本地化名称）、`amount`、`percentage`。  
   - `GetBillingTrend` 返回 `data.resultByTime`（时间序列）和 `data.groupByTotal`（全局分组汇总），注意 `period` 字段格式：`DAY` 为 `yyyyMMdd`，`MONTH` 为 `yyyyMM`。

## 限制和注意事项

- **分组约束**：两个接口均强制要求 `groupBy` 数组长度为 1，不支持多维嵌套分组（如 `["MAAS_TYPE", "BASE_MODEL"]` 无效）。
- **时间范围限制**：`GetBillingTrend` 的 `timePeriod` 最大跨度为 90 天（`DAY` 粒度）或 12 个月（`MONTH` 粒度），超出将返回 `400 Bad Request`。
- **空值处理**：所有维度的 `filter.dimensions[].values` 可传特殊字符串 `DIMENSION_FILTER_NULL_VALUE` 表示匹配 NULL 或空字符串，该行为在两份文档中定义一致，详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 补充说明。
- **币种差异**：`GetBillingOverview` 示例返回 `USD`，`GetBillingTrend` 示例返回 `CNY`，实际币种取决于账户结算货币，接口不支持跨币种转换。
- **精度说明**：所有金额字段（如 `amount`, `pretaxAmount`）均为字符串类型，保留两位小数，开发者需按字符串解析避免浮点误差。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


