# billing api

billing api 是百炼平台提供的用于查询账户账单信息的一组 RESTful 接口，支持按时间范围获取账单概览与消费趋势数据。所有接口均需通过 API Key 认证，并遵循统一的错误响应格式。该 API 仅面向已开通计费功能的企业账号开放。

## 支持的模型/功能

billing api 不涉及模型调用，而是提供两类账单查询能力：  
- `GET /billing/overview`：返回指定周期内总消费金额、资源使用量、服务类型分布等聚合信息；  
- `GET /billing/trend`：返回按日/周/月粒度划分的消费趋势曲线，支持多维度（如模型、项目、地域）下钻分析。  
具体字段定义与示例响应详见 [查询账单概览](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 和 [查询账单趋势](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 的原始文档。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `start_date` | string (YYYY-MM-DD) | 是 | 查询起始日期（含），支持最大 90 天跨度 |
| `end_date` | string (YYYY-MM-DD) | 是 | 查询结束日期（含），不得早于 `start_date` |
| `granularity` | string | 否 | 仅 `trend` 接口支持，取值 `day`/`week`/`month`，默认 `day` |
| `group_by` | string | 否 | 趋势数据分组维度，如 `model`, `project_id`, `region`；详见 [查询账单趋势](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) |

> **注意**：`group_by=region` 在 [查询账单趋势](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 中声明为实验性参数，实际调用可能返回 `400 UnsupportedGroupBy`，建议生产环境暂不启用。

## 使用方式

1. 确保 API Key 具备 `billing:read` 权限（参见权限配置文档）；  
2. 构造请求 URL，例如：  
   ```bash
   curl -X GET "https://dashscope.aliyuncs.com/api/v1/billing/overview?start_date=2024-01-01&end_date=2024-01-31" \
        -H "Authorization: Bearer YOUR_API_KEY"
   ```  
3. 解析 JSON 响应，重点关注 `data.total_amount`, `data.items` 等字段；完整结构请参考 [查询账单概览](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)。

## 限制和注意事项

- 单次请求时间跨度不得超过 90 天；  
- 每分钟调用频率上限为 60 次（按 API Key 限流）；  
- 账单数据延迟约 2 小时，`end_date` 不建议设为当前小时或更近时间点；  
- 所有金额单位为人民币（CNY），精确到小数点后 2 位，无四舍五入误差。

## 来源文档

- [账单](../../raw/model-api-reference/billing-api.md)


