# billing api

billing api 是百炼平台提供的用于查询账户账单信息的一组 RESTful 接口，支持按时间范围获取账单概览与消费趋势数据。所有接口均需通过 API Key 认证，并遵循统一的请求签名与错误响应规范。该 API 仅面向已开通计费功能的企业级账号开放。

## 支持的模型/功能

当前 billing api 提供两类核心能力：  
- `GET /billing/overview`：返回指定周期内总费用、用量分布及服务维度明细（如模型调用、存储、API 调用次数等）；  
- `GET /billing/trend`：返回按日/周/月粒度聚合的消费趋势曲线，支持多服务类型叠加对比。  
以上功能覆盖百炼平台全部计费项，包括模型推理（如 Qwen 系列、Qwen-VL）、向量检索、工作流执行及 API 网关调用。详细字段定义请参见 [查询账单概览](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 和 [查询账单趋势](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 的原始文档。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `start_date` | string (YYYY-MM-DD) | 是 | 查询起始日期（含），不支持早于 90 天前的数据 |
| `end_date` | string (YYYY-MM-DD) | 是 | 查询结束日期（含），与 `start_date` 间隔不得超过 365 天 |
| `granularity` | string | 否 | 仅 `trend` 接口支持：`day` / `week` / `month`；默认为 `day` |
| `service_type` | string[] | 否 | 过滤特定服务类型，如 `qwen-inference`, `vector-search`；空数组表示返回全部 |

> **注意**：`service_type` 参数在 [查询账单趋势](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 中支持数组格式，但 [查询账单概览](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 仅接受单值字符串，实际调用时需按接口分别处理。

## 使用方式

1. 构造带认证头的 HTTPS 请求（`Authorization: Bearer <api_key>`）；  
2. 按需选择 endpoint：`https://dashscope.aliyuncs.com/api/v1/billing/overview` 或 `/trend`；  
3. 以 query string 传递参数（不支持 request body）；  
4. 解析 JSON 响应中的 `data` 字段，其中 `items` 为结果数组，`summary` 为汇总统计。  
完整请求示例和响应结构详见 [查询账单概览](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)。

## 限制和注意事项

- 单次请求最多返回 1000 条明细记录，超出需分页（使用 `next_token` 字段）；  
- 账单数据延迟约 2 小时，不保证实时性；  
- 免费额度消耗不单独展示，已自动折抵在 `total_amount` 中；  
- 若 `end_date` 超出当前账期（如跨月未结算），部分数据可能为空或为预估值。  
开发者应始终以 [查询账单趋势](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 文档中声明的 SLA 和字段语义为准，避免依赖未文档化的返回字段。

## 来源文档

- [账单](../../raw/model-api-reference/billing-api.md)


