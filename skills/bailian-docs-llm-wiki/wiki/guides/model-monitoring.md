# model monitoring

百炼平台的 model monitoring 是面向开发者的一体化可观测性能力，提供分钟级延迟的模型调用统计、性能指标监控、异常告警与审计/推理日志追踪。它与计费系统解耦（监控数据不作为计费依据），聚焦于服务健康度、稳定性与成本优化辅助决策。核心能力覆盖用量分析、实时指标监控、多维告警配置及结构化日志回溯，适用于生产环境问题排查、SLA 保障与资源治理。

## 支持的模型/功能

- **模型范围**：全部在百炼模型列表中上线的模型均支持基础监控（调用次数、失败率、时延等），但语音、图像/视频生成及三方直连类模型部分指标可能受限；具体支持情况需以控制台实时展示为准 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  
- **功能模块**：
  - **模型用量统计**：按业务空间维度聚合 Token、调用次数、图片张数、视频秒数等收费量纲数据，支持分钟至月粒度查询 [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)；
  - **实时监控图表**：展示调用次数、失败次数、首 Token 延时、调用时长等 15+ 指标，支持按时间、API Key、推理类型筛选；
  - **告警管理**：基于预置或自定义模板对关键指标（如失败率、TotalToken 数、429 次数）配置阈值告警，支持通知渠道与重复策略 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)；
  - **日志能力**：默认开启审计日志（含 Request ID、状态码、用量、延时），推理日志（含完整 Prompt/Response）需手动开启并依赖日志投递 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

> **注意**：文档 1 中称“失败次数、失败率、限流错误次数和内容安全拦截次数已移至[模型监控](raw/model-user-guide/model-monitoring/model-telemetry.md)页面”，而文档 2 的指标表明确列出“内容安全错误次数”和“限流错误次数”为监控指标，但注明“不支持告警”。二者无实质矛盾，仅说明前者已从用量页移出、后者在监控页保留只读展示。

## 关键参数

| 参数名 | 说明 | 是否支持告警 | 备注 |
|--------|------|--------------|------|
| `调用次数` | 模型被调用的总次数 | ✅ | 随业务波动，可用于容量规划 |
| `失败率` | 失败次数 / 总调用次数 | ✅ | 推荐配置告警（如 >1%），保障可用性 |
| `首 Token 延时` | 请求到首个 Token 返回的耗时 | ✅ | 核心用户体验指标，建议阈值 ≤10 秒 |
| `模型消耗 TotalToken 数` | 按模型维度统计的 Token 消耗总量 | ✅ | 预置告警模板专用指标，用于成本突增监控 |
| `限流错误次数` | HTTP 429 触发次数 | ✅ | 直接反映配额瓶颈，需结合 RPM/TPM 分析 |
| `内容安全错误次数` | 内容安全拦截次数 | ❌ | 仅展示，不可配置告警 |
| `非首 Token 延时` | 首 Token 后每 Token 平均生成耗时 | ❌ | 仅用于性能分析，不支持告警 |

> **注意**：文档 1 提到“批量离线推理和批量在线推理不展示调用次数”，而文档 2 的监控详情页未明确排除批量推理——实际以控制台行为为准：批量推理调用计入“调用次数”，但**不参与首 Token 延时等实时性指标计算**（因其非流式响应）。

## 使用方式

1. **访问入口**：登录百炼控制台 → 左侧导航栏 **运维管理 > 模型监控**（概览页）或 **运维管理 > 模型告警**（告警规则页）。
2. **查看监控**：
   - 在概览页筛选时间、推理类型、API Key，快速查看整体调用规模与健康度；
   - 点击模型行的 **查看详情** 进入单模型监控详情页，查看调用统计与性能图表；
   - 点击 **查看日志** 进入审计日志页签，支持按 Request ID、状态码（200/4XX/5XX）等筛选。
3. **配置告警**：
   - 在监控详情页图表上点击告警铃铛图标，快速为当前指标创建规则；
   - 或前往 [模型告警页面](https://bailian.console.aliyun.com/cn-beijing/model/alert) → **告警规则** 页签，使用预置模板（如“模型调用失败占比1分钟总和大于1%”）创建全模型告警；
   - 创建前需先完成[监控数据投递](../../raw/model-user-guide/model-monitoring/model-telemetry.md)中的云监控服务角色授权。
4. **开启推理日志**：
   - 进入日志页签 → 点击 **日志投递配置** → 完成 SLS 角色授权、开通日志服务、创建日志库；
   - 推理日志仅在北京、新加坡地域可用，且需先开启审计日志投递 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

## 限制和注意事项

- **数据时效性**：监控数据延迟约 1 分钟（调用次数）至 10 分钟（Token 用量）；审计日志最长可查 30 天，推理日志依赖 SLS 保留策略。
- **地域与时间限制**：
  - 模型用量数据仅支持查询 **2026 年 9 月及之后**的数据（美国弗吉尼亚地域为 2026 年 10 月起）[模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)；
  - 推理日志仅支持北京、新加坡地域 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
- **权限与隔离**：所有监控、用量、日志数据均按 **业务空间（Workspace）** 维度隔离，不支持跨空间或按阿里云主账号汇总。
- **告警依赖项**：创建告警规则前必须完成云监控服务角色授权，否则按钮禁用；授权后将自动开通云监控、SLS 及 Prometheus 服务，相关费用按实际用量收取。
- **日志投递风险**：关闭日志投递后，期间产生的日志**无法补录**；删除 SLS 日志库将导致投递失败，且索引不可修改 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
- **免费额度联动**：“免费额度用完即停”功能开启后，额度耗尽将返回 `403 AllocationQuota.FreeTierOnly` 错误，该状态**不触发监控告警**，需通过免费额度页面主动监控 [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


