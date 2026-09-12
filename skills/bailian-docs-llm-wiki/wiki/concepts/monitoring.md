# 监控与可观测性

监控与可观测性是百炼平台统一提供的运行时洞察能力，用于持续采集、聚合和分析模型服务及应用的调用行为、性能表现与稳定性状态；它不依赖用户手动埋点，开箱即用，是保障服务可靠性、加速问题定位与支撑数据驱动优化的核心基础设施。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台中，“监控与可观测性”并非单一功能模块，而是贯穿模型服务、工作流节点、API 网关和应用层的横切能力，按使用粒度与目标分为两类：

- **模型级监控（Model Monitoring）**：面向已部署的模型服务（含 API 模型、自定义模型、微调模型），自动采集用量（QPS、总请求数、[Token](token.md) 消耗）、性能（P50/P90/P99 延迟、首 [Token](token.md) 时间）和稳定性（HTTP 4xx/5xx 错误率、模型内部错误码）。适用于模型 SLO 验证、容量规划与版本对比。  
  ✅ 支持所有控制台部署的模型服务  
  ✅ 工作流节点需显式开启「启用可观测性」开关才采集节点级指标  

- **应用级可观测性（Application Monitoring & Evaluation）**：面向完整应用链路（如 RAG 应用、多步工作流、集成 SDK 的业务系统），提供调用链路追踪、多维下钻（`model_id`/`app_id`/`status_code`）、实时日志采样（1% 默认）及错误上下文追溯。同时，评测类能力（模型评测、应用评测）延伸了可观测性的深度——将“运行时表现”与“业务效果”对齐，例如通过评测任务量化延迟上升是否导致准确率下降。  
  ✅ 默认启用，覆盖所有通过百炼 API 网关发布的生产服务  
  ✅ 评测任务本身也依赖可观测性数据（如 `latency_ms`、`error_rate_5xx`）作为输入指标或归因依据  

> ⚠️ 注意：`debug` 环境、本地调试模式（`--local-mode`）不纳入可观测范围；指标数据默认保留 30 天（聚合指标保留 90 天）。

## 关键参数和配置

| 场景 | 参数名 | 类型 | 必填 | 说明 | 典型值示例 |
|------|--------|------|------|------|-------------|
| **通用查询** | `model_id` / `app_id` | string | 是（按场景） | 指标归属标识，用于聚合与告警绑定 | `"qwen-max-20240601"`, `"app-abc123"` |
| | `time_range` 或 `start_time`/`end_time` | string (ISO8601) | 是（API 查询） | 时间窗口，最大单次跨度为 7 天（应用监控）或默认 `last_1h`（模型监控） | `"last_24h"`, `"2024-06-01T00:00:00Z"` |
| | `granularity` | string | 否 | 采样粒度，影响图表精度与查询性能 | `"1m"`, `"5m"`, `"1h"` |
| **多维分析** | `group_by` | string[] | 否 | 最多支持 2 个维度下钻 | `["model_id", "status_code"]` |
| | `metrics` | string[] | 否 | 指定返回指标，减少响应体积 | `["qps", "latency_p95", "error_rate_5xx"]` |
| **评测联动** | `timeout` / `timeout_ms` | integer | 否（但强建议） | 控制单样本等待上限，避免阻塞评测流程 | `30000`（毫秒） |
| | `concurrency` | integer | 否 | 并发请求数，影响可观测数据采集密度与评测压力 | `10`（免费版上限 5） |

> ✅ 所有监控 API 均需携带 `Authorization: Bearer <API_KEY>`，且调用方需具备 `dashscope:MonitorRead` 权限。  
> ❌ `region` 不再支持作为 `group_by` 维度（v2.3.0+ 已移除）；`workflow_node_id` 已统一为 `node_id`（v3.2.0+）。

## 面向开发者：快速上手建议

- **第一步：看一眼** → 进入控制台「模型服务」→ 选模型 → 「监控」页签，10 秒内掌握当前健康水位；  
- **第二步：查异常** → 用 `GET /v1/monitoring/metrics` 拉取最近 1 小时 `error_rate_5xx` + `latency_p99`，结合 `group_by=["status_code"]` 定位错误类型；  
- **第三步：设告警** → 在「告警管理」中新建规则，条件示例：`error_rate_5xx > 0.03 AND qps > 10`，通知方式选钉钉/邮件；  
- **第四步：连评测** → 在创建模型/应用评测任务时，勾选 `latency_ms`、`error_rate_5xx` 等可观测指标，让效果评估自带“上下文”；  
- **避坑提示**：[Token](token.md) 消耗仅对 LLM 类模型生效；多版本模型（`qwen-max-v1`/`v2`）共享同一监控流，如需隔离请使用不同 `model_id` 命名。

> 提示：所有监控数据均经脱敏处理，不包含原始请求/响应内容（日志采样除外，且仅含错误上下文片段）。如需深度诊断，请结合应用评测的人工标注或导出原始指标做归因分析。

## 关联主题页

- [model monitoring](../guides/model-monitoring.md)
- [application monitoring](../guides/application-monitoring.md)
- [model evaluation introduction](../guides/model-evaluation-introduction.md)
- [application evaluation](../guides/application-evaluation.md)


