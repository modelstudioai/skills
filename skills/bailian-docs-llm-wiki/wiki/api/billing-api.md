# billing api

Billing API 提供账单数据查询能力，支持按月获取费用总览（`GetBillingOverview`）和按时间范围获取费用趋势（`GetBillingTrend`）。所有接口均基于 RESTful 设计，通过 HTTPS 调用，返回结构化 JSON 响应。该 API 适用于开发者集成至内部财务看板、成本分析工具或自动化对账系统。

## 支持的模型/功能

Billing API 当前提供两个核心接口：

- `GetBillingOverview`：查询**单个月份**的账单总览，返回按指定维度聚合的 TopN 分组费用及全局合计（含税/不含税/币种）。适用于月度成本复盘与概览展示。  
- `GetBillingTrend`：查询**连续时间段内**（支持 DAY 或 MONTH 粒度）的费用趋势，返回分周期明细（`resultByTime`）、分组汇总（`groupByTotal`）及整体合计（`costTotals`）。适用于成本波动监控与归因分析。

两接口支持的维度 Code 完全一致，包括 `MAAS_TYPE`、`BASE_MODEL`、`API_KEY_ID`、`WORKSPACE_ID`、`FEE_TYPE`、`CHARGE_TYPE`、`BUSINESS_REGION`、`SERVICE_SITE` 和 `ARTICLE_CODE`，详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 的补充说明部分。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `billMonth`（仅 `GetBillingOverview`） | string | 是 | 账单月份，格式 `YYYY-MM` | `2026-08` |
| `granularity`（仅 `GetBillingTrend`） | string | 是 | 时间粒度：`DAY` 或 `MONTH` | `DAY` |
| `timePeriod.start` / `.end`（仅 `GetBillingTrend`） | string | 是 | 查询起止日期，格式 `YYYY-MM-DD`；`end` 可等于 `start` | `2026-08-01`, `2026-08-31` |
| `groupBy` | array<object> | 是 | **必须且仅含一个元素**，指定分组维度；`code` 值需从标准维度列表中选取 | `[{"code": "BASE_MODEL"}]` |
| `filter.dimensions` | array<object> | 否 | 维度过滤条件，支持多维组合；每个 `dimensions` 对象需指定 `code`、`values` 和 `selectType` | `[{"code": "MAAS_TYPE", "values": ["inference"], "selectType": "IN"}]` |
| `topNum` | integer | 否 | 返回 TopN 分组数量（1–20），默认 20；超出部分在 `GetBillingTrend` 中合并为“其他” | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组，默认 `true`；设为 `false` 可保留空分组 | `false` |
| `locale` | string | 否 | 返回语言，`zh-CN`（中文）或 `en-US`（英文），影响 `name` 字段展示 | `zh-CN` |

> **注意**：两接口均支持 `DIMENSION_FILTER_NULL_VALUE` 作为 `filter.dimensions.values` 的特殊值，用于匹配 NULL 或空字符串字段；该行为在 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 和 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 中定义一致，无矛盾。

## 使用方式

1. **认证**：所有请求需携带有效的 Bearer [Token](../concepts/token.md)（通过百炼平台 AccessKey 获取），并设置 `Authorization: Bearer <token>` 请求头。
2. **端点**：
   - `GET /modelstudio/billing/overview`（[GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)）
   - `GET /modelstudio/billing/trend`（[GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)）
3. **构造请求**：将参数以 query string 形式拼接（如 `?billMonth=2026-08&groupBy=[{"code":"MAAS_TYPE"}]&locale=zh-CN`），注意 `groupBy` 和 `filter` 需 URL 编码。
4. **解析响应**：检查 `success` 字段及 `code` 值（`200` 表示成功）；关键业务数据位于 `data` 下，注意金额字段均为字符串类型（含小数位），需按需转换。

## 限制和注意事项

- 单次请求最多返回 20 个分组（由 `topNum` 控制），超出部分在 `GetBillingTrend` 的 `groupByTotal` 中归入 `DIMENSION_GROUP_OTHERS_VALUE`，但 `GetBillingOverview` 不提供“其他”分组。
- `GetBillingOverview` 仅支持查询已结算完成的账单月份，历史数据通常延迟 1–3 天可查；`GetBillingTrend` 的 `timePeriod.end` 最早支持查询至当前日期前 90 天。
- `regionId` 参数不影响账单数据源（账单为全局聚合），仅用于路由优化，建议与调用方实际地域保持一致。
- 所有金额字段（如 `amount`、`pretaxAmount`）均为字符串格式，**不可直接数值比较或计算**，需先转为浮点数并注意精度（推荐使用 `BigDecimal` 或等效高精度类型处理）。
- `locale=zh-CN` 时，`name` 字段返回中文名称（如 `"模型调用"`），但 `key` 字段始终为原始值（如 `"inference"`），业务逻辑应以 `key` 为准进行判断。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


