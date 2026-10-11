# model monitoring

model monitoring 是百炼平台提供的模型调用行为与性能指标采集能力，用于追踪模型请求量、延迟、错误率等核心运行时数据，支撑容量规划与异常诊断。该功能默认启用，无需额外配置，但部分高级指标需在控制台开启对应开关。所有监控数据均按模型 ID 和 API Key 维度聚合，支持近实时查询（延迟约 30 秒）。

## 支持的模型/功能

- 支持全部百炼托管模型（包括 `qwen-max`、`qwen-plus`、`qwen-turbo` 等）及用户自部署的 vLLM/Serving 模型（需接入百炼 Telemetry Agent）  
- 提供两类基础能力：**用量统计**（调用量、Token 消耗、费用估算）和 **性能监控**（P50/P95 延迟、HTTP 状态码分布、超时/拒绝率）  
- 告警能力依赖 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)，需在控制台配置阈值规则；用量明细可导出 CSV，详见 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)

## 关键参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `model_id` | string | 必填，目标模型唯一标识（如 `qwen-max`） |
| `start_time` / `end_time` | ISO8601 时间戳 | 查询时间范围，最大跨度 30 天；超出将截断并返回警告 |
| `granularity` | string | 可选 `1m` / `5m` / `1h` / `1d`；`1m` 粒度仅保留最近 2 小时数据，历史数据自动降采样为 `5m` |

> **注意**：原始文档 [用量统计与性能监控](../../raw/model-user-guide/model-monitoring.md) 中提及“支持按 API Key 维度下钻”，但当前 API 实际仅支持 `model_id` + `api_key_hash`（哈希后不可逆）组合过滤，详细字段约束见 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)

## 使用方式

1. **控制台查看**：进入「模型管理 → 目标模型 → 监控」页，选择时间范围与指标类型  
2. **API 查询**：调用 `GET /v1/monitoring/metrics`，需携带 `Authorization: Bearer <access_token>` 与上述关键参数  
3. **告警配置**：在「告警中心 → 创建规则」中选择 `model.*` 类指标，阈值触发后推送至钉钉/邮件；配置入口与逻辑说明见 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)

## 限制和注意事项

- 单次 API 查询最多返回 10,000 条时间序列点，建议缩小 `granularity` 或缩短时间窗口  
- Token 统计基于请求/响应内容长度粗略估算（非精确 tokenizer 计数），与账单系统存在 ≤3% 偏差  
- 自部署模型必须部署 [Telemetry Agent v2.3+](../../raw/model-user-guide/model-monitoring/model-telemetry.md)，低于此版本无法上报延迟与错误详情  
- 所有监控数据默认保留 90 天，不支持手动延长；如需长期归档，请调用 API 定期拉取并落库

## 来源文档

- [用量统计与性能监控](../../raw/model-user-guide/model-monitoring.md)


