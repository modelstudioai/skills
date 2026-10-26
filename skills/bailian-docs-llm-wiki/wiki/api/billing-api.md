# billing api

Billing API 提供账单数据查询能力，支持按月获取费用总览（`GetBillingOverview`）和按时间范围获取费用趋势（`GetBillingTrend`）。所有接口均基于 RESTful 设计，通过 HTTPS 调用，返回结构化 JSON 响应。该 API 适用于开发者集成至内部财务看板、成本分析系统或自动化对账流程。

## 支持的模型/功能

Billing API 当前提供两个核心功能接口：

- `GetBillingOverview`：查询**单个月份**的账单总览，返回按指定维度聚合的 TopN 分组费用及占比，适用于月度成本复盘与归因分析。详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)。
- `GetBillingTrend`：查询**指定起止日期范围内**（支持 DAY/MONTH 粒度）的费用趋势，返回分周期、分组的明细金额与税费拆分，适用于成本波动监控与预测。详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)。

> **注意**：两接口均要求 `groupBy` 数组**必须且仅含一个元素**，不支持多维嵌套分组；文档中未提及但实际调用时若传入多个 `groupBy` 元素，将返回 `400 Bad Request` 错误。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `billMonth`（仅 `GetBillingOverview`） | string | 是 | 账单月份，格式 `YYYY-MM` | `2026-08` |
| `granularity`（仅 `GetBillingTrend`） | string | 是 | 时间粒度，取值 `DAY` 或 `MONTH` | `DAY` |
| `timePeriod.start` / `.end`（仅 `GetBillingTrend`） | string | 是 | 查询起止日期，格式 `YYYY-MM-DD`；`end` 需 ≥ `start`，且跨度 ≤ 90 天（`DAY`）或 ≤ 24 个月（`MONTH`） | `2026-08-01`, `2026-08-31` |
| `groupBy[].code` | string | 是 | 分组维度 Code，统一使用大写；两接口支持完全相同的维度列表（如 `MAAS_TYPE`, `BASE_MODEL`, `API_KEY_ID` 等），详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 补充说明部分 |
| `filter.dimensions` | array | 否 | 维度过滤条件，支持 `IN`/`NOT` 语义；各维度 `values` 可传 `DIMENSION_FILTER_NULL_VALUE` 匹配空值 | `[{"code": "BASE_MODEL", "values": ["qwen-plus"], "selectType": "IN"}]` |
| `topNum` | integer | 否 | 返回 TopN 分组数（1–20，默认 20）；超出部分在 `GetBillingTrend` 中合并为“其他”，`GetBillingOverview` 中直接截断 |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组（默认 `true`） |

## 使用方式

1. **认证**：所有请求需携带有效的 `Authorization` Header（如 Bearer [Token](../concepts/token.md)），具体鉴权方式参见平台通用认证文档。
2. **Endpoint**：
   - `GET /modelstudio/billing/overview` → `GetBillingOverview`
   - `GET /modelstudio/billing/trend` → `GetBillingTrend`
3. **示例请求（curl）**：
   ```bash
   curl -X GET \
     "https://dashscope.aliyuncs.com/modelstudio/billing/overview?billMonth=2026-08&groupBy[0].code=MAAS_TYPE&filter.dimensions[0].code=BASE_MODEL&filter.dimensions[0].values[0]=qwen-plus&filter.dimensions[0].selectType=IN&locale=zh-CN" \
     -H "Authorization: Bearer YOUR_TOKEN"
   ```
4. **响应解析**：关注 `data` 字段下的结构差异：
   - `GetBillingOverview` 返回 `data.groups[]`（分组列表）和汇总金额（`totalAmount`, `pretaxAmount`, `taxAmount`）；
   - `GetBillingTrend` 返回 `data.resultByTime[]`（时间序列）、`data.groupByTotal[]`（分组汇总）和 `data.costTotals`（全局合计）。

## 限制和注意事项

- **时间范围限制**：`GetBillingTrend` 的 `timePeriod` 跨度严格受限——`DAY` 粒度最大 90 天，`MONTH` 粒度最大 24 个月；超出将返回 `400` 错误。
- **币种一致性**：单次响应中所有金额字段（`amount`, `pretaxAmount`, `taxAmount`）的 `currency` 值**始终相同**，但不同账户/地域可能返回 `USD` 或 `CNY`，不可预设。
- **空值处理**：当 `filter.dimensions[].values` 包含 `DIMENSION_FILTER_NULL_VALUE` 时，匹配对应维度为空或 `NULL` 的账单记录；该行为在两接口中一致，详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 补充说明。
- > **注意**：`GetBillingOverview` 文档示例中 `message` 字段值为 `"null"`（字符串），而 `GetBillingTrend` 示例中为 `null`（JSON null）；实际生产环境以 `message` 字段是否为 `null` 判断业务错误，非空字符串表示具体错误提示，不应依赖字面值 `"null"` 做逻辑判断。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


