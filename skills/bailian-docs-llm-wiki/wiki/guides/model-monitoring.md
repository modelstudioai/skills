# model monitoring

百炼平台的 model monitoring 是面向生产环境的模型可观测性能力，提供分钟级延迟的调用统计、性能指标监控、告警配置及审计/推理日志能力，帮助开发者实时掌握模型健康度、排查异常并控制成本。该能力按业务空间隔离，数据不跨空间共享，且监控数据仅作参考，**不作为计费依据**（计费以费用中心账单为准）[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

## 支持的模型与功能

- **支持范围**：所有在百炼模型列表中可调用的模型（含基于其调优后的模型）均支持用量查看与基础监控 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)；但**语音、图片、视频生成及三方直连等部分模型不支持监控告警功能**，具体需以控制台实际展示为准 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
- **核心功能模块**：
  - **用量统计**：按模型 Code、API-Key、时间维度（分钟/小时/天）查看 [Token](../concepts/token.md)、图像张数、视频秒数等模态化用量；
  - **实时监控**：调用次数、失败率、首 [Token](../concepts/token.md) 延时、调用时长、限流错误次数等 14+ 指标，图表化呈现；
  - **告警管理**：支持基于预置或自定义模板为关键指标（如失败率、Total[Token](../concepts/token.md) 数、429 次数）配置阈值告警；
  - **日志能力**：审计日志（默认开启，含 Request ID、状态码、Token 用量等）与推理日志（需手动开启，含完整 Prompt/Response，最大 128KB）；
  - **数据投递**：可将监控指标投递至云监控 Prometheus 实例，或将日志投递至 SLS 日志库（用于长期留存或对接自有运维系统）。

> **注意**：文档 1 中称“所有模型均支持查看用量”，而文档 2 明确指出“语音、图片、视频生成及三方直连等部分模型不支持监控告警”。二者无矛盾——**用量统计（计量）与监控告警（可观测性）是两个独立能力层**，前者覆盖更广，后者有模型兼容性限制。

## 关键参数

| 参数类别 | 参数名 | 说明 | 是否支持告警 | 来源 |
|----------|--------|------|----------------|------|
| 调用统计 | 调用次数 / 失败次数 / 失败率 | 总调用、失败绝对值及比率 | ✅ | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| 性能指标 | 首 Token 延时 / 调用时长 | 首包延时（TTFT）、端到端耗时（E2E） | ✅ | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| 成本指标 | 模型消耗 TotalToken 数 | 按模型维度聚合的 Token 消耗总量（预置告警专用） | ✅ | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| 限流安全 | 限流错误次数（429） / 内容安全错误次数 | 触发限流或内容拦截的请求计数 | ✅（429） / ❌（内容安全） | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| 用量单位 | Token / 张 / 秒 / 字符 | 不同模型类型对应不同计费单位（见[模型用量统计单位说明](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)） | — | [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) |

## 使用方式

1. **访问入口**：
   - 用量统计：控制台 → [模型用量](https://bailian.console.aliyun.com/cn-beijing/costing-balance/usage-statistics)
   - 监控告警：控制台 → 运维管理 → [模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)
   - 告警规则：控制台 → 运维管理 → [模型告警](https://bailian.console.aliyun.com/cn-beijing/model/alert)
   - 日志：模型监控详情页 → 「查看日志」或「日志」页签

2. **快速配置告警**：
   - 在模型监控详情页图表中，点击支持告警的指标（如失败率、TotalToken 数）旁的蓝色铃铛图标；
   - 选择预置模板（如“模型调用失败占比1分钟总和大于1%”），填写通知对象、时段、重复策略后保存；
   - **首次使用前必须完成云监控服务角色授权**（否则创建按钮禁用）[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

3. **开启推理日志**：
   - 先确保已开启审计日志投递；
   - 进入日志页面 → 切换至「推理日志」页签 → 点击「开始配置」完成 SLS 授权与日志库绑定；
   - 开启后，日志将包含完整 Prompt/Response（截断上限 128KB）[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

## 限制和注意事项

- **数据延迟与保留**：
  - 用量统计延迟约 **1 小时**；监控图表数据延迟 **分钟级**；
  - 审计日志最多查询 **最近 30 天**；告警历史仅保留 **2026年9月3日之后** 的记录（此前需查云监控）；
  - 不支持查看 **30 天以前** 的用量统计数据，更早数据需通过费用中心账单查询 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

- **权限与依赖**：
  - 告警功能强依赖云监控服务角色授权，未授权则无法创建规则；
  - 推理日志开启前提为审计日志投递已启用，且关闭审计投递将**自动关闭推理日志投递**；
  - 数据投递至 SLS 后，**禁止删除百炼创建的日志库**，否则导致投递失败。

- **模型兼容性**：
  - 免费额度管理、用量统计覆盖全部模型；
  - 监控告警、推理日志等功能**不支持语音/图片/视频生成及三方直连模型**，控制台中对应模型将不显示监控入口或提示“不支持”。

- **其他重要约束**：
  - 监控数据**不作为计费依据**，对账请以费用中心账单为准；
  - “免费额度用完即停”功能**仅可在仍有未消耗额度时开启**，关闭操作需待额度完全耗尽后方可执行 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)；
  - 批量推理场景下，仅「大语言模型」页签支持按推理类型（实时/批量）筛选，其余模型类型不区分。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


