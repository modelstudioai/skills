# billing api

Billing API 提供账单数据查询能力，支持按月汇总（`GetBillingOverview`）和按时间趋势分析（`GetBillingTrend`）两类核心场景。所有接口均通过 HTTPS GET 调用，返回结构化 JSON 响应，适用于成本分摊、用量监控与财务对账等开发者需求。接口设计遵循统一的维度模型与过滤机制，便于跨接口复用参数逻辑。

## 支持的模型/功能

Billing API 当前提供两个核心功能接口：

- `GetBillingOverview`：获取**单个月份**的账单总览，返回按指定维度聚合的 TopN 分组金额及占比，适合月度成本概览与快速归因。详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)。
- `GetBillingTrend`：获取**连续时间段内**（按天或按月粒度）的费用趋势，返回分周期明细、分组汇总及“其他”合并项，适合用量波动分析与预算预测。详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)。

> **注意**：两文档均声明 `groupBy` 必须且只能传入一个维度对象，但 `GetBillingTrend` 的返回结构中 `resultByTime.periodDetails` 支持同一周期内多个分组（如多模型并行调用），而 `GetBillingOverview` 的 `data.groups` 为扁平数组，不体现周期嵌套。此为功能定位差异，非矛盾。

## 关键参数

以下参数在两个接口中语义一致，可复用：

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `groupBy[].code` | string | 是 | 分组维度 Code，**必须且仅支持一个**。推荐大写。支持值见下表。 | `MAAS_TYPE` |
| `filter.dimensions[].code` | string | 否 | 筛选维度 Code，与 `groupBy[].code` 共享取值集。 | `BASE_MODEL` |
| `filter.dimensions[].values` | string[] | 否 | 筛选值列表；可传 `DIMENSION_FILTER_NULL_VALUE` 匹配空值。 | `["qwen-max"]` |
| `filter.dimensions[].selectType` | string | 否 | 筛选类型：`IN`（包含）或 `NOT`（排除）。默认 `IN`。 | `IN` |
| `topNum` | integer | 否 | 返回 TopN 分组数，范围 1–20，默认 20。超出部分在 `GetBillingTrend` 中合并为“其他”。 | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组，默认 `true`。 | `false` |
| `regionId` | string | 否 | 地域 ID，用于限定账单数据范围。 | `cn-beijing` |
| `locale` | string | 否 | 返回语言：`zh-CN`（中文）或 `en-US`（英文），影响 `name` 字段展示。默认 `en-US`。 | `zh-CN` |

**支持的维度 Code（全量一致）**  
`MAAS_TYPE`, `BASE_MODEL`, `API_KEY_ID`, `WORKSPACE_ID`, `FEE_TYPE`, `CHARGE_TYPE`, `BUSINESS_REGION`, `SERVICE_SITE`, `ARTICLE_CODE`。  
详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 和 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 的“补充说明”章节。

## 使用方式

### 请求地址
- `GET /modelstudio/billing/overview` → `GetBillingOverview`
- `GET /modelstudio/billing/trend` → `GetBillingTrend`

### 公共请求头
需携带认证 Header（如 `Authorization: Bearer <token>`），具体鉴权方式参见平台通用认证文档。

### 入参示例（`GetBillingTrend`）
```http
GET /modelstudio/billing/trend?granularity=DAY&timePeriod.start=2026-08-01&timePeriod.end=2026-08-07&groupBy[0].code=BASE_MODEL&filter.dimensions[0].code=MAAS_TYPE&filter.dimensions[0].values[0]=inference&locale=zh-CN HTTP/1.1
```

### 响应解析要点
- 所有金额字段（如 `amount`, `pretaxAmount`）均为**字符串类型**，含两位小数，需按字符串解析避免浮点精度丢失。
- `GetBillingOverview` 的 `data.groups[].percentage` 表示该分组占 **TopN 分组合计金额** 的比例，非占全量账单比例。
- `GetBillingTrend` 的 `resultByTime[].periodDetails[].percentage` 表示该分组占 **当前周期总金额** 的比例。

## 限制和注意事项

- **时间范围限制**：`GetBillingTrend` 的 `timePeriod.end` 不能晚于当前日期；`timePeriod.start` 至 `end` 最长支持 90 天（`DAY` 粒度）或 24 个月（`MONTH` 粒度）。
- **维度一致性**：`groupBy[].code` 与 `filter.dimensions[].code` 必须属于同一维度集合，**不可混用不兼容维度**（例如 `groupBy.code=MAAS_TYPE` 时，`filter.dimensions[].code` 不得为 `ARTICLE_CODE`，因二者无直接关联性）。
- **空值处理**：`filter.dimensions[].values` 传 `DIMENSION_FILTER_NULL_VALUE` 可匹配 NULL 或空字符串，但 `groupBy[].code` 本身不可为 NULL。
- > **注意**：`GetBillingOverview` 文档中 `billMonth` 格式为 `YYYY-MM`，而 `GetBillingTrend` 的 `timePeriod.start/end` 为 `YYYY-MM-DD`；两者时间格式不兼容，**不可互换使用**。开发者需严格按接口要求构造日期参数。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


