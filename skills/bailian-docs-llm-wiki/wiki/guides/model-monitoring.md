# model monitoring

百炼平台的 model monitoring 是面向生产环境的模型调用可观测性能力，提供分钟级延迟的实时监控、多维告警与审计/推理日志能力，覆盖调用规模、健康度、性能与安全拦截等核心维度。该能力按业务空间隔离，数据不跨空间共享，且监控指标（如失败率、首 Token 延时）与用量统计（如 Token 数、调用次数）分属不同系统，需结合使用以实现完整运维闭环。详细背景可参见 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) 和 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) 两篇原始文档。

## 支持的模型与功能

- **支持范围**：全部在模型列表中公开的模型（含调优后模型）均支持基础监控；但语音、图像/视频生成及三方直连类模型部分功能受限，具体支持情况需在控制台确认（详见 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。
- **核心功能模块**：
  - **监控概览与详情**：展示总调用次数、失败次数、失败率、调用时长、首 Token 延时等 15+ 指标，支持按时间、API Key、推理类型筛选；
  - **告警管理**：支持基于预置或自定义模板为关键指标（如失败率、429 次数、TotalToken 数）配置阈值告警，告警规则统一纳管于 [模型告警页面](https://bailian.console.aliyun.com/cn-beijing/model/alert)；
  - **日志能力**：默认开启**审计日志**（含 Request ID、状态码、Token 用量、延时等，不含 Prompt/Response）；**推理日志**（含完整 Prompt/Response 与中间步骤）需手动开启，且仅在北京、新加坡地域可用；
  - **数据投递**：支持将监控指标投递至云监控 Prometheus 实例，将审计/推理日志投递至 SLS 日志库，用于长期留存或对接自有运维系统。

> **注意**：文档 1 中提到“失败次数、失败率、限流错误次数和内容安全拦截次数已移至[模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)页面”，而文档 2 明确说明这些指标属于监控范畴且支持告警；但文档 1 的“模型用量”页面已不再展示它们——这表明用量统计（计费导向）与监控（运维导向）已彻底分离，开发者应以 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) 为准进行异常排查。

## 关键参数

| 参数名 | 说明 | 是否支持告警 | 备注 |
|--------|------|--------------|------|
| `失败率` | 失败次数 / 总调用次数 | ✅ | 推荐为关键服务配置 `>1%` 告警（参考预置模板） |
| `模型消耗 TotalToken 数` | 按模型维度聚合的 Token 消耗总量 | ✅ | 控制成本的核心指标，推荐配置环比突增告警（见 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)） |
| `首 Token 延时` | 请求到首个 Token 返回的耗时 | ✅ | 衡量模型响应启动性能，典型阈值建议 `<10s` |
| `调用时长` | 完整请求-响应耗时 | ✅ | 用于识别整体性能退化，建议结合首 Token 延时交叉分析 |
| `限流错误次数（429）` | 触发限流的调用次数 | ✅ | 直接反映配额瓶颈，需联动 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) 查看 RPM/TPM 实际占用 |
| `内容安全错误次数` | 被内容安全策略拦截的次数 | ❌ | 仅展示，不可配置告警；需结合审计日志排查违规输入 |

## 使用方式

1. **访问入口**：
   - 监控概览页：[百炼控制台 → 运维管理 → 模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)
   - 告警管理页：[百炼控制台 → 运维管理 → 模型告警](https://bailian.console.aliyun.com/cn-beijing/model/alert)
   - 日志页面：在监控概览页点击任一模型的“查看日志”进入

2. **快速配置告警**：
   - 在模型监控详情页图表中，点击支持告警指标旁的蓝色铃铛图标 → 填写告警名称、选择预置模板（如“模型调用失败占比1分钟总和大于1%”）、配置通知对象与时段 → 创建完成；
   - 首次使用前需在[监控数据投递](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)中授权云监控服务角色（否则按钮置灰）。

3. **启用推理日志**：
   - 进入日志页面 → 切换至“推理日志”页签 → 点击“开始配置” → 完成 SLS 角色授权、开通日志服务、创建日志库三步；
   - **注意**：推理日志依赖审计日志投递，且仅北京/新加坡地域可用（见 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。

## 限制和注意事项

- **数据时效性**：监控数据延迟约 1 分钟（调用次数）至 10 分钟（Token 用量）；审计日志查询最长支持 30 天，推理日志依赖 SLS 配置的存储周期。
- **地域与时间限制**：
  - 模型用量数据仅支持查询 **2026 年 9 月及之后**的数据（更早数据需查账单）；美国（弗吉尼亚）地域的调用次数仅支持 **2026 年 10 月及之后**（见 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）；
  - 推理日志仅在北京、新加坡地域可用，其他地域开启后显示“当前模型不支持”。
- **权限与隔离**：所有监控、告警、日志数据严格按**业务空间**维度隔离，不支持跨空间或按阿里云账号维度汇总。
- **告警依赖项**：创建告警规则前必须完成云监控服务角色授权，否则无法创建；授权后将自动开通云监控、SLS 及 Prometheus 服务，相关费用按实际用量收取。
- **日志投递风险**：关闭审计日志投递将**同步关闭推理日志投递**；关闭期间产生的日志**无法补录**至 SLS（见 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。
- **免费额度联动**：“免费额度用完即停”功能开启后，服务将在额度耗尽时返回 `403 AllocationQuota.FreeTierOnly` 错误，此时监控中会集中出现失败率飙升，需与 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) 中的免费额度剩余量联动判断。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


