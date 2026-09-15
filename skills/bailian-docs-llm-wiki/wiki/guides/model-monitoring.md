# model monitoring

百炼平台的 model monitoring 是面向开发者的一套可观测性能力，覆盖模型调用统计、性能指标监控、异常告警及审计/推理日志全链路。数据按业务空间隔离，分钟级延迟，支持实时排查与成本治理。核心能力分为用量统计（计费依据）和监控告警（运维依据）两类，二者指标口径一致但用途不同：前者用于对账与预算管理，后者用于 SLO 保障与故障响应。

## 支持的模型/功能

- **支持范围**：所有在[模型列表](raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)中可调用的模型（含调优后模型）均支持用量统计与基础监控；但语音、图片、视频生成及三方直连等部分模型**不支持监控告警**，具体以控制台实际展示为准 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
- **核心功能模块**：
  - **用量统计**：按模型 Code、API-Key、时间维度聚合 Token/张/秒等计量单位，支持分钟级精度（≤1天）、小时级（≤7天）、天级（≤30天）查看，数据延迟约 1 小时 [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。
  - **监控告警**：提供调用次数、失败率、首 Token 延时、调用时长、限流错误次数等 14 项核心指标的实时图表与阈值告警，支持按推理类型（实时/批量）和 API-Key 筛选 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
  - **日志能力**：默认开启审计日志（含 Request ID、状态码、Token 用量、延时等，不含 Prompt/Response）；推理日志需手动开启并配置日志投递，记录完整 Prompt/Response（上限 128KB）[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

> **注意**：文档 1 中“免费额度用完即停”功能说明提到“控制台免费额度数据分钟级更新”，而文档 2 中明确指出“监控数据按业务空间隔离，仅可查看当前选中业务空间的数据”，二者未冲突但需注意：免费额度是账户级资源配额，而监控数据是空间级运行时指标，不可跨空间聚合。

## 关键参数

| 参数 | 说明 | 取值范围/约束 | 来源 |
|------|------|----------------|------|
| `time_range` | 时间筛选范围 | 最大支持 30 天；超过 30 天需通过[费用与成本](https://billing-cost.console.aliyun.com/finance/expense-report/expense-detail-by-instance)查询 | [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) |
| `time_granularity` | 时间精度 | 分钟（≤1天）、小时（≤7天）、天（≤30天）；精度不可跨档混用 | [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) |
| `api_key_id` | API-Key 筛选 | 仅展示当前业务空间下已创建且未删除的 API-Key；删除后日志中仅保留 ID | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `alert_check_period` | 告警检查周期 | 必填，单位为秒；最小值为 0（触发即告警），默认 60 秒 | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `alert_duration` | 告警持续时间 | 必填，单位为分钟；用于定义连续多少分钟满足阈值才触发告警 | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |

## 使用方式

1. **访问入口**：
   - 用量统计：[模型用量](https://bailian.console.aliyun.com/cn-beijing/costing-balance/usage-statistics) 页面（按模型类型页签切换）
   - 监控告警：[模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry) 页面（左侧导航栏「运维管理 > 模型监控」）
   - 告警规则：[模型告警](https://bailian.console.aliyun.com/cn-beijing/model/alert) 页面
   - 日志：模型监控详情页 → 「查看日志」或概览页模型列表操作列

2. **快速配置告警**：
   - 在模型监控详情页任一支持告警的指标图表上点击蓝色/灰色告警铃铛图标，直接打开该指标的告警规则配置侧边面板；
   - 或前往[模型告警页面](https://bailian.console.aliyun.com/cn-beijing/model/alert)，使用预置模板（如「模型调用失败占比1分钟总和大于1%」）一键创建；
   - **必须前置授权**：首次创建前需在「监控数据投递」中完成云监控服务角色授权，否则按钮禁用 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

3. **启用推理日志**：
   - 先确保「审计日志投递」已开启（需授权 SLS 角色、开通日志服务、创建日志库）；
   - 进入日志页面 → 切换至「推理日志」页签 → 点击「开始配置」完成投递设置；
   - 开启后日志将写入指定 SLS 日志库，可用于调试与日志回流 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

## 限制和注意事项

- **数据时效性**：用量统计延迟约 1 小时；监控图表数据延迟为分钟级；审计日志最长可查 30 天，推理日志依赖 SLS 配置的存储周期。
- **权限与隔离**：所有监控与用量数据严格按**业务空间**维度隔离，不支持跨空间或账号维度聚合；API-Key 筛选仅限当前空间内有效 Key。
- **告警能力限制**：
  - 仅表中明确标注「可配置告警」的指标（如失败率、调用时长、TotalToken 数）支持告警；非首 Token 延时、RPM、TPM 等**不支持告警** [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
  - 预置告警模板覆盖 12 类常见场景，自定义模板最多支持 10 个参数组合（AND/OR 逻辑）。
- **投递依赖与风险**：
  - 监控数据投递依赖云监控 Prometheus 实例，**不支持自建 Prometheus**；
  - 日志投递关闭后，期间日志**无法补录**；SLS 日志库被删除将导致投递永久失败 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
- **计费差异**：监控数据本身免费；但开启日志投递（SLS）或监控投递（Prometheus）将产生对应云产品费用；用量统计数据是计费唯一依据，监控图表**不作为对账凭证** [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


