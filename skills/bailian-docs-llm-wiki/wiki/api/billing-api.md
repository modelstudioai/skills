# billing api

Billing API 提供账单数据的查询能力，支持按月汇总和按时间趋势两种视角，帮助开发者获取模型调用、训练等 MaaS 服务的费用明细。当前仅开放 `GetBillingOverview` 和 `GetBillingTrend` 两个核心接口，均基于 RESTful 设计，需通过 HTTPS 调用并携带有效认证凭证。所有接口返回结构统一，含 `requestId`、`code`、`success` 及业务数据 `data` 字段，便于程序化解析与监控集成。

## 支持的模型/功能

- **账单总览**：`GetBillingOverview` 接口用于查询指定单个月份（`billMonth`）的费用聚合结果，适用于月度成本复盘与预算核对。该接口不支持跨月查询，且分组维度必须且仅能指定一个（如 `MAAS_TYPE` 或 `BASE_MODEL`）[GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)。  
- **账单趋势**：`GetBillingTrend` 接口支持按天（`DAY`）或按月（`MONTH`）粒度查询连续时间段（`timePeriod.start` 至 `timePeriod.end`）的费用变化，返回分组维度下的周期性明细及汇总，适用于用量波动分析与异常检测 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)。  
- 两接口均支持相同维度体系（如 `BASE_MODEL`、`API_KEY_ID`、`WORKSPACE_ID` 等），且 `filter.dimensions[].values` 均可传入 `DIMENSION_FILTER_NULL_VALUE` 表示匹配空值，语义一致 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `billMonth`（仅 Overview） | string | 是 | 账单月份，格式 `YYYY-MM` | `"2026-08"` |
| `granularity`（仅 Trend） | string | 是 | 时间粒度，取值 `DAY` 或 `MONTH` | `"DAY"` |
| `timePeriod`（仅 Trend） | object | 是 | 含 `start`（`YYYY-MM-DD`）和 `end`（`YYYY-MM-DD`） | `{"start":"2026-08-01","end":"2026-08-31"}` |
| `groupBy` | array<object> | 是 | 分组维度，必须且仅含一个元素；`code` 值需从标准维度列表中选取 | `[{"code":"MAAS_TYPE"}]` |
| `filter` | object | 否 | 维度过滤条件，支持多维组合筛选 | `{"dimensions":[{"code":"BASE_MODEL","values":["qwen-plus"],"selectType":"IN"}]}` |
| `topNum` | integer | 否 | 返回 TopN 分组数量（1–20），默认 20；超出部分在 Trend 中合并为“其他” | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组，默认 `true` | `false` |
| `locale` | string | 否 | 返回语言，`zh-CN` 或 `en-US`，影响 `name` 字段展示 | `"zh-CN"` |

> **注意**：`GetBillingOverview` 的 `filter.dimensions[].code` 与 `GetBillingTrend` 的对应字段完全一致，但文档 1 中 `filter.dimensions.values` 示例写为 `["qwen-max"]`，而文档 2 示例为 `["qwen-plus"]`；实际传值应以账单系统中真实出现的模型标识为准，建议通过 `GetBillingOverview` 先查询可用值再用于 `filter`。

## 使用方式

1. **认证**：所有请求需在 HTTP Header 中携带有效的 `Authorization`（如 Bearer Token）及 `x-acs-region-id`（若指定 `regionId` 参数）。
2. **构造 URL**：
   - 总览：`GET https://<endpoint>/modelstudio/billing/overview?billMonth=2026-08&groupBy=[{"code":"BASE_MODEL"}]&locale=zh-CN`
   - 趋势：`GET https://<endpoint>/modelstudio/billing/trend?granularity=DAY&timePeriod.start=2026-08-01&timePeriod.end=2026-08-31&groupBy=[{"code":"MAAS_TYPE"}]`
3. **解析响应**：
   - `data.currency` 标识币种（如 `CNY`、`USD`），金额字段（如 `amount`、`pretaxAmount`）均为字符串类型，需转为数值处理；
   - `data.groups`（Overview）与 `data.resultByTime.periodDetails`（Trend）中的 `percentage` 为小数格式（如 `"0.6667"`），非百分比整数。

## 限制和注意事项

- **时间范围限制**：`GetBillingTrend` 的 `timePeriod.end` 不能晚于当前日期，且 `end - start` 最大跨度为 90 天（`DAY` 粒度）或 12 个月（`MONTH` 粒度）；`GetBillingOverview` 仅支持已结算完成的月份，通常延迟 1–3 个工作日。
- **分组约束**：两个接口均强制要求 `groupBy` 数组长度为 1，不支持多维嵌套分组；若需交叉分析，需客户端自行聚合。
- **空值处理**：当 `filter.dimensions[].values` 包含 `DIMENSION_FILTER_NULL_VALUE` 时，将匹配数据库中该字段为 `NULL` 或空字符串的记录，此行为在两接口中完全一致。
- **错误响应**：所有接口统一使用 `code` 字段表示业务状态（如 `"400"` 表示参数错误），`message` 字段提供可读提示，`success: false` 时 `data` 可能为空或不完整。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


