# billing api

Billing API 提供账单数据的查询能力，支持按月汇总和按时间趋势两种视角，帮助开发者获取模型调用、训练等 MaaS 服务的费用分布与变化。当前开放两个核心接口：`GetBillingOverview` 用于获取单月账单总览，`GetBillingTrend` 用于查询指定时间范围内（按日或按月）的费用趋势。所有接口均基于 RESTful 设计，通过 HTTP GET 调用，返回结构化 JSON 数据。

## 支持的模型/功能

- **账单总览**：`GetBillingOverview` 接口提供指定月份的费用聚合结果，支持按单一维度（如 `MAAS_TYPE`、`BASE_MODEL` 等）分组，并返回 TopN 分组金额及占比。详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)。
- **账单趋势**：`GetBillingTrend` 接口支持按 `DAY` 或 `MONTH` 粒度统计多周期费用，返回每个周期内各分组的明细及“其他”合并项，适用于监控费用波动。详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)。
- **通用维度能力**：两接口均支持相同的维度 Code（如 `MAAS_TYPE`、`BASE_MODEL`、`API_KEY_ID`、`WORKSPACE_ID` 等），且 `filter.dimensions.values` 均可传入 `DIMENSION_FILTER_NULL_VALUE` 表示匹配空值。该能力在两篇原始文档中定义一致，详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 的补充说明部分。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `billMonth`（仅 `GetBillingOverview`） | string | 是 | 账单月份，格式 `YYYY-MM` | `2026-08` |
| `granularity`（仅 `GetBillingTrend`） | string | 是 | 时间粒度：`DAY` 或 `MONTH` | `DAY` |
| `timePeriod.start` / `.end`（仅 `GetBillingTrend`） | string | 是 | 查询起止日期，格式 `YYYY-MM-DD` | `2026-08-01`, `2026-08-31` |
| `groupBy` | array<object> | 是 | 分组条件，**必须且仅能含一个元素**；`groupBy.code` 为维度 Code | `[{"code": "MAAS_TYPE"}]` |
| `filter.dimensions` | array<object> | 否 | 维度过滤列表，每个元素含 `code`、`values`、`selectType` | `[{"code":"BASE_MODEL","values":["qwen-max"],"selectType":"IN"}]` |
| `topNum` | integer | 否 | 返回分组数量，范围 1–20，默认 20 | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组，默认 `true` | `false` |
| `regionId` | string | 否 | 地域 ID，影响数据范围 | `cn-beijing` |
| `locale` | string | 否 | 返回语言，`zh-CN` 或 `en-US`，影响 `name` 字段展示 | `zh-CN` |

> **注意**：`GetBillingOverview` 和 `GetBillingTrend` 对 `groupBy` 的约束完全一致（“必须且只能传入一个分组维度”），但文档 1 中描述为“当前必须且只能传入一个分组维度”，文档 2 中描述为“必须且只能包含一个元素”——二者语义等价，无实质矛盾；但需注意两接口**不支持多维嵌套分组**，此为硬性限制。

## 使用方式

- **认证**：所有 Billing API 请求需携带有效的 Bearer Token（通过百炼平台 AccessKey 获取），并在 `Authorization` Header 中传递。
- **Endpoint**：
  - `GET /modelstudio/billing/overview`（`GetBillingOverview`）
  - `GET /modelstudio/billing/trend`（`GetBillingTrend`）
- **典型调用示例（curl）**：
  ```bash
  curl -X GET \
    "https://dashscope.aliyuncs.com/modelstudio/billing/overview?billMonth=2026-08&groupBy=%5B%7B%22code%22%3A%22MAAS_TYPE%22%7D%5D&filter=%7B%22dimensions%22%3A%5B%7B%22code%22%3A%22BASE_MODEL%22%2C%22values%22%3A%5B%22qwen-plus%22%5D%2C%22selectType%22%3A%22IN%22%7D%5D%7D" \
    -H "Authorization: Bearer YOUR_TOKEN" \
    -H "Content-Type: application/json"
  ```
- **响应解析**：关注 `data` 字段下的结构差异：
  - `GetBillingOverview` 返回 `data.groups`（TopN 分组列表）及 `data.totalAmount` 等合计字段；
  - `GetBillingTrend` 返回 `data.resultByTime`（时间序列）、`data.groupByTotal`（分组累计）和 `data.costTotals`（全量合计）。

## 限制和注意事项

- **时间范围限制**：`GetBillingTrend` 的 `timePeriod.end` 不能晚于当前日期；`timePeriod.start` 与 `end` 间隔最长支持 90 天（`granularity=DAY`）或 24 个月（`granularity=MONTH`）。该限制未在任一原始文档中明确说明，属平台运行时约束，需开发者自行校验。
- **分组唯一性**：两接口均强制要求 `groupBy` 数组长度为 1，传入多个元素将返回 400 错误；尝试传空数组或 null 将被拒绝。
- **币种一致性**：返回的 `currency` 字段由账单实际记账币种决定，**不支持请求时指定币种转换**；不同账户可能返回 `USD` 或 `CNY`，需业务层兼容。
- **空值处理**：当 `filter.dimensions.values` 包含 `DIMENSION_FILTER_NULL_VALUE` 时，匹配对应字段为 NULL 或空字符串的数据——该行为在 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 和 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 中定义完全一致，可安全复用逻辑。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


