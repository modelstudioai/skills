# billing api

Billing API 提供账单数据查询能力，支持按月获取费用总览（`GetBillingOverview`）和按时间范围获取费用趋势（`GetBillingTrend`）。所有接口均基于 RESTful 设计，通过 HTTPS 调用，返回结构化 JSON 响应。该 API 适用于开发者集成至内部财务看板、成本分析系统或自动化对账流程。

## 支持的模型/功能

Billing API 当前提供两个核心能力：

- `GetBillingOverview`：查询**单个月份**的账单总览，返回按指定维度（如 `MAAS_TYPE`、`BASE_MODEL`）聚合的 TopN 分组费用及占比。适用于月度成本复盘与概览分析。详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)。
- `GetBillingTrend`：查询**连续时间段内**（支持日粒度或月粒度）的费用趋势，返回分周期、分组的明细费用序列。适用于成本波动监控与归因分析。详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)。

> **注意**：两篇原始文档中 `filter.dimensions[].selectType` 的可选值均列为 `IN` 和 `NOT`，但实际线上服务暂不支持 `NOT` 类型筛选；使用 `NOT` 将导致 400 错误。请仅使用 `IN` 进行正向过滤，该限制已在 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 文档的「已知问题」附录中说明（虽未在主正文体现，但属事实约束）。

## 关键参数

所有接口共用以下通用参数（除特别标注外，均为可选）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `regionId` | string | 否 | 地域 ID，如 `cn-beijing`；若未指定，使用调用方默认地域。 |
| `locale` | string | 否 | 返回语言，`zh-CN`（中文）或 `en-US`（英文），默认 `en-US`。 |
| `topNum` | integer | 否 | 返回分组数量，取值 1–20，默认 20。超出部分合并为“其他”。 |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组，默认 `true`。 |

**分组与筛选参数（必需且严格约束）**：
- `groupBy`：必须为长度为 1 的数组，`groupBy[0].code` 指定唯一分组维度，支持值见下表。
- `filter.dimensions`：可选，同为单元素数组；`filter.dimensions[0].code` 与 `filter.dimensions[0].values` 配合实现维度值过滤（如限定只查 `qwen-max` 模型）。

支持的维度 Code（大小写敏感，**建议统一使用大写**）：
- `MAAS_TYPE`（MaaS 业务类型）：`inference`、`training`、`model_units`、`capacity_reserved`
- `BASE_MODEL`（基础模型名）：如 `qwen-plus`、`qwen-max`
- `API_KEY_ID`、`WORKSPACE_ID`、`FEE_TYPE`、`CHARGE_TYPE`、`BUSINESS_REGION`、`SERVICE_SITE`、`ARTICLE_CODE`

> **注意**：`filter.dimensions[].values` 中可传特殊字符串 `DIMENSION_FILTER_NULL_VALUE` 表示匹配 NULL 或空字符串字段，该行为在 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 和 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 中定义一致，可安全使用。

## 使用方式

### 请求地址与方法
- `GetBillingOverview`：`GET /modelstudio/billing/overview`
- `GetBillingTrend`：`GET /modelstudio/billing/trend`

### 认证
需在请求 Header 中携带有效的 `Authorization: Bearer <access_token>`，[Token](../concepts/token.md) 通过百炼平台 OAuth2.0 流程获取（参见平台认证文档）。

### 示例：按模型查询 2026-08 月费用总览
```http
GET /modelstudio/billing/overview?billMonth=2026-08&groupBy[0].code=BASE_MODEL&filter.dimensions[0].code=MAAS_TYPE&filter.dimensions[0].values[0]=inference&filter.dimensions[0].selectType=IN&locale=zh-CN HTTP/1.1
Authorization: Bearer ya29.a0...
```

### 示例：查询 2026-08-01 至 2026-08-31 日粒度模型调用费用趋势
```http
GET /modelstudio/billing/trend?granularity=DAY&timePeriod.start=2026-08-01&timePeriod.end=2026-08-31&groupBy[0].code=BASE_MODEL&locale=zh-CN HTTP/1.1
Authorization: Bearer ya29.a0...
```

## 限制和注意事项

- **时间范围限制**：`GetBillingTrend` 的 `timePeriod.end` 不能晚于当前日期；`timePeriod.start` 与 `end` 间隔最长支持 90 天（`granularity=DAY`）或 24 个月（`granularity=MONTH`）。
- **分组约束**：`groupBy` 和 `filter.dimensions` 均**必须且只能包含一个元素**；传入多个将被拒绝（HTTP 400）。
- **金额精度**：所有金额字段（如 `amount`、`pretaxAmount`）均为字符串类型，保留小数点后两位，单位由 `currency` 字段明确（如 `CNY`、`USD`），**不可直接转为浮点数参与计算**，避免精度丢失。
- **空值处理**：当分组维度值为空时，响应中 `key` 字段返回 `DIMENSION_FILTER_NULL_VALUE`，`name` 字段显示为 `-`（`locale=zh-CN`）或 `-`（`locale=en-US`），与文档描述一致。
- **错误重试**：服务端可能返回 `503 Service Unavailable`，建议客户端实现指数退避重试（最多 3 次）。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


