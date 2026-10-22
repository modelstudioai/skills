# model monitoring

百炼平台的 model monitoring 是面向生产环境的可观测性能力，提供分钟级延迟的模型调用统计、性能指标监控、多维告警配置及审计/推理日志能力。所有数据按业务空间隔离，不跨空间聚合，且监控数据仅作运维参考，**不作为计费依据**（计费以账单为准）。核心目标是帮助开发者快速定位调用异常、评估服务健康度、控制 Token 成本并保障 SLA。

## 支持的模型/功能

- **支持范围**：模型列表中的所有官方模型均支持基础监控（调用次数、失败率、时延等），但语音、图片、视频生成及三方直连类模型部分功能受限，具体支持情况需在控制台实时确认 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  
- **调用类型覆盖**：支持实时推理（含 API 调用、应用节点、模型广场、Prompt 优化、评测等）和批量推理（仅「大语言模型」页签支持按推理类型筛选）；但批量推理的监控粒度弱于实时推理，部分性能指标（如首 Token 延时）不适用。  
- **日志能力分层**：  
  - 审计日志默认开启，记录 Request ID、模型、Token 用量、状态码、时延等元信息，**不包含 Prompt/Response**；  
  - 推理日志需手动开启，记录完整 Prompt/Response 及中间步骤（长度上限 128K），当前**仅北京和新加坡地域支持** [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  
- **用量统计联动**：监控数据与[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)页面共享同一套模型 Code 和 API-Key 维度，但监控延迟约 1 分钟，用量统计延迟约 1 小时。

> **注意**：文档 1 中称“模型用量数据延迟约为 1 小时”，而文档 2 明确“监控数据调用发生后分钟级即可查看”。二者统计目的不同（计费 vs 运维），但开发者需注意：**告警触发基于分钟级监控数据，而费用对账必须依赖小时级用量数据或账单**，不可混用。

## 关键参数

| 参数 | 说明 | 是否支持告警 | 备注 |
|------|------|--------------|------|
| `调用次数` / `调用量（Token总量）` | 总调用数 / 总 Token 消耗量 | ✅ | `调用量` 即 `模型消耗 TotalToken 数`，预置告警模板中直接使用该名称 |
| `失败率` | 失败次数 ÷ 总调用次数 | ✅ | 推荐为关键可用性指标配置告警，阈值建议 ≥1% |
| `调用时长` | 请求到响应总耗时（ms） | ✅ | 用于评估端到端延迟，含网络与模型处理时间 |
| `首 Token 延时` | 首个 Token 返回耗时（ms） | ✅ | 衡量模型“启动”性能，对流式体验至关重要 |
| `限流错误次数（429）` | 1 分钟内触发限流的请求数 | ✅ | 直接反映配额瓶颈，建议结合 `RPM`/`TPM` 指标分析 |
| `非首 Token 延时` | 后续 Token 平均生成耗时 | ❌ | 不支持告警，仅用于性能归因分析 |
| `缓存命中率` | 缓存命中 Token 数 / 输入 Token 数 | ❌ | 无告警能力，需通过日志或自定义查询分析 |

- **告警阈值单位**：所有预置模板中时间窗口均为 **1 分钟聚合**（如“失败次数1分钟总和大于10”），统计周期字段在自定义模板中可设为 1–10080 分钟。  
- **API-Key 筛选**：监控与用量页面均支持按 API-Key ID 筛选，但**仅展示当前业务空间下已创建且未删除的 API-Key**（已删除 Key 在列表中描述为空）。

## 使用方式

1. **访问入口**：  
   - 监控概览页：[百炼控制台 → 运维管理 → 模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)；  
   - 用量统计页：[模型用量](https://bailian.console.aliyun.com/cn-beijing/costing-balance/usage-statistics)（按模型类型页签切换）；  
   - 告警配置页：[模型告警](https://bailian.console.aliyun.com/cn-beijing/model/alert)。  

2. **快速配置告警**：  
   - 在模型监控详情页图表中，点击支持告警的指标旁的 **蓝色/红色铃铛图标**，直接打开规则配置侧边面板；  
   - 优先选用预置模板（如“模型调用失败占比1分钟总和大于1%”），填入模型、通知对象即可生效；  
   - 创建前**必须完成云监控服务角色授权**（否则按钮置灰），授权后自动开通云监控、SLS 及 Prometheus [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  

3. **日志调试流程**：  
   - 先通过审计日志定位异常 Request ID（按状态码、时间、模型筛选）；  
   - 若需复现问题，**开启推理日志投递**（需先授权 SLS 角色并创建日志库），再在推理日志页签中搜索同一 Request ID 查看完整 Prompt/Response；  
   - 注意：推理日志投递关闭后，期间日志**无法补录**，且 SLS 日志库不可删除 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。  

4. **用量成本管控**：  
   - 在[免费额度](https://bailian.console.aliyun.com/cn-beijing/costing-balance/free-quota)页开启“免费额度用完即停”，避免超额扣费；  
   - 结合用量页的“总调用成功次数 Top 10 模型”和“平均单次请求Token量”卡片，识别高消耗模型并优化 `max_tokens` 或 Prompt [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

## 限制和注意事项

- **数据时效性**：监控数据延迟 **≈1 分钟**，用量统计延迟 **≈1 小时**，账单数据延迟更长（按分钟汇总，T+1 可查），三者不可互为验证依据。  
- **地域限制**：推理日志仅支持北京、新加坡地域；其他地域用户如需完整请求内容，只能依赖客户端侧日志。  
- **告警能力边界**：  
  - 仅预置模板所列指标（共 12 项）支持一键告警，`RPM`、`TPM`、`内容安全错误次数` 等高频指标**不支持告警配置**；  
  - 告警检查周期最小为 60 秒，无法实现秒级响应；  
  - 告警历史仅保留 **2026年9月3日之后** 的记录，此前数据需查云监控控制台。  
- **权限与计费**：  
  - 开启监控/日志投递会自动开通云监控、SLS、Prometheus 服务，**产生对应云产品费用**；  
  - 免费额度管理仅影响模型调用计费，**不影响投递产生的 SLS/云监控费用**；  
  - 手机 App **不支持查看任何监控、用量或告警数据**，必须使用 PC 端控制台 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。  
- **模型维度一致性**：所有监控、用量、告警均以 **模型 Code**（如 `qwen-plus`）为唯一标识，而非模型名称或别名，查询时请严格匹配。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


