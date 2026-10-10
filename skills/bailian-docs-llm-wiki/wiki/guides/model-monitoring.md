# model monitoring

百炼平台的 model monitoring 是面向开发者的一套模型调用可观测性能力，涵盖用量统计、实时性能监控、失败诊断、告警配置与日志审计五大核心场景。所有数据按业务空间隔离，分钟级延迟，不作为计费依据（计费以账单为准）。监控能力与用量统计功能协同使用，是生产环境成本控制与稳定性保障的基础支撑。

## 支持的模型/功能

- **支持范围**：所有在[模型列表](raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)中可调用的模型（含调优后模型）均支持用量查看与基础监控；但语音、图片、视频生成及三方直连等部分模型**不支持监控告警功能**，具体需以控制台实际展示为准 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
- **核心功能模块**：
  - **用量统计**：按模型 Code、API-Key、时间粒度（分钟/小时/天）聚合 [Token](../concepts/token.md)、张数、秒数等计费单位，支持 Top10 模型排序与详情下钻 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。
  - **实时监控**：提供调用次数、失败率、首 [Token](../concepts/token.md) 延时、调用时长、限流错误次数等 15+ 指标图表，支持跨模型对比与趋势分析。
  - **告警管理**：基于预置或自定义模板为关键指标（如失败率 >1%、Total[Token](../concepts/token.md) 数突增）配置阈值告警，支持通知到联系人组 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
  - **日志审计**：默认开启审计日志（含 Request ID、状态码、Token 用量、延时），推理日志需手动开启并投递至 SLS，用于完整 Prompt/Response 复现与调试。

> **注意**：文档 1 中称“所有模型均支持查看用量”，而文档 2 明确指出“语音、图片、视频生成及三方直连等部分模型不支持监控告警”。二者无矛盾——用量统计（文档 1）与监控告警（文档 2）是两个独立能力集，前者覆盖更广，后者有模型兼容性限制。开发者需根据目标模型在控制台实际界面确认告警可用性。

## 关键参数

| 参数 | 说明 | 是否必填 | 来源 |
|------|------|----------|------|
| `时间范围` | 支持最近 30 天内查询，超期数据需通过费用中心账单获取 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) | 是 | 控制台筛选栏 |
| `推理类型` | 仅「大语言模型」页签支持筛选「实时推理」或「批量推理」；其他模型类型固定为实时推理 | 否 | [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) |
| `API-Key` | 用于按密钥维度归因用量与监控数据，仅显示当前业务空间下已创建的 Key | 否 | 两文档均支持 |
| `告警检查周期` | 最小单位为秒，0 表示触发即告警；默认 60 秒 | 是 | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `持续时间` | 告警触发需连续满足阈值的分钟数，例如“失败率 >1% 持续 5 分钟” | 是 | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `统计周期（模板）` | 预置模板中指标计算的时间窗口，合法范围 1–10080 分钟（即 1 周） | 是 | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |

## 使用方式

1. **用量查看**  
   访问 [模型用量](https://bailian.console.aliyun.com/cn-beijing/costing-balance/usage-statistics)，选择模型类型页签（如「大语言模型」）、时间范围与精度（分钟/小时/天），输入模型名称搜索或筛选 API-Key。概览页四张卡片（调用模型数、成功总次数、Token 总量等）支持本周期/上周期对比。

2. **监控与告警配置**  
   进入 [模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry) → 在模型列表点击「查看详情」进入详情页 → 对支持告警的指标（如失败率、TotalToken 数）点击图表旁的蓝色铃铛图标 → 选择预置模板或自定义规则 → 配置通知对象与时段 → 创建。  
   **前置依赖**：首次创建告警前，须在「监控数据投递」中授权云监控服务角色（自动开通云监控、SLS、Prometheus）[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

3. **日志排查**  
   - 审计日志：默认开启，在监控概览页点击模型行「查看日志」即可访问，支持按 Request ID、状态码（200/4XX/5XX）筛选。  
   - 推理日志：需先完成日志投递配置（授权 SLS 角色 + 创建日志库），再于日志页签开启；仅北京、新加坡地域支持 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

## 限制和注意事项

- **数据延迟与保留**：用量统计延迟约 1 小时；审计日志最长可查 30 天；告警历史仅保留 2026 年 9 月 3 日后记录，此前数据需查云监控控制台 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
- **地域与功能限制**：推理日志投递仅支持北京、新加坡地域；监控数据投递仅支持云监控 Prometheus 实例，不支持自建 Prometheus [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
- **计费与用量分离**：监控数据**不作为计费依据**，仅作参考；真实用量与费用请以[费用中心账单](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)为准 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。
- **免费额度联动**：「免费额度用完即停」开关开启后，额度耗尽将返回 `403 AllocationQuota.FreeTierOnly` 错误；该功能仅在仍有未消耗额度时可开启，关闭需待额度完全耗尽后操作 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。
- **权限与隔离**：所有监控、用量、日志数据严格按**业务空间**维度隔离，不支持跨空间或按阿里云主账号汇总 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


