# model monitoring

model monitoring 是百炼平台提供的模型调用行为与性能指标观测能力，用于追踪请求量、延迟、错误率等核心运行时数据，支撑稳定性分析与成本优化。该功能默认启用，无需额外配置即可查看基础指标；高级告警与自定义维度需通过控制台或 OpenAPI 配置。所有监控数据基于实际 API 调用实时采集，延迟通常在 30 秒以内。

## 支持的模型/功能

- 支持全部已接入百炼平台的托管模型（包括 `qwen-max`、`qwen-plus`、`qwen-turbo` 及第三方模型），但**不支持本地部署模型或 BYOvCPU 场景下的私有模型实例**。
- 提供两类核心能力：  
  - **用量统计**：按小时/天粒度聚合调用次数、Token 消耗（输入/输出分别统计）、费用估算；详见 [用量统计与性能监控](../../raw/model-user-guide/model-monitoring.md)。  
  - **性能监控**：P50/P95/P99 延迟、HTTP 状态码分布、模型内部错误码（如 `model_timeout`、`context_length_exceeded`）；该能力依赖模型服务层埋点，部分旧版模型可能缺失部分错误维度，具体覆盖情况请参考 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

## 关键参数

- `model_name`（必需）：模型唯一标识符，必须与 `model.list` 接口返回的 `id` 字段完全一致（区分大小写）。  
- `start_time` / `end_time`（必需）：时间范围需满足 `end_time - start_time ≤ 30 days`，且时间戳为 ISO 8601 格式（如 `2024-01-01T00:00:00Z`）。  
- `granularity`（可选）：支持 `hour`（默认）、`day`；注意 `hour` 粒度下最多返回最近 7 天数据，超出部分自动降级为 `day`，此行为与 [用量统计与性能监控](../../raw/model-user-guide/model-monitoring.md) 中描述一致。  
- `dimensions`（可选）：支持 `api_key_id`、`app_id`、`error_code` 等分组字段，但 `error_code` 仅对启用了详细错误上报的模型生效（参见 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。

## 使用方式

- **控制台**：进入「监控中心」→「模型监控」页，选择目标模型与时间范围，支持图表可视化与 CSV 导出。  
- **OpenAPI**：调用 `GET /v1/monitoring/models/{model_name}/metrics`，需携带 `Authorization: Bearer <access_token>` 及上述查询参数。  
- **告警配置**：仅支持通过控制台设置阈值告警（如 P95 延迟 > 5s 或错误率 > 1%），当前 API 不开放告警规则创建接口——该限制在 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) 中未明确说明，但实测 `POST /v1/alerts` 返回 `405 Method Not Allowed`，请以控制台为准。

## 限制和注意事项

- 单次 API 查询最多返回 10,000 条时间序列数据点；若结果超限，需缩小时间范围或提高 `granularity`。  
- Token 统计基于模型服务层解析，**不等同于客户端实际发送的 Token 数**（例如经百炼路由转发、重试或流式响应拆分可能导致差异），精确计费以账单系统为准。  
- > **注意**：原始文档 [用量统计与性能监控](../../raw/model-user-guide/model-monitoring.md) 提到“支持按用户 ID 分组”，但当前 API 与控制台均未开放 `user_id` 维度，该描述已过时，应忽略。  
- > **注意**：[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) 中称“所有模型默认开启全量错误码上报”，但实测 `qwen-turbo` v2.3.1 版本仍仅上报 `5xx` 状态码，不返回具体 `error_code`，建议升级至 v2.4+ 或联系技术支持确认模型版本兼容性。

## 来源文档

- [用量统计与性能监控](../../raw/model-user-guide/model-monitoring.md)


