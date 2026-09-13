# model monitoring

model monitoring 是百炼平台提供的模型调用行为与性能指标观测能力，用于追踪请求量、延迟、错误率等核心运行时数据，支撑稳定性分析与容量规划。该功能默认启用，无需额外开通，但需确保调用方已正确配置 `X-Bailian-Trace-ID` 等上下文头以保障链路归因准确性。监控数据延迟通常为 1–3 分钟，聚合粒度为 1 分钟。

## 支持的模型/功能

- 支持所有在百炼控制台**已部署并启用 API 访问**的模型（包括自定义微调模型、第三方托管模型及百炼原生模型），但不支持仅用于工作流内部调用、未暴露独立 endpoint 的子模型实例。  
- 提供两类核心监控能力：**用量统计**（如 QPS、总请求数、[Token](../concepts/token.md) 消耗）和**性能监控**（如 P95 延迟、HTTP 错误码分布、模型内部错误率）。  
- 告警能力依赖 [监控告警](https://help.aliyun.com/zh/model-studio/model-telemetry) 配置，需在 Model Studio 控制台单独设置阈值与通知渠道，详见 [原文标题](../../raw/model-user-guide/model-monitoring.md)。

## 关键参数

- `model_id`：必填，监控数据按此 ID 聚合，须与调用时 `model` 字段完全一致（区分大小写与版本后缀，如 `qwen-max:20240601`）。  
- `region`：影响数据归属，默认取调用 endpoint 所属地域；跨 region 调用将导致监控数据分散，建议统一使用 `cn-beijing` 或 `cn-hangzhou` 等主流 region endpoint。  
- `trace_id`（即 `X-Bailian-Trace-ID`）：非必填但强烈推荐，缺失时部分延迟与错误归因会降级为“未知链路”，影响根因分析。该字段格式要求与 [原文标题](../../raw/model-user-guide/model-monitoring.md) 中“链路追踪”章节一致。

## 使用方式

1. **查看监控看板**：登录百炼控制台 → 进入「Model Studio」→ 选择目标模型 → 「监控」页签，可切换时间范围（1h/24h/7d）与指标维度（全局/按 API Key/按来源 IP）。  
2. **查询原始指标**：通过 OpenAPI `DescribeModelMonitoringData` 获取分钟级聚合数据，需传入 `StartTime`、`EndTime` 和 `MetricName`（如 `RequestCount`, `P95LatencyMs`）。  
3. **配置告警**：在 Model Studio 的模型监控页点击「创建告警规则」，支持基于 `ErrorRate > 5%` 或 `P99LatencyMs > 10000` 等条件触发，配置入口与逻辑说明见 [原文标题](../../raw/model-user-guide/model-monitoring.md)。

## 限制和注意事项

- 单模型监控数据保留周期为 **30 天**，超期后不可查；历史数据导出需调用 `ExportMonitoringData` 接口并指定 `Format=CSV`。  
- [Token](../concepts/token.md) 统计仅覆盖 `input_tokens` 与 `output_tokens` 字段，**不包含系统提示词（system [prompt](prompt.md)）隐式消耗的 tokens**，该行为与部分竞品平台不同，需注意成本估算偏差。  
- > **注意**：原始文档中“[模型用量](https://help.aliyun.com/zh/model-studio/model-usage-statistics)”链接指向的页面当前（2024Q3）已下线，实际用量数据仅可通过控制台监控页或 OpenAPI 获取，旧文档未同步更新，以 [原文标题](../../raw/model-user-guide/model-monitoring.md) 中的当前链接为准。

## 来源文档

- [用量统计与性能监控](../../raw/model-user-guide/model-monitoring.md)


