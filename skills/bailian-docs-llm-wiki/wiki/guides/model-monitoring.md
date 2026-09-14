# model monitoring

model monitoring 是百炼平台提供的模型调用行为与性能指标观测能力，用于追踪请求量、延迟、错误率等核心运行时指标，支持问题定位与容量规划。该功能面向已部署的 API 模型（包括通义千问系列、文本嵌入、多模态等），无需额外埋点即可自动采集。详细能力边界和配置方式请参考 [用量统计与性能监控](../../raw/model-user-guide/model-monitoring.md)。

## 支持的模型/功能

- **支持模型类型**：所有通过百炼控制台部署的 API 模型（含 `qwen-max`、`qwen-plus`、`text-embedding-v1` 等），不支持直接调用 [OpenAI 兼容接口](../concepts/openai-compatibility.md)的第三方模型代理。
- **核心监控维度**：
  - 请求量（QPS、总调用数）
  - 延迟（P50/P90/P99、首 token 延迟）
  - 错误率（HTTP 4xx/5xx、模型内部错误 code）
  - [Token](../concepts/token.md) 消耗（输入/输出 token 数，按模型精度分项统计）
- 实时告警、历史趋势分析、按应用/模型/环境（prod/staging）多维下钻均已在 [用量统计与性能监控](../../raw/model-user-guide/model-monitoring.md) 中说明。

## 关键参数

- `app_id`：必填，标识调用方应用（需在百炼控制台创建并绑定模型）
- `model_id`：可选，指定监控粒度为某具体模型实例（默认聚合当前 app 下全部模型）
- `time_range`：支持 `last_1h` / `last_24h` / `custom`（ISO8601 时间范围），最小时间粒度为 1 分钟
- `metrics`：可选，如 `["request_count", "p99_latency_ms", "error_rate"]`，未指定则返回全部默认指标  
> **注意**：`custom` 时间范围在部分旧版 SDK 中存在解析异常，建议优先使用预设范围，详见 [用量统计与性能监控](../../raw/model-user-guide/model-monitoring.md) 的“API 调用示例”章节。

## 使用方式

1. **控制台查看**：进入「模型服务」→「监控中心」，选择目标应用与时间范围，图表自动渲染。
2. **API 查询**：调用 `GET /v1/monitor/metrics`，需携带 `Authorization: Bearer <access_token>` 和上述关键参数。
3. **告警配置**：在监控中心点击「创建告警规则」，支持基于错误率 >5% 或 P99 延迟 >3000ms 触发钉钉/邮件通知（配置入口见 [用量统计与性能监控](../../raw/model-user-guide/model-monitoring.md)）。

## 限制和注意事项

- 监控数据延迟：最大 2 分钟（非实时流式上报，不适用于毫秒级故障诊断）。
- 数据保留期：原始指标保留 30 天，聚合报表保留 90 天。
- 单次 API 查询最多返回 1000 条时间序列点；超限时需缩小 `time_range` 或增大 `step` 参数。
- 不支持对异步任务（如 `batch_inference`）的细粒度延迟拆解，仅统计整体请求生命周期。

## 来源文档

- [用量统计与性能监控](../../raw/model-user-guide/model-monitoring.md)


