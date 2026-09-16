# billing api

billing api 是百炼平台提供的账单数据查询接口集合，用于获取账户级账单概览、消费趋势等核心计费信息。所有接口均基于 RESTful 设计，需通过 API Key 进行身份认证，并遵循统一的版本前缀（如 `2026-02-10`）。该能力面向企业客户和开发者，适用于成本监控、财务对账与自动化报表等场景。

## 支持的模型/功能

当前 billing api 仅提供两类账单查询能力，不涉及模型调用或推理功能：  
- **账单概览**：返回指定周期内总消费金额、已用额度、剩余额度及服务维度汇总（如 Model Studio、API 调用等）；  
- **账单趋势**：按日/周/月粒度返回连续时间段内的消费金额变化曲线，支持多服务类型分组聚合。  
> **注意**：文档中未提及按项目（Project）或工作空间（Workspace）粒度拆分账单的能力，[查询账单概览](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 和 [查询账单趋势](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 均仅支持账户（Account）级别聚合，与部分旧版控制台文档描述的“项目级账单导出”存在口径不一致，以本 API 行为为准。

## 关键参数

所有 billing api 接口共用以下必需参数：  
- `start_date`（string, YYYY-MM-DD）：查询起始日期（含），不可早于 90 天前；  
- `end_date`（string, YYYY-MM-DD）：查询结束日期（含），不可晚于今日；  
- `granularity`（string, 可选）：仅 `getbillingtrend` 支持，取值 `daily` / `weekly` / `monthly`；  
- `service_type`（string, 可选）：过滤特定服务，如 `model_studio`, `api_call`，默认返回全部。  
详细字段定义请参考 [查询账单概览](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 的响应结构说明。

## 使用方式

1. **认证**：在 HTTP Header 中携带 `Authorization: Bearer <API_KEY>`；  
2. **请求地址**：`https://dashscope.aliyuncs.com/api/v1/billing/{endpoint}`，其中 `{endpoint}` 为 `getbillingoverview` 或 `getbillingtrend`；  
3. **示例请求**（curl）：  
   ```bash
   curl -X GET \
     "https://dashscope.aliyuncs.com/api/v1/billing/getbillingtrend?start_date=2024-01-01&end_date=2024-01-31&granularity=daily" \
     -H "Authorization: Bearer sk-xxx"
   ```  
完整调用规范与错误码详见 [查询账单趋势](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 文档。

## 限制和注意事项

- 单次查询时间跨度不得超过 90 天；  
- 每个 API Key 每分钟限流 60 次（QPM），超出将返回 `429 Too Many Requests`；  
- 账单数据延迟约 2–4 小时，当日消费可能未实时计入；  
- 所有接口均不支持跨账号查询，且无法返回明细流水（如单次 API 调用 ID、模型名称、Token 数等），如需明细请使用控制台导出或对接 [费用中心 OpenAPI](../../raw/finance/finance-billing-detail.md)（注意路径差异）。

## 来源文档

- [账单](../../raw/model-api-reference/billing-api.md)


