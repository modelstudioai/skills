# model monitoring

model monitoring 是百炼平台提供的模型调用行为可观测能力，用于追踪模型请求量、延迟、错误率等核心指标，并支持配置告警策略。该能力面向已部署的 API 模型（包括通义千问系列、Qwen-VL、Qwen-Audio 等）和自定义微调模型，不适用于控制台直接试用的沙箱环境。所有监控数据基于真实 API 调用日志聚合生成，延迟约 1–3 分钟。

## 支持的模型与功能

- **支持的模型类型**：所有通过 `POST /v1/services/aigc/text-generation`、`/v1/services/aigc/multimodal-generation` 等标准百炼 API 接入的模型，包括官方模型（如 `qwen-max`, `qwen-plus`）及用户上传的 LoRA 微调模型（需已发布为服务）  
- **核心功能**：  
  - 实时用量统计（QPS、总请求数、[Token](../concepts/token.md) 消耗）  
  - 延迟分布（P50/P90/P99）与错误码分桶（如 `429`, `500`, `model_not_found`）  
  - 自定义告警规则（阈值触发、持续周期、通知渠道）  
  - 可视化趋势图（按小时/天粒度，最长保留 90 天）  
  详细指标定义参见 [用量监控](../../raw/model-user-guide/model-monitoring.md)。

## 关键参数

监控能力通过 API 请求头与查询参数协同生效：  
- `X-Bailian-Trace-ID`：用于单请求链路追踪（需客户端透传），与 [模型用量](../../raw/model-monitoring/model-usage-statistics.md) 中的 trace 关联分析强依赖此字段  
- `X-Bailian-Model-ID`：显式声明调用模型 ID（推荐在多模型复用同一 endpoint 场景下设置），否则系统按实际路由模型自动识别  
- `start_time` / `end_time`（仅查询接口）：时间范围必须在最近 90 天内，且跨度 ≤ 7 天（批量拉取时）  
> **注意**：文档 [监控告警](../../raw/model-monitoring/model-telemetry.md) 中提到的 `alert_window_sec=300` 参数已被弃用，当前统一使用 `duration="5m"` 字符串格式，新配置请以控制台告警创建页为准。

## 使用方式

1. **启用监控**：无需额外开通，只要模型已发布为 API 服务且有真实调用，即自动采集  
2. **查看数据**：  
   - 控制台路径：`模型服务 > 服务管理 > 选择服务 > 监控`  
   - OpenAPI：调用 `GET /v1/monitoring/usage`（需 `service_id` 和时间范围）  
3. **配置告警**：在监控页点击「创建告警」，选择指标（如 `error_rate > 5% for 5m`），指定通知方式（Webhook / 钉钉 / 邮件）  
   具体告警配置逻辑详见 [监控告警](../../raw/model-monitoring/model-telemetry.md)。

## 限制和注意事项

- 单服务监控数据默认保留 90 天；如需长期归档，须调用 OpenAPI 导出并自行存储  
- [Token](../concepts/token.md) 统计仅覆盖 `input_tokens` + `output_tokens`，不含系统提示词或工具调用开销（该偏差已在 [用量监控](../../raw/model-user-guide/model-monitoring.md) 的“计量说明”章节明确标注）  
- 同一 `service_id` 下若存在灰度/AB 测试流量，监控页默认聚合全部流量；如需分桶分析，必须在请求中携带 `X-Bailian-Traffic-Tag` 标签  
- 错误率计算不含客户端超时（如 SDK 设置 `timeout=10s` 但服务端响应耗时 12s），此类请求不计入监控错误桶，仅记录为“无响应”  
- 每分钟最多触发 10 条告警通知（防刷），超出部分将被静默丢弃

## 来源文档

- [用量监控](../../raw/model-user-guide/model-monitoring.md)


