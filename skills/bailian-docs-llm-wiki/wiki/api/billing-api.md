# billing api

billing api 是百炼平台提供的用于查询账户账单数据的 RESTful 接口集合，支持按时间范围获取账单概览与消费趋势。所有接口均需使用 `Bearer` 认证，并通过 `X-Studio-Region` 指定地域（如 `cn-beijing`）。该 API 仅面向已开通计费功能的企业版用户开放，不支持个人免费额度查询。

## 支持的模型/功能

当前 billing api 仅提供两类账单查询能力：
- **账单概览**：返回指定周期内总消费金额、调用次数、用量明细（按模型分组）等聚合信息，对应接口 [查询账单概览](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)；
- **账单趋势**：返回按日/周/月粒度划分的消费金额与调用次数变化曲线，支持多模型对比，对应接口 [查询账单趋势](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md)。

> **注意**：原始文档中未列出任何模型名称或具体计费项映射关系；实际支持的模型列表以 [查询账单概览](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 响应中的 `model_name` 字段为准，常见值包括 `qwen-max`、`qwen-plus`、`qwen-turbo` 等，但 `qwen-vl` 和 `qwen-audio` 在部分旧版响应中可能缺失计费标识，建议以最新接口返回为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `start_date` | string (YYYY-MM-DD) | 是 | 查询起始日期（含），支持最大 90 天跨度 |
| `end_date` | string (YYYY-MM-DD) | 是 | 查询结束日期（含），不可晚于当前日期 |
| `granularity` | string | 否 | 趋势接口专用，取值 `day` / `week` / `month`；概览接口忽略此参数 |
| `model_name` | string | 否 | 指定模型过滤（如 `qwen-max`），为空时返回全部模型汇总 |

所有请求必须携带 `X-Studio-Region` 请求头，且 region 需与账单归属地域一致；否则将返回 `403 Forbidden`。详情见 [查询账单趋势](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 的认证章节。

## 使用方式

1. 获取有效的 API Key（需具备 `billing:read` 权限）；
2. 构造 HTTPS GET 请求，例如：
   ```bash
   curl -X GET \
     "https://dashscope.aliyuncs.com/api/v1/billing/overview?start_date=2024-01-01&end_date=2024-01-31" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "X-Studio-Region: cn-beijing"
   ```
3. 解析 JSON 响应，重点关注 `data.items`（概览）或 `data.trends`（趋势）字段。

完整请求示例与响应结构详见 [查询账单概览](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)。

## 限制和注意事项

- 单次查询时间跨度上限为 90 天，超出将返回 `400 Bad Request`；
- 接口调用频率限制为 10 次/分钟/账号，超限返回 `429 Too Many Requests`；
- 账单数据延迟约 2 小时，当日消费通常在次日 02:00 后可查；
- `model_name` 参数区分大小写，且必须与控制台模型管理页显示的名称完全一致（例如 `qwen-max` ≠ `Qwen-Max`）；
- > **注意**：[查询账单趋势](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 文档中示例使用了 `v1/billing/trend` 路径，但生产环境实际路径为 `v1/billing/trends`（复数形式），请以最新 SDK 或 OpenAPI 规范为准。

## 来源文档

- [账单](../../raw/model-api-reference/billing-api.md)


