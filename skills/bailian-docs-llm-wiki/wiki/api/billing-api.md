# billing api

billing api 是百炼平台提供的用于查询账户账单数据的 RESTful 接口集合，支持按时间范围获取账单概览与消费趋势。所有接口均需使用 `Bearer` 认证，并通过 `X-Studio-Region` 指定地域（如 `cn-beijing`）。该 API 仅面向已开通计费权限的企业主体账号，个人开发者不可直接调用。

## 支持的模型/功能

当前 billing api 提供两类核心能力：  
- **账单概览**：返回指定周期内总费用、用量分布、Top 模型消耗等聚合信息；  
- **账单趋势**：按日/周/月粒度返回连续时间段内的费用变化曲线，支持多维度分组（如按模型、按项目）。  
所有功能均基于 [查询账单概览](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 和 [查询账单趋势](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 两个端点实现，暂不支持按实例或 API Key 级别拆分账单。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `start_date` | string (YYYY-MM-DD) | 是 | 查询起始日期（含），最小支持 90 天前 |
| `end_date` | string (YYYY-MM-DD) | 是 | 查询结束日期（含），不可晚于今日 |
| `granularity` | string | 否 | 仅 `getbillingtrend` 支持：`daily` / `weekly` / `monthly`；默认 `daily` |
| `group_by` | string[] | 否 | 如 `["model", "project_id"]`，最大长度 2；详见 [查询账单趋势](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) |

> **注意**：`getbillingoverview` 接口文档中声明支持 `currency` 参数，但实测传入 `USD` 或 `CNY` 均返回人民币计价结果，该字段当前无效，以 [查询账单概览](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 实际响应为准。

## 使用方式

1. 获取访问凭证：调用 `/v1/auth/token` 获取短期 `access_token`（有效期 1 小时）；  
2. 构造请求：  
   ```bash
   curl -X GET "https://dashscope.aliyuncs.com/api/v1/billing/overview?start_date=2024-01-01&end_date=2024-01-31" \
     -H "Authorization: Bearer $TOKEN" \
     -H "X-Studio-Region: cn-beijing"
   ```  
3. 解析响应：成功时返回 `200 OK`，结构统一为 `{ "code": 200, "data": { ... } }`；错误码详见 [查询账单概览](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 的“错误响应”章节。

## 限制和注意事项

- 单次查询时间跨度不得超过 90 天；  
- 每个账号每分钟最多发起 60 次请求（QPM），超限返回 `429 Too Many Requests`；  
- 账单数据延迟约 2 小时，当日消费无法实时查询；  
- 所有接口均不支持跨地域查询（即 `X-Studio-Region` 必须与账单归属地域一致）；  
- 若原始文档中提及“支持按 API Key 统计”，请忽略——该能力尚未上线，实际行为以 [查询账单趋势](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 当前实现为准。

## 来源文档

- [账单](../../raw/model-api-reference/billing-api.md)


