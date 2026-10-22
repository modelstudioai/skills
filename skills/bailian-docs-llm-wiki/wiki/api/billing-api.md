# billing api

Billing API 提供账单数据查询能力，支持按月获取费用总览（`GetBillingOverview`）和按时间范围获取费用趋势（`GetBillingTrend`）。所有接口均基于 RESTful 设计，通过 HTTPS 调用，返回结构化 JSON 响应。该 API 适用于开发者集成至内部财务看板、成本分析系统或自动化对账流程。

## 支持的模型/功能

Billing API 当前提供两个核心功能接口：

- `GetBillingOverview`：查询**单个月份**的账单总览，返回按指定维度（如 `MAAS_TYPE`、`BASE_MODEL` 等）聚合的 TopN 分组费用及占比。适用于月度成本复盘与概览分析。详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)。
- `GetBillingTrend`：查询**连续时间段内**（支持日粒度或月粒度）的费用趋势，返回分周期、分组的明细费用变化。适用于成本波动监控与归因分析。详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)。

> **注意**：两接口均仅支持单维度分组（`groupBy` 数组长度必须为 1），且不支持多维嵌套聚合；若需交叉分析（如“按模型+地域”组合），需客户端自行聚合原始数据。该限制在 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 和 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 中保持一致，无矛盾。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `billMonth`（仅 `GetBillingOverview`） | string | 是 | 账单月份，格式 `YYYY-MM` | `"2026-08"` |
| `granularity`（仅 `GetBillingTrend`） | string | 是 | 时间粒度，取值 `DAY` 或 `MONTH` | `"DAY"` |
| `timePeriod.start` / `.end`（仅 `GetBillingTrend`） | string | 是 | 查询起止日期，格式 `YYYY-MM-DD`；`end` 可等于 `start`（单日） | `"2026-08-01"`, `"2026-08-31"` |
| `groupBy` | array<object> | 是 | 分组维度，**必须且仅含 1 个对象**；`code` 字段指定维度类型 | `[{"code": "BASE_MODEL"}]` |
| `filter.dimensions` | array<object> | 否 | 筛选条件，支持多维组合；每个元素含 `code`、`values`、`selectType` | `[{"code": "MAAS_TYPE", "values": ["inference"], "selectType": "IN"}]` |
| `topNum` | integer | 否 | 返回 TopN 分组数，范围 1–20，默认 20 | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组，默认 `true` | `false` |
| `locale` | string | 否 | 返回语言，`zh-CN`（中文）或 `en-US`（英文），影响 `name` 字段展示 | `"zh-CN"` |

**维度 Code 统一说明**：`groupBy.code` 与 `filter.dimensions[].code` 共享同一套枚举值，包括 `MAAS_TYPE`、`BASE_MODEL`、`API_KEY_ID`、`WORKSPACE_ID`、`FEE_TYPE`、`CHARGE_TYPE`、`BUSINESS_REGION`、`SERVICE_SITE`、`ARTICLE_CODE`。所有维度均支持传入 `DIMENSION_FILTER_NULL_VALUE` 匹配空值。

## 使用方式

1. **认证**：使用平台标准 API Key 认证（HTTP Header `Authorization: Bearer <api_key>`）。
2. **请求路径**：
   - `GET /modelstudio/billing/overview` → `GetBillingOverview`
   - `GET /modelstudio/billing/trend` → `GetBillingTrend`
3. **构造查询**：
   - `GetBillingOverview`：必传 `billMonth` + `groupBy`；
   - `GetBillingTrend`：必传 `granularity` + `timePeriod` + `groupBy`；
   - 过滤、分页、语言等为可选参数，按需添加。
4. **响应解析**：
   - 公共字段：`requestId`、`code`、`success`、`message`；
   - `GetBillingOverview` 主要关注 `data.groups`（TopN 分组列表）和 `data.totalAmount`；
   - `GetBillingTrend` 主要关注 `data.resultByTime`（时间序列明细）和 `data.groupByTotal`（分组汇总）。

## 限制和注意事项

- **时间范围限制**：`GetBillingTrend` 的 `timePeriod.end` 不能晚于当前日期；`timePeriod.start` 到 `end` 的跨度最大为 90 天（`granularity=DAY`）或 12 个月（`granularity=MONTH`）。
- **币种一致性**：单次响应中 `currency` 字段全局统一（如 `CNY` 或 `USD`），但不同账户、不同时段可能返回不同币种，**不可跨响应直接加总**。
- **空值处理**：`filter.dimensions[].values` 中传 `DIMENSION_FILTER_NULL_VALUE` 表示匹配 NULL 或空字符串，但 `groupBy.code` 本身不可为 NULL。
- **精度说明**：所有金额字段（如 `amount`、`pretaxAmount`）均为字符串类型，保留两位小数，**开发者须按字符串解析，避免浮点计算误差**。
- **地域参数**：`regionId` 仅用于路由优化，不影响账单数据范围；账单数据始终覆盖全量已开通地域。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


