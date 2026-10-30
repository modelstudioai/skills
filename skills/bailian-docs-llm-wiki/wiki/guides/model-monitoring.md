# model monitoring

百炼平台提供分钟级延迟的模型调用监控能力，覆盖调用规模、健康度、性能指标与异常事件，支持可视化分析、告警配置及日志追溯。监控数据按业务空间隔离，仅反映当前选中空间内的调用行为，**不作为计费依据**（计费请以[费用中心](https://bailian.console.aliyun.com/cn-beijing/costing-balance/overview)账单为准）。核心能力围绕模型可观测性构建，面向运维与成本治理场景。

## 支持的模型与功能

- **支持范围**：所有在百炼控制台模型列表中可见的模型（含调优后模型），但语音、图片、视频生成及三方直连类模型**部分不支持**监控与告警，具体需以控制台实时展示为准 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  
- **核心功能**：
  - **监控概览**：展示整体调用次数、失败次数、失败率、平均调用时长、首 [Token](../concepts/token.md) 延时等关键卡片；
  - **模型详情页**：按单模型维度查看调用统计（如调用次数、[Token](../concepts/token.md) 总量）与性能指标（如首 [Token](../concepts/token.md) 延时、非首 Token 延时）；
  - **审计日志**：默认开启，记录 Request ID、状态码、Token 用量、延时等元数据，**不含 Prompt/Response**；
  - **推理日志**：需手动开启并配置日志投递，记录完整 Prompt/Response 及中间步骤，适用于深度调试 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)；
  - **用量统计**：独立于监控系统，在[模型用量](https://bailian.console.aliyun.com/cn-beijing/costing-balance/usage-statistics)页面提供按 Token、张、秒等计费单位的用量明细，用于对账与成本分析 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

> **注意**：文档 1 中称“监控数据不作为计费依据”，而文档 2 明确指出“Token 等用量用于核对费用”，二者逻辑一致（监控指标 ≠ 计费源数据），但需注意：**失败次数、失败率、限流错误次数和内容安全拦截次数已从[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)页面移除，统一归入监控模块**，避免重复引用。

## 关键参数与指标

| 指标名称 | 是否支持告警 | 说明 | 数据延迟 |
|----------|--------------|------|-----------|
| 调用次数、失败次数、失败率、调用时长、首 Token 延时、限流错误次数、模型消耗 TotalToken 数 | ✅ | 可直接选用预置告警模板或自定义规则 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) | 分钟级（约 1–3 分钟） |
| 非首 Token 延时、RPM、TPM、缓存命中率、内容安全错误次数 | ❌ | 不在预置模板中，图表无告警铃铛，不可配置告警 | 同上 |
| Tokens 用量、图片张数、视频秒数等 | — | 仅出现在[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)页面，用于计费核对，**不可告警** | 用量延迟约 10 分钟；调用次数延迟约 1 分钟 |

- **告警阈值单位**：失败率以百分比（如 `> 1%`）、调用时长以秒（如 `> 60s`）、TotalToken 数以绝对值（如 `> 10000`）；
- **统计周期**：告警模板中可设 1–10080 分钟（即 7 天），默认检查周期为 60 秒。

## 使用方式

1. **访问入口**：登录百炼控制台 → 左侧导航栏 **运维管理 > 模型监控**（概览页）或 **费用与成本 > 模型用量**（用量页）；
2. **配置告警**：
   - 在模型监控详情页图表中点击告警铃铛，快速为单指标配置规则；
   - 或进入 **运维管理 > 模型告警** 页面，使用预置模板（如“模型调用失败占比1分钟总和大于1%”）创建全量规则；
   - **前提**：必须先完成[监控数据投递](../../raw/model-user-guide/model-monitoring/model-telemetry.md)中的云监控服务角色授权；
3. **开启日志**：
   - 审计日志默认启用，无需操作；
   - 推理日志需在日志页面点击 **开始配置**，完成 SLS 角色授权与日志库创建（仅支持北京、新加坡地域）；
4. **筛选分析**：支持按时间（快捷/自定义）、推理类型（实时/批量）、API-Key、模型等多维组合筛选，详情见[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

## 限制和注意事项

- **地域限制**：推理日志仅在北京、新加坡地域可用；美国（弗吉尼亚）地域不展示调用次数；
- **数据时效性**：监控指标延迟约 1–3 分钟，用量数据中调用次数延迟约 1 分钟、Token 用量延迟约 10 分钟；
- **投递依赖**：告警规则创建、推理日志开启均强依赖[数据投递](../../raw/model-user-guide/model-monitoring/model-telemetry.md)配置；关闭审计日志投递将**自动关闭推理日志投递**；
- **存储与费用**：监控数据默认存储于百炼平台侧；投递至云监控（Prometheus）或日志服务（SLS）将产生对应云产品费用；
- **权限隔离**：所有监控与用量数据严格按**业务空间**隔离，跨空间不可见；
- **历史数据**：告警历史仅保留 2026 年 9 月 3 日之后记录；用量数据仅支持查询 2026 年 9 月 1 日之后记录，更早数据需通过阿里云账单系统导出。

## 来源文档

- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)
- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)


