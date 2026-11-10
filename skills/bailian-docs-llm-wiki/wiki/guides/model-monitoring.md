# model monitoring

model monitoring 是百炼平台提供的模型调用行为可观测性能力，用于追踪模型请求量、延迟、错误率等核心指标，并支持配置阈值告警。该能力面向已部署的 API 接口（含自定义模型和百炼托管模型），不依赖用户侧埋点，数据由平台统一采集与聚合。详细设计目标可参考 [用量监控](../../raw/model-user-guide/model-monitoring.md)。

## 支持的模型/功能

- **支持模型类型**：所有通过百炼控制台发布为 API 的模型，包括 `qwen-max`、`qwen-plus` 等百炼内置模型，以及用户上传并部署的 `custom:xxx` 类型模型  
- **核心监控维度**：每分钟请求数（QPM）、P95/P99 延迟（ms）、HTTP 状态码分布（2xx/4xx/5xx）、[Token](../concepts/token.md) 消耗量（input/output）  
- **告警能力**：支持基于 QPM 下降、错误率突增、延迟超阈值等场景配置企业微信/邮件通知，具体规则配置见 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)

## 关键参数

| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `time_range` | string | 查询时间范围，支持 `last_1h` / `last_24h` / `last_7d` | `last_24h` |
| `granularity` | string | 聚合粒度，仅限 `1m`（分钟级）或 `1h`（小时级） | `1m` |
| `model_id` | string | 必填，模型唯一标识（如 `qwen-max` 或 `custom:my-llm-v2`） | — |
| `status_code` | int | 可选，过滤指定 HTTP 状态码（如 `500`） | 全部 |

> **注意**：文档 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) 中提到的 `region` 参数在 v3.2+ 版本已废弃，实际调用时传入将被忽略；当前所有监控数据按账号全局聚合，不区分地域。

## 使用方式

1. **控制台查看**：进入「模型管理 → 已部署模型 → 监控」页，选择时间范围与粒度，图表自动刷新  
2. **API 查询**：调用 `GET /v3/monitoring/metrics`，需携带 `Authorization: Bearer <api_key>` 和 `model_id` 参数  
3. **告警配置**：在「告警中心 → 新建规则」中选择 `model_telemetry` 类型，关联目标模型后设置触发条件（详见 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）

## 限制和注意事项

- 数据延迟：监控指标从请求完成到平台可查约有 **60–90 秒** 延迟，不适用于亚秒级实时诊断  
- 历史数据保留：原始粒度（1 分钟）数据保留 **7 天**；聚合后（1 小时）数据保留 **90 天**  
- 权限约束：仅 `admin` 和 `monitoring_reader` 角色可访问监控数据；`model_developer` 角色默认无权查看，需显式授权  
- 自定义模型 [Token](../concepts/token.md) 统计：仅当模型服务返回标准 `x-bailian-token-count` Header 时才计入用量，否则该字段恒为 `0`（参见 [用量监控](../../raw/model-user-guide/model-monitoring.md)）

## 来源文档

- [用量监控](../../raw/model-user-guide/model-monitoring.md)


