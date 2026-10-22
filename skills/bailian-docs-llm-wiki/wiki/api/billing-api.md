# billing api

Billing API 提供账单数据的查询能力，支持按月汇总和按时间趋势两种视角，帮助开发者获取模型调用、训练等 MaaS 服务的费用分布与变化。当前开放两个核心接口：`GetBillingOverview` 用于获取单月账单总览，`GetBillingTrend` 用于查询指定时间范围内（按日或按月）的费用趋势。所有接口均基于 RESTful 设计，通过 HTTP GET 调用，返回结构化 JSON 数据。

## 支持的模型/功能

- **账单总览**：`GetBillingOverview` 接口提供指定月份的费用聚合结果，支持按单一维度（如 `MAAS_TYPE`、`BASE_MODEL` 等）分组，并返回 TopN 分组金额及占比。详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)。
- **账单趋势**：`GetBillingTrend` 接口支持按 `DAY` 或 `MONTH` 粒度统计费用变化，返回时间序列数据（`resultByTime`）及全局分组汇总（`groupByTotal`），适用于监控与成本分析。详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)。
- **通用维度能力**：两个接口共享同一套维度体系（如 `MAAS_TYPE`、`BASE_MODEL`、`API_KEY_ID` 等），且均支持 `filter.dimensions[].selectType: IN/NOT` 和空值匹配（`DIMENSION_FILTER_NULL_VALUE`）。该能力在 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 的补充说明中明确定义，`GetBillingOverview` 文档亦同步引用相同维度列表，二者一致。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `billMonth`（仅 `GetBillingOverview`） | string | 是 | 账单月份，格式 `YYYY-MM` | `"2026-08"` |
| `granularity`（仅 `GetBillingTrend`） | string | 是 | 时间粒度：`DAY` 或 `MONTH` | `"DAY"` |
| `timePeriod.start` / `.end`（仅 `GetBillingTrend`） | string | 是 | 查询起止日期，格式 `YYYY-MM-DD` | `"2026-08-01"`, `"2026-08-31"` |
| `groupBy` | array<object> | 是 | 分组条件，**必须且仅能传入一个维度**；`code` 值需从标准维度 Code 中选取（如 `"MAAS_TYPE"`） | `[{"code": "BASE_MODEL"}]` |
| `filter.dimensions` | array<object> | 否 | 维度过滤，支持多维组合；每个元素含 `code`、`values`（字符串数组）、`selectType`（`IN`/`NOT`） | `[{"code": "BASE_MODEL", "values": ["qwen-max"], "selectType": "IN"}]` |
| `topNum` | integer | 否 | 返回分组数量，1–20，默认 20；超出部分在 `GetBillingTrend` 中合并为“其他” | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组，默认 `true` | `false` |
| `locale` | string | 否 | 返回语言，`zh-CN`（中文）或 `en-US`（英文），影响 `name` 字段展示 | `"zh-CN"` |

> **注意**：`GetBillingOverview` 文档中 `filter.dimensions[].code` 示例值为 `BASE_MODEL`，而 `GetBillingTrend` 文档同位置示例为 `BASE_MODEL`，二者一致；但 `GetBillingOverview` 请求参数表格中 `filter.dimensions.code` 行标注为“否”，而其子字段 `filter.dimensions.values` 却标记为“否”（无误），实际逻辑是：若 `filter.dimensions` 存在，则其内 `code` 和 `values` 均为必填。此为文档表述歧义，以 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 中明确的嵌套必填规则为准。

## 使用方式

- **基础调用路径**：
  - 总览：`GET /modelstudio/billing/overview`
  - 趋势：`GET /modelstudio/billing/trend`
- **认证**：需在请求 Header 中携带有效的 `Authorization`（如 Bearer Token）及 `x-acs-signature-nonce` 等标准鉴权字段（具体参见平台通用认证文档）。
- **分组与过滤示例**：  
  查询 2026 年 8 月按基础模型分组的费用，并仅统计 `qwen-plus` 和 `qwen-max` 的数据：
  ```http
  GET /modelstudio/billing/overview?billMonth=2026-08&groupBy[0].code=BASE_MODEL&filter.dimensions[0].code=BASE_MODEL&filter.dimensions[0].values=qwen-plus&qwen-max&filter.dimensions[0].selectType=IN
  ```
- **响应解析重点**：  
  - `data.groups`（`GetBillingOverview`）或 `data.resultByTime[].periodDetails`（`GetBillingTrend`）中 `amount` 为字符串类型，需转为数字进行计算；  
  - `percentage` 字段为小数形式（如 `"0.6667"`），非百分比整数；  
  - 所有金额字段（`amount`/`pretaxAmount`/`taxAmount`）单位由 `currency` 字段声明，**不可假设为固定币种**。

## 限制和注意事项

- **时间范围限制**：`GetBillingTrend` 的 `timePeriod.end` 与 `start` 间隔最长支持 90 天（`DAY` 粒度）或 24 个月（`MONTH` 粒度）；超出将返回 `400` 错误。
- **分组约束**：两个接口均强制要求 `groupBy` 数组长度为 1，传入多个维度将导致 `400` 错误；不支持复合分组（如同时按 `BASE_MODEL` 和 `MAAS_TYPE`）。
- **空值处理**：当 `filter.dimensions[].values` 包含 `DIMENSION_FILTER_NULL_VALUE` 时，匹配对应维度为空或 `NULL` 的账单记录；该行为在两篇原始文档的“说明”章节中完全一致。
- **地域与站点**：`regionId` 和 `SERVICE_SITE` 等参数影响数据源范围，但**不保证跨地域账单数据实时同步**；建议优先使用 `BUSINESS_REGION` 维度进行业务侧过滤，而非依赖 `regionId` 请求参数。
- **精度与一致性**：`GetBillingOverview` 返回 `data.totalAmount` 为全量金额，而 `GetBillingTrend` 的 `data.costTotals.amount` 为所选 `topNum` 分组 + “其他”的合计，二者在 `topNum < 实际分组数` 时数值可能不等——这是设计使然，非数据错误。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


