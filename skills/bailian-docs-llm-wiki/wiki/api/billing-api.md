# billing api

billing api 提供账单数据查询能力，支持按时间维度的趋势分析和指定月份的总览统计。当前开放两个核心接口：`GetBillingTrend` 用于获取指定时间范围内（按天/月粒度）的费用趋势与分组明细；`GetBillingOverview` 用于获取单月账单的聚合概览。所有接口均基于 RESTful 设计，需通过 HTTPS 调用，并遵循统一的鉴权与参数规范。

## 支持的模型/功能

- **趋势分析**：通过 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 获取连续时间段内的费用变化趋势，支持 `DAY` 或 `MONTH` 粒度聚合，返回含时间序列、分组汇总及周期内明细的三层结构数据。
- **月度总览**：通过 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 获取单月（`YYYY-MM` 格式）账单整体情况，返回币种、总金额、各分组金额及占比，适用于快速成本盘点。
- **多维分组与筛选**：两个接口均支持相同维度 Code（如 `MAAS_TYPE`、`BASE_MODEL`、`API_KEY_ID` 等）进行 `groupBy` 和 `filter`，且 `filter.dimensions.values` 均支持传入 `DIMENSION_FILTER_NULL_VALUE` 表示匹配空值 —— 此行为在两份文档中定义一致，详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 补充说明。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `granularity`（仅 `GetBillingTrend`） | string | 是 | 取值 `DAY` 或 `MONTH`；决定时间轴聚合粒度 |
| `timePeriod.start` / `timePeriod.end`（仅 `GetBillingTrend`） | string | 是 | 格式 `YYYY-MM-DD`，闭区间，最大跨度 366 天 |
| `billMonth`（仅 `GetBillingOverview`） | string | 是 | 格式 `YYYY-MM`，仅支持查询已出账的自然月 |
| `groupBy` | array<object> | 是 | 必须且仅允许 1 个元素；`code` 字段需从[支持维度列表](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)中选择 |
| `filter.dimensions` | array<object> | 否 | 支持多维组合过滤，每个 `dimensions` 对象含 `code`、`values`（string 数组）、`selectType`（`IN`/`NOT`） |
| `topNum` | integer | 否 | 1–20，默认 20；超出 TopN 的分组合并为“其他” |
| `zeroFilter` | boolean | 否 | 是否排除金额为 0 的分组，默认 `true` |

> **注意**：`GetBillingTrend` 的 `timePeriod.end` 为闭区间，而 `GetBillingOverview` 的 `billMonth` 为整月粒度；二者时间语义不同，不可混用。此外，`GetBillingOverview` 返回 `data.currency` 示例为 `"USD"`，但实际值取决于账户结算币种，该字段行为以 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 文档为准，而非硬编码。

## 使用方式

- **HTTP 方法与路径**：
  - `GET /modelstudio/billing/trend` → `GetBillingTrend`
  - `GET /modelstudio/billing/overview` → `GetBillingOverview`
- **认证**：需在请求 Header 中携带有效的 `Authorization`（如 Bearer Token）及 `x-acs-region-id`（若未通过 `regionId` 参数显式指定）。
- **语言控制**：通过 `locale=zh-CN` 可使 `name` 字段返回中文（如 `模型调用`），默认 `en-US`。
- **典型场景示例**：  
  查询 2026-08 全月按基础模型分组的费用总览：  
  `GET /modelstudio/billing/overview?billMonth=2026-08&groupBy[0].code=BASE_MODEL&filter.dimensions[0].code=MAAS_TYPE&filter.dimensions[0].values[0]=inference`

## 限制和注意事项

- 时间范围限制：`GetBillingTrend` 最大支持 366 天查询跨度；`GetBillingOverview` 仅支持已生成账单的自然月，不支持未来月份或非标准月格式。
- 分组约束：`groupBy` 必须且只能传入一个维度对象，传入多个将返回参数错误（`InvalidParameter.GroupByCount`）。
- 空值处理：所有维度的 `filter.dimensions.values` 均支持 `DIMENSION_FILTER_NULL_VALUE` 字符串字面量，用于匹配数据库中 NULL 或空字符串字段，该机制在两份文档中定义完全一致。
- 货币一致性：响应中 `currency` 字段由账户主结算币种决定，非固定值；开发者应以返回值为准，不可预设为 `CNY` 或 `USD`。
- 性能提示：高频调用建议缓存 `locale=zh-CN` 的分组名称映射，避免重复请求。

## 来源文档

- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)
- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)


