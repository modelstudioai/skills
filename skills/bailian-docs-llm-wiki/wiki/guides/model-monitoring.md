# model monitoring

百炼平台的 model monitoring 是面向开发者的一套可观测性能力，提供分钟级延迟的模型调用统计、性能指标监控、告警配置及审计/推理日志能力，覆盖用量分析、健康度评估与异常排查全链路。所有监控数据按业务空间隔离，不跨空间聚合，且**不作为计费依据**（计费以账单为准）[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。核心能力分为用量统计、实时监控、告警策略和日志溯源四类，需结合 [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) 与 [监控告警 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md) 两份文档协同使用。

## 支持的模型/功能

- **用量统计**：支持所有百炼平台公开模型（含调优后模型）[模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)，包括大语言模型（Token）、视觉模型（张/秒）、语音模型（秒/字符/Token）、全模态模型（Token）和向量模型（Token）。
- **实时监控与告警**：支持绝大多数官方模型，但语音、图片/视频生成及三方直连等部分模型**不支持**监控与告警，具体以控制台实际可选模型为准 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
- **日志能力**：
  - 审计日志：默认开启，记录 Request ID、模型、Token 用量、延迟、状态码等元信息，**不包含 Prompt/Response**；
  - 推理日志：需手动开启，记录完整 Prompt/Response（上限 128KB）及中间步骤，依赖日志投递至 SLS 日志库 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

> **注意**：文档 1 中“适用于模型列表中的所有模型”与文档 2 中“语音、图片、视频生成及三方直连等部分模型不支持”存在范围矛盾。以文档 2 的实时监控能力描述为准——用量统计（文档 1）覆盖全模型，但**监控图表、告警配置、推理日志等高级可观测能力仅限支持模型可用**。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `time_range` | 时间范围：用量统计最多查 30 天；审计日志最多查 30 天；监控图表默认保留 7 天（控制台可手动刷新同步） | [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) |
| `granularity` | 时间精度：用量页支持分钟/小时/天（跨度 >1 天禁用分钟；>7 天仅支持天）；监控详情页才支持分钟级筛选 | [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) |
| `api_key_id` | 所有用量、监控、日志均支持按 API Key 筛选，用于多租户/多应用隔离分析 | [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) |
| `inference_type` | 仅「大语言模型」用量页支持按「实时推理」或「批量推理」筛选；监控页也支持该维度，但推理日志页**不支持**该筛选 | [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) |
| `alert_check_period` | 告警检查周期：最小单位为秒，必填且 ≥0（0 表示触发即告警），默认 60 秒 | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |

## 使用方式

1. **查看用量**：访问 [模型用量](https://bailian.console.aliyun.com/cn-beijing/costing-balance/usage-statistics)，选择模型类型页签（如「大语言模型」）、时间范围、API Key 等筛选条件；支持搜索模型名（如 `qwen-plus`）定位单模型用量 [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。
2. **查看监控**：进入 [模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)，在概览页查看整体调用规模与健康度；点击模型行「查看详情」进入单模型监控详情页，查看调用次数、失败率、首 Token 延时等指标图表 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
3. **配置告警**：
   - 先完成[监控数据投递](https://help.aliyun.com/zh/model-studio/model-telemetry#h2-sec-delivery)中云监控服务角色授权；
   - 进入 [模型告警页面](https://bailian.console.aliyun.com/cn-beijing/model/alert)，使用预置模板（如「模型调用失败占比1分钟总和大于1%」）快速创建规则；
   - 或点击监控图表上的蓝色/红色告警铃铛，为当前模型+指标一键配置 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
4. **查看日志**：
   - 审计日志：默认可用，在监控概览页点击模型行「查看日志」即可；
   - 推理日志：需先开启审计日志投递，再在日志页切换至「推理日志」页签并点击「开始配置」完成 SLS 授权与日志库绑定 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

## 限制和注意事项

- **数据延迟**：用量统计数据延迟约 1 小时；监控图表数据延迟为分钟级；审计日志查询最大跨度为 30 天 [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。
- **权限隔离**：所有监控、用量、日志数据严格按**业务空间**维度隔离，不支持按阿里云主账号维度聚合 [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。
- **告警限制**：仅表中明确标注“支持告警”的指标（如失败率、调用时长、TotalToken 数）可配置；RPM、TPM、非首 Token 延时等指标**不支持告警** [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
- **日志投递风险**：关闭审计日志投递将**自动关闭推理日志投递**；关闭期间产生的日志**无法补录**至 SLS [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
- **费用提示**：监控数据投递至云监控 Prometheus、日志投递至 SLS 均会产生对应云产品费用；推理日志存储于自有 SLS 日志库，**不在百炼免费额度覆盖范围内** [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


