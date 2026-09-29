# model monitoring

百炼平台的 model monitoring 是面向生产环境的模型调用可观测性能力，提供分钟级延迟的用量统计、性能指标监控、失败诊断、告警配置及日志审计功能。所有数据按业务空间隔离，不跨空间聚合；监控数据仅作运维参考，计费以账单为准。核心能力覆盖用量追踪、健康度评估、异常告警与请求级排查，适用于模型服务稳定性保障与成本精细化管控。

## 支持的模型/功能

- **支持范围**：所有在[模型列表](raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)中可调用的模型（含调优后模型）均支持用量查看与基础监控；但语音、图片、视频生成及三方直连等部分模型**不支持监控告警功能**，具体需以控制台实际展示为准 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
- **核心功能模块**：
  - **用量统计**：按模型 Code、API-Key、时间维度（分钟/小时/天）查看 Token、图像张数、视频秒数等用量，支持 Top10 模型排序与导出 [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。
  - **实时监控**：调用后分钟级可见调用次数、失败率、首 Token 延时、调用时长等 14+ 指标，支持图表趋势分析与下钻至单模型详情页 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
  - **告警管理**：基于预置或自定义模板为关键指标（如失败率、TotalToken 数、429 次数）配置阈值告警，支持多通知渠道与重复策略。
  - **日志审计**：默认开启审计日志（含 Request ID、状态码、Token 用量、延时），可选开启推理日志（含完整 Prompt/Response，需投递至 SLS）。

> **注意**：文档 1 中“免费额度用完即停”功能描述为“返回403错误：AllocationQuota.FreeTierOnly”，但该错误码未在文档 2 的[错误码](raw/model-api-reference/preparations/error-code.md)引用中明确列出；实际行为应以控制台提示和最新错误码文档为准。

## 关键参数

| 参数 | 说明 | 取值/约束 | 来源 |
|------|------|-----------|------|
| `time_range` | 监控/用量查询时间范围 | 最大支持 30 天；超期数据需通过费用中心查询 [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) | [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) |
| `granularity` | 时间精度 | 分钟（≤1天）、小时（≤7天）、天（任意跨度）；分钟精度在跨天查询时不可用 | [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) |
| `api_key_id` | API-Key 筛选 | 仅显示当前业务空间下已创建且未删除的 API-Key；删除后日志中仅保留 ID | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `alert_check_period` | 告警检查周期 | 必填，单位为秒；最小值为 0（触发即告警），默认 60 秒 | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `alert_duration` | 告警持续时间 | 必填，单位为分钟；用于判断指标是否持续越界 | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |

## 使用方式

1. **访问入口**：
   - 用量统计：控制台 → [模型用量](https://bailian.console.aliyun.com/cn-beijing/costing-balance/usage-statistics)
   - 监控告警：控制台 → 运维管理 → [模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)
   - 告警规则：控制台 → [模型告警](https://bailian.console.aliyun.com/cn-beijing/model/alert)
   - 日志审计：模型监控页 → 模型列表 → 「查看日志」

2. **快速配置告警**：
   - 在模型监控详情页，点击任一支持告警的指标（如「失败率」）旁的蓝色铃铛图标；
   - 选择预置模板（如“模型调用失败占比1分钟总和大于1%”），填写通知对象与时段，点击创建；
   - **前提**：需先完成[监控数据投递](../../raw/model-user-guide/model-monitoring/model-telemetry.md)中的云监控服务角色授权。

3. **启用推理日志**：
   - 进入日志页面 → 切换至「推理日志」页签 → 点击「开始配置」；
   - 依次完成日志服务角色授权、开通日志服务、创建日志库；
   - **注意**：必须先开启审计日志投递，否则无法启用推理日志 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

## 限制和注意事项

- **数据延迟与范围**：
  - 用量统计数据延迟约 1 小时，且**不支持查询 30 天以前的数据**；更早数据需导出账单 [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。
  - 监控数据同样存在分钟级延迟，且**不作为计费依据**，对账请以费用中心账单为准 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

- **功能可用性限制**：
  - 部分模型（语音、图片、视频生成、三方直连）**不支持监控告警**，控制台对应模型行无「查看详情」入口 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
  - 推理日志长度上限为 128KB，超长内容将被截断；如需完整 Prompt/Response，请在客户端自行记录。

- **权限与依赖**：
  - 创建告警规则前，**必须完成云监控服务角色授权**，否则按钮置灰并提示“未授权云监控服务角色” [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
  - 关闭审计日志投递将**自动关闭推理日志投递**，且关闭期间日志**无法补录** [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

- **成本与计费**：
  - 告警规则本身免费，但依赖的云监控、SLS、Prometheus 服务按实际用量计费；
  - 免费额度用完即停功能仅在**仍有未消耗额度时可开启**；额度耗尽后需等待额度清零才能关闭该开关 [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


