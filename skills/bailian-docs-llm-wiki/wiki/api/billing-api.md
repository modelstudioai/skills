# billing api

Billing API 提供账单数据查询能力，支持按月获取费用总览（`GetBillingOverview`）和按时间范围获取费用趋势（`GetBillingTrend`）。所有接口均基于 RESTful 设计，使用 HTTPS 协议，需通过 API Key 进行身份认证。返回数据包含金额、税费、币种及多维度分组统计，适用于成本分析、用量监控与财务对账等场景。

## 支持的模型/功能

Billing API 当前提供两个核心功能：

- `GetBillingOverview`：查询**单个月份**的账单总览，返回按指定维度聚合的 TopN 分组及其金额占比。适用于快速掌握某月费用构成。详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)。
- `GetBillingTrend`：查询**连续时间范围内**（按天或按月粒度）的费用趋势，返回各周期内分组明细及累计汇总。适用于用量波动分析与预算跟踪。详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)。

> **注意**：两文档均声明 `groupBy` 必须且只能传入一个维度，但未明确禁止空数组或重复 code；实际调用时若传入多个 `groupBy` 元素将返回 400 错误。该约束在 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 的“请求参数”中被显式强调，而 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 仅在描述中提及，建议以 `GetBillingTrend` 文档为准并严格校验输入。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `billMonth`（仅 `GetBillingOverview`） | string | 是 | 账单月份，格式 `YYYY-MM` | `2026-08` |
| `granularity`（仅 `GetBillingTrend`） | string | 是 | 时间粒度：`DAY` 或 `MONTH` | `DAY` |
| `timePeriod.start` / `.end`（仅 `GetBillingTrend`） | string | 是 | 查询起止日期，格式 `YYYY-MM-DD` | `2026-08-01`, `2026-08-31` |
| `groupBy[].code` | string | 是 | 分组维度 Code，统一使用大写。支持值包括：`MAAS_TYPE`, `BASE_MODEL`, `API_KEY_ID`, `WORKSPACE_ID`, `FEE_TYPE`, `CHARGE_TYPE`, `BUSINESS_REGION`, `SERVICE_SITE`, `ARTICLE_CODE` | `BASE_MODEL` |
| `filter.dimensions[]` | array | 否 | 维度过滤条件，每个元素含 `code`, `values`, `selectType` | `[{"code":"BASE_MODEL","values":["qwen-max"],"selectType":"IN"}]` |
| `topNum` | integer | 否 | 返回分组数量（1–20），默认 20；超出部分合并为“其他” | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组，默认 `true` | `false` |
| `regionId` | string | 否 | 地域 ID，用于限定账单数据范围 | `cn-beijing` |
| `locale` | string | 否 | 返回语言：`zh-CN`（中文）或 `en-US`（英文），影响 `name` 字段展示 | `zh-CN` |

> **注意**：`filter.dimensions[].values` 可传特殊值 `DIMENSION_FILTER_NULL_VALUE` 表示匹配 NULL 或空字符串，该行为在两篇原始文档的“补充说明”中一致定义，但实际调用时需确保服务端已启用该特性（参见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 补充说明）。

## 使用方式

1. **认证**：在 HTTP Header 中携带 `Authorization: Bearer <API_KEY>`。
2. **构造请求**：
   - `GetBillingOverview`：`GET /modelstudio/billing/overview?billMonth=2026-08&groupBy[0].code=MAAS_TYPE&locale=zh-CN`
   - `GetBillingTrend`：`GET /modelstudio/billing/trend?granularity=DAY&timePeriod.start=2026-08-01&timePeriod.end=2026-08-31&groupBy[0].code=BASE_MODEL`
3. **解析响应**：
   - 成功时 `success: true`，费用金额均为字符串类型（含两位小数），需转为数值处理；
   - `data.currency` 标识币种（如 `CNY`, `USD`），不同账单周期可能混用；
   - `data.groups`（`GetBillingOverview`）与 `data.resultByTime`（`GetBillingTrend`）是核心业务数据结构，注意 `percentage` 为字符串格式的小数（如 `"0.10"`）。

## 限制和注意事项

- **时间范围限制**：`GetBillingTrend` 的 `timePeriod.end` 不能晚于当前日期；`timePeriod.start` 与 `end` 间隔最长支持 90 天（`DAY` 粒度）或 24 个月（`MONTH` 粒度）。
- **分组与筛选一致性**：`groupBy[].code` 和 `filter.dimensions[].code` 必须属于同一维度集合，不可跨类组合（例如不能 `groupBy.code=MAAS_TYPE` 同时 `filter.dimensions.code=WORKSPACE_ID`）。
- **空值处理**：当分组 key 为空时，返回 `DIMENSION_FILTER_NULL_VALUE`（如 `"key": "DIMENSION_FILTER_NULL_VALUE"`），前端需做兼容渲染。
- **精度与税额**：金额字段（`amount`, `pretaxAmount`, `taxAmount`）均为字符串，避免浮点运算误差；税费可能因地域政策动态计算，不可简单相减推导。
- **错误响应**：通用错误码（如 `400 Bad Request`, `401 Unauthorized`, `429 Too Many Requests`）遵循标准 HTTP 规范，具体业务错误见 `code` 与 `message` 字段。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


