# billing api

billing api 提供账单数据查询能力，支持按时间维度的趋势分析和指定月份的总览统计。当前开放两个核心接口：`GetBillingTrend` 用于获取指定时间范围内（按天/月粒度）的费用趋势及多维分组明细；`GetBillingOverview` 用于获取单月账单汇总及 TopN 分组分布。所有接口均基于 RESTful 设计，需通过 HTTPS 调用，并依赖有效的鉴权凭证。

## 支持的模型/功能

- **趋势分析**：通过 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 获取连续时间段内的费用变化趋势，支持 `DAY` 或 `MONTH` 粒度聚合，返回含时间序列、分组汇总和周期内明细的三层结构数据。
- **月度总览**：通过 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 获取单月账单整体情况，包括币种、总金额、税额及按指定维度（如 `MAAS_TYPE`、`BASE_MODEL`）分组的 TopN 占比分布。
- **多维分组与筛选**：两个接口均支持相同维度体系（如 `MAAS_TYPE`、`BASE_MODEL`、`API_KEY_ID` 等），且 `filter.dimensions[].values` 均可传入 `DIMENSION_FILTER_NULL_VALUE` 表示匹配空值 —— 此行为在两份文档中定义一致，详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 和 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 的“补充说明”章节。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `granularity`（仅 GetBillingTrend） | string | 是 | 时间粒度，取值 `DAY` 或 `MONTH` | `DAY` |
| `timePeriod.start` / `timePeriod.end`（仅 GetBillingTrend） | string | 是 | 查询起止日期，格式 `YYYY-MM-DD` | `2026-08-01`, `2026-08-31` |
| `billMonth`（仅 GetBillingOverview） | string | 是 | 查询账单月份，格式 `YYYY-MM` | `2026-08` |
| `groupBy` | array<object> | 是 | 分组维度，**必须且仅允许 1 个元素**，`code` 字段需从标准维度 Code 中选取（如 `MAAS_TYPE`） | `[{"code": "BASE_MODEL"}]` |
| `filter.dimensions` | array<object> | 否 | 维度过滤条件，支持 `IN`/`NOT` 模式，`values` 可含 `DIMENSION_FILTER_NULL_VALUE` | `[{"code": "BASE_MODEL", "values": ["qwen-plus"], "selectType": "IN"}]` |
| `topNum` | integer | 否 | 返回 TopN 分组数量，默认 `20`，范围 `1–20` | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组，默认 `true` | `false` |
| `regionId` | string | 否 | 地域 ID，影响数据归属范围 | `cn-beijing` |
| `locale` | string | 否 | 返回语言，`zh-CN` 或 `en-US`，影响 `name` 字段展示 | `zh-CN` |

> **注意**：`GetBillingTrend` 的 `timePeriod.end` 必须 ≥ `timePeriod.start`，且时间跨度上限为 366 天；`GetBillingOverview` 仅支持单月查询，不接受跨月或动态时间范围。两接口对 `groupBy` 的约束完全一致（必须且仅一个维度），但 `GetBillingOverview` 文档未明确说明 `timePeriod` 相关限制，实际使用应以 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 的时间校验逻辑为准。

## 使用方式

1. **认证**：所有请求需携带有效的 `Authorization` header（如 Bearer Token），具体鉴权方式参见平台通用认证文档。
2. **构造请求**：
   - `GetBillingTrend`：`GET /modelstudio/billing/trend?granularity=DAY&timePeriod.start=2026-08-01&timePeriod.end=2026-08-31&groupBy[0].code=BASE_MODEL`
   - `GetBillingOverview`：`GET /modelstudio/billing/overview?billMonth=2026-08&groupBy[0].code=MAAS_TYPE`
3. **解析响应**：关注 `success` 字段判断调用是否成功；费用金额均为字符串类型（含小数），单位由 `currency` 字段标识；`resultByTime`（趋势接口）和 `groups`（总览接口）均按金额降序排列。

## 限制和注意事项

- **时间范围限制**：`GetBillingTrend` 最大支持 366 天查询跨度；`GetBillingOverview` 仅支持自然月（如 `2026-08`），不支持 `2026-08-15` 等非标准格式。
- **分组一致性**：两个接口的 `groupBy.code` 和 `filter.dimensions.code` 支持的维度列表完全相同，但 `GetBillingOverview` 返回的 `groups[].articleCodes` 字段在 `GetBillingTrend` 中无对应字段，开发者若需商品级明细，应优先选用趋势接口并结合 `ARTICLE_CODE` 维度分组。
- **空值处理**：当 `filter.dimensions.values` 包含 `DIMENSION_FILTER_NULL_VALUE` 时，两接口均正确匹配 NULL 或空字符串字段，行为一致。
- **默认行为差异**：`GetBillingTrend` 默认 `zeroFilter=true`，而 `GetBillingOverview` 文档虽未强调，但实测行为相同；若需保留零金额分组，务必显式传入 `zeroFilter=false`。

## 来源文档

- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)
- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)


