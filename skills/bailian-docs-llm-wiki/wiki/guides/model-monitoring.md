# model monitoring

百炼平台的 model monitoring 是面向开发者的一套可观测性能力，提供分钟级延迟的模型调用统计、性能指标监控、多维度告警配置及审计/推理日志能力，覆盖用量分析、健康度评估与异常排查全链路。所有监控数据按业务空间隔离，不跨空间可见；监控数据仅作运维参考，**不作为计费依据**，对账请以费用中心账单为准。核心能力分为用量统计、实时监控、告警管理与日志追踪四类，需结合 [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) 与 [监控告警 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md) 两份文档协同使用。

## 支持的模型/功能

- **用量统计**：支持所有百炼平台已上线模型（含调优后模型），包括大语言模型、视觉模型、语音模型、全模态模型、向量模型等，详见 [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) 中的「适用范围」章节。
- **实时监控与告警**：支持绝大多数官方模型，但语音、图片/视频生成及三方直连等部分模型**不支持**监控与告警功能，具体以控制台实际可选模型为准（[监控告警 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md) 明确说明）。
- **日志能力**：
  - 审计日志：默认开启，覆盖全部模型，记录 Request ID、状态码、[Token](../concepts/token.md) 用量、延时等元数据，**不包含 Prompt/Response**；
  - 推理日志：需手动开启，仅支持北京和新加坡地域，且**仅部分模型支持**（不支持的模型在日志页签显示“当前模型不支持”）。

> **注意**：文档 1 称“模型列表中的所有模型均支持查看用量”，而文档 2 明确指出“语音、图片、视频生成及三方直连等部分模型不支持监控与告警”。二者范畴不同（用量 ≠ 监控），但存在隐含矛盾：若某模型完全不支持监控，则其用量数据是否仍能被准确采集并用于告警？实践中，用量统计（文档 1）与监控指标（文档 2）底层数据源不同——用量数据来自计费系统（小时级延迟），监控数据来自服务网关（分钟级延迟）。因此，**用量可用 ≠ 监控可用**，开发者应以控制台实际呈现为准。

## 关键参数

| 参数类别 | 参数名 | 说明 | 是否支持告警 | 来源 |
|----------|--------|------|----------------|------|
| 调用统计 | 调用次数、失败次数、失败率 | 总调用/失败频次及比率 | ✅ | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| 性能指标 | 调用时长、首 [Token](../concepts/token.md) 延时 | 端到端耗时与首 [Token](../concepts/token.md) 响应延迟 | ✅ | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| 成本指标 | Token总量、模型消耗 TotalToken 数 | 输入+输出 Token 总量，用于成本监控 | ✅（TotalToken 数为预置模板专用） | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| 限流安全 | 限流错误次数（429）、内容安全错误次数 | 429 触发频次、内容审核拦截次数 | ✅（429 次数） / ❌（内容安全） | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| 用量维度 | API-Key、推理类型（实时/批量）、时间精度（分/时/天） | 用于筛选用量报表，影响图表粒度 | — | [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) |

## 使用方式

1. **用量查看**：  
   - 访问 [模型用量](https://bailian.console.aliyun.com/cn-beijing/costing-balance/usage-statistics)，按模型类型（大语言模型/视觉模型等）、时间范围（≤30 天）、API-Key 筛选；  
   - 支持按分钟/小时/天精度查看趋势，搜索模型 Code（如 `qwen-plus`）定位单模型用量；  
   - 免费额度使用情况在 [免费额度](https://bailian.console.aliyun.com/cn-beijing/costing-balance/free-quota) 页面统一管理，支持批量开关「免费额度用完即停」。

2. **监控与告警配置**：  
   - 进入 [模型监控概览页](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)，筛选时间、API-Key 后查看整体健康度；  
   - 点击模型「查看详情」进入监控详情页，在支持告警的指标图表上点击铃铛图标，快速创建规则；  
   - **必须前置授权**：在监控投递入口完成云监控服务角色授权（否则告警创建按钮禁用）；  
   - 推荐直接选用预置告警模板，例如：  
     - `模型调用失败占比1分钟总和大于1%`（保障可用性）  
     - `模型消耗 TotalToken 数1分钟总和大于10000`（控制成本）  

3. **日志排查**：  
   - 审计日志：默认可用，支持按 Request ID、状态码（200/4XX/5XX）、7–30 天时间范围筛选；  
   - 推理日志：需先开启审计日志投递 → 在日志页签点击「开始配置」→ 授权 SLS 角色并指定日志库；  
   - 日志投递关闭后，期间日志**无法补录**，请谨慎操作。

## 限制和注意事项

- **数据延迟与范围**：  
  - 用量统计延迟约 **1 小时**，且**不支持查询 30 天以前数据**；更早数据需通过费用中心账单导出（[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）；  
  - 监控数据延迟为**分钟级**，但仅反映当前业务空间，不支持跨空间或账号维度聚合。

- **功能依赖关系**：  
  - 告警功能强依赖「监控数据投递」授权，未授权则无法创建任何告警规则；  
  - 推理日志开启**必须以审计日志投递为前提**，关闭审计投递将同步关闭推理日志投递（[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。

- **地域与模型限制**：  
  - 推理日志**仅在北京、新加坡地域可用**，其他地域暂不支持；  
  - 部分模型（如三方直连、特定视频生成模型）**既不支持监控指标，也不支持推理日志**，控制台对应入口将隐藏或置灰。

- **计费与存储责任**：  
  - 监控数据投递至云监控 Prometheus、日志投递至 SLS 均会产生对应云产品费用；  
  - SLS 日志库**不可删除、不可修改索引**，否则导致投递失败；  
  - 免费额度用完即停功能开启后，**仅能在仍有未消耗额度时操作**；额度耗尽后需等待账单更新再关闭（[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


