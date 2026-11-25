# model monitoring

model monitoring 是百炼平台提供的核心运维能力，用于实时观测模型调用的健康度、性能与异常行为。它覆盖调用统计、延迟指标、错误分布及日志审计四大维度，数据分钟级更新，支持按业务空间隔离查看。监控数据**不作为计费依据**，对账请以[费用中心账单](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)为准；用量类指标（如 [Token](../concepts/token.md)）的精确计费数据需参考[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)页面。

## 支持的模型与功能

- **模型范围**：所有在百炼模型列表中可选的模型均支持基础监控（调用次数、失败率、调用时长、首 [Token](../concepts/token.md) 延时等），但语音、图片/视频生成及三方直连模型部分指标可能受限，具体以控制台实际展示为准 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
- **核心功能**：
  - **实时监控图表**：概览页展示总调用次数、失败次数、平均调用时长、首包时长等卡片；详情页提供单模型多维指标趋势图。
  - **审计日志**：默认开启，记录 Request ID、时间、模型、[Token](../concepts/token.md) 用量、状态码、延迟等，**不含 Prompt/Response**。
  - **推理日志**：需手动开启，记录完整 Prompt/Response 与中间步骤，仅支持北京、新加坡地域 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
  - **告警系统**：支持为关键指标（如失败率、TotalToken 数、429 次数）配置阈值告警，预置 12 类模板覆盖常见场景 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

## 关键参数

| 参数 | 说明 | 是否支持告警 | 备注 |
|------|------|--------------|------|
| `调用次数` | 成功 + 失败的总请求量 | ✅ | 包含预置/独占吞吐单元调用 |
| `失败率` | 失败次数 / 总调用次数 | ✅ | 排查可用性问题首选指标 |
| `模型消耗 TotalToken 数` | 按模型维度统计的 Token 消耗总量 | ✅ | 预置告警模板专用指标，用于成本突增监控 |
| `首 Token 延时` | 请求到首个 Token 返回的耗时 | ✅ | 衡量模型响应启动性能的关键指标 |
| `调用时长` | 完整请求-响应耗时 | ✅ | 含网络与模型处理全链路 |
| `限流错误次数（429）` | 触发限流的请求次数 | ✅ | 直接反映配额或规格瓶颈 |
| `非首 Token 延时` | 首 Token 后每 Token 平均生成耗时 | ❌ | 仅用于性能分析，不可配置告警 |
| `缓存命中率` | 缓存命中 Token 数 / 输入 Token 数 | ❌ | 依赖上下文缓存功能启用 |

> **注意**：文档 1 中称“失败次数、失败率、限流错误次数已移至[模型监控](model-telemetry.md)页面”，而文档 2 明确其属于监控指标且支持告警；但文档 1 的表格中将“调用量”列为 Token 总量，文档 2 的指标表中对应项名为“模型消耗 TotalToken 数”——二者实为同一概念，推荐统一使用 **`模型消耗 TotalToken 数`** 这一术语，因其在告警模板和控制台 UI 中保持一致。

## 使用方式

1. **访问入口**：登录百炼控制台 → 左侧导航栏 **运维管理 > 模型监控**（[概览页](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)）。
2. **筛选数据**：
   - 时间：支持快捷选择（最近1h/24h/7d）或自定义起止时间；
   - 推理类型：在线推理、批量离线推理（Batch File）、批量在线推理（Batch Chat）；
   - API Key：仅显示当前业务空间下已创建的 Key。
3. **配置告警**：
   - 在监控详情页图表上点击 **告警铃铛图标**，快速为当前模型+指标创建规则；
   - 或进入 [模型告警页面](https://bailian.console.aliyun.com/cn-beijing/model/alert) → **告警规则** 页签，使用预置模板（如“模型调用失败占比1分钟总和大于1%”）或自定义规则；
   - **前提**：必须先完成[监控数据投递](../../raw/model-user-guide/model-monitoring/model-telemetry.md#h2-sec-delivery)中的云监控服务角色授权。
4. **查看日志**：
   - 审计日志：监控概览页 → 点击模型行“查看日志”；
   - 推理日志：需先开启审计日志投递，再在日志页签切换至“推理日志”并完成 SLS 日志库配置。

## 限制和注意事项

- **数据时效性**：监控数据延迟约 1–2 分钟；审计日志查询最长支持 30 天；推理日志仅北京/新加坡地域可用。
- **地域与时间限制**：模型用量数据仅支持查询 **2026年9月及之后**（美国弗吉尼亚为 2026年10月起）；更早数据需通过阿里云费用中心导出账单 [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。
- **权限与隔离**：所有监控数据按**业务空间**维度隔离，无法跨空间或按阿里云主账号汇总。
- **告警依赖**：创建告警规则前，必须完成云监控服务角色授权；未授权时按钮置灰并提示“未授权云监控服务角色，无法创建告警规则”。
- **日志投递风险**：
  - 关闭审计日志投递将**自动关闭推理日志投递**；
  - 关闭投递后，期间日志**无法补录**；
  - SLS 日志库不可删除，否则导致投递失败。
- **不支持场景**：阿里云 App 不支持查看监控数据；批量推理（Batch Chat）的 API Key ID 在监控中为空。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


