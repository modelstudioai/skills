# model monitoring

model monitoring 是百炼平台面向开发者提供的核心可观测性能力，用于实时掌握模型调用的规模、健康度与性能表现。它覆盖调用统计、错误分析、延迟诊断、用量追踪及告警响应全链路，数据分钟级可见，按业务空间隔离，不作为计费依据（计费请以[费用中心](https://bailian.console.aliyun.com/cn-beijing/costing-balance/overview)为准）。监控能力与用量统计功能协同使用，可支撑成本优化、SLA 保障与故障快速定位。

## 支持的模型与功能

- **支持范围**：全部在模型列表中公开的模型（含基于其[调优后的模型](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)）均支持基础监控；但语音、图片、视频生成及三方直连等部分模型**不支持监控与告警**，具体需在控制台确认 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
- **核心功能模块**：
  - **调用统计**：调用次数、失败次数、失败率、限流错误次数（429）、内容安全拦截次数等；
  - **性能指标**：调用时长、首 Token 延时、非首 Token 延时、缓存命中量/率；
  - **用量指标**：Token 总量、模型消耗 TotalToken 数、平均单次请求调用量；
  - **日志能力**：默认开启审计日志（含 Request ID、状态码、用量、延迟等，不含 Prompt/Response）；推理日志需手动开启，记录完整 Prompt/Response 与中间步骤，**目前仅在北京和新加坡地域支持** [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)；
  - **告警体系**：支持为关键指标配置阈值告警，并提供预置模板（如“模型调用失败占比1分钟总和大于1%”）和自定义规则。

> **注意**：文档 1 中称“失败次数、失败率、限流错误次数和内容安全拦截次数已移至[模型监控](raw/model-user-guide/model-monitoring/model-telemetry.md)页面”，而文档 2 明确将这些指标列为监控详情页核心指标；二者一致，无矛盾。但文档 1 的[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)页面**仅展示调用次数、Tokens 用量等计费相关指标**，不包含失败率等健康度指标——该划分符合设计意图，非过时信息。

## 关键参数

| 参数名 | 说明 | 是否支持告警 | 来源 |
|--------|------|--------------|------|
| `调用次数` | 模型被调用的总次数 | ✅ | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `失败率` | 失败次数 / 总调用次数 | ✅ | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `首 Token 延时` | 请求发起到返回首个 Token 的耗时 | ✅ | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `调用时长` | 请求到完整响应的总耗时 | ✅ | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `限流错误次数`（429） | 触发速率限制的次数 | ✅ | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `模型消耗 TotalToken 数` | 按模型维度统计的 Token 消耗总量（预置告警模板专用） | ✅ | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `平均单次请求调用量` | 用量 / 成功调用次数 | ❌ | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `RPM` / `TPM` | 每分钟请求数 / Token 数 | ❌ | [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |

> **注意**：是否支持告警取决于是否被纳入预置告警模板；不在模板中的指标（如 RPM、内容安全错误次数）图表上不显示告警铃铛，无法直接配置 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

## 使用方式

1. **访问入口**：登录百炼控制台 → 左侧导航栏 **运维管理 > 模型监控**（[概览页](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)）。
2. **筛选数据**：支持按时间（快捷/自定义）、推理类型（在线/批量离线/批量在线）、API Key（仅当前业务空间下存在的 Key）筛选。
3. **查看详情**：
   - 在概览页模型列表点击 **查看详情** 进入单模型监控详情页（含图表与告警铃铛）；
   - 点击 **查看日志** 进入审计日志页签（默认开启）；推理日志需先开启[日志投递](../../raw/model-user-guide/model-monitoring/model-telemetry.md)并配置 SLS 日志库。
4. **配置告警**：
   - 在监控图表上点击告警铃铛，快速为当前模型+指标创建规则；
   - 或前往 [模型告警页面](https://bailian.console.aliyun.com/cn-beijing/model/alert) → **告警规则** 页签，创建跨模型规则；
   - **前提**：必须先完成[监控数据投递](../../raw/model-user-guide/model-monitoring/model-telemetry.md)中的云监控服务角色授权（否则创建按钮禁用）。
5. **用量联动**：监控数据用于健康诊断，用量数据用于成本对账；二者需结合使用——例如用监控发现失败率突增，再通过[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)页面下钻查看对应时段、模型、API Key 的明细，定位异常来源。

## 限制和注意事项

- **数据时效性**：监控数据分钟级可见；用量数据中，调用次数延迟约 1 分钟，Token/费用延迟约 10 分钟；更早于 2026 年 9 月的数据需通过[费用与成本](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)查询 [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。
- **地域与时间限制**：美国（弗吉尼亚）地域的用量数据仅支持查询 2026 年 10 月及之后；所有地域用量数据均从 2026 年 9 月起支持 [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。
- **权限与隔离**：监控与用量数据均按**业务空间**维度统计和展示，**不支持按阿里云账号维度聚合**；用户只能查看所选业务空间内的数据。
- **日志限制**：
  - 审计日志默认开启，最长可查 30 天；
  - 推理日志需手动开启且依赖日志投递，Prompt/Response 截断上限为 128K；
  - 推理日志**仅北京、新加坡地域支持**，其他地域暂不可用 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
- **告警依赖**：创建告警规则前，必须完成云监控服务角色授权；授权后将自动开通云监控、SLS 及 Prometheus 服务，相关产品按实际用量计费。
- **免费额度联动**：“免费额度用完即停”功能开启后，额度耗尽将返回 `403 AllocationQuota.FreeTierOnly` 错误；该功能**只能在仍有未消耗额度时开启**，关闭需待额度完全耗尽后操作 [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


