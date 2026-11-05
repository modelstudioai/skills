# billing api

billing API 提供账单数据的查询能力，支持按月汇总和按时间趋势两种视角。开发者可通过 `GetBillingOverview` 获取指定月份的费用分组概览，或通过 `GetBillingTrend` 查询跨日/月的费用变化趋势，并支持多维度分组、筛选与语言本地化。所有接口均基于 RESTful HTTP GET 请求，需使用平台颁发的合法凭证鉴权。

## 支持的模型/功能

当前 billing API 提供两个核心接口：

- `GetBillingOverview`：用于查询**单个月份**的账单总览，返回按指定维度（如 `MAAS_TYPE`、`BASE_MODEL`）聚合的 TopN 分组及金额占比。适用于成本归因与月度复盘场景。详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)。
- `GetBillingTrend`：用于查询**指定时间范围内**（支持 DAY 或 MONTH 粒度）的费用趋势，返回分周期的明细（`resultByTime`）及全局分组汇总（`groupByTotal`）。适用于监控用量波动与预算跟踪。详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)。

> **注意**：两接口均要求 `groupBy` 数组**必须且仅含 1 个元素**，不支持多维嵌套分组；文档中“支持的维度 Code”列表完全一致，但 `GetBillingTrend` 的 `resultByTime.periodDetails` 中明确引入了 `DIMENSION_GROUP_OTHERS_VALUE` 表示“其他”分组，而 `GetBillingOverview` 的 `data.groups` 未定义该语义 —— 实际使用中若 `topNum` 截断，超出部分不会被聚合，需自行处理缺失项。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `billMonth`（仅 `GetBillingOverview`） | string | 是 | 账单月份，格式 `YYYY-MM` | `2026-08` |
| `granularity`（仅 `GetBillingTrend`） | string | 是 | 时间粒度：`DAY` 或 `MONTH` | `DAY` |
| `timePeriod.start` / `.end`（仅 `GetBillingTrend`） | string | 是 | 查询起止日期，格式 `YYYY-MM-DD` | `2026-08-01`, `2026-08-31` |
| `groupBy[].code` | string | 是 | 分组维度 Code，大小写敏感，建议全大写 | `MAAS_TYPE`, `BASE_MODEL` |
| `filter.dimensions` | array<object> | 否 | 维度过滤条件，支持 `IN`/`NOT` 操作 | `[{"code": "BASE_MODEL", "values": ["qwen-max"], "selectType": "IN"}]` |
| `topNum` | integer | 否 | 返回分组数量（1–20），默认 20 | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组，默认 `true` | `false` |
| `locale` | string | 否 | 返回语言：`zh-CN`（中文）或 `en-US`（英文） | `zh-CN` |

所有维度 Code（如 `API_KEY_ID`, `WORKSPACE_ID`, `ARTICLE_CODE` 等）及其可选值均在两篇原始文档的“补充说明”中统一定义，详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 和 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)。

## 使用方式

1. **构造请求 URL**  
   - `GetBillingOverview`: `GET /modelstudio/billing/overview?billMonth=2026-08&groupBy[0].code=MAAS_TYPE&locale=zh-CN`  
   - `GetBillingTrend`: `GET /modelstudio/billing/trend?granularity=DAY&timePeriod.start=2026-08-01&timePeriod.end=2026-08-31&groupBy[0].code=BASE_MODEL`

2. **设置请求头**  
   - `Authorization: Bearer <your_access_token>`  
   - `Content-Type: application/json`

3. **解析响应**  
   - 共同结构：检查 `success === true` 且 `code === "200"`；错误时参考 `message` 字段。  
   - `GetBillingOverview`: 主要数据在 `data.groups`，含 `key`（原始值）、`name`（本地化名称）、`amount`、`percentage`。  
   - `GetBillingTrend`: 核心趋势数据在 `data.resultByTime`（按时间升序），每项含 `period`、`total.amount` 及 `periodDetails`（当期各分组明细）。

## 限制和注意事项

- **时间范围限制**：`GetBillingTrend` 的 `timePeriod` 最大跨度为 90 天（`DAY` 粒度）或 12 个月（`MONTH` 粒度），超出将返回 400 错误。  
- **空值处理**：所有 `filter.dimensions[].values` 均支持传入 `DIMENSION_FILTER_NULL_VALUE` 表示匹配 NULL 或空字符串字段，该行为在两篇文档中定义一致。  
- **币种差异**：`GetBillingOverview` 示例返回 `USD`，`GetBillingTrend` 示例返回 `CNY`，实际币种取决于账户结算货币，**不可假设固定值**。  
- **分组截断逻辑**：`topNum` 仅控制返回的 TopN 分组数量；`GetBillingTrend` 明确将剩余分组合并为 `DIMENSION_GROUP_OTHERS_VALUE`，而 `GetBillingOverview` 不提供“其他”汇总，调用方需注意数据完整性。  
- **地域参数**：`regionId` 用于限定查询地域账单，但其取值（如 `cn-beijing`）需与实际开通地域严格一致，否则可能返回空数据或权限错误。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


