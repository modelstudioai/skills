# model monitoring

百炼平台的模型监控（Model Monitoring）是一套面向生产环境的可观测性能力，提供分钟级延迟的调用统计、性能指标、审计日志及告警能力，帮助开发者实时掌握模型服务健康度、排查异常、控制成本并保障 SLA。监控数据按业务空间隔离，不作为计费依据；用量与费用请以[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)和费用中心为准。核心能力覆盖调用规模、失败分析、延迟诊断、[Token](../concepts/token.md) 消耗追踪及可配置告警。

## 支持的模型与功能

- **支持范围**：全部百炼平台托管模型（含调优后模型）均支持基础监控指标（如调用次数、失败率、调用时长、首 [Token](../concepts/token.md) 延时），但语音、图像/视频生成及三方直连类模型部分指标可能受限，具体以控制台实际展示为准 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  
- **核心功能模块**：
  - **监控概览与详情**：按业务空间聚合总调用、失败、延时等卡片，支持下钻至单模型维度查看趋势图表；
  - **审计日志**：默认开启，记录 Request ID、模型、[Token](../concepts/token.md) 用量、状态码、首包延时等元数据，**不包含 Prompt/Response 内容**；
  - **推理日志**：需手动开启，记录完整 Prompt/Response 及中间步骤（长度上限 128KB），仅支持北京、新加坡地域 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)；
  - **告警系统**：支持基于预置或自定义模板为关键指标配置实时告警，如失败率突增、TotalToken 数环比激增等；
  - **数据投递**：可将监控指标投递至云监控 Prometheus 实例，或将审计/推理日志投递至 SLS 日志库，用于长期留存或对接自有运维体系。

> **注意**：文档 1 中“失败次数、失败率、限流错误次数和内容安全拦截次数已移至[模型监控](raw/model-user-guide/model-monitoring/model-telemetry.md)页面”与文档 2 的实际功能一致，但文档 1 的标题“模型用量”易引发歧义——其内容实为用量统计（计费导向），而文档 2 的“监控告警”才是真正的运行时可观测性系统。二者定位不同，不可混用。

## 关键参数

| 参数名 | 说明 | 是否支持告警 | 来源 |
|--------|------|--------------|------|
| `调用次数` | 模型被成功/失败调用的总次数 | ✅ | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `失败次数` / `失败率` | 失败请求计数及占比（失败次数 ÷ 总次数） | ✅ | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `调用时长` | 请求端到端耗时（含网络+排队+模型推理） | ✅ | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `首 Token 延时` | 首个 Token 返回耗时（关键性能指标） | ✅ | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `模型消耗 TotalToken 数` | 按模型维度汇总的 Token 消耗总量（预置告警模板专用） | ✅ | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `限流错误次数`（429） | 触发配额限流的次数 | ✅ | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `内容安全错误次数` | 被内容安全策略拦截的次数 | ❌ | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `非首 Token 延时` | 后续 Token 平均生成耗时 | ❌ | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |

> **注意**：是否支持告警取决于预置告警模板是否包含该指标；未在预置模板中的指标（如 `RPM`、`TPM`、`内容安全错误次数`）无法配置告警，控制台图表中不显示告警铃铛图标。

## 使用方式

1. **访问入口**：登录百炼控制台 → 左侧导航栏 **运维管理 > 模型监控**（[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。
2. **查看监控**：
   - 概览页查看整体调用规模与健康度（总调用、失败率、平均首包延时等）；
   - 在模型列表点击 **查看详情** 进入单模型监控详情页，筛选时间、推理类型、API Key；
   - 点击 **查看日志** 进入审计日志页签（默认开启），或切换至推理日志页签（需先开启投递）。
3. **配置告警**：
   - 在监控详情页图表上点击告警铃铛图标，快速为当前指标创建规则；
   - 或进入 **[模型告警页面](https://bailian.console.aliyun.com/cn-beijing/model/alert)** → **告警规则** 页签，使用预置模板（如“模型调用失败占比1分钟总和大于1%”）创建规则；
   - **前提**：必须先完成[监控数据投递](../../raw/model-user-guide/model-monitoring/model-telemetry.md)中的云监控服务角色授权。
4. **开启日志投递**：
   - 审计日志投递：在日志页面右上角点击 **日志投递配置** → 授权日志服务角色 + 创建 SLS 日志库；
   - 推理日志投递：需先开启审计日志投递，再在推理日志页签点击 **开始配置**；
   - 投递后日志将写入用户自有 SLS 日志库，可用于回流训练数据集 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

## 限制和注意事项

- **数据时效性**：监控数据延迟约 1 分钟（调用次数）至 10 分钟（Token 用量）；审计日志查询最长支持 30 天，推理日志依赖 SLS 保留策略。
- **地域与时间限制**：
  - 模型用量数据仅支持查询 **2026 年 9 月及之后**的数据（美国弗吉尼亚地域为 2026 年 10 月起）[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)；
  - 推理日志仅在北京、新加坡地域可用，其他地域暂不支持 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
- **权限与隔离**：所有监控、日志、告警数据严格按 **业务空间** 维度隔离，不支持跨空间或按阿里云账号维度聚合。
- **费用与依赖**：
  - 告警规则本身免费，但启用监控数据投递会自动开通云监控、SLS、Prometheus 服务，按实际用量计费；
  - 关闭审计日志投递将**同步关闭推理日志投递**，且关闭期间日志**不可补录**；
  - SLS 日志库不可删除，否则导致投递失败；索引不可修改，否则查询失败。
- **模型兼容性**：语音、图片/视频生成、三方直连模型的部分监控指标（如首 Token 延时）可能不适用或缺失，需以控制台实际展示为准 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


