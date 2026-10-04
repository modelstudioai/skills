# model monitoring

model monitoring 是百炼平台提供的模型调用行为与性能指标的可观测能力，用于追踪用量、延迟、错误率等关键维度，支撑容量规划与故障排查。该功能默认启用，无需额外开通，但部分高级指标需配合特定模型版本或配额权限。所有监控数据均按项目（Project）隔离，且保留周期为 30 天。

## 支持的模型/功能

- 支持全部已接入百炼平台的托管模型（包括 `qwen-max`、`qwen-plus`、`qwen-turbo` 及自定义微调模型），但 [模型用量](raw/model-user-guide/model-monitoring/model-usage-statistics.md) 中的 token 粒度统计仅对 v2.3+ 版本模型生效；  
- 提供两类核心能力：**用量统计**（请求量、输入/输出 token 数、费用估算）和 **性能监控**（P95 延迟、HTTP 状态码分布、重试率）；  
- 告警规则配置依赖 [监控告警](raw/model-user-guide/model-monitoring/model-telemetry.md) 模块，支持基于阈值或同比异常触发企业微信/邮件通知。

## 关键参数

| 参数 | 类型 | 说明 | 是否必需 |
|------|------|------|----------|
| `project_id` | string | 项目唯一标识，用于数据隔离与权限校验 | 是 |
| `start_time` / `end_time` | ISO8601 | 查询时间范围，跨度不可超过 7 天 | 是 |
| `model_name` | string | 模型名称（如 `qwen-turbo`），支持通配符 `*` | 否（留空则聚合全模型） |
| `granularity` | enum | `minute` / `hour` / `day`，影响指标聚合粒度 | 否（默认 `hour`） |

> **注意**：原始文档 [用量统计与性能监控 (raw/model-user-guide/model-monitoring.md)](../../raw/model-user-guide/model-monitoring.md) 中提及“支持按 API Key 维度拆分”，但该能力已于 v3.1 版本下线，实际仅支持 `project_id` 维度，详见 [模型用量](raw/model-user-guide/model-monitoring/model-usage-statistics.md) 的最新说明。

## 使用方式

1. **API 调用**：通过 `GET /v1/monitoring/metrics` 接口获取指标数据，需在 Header 中携带 `Authorization: Bearer <access_token>`；  
2. **控制台查看**：登录百炼控制台 → 进入「监控中心」→ 选择目标项目 → 切换至「模型调用」页签；  
3. **告警配置**：在 [监控告警](raw/model-user-guide/model-monitoring/model-telemetry.md) 页面创建规则，例如设置 `error_rate > 5% for 5m` 触发通知；  
4. **导出数据**：控制台支持 CSV 导出，API 返回 JSON 格式，字段结构与 [用量统计与性能监控 (raw/model-user-guide/model-monitoring.md)](../../raw/model-user-guide/model-monitoring.md) 中定义一致。

## 限制和注意事项

- 单次查询最多返回 10,000 条时间序列点，超限时需缩小时间范围或提高 `granularity`；  
- 错误码 `429`（Rate Limit Exceeded）不计入 `error_rate`，因其属于限流策略而非模型服务异常；  
- 自定义微调模型的 token 统计精度依赖于推理引擎版本，v2.2 以下版本可能高估输入 token 数，建议升级至 [模型用量](raw/model-user-guide/model-monitoring/model-usage-statistics.md) 所述的兼容版本；  
- 所有监控数据延迟约 2–5 分钟，不适用于实时 SLA 验证场景。

## 来源文档

- [用量统计与性能监控](../../raw/model-user-guide/model-monitoring.md)


