# model monitoring

百炼平台的模型监控（Model Monitoring）是一套面向开发者的服务可观测性能力，提供分钟级延迟的调用统计、性能指标与告警能力，用于实时掌握模型健康度、排查异常、控制 Token 成本及保障服务可用性。监控数据按业务空间隔离，仅对当前选中空间生效；所有监控指标均不作为计费依据，对账请以费用中心账单为准。该能力与[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)功能互补：前者聚焦实时运行态（如失败率、首 Token 延时），后者侧重离线用量汇总与成本分析。

## 支持的模型与功能

- **支持范围**：所有在百炼模型列表中可调用的模型（含调优后模型）均支持基础监控，但语音、图片、视频生成及三方直连等部分模型**不支持监控与告警**，具体以控制台实际展示为准（详见[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)文档说明）。
- **核心功能**：
  - **调用统计**：调用次数、失败次数、失败率、限流错误次数（429）、内容安全错误次数等；
  - **性能指标**：调用时长、首 Token 延时、非首 Token 延时、平均单次请求调用量等；
  - **资源消耗**：Token 总量、模型消耗 TotalToken 数（预置告警模板专用）；
  - **日志能力**：审计日志（默认开启，含 Request ID、状态码、延迟等，不含 Prompt/Response）；推理日志（需手动开启并配置日志投递，含完整 Prompt/Response，长度上限 128K）；
  - **告警管理**：支持基于预置或自定义模板为指定指标配置告警规则，并通过云监控通知渠道发送。

> **注意**：文档 2 中“应用于生产环境”章节提到“通过[模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)监控用量趋势”，但模型监控本身**不提供用量趋势图表**——用量趋势属于[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)页面功能，二者逻辑分离。此处引用存在概念混淆，应以实际控制台功能为准。

## 关键参数

| 参数名 | 是否必填 | 说明 | 来源 |
|--------|----------|------|------|
| `时间范围` | 是 | 支持快捷选择（如最近1小时）或自定义区间；审计日志最长查30天，监控图表无此限制 | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `推理类型` | 否（默认实时推理） | 仅影响筛选，不改变指标计算逻辑；批量推理用量需在[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)页签单独查看 | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `API-Key ID` | 否 | 仅展示当前业务空间下已创建且未删除的 API-Key；删除后日志中仅保留 ID，描述为空 | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `告警检查周期` | 是 | 默认 60 秒，单位为秒；设为 `0` 表示触发即告警 | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `持续时间` | 是 | 告警触发需满足阈值条件的连续时长（分钟），用于抑制瞬时抖动 | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |

## 使用方式

1. **访问入口**：登录百炼控制台 → 左侧导航栏 **运维管理 > 模型监控**（概览页）→ 或直接访问 [https://bailian.console.aliyun.com/cn-beijing/model/telemetry](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)。
2. **查看监控**：
   - 概览页：查看整体调用规模（总次数、失败次数、平均调用时长等）；
   - 模型列表：点击目标模型的 **查看详情** 进入监控详情页（含图表+告警铃铛），或 **查看日志** 进入审计日志页签；
   - 详情页：支持按时间精度（分钟/小时/天）、推理类型、API-Key 筛选；告警铃铛图标（灰色/蓝色/红色）直观标识配置与触发状态。
3. **配置告警**：
   - 方式一（快捷）：在详情页指标图表上点击告警铃铛 → 配置规则 → 保存；
   - 方式二（完整）：进入[模型告警页面](https://bailian.console.aliyun.com/cn-beijing/model/alert) → **告警规则**页签 → 创建规则（需先完成[监控数据投递](../../raw/model-user-guide/model-monitoring/model-telemetry.md)中的云监控服务角色授权）；
   - 推荐优先使用**预置告警模板**（如“模型调用失败占比1分钟总和大于1%”），避免手动配置阈值偏差。
4. **开启日志**：
   - 审计日志：默认开启，无需配置；
   - 推理日志：需先完成[日志投递](../../raw/model-user-guide/model-monitoring/model-telemetry.md)授权与 SLS 日志库配置，再于日志页面切换至“推理日志”页签并点击“开始配置”。

## 限制和注意事项

- **数据延迟**：监控图表数据延迟约 **1–3 分钟**；审计日志查询延迟约 **1 分钟**；模型用量数据延迟约 **1 小时**（见[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）。
- **告警限制**：
  - 仅表中明确标注“可配置告警”的指标（如失败率、调用时长、TotalToken 数）支持配置，`RPM`、`TPM`、`内容安全错误次数` 等不支持；
  - 告警依赖云监控服务角色授权，未授权时告警按钮置灰（提示“未授权云监控服务角色”）；
  - 告警历史仅保留 **2026年9月3日之后** 的记录，此前数据需前往云监控控制台查询。
- **日志限制**：
  - 审计日志不包含 Prompt/Response，调试需开启推理日志；
  - 推理日志单条 Prompt/Response 截断上限为 **128KB**，超长内容不可恢复；
  - 关闭日志投递后，**关闭期间产生的日志不会补录**，且无法复原。
- **投递依赖**：
  - 监控数据投递仅支持阿里云云监控 Prometheus 实例（不支持自建）；
  - 日志投递必须授权日志服务角色，且**禁止删除百炼自动创建的 SLS 日志库**，否则导致投递失败；
  - 开启推理日志投递前，**必须先开启审计日志投递**；关闭审计日志投递将同步关闭推理日志投递。
- **其他**：
  - 所有监控数据按**业务空间**隔离，跨空间不可见；
  - 监控数据**不作为计费依据**，费用以费用中心账单为准；
  - 免费额度使用情况与监控无关，需单独在[免费额度](https://bailian.console.aliyun.com/cn-beijing/costing-balance/free-quota)页面管理。

## 来源文档

- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)
- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)


