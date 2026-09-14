# billing api

billing api 提供账单数据的程序化访问能力，支持查询账户级账单概览与时间趋势，适用于成本监控、自动化对账等场景。该 API 属于 Model Studio 服务的 OpenAPI 子集，需通过阿里云统一身份认证（AccessKey）调用。所有接口均遵循 RESTful 设计，返回 JSON 格式响应。

## 支持的模型/功能

当前 billing api 仅包含两个核心功能：
- `GetBillingOverview`：获取指定周期内（默认最近30天）的总消费金额、调用次数、模型分布等聚合指标；
- `GetBillingTrend`：按日/周/月粒度返回账单金额与调用次数的时间序列数据，支持最多180天的历史范围。

> **注意**：原始文档中未说明是否支持按模型实例或工作空间维度下钻查询；实际调用时若需细粒度账单，应参考 [账单](../../raw/model-api-reference/billing-api.md) 中链接的官方帮助文档确认权限与参数组合。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `StartTime` | string (ISO8601) | 是 | 查询起始时间，精度到日（如 `2024-01-01T00:00:00Z`） |
| `EndTime` | string (ISO8601) | 是 | 查询结束时间，需晚于 `StartTime`，且跨度 ≤ 180 天 |
| `Granularity` | string | 否 | 仅 `GetBillingTrend` 支持：`DAY` / `WEEK` / `MONTH`；默认 `DAY` |
| `RegionId` | string | 否 | 指定地域 ID，不传则返回全局账单（含所有已开通地域） |

注意：`GetBillingOverview` 不支持 `Granularity` 参数，若误传将被忽略；该行为与 [账单](../../raw/model-api-reference/billing-api.md) 中接口描述一致，但与部分旧版 SDK 示例存在出入。

## 使用方式

1. 确保 RAM 用户已授予 `modelstudio:GetBilling*` 权限（最小权限策略见 [账单](../../raw/model-api-reference/billing-api.md)）；
2. 构造 HTTPS GET 请求，Host 为 `modelstudio.aliyuncs.com`，Path 为 `/api/v1/billing/overview` 或 `/api/v1/billing/trend`；
3. 所有请求必须携带阿里云标准签名（V4），推荐使用 [aliyun-openapi-python-sdk](https://pypi.org/project/aliyun-openapi-python-sdk/) 自动处理；
4. 示例请求（curl）：
   ```bash
   curl -X GET "https://modelstudio.aliyuncs.com/api/v1/billing/overview?StartTime=2024-06-01T00:00:00Z&EndTime=2024-06-30T23:59:59Z" \
     -H "Authorization: acs <access_key_id>:<signature>"
   ```

## 限制和注意事项

- 单账号每分钟最多调用 60 次（QPS=1），超出将返回 `429 Too Many Requests`；
- `StartTime` 和 `EndTime` 必须在当前时间前推 180 天范围内，不支持查询未来账单；
- 返回数据延迟约 2–4 小时（非实时），最新消费可能尚未计入；
- 账单数据按自然日切分，`GetBillingTrend` 的 `DAY` 粒度结果以 UTC+0 时间为准，前端展示时需自行时区转换；
- 若发现接口返回空数据但控制台可见账单，请检查 `RegionId` 是否匹配资源部署地域——此问题已在 [账单](../../raw/model-api-reference/billing-api.md) 的 FAQ 区域明确提示。

## 来源文档

- [账单](../../raw/model-api-reference/billing-api.md)


