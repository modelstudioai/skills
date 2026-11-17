# model monitoring

model monitoring 是百炼平台面向开发者提供的模型调用可观测性能力，涵盖用量统计、性能指标监控、失败诊断、告警配置与日志审计四大核心能力。所有数据按**业务空间**维度隔离，分钟级延迟可见，不作为计费依据（计费以[费用中心账单](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)为准）。监控与用量功能相互补充：用量聚焦计费对账，监控侧重运行健康度与异常定位。

## 支持的模型/功能

- **覆盖模型范围**：全部在模型列表中公开的模型均支持用量查看与基础监控（含调优后模型）；但语音、图片、视频生成及三方直连等部分模型**不支持监控告警功能**，具体需在控制台确认 [监控告警](raw/model-user-guide/model-monitoring/model-telemetry.md) 页面可用性。
- **核心功能模块**：
  - **用量统计**：按 [Token](../concepts/token.md)、图像张数、视频秒数、语音时长等计费单位聚合，支持分组（模型/API Key/地域/规格等）与多维筛选 [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。
  - **实时监控**：调用次数、失败率、首 [Token](../concepts/token.md) 延时、调用时长、限流错误次数等 15+ 指标，图表化展示趋势 [监控告警](raw/model-user-guide/model-monitoring/model-telemetry.md)。
  - **告警管理**：支持基于预置/自定义模板为关键指标（如失败率、Total[Token](../concepts/token.md) 数、429 次数）配置阈值告警，并集成云监控通知渠道 [监控告警](raw/model-user-guide/model-monitoring/model-telemetry.md)。
  - **日志审计**：默认开启审计日志（含 Request ID、状态码、用量、延时），可选开启推理日志（含完整 Prompt/Response，需投递至 SLS） [监控告警](raw/model-user-guide/model-monitoring/model-telemetry.md)。

> **注意**：文档 1 中“失败次数、失败率、限流错误次数已移至[模型监控](raw/model-user-guide/model-monitoring/model-telemetry.md)页面”与文档 2 的实际功能划分一致；但文档 1 提到“批量离线推理和批量在线推理不展示调用次数”，而文档 2 的监控详情页明确支持按“推理类型”（含 Batch File / Batch Chat）筛选，且指标表中“调用次数”列为“可配置告警”。此处以文档 2 的监控能力描述为准——调用次数在监控系统中完整支持，仅在用量页面的图表视图中受限。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `模型消耗 TotalToken 数` | 预置告警模板专用指标，按模型维度统计的 Token 消耗总量，推荐用于成本突增告警 | [监控告警](raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `失败率` | 失败次数 / 总调用次数，建议配置阈值告警（如 >1%）保障可用性 | [监控告警](raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `首 Token 延时` | 请求到首个 Token 返回的耗时，是感知模型响应速度的核心指标 | [监控告警](raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `max_tokens` | API 调用参数，限制输出长度，直接影响 Token 用量与费用，建议生产环境必设 | [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) |

## 使用方式

1. **访问入口**：
   - 用量统计：控制台 → [模型用量](https://bailian.console.aliyun.com/cn-beijing/costing-balance/usage-statistics)
   - 监控告警：控制台 → 运维管理 → [模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)
   - 告警规则：控制台 → 运维管理 → [模型告警](https://bailian.console.aliyun.com/cn-beijing/model/alert)
   - 日志：模型监控详情页 → 切换至“日志”页签

2. **快速上手**：
   - 在监控概览页点击目标模型的 **查看详情**，进入该模型专属监控页，直接使用图表上的 **告警铃铛** 配置单指标告警；
   - 在告警页面选择 **预置告警模板**（如“模型调用失败占比1分钟总和大于1%”），填入模型即可创建；
   - 开启推理日志前，必须先完成 [日志投递](raw/model-user-guide/model-monitoring/model-telemetry.md) 的 SLS 授权与日志库配置。

3. **数据时效性**：
   - 调用次数：约 1 分钟后可见；
   - Token 用量/费用：约 10 分钟后更新；
   - 审计日志：最长支持查询 30 天，实时写入；
   - 告警历史：2026年9月3日后记录在百炼平台，此前数据需查云监控控制台。

## 限制和注意事项

- **地域与时间限制**：用量数据仅支持查询 **2026年9月及之后** 的记录（美国弗吉尼亚地域为 2026年10月起）；更早数据需通过 [费用与成本](https://usercenter2.aliyun.com/finance/expense-report/expense-detail) 查看 [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。
- **权限与隔离**：所有监控与用量数据严格按 **业务空间** 维度隔离，不支持跨空间或按阿里云主账号汇总。
- **告警依赖条件**：创建告警规则前，**必须完成云监控服务角色授权**，否则按钮不可用；授权后将自动开通云监控、SLS 及 Prometheus 服务（按量计费） [监控告警](raw/model-user-guide/model-monitoring/model-telemetry.md)。
- **日志投递风险**：关闭审计日志投递将**同步关闭推理日志投递**；关闭期间日志**无法补录**，请谨慎操作 [监控告警](raw/model-user-guide/model-monitoring/model-telemetry.md)。
- **免费额度联动**：“免费额度用完即停”功能开启后，仅当账户内**仍有未消耗额度时才可开启**；若需关闭，须待额度完全耗尽后操作 [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


