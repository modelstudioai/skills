# model monitoring

模型监控是百炼平台提供的核心可观测性能力，用于实时掌握模型调用健康度、性能表现与资源消耗。数据在调用发生后分钟级即可在控制台呈现，支持按业务空间隔离查看，所有监控指标均不作为计费依据（对账请以[费用中心](https://bailian.console.aliyun.com/cn-beijing/costing-balance/overview)为准）。该功能面向运维与开发人员，聚焦问题定位、成本管控与服务稳定性保障。

## 支持的模型与功能

- **支持范围**：文本生成、深度思考、视觉理解、全模态、向量等主流大模型及调优后模型；语音、图片、视频生成及三方直连等部分模型**不支持**监控与告警，具体以控制台实际展示为准（详见[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。
- **核心功能模块**：
  - **监控概览与详情**：提供整体调用规模（总次数、失败次数）、健康度（失败率）、性能（调用时长、首 [Token](../concepts/token.md) 延时）等实时图表；
  - **审计日志**：默认开启，记录 Request ID、状态码、[Token](../concepts/token.md) 用量、延迟等元数据，**不含 Prompt/Response**；
  - **推理日志**：需手动开启，记录完整 Prompt/Response 及中间步骤，依赖日志投递至 SLS，仅支持北京和新加坡地域（详见[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）；
  - **告警管理**：支持基于预置或自定义模板为关键指标配置告警规则，并通过云监控通知渠道触达；
  - **数据投递**：可将监控指标投递至云监控 Prometheus 实例，将审计/推理日志投递至 SLS 日志库，用于长期留存或对接自有运维系统。

> **注意**：文档 2 中提到“失败次数、失败率、限流错误次数和内容安全拦截次数已移至[模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)页面”，与文档 1 的指标分类完全一致，确认该迁移已完成，模型用量页面不再提供这些运行时异常指标。

## 关键参数与指标

| 指标名称 | 含义 | 是否支持告警 | 说明 |
|----------|------|----------------|------|
| 调用次数 | 模型被调用的总次数 | ✅ | 随业务波动，可用于容量规划 |
| 失败次数 / 失败率 | 调用失败次数及占比 | ✅ | **排查失败突增的首要指标**（见[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)） |
| 调用时长 | 请求到响应的总耗时 | ✅ | 端到端延迟，含网络与模型推理 |
| 首 [Token](../concepts/token.md) 延时 | 请求发起到返回首个 Token 的延时 | ✅ | **排查首包性能退化的关键指标**（见[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)） |
| 模型消耗 TotalToken 数 | 按模型维度统计的 Token 消耗总量 | ✅ | **推荐配置环比突增告警以控制 Token 成本**（见[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)） |
| 限流错误次数（429） | 触发限流的次数 | ✅ | 直接反映配额瓶颈 |
| 非首 Token 延时 / RPM / TPM / 缓存命中率等 | 详见文档 1 表格 | ❌ | 不在预置告警模板中，无法配置告警 |

## 使用方式

1. **访问入口**：登录[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)，左侧导航栏选择 **运维管理 > 模型监控** 进入概览页。
2. **快速配置告警**：
   - 在模型监控详情页的指标图表上，点击蓝色/红色告警铃铛图标，直接为当前模型+当前指标创建规则；
   - 或前往[模型告警页面](https://bailian.console.aliyun.com/cn-beijing/model/alert)，在“告警规则”页签中使用预置模板（如“模型调用失败占比1分钟总和大于1%”）批量创建。
3. **开启日志**：
   - 审计日志：默认开启，无需配置；
   - 推理日志：需先完成[日志投递](../../raw/model-user-guide/model-monitoring/model-telemetry.md)授权与 SLS 日志库配置，再在日志页面切换至“推理日志”页签并点击“开始配置”。
4. **数据投递**：
   - 监控投递：需在模型监控概览页左上方完成**云监控服务角色授权**（否则告警创建按钮禁用），授权后自动开通云监控与 Prometheus；
   - 日志投递：需在日志页面右上方完成**日志服务角色授权**，且**推理日志投递依赖审计日志投递已开启**。

## 限制和注意事项

- **地域与时间限制**：
  - 推理日志仅支持北京、新加坡地域；
  - 模型用量数据仅支持查询 2026 年 9 月及之后（见[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）；
  - 美国（弗吉尼亚）地域的调用次数仅支持 2026 年 10 月及之后。
- **权限与依赖**：
  - 创建告警规则前**必须完成云监控服务角色授权**，否则按钮不可点击（见[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）；
  - 开启推理日志前**必须已开启审计日志投递**；关闭审计日志投递将**同步关闭推理日志投递**。
- **数据时效性与精度**：
  - 监控图表数据延迟约 1–2 分钟；
  - 模型用量页面中：调用次数延迟约 1 分钟，Token 用量与费用延迟约 10 分钟；
  - 审计日志查询最长支持 30 天，推理日志无明确上限但受 SLS 配置约束。
- **其他重要限制**：
  - 告警仅支持预置模板所列指标（共 12 个），非模板指标（如 RPM、TPM、缓存命中率）无法配置告警；
  - SLS 侧**禁止修改百炼创建的日志库索引**，否则导致查询失败；
  - **关闭日志投递后，关闭期间产生的日志无法补录**，请谨慎操作；
  - 批量离线推理（Batch File）和批量在线推理（Batch Chat）在用量页面**不展示调用次数**。

## 来源文档

- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)
- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)


