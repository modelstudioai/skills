# model monitoring

百炼平台的 model monitoring 是面向生产环境的模型可观测性能力，提供分钟级延迟的调用统计、性能指标监控、告警配置及审计/推理日志能力。所有数据按业务空间维度隔离，不支持跨空间聚合；监控数据仅作运维参考，**不作为计费依据**，对账请以费用中心账单为准。核心能力覆盖用量追踪、健康度评估、异常告警与请求级排查，适用于模型上线后的稳定性保障与成本治理。

## 支持的模型/功能

- **支持范围**：所有在[模型列表](raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)中可调用的模型（含调优后模型）均支持基础监控与用量统计，但语音、图片、视频生成及三方直连等部分模型**不支持监控告警功能**，需在控制台实际确认 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) 页面可用性。
- **核心功能模块**：
  - **用量统计**：按模型 Code、API-Key、时间粒度（分钟/小时/天）展示调用次数、[Token](../concepts/token.md) 总量、图像张数、视频秒数等，单位详见[模型用量统计单位说明](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)；
  - **性能监控**：首 [Token](../concepts/token.md) 延时、调用时长、非首 [Token](../concepts/token.md) 延时、TPS 等实时指标；
  - **告警能力**：支持为调用次数、失败率、限流错误次数、模型消耗 TotalToken 数等关键指标配置阈值告警，依赖预置或自定义告警模板；
  - **日志能力**：审计日志（默认开启，含 Request ID、状态码、用量、延时，不含 Prompt/Response）；推理日志（需手动开启并配置日志投递，含完整 Prompt/Response，长度上限 128K）。

> **注意**：文档 1 中“[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)”提到“数据延迟约为 1 小时”，而文档 2 中“[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)”明确说明“调用发生后分钟级之后即可在监控图表查看”。二者存在时效性矛盾——**用量统计（计费口径）延迟约 1 小时，而监控指标（运维口径）延迟为分钟级**，开发者应据此区分使用场景：成本分析用用量页面，故障排查用监控页面。

## 关键参数

| 参数名 | 说明 | 是否必填 | 备注 |
|--------|------|----------|------|
| `时间范围` | 支持快捷选择（如最近 1h/24h）或自定义起止时间 | 是 | 用量页面不支持查询 30 天以前数据；审计日志最长支持 30 天查询 |
| `推理类型` | 仅「大语言模型」页签支持筛选「实时推理」或「批量推理」 | 否 | 若空间无批量推理数据，下拉框仅显示「实时推理」 |
| `API-Key` | 按 API Key ID 筛选调用来源 | 否 | 仅展示当前业务空间下已创建且未删除的 API-Key |
| `时间精度` | 分钟 / 小时 / 天 | 否 | 时间跨度 >1 天时不可选分钟；>7 天时仅支持按天 |
| `告警检查周期` | 默认 60 秒，单位为秒 | 是 | 必须为 ≥0 的整数；0 表示触发即告警 |

## 使用方式

1. **访问入口**：
   - 监控概览页：[百炼控制台 → 运维管理 → 模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)
   - 用量统计页：[模型用量](https://bailian.console.aliyun.com/cn-beijing/costing-balance/usage-statistics)
   - 告警规则页：[模型告警](https://bailian.console.aliyun.com/cn-beijing/model/alert)
   - 日志页：监控概览页 → 模型列表 → 「查看日志」

2. **快速配置告警**：
   - 在模型监控详情页，点击任一支持告警的指标（如「失败率」「模型消耗 TotalToken 数」）旁的蓝色铃铛图标；
   - 在弹出侧边面板中选择预置模板（如「模型调用失败占比1分钟总和大于1%」），填写通知对象、时段等后保存；
   - 或前往[告警页面](https://bailian.console.aliyun.com/cn-beijing/model/alert) → 「告警规则」页签 → 「创建告警规则」，手动配置。

3. **开启推理日志**：
   - 需先完成[日志投递](../../raw/model-user-guide/model-monitoring/model-telemetry.md)授权（日志服务角色 + SLS 日志库）；
   - 在日志页面切换至「推理日志」页签 → 点击「开始配置」→ 完成投递配置；
   - **警告**：关闭审计日志投递将同步关闭推理日志投递，且关闭期间日志无法补录。

## 限制和注意事项

- **数据隔离与延迟**：所有监控与用量数据严格按**业务空间**维度隔离，不支持阿里云账号级汇总；用量数据延迟约 1 小时，监控指标延迟为分钟级，二者不可混用作对账依据。
- **告警依赖前置授权**：创建告警规则前，必须在[监控数据投递](../../raw/model-user-guide/model-monitoring/model-telemetry.md)中完成**云监控服务角色授权**，否则按钮置灰并提示“未授权云监控服务角色”。
- **不支持告警的指标**：内容安全错误次数、RPM、TPM、平均单次请求调用量、非首 Token 延时等指标**不支持配置告警**，因其未纳入预置告警模板（见[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)指标说明表）。
- **日志存储与安全**：审计日志默认存储于百炼平台侧；推理日志需投递至自有 SLS 日志库，**禁止删除百炼创建的 SLS 日志库**，否则导致投递失败；SLS 侧不支持修改索引，修改将导致查询失败。
- **免费额度联动**：「免费额度用完即停」开关仅在仍有未消耗额度时可开启，关闭需待额度完全耗尽后操作；该功能与监控告警无直接关联，但建议为「模型消耗 TotalToken 数」配置环比突增告警，主动规避额度耗尽风险。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


