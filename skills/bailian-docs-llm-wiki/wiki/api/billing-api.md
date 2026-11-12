# billing api

billing api 是百炼平台提供的用于查询账户账单信息的一组 RESTful 接口，支持按时间范围获取账单概览与消费趋势数据。所有接口均需通过 API Key 认证，并遵循统一的错误响应格式。该 API 适用于开发者集成财务监控、成本分析或自动化对账能力。

## 支持的模型/功能

当前 billing api 提供两类核心功能：
- `GET /billing/overview`：返回指定周期内（默认最近30天）的总消费金额、调用次数、模型维度分布等聚合数据；
- `GET /billing/trend`：返回按日/周/月粒度划分的消费趋势曲线，支持多模型、多项目（Project ID）维度筛选。

这两项能力在 [查询账单概览](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 和 [查询账单趋势](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 文档中有详细定义，包括各字段语义与示例响应。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `start_date` | string (YYYY-MM-DD) | 是 | 查询起始日期（含），最早支持 90 天前 |
| `end_date` | string (YYYY-MM-DD) | 是 | 查询结束日期（含），不可晚于当前日期 |
| `project_id` | string | 否 | 指定项目 ID，留空则返回全部项目汇总 |
| `granularity` | string | 否 | 仅 `trend` 接口支持，可选 `day`/`week`/`month`，默认 `day` |

> **注意**：[查询账单概览](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 文档中曾标注 `end_date` 可省略（自动设为今日），但实测未提供默认值时将返回 400 错误；请始终显式传入该参数以确保兼容性。

## 使用方式

1. 在百炼控制台「API 密钥管理」中创建具备 `billing:read` 权限的 API Key；
2. 发起 HTTPS GET 请求，Header 中携带 `Authorization: Bearer <your_api_key>`；
3. 示例请求（curl）：
   ```bash
   curl -X GET "https://dashscope.aliyuncs.com/api/v1/billing/overview?start_date=2024-01-01&end_date=2024-01-31" \
        -H "Authorization: Bearer sk-xxx"
   ```

完整请求路径、状态码说明及响应结构详见 [查询账单概览](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)。

## 限制和注意事项

- 单次查询时间跨度不得超过 90 天；
- 每个 API Key 每分钟最多调用 60 次（QPM），超出将返回 `429 Too Many Requests`；
- 账单数据延迟约 2 小时，即 `end_date=2024-01-01` 的结果不包含当日 00:00–02:00 的消费；
- 所有接口均不支持跨账号查询，`project_id` 必须属于当前 API Key 所属主账号。

> **注意**：原始文档 [查询账单趋势](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 中描述的 `model_type` 过滤参数已下线，实际调用时传入将被忽略；请改用 `model_name` 字段进行模型级筛选（如 `qwen-max`, `qwen-plus`）。

## 来源文档

- [账单](../../raw/model-api-reference/billing-api.md)


