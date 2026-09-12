# application monitoring

应用观测（Application Monitoring）是百炼平台提供的运行时可观测能力，用于追踪模型服务的调用链路、统计请求量/延迟/错误率等核心指标，并支持基于指标的告警配置。该功能默认启用，无需额外部署探针，适用于所有通过百炼 API 网关发布的模型服务。详细背景与设计目标见 [应用观测](../../raw/application-user-guide/application-monitoring.md)。

## 支持的模型/功能

- 支持所有已发布至生产环境的模型服务（包括 `qwen-max`、`qwen-plus`、自定义微调模型及 RAG 应用）
- 提供三大维度监控：**调用量（QPS/总请求数）**、**性能（P50/P95/P99 延迟、首 [Token](../concepts/token.md) 时间）**、**稳定性（HTTP 4xx/5xx 错误率、模型内部错误码）**
- 支持按 `model_id`、`app_id`、`region`、`api_version` 多维下钻分析，且可导出近 30 天原始指标数据
- 实时日志采样（1% 默认采样率）支持错误上下文追溯，详情参见 [用量监控与性能分析](../../raw/application-user-guide/application-monitoring.md)

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `start_time` / `end_time` | ISO8601 字符串 | 是 | 查询时间范围，最大跨度为 7 天（单次请求）；超过需分页拉取 |
| `metrics` | string 数组 | 否 | 可选值：`["qps", "latency_p95", "error_rate_5xx"]`；未指定则返回全部基础指标 |
| `group_by` | string 数组 | 否 | 支持 `["model_id", "app_id", "status_code"]`；最多指定 2 个维度 |

> **注意**：文档中曾提及 `group_by: ["region"]` 为合法值，但实测 v2.3.0+ API 返回 `400 Bad Request`；当前仅支持上述 3 个维度，以 [用量监控与性能分析](../../raw/application-user-guide/application-monitoring.md) 中最新接口规范为准。

## 使用方式

1. **控制台查看**：进入「模型服务」→ 选择目标模型 → 「监控」页签，默认展示最近 1 小时聚合图表  
2. **API 调用**：调用 `GET /v1/monitoring/metrics`（需携带 `Authorization: Bearer <token>`），示例：
   ```bash
   curl -H "Authorization: Bearer $API_KEY" \
        "https://dashscope.aliyuncs.com/v1/monitoring/metrics?start_time=2024-06-01T00:00:00Z&end_time=2024-06-01T01:00:00Z&metrics[]=latency_p95&group_by[]=model_id"
   ```
3. **告警配置**：在监控页签点击「创建告警规则」，支持基于 `error_rate_5xx > 0.05` 或 `latency_p95 > 5000` 等条件触发钉钉/邮件通知

## 限制和注意事项

- 指标数据延迟：实时指标最大延迟为 60 秒，历史数据聚合延迟不超过 5 分钟  
- 数据保留：原始监控数据保留 30 天，聚合指标（如日粒度）保留 90 天  
- 权限要求：调用监控 API 需具备 `dashscope:MonitorRead` 权限策略，否则返回 `403 Forbidden`  
- 不支持对 `debug` 环境或本地调试模式（`--local-mode`）的服务进行观测，该限制已在 [应用观测](../../raw/application-user-guide/application-monitoring.md) 中明确说明

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring.md)


