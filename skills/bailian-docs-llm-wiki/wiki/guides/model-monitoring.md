# model monitoring

百炼平台的 model monitoring 是面向生产环境的模型可观测性能力，提供分钟级延迟的调用统计、性能指标、失败分析与告警能力，帮助开发者实时掌握模型服务健康度、排查异常并控制成本。监控数据按业务空间隔离，不作为计费依据；用量对账请以[费用中心账单](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)为准。核心能力覆盖用量观测、健康度诊断、细粒度告警配置及日志审计，适用于所有已接入百炼平台的模型服务。

## 支持的模型与功能

- **支持范围**：全部在模型列表中可见的模型（含[调优后的模型](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)）均支持基础监控；但语音、图片、视频生成及三方直连等部分模型**不支持监控与告警**，具体需在控制台确认 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
- **核心功能模块**：
  - **用量统计**：调用次数、[Token](../concepts/token.md)s 用量、图片张数、视频秒数、语音合成字数、工具调用次数等，按模型/ API Key / 业务空间 / 地域等多维分组 [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)；
  - **健康度监控**：失败次数、失败率、限流错误次数（429）、内容安全拦截次数、调用时长、首 [Token](../concepts/token.md) 延时等；
  - **日志能力**：默认开启审计日志（含 Request ID、状态码、用量、延时，不含 Prompt/Response）；推理日志需手动开启，记录完整 Prompt/Response 与中间步骤，**仅在北京和新加坡地域支持**；
  - **告警体系**：支持为关键指标配置实时告警，含预置模板与自定义规则，告警触发后可通过邮件等渠道通知。

> **注意**：文档 1 中称“失败次数、失败率、限流错误次数和内容安全拦截次数已移至[模型监控](raw/model-user-guide/model-monitoring/model-telemetry.md)页面”，而文档 2 明确将这些指标列为监控详情页核心指标；二者一致，无矛盾。但文档 1 的“模型用量”页面已**不再展示失败类指标**，实际排查应以 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md) 为准。

## 关键参数

| 参数名 | 含义 | 是否支持告警 | 说明 |
|--------|------|----------------|------|
| `调用次数` | 模型被成功/失败调用的总次数 | ✅ | 包含预置吞吐单元、独占吞吐单元等调用 |
| `调用量`（[Token](../concepts/token.md) 总量） | 输入+输出 Token 总和 | ✅ | 仅统计按 Token 后付费的模型调用，不含训练、吞吐单元等 [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) |
| `失败次数` / `失败率` | 调用失败绝对值及占比 | ✅ | 排查突增首选指标；失败率 = 失败次数 / 总调用次数 |
| `限流错误次数`（429） | 触发限流的请求次数 | ✅ | 直接反映配额或 QPS 瓶颈 |
| `首 Token 延时` | 请求到首个 Token 返回的耗时 | ✅ | 衡量模型冷启与首响应性能的关键指标 |
| `调用时长` | 全请求生命周期耗时 | ✅ | 用于识别整体性能退化 |
| `模型消耗 TotalToken 数` | 预置告警模板专用指标 | ✅ | 推荐用于配置 Token 成本突增告警 |
| `非首 Token 延时` | 首 Token 后每 Token 平均生成耗时 | ❌ | 不支持告警配置 |
| `RPM` / `TPM` / `TPS` | 每分钟请求数/Token 数/每秒输出 Token 数 | ❌ | 仅作观测，不可配置告警 |

## 使用方式

1. **访问入口**：
   - 监控概览页：[百炼控制台 → 运维管理 → 模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)
   - 用量查询页：[模型用量](https://bailian.console.aliyun.com/cn-beijing/costing-balance/usage-statistics)
   - 告警配置页：[模型告警](https://bailian.console.aliyun.com/cn-beijing/model/alert)
   - 日志页：监控详情页 → 切换至「日志」页签

2. **快速配置告警**：
   - 在模型监控详情页图表中，点击支持告警的指标旁的**蓝色/红色告警铃铛**，直接打开规则配置侧边面板；
   - 或前往告警页面 → 「告警规则」页签 → 「创建告警规则」，选择预置模板（如“模型调用失败占比1分钟总和大于1%”）并填写模型、持续时间、通知对象等；
   - **必须前置授权**：首次创建前需在「监控数据投递」中完成云监控服务角色授权 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

3. **查看日志**：
   - 审计日志：默认开启，支持按 Request ID、状态码（200/4XX/5XX）、时间范围（最长30天）筛选；
   - 推理日志：需先开启审计日志投递 → 在日志页签点击「开始配置」→ 授权 SLS 角色并指定日志库 → 开启后即可查看 Prompt/Response（截断上限 128K）。

## 限制和注意事项

- **数据延迟与范围**：
  - 调用次数统计延迟约 1 分钟，Token/费用类指标延迟约 10 分钟；
  - 模型用量页面**仅支持查询 2026 年 9 月 1 日及之后的数据**；更早数据需通过[费用中心账单](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)导出；
  - 监控数据按**业务空间维度隔离**，不支持跨空间或按阿里云主账号汇总。

- **地域与模型限制**：
  - 美国（弗吉尼亚）地域在用量页面**暂不展示调用次数**；
  - 推理日志**仅在北京和新加坡地域可用**，其他地域开启失败；
  - 部分模型（语音、视频生成、三方直连等）**不支持监控与告警功能**，控制台会明确标识。

- **告警与投递约束**：
  - 告警规则依赖云监控服务，授权后将**自动开通云监控、SLS 及 Prometheus**，相关产品按实际用量计费；
  - 关闭审计日志投递将**同步关闭推理日志投递**，且关闭期间日志**无法补录**；
  - SLS 日志库禁止删除或修改索引，否则导致投递失败。

- **用量与计费差异**：
  - 监控数据**仅供参考，不作为计费依据**；用量对账请以费用中心账单为准；
  - “免费额度用完即停”功能开启后，额度耗尽将返回 `403 AllocationQuota.FreeTierOnly` 错误，该行为属于额度管控，**不计入监控失败率**。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


