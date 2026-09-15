# model monitoring

百炼平台的 model monitoring 是面向开发者的一套可观测性能力，覆盖用量统计、实时性能监控、告警配置与日志审计四大核心场景。所有数据按**业务空间**维度隔离，分钟级延迟，不支持跨空间或账号维度聚合。监控数据仅用于运维参考，**不作为计费依据**，对账请以费用中心账单为准（详见[模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）。

## 支持的模型/功能

- **全量支持模型用量查看**：包括大语言模型、视觉模型、语音模型、全模态模型、向量模型等所有在模型列表中可见的模型，及其调优后的衍生模型（见[模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）。
- **监控与告警能力存在模型差异**：语音、图片/视频生成及三方直连类模型部分不支持监控告警（见[监控告警 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md)），具体支持状态需在控制台实时确认。
- **功能模块**：
  - **用量统计**：按模型 Code、API-Key、时间范围（最大30天）、推理类型（仅大语言模型支持区分实时/批量）多维聚合；
  - **实时监控**：调用次数、失败率、首 [Token](../concepts/token.md) 延时、调用时长、[Token](../concepts/token.md) 总量等14+指标，图表化展示；
  - **告警**：支持基于预置模板快速配置，覆盖失败率、限流（429）、[Token](../concepts/token.md) 消耗突增等关键场景；
  - **日志**：审计日志默认开启（含 Request ID、用量、延迟、状态码）；推理日志需手动开启（含完整 Prompt/Response，上限 128KB）。

> **注意**：文档1中“实时推理”定义包含模型广场、应用测试态/发布态、Prompt反馈优化等场景；而文档2中“推理类型”筛选仅在监控详情页提供，且明确说明“仅「大语言模型」页签支持按推理类型筛选”。二者范围描述存在粒度差异，**以控制台实际可筛选项为准**——即监控图表中的“推理类型”下拉框是否可用，取决于当前选中的模型类型页签。

## 关键参数

| 参数 | 说明 | 取值/约束 |
|------|------|-----------|
| `时间范围` | 监控与用量数据查询窗口 | 最大支持 **30 天**；审计日志最长可查 **30 天**；用量统计不支持查询 30 天以前数据（见[模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)） |
| `时间精度` | 图表时间粒度 | 分钟（≤1天）、小时（≤7天）、天（任意跨度）；精度选项动态禁用，不支持手动越界选择 |
| `API-Key` | 调用身份标识 | 仅显示当前业务空间下已创建且未删除的 API-Key；被删除的 Key 在日志中仅保留 ID |
| `推理类型` | 区分实时 vs 批量调用 | 仅大语言模型页签支持；若空间无批量推理历史，该下拉框仅显示“实时推理” |
| `告警检查周期` | 告警规则触发检测频率 | 必填，单位为秒；默认 60 秒；支持设为 0（即触发即告警） |
| `持续时间` | 告警触发需满足阈值的连续时长 | 必填，单位为分钟；用于过滤瞬时抖动 |

## 使用方式

1. **访问入口**：
   - 用量统计：[模型用量](https://bailian.console.aliyun.com/cn-beijing/costing-balance/usage-statistics)
   - 监控与告警：[模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry) → 概览页 → 点击模型「查看详情」
   - 告警管理：[模型告警页面](https://bailian.console.aliyun.com/cn-beijing/model/alert)
   - 日志审计：监控概览页 → 模型列表点击「查看日志」

2. **配置告警**（需前置授权）：
   - 首先在**监控数据投递**中完成云监控服务角色授权（见[监控告警 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）；
   - 进入告警规则页签 → 点击「创建告警规则」→ 选择**预置模板**（如“模型调用失败占比1分钟总和大于1%”）或自定义 → 设置模型、阈值、通知对象；
   - 推荐组合：为 `失败率` 配置可用性告警，为 `模型消耗 TotalToken 数` 配置环比突增告警以控本。

3. **开启推理日志**：
   - 前置条件：必须先开启**审计日志投递**（授权 SLS 角色 + 创建日志库）；
   - 在日志页面切换至「推理日志」页签 → 点击「开始配置」→ 完成 SLS 投递配置；
   - **警告**：关闭审计日志投递将同步关闭推理日志投递，且关闭期间日志不可补录。

## 限制和注意事项

- **数据延迟**：用量统计延迟约 **1 小时**；监控图表数据延迟为**分钟级**；审计日志查询延迟 ≤5 分钟。
- **权限隔离**：所有监控、用量、日志数据严格按**业务空间**隔离，无法跨空间汇总或导出。
- **计费一致性**：监控中“Token总量”等指标**不作为计费依据**，精确用量请以[费用中心账单](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)为准（见[模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）。
- **模型兼容性**：语音、图像/视频生成、三方直连模型可能不支持全部监控指标或告警配置，控制台界面会动态隐藏不支持项。
- **日志截断**：推理日志中 Prompt/Response 单条长度上限为 **128KB**，超长内容自动截断。
- **投递依赖**：告警规则创建、推理日志开启均强依赖对应云产品（云监控 Prometheus / 日志服务 SLS）的授权与开通，未完成则对应功能按钮置灰。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


