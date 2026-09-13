# billing api

billing api 提供账单数据查询能力，支持获取账户级账单概览与时间维度的消费趋势，适用于成本分析、预算监控等场景。所有接口均通过 HTTPS 调用，需使用阿里云 AccessKey 进行签名认证。该 API 属于 Model Studio 服务的计费子系统，版本为 `2026-02-10`。

## 支持的模型/功能

当前 billing api 仅提供两类只读功能：
- `GetBillingOverview`：返回指定周期内（默认最近30天）的总费用、已用额度、剩余配额等聚合指标；
- `GetBillingTrend`：按日/周/月粒度返回连续时间段内的费用变化曲线，支持最多90天历史数据拉取。

> **注意**：原始文档中未提及对模型调用明细（如 per-model token 消耗）的支持，与 [账单 (raw/model-api-reference/billing-api.md)](../../raw/model-api-reference/billing-api.md) 所列功能范围一致；但需注意，[Model Studio 计费说明](../../raw/model-api-reference/pricing.md) 中提到的“按模型实例计费”细节无法通过本 API 获取，属功能缺口。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `StartTime` | string (ISO8601) | 是 | 查询起始时间，精度到日，格式如 `2024-01-01T00:00:00Z` |
| `EndTime` | string (ISO8601) | 是 | 查询结束时间，必须晚于 `StartTime`，且跨度 ≤90 天 |
| `Granularity` | string | 否 | 仅 `GetBillingTrend` 支持，可选 `DAILY` / `WEEKLY` / `MONTHLY`；默认 `DAILY` |
| `BillingCycle` | string | 否 | 仅 `GetBillingOverview` 支持，指定账期（如 `2024-01`），若不传则按自然月滚动计算 |

所有请求均需携带标准阿里云公共请求头（`x-acs-version`, `x-acs-signature-nonce`, `Authorization` 等），详情见 [账单 (raw/model-api-reference/billing-api.md)](../../raw/model-api-reference/billing-api.md)。

## 使用方式

1. 构造请求 URL（以 `GetBillingTrend` 为例）：  
   `POST https://modelstudio.aliyuncs.com/?Action=GetBillingTrend&Version=2026-02-10`
2. 设置请求体（JSON 格式）：
   ```json
   {
     "StartTime": "2024-05-01T00:00:00Z",
     "EndTime": "2024-05-31T23:59:59Z",
     "Granularity": "DAILY"
   }
   ```
3. 使用阿里云 SDK（推荐 Python/Java）或自行实现签名逻辑；参考 [账单 (raw/model-api-reference/billing-api.md)](../../raw/model-api-reference/billing-api.md) 中的签名示例。

## 限制和注意事项

- 单账号 QPS 限流为 5，超出将返回 `Throttling` 错误；
- `GetBillingOverview` 不支持跨账期聚合，若需多月对比需多次调用；
- 返回数据延迟约 2 小时（即 T+2 可查 T 时刻消费），不适用于实时扣费监控；
- 接口不返回明细账单（如具体模型、API 调用次数、token 数量），如需该类数据，请使用阿里云费用中心导出 CSV 或调用 `CostExplorer` 服务。

## 来源文档

- [账单](../../raw/model-api-reference/billing-api.md)


