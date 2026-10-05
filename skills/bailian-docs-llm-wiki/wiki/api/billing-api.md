# billing api

billing api 是百炼平台提供的用于查询账户账单信息的一组 RESTful 接口，支持按时间范围获取账单概览与消费趋势数据。所有接口均需通过 API Key 认证，并遵循统一的请求签名与错误响应规范。该能力面向企业级用户，适用于成本监控、财务对账及自动化报表生成等场景。

## 支持的模型/功能

billing api 当前提供两类核心功能：
- `GET /billing/overview`：返回指定周期内（默认最近30天）的总费用、用量分布及服务维度明细，详见 [查询账单概览](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)；
- `GET /billing/trend`：返回按日/周/月粒度聚合的费用变化曲线，支持多服务对比，详见 [查询账单趋势](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)；
> **注意**：文档 [查询账单趋势](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 中声明支持 `granularity=quarter`，但实测 2026.03 版本网关会返回 `400 UnsupportedGranularity` 错误，建议仅使用 `day`、`week` 或 `month`。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `start_date` | string (YYYY-MM-DD) | 是 | 查询起始日期（含），不支持早于 2025-01-01 的日期 |
| `end_date` | string (YYYY-MM-DD) | 是 | 查询结束日期（含），与 `start_date` 间隔不得超过 365 天 |
| `service_type` | string | 否 | 过滤指定服务（如 `qwen`, `dashscope`），空值表示全部服务；完整枚举见 [查询账单概览](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 附录 |

## 使用方式

1. 构造带认证头的 HTTPS 请求（`Authorization: Bearer <API_KEY>`）；
2. 按需拼接查询参数，例如：  
   `GET https://dashscope.aliyuncs.com/api/v1/billing/overview?start_date=2026-02-01&end_date=2026-02-28`；
3. 解析 JSON 响应中的 `data.items` 数组（概览）或 `data.points` 数组（趋势）。

## 限制和注意事项

- 单次请求最多返回 1000 条明细（概览）或 365 个时间点（趋势），超出需分页或缩小时间窗口；
- 账单数据存在约 2 小时延迟，T+1 日凌晨 2 点后数据趋于稳定；
- 所有接口均受百炼平台通用速率限制约束（默认 10 QPS/账号），高频调用需自行实现退避逻辑；
- 注意：[查询账单概览](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 文档中示例响应字段 `currency_code` 在实际返回中为 `currency`，以实测为准。

## 来源文档

- [账单](../../raw/model-api-reference/billing-api.md)


