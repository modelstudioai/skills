# billing api

Billing API 提供账单数据查询能力，支持按月获取费用总览（`GetBillingOverview`）和按时间范围获取费用趋势（`GetBillingTrend`）。所有接口均基于 RESTful 设计，需通过 HTTPS 调用，并依赖平台身份认证（如 AccessKey）。返回数据为 JSON 格式，含金额、税费、分组明细等结构化字段，适用于成本分析、预算监控与自动化对账场景。

## 支持的模型/功能

Billing API 当前提供两个核心能力：
- `GetBillingOverview`：查询**单个月份**的账单总览，返回按指定维度聚合的 TopN 分组及金额占比，适用于月度成本概览与归因分析。详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)。
- `GetBillingTrend`：查询**连续时间范围内**（按天或按月粒度）的费用趋势，返回周期性费用序列及各周期内分组明细，适用于成本波动监测与预测。详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)。

两个接口支持的分组与筛选维度完全一致，包括 `MAAS_TYPE`、`BASE_MODEL`、`API_KEY_ID`、`WORKSPACE_ID` 等共 9 类维度（见下文“关键参数”），且均支持 `DIMENSION_FILTER_NULL_VALUE` 表示空值匹配。

> **注意**：两篇原始文档中 `filter.dimensions[].selectType` 的可选值均列为 `IN` / `NOT`，但实际调用中仅 `IN` 已验证可用；`NOT` 尚未在集成测试中确认行为，建议暂仅使用 `IN` 进行正向筛选。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| `groupBy` | `array<object>` | 是 | 分组条件数组，**必须且仅允许 1 个元素**。`groupBy[0].code` 指定维度 Code（如 `MAAS_TYPE`）。详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 中的维度对照表。 |
| `filter.dimensions` | `array<object>` | 否 | 维度筛选列表，每个元素含 `code`、`values` 和 `selectType`。`values` 可传具体值（如 `["qwen-plus"]`）或 `DIMENSION_FILTER_NULL_VALUE`。 |
| `topNum` | `integer` | 否 | 返回分组数量，取值 1–20，默认 20。超出部分在 `GetBillingTrend` 中合并为“其他”，而 `GetBillingOverview` 不做合并。 |
| `zeroFilter` | `boolean` | 否 | 是否过滤金额为 0 的分组，默认 `true`。设为 `false` 可保留零消费分组（如未调用但已分配的 workspace）。 |
| `locale` | `string` | 否 | 响应语言，`zh-CN`（中文）或 `en-US`（英文），影响 `name` 字段展示。默认 `en-US`。 |

> **注意**：`GetBillingTrend` 要求必填 `timePeriod`（含 `start`/`end`，格式 `YYYY-MM-DD`），而 `GetBillingOverview` 要求必填 `billMonth`（格式 `YYYY-MM`）。二者不可混用，且 `timePeriod.end` 不能晚于当前日期（系统校验严格），`billMonth` 亦不支持未来月份。

## 使用方式

1. **鉴权**：所有请求需携带标准阿里云签名头（`Authorization`, `x-acs-date`, `x-acs-signature-nonce` 等），参考通用认证规范。
2. **Endpoint**：
   - `GET /modelstudio/billing/overview` → `GetBillingOverview`
   - `GET /modelstudio/billing/trend` → `GetBillingTrend`
3. **示例请求（curl）**：
   ```bash
   curl -X GET "https://dashscope.aliyuncs.com/modelstudio/billing/overview?billMonth=2026-08&groupBy[0].code=MAAS_TYPE&filter.dimensions[0].code=BASE_MODEL&filter.dimensions[0].values=qwen-plus&locale=zh-CN" \
     -H "Authorization: ACS <access_key_id>:<signature>"
   ```
4. **响应处理**：关注 `success` 字段判断是否成功；`data.groups`（`overview`）或 `data.resultByTime`（`trend`）为业务数据主体；金额字段均为字符串类型（含两位小数），需转为数值计算。

## 限制和注意事项

- **时间范围限制**：`GetBillingTrend` 的 `timePeriod` 最大跨度为 90 天（`DAY` 粒度）或 12 个月（`MONTH` 粒度）；超出将返回 `400` 错误。
- **分组约束**：`groupBy` 严格限定为单维度，传入多个元素将被拒绝；`groupBy.code` 必须在[支持维度列表](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)中，否则返回 `400`。
- **空值处理**：`filter.dimensions[].values` 传 `DIMENSION_FILTER_NULL_VALUE` 时，匹配数据库中 `NULL` 或空字符串字段；但 `groupBy.code` 不支持该值。
- **币种一致性**：单次响应中 `currency` 字段全局统一（如 `CNY` 或 `USD`），不支持跨币种聚合；多币种账户需分别查询并自行换算。
- **数据延迟**：账单数据通常有 24–48 小时延迟，`billMonth=2026-08` 的数据在 2026-09-02 后方可完整查询。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


