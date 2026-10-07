# model monitoring

百炼平台的 model monitoring 是面向生产环境的模型可观测性能力，提供分钟级延迟的调用统计、性能指标监控、告警配置及审计/推理日志能力，帮助开发者实时掌握模型健康度、排查异常并控制成本。该能力按业务空间隔离，数据不跨空间共享，且监控数据仅作运维参考，**不作为计费依据**（计费以费用中心账单为准）。核心能力覆盖用量观测、健康度诊断、异常告警与请求级溯源四个层次。

## 支持的模型/功能

- **支持范围**：所有在[模型列表](raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)中可调用的模型（含调优后模型）均支持基础监控与用量统计，但部分模型存在功能限制：语音、图片、视频生成及三方直连等模型**不支持监控告警与日志功能**，具体需以控制台实际展示为准 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
- **核心功能模块**：
  - **用量统计**：按模型 Code、API-Key、时间粒度（分钟/小时/天）聚合调用次数、[Token](../concepts/token.md) 总量、图像张数、视频秒数等，支持 TOP10 模型排行与详情下钻 [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。
  - **性能监控**：首 [Token](../concepts/token.md) 延时、调用时长、非首 [Token](../concepts/token.md) 延时、TPS 等指标，其中首 Token 延时与调用时长是性能退化排查关键项 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
  - **告警管理**：支持基于预置模板（如“失败率 >1%”“TotalToken 数突增”）快速配置规则，覆盖失败次数、失败率、限流错误次数（429）、调用时长等 8 个可告警指标；内容安全错误次数、RPM、TPM 等**不支持告警** [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
  - **日志能力**：审计日志默认开启（含 Request ID、状态码、Token 用量、延时等），推理日志需手动开启并投递至 SLS，用于获取完整 Prompt/Response（长度上限 128KB）。

> **注意**：文档 1 中称“模型列表中的所有模型均支持查看用量”，而文档 2 明确指出“语音、图片、视频生成及三方直连等部分模型不支持监控告警”。二者不矛盾——用量统计（文档 1）与监控告警（文档 2）是不同能力层，但控制台对不支持告警的模型可能隐藏其监控详情入口，开发者应以实际控制台界面为准。

## 关键参数

| 参数名 | 说明 | 取值范围/约束 | 来源 |
|--------|------|----------------|------|
| `时间精度` | 监控图表与用量统计的时间粒度 | 分钟（≤1 天）、小时（≤7 天）、天（任意跨度）；用量页面不支持查看 30 天以前数据 [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) | 文档 1 |
| `推理类型` | 区分实时推理与批量推理 | 仅「大语言模型」页签支持筛选；若无批量推理数据，下拉框仅显示「实时推理」 | 文档 1 |
| `API-Key` | 用量与监控数据的归属标识 | 仅展示当前业务空间下已创建的 API-Key；被删除的 Key 在日志中仅显示 ID，无描述 | 文档 1 & 2 |
| `告警检查周期` | 告警规则触发检测频率 | 必填，单位为秒；默认 60 秒，最小值为 0（表示触发即告警） | 文档 2 |
| `持续时间` | 告警触发需满足阈值的连续时长 | 必填，单位为分钟；用于过滤瞬时抖动 | 文档 2 |

## 使用方式

1. **访问入口**：
   - 用量统计：[模型用量](https://bailian.console.aliyun.com/cn-beijing/costing-balance/usage-statistics) 页面（按模型类型页签切换）
   - 监控与告警：[模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry) → 概览页 → 点击模型「查看详情」或「查看日志」
   - 告警规则管理：[模型告警](https://bailian.console.aliyun.com/cn-beijing/model/alert) 页面
   - 免费额度管理：[免费额度](https://bailian.console.aliyun.com/cn-beijing/costing-balance/free-quota) 页面（含「用完即停」开关）

2. **快速配置告警**：
   - 在模型监控详情页图表中，点击支持告警的指标旁的蓝色铃铛图标，直接进入该指标的告警规则配置侧边面板；
   - 或前往告警页面，选择预置模板（如“模型调用失败占比1分钟总和大于1%”），填写模型、持续时间、通知对象后创建。

3. **开启推理日志**：
   - 需先完成**日志投递配置**（授权 SLS 角色 + 创建日志库）；
   - 在日志页面切换至「推理日志」页签，点击「开始配置」完成投递设置；
   - 开启后，日志列表将显示 Prompt 与 Response 字段（截断长度 ≤128KB）。

## 限制和注意事项

- **数据延迟与范围**：用量统计数据延迟约 1 小时；监控数据分钟级可见；用量不支持查询 30 天以前数据，更早数据需通过[费用与成本](https://billing-cost.console.aliyun.com/finance/expense-report/expense-detail-by-instance)页面导出账单获取 [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。
- **权限与隔离**：所有监控、用量、告警数据严格按**业务空间**维度隔离，不支持跨空间或按阿里云主账号维度汇总。
- **计费差异**：监控数据**不作为计费依据**，用量以费用中心账单为准；免费额度“用完即停”功能开启后，额度耗尽将返回 `403 AllocationQuota.FreeTierOnly` 错误，且**仅能在仍有未消耗额度时开启**，关闭需待额度完全耗尽后操作 [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。
- **投递依赖**：开启推理日志**必须先开启审计日志投递**；关闭审计日志投递将**自动关闭推理日志投递**，且关闭期间日志**无法补录**。
- **移动端限制**：阿里云 App **暂不支持**查看免费额度、模型用量及监控数据，仅限 PC 端控制台使用 [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


