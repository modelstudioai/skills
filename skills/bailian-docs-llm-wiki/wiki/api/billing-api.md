# billing api

billing api 提供账单数据查询能力，支持获取账户级账单概览与时间维度的消费趋势，适用于成本分析、预算监控等场景。所有接口均通过 HTTPS 调用，需使用阿里云 AccessKey 进行签名认证。该 API 属于 Model Studio 服务的计费子系统，版本为 `2026-02-10`。

## 支持的模型/功能

当前 billing api 仅提供两类只读功能：
- `GetBillingOverview`：返回指定周期内（默认最近30天）的总费用、已用额度、剩余额度等聚合指标；
- `GetBillingTrend`：按日/周/月粒度返回指定时间范围内各时段的费用变化曲线，支持最多90天跨度。

> **注意**：原始文档中未提及对具体模型（如 Qwen、Qwen2-VL）的账单拆分能力；若需按模型维度统计，应结合 [模型调用日志](../../raw/model-api-reference/model-logging.md) 与账单 API 交叉分析 —— 此能力在 [账单 (raw/model-api-reference/billing-api.md)](../../raw/model-api-reference/billing-api.md) 中未说明，属平台隐式行为，非 API 原生支持。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `StartTime` | string (ISO8601) | 是 | 查询起始时间，精度到日，格式如 `2025-04-01T00:00:00Z` |
| `EndTime` | string (ISO8601) | 是 | 查询结束时间，需晚于 `StartTime`，且跨度 ≤ 90 天 |
| `Granularity` | string | 否 | 仅 `GetBillingTrend` 使用，可选 `DAILY` / `WEEKLY` / `MONTHLY`；默认 `DAILY` |
| `RegionId` | string | 否 | 指定地域，如 `cn-shanghai`；不传则返回全局账单（含所有已开通地域） |

所有请求均需携带标准阿里云公共请求头（`x-acs-signature-nonce`, `x-acs-signature-method`, `x-acs-version` 等），详情见 [账单 (raw/model-api-reference/billing-api.md)](../../raw/model-api-reference/billing-api.md)。

## 使用方式

1. 确保主账号或 RAM 子用户已授予 `modelstudio:DescribeBilling*` 权限；
2. 构造请求 URL，例如 `https://modelstudio.cn-shanghai.aliyuncs.com/?Action=GetBillingOverview&Version=2026-02-10&StartTime=2025-04-01T00:00:00Z&EndTime=2025-04-30T23:59:59Z`；
3. 使用阿里云 SDK（如 Python 的 `aliyun-python-sdk-modelstudio`）或自行实现签名逻辑发起调用；
4. 解析 JSON 响应中的 `Data` 字段，结构详见 [账单 (raw/model-api-reference/billing-api.md)](../../raw/model-api-reference/billing-api.md)。

## 限制和注意事项

- 单次 `GetBillingTrend` 请求最多返回 90 个时间点的数据（如 `DAILY` 模式下最多查90天）；
- `StartTime` 和 `EndTime` 必须落在过去180天内，不支持查询历史超期账单；
- 接口响应延迟通常 < 2s，但首次调用或跨大时间范围时可能达 5s，建议添加超时重试（最大重试 2 次）；
- 账单数据存在约 2–4 小时延迟，实时性要求高的场景请勿依赖最新1小时内消费数据。

## 来源文档

- [账单](../../raw/model-api-reference/billing-api.md)



