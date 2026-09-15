# application monitoring

应用观测（Application Monitoring）是百炼平台为开发者提供的运行时可观测能力，用于实时跟踪大模型应用的调用链路、性能指标与错误分布。它支持对 API 调用、模型推理、工具调用等关键环节进行细粒度埋点与聚合分析，帮助快速定位延迟瓶颈与异常根因。该能力默认启用，无需额外部署探针。

## 支持的模型/功能

- 支持所有通过 `app.run()` 或 `app.async_run()` 启动的百炼应用实例（含 Stream 模式）
- 覆盖模型调用（Qwen 系列、GLM 系列等）、RAG 检索、Function Calling、自定义工具执行等全链路节点
- 提供预置看板：调用量趋势、P95 延迟热力图、错误率分桶、[Token](../concepts/token.md) 消耗统计  
- 支持按 `app_id`、`trace_id`、`session_id`、`user_id` 多维下钻查询  
- 详细能力说明见 [应用观测](../../raw/application-user-guide/application-monitoring.md)

## 关键参数

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `enable_monitoring` | bool | `true` | 全局开关；设为 `false` 将禁用所有埋点（包括日志与指标上报） |
| `sampling_rate` | float (0.0–1.0) | `1.0` | 全链路采样率；生产环境建议设为 `0.1`～`0.3` 以降低开销 |
| `max_span_depth` | int | `5` | 最大嵌套跨度深度；超过此值的子 Span 将被截断（避免递归过深导致内存溢出） |

> **注意**：`max_span_depth` 的默认值在 [用量监控与性能分析](../../raw/application-user-guide/application-monitoring/application-observation.md) 中被误标为 `10`，实际生效值以本页及 SDK 运行时为准（v2.12.0+）。

## 使用方式

1. 确保应用已接入百炼 SDK（≥ v2.11.0），并在初始化 `App` 时显式配置：
   ```python
   app = App(
       app_id="xxx",
       enable_monitoring=True,
       sampling_rate=0.2
   )
   ```
2. 所有 `app.run()` 调用将自动注入 trace 上下文；若需手动关联外部请求，可传入 `trace_id` 和 `span_id`：
   ```python
   app.run(input="...", trace_id="trc_abc123", span_id="spn_def456")
   ```
3. 查看数据：登录百炼控制台 → 应用详情页 → 「观测分析」标签页；或通过 [用量监控与性能分析](../../raw/application-user-guide/application-monitoring/application-observation.md) 文档中的 CLI 工具导出原始 trace 数据。

## 限制和注意事项

- Trace 数据保留周期为 7 天（不可配置），超出后自动清理  
- 单次请求中 Span 总数超过 1000 个时，后续 Span 将被丢弃（不报错）  
- 不支持跨进程/跨服务的分布式链路透传（如调用非百炼托管的微服务）；仅限百炼应用内部调用链  
- 若应用使用 `fork()` 创建子进程（如某些 Gunicorn 配置），子进程中监控将失效——请改用 `spawn` 启动方式，详见 [应用观测](../../raw/application-user-guide/application-monitoring.md) 的「多进程适配」章节

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring.md)


