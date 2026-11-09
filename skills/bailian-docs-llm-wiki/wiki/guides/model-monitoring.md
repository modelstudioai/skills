# model monitoring

百炼平台的 model monitoring 是面向生产环境的模型可观测性能力，提供分钟级延迟的调用统计、性能指标、审计日志及告警配置，帮助开发者实时掌握模型健康度、排查异常并控制成本。监控数据按业务空间隔离，不作为计费依据；用量与费用核对请以[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)和账单为准。核心能力覆盖调用规模、失败分析、延迟诊断、安全拦截与限流识别等场景。

## 支持的模型/功能

- **支持范围**：全部在模型列表中可见的官方模型（含文本、视觉、语音、全模态、向量模型）及其[调优后的模型](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)，但语音、图片、视频生成及三方直连等部分模型**不支持监控与告警**，具体需在控制台确认（见[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)说明）。
- **核心功能模块**：
  - **监控概览与详情**：总调用次数、失败率、首 [Token](../concepts/token.md) 延时、调用时长、限流错误次数（429）、内容安全拦截次数等；
  - **审计日志**：默认开启，记录 Request ID、模型、[Token](../concepts/token.md) 用量、状态码、延迟等，**不含 Prompt/Response**；
  - **推理日志**：需手动开启，记录完整 Prompt/Response 与中间步骤，仅支持北京和新加坡地域；
  - **告警配置**：支持为关键指标（如失败率、Total[Token](../concepts/token.md) 数、429 次数）创建规则，依赖[数据投递](../../raw/model-user-guide/model-monitoring/model-telemetry.md)授权云监控服务角色；
  - **数据投递**：监控指标可投递至云监控 Prometheus 实例；日志可投递至 SLS 日志库（审计日志投递是开启推理日志的前提）。

> **注意**：文档 1 中“失败次数、失败率、限流错误次数和内容安全拦截次数已移至[模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)页面”与文档 2 的实际功能一致；但文档 1 提到“批量离线推理和批量在线推理不展示调用次数”，而文档 2 的监控详情页明确支持按“推理类型”（含 Batch File / Batch Chat）筛选，且指标表中“调用次数”列为“可配置告警”，表明**批量推理的调用次数已被纳入监控体系**，文档 1 此处描述已过时。

## 关键参数

| 参数名 | 含义 | 是否支持告警 | 说明 |
|--------|------|----------------|------|
| `调用次数` | 模型被调用的总次数 | ✅ | 包含预置吞吐单元、独占吞吐单元等调用（见[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)） |
| `失败次数` / `失败率` | 调用失败次数及占比 | ✅ | 排查突增应重点关注；失败率告警推荐阈值 ≥1%（见预置模板） |
| `模型消耗 TotalToken 数` | 按模型维度统计的 Token 消耗总量 | ✅ | **控制 Token 成本的核心指标**，推荐配置环比突增告警（见[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)） |
| `首 Token 延时` | 请求发起到返回首个 Token 的延时 | ✅ | 性能退化关键指标，预置模板建议阈值 >10 秒 |
| `限流错误次数`（429） | 触发限流的次数 | ✅ | 预置模板支持“1 分钟总和大于 10”等条件 |
| `内容安全错误次数` | 内容安全拦截次数 | ❌ | 不支持告警，仅用于审计日志排查 |
| `非首 Token 延时` | 首 Token 后每 Token 平均耗时 | ❌ | 仅展示，不可配置告警 |

## 使用方式

1. **访问入口**：登录百炼控制台 → 左侧导航栏 **运维管理 > 模型监控**（[概览页](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)）。
2. **快速查看**：
   - 概览页查看整体调用规模与健康度（总调用、失败率、平均时长等）；
   - 模型列表点击 **查看详情** 进入单模型监控详情页（支持按时间、推理类型、API Key 筛选）；
   - 点击 **查看日志** 进入审计日志页签（默认开启）或推理日志页签（需手动配置）。
3. **配置告警**：
   - 在监控图表上点击 **告警铃铛**（仅支持告警的指标显示）快速创建规则；
   - 或进入 [模型告警页面](https://bailian.console.aliyun.com/cn-beijing/model/alert) → **告警规则** 页签，使用预置模板（如“模型调用失败占比1分钟总和大于1%”）创建；
   - **前提**：必须先在[数据投递](../../raw/model-user-guide/model-monitoring/model-telemetry.md)中授权云监控服务角色（否则创建按钮禁用）。
4. **开启推理日志**：
   - 进入日志页面 → 切换至 **推理日志** 页签 → 点击 **开始配置**；
   - 需先完成审计日志投递授权，并确保地域为北京或新加坡。

## 限制和注意事项

- **数据延迟与范围**：监控数据分钟级更新，**不作为计费依据**；用量与费用请以[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)和账单为准。用量页面仅支持查询 2026 年 9 月 1 日及之后数据；告警历史 2026 年 9 月 3 日前需查云监控控制台。
- **地域限制**：推理日志仅支持北京、新加坡地域；美国（弗吉尼亚）地域在[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)中暂不展示调用次数（但监控详情页仍可查）。
- **权限与依赖**：
  - 告警依赖云监控服务角色授权，授权后将自动开通云监控、SLS 及 Prometheus（按量计费）；
  - 推理日志依赖审计日志投递，**关闭审计日志投递将同步关闭推理日志投递**；
  - SLS 日志库禁止删除或修改索引，否则导致投递失败。
- **免费额度联动**：监控本身不控制额度，但可配合[免费额度用完即停](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)功能规避超支——该开关仅在仍有未消耗额度时可开启，关闭需待额度完全耗尽后操作。
- **批量操作限制**：阿里云 App **暂不支持**查看免费额度与模型用量（见[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)常见问题），所有监控与告警配置必须通过 PC 端控制台完成。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


