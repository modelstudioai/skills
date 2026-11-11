# model monitoring

百炼平台的 model monitoring 提供分钟级延迟的模型调用可观测能力，覆盖调用统计、性能指标、失败分析与告警配置全链路。它面向业务空间维度隔离数据，不作为计费依据（计费以[费用中心账单](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)为准），主要用于生产环境稳定性保障、成本异常识别与问题快速定位。核心能力分为用量统计、实时监控、日志审计与告警联动四部分，开发者可通过控制台或 API 集成使用。

## 支持的模型/功能

- **模型覆盖范围**：  
  - 全部在模型列表中可见的官方模型（含文本生成、深度思考、视觉理解、图像/视频生成、语音合成与识别、全模态、向量模型等）均支持用量查看与基础监控；  
  - [调优后的模型](raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)同样纳入统计与监控范围；  
  - > **注意**：语音、图片、视频生成及三方直连等部分模型**不支持监控告警功能**，具体支持情况需以控制台实际展示为准（参见[监控告警](raw/model-user-guide/model-monitoring/model-telemetry.md)文档说明）。

- **核心功能模块**：  
  - **用量统计**：按 Token、张、秒、字符等多量纲聚合，支持分钟/小时/天/月粒度查询（详见[模型用量](raw/model-user-guide/model-monitoring/model-usage-statistics.md)）；  
  - **实时监控**：调用次数、失败率、首 Token 延时、调用时长等 15+ 指标图表化呈现，支持按时间精度、推理类型、API Key 筛选；  
  - **审计日志**：默认开启，记录 Request ID、状态码、用量、延时等元数据（不含 Prompt/Response）；  
  - **推理日志**：需手动开启并配置日志投递，记录完整 Prompt/Response 与中间步骤（仅北京、新加坡地域支持）；  
  - **告警系统**：支持基于预置模板或自定义规则对关键指标（如失败率、TotalToken 数、429 次数）配置告警。

## 关键参数

| 参数名 | 说明 | 是否支持告警 | 来源文档 |
|--------|------|--------------|----------|
| `调用次数` | 模型被调用的总次数（含成功与失败） | ✅ | [监控告警](raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `失败率` | 失败次数 / 总调用次数 | ✅ | [监控告警](raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `模型消耗 TotalToken 数` | 按模型维度统计的 Token 消耗总量（预置告警模板专用） | ✅ | [监控告警](raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `首 Token 延时` | 请求发起到返回首个 Token 的耗时 | ✅ | [监控告警](raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `调用时长` | 完整请求响应耗时 | ✅ | [监控告警](raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `限流错误次数` | HTTP 429 触发次数 | ✅ | [监控告警](raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `平均单次请求调用量` | 用量 / 成功调用次数 | ❌ | [监控告警](raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `非首 Token 延时` | 首 Token 后每 Token 平均生成耗时 | ❌ | [监控告警](raw/model-user-guide/model-monitoring/model-telemetry.md) |

> **注意**：是否支持告警取决于该指标是否被纳入预置告警模板（如 `内容安全错误次数`、`RPM`、`TPM` 等均不支持告警配置）。

## 使用方式

1. **访问入口**：  
   - 用量统计：进入[模型用量](https://bailian.console.aliyun.com/cn-beijing/costing-balance/usage-statistics)页面；  
   - 实时监控与告警：进入[模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry) → 运维管理 > 模型监控；  
   - 日志查看：在模型监控概览页点击模型行的“查看日志”；  
   - 告警配置：进入[模型告警页面](https://bailian.console.aliyun.com/cn-beijing/model/alert)。

2. **典型操作路径**：  
   - **快速配置告警**：在模型监控详情页任一支持告警的指标图表上点击告警铃铛 → 填写规则名称、选择预置模板（如“模型调用失败占比1分钟总和大于1%”）、设置通知对象与时段 → 创建；  
   - **排查失败突增**：在监控概览页关注“失败次数”“限流错误次数”“失败率”三项趋势，结合审计日志按 `4XX`/`5XX`/`429` 状态筛选；  
   - **分析性能退化**：对比“首 Token 延时”与“调用时长”历史曲线，若持续上升需检查模型负载、输入长度或网络链路；  
   - **启用推理日志**：先完成[日志投递](raw/model-user-guide/model-monitoring/model-telemetry.md)授权与 SLS 日志库配置，再在日志页签开启推理日志（仅限北京、新加坡地域）。

3. **数据时效性**：  
   - 调用次数：约 1 分钟后可见；  
   - Token 用量与费用：约 10 分钟延迟；  
   - 审计日志：最长支持查询 30 天内数据；  
   - 监控图表：支持按分钟精度筛选（仅详情页），但按分钟查询最多回溯 1 天。

## 限制和注意事项

- **地域限制**：  
  - 美国（弗吉尼亚）地域**不展示调用次数**（仅用量统计缺失）；  
  - 推理日志**仅在北京、新加坡地域支持**，其他地域开启无效。

- **数据范围限制**：  
  - 所有监控与用量数据均按**业务空间维度隔离**，不支持跨空间或按阿里云账号维度汇总；  
  - 模型用量页面**仅支持查询 2026 年 9 月 1 日及之后的数据**，更早数据需通过[费用中心账单](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)导出；  
  - 告警历史仅保留**2026 年 9 月 3 日之后**的记录，此前数据需前往[云监控控制台](https://cloudmonitor.console.aliyun.com/)查看。

- **功能依赖与权限**：  
  - 创建告警规则前**必须完成云监控服务角色授权**，否则按钮不可点击（参见[监控告警](raw/model-user-guide/model-monitoring/model-telemetry.md)）；  
  - 开启推理日志**必须先开启审计日志投递**，且关闭审计日志投递将同步关闭推理日志投递；  
  - 关闭日志投递后，**关闭期间产生的日志无法补录至 SLS**，请谨慎操作。

- **计费与成本提示**：  
  - 监控数据本身免费，但开启[数据投递](raw/model-user-guide/model-monitoring/model-telemetry.md)会触发云监控、SLS 或 Prometheus 的实际用量计费；  
  - 免费额度用完即停功能开启后，**仅在仍有未消耗额度时可开启**；关闭该功能需等待额度完全耗尽后才可操作（以控制台显示为准）。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


