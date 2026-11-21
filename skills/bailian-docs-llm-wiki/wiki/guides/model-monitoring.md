# model monitoring

百炼平台的模型监控（Model Monitoring）是一套面向生产环境的可观测性能力，提供分钟级延迟的调用统计、性能指标、失败分析与告警能力，帮助开发者实时掌握模型服务健康度、排查异常并控制成本。监控数据按业务空间隔离，不作为计费依据；用量对账请以[费用中心账单](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)为准。核心功能覆盖从概览、详情、日志到告警的全链路运维闭环。

## 支持的模型与功能

- **支持范围**：全部百炼平台内置模型（含文本生成、视觉理解、图像/视频生成、语音合成与识别、全模态、向量模型等）均支持基础监控指标（如调用次数、失败率、首 Token 延时），但部分模型（如语音、图片、视频生成及三方直连模型）**不支持告警配置与推理日志**，具体需在控制台确认 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
- **核心功能模块**：
  - **监控概览与详情**：查看整体调用规模、单模型指标趋势、多维度（时间/推理类型/API Key）筛选；
  - **审计日志**：默认开启，记录 Request ID、状态码、Token 用量、延时等元数据，**不包含 Prompt/Response**；
  - **推理日志**：需手动开启，记录完整 Prompt/Response 及中间步骤，当前**仅在北京和新加坡地域支持** [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)；
  - **告警管理**：支持基于预置或自定义模板为关键指标（如失败率、TotalToken 数、429 次数）配置实时告警；
  - **数据投递**：可将监控指标投递至云监控 Prometheus 实例，或将日志投递至 SLS 日志库，用于长期留存或对接自有运维系统 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

> **注意**：文档 1 中“模型用量”页面已明确说明“失败次数、失败率、限流错误次数和内容安全拦截次数已移至[模型监控](raw/model-user-guide/model-monitoring/model-telemetry.md)页面”，而文档 2 的监控详情页也完整列出了这些指标。但文档 1 的“模型用量”表格中仍提及“工具调用次数”等收费相关指标，而文档 2 的监控指标表未包含该类字段——这表明**用量统计（计费导向）与监控指标（运维导向）存在职能分离，二者不可混用**。用量数据请严格参考 [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)，监控数据仅作健康度参考。

## 关键参数

| 参数名 | 说明 | 是否支持告警 | 备注 |
|--------|------|--------------|------|
| `调用次数` | 成功 + 失败的总请求次数 | ✅ | 包含在线推理、Batch File、Batch Chat |
| `失败次数` / `失败率` | 失败请求计数及占比 | ✅ | 排查突增首选指标；失败率 = 失败次数 / 总调用次数 |
| `模型消耗 TotalToken 数` | 按模型维度聚合的 Token 消耗总量 | ✅ | **推荐用于成本突增告警**，直接对应预置模板 |
| `调用时长` | 端到端响应时间（ms） | ✅ | 含网络传输与模型推理耗时 |
| `首 Token 延时` | 首 Token 返回延迟（ms） | ✅ | 衡量首包体验的关键性能指标 |
| `限流错误次数`（429） | 触发限流的请求次数 | ✅ | 与配额、RPM/TPM 设置强相关 |
| `内容安全错误次数` | 内容安全拦截次数 | ❌ | 不支持告警，仅用于审计日志分析 |
| `非首 Token 延时` | 后续 Token 平均生成耗时 | ❌ | 仅展示，不可配置告警 |
| `缓存命中率` | 缓存命中 Token 占输入 Token 比例 | ❌ | 依赖上下文缓存功能启用 |

## 使用方式

1. **访问入口**：登录百炼控制台 → 左侧导航栏 **运维管理 > 模型监控**（[概览页](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)）。
2. **快速排查**：
   - 在概览页模型列表点击 **查看详情** 进入单模型监控详情页，查看调用统计与性能图表；
   - 点击 **查看日志** 进入审计日志页签，按 Request ID 或状态码（如 `429`、`500`）筛选定位异常请求；
   - 如需完整 Prompt/Response，请先在日志页签开启**推理日志投递**（需授权 SLS 并创建日志库）。
3. **配置告警**：
   - 在监控详情页图表上点击 **告警铃铛图标**，快速为当前指标创建规则；
   - 或进入 [模型告警页面](https://bailian.console.aliyun.com/cn-beijing/model/alert) → **告警规则** 页签，使用预置模板（如“模型调用失败占比1分钟总和大于1%”）创建；
   - **前提**：必须先完成[监控数据投递](https://help.aliyun.com/zh/model-studio/model-telemetry#h2-sec-delivery)中的云监控服务角色授权。
4. **用量联动**：监控数据不用于计费，但可结合 [模型用量](https://bailian.console.aliyun.com/cn-beijing/costing-balance/usage-statistics) 页面（如 Tokens 用量、调用次数趋势）交叉验证成本合理性 [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

## 限制和注意事项

- **数据时效性**：监控指标延迟约 **1–2 分钟**；审计日志查询最长支持 **30 天**；推理日志需手动开启且仅限北京/新加坡地域。
- **地域与时间限制**：模型用量数据仅支持查询 **2026 年 9 月及之后**（美国弗吉尼亚为 10 月起）；更早数据需通过阿里云费用中心导出账单 [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。
- **权限与隔离**：所有监控与用量数据均按 **业务空间（Workspace）维度隔离**，不支持跨空间或按阿里云主账号汇总。
- **告警限制**：
  - 仅预置模板所列指标（共 12 类）支持告警配置，如 `RPM`、`TPM`、`内容安全错误次数` 等不可告警；
  - 告警检查周期最小为 **60 秒**（0 表示触发即告警，不推荐生产环境使用）；
  - 告警规则依赖云监控服务，授权后将自动开通云监控、SLS 及 Prometheus，产生对应云产品费用。
- **日志投递警告**：
  - 关闭审计日志投递将**同步关闭推理日志投递**；
  - 关闭投递期间产生的日志**无法补录**；
  - SLS 日志库由百炼创建，**禁止手动删除**，否则导致投递失败。
- **免费额度联动**：监控本身不控制额度，但可配合 [免费额度用完即停](https://bailian.console.aliyun.com/cn-beijing/costing-balance/free-quota) 开关实现成本兜底——该功能仅在仍有未消耗额度时可开启 [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


