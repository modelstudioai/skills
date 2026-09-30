# model monitoring

百炼平台提供面向生产环境的模型调用可观测能力，覆盖分钟级监控指标、审计日志、推理日志及告警配置，帮助开发者快速定位性能退化、失败突增、限流异常等典型问题。监控数据按业务空间隔离，不作为计费依据；用量统计与费用数据需通过[费用中心](https://bailian.console.aliyun.com/cn-beijing/costing-balance/overview)单独查看。所有功能均需在百炼控制台对应页面操作，无需额外部署。

## 支持的模型与功能

- **支持模型范围**：所有在模型列表中可见的模型（含调优后模型）均支持基础监控与用量统计，但语音、图片、视频生成及三方直连类模型部分不支持监控告警，具体以控制台实时展示为准（详见 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。
- **核心功能模块**：
  - **监控概览与详情**：展示调用次数、失败率、首 Token 延时、调用时长、TotalToken 消耗等 14 项指标，支持按时间、推理类型、API-Key 筛选；
  - **审计日志**：默认开启，记录 Request ID、状态码、Token 用量、延迟等元数据，**不包含 Prompt/Response**；
  - **推理日志**：需手动开启，记录完整 Prompt/Response 及中间步骤（截断上限 128K），依赖日志投递至 SLS；
  - **告警管理**：支持基于预置或自定义模板为指定指标配置规则，触发后推送至联系人/组；
  - **数据投递**：监控数据可投递至云监控 Prometheus 实例；日志可投递至 SLS 日志库（审计日志投递是推理日志开启前提）。

> **注意**：文档 2 中“模型用量”页面描述的数据延迟为“约 1 小时”，而文档 1 明确说明“模型监控数据按分钟级之后即可在监控图表查看”。二者统计目的不同（用量用于计费对账，监控用于实时运维），但存在口径混淆风险——**监控图表中的“调用次数”“失败次数”等指标为分钟级延迟，而用量统计页的“Token总量”等字段为小时级延迟**，不可混用作实时决策依据。

## 关键参数

| 参数 | 说明 | 是否支持告警 | 来源文档 |
|------|------|--------------|----------|
| `失败率` | 失败次数 / 总调用次数 | ✅ | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `首 Token 延时` | 请求发起到返回首个 Token 的耗时 | ✅ | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `调用时长` | 完整请求响应耗时 | ✅ | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `模型消耗 TotalToken 数` | 模型维度 Token 消耗总量（预置告警模板专用） | ✅ | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `限流错误次数`（429） | 触发限流的请求次数 | ✅ | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `非首 Token 延时` | 首 Token 后每 Token 平均生成耗时 | ❌ | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `RPM` / `TPM` | 每分钟请求数 / Token 数 | ❌ | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |

## 使用方式

1. **访问入口**：
   - 监控概览页：[百炼控制台 → 运维管理 → 模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)
   - 告警配置页：[百炼控制台 → 运维管理 → 模型告警](https://bailian.console.aliyun.com/cn-beijing/model/alert)
   - 用量统计页：[百炼控制台 → 费用与成本 → 模型用量](https://bailian.console.aliyun.com/cn-beijing/costing-balance/usage-statistics)

2. **快速配置告警**：
   - 在模型监控详情页图表中点击指标旁的蓝色/灰色告警铃铛 → 填写规则名称、选择预置模板（如“模型调用失败占比1分钟总和大于1%”）、设置持续时间与通知对象 → 创建完成；
   - **首次使用前必须完成云监控服务角色授权**（见 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) 中“数据投递”章节）。

3. **开启推理日志**：
   - 先在日志页面开启**审计日志投递**（授权 SLS 角色 + 创建日志库）；
   - 切换至“推理日志”页签 → 点击“开始配置” → 复用已有 SLS 配置 → 完成后即可查询带 Prompt/Response 的日志。

## 限制和注意事项

- **数据时效性差异**：监控图表数据延迟约 **1–3 分钟**；用量统计页数据延迟约 **1 小时**；审计日志查询最长支持 **30 天**，推理日志依赖 SLS 保留策略。
- **模型兼容性限制**：语音、图片、视频生成及三方直连模型**不支持监控告警功能**，控制台对应模型行将隐藏“查看详情”入口（见 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。
- **投递依赖关系**：
  - 推理日志开启**强依赖审计日志投递**；关闭审计日志投递将自动关闭推理日志投递；
  - 关闭日志投递后，**停用期间日志无法补录**，SLS 中无对应数据。
- **告警能力边界**：
  - 仅预置模板所列指标（如失败率、TotalToken 数）支持一键配置；`内容安全错误次数`、`RPM` 等未出现在预置模板中的指标**无法配置告警**；
  - 告警检查周期最小为 **60 秒**（0 表示“触发即告警”，但实际受数据采集延迟影响）。
- **用量与监控分离**：监控指标（如“调用次数”）用于运维健康度判断，**不作为计费依据**；计费以费用中心账单为准（见 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）。

## 来源文档

- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)
- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)


