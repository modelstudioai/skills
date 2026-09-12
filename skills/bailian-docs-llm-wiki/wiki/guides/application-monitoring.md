# application monitoring

应用观测（Application Monitoring）是百炼平台提供的运行时可观测能力，用于实时追踪大模型应用的调用链路、性能指标与资源消耗。它支持对 API 调用、推理延迟、[Token](../concepts/token.md) 使用量、错误率等关键维度进行采集与可视化，帮助开发者快速定位瓶颈与异常。该能力默认集成于百炼控制台的应用管理模块，无需额外部署探针。

## 支持的模型/功能

- 支持所有通过百炼 SDK 或 REST API 部署的 **托管模型应用**（如 Qwen 系列、Qwen2-VL、Qwen3 等），包括流式与非流式响应场景  
- 提供以下核心观测能力：  
  - 全链路请求追踪（Trace ID 关联）  
  - 按应用/版本/环境粒度的 QPS、P95 延迟、成功率统计  
  - 输入/输出 [Token](../concepts/token.md) 数、总 [Token](../concepts/token.md) 成本（按模型计费规格折算）  
  - 错误分类（如 `model_timeout`、`rate_limit_exceeded`、`invalid_param`）  
- 不支持直接监控用户自建后端服务（如 Flask/FastAPI 封装层），需自行接入 OpenTelemetry 或通过 [用量监控与性能分析](https://help.aliyun.com/zh/model-studio/application-observation) 手动上报指标。该能力说明详见 [应用观测](../../raw/application-user-guide/application-monitoring.md)。

## 关键参数

| 参数名 | 类型 | 是否必需 | 说明 |
|--------|------|----------|------|
| `app_id` | string | 是 | 百炼控制台中应用的唯一标识，用于关联监控数据 |
| `trace_id` | string | 否 | 开发者可透传的追踪 ID，用于跨系统链路对齐；若未提供，平台自动注入 |
| `env` | string | 否 | 环境标签（如 `prod`/`staging`），影响监控分组与告警策略，默认为 `default` |

> **注意**：文档中曾提及 `enable_monitoring: true` 作为初始化参数，但该字段在 v3.2+ SDK 中已废弃，实际启用状态由控制台应用配置页统一控制——请以 [应用观测](../../raw/application-user-guide/application-monitoring.md) 中的最新配置流程为准。

## 使用方式

1. **控制台启用**：进入「应用管理」→ 选择目标应用 → 「监控设置」页开启「启用应用观测」开关（默认关闭）  
2. **SDK 调用（Python 示例）**：
   ```python
   from alibabacloud_bailian20231229 import models as bailian_models
   client = BailianClient(...)
   # trace_id 可选，用于链路透传
   response = client.chat_completions(
       app_id="app-xxx",
       messages=[{"role": "user", "content": "你好"}],
       trace_id="trace-abc123"
   )
   ```
3. **查看数据**：在控制台「应用详情」→ 「监控」页查看实时图表，或导出近 7 天原始指标（CSV）。历史数据保留周期为 30 天，更长期存储需对接 SLS —— 具体操作参见 [用量监控与性能分析](https://help.aliyun.com/zh/model-studio/application-observation) 文档，其内容与 [应用观测](../../raw/application-user-guide/application-monitoring.md) 保持同步。

## 限制和注意事项

- 单应用每秒最大采样 1000 条请求（超出部分丢弃），高吞吐场景建议结合 `env` 标签做流量分层  
- Token 统计基于模型返回的 `usage` 字段，若使用 `stream=True` 且未完整消费流，则可能漏计输出 Token  
- 监控数据存在最多 60 秒延迟，不适用于亚秒级故障诊断  
- 自定义 HTTP Header（如 `X-Bailian-Trace-ID`）可替代 SDK 的 `trace_id` 参数，但需确保格式符合 W3C Trace Context 规范 —— 此细节在 [应用观测](../../raw/application-user-guide/application-monitoring.md) 中未明确说明，建议参考阿里云 SLS 分布式追踪文档验证兼容性

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring.md)


