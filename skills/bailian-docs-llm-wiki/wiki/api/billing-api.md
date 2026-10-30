# billing api

billing api 是百炼平台提供的账单数据查询接口集合，用于获取账户级账单概览、消费趋势等财务信息。所有接口均基于 RESTful 设计，需通过 API Key 认证，并遵循统一的版本前缀（如 `2026-02-10`）。该能力面向企业客户和开发者，适用于成本监控、自动化对账及财务看板集成等场景。

## 支持的模型/功能

billing api 当前不涉及模型调用，而是提供两类核心财务数据能力：  
- **账单概览**：返回指定周期内总消费金额、已用额度、剩余配额等聚合指标；  
- **账单趋势**：按日/周/月粒度返回近 365 天的消费变化曲线，支持多维度分组（如按模型、项目、地域）。  
详细字段定义与响应结构请参阅 [查询账单概览](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 和 [查询账单趋势](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 的原始文档。

## 关键参数

所有 billing api 接口共用以下必需参数：  
- `X-Api-Key`（Header）：有效的百炼平台 API Key；  
- `start_date` / `end_date`（Query）：ISO 8601 格式日期（如 `2024-01-01`），时间范围最长支持 365 天；  
- `granularity`（Query，仅趋势接口）：可选 `day`、`week` 或 `month`；  
- `group_by`（Query，可选）：支持 `model`、`project_id`、`region`，多个值用英文逗号分隔。  
参数约束与默认行为详见 [查询账单趋势](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 文档说明。

## 使用方式

1. 确保 API Key 已在 [百炼控制台 → API 密钥管理](https://dash.aliyun.com) 中启用且具备 `BillingReadOnly` 权限；  
2. 构造请求 URL，例如查询最近 7 日账单趋势：  
   ```bash
   GET https://dash.aliyun.com/api/v1/billing/trend?start_date=2024-06-01&end_date=2024-06-07&granularity=day
   ```  
3. 解析 JSON 响应中的 `data.items` 数组，每项含 `timestamp`、`amount_cny`、`breakdown` 等字段。  
完整请求示例与错误码说明见 [查询账单概览](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)。

## 限制和注意事项

- 单次请求时间跨度不得超过 365 天；  
- 每分钟调用频率上限为 60 次（按 API Key 维度限流）；  
- 账单数据延迟约 2 小时（即 T+2 可查），不支持实时消费查询；  
> **注意**：原始文档中 `api-modelstudio-2026-02-10-getbillingtrend.md` 提到支持 `group_by=service`，但当前 API 实际返回 `400 Bad Request`，该字段暂未生效，请勿使用；以 [查询账单趋势](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 的最新运行时行为为准。

## 来源文档

- [账单](../../raw/model-api-reference/billing-api.md)


