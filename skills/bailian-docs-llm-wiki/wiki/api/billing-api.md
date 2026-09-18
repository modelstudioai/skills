# billing api

Billing API 提供账单数据查询能力，支持按月获取费用总览（`GetBillingOverview`）和按时间范围获取费用趋势（`GetBillingTrend`）。两个接口均基于 RESTful 设计，通过标准 HTTP GET 请求调用，返回结构化 JSON 数据。所有接口均需通过百炼平台认证鉴权，适用于成本分析、用量监控与财务对账等场景。

## 支持的模型/功能

Billing API 当前提供两类核心功能：
- `GetBillingOverview`：查询**单个月份**的账单总览，返回按指定维度聚合的 TopN 分组费用及占比，适用于月度成本概览分析。详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)。
- `GetBillingTrend`：查询**连续时间段内**（按天或按月粒度）的费用趋势，返回分周期、分组的明细金额与税费，支持多维下钻分析。详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)。

> **注意**：两接口均仅支持单维度分组（`groupBy` 数组长度必须为 1），且不支持嵌套分组或多维度联合聚合。如需交叉分析（如“按模型+地域”），需在客户端自行聚合。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `billMonth`（仅 `GetBillingOverview`） | string | 是 | 账单月份，格式 `YYYY-MM` | `"2026-08"` |
| `granularity`（仅 `GetBillingTrend`） | string | 是 | 时间粒度，取值 `DAY` 或 `MONTH` | `"DAY"` |
| `timePeriod.start` / `timePeriod.end`（仅 `GetBillingTrend`） | string | 是 | 查询起止日期，格式 `YYYY-MM-DD`；`end` 可等于 `start` | `"2026-08-01"`, `"2026-08-31"` |
| `groupBy[].code` | string | 是 | 分组维度 Code，**必须且仅能传一个**。支持值包括 `MAAS_TYPE`, `BASE_MODEL`, `API_KEY_ID`, `WORKSPACE_ID`, `FEE_TYPE`, `CHARGE_TYPE`, `BUSINESS_REGION`, `SERVICE_SITE`, `ARTICLE_CODE` | `"BASE_MODEL"` |
| `filter.dimensions` | array<object> | 否 | 维度过滤条件，每个元素含 `code`、`values`、`selectType`（`IN`/`NOT`） | `[{"code":"BASE_MODEL","values":["qwen-max"],"selectType":"IN"}]` |
| `topNum` | integer | 否 | 返回 TopN 分组数量（1–20），默认 20；超出部分在 `GetBillingTrend` 中合并为“其他” | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组，默认 `true` | `false` |
| `regionId` | string | 否 | 地域 ID，用于限定账单数据范围 | `"cn-beijing"` |
| `locale` | string | 否 | 返回语言，`zh-CN`（中文）或 `en-US`（英文），影响 `name` 字段展示 | `"zh-CN"` |

所有维度的 `filter.dimensions[].values` 均可传特殊值 `DIMENSION_FILTER_NULL_VALUE` 表示匹配 NULL 或空字符串字段。

## 使用方式

1. **构造请求 URL**  
   - `GetBillingOverview`: `GET /modelstudio/billing/overview?billMonth=2026-08&groupBy[0].code=MAAS_TYPE&locale=zh-CN`  
   - `GetBillingTrend`: `GET /modelstudio/billing/trend?granularity=DAY&timePeriod.start=2026-08-01&timePeriod.end=2026-08-31&groupBy[0].code=BASE_MODEL`

2. **添加认证头**（如 Bearer Token 或 AK/SK 签名，具体见平台鉴权文档）

3. **解析响应**  
   - 共同字段：`requestId`, `code`, `success`, `message`, `data`  
   - `GetBillingOverview` 主要关注 `data.groups`（分组列表）和 `data.totalAmount`（总额）  
   - `GetBillingTrend` 主要关注 `data.resultByTime`（时间序列）、`data.groupByTotal`（分组汇总）和 `data.costTotals`（总计）  

4. **错误处理**  
   响应 `code ≠ "200"` 或 `success === false` 时，依据 `message` 字段定位问题（如参数格式错误、权限不足、账单数据未就绪等）。

## 限制和注意事项

- **时间范围限制**：`GetBillingTrend` 的 `timePeriod` 最大跨度为 90 天（`DAY` 粒度）或 12 个月（`MONTH` 粒度）；超出将返回 400 错误。
- **数据延迟**：账单数据通常有 24–48 小时延迟，查询当日或次日账单可能返回空或不完整结果。
- **币种一致性**：单次请求返回的所有金额字段（`amount`, `pretaxAmount`, `taxAmount`）使用同一币种（`currency` 字段），但不同账户/地域可能返回不同币种（如 `USD` 或 `CNY`），**不可直接跨请求加总**。
- **空值处理**：当 `filter.dimensions[].values` 包含 `DIMENSION_FILTER_NULL_VALUE` 时，该条件匹配字段为 NULL 或空字符串的数据；但 `groupBy[].code` 不支持此值作为分组维度。
- > **注意**：文档 1 中 `GetBillingOverview` 示例返回的 `data.groups.percentage` 为字符串（如 `"0.10"`），而文档 2 中 `GetBillingTrend` 的 `periodDetails.percentage` 同样为字符串但精度更高（如 `"0.6667"`）。二者语义一致（占当前分组/周期的比例），但计算逻辑独立，**不可混用公式推导**。实际使用请以各接口返回值为准，勿自行转换。详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 与 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 的返回参数定义。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


