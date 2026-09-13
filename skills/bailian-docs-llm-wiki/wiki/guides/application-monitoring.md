# application monitoring

应用观测（Application Monitoring）是百炼平台提供的运行时可观测能力，用于追踪大模型应用的请求链路、性能指标与资源消耗。它支持对 API 调用、模型推理、工具调用等关键环节进行细粒度埋点与聚合分析，帮助开发者快速定位延迟瓶颈、异常错误和成本热点。该能力默认启用，无需额外配置即可采集基础指标。

## 支持的模型/功能

- 支持所有通过百炼 `app.run()` 或 `app.invoke()` 启动的模型应用（含 LLM、RAG、Agent 流程）
- 内置覆盖以下可观测维度：  
  - 请求成功率、P95/P99 延迟、[Token](../concepts/token.md) 消耗量、缓存命中率  
  - 模型调用层级拆分（如 Router → LLM → Tool）  
  - 错误分类（网络超时、模型拒绝、Schema 校验失败等）  
- 支持自定义事件打点（`app.log_event()`），详见 [应用观测](../../raw/application-user-guide/application-monitoring.md)

## 关键参数

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `enable_monitoring` | bool | `true` | 全局开关；设为 `false` 将禁用所有埋点（包括日志与指标） |
| `sampling_rate` | float (0.0–1.0) | `1.0` | 采样率，适用于高吞吐场景降噪；低于 `0.1` 时部分低频错误可能丢失 |
| `trace_header` | string | `"x-bailian-trace-id"` | 用于透传与外部系统（如 SkyWalking）关联的 Trace ID 头字段 |

> **注意**：`sampling_rate` 在 [应用观测](../../raw/application-user-guide/application-monitoring.md) 中被描述为“仅影响 trace 上报”，但实际也控制指标聚合精度；建议生产环境保持 ≥0.5 以保障错误统计完整性。

## 使用方式

1. 确保应用已部署并启用监控（默认开启）  
2. 访问控制台「应用管理 → 应用详情 → 监控」页查看实时仪表盘  
3. 通过 OpenAPI 查询历史数据：  
   ```bash
   curl -X GET "https://dashscope.aliyuncs.com/api/v1/applications/{app_id}/metrics?start=1717027200&end=1717113600" \
        -H "Authorization: Bearer $DASHSCOPE_API_KEY"
   ```
4. 集成自定义事件（需 SDK v2.12.0+）：  
   ```python
   app.log_event("user_action", {"action": "click_submit", "step": "final"})
   ```
   事件将出现在「Trace 列表」中，并参与延迟归因分析，具体用法见 [应用观测](../../raw/application-user-guide/application-monitoring.md)

## 限制和注意事项

- 最大保留原始 trace 数据 7 天，聚合指标保留 90 天  
- 单次 trace 跨度超过 30 秒将被截断（不触发告警，但影响 P99 统计）  
- 不支持跨 workspace 的 trace 关联；若应用调用其他 workspace 的 API，链路将在边界中断  
- 自定义事件字段数上限为 20 个，总 JSON 大小 ≤ 4KB  
- 当前不支持对流式响应（`stream=True`）的逐 chunk 延迟打点，仅记录整体完成时间 —— 此行为与 [应用观测](../../raw/application-user-guide/application-monitoring.md) 文档一致，但已在内部需求池中标记为待优化项

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring.md)


