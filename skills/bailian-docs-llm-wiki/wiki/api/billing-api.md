# billing api

billing api 是百炼平台提供的账单数据查询接口集合，用于获取账户级账单概览、消费趋势等核心计费信息。所有接口均基于 RESTful 设计，需通过 API Key 认证，并遵循统一的错误响应格式。开发者可通过该 API 实现自动化账单监控、成本分析与预算告警。

## 支持的模型/功能

当前 billing api 仅提供两类账单查询能力：  
- **账单概览**：返回指定周期内总消费金额、已用额度、剩余额度及各服务（如 Model Studio、API 调用）的分项费用；  
- **账单趋势**：按日/周/月粒度返回连续时间段内的消费变化曲线，支持多维度聚合（如按模型、地域、计费类型）。  
> **注意**：文档中未提及对预留实例、资源包抵扣明细或退款记录的查询能力，相关需求请参考 [账单 (raw/model-api-reference/billing-api.md)](../../raw/model-api-reference/billing-api.md) 的后续更新说明。

## 关键参数

所有 billing api 接口共用以下必需参数：  
- `start_date`（string, YYYY-MM-DD）：查询起始日期（含）；  
- `end_date`（string, YYYY-MM-DD）：查询结束日期（含），跨度最长支持 90 天；  
- `granularity`（string, optional）：仅 `getbillingtrend` 支持，可选 `daily` / `weekly` / `monthly`；  
- `service_type`（string, optional）：过滤特定服务，如 `model_studio`, `api_call`，详见 [查询账单趋势](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 文档。

## 使用方式

1. 确保调用方已开通账单查询权限（RAM Policy 中需包含 `bss:Describe*` 权限）；  
2. 构造 HTTPS GET 请求，Host 为 `billing.aliyuncs.com`，Path 为对应接口路径（如 `/api/v1/billing/overview`）；  
3. 在 Header 中携带 `Authorization: Bearer <API_KEY>`；  
4. 示例请求（账单概览）：  
   ```bash
   curl -H "Authorization: Bearer ak-xxx" \
        "https://billing.aliyuncs.com/api/v1/billing/overview?start_date=2024-01-01&end_date=2024-01-31"
   ```  
详细请求结构与响应字段定义请参阅 [查询账单概览](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md)。

## 限制和注意事项

- 单账号每分钟最多发起 60 次 billing api 调用（QPS 限制）；  
- `start_date` 与 `end_date` 必须在近 180 天范围内，且 `end_date` 不得晚于当前日期；  
- 账单数据存在约 2 小时延迟，实时性要求高的场景不建议依赖该 API；  
- 若发现 `getbillingtrend` 返回的 `total_amount` 与 `getbillingoverview` 同期结果不一致，请以 [查询账单概览](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 为准，该差异已在 [账单 (raw/model-api-reference/billing-api.md)](../../raw/model-api-reference/billing-api.md) 的 v2026-03 版本中修复。

## 来源文档

- [账单](../../raw/model-api-reference/billing-api.md)


