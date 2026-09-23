# model monitoring

百炼平台提供面向生产环境的模型调用可观测能力，覆盖分钟级监控指标、审计日志、推理日志及告警配置，帮助开发者实时掌握模型健康度、性能表现与用量趋势。监控数据按业务空间隔离，不作为计费依据；用量统计则独立提供小时级延迟的计费口径数据，二者互补构成完整的运维与成本治理视图。详细设计与限制请参见 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) 和 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

## 支持的模型/功能

- **监控覆盖范围**：所有在百炼模型列表中可调用的模型（含调优后模型）均支持基础监控指标（调用次数、失败率、调用时长、首 [Token](../concepts/token.md) 延时等），但语音、图片、视频生成及三方直连等部分模型**不支持监控与告警**，具体以控制台实际展示为准（见 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。
- **日志能力分层**：
  - **审计日志**：默认开启，记录 Request ID、时间、模型、[Token](../concepts/token.md) 用量、状态码、延迟等元信息，**不包含 Prompt/Response**。
  - **推理日志**：需手动开启，记录完整 Prompt/Response 及中间步骤（长度上限 128K），依赖日志投递至 SLS 日志库，仅对支持该能力的模型生效（不支持模型在日志页签提示“当前模型不支持”）。
- **用量统计**：所有模型均支持用量查看，但统计单位因模态而异（如大语言模型按 [Token](../concepts/token.md)、图像生成按“张”、语音合成按“秒”或“字符”），详见 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) 中的“模型用量统计单位说明”。

> **注意**：文档 1 称监控数据“分钟级之后即可查看”，而文档 2 明确用量统计“延迟约为 1 小时”。二者定位不同：前者指监控指标（用于运维响应），后者指用量数据（用于计费对账），不可混用。用量页面不提供监控级别的实时性。

## 关键参数

| 参数 | 说明 | 是否支持告警 | 来源 |
|------|------|--------------|------|
| `调用次数` / `失败次数` / `失败率` | 基础可用性指标，排查失败突增首选 | ✅ | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `调用时长` / `首 Token 延时` | 核心性能指标，用于识别响应退化 | ✅ | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `模型消耗 TotalToken 数` | 预置告警模板专用指标，用于成本突增监控 | ✅ | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `限流错误次数`（429） | 直接反映配额瓶颈，建议配置告警 | ✅ | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `非首 Token 延时` / `RPM` / `TPM` / `内容安全错误次数` | 不在预置告警模板中，图表无告警铃铛，**无法配置告警** | ❌ | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |

## 使用方式

1. **访问入口**：
   - 监控概览页：[百炼控制台 → 运维管理 → 模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)
   - 用量统计页：[百炼控制台 → 费用与成本 → 模型用量](https://bailian.console.aliyun.com/cn-beijing/costing-balance/usage-statistics)
   - 告警配置页：[百炼控制台 → 运维管理 → 模型告警](https://bailian.console.aliyun.com/cn-beijing/model/alert)

2. **快速配置告警**：
   - 在模型监控详情页，点击指标图表旁的蓝色/灰色告警铃铛，直接为该模型+该指标创建规则；
   - 或进入告警规则页，选择预置模板（如“模型调用失败占比1分钟总和大于1%”），填写模型、持续时间、通知对象后创建。

3. **开启日志投递（必需步骤）**：
   - 推理日志依赖日志投递：需先完成**日志服务角色授权** → **开通日志服务** → **创建 SLS 日志库**；
   - 审计日志投递为推理日志投递的前提，关闭前者将自动关闭后者（见 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。

4. **用量分析**：
   - 在用量页面按模型类型（大语言模型/视觉模型等）、时间范围（最长30天）、API-Key 筛选；
   - 支持分钟/小时/天三种时间精度（跨度 >1 天时分钟精度不可选）；
   - 点击单模型行进入“用量详情页”，查看细粒度趋势图。

## 限制和注意事项

- **数据隔离与延迟**：监控数据严格按业务空间隔离；监控指标延迟约 1–2 分钟，用量统计延迟约 1 小时，**二者不可互替用于计费核对**。
- **告警能力限制**：
  - 仅预置告警模板所列指标（共12项）支持配置告警，如 `RPM`、`TPM`、`内容安全错误次数` 等明确不支持（见 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) 表格说明）；
  - 创建告警规则前**必须完成云监控服务角色授权**，否则按钮置灰且悬停提示。
- **日志投递风险**：
  - 关闭日志投递后，**关闭期间产生的日志无法补录**；
  - SLS 日志库由百炼自动创建，**禁止手动删除**，否则导致投递失败；
  - SLS 侧不支持修改索引，修改将导致查询失败。
- **免费额度联动**：用量页面的“免费额度用完即停”开关开启后，额度耗尽将返回 `403 AllocationQuota.FreeTierOnly` 错误；该功能仅在仍有未消耗额度时可开启，关闭需待额度完全耗尽后操作（见 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）。

## 来源文档

- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)
- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)


