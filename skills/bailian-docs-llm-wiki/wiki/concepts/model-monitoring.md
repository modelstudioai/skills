# 模型可观测性

模型可观测性是指在百炼平台上对模型调用行为、性能表现、资源消耗及异常状态进行实时采集、多维分析与主动反馈的能力，是保障模型服务稳定性、可解释性与持续优化的基础支撑能力。

## 在百炼平台的不同场景中，这个概念如何使用

模型可观测性并非单一功能模块，而是贯穿模型生命周期的关键横切能力，在以下核心场景中被具体化和落地：

- **模型监控（Model Monitoring）**：作为可观测性的主入口，提供分钟级延迟的指标采集与可视化，覆盖调用次数、失败率、首 Token 延时、TotalToken 消耗等 15+ 核心指标；支持按业务空间隔离数据，用于快速定位性能退化、失败突增或限流瓶颈。审计日志默认开启（含 Request ID、状态码、延时、用量），推理日志需手动启用（记录完整 Prompt/Response，仅限北京、新加坡地域）。

- **Agent 治理（Agent Governance）**：扩展可观测性至运行时决策链路。通过 `X-Bailian-Governance-Result` 响应头返回治理动作详情（如拦截原因、重写结果、工具调用白名单匹配状态），使 Agent 的“黑盒”行为可审计、可归因；治理日志独立保留 7 天，支持导出用于策略复盘与进化训练。

- **模型管理（Model Management）**：将可观测性前置到配置层。限流参数（`request_limit`/`usage_limit`）本身即可观测性约束的执行依据；调用配额的实时生效状态、权限变更记录，均可通过 API 查询，为容量规划与成本治理提供数据基线。

- **计费对接（Billing API）**：虽不直接提供可观测能力，但为可观测性提供关键校验维度。账单趋势（T+2 小时延迟）与监控用量（T+10 分钟）存在时间差与统计口径差异（如 Token 计算逻辑），开发者需结合二者交叉验证——例如当监控显示某模型 TPM 异常飙升，但账单未同步体现，可能提示用量统计延迟、计费采样偏差或非计费调用路径（如调试请求）。

> ⚠️ 注意：语音、图片、视频生成及三方直连类模型暂不支持告警功能；美国（弗吉尼亚）地域不展示调用次数指标；推理日志功能仅在北京、新加坡地域可用。

## 关键参数和配置

| 参数名 | 所属场景 | 说明 | 是否支持告警 | 典型用途 |
|--------|----------|------|--------------|----------|
| `调用次数` | Model Monitoring | 总调用数（含成功/失败） | ✅ | 监控流量基线、识别突发调用 |
| `失败率` | Model Monitoring | 失败次数 / 总调用次数 | ✅ | 快速发现模型或网关异常 |
| `首 Token 延时` | Model Monitoring | 请求发起到首个 Token 返回耗时 | ✅ | 衡量模型冷启与首响性能 |
| `调用时长` | Model Monitoring | 完整响应耗时 | ✅ | 诊断长尾延迟与生成效率 |
| `限流错误次数（429）` | Model Monitoring | HTTP 429 触发频次 | ✅ | 判断配额不足或限流策略过严 |
| `模型消耗 TotalToken 数` | Model Monitoring | 模型维度 Token 总消耗量 | ✅ | 关联计费与成本异常分析 |
| `X-Bailian-Governance-Result` | Agent Governance | 响应头中返回的 JSON 字符串，含治理动作详情 | ❌（需自行解析并上报） | 构建自定义治理看板、触发二次告警 |
| `request_limit` / `usage_limit` | Model Management | QPM/TPM 配额配置值 | ❌（但其超限行为会触发监控指标） | 设置可观测性边界，驱动告警阈值设定 |

## 面向开发者，简洁实用

- **起步最快**：登录控制台 → 进入 [模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry) → 查看目标模型的「失败率」与「首 Token 延时」趋势图，点击图表右上角铃铛图标，1 分钟内完成预置告警（如“失败率 1 分钟总和 > 1%”）。
- **排查必查三件套**：当服务异常时，同步打开三个视图：① 监控页的「失败次数 + 429 次数」曲线；② 审计日志页，按 `status_code: 4xx or 5xx` 筛选；③ Billing 账单趋势页，确认消费是否同步激增——三者交叉印证根因（模型故障？配额不足？恶意刷量？）。
- **日志要开早**：若需分析 Prompt/Response 质量或安全问题，务必提前在 [日志投递](raw/model-user-guide/model-monitoring/model-telemetry.md) 中完成 SLS 授权，并在监控页开启「推理日志」；该配置不可回溯，历史请求无记录。
- **告警别只看数字**：`失败率` 告警有效，但 `平均单次请求调用量` 不支持告警；如需监控 Token 异常增长，应使用 `模型消耗 TotalToken 数` 指标 + 自定义规则（如“过去 5 分钟环比上升 300%”）。
- **API 集成建议**：  
  - 监控数据 → 调用 `/api/v1/telemetry/metrics`（需 WorkspaceId + API Key）；  
  - 治理结果 → 解析响应头 `X-Bailian-Governance-Result`，推荐用 JSON Schema 校验结构；  
  - 账单比对 → 每日定时调用 `getbillingtrend?granularity=daily`，与监控 `TotalToken` 数据做 Delta 校验。

## 关联主题页

- [model monitoring](../guides/model-monitoring.md)
- [agent governance](../guides/agent-governance.md)
- [billing api](../api/billing-api.md)
- [model management](../api/model-management.md)


