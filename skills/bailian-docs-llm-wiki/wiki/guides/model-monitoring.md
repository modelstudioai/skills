# model monitoring

百炼平台提供面向模型调用全链路的可观测能力，覆盖分钟级监控指标、审计日志、推理日志及告警配置，帮助开发者实时掌握模型健康度、性能表现与用量趋势。监控数据按业务空间隔离，仅对当前选中空间生效；所有监控数据均不作为计费依据，对账请以费用中心账单为准。核心能力已在控制台「运维管理 > 模型监控」统一入口提供，详细操作与限制参见[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

## 支持的模型/功能

- **支持监控的模型**：所有在模型列表中可见的模型（含调优后模型）均支持基础监控指标（如调用次数、失败率、首 Token 延时等），但语音、图片、视频生成及三方直连类模型部分不支持，具体以控制台实际展示为准（详见[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)说明）。
- **核心功能模块**：
  - **监控概览与详情**：查看整体调用规模、健康度卡片及单模型多维度图表；
  - **审计日志**：默认开启，记录 Request ID、状态码、Token 用量、延迟等元信息，不含 Prompt/Response；
  - **推理日志**：需手动开启并完成日志投递配置，记录完整 Prompt/Response（截断上限 128K）及中间步骤；
  - **告警管理**：支持基于预置或自定义模板为指定指标配置规则，触发后通过邮件等渠道通知；
  - **数据投递**：可将监控指标投递至云监控 Prometheus 实例，日志投递至 SLS 日志库（推理日志依赖此配置）。

> **注意**：文档 2 中提到“模型用量数据延迟约为 1 小时”，而文档 1 明确说明“调用发生后分钟级之后即可在监控图表查看”。二者描述对象不同——前者指[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)页面的汇总统计（用于成本分析），后者指模型监控详情页的实时性能指标（用于运维响应）。两者不可混用，排查线上问题应以监控详情页的分钟级指标为准。

## 关键参数

| 参数 | 说明 | 是否支持告警 | 来源依据 |
|------|------|--------------|----------|
| `调用次数` / `失败次数` / `失败率` | 基础可用性指标，失败率 = 失败次数 / 总次数 | ✅ 支持 | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)指标表 |
| `调用时长` / `首 Token 延时` | 核心性能指标，首 Token 延时即首包时长 | ✅ 支持 | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)指标表 |
| `模型消耗 TotalToken 数` | 预置告警模板专用指标，按模型维度统计 Token 消耗总量 | ✅ 支持 | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)指标表 |
| `非首 Token 延时` / `RPM` / `TPM` / `内容安全错误次数` | 辅助诊断指标，不纳入预置告警模板 | ❌ 不支持 | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)指标表说明 |
| `平均单次请求调用量` | 用量分析指标，用于成本优化，不参与告警 | ❌ 不支持 | [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)表格列说明 |

## 使用方式

1. **访问入口**：登录百炼控制台 → 左侧导航栏「运维管理」→ 「模型监控」进入概览页；或直接访问 [https://bailian.console.aliyun.com/cn-beijing/model/telemetry](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)。
2. **快速配置告警**：
   - 在模型监控详情页，点击任一支持告警的指标图表上的蓝色/红色告警铃铛图标，打开配置侧边面板；
   - 或前往独立告警页面 [https://bailian.console.aliyun.com/cn-beijing/model/alert](https://bailian.console.aliyun.com/cn-beijing/model/alert)，在「告警规则」页签创建完整规则；
   - **前提**：必须先完成[数据投递](../../raw/model-user-guide/model-monitoring/model-telemetry.md)中「监控数据投递」的云监控服务角色授权（否则创建按钮置灰）。
3. **开启推理日志**：
   - 先确保已开启审计日志投递；
   - 在日志页面切换至「推理日志」页签，点击「开始配置」完成 SLS 授权与日志库选择；
   - 配置后，日志将自动写入指定 SLS 日志库，可用于调试与回流训练（详见[日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)）。
4. **用量联动分析**：模型监控详情页指标可与[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)页面数据交叉验证——前者侧重实时性能，后者侧重小时级用量汇总与成本归因。

## 限制和注意事项

- **模型兼容性限制**：语音、图片、视频生成及三方直连模型不支持监控与告警，控制台对应模型行不显示「查看详情」入口（[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)明确说明）。
- **数据时效性差异**：
  - 监控指标：分钟级延迟，适用于实时运维；
  - 模型用量统计：约 1 小时延迟，且不支持查询 30 天以前数据（[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)明确说明）；
  - 审计日志：支持查询最近 30 天，但推理日志依赖 SLS 配置，其保留策略由用户自行设置。
- **投递依赖关系**：
  - 开启推理日志**必须先开启审计日志投递**；关闭审计日志投递将**自动关闭推理日志投递**；
  - 关闭日志投递后，关闭期间产生的日志**无法补录复原**，请谨慎操作（[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)警告）。
- **告警能力边界**：
  - 仅预置告警模板所含指标（如失败率、首 Token 延时、TotalToken 数）支持配置告警，`RPM`、`TPM`、`非首 Token 延时`等指标图表无告警铃铛；
  - 告警检查周期最小为 60 秒（即 `告警检查周期=0` 表示“触发即告警”，但实际仍受数据采集频率约束）。
- **权限与计费**：监控数据在平台侧存储免费；但开启数据投递将自动开通云监控、SLS 及 Prometheus 服务，相关资源按实际用量计费（[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)说明）。

## 来源文档

- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)
- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)


