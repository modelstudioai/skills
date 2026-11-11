# billing api

billing api 是百炼平台提供的账单数据查询接口集合，用于获取账户级账单概览、消费趋势等财务信息。所有接口均需通过 HTTPS 调用，使用 Bearer Token 进行身份认证。该 API 不支持实时扣费查询或明细级账单导出，仅提供聚合维度的统计视图。

## 支持的模型/功能

billing api 当前提供两类核心功能：  
- **账单概览**：返回指定周期内总消费金额、用量分布（按模型、服务类型）、账户余额等摘要信息；  
- **账单趋势**：按日/周/月粒度返回近 365 天的消费金额与调用量变化曲线。  
> **注意**：文档中未提及对 `modelstudio-2026-02-10` 版本以外的 API 版本支持，实际调用时请严格匹配 [查询账单概览](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 和 [查询账单趋势](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 的路径与参数格式，避免因版本不一致导致 404 或字段缺失。

## 关键参数

所有 billing api 接口共用以下必需参数：  
- `start_date`（string, YYYY-MM-DD）：查询起始日期（含），不可早于 90 天前；  
- `end_date`（string, YYYY-MM-DD）：查询结束日期（含），不可晚于当前日期；  
- `granularity`（string, 可选）：仅 `getbillingtrend` 支持，取值 `daily` / `weekly` / `monthly`；  
- `model_type`（string, 可选）：过滤特定模型类型（如 `text-generation`, `embedding`），详见 [查询账单概览](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 的枚举说明。

## 使用方式

1. 确保已开通百炼平台计费权限，并在控制台获取有效的 AccessKey ID 与 Secret；  
2. 构造请求 URL，例如：  
   `GET https://dashscope.aliyuncs.com/api/v1/billing/overview?start_date=2024-01-01&end_date=2024-01-31`；  
3. 在 `Authorization` Header 中传入 `Bearer <your_token>`；  
4. 解析 JSON 响应中的 `data` 字段，注意检查 `code` 是否为 `200`，非 `200` 时参考 [查询账单趋势](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingtrend.md) 的错误码表处理异常。

## 限制和注意事项

- 单次查询时间跨度不得超过 90 天；  
- 每个账户每分钟最多发起 60 次 billing api 请求（QPS 限制）；  
- 返回数据延迟约 2 小时（即 T+2 小时可查 T 时刻消费）；  
- `getbillingoverview` 不支持按项目（project_id）维度筛选，仅支持账户全局视角——此行为与部分旧版文档描述存在差异，请以 [查询账单概览](../../raw/model-api-reference/billing-api/api-modelstudio-2026-02-10-getbillingoverview.md) 实际响应结构为准。

## 来源文档

- [账单](../../raw/model-api-reference/billing-api.md)


