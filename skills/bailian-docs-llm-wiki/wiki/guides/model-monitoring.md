# model monitoring

model monitoring 是百炼平台提供的模型调用行为与性能指标观测能力，用于追踪模型请求量、延迟、错误率等核心运行时指标，支持基于阈值的告警配置。该功能面向已部署的 API 模型（包括通义千问系列、Qwen-VL、Qwen-Audio 等）和自定义微调模型，不适用于本地加载或离线推理场景。所有监控数据默认保留 30 天，可通过控制台或 OpenAPI 查询。

## 支持的模型与功能

- **支持模型类型**：所有通过百炼控制台「模型服务」部署的托管模型（含基础模型、微调模型、Agent 绑定模型），但不支持直接调用 `dashscope` SDK 的裸模型调用（需接入百炼网关才可被监控）。
- **核心功能**：
  - 实时用量统计（QPS、总请求数、[Token](../concepts/token.md) 消耗量）  
  - 性能指标（P50/P90/P99 延迟、首 [Token](../concepts/token.md) 时间、生成 [Token](../concepts/token.md) 时间）  
  - 错误分析（HTTP 状态码分布、`ErrorCode` 分类、`RateLimitExceeded` 等高频错误）  
  - 告警规则配置（支持邮件/钉钉/Webhook 通知）  
  详细能力说明见 [用量统计与性能监控](../../raw/model-user-guide/model-monitoring.md)。

## 关键参数

监控数据按以下维度聚合与暴露：
- `model_id`：必填，对应模型在百炼中的唯一标识（如 `qwen-max-20240815`）  
- `time_range`：支持 `last_1h` / `last_24h` / `custom`（UTC 时间范围，精度至分钟）  
- `granularity`：`1m`（1 分钟）、`5m`、`1h`（仅限 24h 内查询）  
- `metrics`：可选 `request_count`, `error_rate`, `avg_latency_ms`, `token_usage_input`, `token_usage_output`  
- `filter`：支持按 `status_code`, `error_code`, `region` 过滤（注意：`region` 仅对多地域部署模型有效）  
参数语义与约束详见 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) 和 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

## 使用方式

1. **控制台操作**：进入「模型服务」→ 选择目标模型 → 「监控」页签，可查看图表与导出 CSV；告警配置在「告警管理」中统一设置。  
2. **OpenAPI 调用**：调用 `GET /v1/monitoring/metrics`（需 `model_id` + `time_range`），响应为 JSON 格式时间序列数据。  
3. **埋点要求**：必须使用百炼 SDK（`@alibaba/bailian-js-sdk`）或百炼网关 URL（`https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`）发起请求，直连 DashScope 域名的调用不会被采集。  
> **注意**：文档 [用量统计与性能监控](../../raw/model-user-guide/model-monitoring.md) 中提及“支持任意 DashScope 接口监控”，该描述已过时；实际仅限经百炼网关路由的流量，详见 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) 的「数据采集范围」章节。

## 限制和注意事项

- 数据延迟：监控指标存在最大 2 分钟延迟，告警触发延迟通常为 3–5 分钟。  
- Token 统计：输入/输出 Token 数基于模型实际接收与返回内容计算，不含系统提示词（system [prompt](prompt.md)）的硬编码部分。  
- 权限控制：仅模型拥有者及具有 `ModelMonitorReadOnly` 或更高权限的角色可查看监控数据。  
- 免费额度：监控功能本身不额外计费，但所依赖的底层日志存储与计算资源计入项目配额；超出配额后监控数据将停止写入（不触发告警）。  
- 历史数据：原始日志保留 7 天，聚合指标保留 30 天；如需长期归档，请调用 OpenAPI 定期拉取并自行存储。  
更多细节请参考 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

## 来源文档

- [用量统计与性能监控](../../raw/model-user-guide/model-monitoring.md)


