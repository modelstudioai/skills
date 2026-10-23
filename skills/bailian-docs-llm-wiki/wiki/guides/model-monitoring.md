# model monitoring

百炼平台的 model monitoring 是面向开发者的一套模型调用可观测性能力，涵盖用量统计、实时性能监控、失败诊断、告警配置与日志审计五大核心场景。所有数据按业务空间（Workspace）维度隔离，分钟级延迟，不作为计费依据；计费以账单系统为准。监控与用量功能相互补充：前者聚焦调用健康度（如延时、失败率、限流），后者聚焦资源消耗（如 Token、图像张数、秒数）。

## 支持的模型/功能

- **全量支持**：所有在[模型列表](https://bailian.console.aliyun.com/cn-beijing/model/list)中可选的模型（含大语言模型、视觉模型、语音模型、全模态模型、向量模型）均支持用量查看与基础监控（调用次数、失败次数、调用时长等）。
- **部分支持**：语音、图片、视频生成及三方直连类模型的**高级监控指标（如首 Token 延时、非首 Token 延时、缓存命中率）和告警配置可能受限**，具体支持情况需在控制台模型监控详情页确认 —— 详见 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) 文档说明。
- **功能覆盖**：
  - 用量统计：按模型 Code、API-Key、时间范围（最大 30 天）、推理类型（仅大语言模型支持区分实时/批量）多维聚合；
  - 实时监控：调用次数、失败率、首 Token 延时、调用时长、限流错误（429）等关键指标图表化展示；
  - 告警：支持基于预置模板或自定义规则对指定指标（如失败率 >1%、TotalToken 数突增）配置通知；
  - 日志：默认开启审计日志（含 Request ID、状态码、Token 用量、延时）；推理日志（含完整 Prompt/Response）需手动开启并配置日志投递。

> **注意**：文档 1 中称“模型列表中的所有模型均支持查看用量”，而文档 2 明确指出“语音、图片、视频生成及三方直连等部分模型不支持”监控告警功能。二者范围不一致：**用量统计（文档 1）覆盖全部模型；监控告警（文档 2）存在模型能力差异**。实际使用时，请以控制台对应模型的监控详情页是否显示指标图表及告警铃铛为准。

## 关键参数

| 参数 | 说明 | 是否支持告警 | 来源 |
|------|------|--------------|------|
| `失败率` | 失败次数 / 总调用次数 | ✅ 支持（预置模板：`模型调用失败占比1分钟总和大于1%`） | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `模型消耗 TotalToken 数` | 按模型维度统计的 Token 消耗总量（预置告警专用指标） | ✅ 支持（预置模板：`模型消耗 TotalToken 数1分钟总和大于10000`） | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `首 Token 延时` | 请求发起到返回首个 Token 的耗时（首包时长） | ✅ 支持（预置模板：`模型首包时长1分钟均值大于10秒`） | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `调用量（Token总量）` | 输入 + 输出 Token 总和 | ✅ 支持 | [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) |
| `RPM`（每分钟请求数） | 单位时间请求频次 | ❌ 不支持告警 | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |

## 使用方式

1. **访问入口**：
   - 用量统计：[模型用量](https://bailian.console.aliyun.com/cn-beijing/costing-balance/usage-statistics) 页面（支持按模型 Code 搜索、API-Key 筛选、分钟/小时/天精度切换）；
   - 监控告警：[模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry) → 概览页 → 点击模型「查看详情」；
   - 告警配置：[模型告警](https://bailian.console.aliyun.com/cn-beijing/model/alert) 页面，或直接点击监控图表上的告警铃铛；
   - 日志查看：监控概览页模型列表点击「查看日志」进入审计日志；推理日志需先开启日志投递。

2. **快速配置告警**：
   - 在模型监控详情页，点击任一支持告警的指标图表旁的蓝色铃铛图标；
   - 选择预置模板（如“模型调用失败占比1分钟总和大于1%”），填写通知对象、时段、重复策略后保存；
   - **前置依赖**：必须先完成[监控数据投递](../../raw/model-user-guide/model-monitoring/model-telemetry.md)中的云监控服务角色授权，否则创建按钮不可用。

3. **用量优化实践**（来自文档 1）：
   - 控制输出长度：调用 API 时显式设置 `max_tokens`；
   - 合理选型：简单任务优先选用轻量级模型；
   - 使用批量推理：非实时任务通过 OpenAI 兼容 Batch 接口降本；
   - Prompt 优化：减少冗余输入，降低 Token 消耗。

## 限制和注意事项

- **数据延迟**：用量统计延迟约 **1 小时**；监控数据延迟为**分钟级**；免费额度数据支持手动刷新同步。
- **时间范围限制**：
  - 用量统计：仅支持查询最近 **30 天** 内数据，更早数据需查账单；
  - 审计日志：最长支持查询 **30 天** 内日志；
  - 告警历史：2026年9月3日前的历史需前往[云监控控制台](https://cloudmonitor.console.aliyun.com/)查看。
- **地域限制**：推理日志功能**仅在北京和新加坡地域支持**，其他地域暂不可用。
- **投递依赖与风险**：
  - 开启推理日志**必须先开启审计日志投递**；关闭审计日志投递将自动关闭推理日志投递；
  - 关闭日志投递后，**关闭期间产生的日志无法补录**；
  - SLS 日志库被删除将导致日志投递失败，且平台侧不支持修改索引。
- **计费说明**：监控与告警功能本身**免费**；但开启监控数据投递（至 Prometheus）或日志投递（至 SLS）将产生对应云产品费用。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


