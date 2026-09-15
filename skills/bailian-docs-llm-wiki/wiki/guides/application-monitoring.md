# application monitoring

应用观测（Application Monitoring）是百炼平台提供的核心可观测性能力，用于实时追踪大模型应用的调用链路、性能指标与资源消耗。它支持对 API 调用、推理延迟、Token 使用量、错误率等关键维度进行细粒度采集与可视化分析。该能力默认集成于所有通过百炼控制台或 SDK 部署的应用实例中，无需额外埋点。

## 支持的模型/功能

- 支持所有在百炼平台托管的模型服务，包括 Qwen 系列（Qwen1.5、Qwen2、Qwen2.5）、Qwen-VL、Qwen-Audio 及用户自定义微调模型（LoRA/QLoRA）  
- 提供三大核心观测维度：  
  - **调用链路追踪**：基于 OpenTelemetry 标准，自动注入 trace_id，支持跨服务上下文透传  
  - **性能指标监控**：端到端延迟（P95/P99）、首 Token 延迟、生成 Token 数、输入 Token 数、模型加载耗时  
  - **资源与用量统计**：GPU 显存占用峰值、vCPU 使用率、每分钟请求数（RPM）、累计 Token 消耗量  
- 详细功能说明见 [应用观测](../../raw/application-user-guide/application-monitoring.md)

## 关键参数

以下参数可通过 `monitoring_config` 字段在应用部署配置（YAML 或 SDK `create_app` 接口）中启用或调整：

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `enabled` | boolean | `true` | 是否启用观测；设为 `false` 将完全禁用数据采集与上报 |
| `sample_rate` | float (0.0–1.0) | `0.1` | trace 采样率；生产环境建议 ≤0.2 以降低开销 |
| `include_input` | boolean | `false` | 是否在 trace 中记录原始输入内容（含 [prompt](prompt.md)）；**开启将影响隐私合规性**，仅调试阶段建议启用 |
| `metrics_granularity` | string | `"1m"` | 指标聚合粒度，支持 `"1m"`, `"5m"`, `"1h"` |

> **注意**：`include_input` 在 [用量监控与性能分析](../../raw/application-user-guide/application-monitoring/application-observation.md) 中被标记为 `deprecated`，新版本 SDK 已移除该字段，实际行为以当前 SDK 文档为准。

## 使用方式

1. **控制台启用**：在「应用管理 → 应用详情 → 监控」页签中，开关默认开启；可点击「查看监控大盘」跳转 Grafana 实时视图  
2. **API/SDK 配置**：在创建或更新应用时，传入 `monitoring_config` 对象（参考 [应用观测](../../raw/application-user-guide/application-monitoring.md) 中的 YAML 示例）  
3. **查询 trace**：通过 `/v1/traces` REST API 或 `list_traces()` SDK 方法，按 `app_id`、`status`、时间范围检索；trace 数据保留 7 天  
4. **自定义指标上报**：支持通过 OpenTelemetry SDK 手动打点（需使用百炼兼容的 OTLP endpoint：`https://otel-api.bailian.aliyuncs.com/v1/traces`）

## 限制和注意事项

- 单应用 trace 上报 QPS 上限为 100，超出部分将被限流并返回 `429 Too Many Requests`  
- `sample_rate = 1.0` 仅允许在测试环境使用，生产环境强制降级为 `0.2`（由平台侧拦截）  
- 不支持对流式响应（`stream=true`）的逐 chunk 延迟拆分统计，当前仅记录整体完成延迟  
- 所有监控数据均经脱敏处理，但若启用 `include_input`，原始 [prompt](prompt.md) 将明文落盘——该行为已在 [用量监控与性能分析](../../raw/application-user-guide/application-monitoring/application-observation.md) 中明确列为高风险操作，强烈建议禁用

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring.md)


