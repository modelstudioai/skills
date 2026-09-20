# model monitoring

百炼平台的 model monitoring 是面向开发者的一套可观测性能力，提供分钟级延迟的模型调用统计、性能指标监控、告警配置及审计/推理日志支持，覆盖用量分析、健康度评估与异常排查全链路。所有监控数据按业务空间隔离，不跨空间聚合，且**不作为计费依据**（计费以费用中心账单为准）。核心能力分为用量统计、实时监控、告警策略和日志溯源四类，需结合 [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) 与 [监控告警 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md) 两份文档协同使用。

## 支持的模型/功能

- **模型范围**：所有在百炼模型列表中上线的模型（含[调优后的模型](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)）均支持用量查看与基础监控；但语音、图片、视频生成及三方直连等部分模型**不支持监控告警功能**，具体以控制台实际可选模型为准。
- **功能覆盖**：
  - ✅ 用量统计：支持大语言模型（Token）、视觉模型（张/秒）、语音模型（秒/字符/Token）、全模态模型（Token）、向量模型（Token）等多模态用量维度；
  - ✅ 实时监控：调用次数、失败率、调用时长、首 Token 延时、限流错误次数等 13 项核心指标（详见下文“关键参数”）；
  - ✅ 告警配置：仅预置模板覆盖的指标（如失败率、TotalToken 数、429 次数等）支持告警，非预置指标（如 RPM、TPM、内容安全错误次数）**不可配置告警**；
  - ✅ 日志能力：审计日志默认开启（不含 Prompt/Response）；推理日志需手动开启并依赖日志投递至 SLS。

> **注意**：文档 1 中提到“模型列表中的所有模型均支持查看用量”，而文档 2 明确指出“语音、图片、视频生成及三方直连等部分模型不支持监控告警”。二者无矛盾——用量统计（文档 1）与监控告警（文档 2）是独立能力，但开发者需知：**有用量 ≠ 有监控图表/告警**。实际使用前请在控制台确认目标模型是否出现在模型监控列表中。

## 关键参数

| 指标名称 | 含义 | 是否支持告警 | 说明 |
|----------|------|----------------|------|
| 调用次数 | 模型被调用总次数 | ✅ | 可配置突增/骤降告警 |
| 失败次数 / 失败率 | 请求失败次数及占比 | ✅ | 排查可用性问题首选指标（见 [监控告警 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md)） |
| 模型消耗 TotalToken 数 | 按模型维度统计的 Token 总消耗量 | ✅ | 预置告警模板专用指标，用于成本突增监控 |
| 调用时长 | 请求到响应总耗时 | ✅ | 端到端延迟，含网络与模型计算 |
| 首 Token 延时 | 请求发起到首个 Token 返回的耗时 | ✅ | 衡量模型“启动”性能的关键指标 |
| 限流错误次数（429） | 触发限流的请求次数 | ✅ | 直接反映配额或 QPS 瓶颈 |
| 非首 Token 延时 | 首 Token 后每 Token 平均生成耗时 | ❌ | 仅展示，不可告警 |
| RPM / TPM / TPS | 每分钟请求数 / Token 数 / 每秒输出 Token 数 | ❌ | 仅展示，不支持告警配置 |
| 内容安全错误次数 | 被内容安全策略拦截次数 | ❌ | 仅审计日志可追溯，监控页不支持告警 |

## 使用方式

1. **访问入口**：
   - 用量统计：[模型用量页面](https://bailian.console.aliyun.com/cn-beijing/costing-balance/usage-statistics)（数据延迟约 1 小时，不支持 30 天以前数据）；
   - 实时监控与告警：[模型监控页面](https://bailian.console.aliyun.com/cn-beijing/model/telemetry) → 运维管理 > 模型监控；
   - 告警规则管理：[模型告警页面](https://bailian.console.aliyun.com/cn-beijing/model/alert)；
   - 日志查看：监控概览页 → 模型列表点击「查看日志」。

2. **关键操作**：
   - **用量筛选**：支持按模型 Code、API-Key、时间范围（分钟/小时/天）、推理类型（仅大语言模型支持区分实时/批量）筛选；
   - **监控告警配置**：在模型监控详情页图表上点击告警铃铛图标，快速为当前指标创建规则；或前往告警页面使用预置模板（如“模型调用失败占比1分钟总和大于1%”）；
   - **日志开启**：推理日志需先完成[日志投递](../../raw/model-user-guide/model-monitoring/model-telemetry.md)配置（授权 SLS 角色 + 创建日志库），再于日志页签开启；
   - **批量管理**：免费额度页面支持批量开启/关闭「免费额度用完即停」，但该功能与监控告警无直接关联（见 [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）。

## 限制和注意事项

- **数据延迟与范围**：
  - 用量统计延迟约 1 小时，且**不支持查询 30 天以前数据**；更早数据需通过费用中心账单导出；
  - 监控数据延迟为**分钟级**，但仅限当前业务空间，不支持跨空间或账号维度聚合；
  - 审计日志最长支持查询**30 天内**数据，推理日志依赖 SLS 配置的存储周期。

- **权限与依赖**：
  - 告警规则创建前**必须授权云监控服务角色**，否则按钮禁用（见 [监控告警 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）；
  - 推理日志开启前**必须先开启审计日志投递**，关闭审计投递将同步关闭推理投递；
  - 开启监控/日志投递会自动开通云监控、SLS、Prometheus 服务，产生对应云产品费用。

- **行为约束**：
  - 「免费额度用完即停」功能**仅能在仍有未消耗额度时开启**，关闭需待额度完全耗尽后操作；
  - SLS 日志库**不可删除或修改索引**，否则导致投递失败且无法恢复；
  - 关闭日志投递后，**关闭期间产生的日志永久丢失，无法补录**。

- **其他**：
  - 阿里云 App **暂不支持**查看免费额度、用量或监控数据，仅限 PC 控制台；
  - Token 统计以模型分词器实际切分结果为准，非字符串长度；各模型最大输入/输出 Token 限制详见模型列表。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


