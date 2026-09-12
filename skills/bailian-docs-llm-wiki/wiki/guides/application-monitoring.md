# application monitoring

应用观测（Application Monitoring）是百炼平台提供的运行时可观测能力，用于追踪大模型应用的请求链路、性能指标与资源消耗。它支持对 API 调用、模型推理、工具调用等关键环节进行细粒度监控，并提供可视化仪表盘与告警配置能力。该功能默认启用，无需额外部署探针，但需在应用创建时开启「启用观测」开关。

## 支持的模型/功能

- 支持所有百炼托管模型（包括 Qwen 系列、Qwen-VL、Qwen-Audio 及第三方接入模型）的端到端调用链路追踪  
- 支持多跳 RAG 流程中检索、重排、生成各阶段的耗时与成功率统计  
- 支持自定义工具（Tool Calling）的执行状态、输入/输出摘要与错误分类  
- 支持并发请求量、P95 延迟、[Token](../concepts/token.md) 消耗量、失败率等核心业务指标聚合  
- 不支持非百炼 SDK 发起的直连调用（如手动构造 HTTP 请求绕过 SDK）的完整链路还原  

> **注意**：原始文档中提及的「用量监控与性能分析」链接指向 Model Studio 帮助中心，但该页面实际描述的是旧版 Model Studio 的独立监控能力；百炼平台当前的应用观测能力已统一收敛至 [应用观测 (raw/application-user-guide/application-monitoring.md)](../../raw/application-user-guide/application-monitoring.md)，其功能范围与数据模型均以该文档为准。

## 关键参数

| 参数名 | 类型 | 说明 | 默认值 |
|--------|------|------|--------|
| `enable_monitoring` | boolean | 是否启用应用级观测（创建后不可修改） | `true` |
| `sampling_rate` | number (0.0–1.0) | 全链路采样率，设为 `0.1` 表示 10% 请求被完整追踪 | `0.05` |
| `trace_ttl_days` | integer | 调用链路数据保留天数 | `7` |
| `metric_granularity` | string | 指标聚合粒度（`minute` / `hour`） | `minute` |

## 使用方式

1. 创建应用时，在「高级设置」中勾选「启用观测」；若已创建，需重建应用才能开启（[应用观测 (raw/application-user-guide/application-monitoring.md)](../../raw/application-user-guide/application-monitoring.md) 明确说明该配置为只读）  
2. 部署后，通过控制台「应用详情 → 观测」页查看实时仪表盘与历史趋势  
3. 调用 `/v1/applications/{app_id}/traces` 接口可拉取原始 trace 数据（需携带 `X-Bailian-Trace-Query-Token`）  
4. 如需对接外部 APM（如 Prometheus），可启用 OpenTelemetry Exporter，配置 endpoint 为 `https://otel.bailian.aliyuncs.com/v1/traces`（详见 [应用观测 (raw/application-user-guide/application-monitoring.md)](../../raw/application-user-guide/application-monitoring.md)）

## 限制和注意事项

- 单应用最大支持 1000 TPS 的全量 trace 上报，超限后自动降级为采样模式  
- [Token](../concepts/token.md) 统计仅基于模型侧返回的 `usage` 字段，不包含预处理/后处理阶段的文本长度计算  
- 自定义工具的错误分类依赖 `tool_result.status` 字段，若未按规范返回 `success`/`failed`/`timeout`，将归类为 `unknown`  
- 当前不支持跨应用（multi-app）联合链路追踪，同一用户在不同应用间的调用无法关联  
- 所有 trace 数据经脱敏处理，原始 [prompt](prompt.md) 和 response 内容默认不落盘，如需审计需单独申请开通（参见 [应用观测 (raw/application-user-guide/application-monitoring.md)](../../raw/application-user-guide/application-monitoring.md) 中的「数据保留策略」章节）

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring.md)



