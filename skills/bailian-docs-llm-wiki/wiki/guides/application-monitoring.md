# application monitoring

应用观测（Application Monitoring）是百炼平台提供的运行时可观测能力，用于追踪大模型应用的请求链路、性能指标与资源消耗。它支持对 API 调用、模型推理、工具调用等关键环节进行细粒度监控，并提供可视化仪表盘与告警配置能力。该功能默认启用，无需额外部署探针，但需在应用创建时开启「启用观测」开关。

## 支持的模型/功能

- 支持所有百炼托管模型（包括 Qwen 系列、Qwen-VL、Qwen-Audio 及第三方接入模型）的端到端延迟、[Token](../concepts/token.md) 消耗、错误率统计  
- 支持多跳 RAG 流程中检索、重排、生成各阶段的耗时拆分  
- 支持自定义工具（Function Calling）调用链路追踪，含入参/出参采样（默认关闭，需通过 `trace_tool_inputs` 参数启用）  
- 支持基于 OpenTelemetry 兼容格式导出 trace 数据，可对接外部 APM 系统  
详情请参考 [应用观测](../../raw/application-user-guide/application-monitoring.md)。

## 关键参数

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `enable_monitoring` | boolean | `true` | 应用级总开关，创建后不可修改；设为 `false` 将完全禁用所有观测数据采集 |
| `trace_sampling_rate` | number (0.0–1.0) | `0.1` | trace 采样率，设为 `0` 表示关闭 trace，仅保留 metrics |
| `log_level` | string (`error`, `warn`, `info`) | `warn` | 控制日志上报级别，`info` 级别将记录完整输入输出（含敏感字段，慎用） |
| `trace_tool_inputs` | boolean | `false` | 是否在 trace 中记录工具调用的原始输入参数（含可能的 PII 数据） |

> **注意**：`log_level: info` 在 [应用观测](../../raw/application-user-guide/application-monitoring.md) 中被标记为「不推荐生产环境启用」，但部分旧版 SDK 文档未同步该限制，请以该文档为准。

## 使用方式

1. 创建应用时，在「高级设置」中勾选「启用观测」（对应 `enable_monitoring: true`）  
2. 部署后，访问控制台 → 应用详情页 → 「观测」标签页，查看实时指标与 trace 列表  
3. 如需调试单次请求，可在调用 API 时添加 HTTP Header：`X-Bailian-Trace-ID: <custom-id>`，该 ID 将透传至所有下游服务并聚合显示  
4. 导出 trace 数据：在观测页点击「导出 JSON」，或通过 `/v1/monitoring/traces` 接口按时间范围拉取（需 `monitoring:read` 权限）  
完整操作指引见 [应用观测](../../raw/application-user-guide/application-monitoring.md)。

## 限制和注意事项

- 单应用 trace 存储保留期为 7 天，metrics 数据保留 30 天  
- trace 采样率超过 `0.3` 时可能导致高并发下数据丢失，建议压测期间临时调高，日常保持 ≤0.1  
- 启用 `trace_tool_inputs` 后，trace 数据体积显著增大，且可能违反 GDPR/《个人信息保护法》，必须确保已获得用户明确授权  
- 当前不支持跨应用（multi-app）联合 trace，即 A 应用调用 B 应用 API 时，B 的 trace 不会自动关联至 A 的父 span  
- 若发现 trace 中缺失模型推理阶段耗时，可能是由于使用了异步流式响应但未正确调用 `stream_end` 回调 —— 请确认 SDK 版本 ≥ v3.2.1，详见 [应用观测](../../raw/application-user-guide/application-monitoring.md)。

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring.md)


