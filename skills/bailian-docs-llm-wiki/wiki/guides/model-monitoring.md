# model monitoring

百炼平台的模型监控（model monitoring）是一套面向生产环境的可观测性能力，覆盖用量统计、性能指标、调用日志与告警配置四大维度，帮助开发者实时掌握模型服务健康度、成本消耗与异常行为。监控数据按业务空间隔离，分钟级延迟，不作为计费依据；计费以账单为准。核心能力分散在用量统计与监控告警两个子系统中，需结合使用 [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) 和 [监控告警 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md) 文档理解全貌。

## 支持的模型/功能

- **支持模型范围**：所有在百炼模型列表中可见的模型（含调优后模型）均支持用量查看与基础监控；但语音、图片、视频生成及三方直连等部分模型**不支持监控告警功能**，具体以控制台实际可选模型为准（详见 [监控告警 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。
- **核心功能模块**：
  - **用量统计**：按模型 Code、API-Key、时间范围（最大30天）、推理类型（仅大语言模型支持区分实时/批量）查看调用次数、[Token](../concepts/token.md)/张/秒等单位用量；
  - **性能监控**：支持调用次数、失败率、调用时长、首 [Token](../concepts/token.md) 延时、限流错误次数等12+指标的图表化展示；
  - **审计日志**：默认开启，记录 Request ID、模型、[Token](../concepts/token.md) 用量、状态码、延迟等元信息，**不含 Prompt/Response**；
  - **推理日志**：需手动开启并配置日志投递，记录完整 Prompt/Response（上限128KB）及中间步骤，用于深度调试；
  - **告警配置**：支持为关键指标（如失败率、TotalToken 数、429 次数）创建规则，依赖预置模板或自定义条件。

> **注意**：文档1中“应用于生产环境”建议使用[模型监控](raw/model-user-guide/model-monitoring/model-telemetry.md)配置告警，但该链接指向的是旧路径（`raw/...`），而当前有效文档为 [监控告警 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md)，二者内容主体一致，但后者结构更完整、指标定义更精确，应以本链接为准。

## 关键参数

| 参数类别 | 参数名 | 说明 | 是否必填 | 备注 |
|----------|--------|------|----------|------|
| **告警规则** | 持续时间 | 告警触发需连续满足阈值的分钟数 | 是 | 单位为分钟，最小值1 |
| | 告警检查周期 | 检查指标是否越界的频率 | 是 | 默认60秒，必须为≥0整数（0=立即触发） |
| | 告警等级 | INFO / WARNING / ERROR / CRITICAL | 否 | 影响通知优先级 |
| | 通知时段 | 告警发送的时间窗口 | 是 | 支持跨天（如23:00–01:00） |
| **用量查询** | 时间精度 | 分钟/小时/天 | — | 跨度＞1天不可选分钟；＞7天仅支持天粒度 |
| | API-Key 筛选 | 按 API Key ID 过滤用量 | — | 仅显示当前空间下已存在的 Key |
| **日志投递** | SLS 日志库 | 推理日志投递目标 | 是（开启时） | 删除该日志库将导致投递失败，且**无法补录**关闭期间日志 |

## 使用方式

1. **查看用量**：访问 [模型用量](https://bailian.console.aliyun.com/cn-beijing/costing-balance/usage-statistics)，选择模型类型页签（如「大语言模型」）、时间范围与精度，支持按模型名称搜索或 API-Key 筛选；数据延迟约1小时，不支持30天以前数据（更早数据需查费用中心账单）。
2. **查看监控详情**：进入 [模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)，在模型列表点击「查看详情」，查看单模型的调用统计与性能图表；点击指标旁的蓝色/红色告警铃铛可快速配置或管理告警规则。
3. **配置告警**：前往 [模型告警页面](https://bailian.console.aliyun.com/cn-beijing/model/alert)，先完成[监控数据投递](../../raw/model-user-guide/model-monitoring/model-telemetry.md)中的云监控服务角色授权，再创建告警规则——推荐直接选用预置模板（如“模型调用失败占比1分钟总和大于1%”）。
4. **开启推理日志**：在监控概览页进入日志页面 → 切换至「推理日志」页签 → 点击「开始配置」完成 SLS 授权与日志库设置；**审计日志投递为前置条件**，关闭审计投递将同步关闭推理日志投递。

## 限制和注意事项

- **数据隔离与延迟**：所有监控与用量数据按**业务空间**维度隔离，不支持跨空间或按阿里云主账号汇总；监控数据延迟约1分钟，用量统计延迟约1小时；账单数据为最终计费依据，存在分钟级更新差异。
- **模型兼容性限制**：语音、图片、视频生成及三方直连模型**不支持监控告警功能**（见 [监控告警 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md)），但用量统计仍可用。
- **告警能力边界**：仅表中明确标注“支持告警”的指标（如失败率、TotalToken 数）可配置；RPM、TPM、非首 Token 延时等**不支持告警**；内容安全错误次数、平均单次请求调用量等亦不可告警。
- **日志与投递风险**：关闭日志投递后，期间产生的日志**永久丢失，不可补录**；SLS 日志库被删除将导致投递失败，且平台侧不提供恢复机制；索引在 SLS 侧不可修改，否则查询失效。
- **免费额度联动**：「免费额度用完即停」开关仅在仍有未消耗额度时可开启，关闭需待额度完全耗尽后操作（额度消耗记录以账单为准，控制台数据分钟级更新）。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


