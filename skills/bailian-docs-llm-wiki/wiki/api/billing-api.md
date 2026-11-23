# billing api

Billing API 提供账单数据查询能力，支持按月获取费用总览（`GetBillingOverview`）和按时间范围获取费用趋势（`GetBillingTrend`）。所有接口均基于 RESTful 设计，通过 HTTPS 调用，返回结构化 JSON 响应。该 API 适用于开发者集成至内部财务看板、成本分析工具或自动化对账系统。

## 支持的模型/功能

Billing API 当前提供两个核心接口：

- `GetBillingOverview`：查询**单个月份**的账单总览，返回按指定维度聚合的 TopN 分组费用及全局合计（含税/不含税/币种）。适用于月度成本复盘与概览展示。  
- `GetBillingTrend`：查询**指定起止日期范围内**的账单趋势，支持按 `DAY` 或 `MONTH` 粒度聚合，并返回各周期内分组明细及整体费用分布。适用于成本波动监控与归因分析。

两接口均支持相同的维度体系（如 `MAAS_TYPE`、`BASE_MODEL`、`API_KEY_ID` 等）进行分组与过滤，详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 和 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 的补充说明章节。

> **注意**：文档中 `filter.dimensions[].values` 均可传 `DIMENSION_FILTER_NULL_VALUE` 表示匹配空值，但实际调用时需确保该字符串字面量（而非 `null`）被正确序列化为 JSON 字符串；否则可能被服务端忽略。该行为在 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 示例中未显式体现，建议以 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 的说明为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `billMonth`（仅 `GetBillingOverview`） | string | 是 | 账单月份，格式 `YYYY-MM` | `"2026-08"` |
| `granularity`（仅 `GetBillingTrend`） | string | 是 | 聚合粒度：`DAY` 或 `MONTH` | `"DAY"` |
| `timePeriod.start` / `timePeriod.end`（仅 `GetBillingTrend`） | string | 是 | 查询起止日期，格式 `YYYY-MM-DD`；`end` 可等于 `start` | `"2026-08-01"`, `"2026-08-31"` |
| `groupBy` | array<object> | 是 | 分组条件，**必须且仅能包含一个元素**；`code` 值须从标准维度列表中选取 | `[{"code": "MAAS_TYPE"}]` |
| `filter.dimensions` | array<object> | 否 | 维度过滤器，支持多维组合；每个 `dimensions` 对象需指定 `code`、`values` 和 `selectType` | `[{"code":"BASE_MODEL","values":["qwen-plus"],"selectType":"IN"}]` |
| `topNum` | integer | 否 | 返回分组数量（1–20），默认 20；超出部分合并为“其他” | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组，默认 `true` | `false` |
| `regionId` / `locale` | string | 否 | 地域 ID 与返回语言（`zh-CN`/`en-US`），影响 `name` 字段展示 | `"cn-beijing"`, `"zh-CN"` |

## 使用方式

1. **认证**：所有请求需携带有效的 Bearer Token（通过百炼平台 AccessKey 签名生成，具体鉴权流程参见平台通用认证文档）。
2. **Endpoint**：
   - `GET /modelstudio/billing/overview` → `GetBillingOverview`
   - `GET /modelstudio/billing/trend` → `GetBillingTrend`
3. **构造请求**：将参数作为 query string 附加（如 `?billMonth=2026-08&groupBy[0].code=MAAS_TYPE&locale=zh-CN`），注意 URL 编码。
4. **解析响应**：
   - 共同字段：`requestId`（用于问题排查）、`code`（HTTP 状态码语义等效）、`success`（业务成功标识）。
   - `GetBillingOverview` 主要关注 `data.totalAmount` 和 `data.groups` 数组；
   - `GetBillingTrend` 需结合 `data.resultByTime`（时间序列明细）与 `data.groupByTotal`（全局分组汇总）使用。

## 限制和注意事项

- **时间范围限制**：`GetBillingTrend` 的 `timePeriod` 最大跨度为 90 天（`end - start ≤ 90 days`），超出将返回 `400` 错误。
- **分组约束**：`groupBy` 严格限定为单维度，传入多个元素将导致 `400`；不支持嵌套或多级分组。
- **空值处理**：`filter.dimensions[].values` 中传入 `"DIMENSION_FILTER_NULL_VALUE"` 可匹配数据库中 `NULL` 或空字符串字段，但该字符串**不可加引号转义为 JSON 字符串字面量以外的形式**（例如不能传 `["\"DIMENSION_FILTER_NULL_VALUE\""]`）。
- **货币单位**：返回的 `currency` 字段取决于账户结算币种，同一账户下不同月份/周期可能返回不同币种（如 `USD`/`CNY`），客户端需兼容处理。
- **精度说明**：所有 `amount`、`pretaxAmount`、`taxAmount` 字段均为字符串类型，保留两位小数，**禁止直接转为浮点数计算**，应使用高精度 decimal 库解析。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


