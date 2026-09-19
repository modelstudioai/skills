# model monitoring

模型监控是百炼平台提供的核心运维能力，用于实时观测模型调用状态、性能指标与异常行为。监控数据分钟级延迟，按业务空间隔离，支持图表化分析、告警配置与日志追溯。该功能不作为计费依据，对账请以费用中心账单为准 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

## 支持的模型与功能

- **支持范围**：所有在模型列表中可见的模型（含调优后模型）均支持基础监控与用量统计；但语音、图片、视频生成及三方直连等部分模型**不支持监控与告警**，具体以控制台实际展示为准 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
- **核心功能**：
  - **监控概览与详情**：查看整体调用规模（总次数、失败次数、平均调用时长、首 [Token](../concepts/token.md) 延时等）及单模型维度的调用统计与性能趋势。
  - **审计日志**：默认开启，记录 Request ID、时间、模型、[Token](../concepts/token.md) 用量、延迟、状态码等，**不含 Prompt/Response**。
  - **推理日志**：需手动开启并配置日志投递，记录完整 Prompt/Response 与中间步骤，适用于深度调试与问题复现 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
  - **用量统计**：按模型、API-Key、时间粒度（分钟/小时/天）统计 [Token](../concepts/token.md)、图像张数、视频秒数等，数据延迟约 1 小时 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

> **注意**：文档 1 称“监控数据按业务空间隔离”，而文档 2 在“查看模型用量”小节明确说明“数据按[业务空间]维度统计，不支持按阿里云账号维度统计”，二者一致；但文档 2 的“常见问题”中又指出“可在账单详情页面按阿里云账号查看 Token 总用量”，该口径差异属计费系统范畴，不影响监控功能本身的数据隔离逻辑。

## 关键参数与指标

| 指标名称 | 含义 | 是否支持告警 | 说明 |
|----------|------|----------------|------|
| 调用次数 | 模型被调用的总次数 | ✅ | 可配置突增告警 |
| 失败次数 / 失败率 | 调用失败次数及占比 | ✅ | 排查可用性问题的首要指标 |
| 调用时长 | 请求到响应总耗时 | ✅ | 反映端到端延迟 |
| 首 Token 延时 | 首个 Token 返回延迟 | ✅ | 衡量首响性能的关键指标 |
| 模型消耗 TotalToken 数 | 模型维度 Token 消耗总量 | ✅ | **推荐配置环比突增告警以控制成本** [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| 限流错误次数（429） | 触发限流的次数 | ✅ | 直接反映配额瓶颈 |
| 非首 Token 延时 | 后续 Token 平均生成耗时 | ❌ | 不在预置告警模板中，无法配置告警 |
| RPM / TPM / TPS | 请求/Token/输出速度指标 | ❌ | 仅用于观察，不支持告警 |

- **告警阈值单位**：所有预置模板均基于**1 分钟统计周期**（如“失败次数1分钟总和大于10”），自定义模板支持 1–10080 分钟周期。
- **用量单位**：依模型类型而异——大语言/全模态/向量模型按 **Token**；视觉模型按 **张**；视频模型按 **秒**；语音模型按 **秒/字符/Token**（详见 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）。

## 使用方式

1. **访问入口**：
   - 监控概览页：[百炼控制台 → 运维管理 → 模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)
   - 用量统计页：[百炼控制台 → 费用与成本 → 模型用量](https://bailian.console.aliyun.com/cn-beijing/costing-balance/usage-statistics)
   - 告警配置页：[百炼控制台 → 运维管理 → 模型告警](https://bailian.console.aliyun.com/cn-beijing/model/alert)

2. **快速配置告警**：
   - 在模型监控详情页图表中点击指标旁的 **蓝色/红色告警铃铛**，可为当前模型+当前指标一键配置规则；
   - 或进入告警规则页，选择预置模板（如“模型调用失败占比1分钟总和大于1%”），填写模型、持续时间、通知对象后创建。

3. **开启高级能力**：
   - **推理日志**：需先完成[日志投递](../../raw/model-user-guide/model-monitoring/model-telemetry.md)（授权 SLS 角色 + 创建日志库），再于日志页面开启；
   - **监控数据投递**：需授权云监控服务角色并开通 Prometheus 实例，方可将指标投递至自有监控系统。

## 限制和注意事项

- **数据时效性**：监控图表数据延迟 **分钟级**；用量统计数据延迟 **约 1 小时**；审计日志查询最长支持 **30 天**；推理日志截断长度上限为 **128KB**。
- **权限与隔离**：所有监控、用量、日志数据严格按**业务空间**隔离，跨空间不可见。
- **告警依赖项**：创建告警规则前**必须完成云监控服务角色授权**，否则按钮置灰且提示“未授权云监控服务角色，无法创建告警规则” [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
- **投递风险**：
  - 关闭审计日志投递将**自动关闭推理日志投递**，且关闭期间日志**无法补录**；
  - 在 SLS 中**不得删除百炼创建的日志库**或**修改索引**，否则导致投递失败。
- **模型兼容性**：语音、图片、视频生成及三方直连模型不支持监控与告警，控制台对应模型行不显示“查看详情”入口。
- **免费额度联动**：“免费额度用完即停”功能开启后，额度耗尽将返回 `403 AllocationQuota.FreeTierOnly` 错误，该行为独立于监控告警，但建议结合用量告警提前干预。

## 来源文档

- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)
- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)


