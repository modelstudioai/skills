# model monitoring

model monitoring 是百炼平台提供的模型调用行为与性能指标观测能力，用于追踪请求量、延迟、错误率等核心运行时指标，支持基于阈值的告警配置。该功能面向已部署在百炼上的模型服务（包括 API 调用和工作流节点），无需额外埋点即可启用。详细背景与设计目标见 [用量统计与性能监控](../../raw/model-user-guide/model-monitoring.md)。

## 支持的模型/功能

- 支持所有通过百炼控制台部署的 **API 模型服务**（含自定义模型、百炼内置模型）及 **工作流中启用“可观测性”的节点**；
- 提供三大维度监控：**用量统计**（QPS、总请求数、[Token](../concepts/token.md) 消耗）、**性能指标**（P50/P90/P99 延迟、首 [Token](../concepts/token.md) 延迟）、**稳定性指标**（HTTP 4xx/5xx 错误率、模型内部错误 code）；
- 告警能力依赖阿里云 [监控告警](../../raw/model-user-guide/model-monitoring.md) 配置，支持按模型 ID、工作流 ID 或标签粒度设置阈值规则。

## 关键参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `model_id` | string | 必填，模型唯一标识（如 `qwen-max-20240601`），用于指标聚合与告警绑定 |
| `time_range` | string | 可选，时间范围（如 `last_1h`, `last_24h`），默认为 `last_1h`；注意该参数仅影响查询结果，不影响数据采集周期 |
| `granularity` | string | 可选，采样粒度（`1m`, `5m`, `1h`），最小支持 `1m`；详见 [用量统计与性能监控](../../raw/model-user-guide/model-monitoring.md) 中的指标采集说明 |

> **注意**：文档中提及的 `workflow_node_id` 在 v3.2.0+ 版本中已统一替换为 `node_id`，旧参数名将被弃用，请以控制台 API 文档为准。

## 使用方式

1. **控制台查看**：进入「模型服务」→ 选择目标模型 → 点击「监控」页签，可实时查看图表与原始指标；
2. **API 查询**：调用 `GET /api/v1/monitor/metrics`，传入 `model_id` 和可选参数（如 `time_range=last_24h&granularity=5m`）；
3. **告警配置**：在「告警管理」中新建规则，选择数据源为 `ModelStudio/Metric`，指标名称参考 [模型用量](../../raw/model-user-guide/model-monitoring.md) 所列标准指标集。

## 限制和注意事项

- 指标数据保留期为 **30 天**，超出后自动清理；
- 工作流节点监控需在创建工作流时显式开启「启用可观测性」开关，否则不采集节点级指标；
- [Token](../concepts/token.md) 统计仅对 LLM 类模型生效（如 Qwen 系列），非文本生成类模型（如 embedding、rerank）不提供 token 消耗指标；
- 同一 `model_id` 下多个版本（如 `qwen-max-v1`, `qwen-max-v2`）共享同一监控数据流，无法按版本拆分——此行为与 [用量统计与性能监控](../../raw/model-user-guide/model-monitoring.md) 描述一致，但与部分早期 SDK 示例存在出入，建议以控制台实际展示为准。

## 来源文档

- [用量统计与性能监控](../../raw/model-user-guide/model-monitoring.md)


