# model monitoring

model monitoring 是百炼平台提供的模型调用行为与性能指标观测能力，用于追踪用量、延迟、错误率等关键维度，支撑容量规划与异常诊断。该功能默认启用，无需额外开通，但部分高级指标需配合特定模型版本或配额权限。所有监控数据均按自然日聚合，T+1 可查。

## 支持的模型/功能

- 支持全部百炼托管模型（包括 `qwen-max`、`qwen-plus`、`qwen-turbo` 等）及用户自部署的 API 接入模型（需符合 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) 中定义的上报规范）  
- 提供两类核心能力：**用量统计**（调用量、[Token](../concepts/token.md) 消耗、费用估算）和 **性能监控**（P95 延迟、HTTP 状态码分布、重试率）  
- 告警能力依赖 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) 配置，支持基于阈值或同比波动触发企业微信/邮件通知  

## 关键参数

| 参数 | 说明 | 是否必需 | 备注 |
|------|------|----------|------|
| `model_name` | 模型唯一标识（如 `qwen-max`），用于指标过滤 | 是 | 必须与 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) 中注册名称一致 |
| `start_time` / `end_time` | ISO8601 时间范围（UTC），最大跨度 30 天 | 是 | 超出 T+1 数据延迟期将返回空结果 |
| `granularity` | `day`（默认）或 `hour` | 否 | `hour` 粒度仅保留最近 7 天数据 |

> **注意**：原始文档中提及的 `region` 参数在最新 SDK v2.3+ 已废弃，实际请求中传入将被忽略；请以 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) 的当前接口定义为准。

## 使用方式

1. **控制台查看**：登录百炼控制台 →「模型服务」→「监控中心」，选择目标模型与时间范围即可可视化查看  
2. **API 查询**：调用 `GET /v1/monitoring/metrics`，需携带 `Authorization: Bearer <api_key>` 和上述关键参数  
3. **告警配置**：通过 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) 页面创建规则，支持组合条件（如 `error_rate > 5% AND p95_latency > 3000ms`）

## 限制和注意事项

- 单次 API 查询最多返回 10,000 条时间序列点；超出需分页（`next_token` 字段）  
- 自部署模型必须主动上报 `x-bailian-request-id` 和标准 OpenTelemetry trace header，否则无法关联至 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) 维度  
- 免费额度内的 [Token](../concepts/token.md) 消耗不计入费用估算字段，该行为与 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) 中“计费一致性”说明存在偏差，建议以账单系统为准

## 来源文档

- [用量统计与性能监控](../../raw/model-user-guide/model-monitoring.md)


