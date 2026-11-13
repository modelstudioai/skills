# billing api

Billing API 提供账单数据的查询能力，支持按月汇总和按时间趋势两种视角，帮助开发者监控和分析模型服务的费用分布。当前开放两个核心接口：`GetBillingOverview` 用于获取指定月份的分组账单总览，`GetBillingTrend` 用于查询指定时间范围内（按日或按月粒度）的费用变化趋势。所有接口均基于 RESTful 设计，通过 HTTP GET 调用，返回结构化 JSON 数据。

## 支持的模型/功能

- **账单总览**：`GetBillingOverview` 接口提供单月账单的维度聚合视图，适用于快速掌握当月费用构成（如按 MaaS 类型、基础模型或 API Key ID 分组）。详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)。
- **账单趋势**：`GetBillingTrend` 接口支持按 `DAY` 或 `MONTH` 粒度查询连续时间段内的费用分布与变化，返回含周期明细（`resultByTime`）和分组汇总（`groupByTotal`）的完整趋势数据。详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)。
- **通用维度能力**：两个接口均支持相同的维度 Code（如 `MAAS_TYPE`、`BASE_MODEL`、`API_KEY_ID` 等），且 `filter.dimensions.values` 均可传入 `DIMENSION_FILTER_NULL_VALUE` 表示匹配空值。该一致性设计已在 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 和 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 中明确说明。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `billMonth`（仅 `GetBillingOverview`） | string | 是 | 账单月份，格式 `YYYY-MM` | `"2026-08"` |
| `granularity`（仅 `GetBillingTrend`） | string | 是 | 时间粒度，取值 `DAY` 或 `MONTH` | `"DAY"` |
| `timePeriod.start` / `timePeriod.end`（仅 `GetBillingTrend`） | string | 是 | 查询起止日期，格式 `YYYY-MM-DD`，最大跨度为 366 天 | `"2026-08-01"`, `"2026-08-31"` |
| `groupBy` | array<object> | 是 | 分组条件，**必须且仅能包含一个元素**；`groupBy.code` 须为支持的维度 Code（如 `MAAS_TYPE`） | `[{"code": "BASE_MODEL"}]` |
| `filter.dimensions` | array<object> | 否 | 维度过滤器，支持多维组合（如同时按 `BASE_MODEL` 和 `CHARGE_TYPE` 过滤） | `[{"code": "BASE_MODEL", "values": ["qwen-max"], "selectType": "IN"}]` |
| `topNum` | integer | 否 | 返回 TopN 分组数量，范围 `1–20`，默认 `20`；超出部分在 `GetBillingTrend` 中合并为“其他” | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组，默认 `true` | `false` |
| `locale` | string | 否 | 返回语言，`zh-CN`（中文）或 `en-US`（英文），影响 `name` 字段展示 | `"zh-CN"` |

> **注意**：`GetBillingOverview` 的 `billMonth` 与 `GetBillingTrend` 的 `timePeriod` 时间范围逻辑不同，前者为静态月度快照，后者为动态区间查询；二者不可混用参数，且无跨接口兼容性设计。

## 使用方式

1. **认证**：所有 Billing API 请求需携带有效的 `Authorization: Bearer <access_token>` 请求头（OAuth2.0 访问令牌），并确保对应账号具备 `billing:read` 权限。
2. **构造请求**：
   - `GetBillingOverview`：`GET /modelstudio/billing/overview?billMonth=2026-08&groupBy=[{"code":"MAAS_TYPE"}]&locale=zh-CN`
   - `GetBillingTrend`：`GET /modelstudio/billing/trend?granularity=DAY&timePeriod.start=2026-08-01&timePeriod.end=2026-08-31&groupBy=[{"code":"BASE_MODEL"}]`
3. **解析响应**：
   - 成功时 `success === true`，费用金额字段（如 `amount`、`pretaxAmount`）均为字符串类型，**需转为浮点数处理**；
   - `data.groups`（`GetBillingOverview`）与 `data.resultByTime`（`GetBillingTrend`）均按金额降序排列；
   - `DIMENSION_FILTER_NULL_VALUE` 在 `key` 字段中表示空值分组，前端应统一映射为 `"-"` 或 `"未指定"`。

## 限制和注意事项

- **调用频率限制**：单账号每分钟最多调用 60 次 Billing API（两个接口共享配额），超限返回 `429 Too Many Requests`。
- **时间范围约束**：
  - `GetBillingOverview`：`billMonth` 仅支持近 13 个月（含当月）的历史账单，例如当前为 2026-09，则有效范围为 `2025-09` 至 `2026-09`；
  - `GetBillingTrend`：`timePeriod.end` 不得晚于当前日期，且 `end - start ≤ 366 days`。
- **维度值大小写敏感**：所有 `filter.dimensions.values` 和 `groupBy.code` **必须使用大写形式**（如 `"MAAS_TYPE"`），小写将导致筛选失败或 400 错误。
- **币种不一致风险**：`GetBillingOverview` 示例返回 `USD`，而 `GetBillingTrend` 示例返回 `CNY`；实际币种取决于账户结算主体，**不可硬编码假设**，需以响应中 `currency` 字段为准。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


