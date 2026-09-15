# 可观测性监控

可观测性监控是百炼平台统一的运行时洞察能力，通过采集、聚合、分析和可视化调用链路、性能指标与资源用量数据，帮助开发者快速定位问题、保障 SLO、优化成本与持续改进模型应用质量。它不是单一工具，而是贯穿模型服务、应用实例、评测任务等全生命周期的数据基础设施。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型服务层（Model Monitoring）**：面向底层模型调用，提供账户/业务空间粒度的用量统计（Token/张/秒）、核心性能指标（首 Token 延迟、失败率、限流次数）及审计日志。适用于计费对账、容量规划与模型级 SLO 治理；推理日志需显式开启，用于深度调试。
  
- **应用实例层（Application Monitoring）**：面向大模型应用（含智能体、工作流），自动注入 OpenTelemetry trace，提供端到端调用链追踪、细粒度延迟拆解（首 Token / 生成 Token / 模型加载）、GPU/vCPU 资源消耗及每分钟请求数（RPM）。默认启用，无需埋点，是应用性能分析与故障根因定位的核心依据。

- **应用评测场景（Application Evaluation）**：可观测性监控为评测提供真实线上数据源——支持将应用观测中采集的 trace 和指标数据一键导入生成评测集，使评测样本具备真实流量分布、BadCase 上下文与性能标签，显著提升评测结果的代表性和归因准确性。

- **成本治理层（Billing API）**：虽不直接提供监控能力，但可观测性监控输出的用量与性能数据（如 Token 消耗、调用频次、延迟分布）是账单明细与消费趋势分析的底层依据；`/billing/trend` 接口返回的按模型/项目分组的消费曲线，其原始数据即来源于模型与应用监控系统的聚合结果。

> ✅ 共同特点：所有场景均基于统一数据模型（OpenTelemetry 兼容 schema）、统一存储与保留策略（trace 7 天，指标 30 天），且严格按「业务空间」隔离，确保数据权限与合规边界清晰。

## 关键参数和配置

| 场景 | 参数名 | 类型 | 默认值 | 说明 |
|------|--------|------|--------|------|
| **应用监控** | `enabled` | boolean | `true` | 全局开关；设为 `false` 将停用 trace 采集与指标上报 |
| | `sample_rate` | float (0.0–1.0) | `0.1` | 生产环境强制上限 `0.2`；测试环境可设 `1.0`（需控制台白名单） |
| | `metrics_granularity` | string | `"1m"` | 支持 `"1m"`, `"5m"`, `"1h"`；影响指标图表刷新精度与查询延迟 |
| **模型监控** | `alert_check_period` | int (秒) | `60` | 告警规则检查频率；最小值 `0`（事件触发式） |
| | `alert_duration` | int (分钟) | `1` | 连续满足阈值的最短时长才触发告警，防抖必备 |
| | `time_granularity` | string | 动态 | 分钟（≤1天）、小时（≤7天）、天（≤30天）；由 `time_range` 自动推导，不可手动冲突设置 |
| **通用** | `include_input`（已弃用） | — | — | **禁止启用**：旧版 trace 中记录原始 [prompt](../guides/prompt.md)，存在隐私风险；新 SDK 已移除该字段 |

> ⚠️ 注意：`include_input` 已在 v2.3+ SDK 中彻底移除，任何尝试通过 YAML 或低版本 SDK 启用的行为均无效；审计日志默认不包含 [prompt](../guides/prompt.md)/response，仅推理日志（需手动开启并投递至 SLS）才记录完整输入输出。

## 面向开发者，简洁实用

- **快速上手**：控制台中「应用管理 → 监控」或「模型监控」页签即开即用，无需代码修改；首次使用前完成云监控角色授权即可创建告警。
- **调试优先**：开发阶段将 `sample_rate` 设为 `1.0`（测试环境），配合 `/v1/traces` API 或 SDK `list_traces()` 快速检索问题请求；上线后立即调回 `0.1`～`0.2`。
- **告警必配**：对关键应用，至少配置两项基础告警：① `失败率 > 1% in 1m`，② `P95 延迟 > 5s in 5m`；使用预置模板 30 秒完成。
- **评测联动**：在「应用监控」页点击「导出为评测集」，自动提取最近 24 小时高延迟/失败 trace，生成带上下文的 BadCase 样本，直连评测流程。
- **排查口诀**：  
  - 延迟高？→ 查 `first_token_latency` vs `total_latency`：若前者高，聚焦模型加载/前置处理；若后者高，聚焦生成逻辑或流式 chunk 处理；  
  - 错误多？→ 查 `status_code` 分布 + `error_type`（如 `rate_limit_exceeded`, `model_not_found`）；  
  - 成本异常？→ 对齐「模型监控」用量统计与「账单 API」消费明细，确认是否为某 API-Key 或某模型突增调用。

所有监控数据均经平台侧脱敏与权限过滤，开发者仅能访问所属业务空间内授权资源的数据。

## 关联主题页

- [application monitoring](../guides/application-monitoring.md)
- [model monitoring](../guides/model-monitoring.md)
- [application evaluation](../guides/application-evaluation.md)
- [billing api](../api/billing-api.md)


