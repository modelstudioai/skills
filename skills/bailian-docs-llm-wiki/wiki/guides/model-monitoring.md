# model monitoring

model monitoring 是百炼平台提供的模型调用行为与性能指标观测能力，用于跟踪模型的请求量、延迟、错误率等核心运行时指标，支持基于阈值的告警配置。该功能面向已部署的 API 模型（包括通义千问系列、文本嵌入、多模态等）及工作流中调用的模型节点。监控数据默认保留 30 天，需通过控制台或 OpenAPI 主动启用。

## 支持的模型/功能

- 支持所有通过百炼控制台部署的 **API 模型**（如 `qwen-max`, `qwen-plus`, `text-embedding-v1` 等）及 **工作流中引用的模型节点**  
- 提供三大维度监控：**用量统计**（调用次数、[Token](../concepts/token.md) 消耗）、**性能指标**（P50/P90 延迟、首 [Token](../concepts/token.md) 时间）、**稳定性指标**（HTTP 4xx/5xx 错误率、模型内部错误 `model_error`）  
- 告警能力依赖 [监控告警](https://help.aliyun.com/zh/model-studio/model-telemetry) 文档所定义的规则配置机制，具体指标支持范围详见 [原文标题](../../raw/model-user-guide/model-monitoring.md)

## 关键参数

- `model_id`：必填，模型唯一标识（如 `qwen-max-20240601`），需与部署时一致  
- `start_time` / `end_time`：时间范围（ISO8601 格式），最大跨度为 7 天；超出将被截断并返回部分数据  
- `granularity`：支持 `1m`（1 分钟）、`5m`、`1h`；若未指定，默认为 `5m`  
- `metrics`：可选数组，如 `["request_count", "p90_latency_ms", "error_rate_5xx"]`；完整列表见 [原文标题](../../raw/model-user-guide/model-monitoring.md)  

## 使用方式

1. **控制台操作**：进入「模型管理」→ 选择目标模型 → 「监控」页签，可查看实时图表与导出 CSV  
2. **OpenAPI 调用**：使用 `GetModelMonitoringData` 接口（`POST /api/v1/models/{model_id}/monitoring/data`），需携带 `Authorization` Header 及上述参数  
3. **告警配置**：在「告警管理」中新建规则，绑定模型 ID 与监控指标；阈值触发逻辑以 [监控告警](https://help.aliyun.com/zh/model-studio/model-telemetry) 文档为准 —— 注意该文档中 `error_rate_5xx` 的计算口径与 [原文标题](../../raw/model-user-guide/model-monitoring.md) 中定义的 `error_rate`（含 4xx+5xx）存在差异  
> **注意**：`error_rate` 指标在 [原文标题](../../raw/model-user-guide/model-monitoring.md) 中明确定义为「HTTP 4xx 与 5xx 总和 / 总请求数」，而 [监控告警](https://help.aliyun.com/zh/model-studio/model-telemetry) 文档仅提及 5xx，实际告警策略应以 `error_rate` 为准，避免漏报客户端错误。

## 限制和注意事项

- 单次 API 查询最多返回 10,000 条时间序列点；若粒度设为 `1m` 且查询 7 天，将自动降级为 `5m`  
- 工作流中模型节点的监控数据仅在工作流启用「全链路追踪」后生效（需在工作流编辑器中开启）  
- 监控数据存在约 2–5 分钟延迟，不适用于亚秒级故障定位  
- [Token](../concepts/token.md) 统计基于模型服务端解析结果，与 SDK 客户端上报值可能存在微小偏差（如 streaming 场景下分块计数差异）

## 来源文档

- [用量统计与性能监控](../../raw/model-user-guide/model-monitoring.md)


