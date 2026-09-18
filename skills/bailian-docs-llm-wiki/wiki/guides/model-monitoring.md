# model monitoring

model monitoring 是百炼平台提供的模型调用行为与性能指标采集能力，用于跟踪模型请求量、延迟、错误率等核心运行时指标，支持基于阈值的告警配置。该功能默认启用，无需额外开通，但需确保调用方正确传递 `X-Trace-ID` 等上下文字段以保障指标归因准确性。详细设计目标与数据语义请参见 [用量统计与性能监控](../../raw/model-user-guide/model-monitoring.md)。

## 支持的模型/功能

- 支持所有通过百炼 API（`/v1/chat/completions`、`/v1/embeddings` 等）调用的托管模型（含 Qwen 系列、Qwen-VL、Qwen-Audio 及第三方接入模型）  
- 提供两类核心能力：**用量统计**（按模型、应用、时间粒度聚合调用量、Token 消耗、费用估算）和 **性能监控**（P50/P95 延迟、HTTP 状态码分布、服务端错误分类）  
- 告警能力依赖 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) 文档中定义的规则引擎，当前仅支持邮件与 Webhook 通知方式  

## 关键参数

- `model`（必填）：模型 ID，需与 `/v1/models` 接口返回的 `id` 字段严格一致  
- `app_id`（可选）：应用标识，用于多租户维度聚合；若未传，则归入 `default` 分组  
- `trace_id`（推荐）：应与请求头 `X-Trace-ID` 一致，否则延迟与错误链路无法关联至原始调用  
- 时间范围：所有查询接口默认按小时粒度聚合，最小支持 5 分钟窗口（需显式指定 `granularity=5m`）  
> **注意**：[用量统计与性能监控](../../raw/model-user-guide/model-monitoring.md) 中提及的 `user_id` 参数在 v2.3+ 版本已废弃，实际生效字段仅为 `app_id` 和 `model`

## 使用方式

1. **查看实时指标**：调用 `GET /v1/monitoring/metrics`，传入 `model` 和 `start_time`/`end_time`（ISO8601 格式）  
2. **配置告警规则**：通过控制台「监控告警」页或 `POST /v1/monitoring/alert-rules` 创建，规则条件支持 `latency_p95 > 3000` 或 `error_rate > 0.05` 等表达式  
3. **导出历史数据**：使用 `GET /v1/monitoring/export`，支持 CSV/JSON 格式，单次最多导出 7 天数据  
所有接口均需 `Authorization: Bearer <api_key>` 认证，权限由 API Key 所属角色控制。完整字段说明与示例见 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

## 限制和注意事项

- 数据保留周期为 30 天，超期后自动清理，不支持延长  
- 每个 `app_id` 下最多创建 20 条活跃告警规则；超出后需停用旧规则方可新增  
- Token 统计基于模型实际返回内容计算，**不包含系统提示词（system [prompt](prompt.md)）的 Token**，与账单计费逻辑一致  
- 若调用方未透传 `X-Trace-ID`，则 `latency` 指标将缺失首跳网络延迟，仅反映服务端处理耗时  
> **注意**：[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) 文档中描述的“支持短信通知”功能尚未上线，当前仅邮件与 Webhook 可用，该描述将在下个文档版本中修正

## 来源文档

- [用量统计与性能监控](../../raw/model-user-guide/model-monitoring.md)


