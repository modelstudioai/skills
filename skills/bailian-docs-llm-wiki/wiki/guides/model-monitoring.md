# model monitoring

百炼平台的 model monitoring 是面向生产环境的模型调用可观测性能力，提供分钟级延迟的用量统计、性能指标监控、失败诊断、告警配置及日志审计功能。所有数据按业务空间隔离，不跨空间聚合；监控数据仅作运维参考，计费以账单为准。核心能力覆盖用量追踪、健康度评估、异常告警与请求级排查，适用于模型服务稳定性保障与成本精细化管控。

## 支持的模型/功能

- **支持范围**：所有在[模型列表](raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)中可调用的模型（含调优后模型）均支持用量查看与基础监控；但语音、图片、视频生成及三方直连等部分模型**不支持监控告警功能**，具体需在控制台确认 [监控告警](raw/model-user-guide/model-monitoring/model-telemetry.md) 页面可用性。
- **核心功能模块**：
  - **用量统计**：按模型 Code、API-Key、时间粒度（分钟/小时/天）统计调用次数、[Token](../concepts/token.md) 数、图像张数、视频秒数等，详见[模型用量](raw/model-user-guide/model-monitoring/model-usage-statistics.md)；
  - **实时监控**：调用后分钟级可见调用次数、失败率、首 [Token](../concepts/token.md) 延时、调用时长等 14 项指标，支持图表化趋势分析；
  - **告警管理**：基于预置或自定义模板为关键指标（如失败率、Total[Token](../concepts/token.md) 数、429 次数）配置阈值告警；
  - **日志审计**：默认开启审计日志（含 Request ID、状态码、用量、延时），推理日志（含完整 Prompt/Response）需手动开启并投递至 SLS；
  - **数据投递**：支持将监控指标投递至云监控 Prometheus 实例，日志投递至 SLS 日志库，用于长期留存或对接自有运维系统。

> **注意**：文档 1 中称“所有模型均支持查看用量”，而文档 2 明确指出“语音、图片、视频生成及三方直连等部分模型不支持监控告警”。二者不矛盾——用量统计（文档 1）与监控告警（文档 2）是不同能力层，但需注意：**不支持监控告警的模型，其用量虽可查，但无法配置性能类告警或查看首 Token 延时等深度指标**。

## 关键参数

| 参数 | 说明 | 是否支持告警 | 来源 |
|------|------|--------------|------|
| `调用次数` / `调用量（Token总量）` | 总调用频次与 Token 消耗量 | ✅ | [监控告警](raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `失败率` | 失败次数 ÷ 总调用次数 | ✅ | [监控告警](raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `模型消耗 TotalToken 数` | 按模型维度统计的 Token 消耗总量（预置告警模板专用） | ✅ | [监控告警](raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `首 Token 延时` | 请求发起到首个 Token 返回的耗时 | ✅ | [监控告警](raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `限流错误次数（429）` | 触发限流的请求次数 | ✅ | [监控告警](raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `非首 Token 延时` | 首 Token 后每 Token 平均生成耗时 | ❌ | [监控告警](raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `RPM` / `TPM` | 每分钟请求数 / 每分钟 Token 数 | ❌ | [监控告警](raw/model-user-guide/model-monitoring/model-telemetry.md) |

## 使用方式

1. **访问入口**：
   - 用量统计：进入[模型用量](https://bailian.console.aliyun.com/cn-beijing/costing-balance/usage-statistics)页面，按模型类型页签（大语言模型、视觉模型等）筛选；
   - 监控告警：登录控制台 → **运维管理 > 模型监控**（[监控告警](raw/model-user-guide/model-monitoring/model-telemetry.md)）；
   - 告警规则：**运维管理 > 模型告警**（`https://bailian.console.aliyun.com/cn-beijing/model/alert`）；
   - 日志审计：模型监控详情页 → 点击「查看日志」。

2. **快速配置告警**：
   - 在模型监控详情页图表中，点击支持告警指标旁的蓝色铃铛图标，直接打开告警规则配置侧边面板；
   - 或前往告警页面，选择预置模板（如“模型调用失败占比1分钟总和大于1%”），填写模型、持续时间、通知对象后创建。

3. **开启推理日志**：
   - 先完成[日志投递](raw/model-user-guide/model-monitoring/model-telemetry.md)授权与 SLS 日志库配置；
   - 在日志页面切换至「推理日志」页签，点击「开始配置」启用；
   - 开启后，日志列表将显示 Prompt 与 Response（截断上限 128KB）。

4. **用量优化建议**（来自[模型用量](raw/model-user-guide/model-monitoring/model-usage-statistics.md)）：
   - 控制 `max_tokens` 限制输出长度；
   - 根据任务复杂度选用轻量级模型；
   - 优化 Prompt 减少冗余输入 Token；
   - 批量任务优先使用批量推理接口。

## 限制和注意事项

- **数据延迟与保留**：
  - 用量数据延迟约 **1 小时**，免费额度数据分钟级更新；
  - 审计日志最多查询 **30 天**内记录；
  - 不支持查看 **30 天以前**的用量统计数据，更早数据需通过[费用与成本](https://billing-cost.console.aliyun.com/finance/expense-report/expense-detail-by-instance)页面查询。

- **权限与依赖**：
  - 创建告警规则前，**必须先授权云监控服务角色**，否则按钮不可点击（见[监控告警](raw/model-user-guide/model-monitoring/model-telemetry.md)）；
  - 推理日志依赖审计日志投递，**关闭审计日志投递将同步关闭推理日志投递**；
  - 关闭日志投递后，期间产生的日志**无法补录复原**。

- **模型与指标限制**：
  - 部分模型（语音/视觉生成/三方直连）不支持监控告警，仅能查看用量；
  - “内容安全错误次数”“RPM”“TPM”等指标**不支持告警配置**，因未纳入预置告警模板；
  - 时间精度筛选仅在模型监控详情页提供，概览页不支持。

- **计费与对账**：
  - 监控数据**不作为计费依据**，对账请以[费用中心账单](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)为准；
  - 数据投递至云监控/Prometheus/SLS 会产生对应云产品费用，需确保账号已绑定有效支付方式。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


