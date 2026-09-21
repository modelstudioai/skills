# billing api

Billing API 提供账单数据的聚合查询能力，支持按月总览和时间趋势两种视角。开发者可通过 `GetBillingOverview` 获取指定月份的费用分组概览，或通过 `GetBillingTrend` 查询指定时间范围内（按日/月粒度）的费用变化趋势。所有接口均基于 RESTful 设计，需使用标准 HTTP GET 请求，并通过 query 参数传递过滤与分组逻辑。

## 支持的模型/功能

Billing API 当前提供两个核心接口：
- `GetBillingOverview`：用于获取**单个月份**的账单总览，返回按指定维度（如 `MAAS_TYPE`、`BASE_MODEL`）聚合的 TopN 分组及金额占比。详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)。
- `GetBillingTrend`：用于获取**连续时间段内**的账单趋势，支持 `DAY` 或 `MONTH` 粒度，返回各周期内分组费用明细及整体趋势分布。详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)。

两个接口均支持相同的维度体系（如 `MAAS_TYPE`、`API_KEY_ID`、`WORKSPACE_ID` 等），且 `filter.dimensions[].values` 均可传入 `DIMENSION_FILTER_NULL_VALUE` 表示匹配空值或 NULL 字段。

> **注意**：两篇原始文档中对 `filter.dimensions.selectType` 的取值描述完全一致（仅支持 `IN`/`NOT`），但 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 的示例未展示该字段用法，而 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 明确列出其为必填项之一 —— 实际调用时应以参数定义为准，`selectType` 为必填字段，不可省略。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `billMonth`（仅 `GetBillingOverview`） | string | 是 | 账单月份，格式 `YYYY-MM` | `2026-08` |
| `granularity`（仅 `GetBillingTrend`） | string | 是 | 时间粒度：`DAY` 或 `MONTH` | `DAY` |
| `timePeriod.start` / `.end`（仅 `GetBillingTrend`） | string | 是 | 查询起止日期，格式 `YYYY-MM-DD` | `2026-08-01`, `2026-08-31` |
| `groupBy` | array<object> | 是 | 分组维度，**必须且仅能含一个元素**；`code` 值须从标准维度列表中选取 | `[{"code": "MAAS_TYPE"}]` |
| `filter.dimensions` | array<object> | 否 | 维度过滤条件，每个元素含 `code`、`values`、`selectType` | `[{"code":"BASE_MODEL","values":["qwen-max"],"selectType":"IN"}]` |
| `topNum` | integer | 否 | 返回 TopN 分组数，范围 1–20，默认 20 | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组，默认 `true` | `false` |
| `regionId` | string | 否 | 地域 ID，影响数据范围 | `cn-beijing` |
| `locale` | string | 否 | 返回语言，`zh-CN` 或 `en-US`，影响 `name` 字段展示 | `zh-CN` |

## 使用方式

1. **认证**：所有请求需携带有效的 Bearer Token（通过百炼平台 AccessKey 鉴权，具体鉴权方式见平台通用认证文档）。
2. **构造 URL**：
   - `GetBillingOverview`: `GET https://<endpoint>/modelstudio/billing/overview?billMonth=2026-08&groupBy[0].code=MAAS_TYPE&locale=zh-CN`
   - `GetBillingTrend`: `GET https://<endpoint>/modelstudio/billing/trend?granularity=DAY&timePeriod.start=2026-08-01&timePeriod.end=2026-08-31&groupBy[0].code=BASE_MODEL`
3. **响应解析**：
   - 成功响应 `success: true`，数据位于 `data` 字段；
   - `data.currency` 标识币种（可能为 `CNY` 或 `USD`），所有金额字段均为字符串类型，需转为数值处理；
   - 分组键值（如 `key`）为空时统一返回 `DIMENSION_FILTER_NULL_VALUE`。

## 限制和注意事项

- **分组限制**：`groupBy` 数组长度**严格限定为 1**，不支持多维嵌套分组。
- **时间范围限制**：`GetBillingTrend` 的 `timePeriod.end` 与 `start` 间隔不得超过 90 天（`DAY` 粒度）或 24 个月（`MONTH` 粒度），超出将返回 400 错误。
- **空值处理**：`filter.dimensions[].values` 中传入 `DIMENSION_FILTER_NULL_VALUE` 可匹配数据库中为 NULL 或空字符串的记录，该行为在两篇文档中定义一致，是唯一推荐的空值筛选方式。
- **精度说明**：所有金额字段（如 `amount`, `pretaxAmount`）均为字符串格式，保留两位小数，**不可直接 JSON.parse() 转 number 后运算**，建议使用 `parseFloat()` 或高精度库处理。
- **地域一致性**：若同时指定 `regionId` 和 `filter.dimensions` 中含 `BUSINESS_REGION`，以 `regionId` 为准，后者将被忽略。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


