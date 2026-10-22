# model monitoring

model monitoring 是百炼平台提供的模型调用行为与性能指标的可观测能力，用于追踪用量、延迟、错误率等关键维度，支撑容量规划与故障排查。该功能默认启用，无需额外开通，但部分高级指标需配合特定模型版本或计费模式使用。详细背景和设计目标参见 [用量统计与性能监控](../../raw/model-user-guide/model-monitoring.md)。

## 支持的模型/功能

- 当前支持所有百炼托管模型（含 `qwen-max`、`qwen-plus`、`qwen-turbo` 及自定义微调模型），但部分细粒度指标（如 token 级拆分、reasoning step 耗时）仅对 v2.3+ 模型版本生效。
- 功能覆盖：请求量统计、P95/P99 延迟、HTTP 状态码分布、token 输入/输出计数、流式响应中断率。异常检测（如突增错误率）需在控制台手动配置告警规则，具体配置项见 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
- 注意：`qwen-vl-plus` 等多模态模型暂不支持图像 token 的独立计费统计，该限制已在 [用量统计与性能监控](../../raw/model-user-guide/model-monitoring.md) 中明确标注。

## 关键参数

- `start_time` / `end_time`：时间范围（ISO 8601 格式），最大跨度为 30 天；超出将被截断并返回警告。
- `model_name`：必填，需与模型注册名完全一致（区分大小写），例如 `qwen-turbo`；通配符 `*` 不被支持。
- `group_by`：可选值包括 `hour`、`day`、`model`、`api_key`，支持组合（如 `["model", "hour"]`），但最多指定 2 个维度。
- `metrics`：默认返回全部基础指标；若指定子集（如 `["request_count", "p95_latency_ms"]`），可减少响应体积。完整字段列表参见 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

## 使用方式

- 通过 REST API 调用 `/v1/monitoring/metrics` 端点，需携带 `Authorization: Bearer <api_key>` 和 `Content-Type: application/json`。
- 示例请求体：
  ```json
  {
    "start_time": "2024-06-01T00:00:00Z",
    "end_time": "2024-06-02T00:00:00Z",
    "model_name": "qwen-turbo",
    "group_by": ["hour"],
    "metrics": ["request_count", "error_rate"]
  }
  ```
- 返回数据为时间序列数组，每项含 `timestamp`、`value`（对象）、`labels`（分组键值）。聚合逻辑为服务端计算，客户端无需二次处理。

## 限制和注意事项

- 数据延迟：原始日志落盘延迟 ≤ 2 分钟，聚合指标可见延迟 ≤ 5 分钟；实时性要求高的场景请勿依赖秒级精度。
- 权限隔离：API Key 仅能查询其自身调用产生的监控数据，跨项目/跨账号不可见。
- > **注意**：文档 [用量统计与性能监控](../../raw/model-user-guide/model-monitoring.md) 中提及“支持按用户 ID 分组”，但当前 API 实际未开放 `user_id` 作为 `group_by` 选项，该描述已过时，请以接口实际响应为准。
- 免费版实例仅保留最近 7 天指标；标准版及以上保留 90 天，且支持导出 CSV。历史数据清理策略详见 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

## 来源文档

- [用量统计与性能监控](../../raw/model-user-guide/model-monitoring.md)


