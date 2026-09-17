# model monitoring

百炼平台的 model monitoring 是面向生产环境的模型可观测性能力，提供分钟级延迟的调用统计、性能指标、审计日志及告警配置，帮助开发者实时掌握模型健康度、排查异常并控制成本。监控数据按业务空间隔离，不作为计费依据；用量统计与费用对账请以[费用中心账单](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)为准。核心能力覆盖用量观测、性能诊断、失败归因与主动告警，需结合[模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)与[监控告警 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md)两套机制协同使用。

## 支持的模型/功能

- **支持范围**：所有在百炼模型列表中可调用的模型（含[调优后的模型](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)）均支持用量查看与基础监控；但**语音、图片、视频生成及三方直连等部分模型不支持完整监控告警功能**，具体以控制台实际展示为准。
- **核心功能模块**：
  - **用量统计**：按模型 Code、API-Key、时间粒度（分钟/小时/天）聚合 [Token](../concepts/token.md)、图像张数、视频秒数等维度，支持 TOP10 模型排行与详情下钻（详见[模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）。
  - **实时监控**：调用后分钟级可见调用次数、失败率、首 [Token](../concepts/token.md) 延时、调用时长等 14 项指标，支持图表化趋势分析与跨模型对比。
  - **日志能力**：默认开启审计日志（含 Request ID、状态码、[Token](../concepts/token.md) 用量、延时，不含 Prompt/Response）；推理日志需手动开启并投递至 SLS，用于完整复现请求上下文。
  - **告警体系**：基于预置/自定义模板为关键指标（如失败率、TotalToken 数、429 次数）配置阈值告警，支持通知渠道、重复策略与时段控制。

> **注意**：文档 1 中“免费额度用完即停”功能描述为「开启后服务自动停止（返回 403）」，而文档 2 的监控告警场景聚焦于运行时异常（如 429、5xx），二者无直接关联；但实践中需注意：该开关关闭后若未配置告警，可能因用量突增导致意外扣费——建议始终为 `模型消耗 TotalToken 数` 配置环比突增告警（见[监控告警 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。

## 关键参数

| 参数 | 说明 | 是否支持告警 | 来源 |
|------|------|--------------|------|
| `调用次数` / `失败次数` / `失败率` | 基础可用性指标，失败率 = 失败次数 / 总调用次数 | ✅ | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `首 Token 延时` | 请求发出到首个 Token 返回的耗时，反映模型冷启与首包性能 | ✅ | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `调用时长` | 端到端总耗时（含网络+排队+生成） | ✅ | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `模型消耗 TotalToken 数` | 按模型维度统计的 Token 消耗总量，用于成本监控 | ✅ | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `限流错误次数`（429） | 触发配额限制的次数，直接关联 API-Key 或模型级 QPS 限制 | ✅ | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `平均单次请求Token量` | 用量概览页指标，用于评估 Prompt 效率 | ❌ | [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) |
| `非首 Token 延时` | 后续 Token 生成速度，反映模型吞吐能力 | ❌ | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |

## 使用方式

1. **访问入口**：
   - 用量统计：[模型用量页面](https://bailian.console.aliyun.com/cn-beijing/costing-balance/usage-statistics)
   - 监控与告警：[模型监控页面](https://bailian.console.aliyun.com/cn-beijing/model/telemetry) → 运维管理 > 模型监控
   - 告警规则管理：[模型告警页面](https://bailian.console.aliyun.com/cn-beijing/model/alert)

2. **快速上手**：
   - 在监控概览页筛选目标**业务空间**、**时间范围**、**API-Key**，查看整体调用规模与健康度卡片；
   - 在模型列表点击「查看详情」进入单模型监控详情页，通过告警铃铛图标为支持指标（如失败率、TotalToken 数）一键配置告警；
   - 在日志页签切换「审计日志」或「推理日志」，通过 Request ID 或状态码（如 `429`）快速定位失败请求；
   - 使用预置告警模板（如「模型调用失败占比1分钟总和大于1%」）降低配置门槛。

3. **高级配置**：
   - 开启**监控数据投递**至云监控 Prometheus 实例，实现与自有监控体系对接（需先授权云监控服务角色）；
   - 开启**日志投递**至 SLS 日志库以持久化审计/推理日志（推理日志依赖审计日志投递已开启）；
   - 通过「告警历史」页签回溯已触发告警，结合「查看详情」侧边面板分析根因。

## 限制和注意事项

- **数据延迟与保留**：监控数据延迟约 **1 分钟**，用量统计延迟约 **1 小时**；审计日志最长查询 **30 天**，用量数据仅支持查看 **最近 30 天**，更早数据需通过[费用与成本页面](https://billing-cost.console.aliyun.com/finance/expense-report/expense-detail-by-instance)导出账单获取。
- **权限与隔离**：所有监控、用量、日志数据严格按**业务空间**维度隔离，无法跨空间或按阿里云主账号维度汇总（[如何解决](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）。
- **功能限制**：
  - 批量推理仅在「大语言模型」页签支持筛选，其他模型类型不区分推理类型；
  - 推理日志不支持所有模型，列表中显示「当前模型不支持」即不可用；
  - 告警仅支持预置模板所列指标（如内容安全错误次数、RPM 不支持告警）；
  - 阿里云 App **暂不支持**查看免费额度与模型用量（见[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）。
- **成本提示**：开启日志投递至 SLS 或监控投递至 Prometheus 会产生对应云产品费用；关闭投递后，**期间日志/指标将无法补录**，请谨慎操作。
- **计费一致性**：监控数据**不作为计费依据**，用量统计口径（如 Token 计算）以[模型用量统计单位说明](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)为准，最终费用以账单明细为准。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


