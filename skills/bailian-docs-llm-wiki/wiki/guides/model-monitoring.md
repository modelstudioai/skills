# model monitoring

model monitoring 是百炼平台提供的模型调用行为可观测能力，用于追踪模型请求量、延迟、错误率等核心指标，并支持配置阈值告警。该功能面向已部署的 API 模型（包括通义千问系列、Qwen-VL、Qwen-Audio 等）和自定义微调模型，不适用于控制台内直接试用的沙箱环境。所有监控数据基于真实 API 调用日志聚合生成，延迟约 1–3 分钟。

## 支持的模型与功能

- **支持模型类型**：所有通过 `POST /v1/chat/completions`、`/v1/completions` 或 `/v1/embeddings` 接口调用的百炼托管模型（含基础模型、微调模型、Agent 编排节点），但不支持 `model_type=local` 的私有部署模型 [用量监控](../../raw/model-user-guide/model-monitoring.md)。  
- **核心功能**：  
  - 实时用量统计（QPS、总请求数、Token 消耗）  
  - 延迟分布（p50/p95/p99）与错误码分类（4xx/5xx）  
  - 自定义告警规则（支持 HTTP 状态码、响应时间、失败率阈值）  
  - 可视化趋势图（按小时/天粒度，最长保留 90 天）  

## 关键参数

监控数据按 `model_id` + `api_key` 维度隔离。关键可配置项包括：  
- `alert_threshold.failure_rate`：失败率告警阈值（默认 5%，最小 0.1%）  
- `alert_threshold.latency_p95_ms`：P95 延迟告警阈值（默认 5000 ms）  
- `time_window_minutes`：告警评估窗口（支持 1/5/15/60 分钟，默认 5）  
> **注意**：`alert_threshold.latency_p95_ms` 在 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) 中定义为毫秒整数，但实际 API 接收浮点值；建议统一使用整数以避免校验失败。

## 使用方式

1. 登录百炼控制台 → 进入「模型管理」→ 选择目标模型 → 点击「监控」页签  
2. 默认展示最近 24 小时用量概览；点击「配置告警」可设置规则并绑定企业微信/钉钉/邮件通知  
3. 所有监控数据可通过 OpenAPI 获取：`GET /v1/monitoring/metrics?model_id={id}&start_time={ts}&end_time={ts}`（需 `monitoring:read` 权限）  
4. 告警事件推送格式详见 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)

## 限制和注意事项

- 监控数据仅从 `X-Bailian-Request-ID` 非空且成功返回 `200 OK` 的请求中采集；流式响应（`stream=true`）的延迟统计以首个 chunk 返回时间为基准  
- 单个模型最多配置 10 条活跃告警规则；超出后需停用旧规则才能新增  
- Token 统计基于模型侧实际计费 Token 数（含 system prompt 和 function call schema），与请求体中 `input_tokens` 字段可能不一致  
- 历史数据不可回溯补采：若未提前开启监控，此前调用无记录 [用量监控](../../raw/model-user-guide/model-monitoring.md)

## 来源文档

- [用量监控](../../raw/model-user-guide/model-monitoring.md)


