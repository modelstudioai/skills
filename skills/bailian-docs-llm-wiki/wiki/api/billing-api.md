# billing api

billing api 是百炼平台提供的账单查询服务接口，用于获取模型调用产生的费用概览与趋势数据。开发者可通过该 API 实时监控资源消耗和成本分布，适用于财务对账、用量分析及预算控制等场景。所有接口均需通过阿里云统一身份认证（STS [Token](../concepts/token.md) 或 AccessKey）鉴权调用。

## 支持的模型/功能

billing api 不直接关联具体大模型（如 Qwen 系列），而是面向整个 Model Studio 计费体系提供通用账单能力，当前支持两类核心功能：
- `GetBillingOverview`：返回指定周期内（默认最近 30 天）的总费用、调用次数、[Token](../concepts/token.md) 消耗量等聚合指标；
- `GetBillingTrend`：按天/周/月粒度返回费用与用量的时间序列趋势，支持多维度分组（如按模型、工作空间、API 类型）。

> **注意**：原始文档中未明确说明是否支持按模型 ID 过滤账单明细，但 [账单 (raw/model-api-reference/billing-api.md)](../../raw/model-api-reference/billing-api.md) 仅列出两个顶层接口，未提供 `GetBillingDetail` 或类似明细查询能力，实际业务中如需明细请确认是否需调用阿里云费用中心 OpenAPI。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `StartTime` | string (ISO8601) | 是 | 查询起始时间，精度到日，不支持小时级；[账单 (raw/model-api-reference/billing-api.md)](../../raw/model-api-reference/billing-api.md) 中示例均使用 `YYYY-MM-DDT00:00:00Z` 格式 |
| `EndTime` | string (ISO8601) | 是 | 查询结束时间，需晚于 `StartTime`，且跨度不超过 90 天 |
| `Granularity` | string | 否 | 仅 `GetBillingTrend` 支持，取值 `DAILY` / `WEEKLY` / `MONTHLY`；默认 `DAILY` |
| `GroupBy` | string | 否 | 可选 `model`, `workspace`, `api_type`；注意部分取值在 [账单 (raw/model-api-reference/billing-api.md)](../../raw/model-api-reference/billing-api.md) 的官方文档链接中未完整列举，建议以最新 help.aliyun.com 接口文档为准 |

## 使用方式

1. 调用前确保已开通 Model Studio 服务并拥有 `AliyunModelStudioFullAccess` 或自定义策略（含 `modelstudio:GetBillingOverview` 和 `modelstudio:GetBillingTrend` 权限）；
2. 构造 HTTPS GET 请求，Endpoint 为 `https://modelstudio.aliyuncs.com`，Region 默认 `cn-shanghai`；
3. 示例请求（`GetBillingOverview`）：
   ```http
   GET /api/v1/billing/overview?StartTime=2024-01-01T00:00:00Z&EndTime=2024-01-31T23:59:59Z HTTP/1.1
   Host: modelstudio.aliyuncs.com
   Authorization: <STS Token or AK/SK signature>
   ```

## 限制和注意事项

- 单次查询时间跨度最大为 90 天，超出将返回 `InvalidParameter.TimeRangeExceeded` 错误；
- `GetBillingTrend` 最多返回 365 条趋势数据，若 `Granularity=DAILY` 且跨度超 365 天，需分段请求；
- 账单数据存在约 2–4 小时延迟，非实时计费结果；
- 所有接口均不支持跨阿里云主账号查询，子用户仅能访问其所属主账号下的账单数据。

## 来源文档

- [账单](../../raw/model-api-reference/billing-api.md)


