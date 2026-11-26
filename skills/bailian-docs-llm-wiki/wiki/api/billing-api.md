# billing api

billing api 提供账单数据查询能力，支持按时间趋势和月度总览两种视角获取费用明细。开发者可通过分组、过滤、聚合等参数灵活定制查询结果，适用于成本分析、用量监控和财务对账等场景。所有接口均基于 RESTful 设计，返回结构化 JSON 数据。

## 支持的模型/功能

billing api 当前提供两个核心接口：

- `GetBillingTrend`：查询指定时间范围内（支持跨日/跨月）的账单趋势，可按天或按月聚合，并返回各周期内分组费用明细及占比。适用于用量波动分析与趋势预测。详见 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)。
- `GetBillingOverview`：查询单个月份（格式 `YYYY-MM`）的账单总览，返回该月费用合计及 TopN 分组汇总。适用于月度成本复盘与预算核对。详见 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)。

两个接口支持的维度 Code 完全一致（如 `MAAS_TYPE`、`BASE_MODEL`、`API_KEY_ID` 等），且均支持 `filter.dimensions[].values` 传入 `DIMENSION_FILTER_NULL_VALUE` 匹配空值，行为一致。> **注意**：文档 1 和文档 2 中 `groupBy` 参数描述存在细微差异——文档 1 写“必须且只能包含一个元素”，文档 2 写“当前必须且只能传入一个分组维度”；二者语义等价，实际服务端仅接受单维度分组，多维分组暂不支持。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| `granularity`（仅 `GetBillingTrend`） | string | 是 | 聚合粒度：`DAY` 或 `MONTH` | `DAY` |
| `timePeriod`（仅 `GetBillingTrend`） | object | 是 | 查询时间范围，含 `start`（`YYYY-MM-DD`）和 `end`（`YYYY-MM-DD`） | `{ "start": "2026-08-01", "end": "2026-08-31" }` |
| `billMonth`（仅 `GetBillingOverview`） | string | 是 | 账单月份，格式 `YYYY-MM` | `"2026-08"` |
| `groupBy` | array<object> | 是 | 分组维度，**必须且仅允许 1 个元素**；`code` 值需从[支持维度列表](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md#补充说明)中选取 | `[{"code": "BASE_MODEL"}]` |
| `filter` | object | 否 | 维度过滤条件，支持嵌套 `dimensions` 数组进行多维筛选 | `{"dimensions": [{"code": "MAAS_TYPE", "values": ["inference"], "selectType": "IN"}]}` |
| `topNum` | integer | 否 | 返回分组数量（1–20），默认 20；超出部分合并为“其他” | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 0 的分组，默认 `true` | `false` |
| `locale` | string | 否 | 返回语言：`zh-CN`（中文）或 `en-US`（英文），影响 `name` 字段展示 | `"zh-CN"` |

## 使用方式

1. **认证**：所有 billing api 请求需携带有效的 Bearer [Token](../concepts/token.md)（通过百炼平台 AccessKey 获取）。
2. **请求方法**：均为 `GET`，参数通过 Query String 传递（`GetBillingTrend`）或 URL Query（`GetBillingOverview`）。
3. **Endpoint**：
   - `GetBillingTrend`: `GET /modelstudio/billing/trend`
   - `GetBillingOverview`: `GET /modelstudio/billing/overview`
4. **示例调用（curl）**：
   ```bash
   curl -X GET "https://dashscope.aliyuncs.com/modelstudio/billing/trend?granularity=DAY&timePeriod.start=2026-08-01&timePeriod.end=2026-08-31&groupBy%5B0%5D.code=BASE_MODEL&filter.dimensions%5B0%5D.code=MAAS_TYPE&filter.dimensions%5B0%5D.values%5B0%5D=inference" \
     -H "Authorization: Bearer YOUR_TOKEN"
   ```

## 限制和注意事项

- **时间范围限制**：`GetBillingTrend` 最大支持 90 天跨度（`end - start ≤ 89 days`）；`GetBillingOverview` 仅支持历史已出账月份，不支持未来月份。
- **分组约束**：`groupBy` 必须且仅能指定一个维度，不支持组合分组（如 `["BASE_MODEL", "MAAS_TYPE"]` 将被拒绝）。
- **空值处理**：`filter.dimensions[].values` 传 `DIMENSION_FILTER_NULL_VALUE` 可匹配数据库中 NULL 或空字符串字段，该行为在两接口中完全一致。
- **货币单位**：返回币种由账户结算币种决定，`GetBillingOverview` 示例中为 `USD`，而 `GetBillingTrend` 示例中为 `CNY`；实际值以 `data.currency` 字段为准，**不可硬编码假设**。
- **精度说明**：所有金额字段（`amount`, `pretaxAmount`, `taxAmount`）均为字符串类型，保留小数点后两位，开发者需按字符串解析或转为 decimal 处理，避免浮点误差。

## 来源文档

- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)
- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)


