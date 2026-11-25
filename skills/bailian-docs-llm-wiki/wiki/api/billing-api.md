# billing api

Billing API 提供账单数据查询能力，支持按月获取费用总览（`GetBillingOverview`）和按时间趋势分析（`GetBillingTrend`），适用于成本监控、分账统计与用量审计等场景。所有接口均基于 RESTful 设计，需通过 HTTPS 调用并携带有效认证凭证。返回数据为 JSON 格式，金额字段均为字符串类型以避免浮点精度问题。

## 支持的模型/功能

Billing API 当前提供两类核心能力：

- **账单总览**：通过 [`GetBillingOverview`](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 查询指定月份的聚合费用概览，支持按单一维度（如 `MAAS_TYPE`、`BASE_MODEL` 等）分组，并可叠加多维过滤。
- **账单趋势**：通过 [`GetBillingTrend`](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 查询指定时间范围内（按天或按月粒度）的费用变化趋势，返回周期级明细及分组汇总，适用于用量波动分析。

> **注意**：两文档中 `groupBy` 均明确要求“必须且只能传入一个分组维度”，但 `filter.dimensions` 支持传入多个维度对象；实际调用时若传入多个 `groupBy` 元素将被服务端拒绝（HTTP 400）。该约束在 [`GetBillingTrend`](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 文档中未加粗强调，易被忽略，应以 [`GetBillingOverview`](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 的明确表述为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| `billMonth`（仅 `GetBillingOverview`） | string | 是 | 账单月份，格式 `YYYY-MM` | `"2026-08"` |
| `granularity`（仅 `GetBillingTrend`） | string | 是 | 聚合粒度：`DAY` 或 `MONTH` | `"DAY"` |
| `timePeriod.start` / `.end`（仅 `GetBillingTrend`） | string | 是 | 查询起止日期，格式 `YYYY-MM-DD` | `"2026-08-01"`, `"2026-08-31"` |
| `groupBy[].code` | string | 是 | 分组维度 Code，**必须且仅能传一个**；支持 `MAAS_TYPE`、`BASE_MODEL`、`API_KEY_ID`、`WORKSPACE_ID`、`FEE_TYPE`、`CHARGE_TYPE`、`BUSINESS_REGION`、`SERVICE_SITE`、`ARTICLE_CODE` | `"BASE_MODEL"` |
| `filter.dimensions[]` | array<object> | 否 | 过滤维度列表，每个元素含 `code`、`values`（支持 `DIMENSION_FILTER_NULL_VALUE`）、`selectType`（`IN`/`NOT`） | `[{"code":"BASE_MODEL","values":["qwen-plus"],"selectType":"IN"}]` |
| `topNum` | integer | 否 | 返回 TopN 分组数量（1–20），默认 20；超出部分在 `GetBillingTrend` 中合并为“其他” | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组，默认 `true` | `false` |
| `regionId` | string | 否 | 地域 ID，用于限定账单归属地域 | `"cn-beijing"` |
| `locale` | string | 否 | 返回语言，`zh-CN`（中文）或 `en-US`（英文），影响 `name` 字段展示 | `"zh-CN"` |

## 使用方式

- **请求方法**：均为 `GET`
- **Endpoint**：
  - 总览：`GET /modelstudio/billing/overview`
  - 趋势：`GET /modelstudio/billing/trend`
- **认证**：需在请求 Header 中携带有效的 `Authorization`（如 Bearer [Token](../concepts/token.md)）及 `x-acs-region-id`（若涉及多地域）
- **示例调用（curl）**：
  ```bash
  curl -X GET \
    "https://dashscope.aliyuncs.com/modelstudio/billing/overview?billMonth=2026-08&groupBy[0].code=MAAS_TYPE&filter.dimensions[0].code=BASE_MODEL&filter.dimensions[0].values=qwen-plus&filter.dimensions[0].selectType=IN&locale=zh-CN" \
    -H "Authorization: Bearer YOUR_TOKEN"
  ```

## 限制和注意事项

- **时间范围限制**：`GetBillingTrend` 的 `timePeriod` 最大跨度为 90 天（`DAY` 粒度）或 12 个月（`MONTH` 粒度）；超出将返回 `400 Bad Request`。
- **分组唯一性**：`groupBy` 数组长度**严格限定为 1**，传入多个元素会导致请求失败；该规则在两份原始文档中一致，但 [`GetBillingTrend`](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 的描述略显模糊，建议开发者始终校验数组长度。
- **空值处理**：所有 `filter.dimensions[].values` 支持特殊值 `DIMENSION_FILTER_NULL_VALUE`，用于匹配 NULL 或空字符串字段，该行为在两文档中定义完全一致。
- **金额精度**：所有 `amount`、`pretaxAmount`、`taxAmount` 字段均为字符串，**不可直接转为 float 计算**，应使用高精度 decimal 库解析。
- **地域一致性**：`regionId` 参数仅用于筛选账单归属地域，不影响 API 接入点；实际调用需确保 endpoint 与所选 region 匹配（如 `cn-beijing` 对应 `dashscope.aliyuncs.com`）。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


