# billing api

Billing API 提供账单数据查询能力，支持按月汇总（`GetBillingOverview`）和按时间趋势分析（`GetBillingTrend`）两类核心场景。所有接口均通过 HTTPS GET 请求调用，需携带有效认证凭证（如 AccessKey）。返回数据为 JSON 格式，金额字段均为字符串类型（含两位小数），币种由 `currency` 字段明确标识。

## 支持的模型/功能

Billing API 当前提供两个核心接口：
- `GetBillingOverview`：获取**单个月份**的账单总览，按指定维度聚合 TopN 分组，适用于快速掌握某月费用分布。详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)。
- `GetBillingTrend`：获取**连续时间段内**（按天或按月粒度）的费用趋势，支持分组+时间双维度下钻，适用于成本监控与周期性分析。详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)。

> **注意**：两文档均列出 `MAAS_TYPE`、`BASE_MODEL` 等 9 个维度 Code，但文档 1 的 `filter.dimensions.values` 示例中 `BASE_MODEL` 值为 `["qwen-max"]`，而文档 2 同位置示例值为 `["qwen-plus"]`；实际传值应以账单系统中真实存在的模型名称为准，建议先调用对应接口并省略 `filter` 参数观察返回的 `key` 值，再用于后续筛选。该差异非接口限制，而是示例值选取不同所致。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 公共性 |
|--------|------|------|------|--------|
| `billMonth`（仅 Overview） | string | 是 | 格式 `YYYY-MM`，指定查询月份 | 仅 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 支持 |
| `granularity`（仅 Trend） | string | 是 | `DAY` 或 `MONTH`，决定时间轴粒度 | 仅 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 支持 |
| `timePeriod`（仅 Trend） | object | 是 | 含 `start`（`YYYY-MM-DD`）和 `end`（`YYYY-MM-DD`） | 仅 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 支持 |
| `groupBy` | array<object> | 是 | 必须且仅含 1 个元素，`code` 字段取值见下方维度表 | 两者均支持 |
| `filter` | object | 否 | 维度过滤条件，支持 `IN`/`NOT` 逻辑，`values` 可含 `DIMENSION_FILTER_NULL_VALUE` | 两者均支持 |
| `topNum` | integer | 否 | 1–20，默认 20；超出 TopN 的分组合并为“其他”（Trend）或直接过滤（Overview） | 两者均支持 |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组，默认 `true` | 两者均支持 |
| `locale` | string | 否 | `zh-CN` 或 `en-US`，影响 `name` 字段展示语言 | 两者均支持 |

**支持的维度 Code（统一使用大写）**  
`MAAS_TYPE`, `BASE_MODEL`, `API_KEY_ID`, `WORKSPACE_ID`, `FEE_TYPE`, `CHARGE_TYPE`, `BUSINESS_REGION`, `SERVICE_SITE`, `ARTICLE_CODE`

## 使用方式

1. **构造请求 URL**  
   - Overview: `GET https://<endpoint>/modelstudio/billing/overview?billMonth=2026-08&groupBy[0].code=MAAS_TYPE&locale=zh-CN`  
   - Trend: `GET https://<endpoint>/modelstudio/billing/trend?granularity=DAY&timePeriod.start=2026-08-01&timePeriod.end=2026-08-31&groupBy[0].code=BASE_MODEL`

2. **设置认证头**  
   所有请求必须携带 `Authorization` 头（如 `Bearer <AccessToken>`）或 `AccessKeyId`/`AccessKeySecret` 签名（具体方式参考平台认证文档）。

3. **解析响应**  
   - `data.currency` 表示币种，不可假设为固定值（示例中 Overview 返回 `USD`，Trend 返回 `CNY`）。  
   - 金额字段（如 `amount`, `pretaxAmount`）均为字符串，需转换为数字进行计算。  
   - `data.groups`（Overview）和 `data.resultByTime`（Trend）是核心数据数组，按金额降序排列。

## 限制和注意事项

- **时间范围限制**：`GetBillingTrend` 的 `timePeriod` 最大跨度为 90 天（`DAY` 粒度）或 12 个月（`MONTH` 粒度），超出将返回 400 错误。  
- **分组数量硬限**：`topNum` 最大为 20，无法通过增大该值获取全部分组；如需全量数据，需结合 `filter` 分页查询。  
- **空值处理**：所有维度的 `filter.dimensions.values` 均可传 `DIMENSION_FILTER_NULL_VALUE` 表示匹配 NULL 或空字符串，但 `groupBy.code` 不支持该值。  
- **地域与站点一致性**：`regionId` 和 `SERVICE_SITE` 属于不同维度，前者指物理部署地域（如 `cn-beijing`），后者指服务覆盖范围（如 `global`），不可混用。  
- **精度提示**：返回金额保留两位小数，但底层计费可能含更高精度；聚合结果中的 `percentage` 为分组金额占 TopN 总和的比例，**不包含“其他”分组**（Trend 中 `costTotals` 才是全量合计）。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


