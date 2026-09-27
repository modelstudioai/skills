# billing api

billing api 是百炼平台提供的用于查询账户账单信息的一组 RESTful 接口，支持按时间范围获取账单概览与消费趋势数据。所有接口均需通过 API Key 认证，并遵循统一的请求签名规范。该 API 仅面向已开通计费功能的企业级账号开放，个人免费额度不在此接口覆盖范围内。

## 支持的模型/功能

当前 billing api 提供两类核心功能：  
- `GET /billing/overview`：返回指定周期内（默认最近30天）的总消费金额、调用次数、用量分布等聚合指标；  
- `GET /billing/trend`：返回按日/周/月粒度划分的消费趋势曲线，支持多维度（如模型、项目、地域）下钻分析。  
具体能力详见 [查询账单概览](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 和 [查询账单趋势](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 的原始定义。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `start_date` | string (YYYY-MM-DD) | 是 | 查询起始日期（含），最早支持 2024-01-01 |
| `end_date` | string (YYYY-MM-DD) | 是 | 查询结束日期（含），与 `start_date` 间隔不得超过 90 天 |
| `granularity` | string | 否 | `day` / `week` / `month`，仅 `trend` 接口有效；默认为 `day` |
| `group_by` | string | 否 | `model` / `project_id` / `region`，用于分组聚合；详见 [查询账单趋势](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) |

> **注意**：`group_by=region` 在 [查询账单概览](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 中未被声明支持，实际调用将返回 400 错误，应以 [查询账单趋势](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 文档为准。

## 使用方式

1. 确保已配置有效的 `X-DashScope-Date`、`Authorization` 及 `Content-Type: application/json` 请求头；  
2. 构造 GET 请求，例如：  
   ```bash
   curl -X GET "https://dashscope.aliyuncs.com/api/v1/billing/trend?start_date=2024-06-01&end_date=2024-06-30&granularity=day&group_by=model" \
     -H "Authorization: Bearer YOUR_API_KEY"
   ```  
3. 解析 JSON 响应中的 `data.items` 字段获取明细数据。完整请求示例和响应结构请参考 [查询账单概览](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)。

## 限制和注意事项

- 单次请求时间跨度上限为 90 天，超出将返回 `400 Bad Request`；  
- 每分钟限流 60 次（按 API Key 维度），超限返回 `429 Too Many Requests`；  
- 账单数据延迟约 2 小时，当日消费不可实时查询；  
- 所有接口均不支持跨账号查询，即使主子账号体系下也仅返回调用方自身账单。  
如需调试或验证字段含义，请务必对照原始文档 [查询账单趋势](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 中的 schema 定义。

## 来源文档

- [账单](../../raw/model-api-reference/billing-api.md)


