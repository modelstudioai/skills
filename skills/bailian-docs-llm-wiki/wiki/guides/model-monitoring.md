# model monitoring

模型监控是百炼平台面向开发者提供的核心可观测性能力，用于实时掌握模型调用的规模、健康度与性能表现。监控数据分钟级延迟即可在控制台呈现，支持按时间、推理类型、API-Key 等多维度筛选；告警能力基于云监控服务构建，可对关键指标配置阈值触发通知。需注意：监控数据**不作为计费依据**，费用核对请以[费用中心](https://bailian.console.aliyun.com/cn-beijing/costing-balance/overview)账单为准 —— 该差异已在[监控告警 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md)中明确强调。

## 支持的模型与功能

- **支持范围**：文本生成、深度思考、视觉理解、全模态、向量等主流大模型均支持完整监控；但语音、图片、视频生成及三方直连类模型**部分不支持**，具体以控制台实际展示为准（见[监控告警 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md)说明）。
- **核心功能模块**：
  - **监控概览**：展示业务空间级总调用次数、失败次数、平均调用时长、首 Token 延时等聚合卡片；
  - **模型详情页**：提供单模型维度的调用统计（如调用次数、失败率）与性能指标（如首 Token 延时、调用时长）趋势图；
  - **审计日志**：默认开启，记录 Request ID、状态码、Token 用量、延迟等元信息，**不含 Prompt/Response**；
  - **推理日志**：需手动开启并配置日志投递，记录完整 Prompt/Response 及中间步骤，适用于深度调试（见[监控告警 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）；
  - **用量统计**：独立于监控系统，在[模型用量](https://bailian.console.aliyun.com/cn-beijing/costing-balance/usage-statistics)页面提供按 Token、图像张数、视频秒数等收费单位的用量明细，延迟约 10 分钟（见[模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）。

> **注意**：文档 2 明确指出“失败次数、失败率、限流错误次数和内容安全拦截次数已移至[模型监控](raw/model-user-guide/model-monitoring/model-telemetry.md)页面，不再在模型用量详情中展示”，而文档 1 的监控指标表仍包含这些字段。这表明**用量页面已剥离故障类指标，统一由监控系统承载**，开发者应以监控页面为准进行异常排查。

## 关键参数

| 参数名 | 说明 | 是否支持告警 | 备注 |
|--------|------|--------------|------|
| `调用次数` | 模型被调用的总次数 | ✅ | RPM（每分钟请求数）不支持告警 |
| `失败率` | 失败次数 / 总调用次数 | ✅ | 排查可用性问题的首选指标 |
| `调用时长` | 请求到响应的总耗时 | ✅ | 单位：毫秒 |
| `首 Token 延时` | 首个 Token 返回耗时 | ✅ | 衡量首包响应性能的关键指标 |
| `模型消耗 TotalToken 数` | 按模型维度统计的 Token 消耗总量 | ✅ | 预置告警模板专用，用于成本突增监控 |
| `限流错误次数` | HTTP 429 触发次数 | ✅ | 直接反映配额瓶颈 |
| `非首 Token 延时` | 后续 Token 平均生成耗时 | ❌ | 仅展示，不可配置告警 |
| `RPM` / `TPM` | 每分钟请求数 / Token 数 | ❌ | 仅用于趋势分析，不支持告警 |

> **注意**：是否支持告警取决于预置告警模板是否覆盖该指标（见[监控告警 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md)），不在模板中的指标（如 `RPM`）图表上不显示告警铃铛。

## 使用方式

1. **访问入口**：登录百炼控制台 → 左侧导航栏 **运维管理 > 模型监控**（概览页）或 **运维管理 > 模型告警**（告警规则页）。
2. **快速配置告警**：
   - 在模型监控详情页的指标图表上点击蓝色/灰色告警铃铛图标；
   - 或进入[模型告警页面](https://bailian.console.aliyun.com/cn-beijing/model/alert)，选择「告警规则」页签 → 「创建告警规则」；
   - **必须前置授权**：首次创建前需在监控投递页完成「云监控服务角色授权」（未授权则按钮禁用）。
3. **日志查看**：
   - 审计日志：概览页模型列表点击「查看日志」→ 切换至「审计日志」页签；
   - 推理日志：需先开启审计日志投递，再在日志页签切换至「推理日志」并完成 SLS 日志库配置（仅北京、新加坡地域支持）。
4. **数据投递**（用于长期留存或对接自有系统）：
   - 监控数据：投递至云监控 Prometheus 实例（需授权 + 开通 Prometheus）；
   - 日志数据：投递至 SLS 日志库（审计日志投递为推理日志前提）。

## 限制和注意事项

- **数据隔离与延迟**：监控数据按**业务空间**隔离，仅可见当前选中空间；监控图表数据延迟约 **1–2 分钟**，审计日志查询最长支持 **30 天**，推理日志依赖 SLS 配置。
- **地域与时间限制**：模型用量数据仅支持查询 **2026 年 9 月及之后**（美国弗吉尼亚地域从 10 月起）；更早数据需通过阿里云账单中心导出（见[模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）。
- **功能限制**：
  - 推理日志**不支持修改 SLS 索引**，否则查询失败；
  - **禁止删除百炼创建的 SLS 日志库**，否则导致投递中断；
  - 关闭审计日志投递将**自动关闭推理日志投递**，且关闭期间日志**无法补录**；
  - 告警规则迁移仅支持从百炼平台创建的 Prometheus 告警规则，云监控侧手动创建的规则不兼容。
- **计费提示**：监控与告警本身**免费使用**，但数据投递依赖的云监控、SLS、Prometheus 产品按实际用量计费（见[监控告警 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。

## 来源文档

- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)
- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)


