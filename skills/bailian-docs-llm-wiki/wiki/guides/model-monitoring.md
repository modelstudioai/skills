# model monitoring

百炼平台的模型监控（model monitoring）是一套面向生产环境的可观测性能力，提供分钟级延迟的调用统计、性能指标、审计日志及告警配置能力，帮助开发者实时掌握模型服务健康度、用量趋势与异常行为。监控数据按业务空间隔离，不作为计费依据，对账请以费用中心账单为准。核心能力覆盖用量观测、失败排查、延迟分析与成本控制，适用于所有已接入百炼平台的模型服务。

## 支持的模型/功能

- **支持范围**：模型列表中的所有官方模型（含大语言模型、视觉模型、语音模型、全模态模型、向量模型）均支持基础监控与用量统计；但[语音、图片、视频生成及三方直连等部分模型不支持监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
- **核心功能**：
  - **用量统计**：按模型 Code、API-Key、推理类型（实时/批量）维度查看调用次数、[Token](../concepts/token.md)/张/秒等单位用量，数据延迟约 1 小时 [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。
  - **性能监控**：首 [Token](../concepts/token.md) 延时、调用时长、非首 [Token](../concepts/token.md) 延时、TPM/RPM 等指标，支持图表化趋势分析。
  - **告警管理**：支持为调用次数、失败率、限流错误次数、模型消耗 TotalToken 数等关键指标配置阈值告警，可复用预置模板或自定义规则 [监控告警 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
  - **日志能力**：默认开启审计日志（含 Request ID、状态码、用量、延迟），推理日志（含完整 Prompt/Response）需手动开启并配置日志投递。

> **注意**：文档 1 中称“所有模型均支持查看用量”，而文档 2 明确指出“语音、图片、视频生成及三方直连等部分模型不支持监控告警”。二者口径不一致——用量统计（文档 1）与监控告警（文档 2）是两个不同能力层，前者覆盖更广，后者存在模型限制。实际使用中，应以控制台模型详情页的「监控」标签是否可见为准。

## 关键参数

| 参数名 | 说明 | 是否支持告警 | 来源 |
|--------|------|--------------|------|
| `调用次数` | 模型被调用总次数 | ✅ | [监控告警 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `失败率` | 失败次数 / 总次数 | ✅ | 同上 |
| `限流错误次数`（429） | 触发限流的请求次数 | ✅ | 同上 |
| `模型消耗 TotalToken 数` | 按模型维度统计的 Token 消耗总量（预置告警模板专用） | ✅ | 同上 |
| `首 Token 延时` | 请求到首个 Token 返回的耗时 | ✅ | 同上 |
| `调用时长` | 完整请求响应耗时 | ✅ | 同上 |
| `平均单次请求调用量` | 每次请求平均 Token 数 | ❌ | 同上 |
| `RPM` / `TPM` | 每分钟请求数 / Token 数 | ❌ | 同上 |

- 所有告警指标的统计周期最小为 1 分钟，持续时间、检查周期需按分钟/秒显式配置；
- 告警阈值支持 `>`, `>=`, `<`, `<=`, `==`, `!=` 六种比较方式；
- 推理日志内容长度上限为 128KB，超长部分自动截断。

## 使用方式

1. **访问入口**：登录百炼控制台 → 左侧导航栏 **运维管理 > 模型监控**（概览页）或 **运维管理 > 模型告警**；
2. **用量查看**：在[模型用量](https://bailian.console.aliyun.com/cn-beijing/costing-balance/usage-statistics)页面，按模型类型页签（如「大语言模型」）、时间范围、API-Key 筛选，支持分钟/小时/天精度；
3. **监控详情**：在概览页模型列表点击「查看详情」，进入单模型监控页，图表支持按时间精度、推理类型、API-Key 动态筛选；
4. **快速告警配置**：在监控图表中点击指标旁的蓝色/灰色告警铃铛，直接为当前模型+当前指标创建告警规则；
5. **日志排查**：
   - 审计日志：默认开启，支持按 Request ID、状态码（200/4XX/5XX）、时间范围（最长 30 天）筛选；
   - 推理日志：需先完成[日志投递](../../raw/model-user-guide/model-monitoring/model-telemetry.md)配置（授权 SLS 角色 + 创建日志库），再在日志页签开启；
6. **告警规则管理**：在[模型告警页面](https://bailian.console.aliyun.com/cn-beijing/model/alert)的「告警规则」页签统一创建、编辑、停止或迁移规则；首次使用需先完成[监控数据投递](../../raw/model-user-guide/model-monitoring/model-telemetry.md)的云监控角色授权。

## 限制和注意事项

- **数据延迟与保留**：监控数据延迟约 1 小时；用量统计不支持查询 30 天以前数据；审计日志最多查询最近 30 天；告警历史仅保留 2026 年 9 月 3 日之后记录，此前数据需前往[云监控控制台](https://cloudmonitor.console.aliyun.com/)查看。
- **权限与依赖**：
  - 告警功能依赖云监控服务角色授权，未授权时「创建告警规则」按钮不可用；
  - 推理日志依赖审计日志投递开启，关闭审计日志投递将同步关闭推理日志投递；
  - 开启日志投递或监控投递将自动开通阿里云日志服务（SLS）、云监控及 Prometheus，相关资源按实际用量计费。
- **模型差异**：
  - 免费额度「用完即停」功能仅在账户仍有未消耗额度时可开启，关闭需待额度完全耗尽后操作；
  - 不同模型用量单位不同（Token/张/秒/字符），详见[模型用量统计单位说明](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)；
- **安全与合规**：审计日志不包含 Prompt/Response 内容；推理日志含完整输入输出，需确保投递目标日志库符合数据安全策略；
- **费用控制建议**：为 `模型消耗 TotalToken 数` 配置环比突增告警，为 `调用失败率` 配置可用性告警，并结合 `max_tokens` 限制与模型选型优化成本 [模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


