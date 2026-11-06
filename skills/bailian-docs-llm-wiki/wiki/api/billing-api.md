# billing api

billing api 是百炼平台提供的用于查询账户账单信息的一组 RESTful 接口，支持按时间范围获取账单概览与消费趋势数据。所有接口均需通过 API Key 认证，并遵循统一的错误响应格式。该 API 不提供账单导出或发票开具能力，相关功能请参考 [账单 (raw/model-api-reference/billing-api.md)](../../raw/model-api-reference/billing-api.md)。

## 支持的模型/功能

当前 billing api 仅提供两类只读功能：
- `GET /billing/overview`：返回指定周期内总消费金额、调用次数、模型维度分布等聚合摘要（详见 [查询账单概览](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)）；
- `GET /billing/trend`：返回按日/周/月粒度划分的消费金额与调用量变化曲线（详见 [查询账单趋势](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)）。

> **注意**：原始文档 [账单 (raw/model-api-reference/billing-api.md)](../../raw/model-api-reference/billing-api.md) 中未声明任何模型专属计费字段（如 `qwen-max` 或 `qwen-plus` 的独立用量），实际响应中 `model_name` 字段值为平台级服务标识（如 `"modelstudio"`），并非具体推理模型名称。此行为与 model api 的模型枚举不一致，请勿将 billing api 的 `model_name` 与 `/v1/chat/completions` 等接口中的模型名直接映射。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `start_date` | string (YYYY-MM-DD) | 是 | 查询起始日期（含），最早支持 90 天前 |
| `end_date` | string (YYYY-MM-DD) | 是 | 查询结束日期（含），不可晚于当前日期 |
| `granularity` | string | 否 | `day`（默认）、`week` 或 `month`；仅 `GET /billing/trend` 支持 |
| `region` | string | 否 | 地域标识（如 `cn-beijing`），若不传则返回全地域汇总 |

所有参数均通过 query string 传递，无 request body。认证使用 `Authorization: Bearer <API_KEY>`。

## 使用方式

1. 确保 API Key 具备 `billing:read` 权限（参见 [账单 (raw/model-api-reference/billing-api.md)](../../raw/model-api-reference/billing-api.md) 的权限说明）；
2. 构造请求 URL，例如：  
   `GET https://dashscope.aliyuncs.com/api/v1/billing/overview?start_date=2024-01-01&end_date=2024-01-31`
3. 发送请求并解析 JSON 响应；成功时 HTTP 状态码为 `200`，结构与 [查询账单概览](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 文档定义一致。

## 限制和注意事项

- 单次查询时间跨度不得超过 90 天；
- 每分钟调用频率上限为 60 次（按 API Key 维度限流）；
- `start_date` 和 `end_date` 必须满足 `start_date <= end_date`，否则返回 `400 Bad Request`；
- 账单数据存在最多 2 小时延迟，实时性要求高的场景请避免依赖最新 2 小时数据；
- 该 API 不返回明细账单（如单次请求 ID、token 数量），如需明细，请使用控制台导出 CSV 功能。

## 来源文档

- [账单](../../raw/model-api-reference/billing-api.md)


