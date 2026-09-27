# model monitoring

百炼平台提供面向生产环境的模型调用可观测能力，覆盖分钟级监控指标、审计日志、推理日志及告警配置。监控数据按业务空间隔离，仅反映当前空间内模型调用行为，不作为计费依据；计费以费用中心账单为准。核心能力聚焦于调用健康度（失败率、限流）、性能（首 [Token](../concepts/token.md) 延时、调用时长）和资源消耗（Total[Token](../concepts/token.md) 数、调用量）三大维度。

## 支持的模型与功能

- **支持范围**：所有在模型列表中可见的模型（含调优后模型）均支持基础监控与用量统计，但语音、图片、视频生成及三方直连等部分模型**不支持监控告警**，具体需以控制台实际展示为准 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  
- **核心功能**：
  - **监控概览与详情**：展示调用次数、失败次数、失败率、调用时长、首 [Token](../concepts/token.md) 延时、TotalToken 数等指标图表；
  - **审计日志**：默认开启，记录 Request ID、时间、模型、Token 用量、延迟、状态码等，**不含 Prompt/Response**；
  - **推理日志**：需手动开启并配置日志投递，记录完整 Prompt/Response 与中间步骤，适用于调试与复现 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)；
  - **用量统计**：按模型、API-Key、时间粒度（分钟/小时/天）统计 Token、图像张数、视频秒数等，数据延迟约 1 小时 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

> **注意**：文档 1 明确指出“语音、图片、视频生成及三方直连等部分模型不支持”监控告警；而文档 2 仅说明“所有模型均支持查看用量”。二者无矛盾——用量统计（如 Token、张数）与监控告警（如失败率、延时告警）是不同能力栈，前者覆盖更广，后者受模型服务架构限制。

## 关键参数

| 参数名 | 说明 | 是否支持告警 | 来源 |
|--------|------|--------------|------|
| `失败次数` / `失败率` | 衡量可用性，失败率 = 失败次数 / 总调用次数 | ✅ 支持 | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `首 Token 延时` | 首包时长，反映模型冷启与首响应性能 | ✅ 支持 | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `调用时长` | 端到端请求耗时 | ✅ 支持 | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `模型消耗 TotalToken 数` | 按模型维度聚合的 Token 消耗总量，用于成本监控 | ✅ 支持（预置模板专用） | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `非首 Token 延时` | 后续 Token 平均生成耗时 | ❌ 不支持 | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `RPM` / `TPM` | 每分钟请求数 / Token 数 | ❌ 不支持 | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |

## 使用方式

1. **访问入口**：登录百炼控制台 → **运维管理** > **模型监控**（概览页）或 **费用与成本** > **模型用量**；
2. **筛选监控数据**：支持按时间（快捷/自定义）、推理类型（实时/批量）、API-Key（仅当前空间存在者）筛选；
3. **配置告警**：
   - 在监控详情页点击指标旁的**告警铃铛**，快速为单指标配置规则；
   - 或前往 [模型告警页面](https://bailian.console.aliyun.com/cn-beijing/model/alert) → **告警规则**页签，使用预置模板（如“模型调用失败占比1分钟总和大于1%”）创建规则；
   - **前提**：必须先完成[监控数据投递](../../raw/model-user-guide/model-monitoring/model-telemetry.md)中的云监控服务角色授权；
4. **查看用量**：进入[模型用量](https://bailian.console.aliyun.com/cn-beijing/costing-balance/usage-statistics)页面，选择模型类型页签（如“大语言模型”），按时间范围、API-Key 等筛选，支持分钟/小时/天粒度查看；
5. **开启推理日志**：需先开启审计日志投递 → 在日志页面切换至**推理日志**页签 → 点击**开始配置**完成 SLS 日志库授权与配置 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

## 限制和注意事项

- **数据延迟**：监控图表数据延迟约 **1 分钟**；模型用量统计延迟约 **1 小时**；审计日志查询最长支持 **30 天**；推理日志截断长度上限为 **128KB**；
- **权限隔离**：所有监控与用量数据严格按**业务空间**隔离，跨空间不可见；
- **告警限制**：
  - 仅预置告警模板所列指标（如失败率、TotalToken 数）可配置告警，`内容安全错误次数`、`RPM` 等不支持；
  - 告警检查周期最小为 **60 秒**（0 表示触发即告警，但不推荐）；
  - 创建告警规则前未授权云监控服务角色，按钮将置灰并提示 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)；
- **投递依赖**：
  - 推理日志开启**强依赖审计日志投递**；关闭审计日志投递将同步关闭推理日志投递；
  - 关闭日志投递后，**关闭期间日志无法补录**；
- **计费说明**：监控与日志功能本身免费，但开启数据投递（至云监控 Prometheus 或 SLS）将产生对应云产品费用；监控数据**不作为计费依据**，对账请以费用中心账单为准。

## 来源文档

- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)
- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)


