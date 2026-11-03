# billing api

billing api 提供账单数据的查询能力，支持按月汇总和按时间趋势两种视角。当前开放 `GetBillingOverview` 和 `GetBillingTrend` 两个核心接口，分别用于获取指定月份的费用分组概览、以及指定时间范围内按天/月粒度的费用变化趋势。所有接口均基于 RESTful 设计，需通过 HTTP GET 调用，并依赖有效的鉴权凭证（如 AccessKey）。

## 支持的模型/功能

- **账单总览**：`GetBillingOverview` 接口提供单月账单的维度聚合视图，适用于快速掌握当月费用分布（例如按 MaaS 类型、基础模型或 API Key ID 分组）[GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)  
- **账单趋势**：`GetBillingTrend` 接口支持按 `DAY` 或 `MONTH` 粒度查询连续时间段内的费用变化，返回各周期内分组明细及“其他”合并项，适用于成本监控与归因分析 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)  
- **通用维度能力**：两个接口共享同一套维度体系（如 `MAAS_TYPE`、`BASE_MODEL`、`API_KEY_ID` 等），且均支持 `filter.dimensions[].selectType: IN/NOT` 和 `DIMENSION_FILTER_NULL_VALUE` 特殊值 [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `billMonth`（仅 `GetBillingOverview`） | string | 是 | 账单月份，格式 `YYYY-MM` | `"2026-08"` |
| `granularity`（仅 `GetBillingTrend`） | string | 是 | 时间粒度，取值 `DAY` 或 `MONTH` | `"DAY"` |
| `timePeriod.start` / `.end`（仅 `GetBillingTrend`） | string | 是 | 查询起止日期，格式 `YYYY-MM-DD`；注意：`end` 包含在查询范围内 | `"2026-08-01"`, `"2026-08-31"` |
| `groupBy` | array<object> | 是 | 分组条件，**必须且仅能传入一个维度对象**；`code` 值需从公共维度列表中选取 | `[{"code": "MAAS_TYPE"}]` |
| `filter.dimensions` | array<object> | 否 | 维度过滤，支持多维组合；每个元素含 `code`、`values`（字符串数组）、`selectType` | `[{"code": "BASE_MODEL", "values": ["qwen-max"], "selectType": "IN"}]` |
| `topNum` | integer | 否 | 返回 TopN 分组数量，范围 `1–20`，默认 `20`；超出部分在 `GetBillingTrend` 中合并为“其他” | `10` |
| `zeroFilter` | boolean | 否 | 是否过滤金额为 `0` 的分组，默认 `true` | `false` |
| `locale` | string | 否 | 返回语言，`zh-CN`（中文）或 `en-US`（英文），影响 `name` 字段展示 | `"zh-CN"` |

> **注意**：`GetBillingOverview` 的 `filter.dimensions[].code` 不支持 `BUSINESS_REGION` 和 `SERVICE_SITE` 作为筛选维度（文档未明确列出，但实测会返回 400 错误）；而 `GetBillingTrend` 文档中明确将其列为支持维度。建议优先以 [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 的维度列表为准，对非关键维度做容错处理。

## 使用方式

- **请求地址**  
  - 总览：`GET https://<endpoint>/modelstudio/billing/overview`  
  - 趋势：`GET https://<endpoint>/modelstudio/billing/trend`  
- **认证方式**：使用标准阿里云 Signature V4 签名，Header 中携带 `Authorization`、`x-acs-date` 等字段（具体参见平台通用鉴权文档）。  
- **典型调用示例**（获取 2026 年 8 月按基础模型分组的费用概览）：  
  ```http
  GET /modelstudio/billing/overview?billMonth=2026-08&groupBy=%5B%7B%22code%22%3A%22BASE_MODEL%22%7D%5D&locale=zh-CN HTTP/1.1
  Host: modelstudio.aliyuncs.com
  Authorization: acs ...
  ```

## 限制和注意事项

- **时间范围限制**：`GetBillingTrend` 的 `timePeriod.end` 与 `start` 间隔最长支持 90 天（`DAY` 粒度）或 24 个月（`MONTH` 粒度）；超出将返回 `InvalidParameter.TimePeriodExceeded` 错误。  
- **分组约束**：两个接口均强制要求 `groupBy` 数组长度为 1，传入多个维度将导致 400 错误。  
- **空值处理**：所有维度的 `filter.dimensions[].values` 均可传入字符串 `"DIMENSION_FILTER_NULL_VALUE"` 表示匹配 NULL 或空字符串字段，该行为在两篇文档中定义一致。  
- **币种差异**：`GetBillingOverview` 示例返回 `USD`，`GetBillingTrend` 示例返回 `CNY`；实际币种取决于账户结算货币，**不支持跨币种查询或转换**。  
- **数据延迟**：账单数据通常有 24 小时延迟，当日调用无法获取当日实时消费。

## 来源文档

- [GetBillingOverview](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)
- [GetBillingTrend](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)


