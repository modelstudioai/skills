# billing api

Billing API 提供账单数据查询能力，支持按月获取费用总览（`GetBillingOverview`）和按时间范围获取费用趋势（`GetBillingTrend`）。所有接口均基于 RESTful 设计，通过 HTTPS 调用，返回结构化 JSON 响应。该 API 适用于开发者集成至内部财务看板、成本分析系统或自动化对账流程。

## 支持的模型/功能

Billing API 当前提供两个核心功能接口：

- `GetBillingOverview`：查询**单个月份**的账单总览，返回按指定维度聚合的 TopN 分组费用及占比，适用于月度成本复盘与归因分析。详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)。
- `GetBillingTrend`：查询**连续时间段内**（按天或按月粒度）的费用趋势，返回分周期、分组的明细金额与税费拆分，适用于成本波动监控与预测建模。详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)。

两接口均支持统一的维度体系（如 `MAAS_TYPE`、`BASE_MODEL`、`API_KEY_ID` 等）进行分组与过滤，且共享相同的维度 Code 定义与 `DIMENSION_FILTER_NULL_VALUE` 空值匹配语义。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `billMonth`（仅 `GetBillingOverview`） | string | 是 | 账单月份，格式 `YYYY-MM` | `2026-08` |
| `granularity`（仅 `GetBillingTrend`） | string | 是 | 时间粒度：`DAY` 或 `MONTH` | `DAY` |
| `timePeriod.start` / `timePeriod.end`（仅 `GetBillingTrend`） | string | 是 | 查询起止日期，格式 `YYYY-MM-DD`；`end` 必须 ≥ `start`，且跨度 ≤ 90 天（`DAY`）或 ≤ 24 个月（`MONTH`） | `2026-08-01`, `2026-08-31` |
| `groupBy` | array<object> | 是 | 分组配置，**必须且仅允许 1 个元素**；`code` 字段需从[维度 Code 表](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)中选取 | `[{"code": "MAAS_TYPE"}]` |
| `filter.dimensions` | array<object> | 否 | 过滤条件列表，每个元素含 `code`、`values`（字符串数组）、`selectType`（`IN`/`NOT`） | `[{"code":"BASE_MODEL","values":["qwen-plus"],"selectType":"IN"}]` |
| `topNum` | integer | 否 | 返回分组数量，范围 1–20，默认 20；超出部分在 `GetBillingTrend` 中合并为“其他”，`GetBillingOverview` 中直接截断 | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组，默认 `true`；设为 `false` 可保留零费用分组用于完整性校验 | `false` |
| `regionId` / `locale` | string | 否 | 地域 ID（如 `cn-beijing`）与返回语言（`zh-CN`/`en-US`），影响 `name` 字段展示 | `cn-beijing`, `zh-CN` |

> **注意**：`filter.dimensions[].code` 和 `groupBy[].code` 的合法取值完全一致，详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 补充说明中的维度 Code 表；但 `GetBillingTrend` 文档未明确声明 `ARTICLE_CODE` 是否支持作为 `groupBy.code`，实际调用中应以 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 的定义为准。

## 使用方式

1. **认证**：所有请求需携带有效的 Bearer [Token](../concepts/token.md)（通过百炼平台 AccessKey/SecretKey 获取 OAuth2 [Token](../concepts/token.md)）。
2. **构造 URL**：
   - `GetBillingOverview`：`GET https://<endpoint>/modelstudio/billing/overview?billMonth=2026-08&groupBy=[{"code":"MAAS_TYPE"}]`
   - `GetBillingTrend`：`GET https://<endpoint>/modelstudio/billing/trend?granularity=DAY&timePeriod.start=2026-08-01&timePeriod.end=2026-08-31&groupBy=[{"code":"BASE_MODEL"}]`
3. **编码要求**：`groupBy` 和 `filter` 参数需进行 URL 编码（如 `[{%22code%22:%22MAAS_TYPE%22}]`），建议使用标准 JSON 序列化后编码。
4. **响应解析**：检查 `success: true` 与 `code: "200"`，再解析 `data` 结构；注意金额字段（如 `amount`、`pretaxAmount`）均为**字符串类型**，需转换为数值进行计算。

## 限制和注意事项

- **调用频率**：单账号默认限流 10 QPS，突发流量可能触发 429 响应，建议添加重试与退避逻辑。
- **时间范围约束**：
  - `GetBillingTrend` 的 `DAY` 粒度最大跨度为 90 天，`MONTH` 粒度最大跨度为 24 个月；
  - `billMonth` 仅支持过去 12 个月及当月（不支持未来月份）。
- **空值处理**：所有维度字段均可传 `DIMENSION_FILTER_NULL_VALUE` 表示匹配 NULL 或空字符串，该行为在两接口中一致，详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 说明。
- **币种差异**：`GetBillingOverview` 示例返回 `USD`，`GetBillingTrend` 示例返回 `CNY`；实际币种由账户结算货币决定，响应中 `currency` 字段为准，**不可硬编码假设**。
- **精度提示**：金额字段为字符串，保留小数点后两位，解析时请使用高精度浮点或定点数处理，避免 JS `Number` 精度丢失。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


