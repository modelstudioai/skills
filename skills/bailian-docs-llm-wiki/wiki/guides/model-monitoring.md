# model monitoring

百炼平台的 model monitoring 是面向生产环境的模型调用可观测性能力，提供分钟级延迟的实时监控、多维指标分析、告警配置及日志审计功能。它与模型用量统计（计费依据）分离，数据仅供运维排查与性能优化参考，不作为费用对账凭证。开发者可通过控制台一站式查看调用规模、健康度、性能瓶颈，并快速定位异常请求。

## 支持的模型/功能

- **覆盖范围**：所有在百炼模型列表中可选的模型均支持基础监控（调用次数、失败率、时延等），但语音、图像/视频生成及三方直连类模型的部分指标可能受限；具体支持情况需以[控制台实际展示](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)为准。  
- **核心功能模块**：  
  - **监控概览与详情**：按业务空间聚合的调用总量、失败次数、首 Token 延时、调用时长等实时图表；  
  - **审计日志**：默认开启，记录 Request ID、模型、Token 用量、状态码、延迟等元数据，**不包含 Prompt/Response 内容**；  
  - **推理日志**：需手动开启并完成日志投递配置，记录完整 Prompt/Response 及中间步骤（长度上限 128KB），仅支持北京和新加坡地域；  
  - **告警系统**：支持为关键指标（如失败率、限流错误次数、TotalToken 数）配置阈值告警，预置 12 条模板，详见[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  

> **注意**：文档 1 中提到“失败次数、失败率、限流错误次数已移至[模型监控](raw/model-user-guide/model-monitoring/model-telemetry.md)页面”，而文档 2 明确这些指标属于监控告警范畴；二者一致，但文档 1 的表述易被误解为“用量页面曾长期包含这些字段”，实际已于新版本下线——该迁移已在文档 2 中明确说明，应以[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)为准。

## 关键参数

| 参数名 | 说明 | 是否支持告警 | 来源文档 |
|--------|------|--------------|----------|
| `调用次数` | 模型被调用的总次数（含成功/失败） | ✅ | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `失败率` | 失败次数 / 总调用次数 | ✅ | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `首 Token 延时` | 请求发出到返回首个 Token 的耗时 | ✅ | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `调用时长` | 完整请求响应耗时（含[流式输出](../concepts/streaming-output.md)总时长） | ✅ | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `限流错误次数` | HTTP 429 触发次数 | ✅ | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `模型消耗 TotalToken 数` | 按模型维度统计的 Token 消耗总量（预置告警模板专用） | ✅ | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `缓存命中率` | 缓存命中 Token 数 / 输入 Token 数 | ❌ | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |

> **注意**：文档 1 中“模型用量”页面的 `Tokens 用量` 是计费口径（后付费模型），而文档 2 中 `模型消耗 TotalToken 数` 是监控口径（含所有调用类型），二者统计逻辑与延迟不同，不可混用。用量对账请严格使用[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)页面数据。

## 使用方式

1. **访问入口**：登录百炼控制台 → 左侧导航栏 **运维管理 > 模型监控**（[概览页](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)）。  
2. **筛选数据**：支持按时间（快捷/自定义）、推理类型（在线/批量离线/批量在线）、API Key（当前业务空间内已存在者）筛选。  
3. **查看详情**：  
   - 在概览页模型列表点击 **查看详情** 进入单模型监控页，查看调用统计与性能图表；  
   - 点击 **查看日志** 进入审计日志页签，支持按 Request ID、状态码（200/4XX/5XX）等过滤；  
4. **配置告警**：  
   - 在监控图表上点击告警铃铛图标，快速为当前指标创建规则；  
   - 或前往[模型告警页面](https://bailian.console.aliyun.com/cn-beijing/model/alert) → **告警规则**页签，使用预置模板（如“模型调用失败占比1分钟总和大于1%”）创建；  
5. **开启日志投递（可选）**：  
   - 推理日志依赖日志投递：需先授权 SLS 服务角色、开通日志服务、创建日志库；  
   - 监控数据投递至云监控 Prometheus 实例，需额外授权云监控服务角色（授权后自动开通相关产品）；  
   - 详细步骤见[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)中“数据投递”章节。

## 限制和注意事项

- **数据隔离与延迟**：监控数据按**业务空间**维度隔离，不支持跨空间或账号维度汇总；指标延迟约 1 分钟，日志查询最长支持 30 天（审计日志）。  
- **地域限制**：推理日志仅在北京、新加坡地域可用；美国（弗吉尼亚）地域在模型用量页面暂不展示调用次数。  
- **告警依赖条件**：创建告警规则前**必须完成云监控服务角色授权**，否则按钮禁用；未授权时鼠标悬停提示“未授权云监控服务角色，无法创建告警规则”。  
- **日志投递风险**：关闭审计日志投递将**同步关闭推理日志投递**；关闭期间日志**无法补录**，且 SLS 日志库被删除会导致投递永久失败。  
- **计费与监控分离**：监控数据（如失败率、首包延时）**不作为计费依据**，费用核对请以[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)和[费用中心](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)账单为准。  
- **模型兼容性**：语音、图片、视频生成及三方直连模型的部分监控指标可能不支持，需在控制台实际验证。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


