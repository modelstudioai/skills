# billing api

billing api 是百炼平台提供的用于查询账户账单信息的一组 RESTful 接口，支持按时间范围获取账单概览与消费趋势数据。所有接口均需通过 API Key 认证，并遵循统一的请求签名与错误响应规范。该能力面向企业级用户和开发者，适用于成本监控、财务对账及自动化报表等场景。

## 支持的模型/功能

billing api 当前提供两类核心功能：
- `GET /api/v1/billing/overview`：返回指定周期内（默认最近30天）的总消费金额、调用次数、模型分布等聚合指标；
- `GET /api/v1/billing/trend`：返回按日/周/月粒度划分的消费趋势序列，支持多维度分组（如按 model、project_id 或 region）。

上述功能定义详见 [账单](../../raw/model-api-reference/billing-api.md) 文档的导航结构，具体接口契约请参考其子文档。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `start_date` | string (YYYY-MM-DD) | 是 | 查询起始日期（含），支持最大90天跨度 |
| `end_date` | string (YYYY-MM-DD) | 是 | 查询结束日期（含） |
| `granularity` | string | 否 | `day` / `week` / `month`；仅 `trend` 接口有效，默认 `day` |
| `group_by` | string[] | 否 | 如 `["model", "project_id"]`；仅 `trend` 接口支持，最多2个字段 |

注意：`overview` 接口不支持 `group_by` 和 `granularity`，若传入将被忽略。此行为与 [查询账单概览](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 的参数说明一致。

## 使用方式

1. 确保已开通百炼平台计费服务并绑定支付方式；
2. 在控制台「API 密钥管理」中创建具备 `billing:read` 权限的 API Key；
3. 构造带 `X-Api-Key` 请求头的 HTTPS GET 请求，例如：

```bash
curl -X GET \
  "https://dashscope.aliyuncs.com/api/v1/billing/overview?start_date=2024-01-01&end_date=2024-01-31" \
  -H "X-Api-Key: sk-xxx"
```

完整请求示例与响应格式见 [查询账单趋势](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 文档。

## 限制和注意事项

- 单次查询时间跨度不得超过 90 天；
- 每分钟调用频率上限为 60 次（按 API Key 维度限流）；
- 账单数据延迟约 2 小时（即 T+2 小时可查 T 时刻消费）；
- > **注意**：原始文档中 `api-modelstudio-2026-02-10-getbillingoverview.md` 提到支持 `currency=USD` 参数，但当前线上版本尚未实现该字段，传入将被静默忽略；实际返回货币单位始终为 CNY。

## 来源文档

- [账单](../../raw/model-api-reference/billing-api.md)


