# model monitoring

model monitoring 是百炼平台提供的核心运维能力，用于实时观测模型调用的规模、健康度与性能表现，支撑成本控制、稳定性保障与问题排查。监控数据分钟级延迟，按业务空间维度隔离，不作为计费依据；用量统计与费用核对请以[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)和账单为准。所有监控功能均需在控制台「运维管理 > 模型监控」入口访问。

## 支持的模型/功能

- **支持范围**：绝大多数百炼内置模型（文本生成、深度思考、视觉理解、全模态、向量模型等）均支持基础监控；但语音、图片/视频生成及三方直连类模型部分指标可能受限，具体以控制台实际展示为准（详见[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)说明）。
- **核心功能模块**：
  - **调用统计**：调用次数、失败次数、失败率、限流错误次数（429）、内容安全拦截次数；
  - **性能指标**：调用时长、首 [Token](../concepts/token.md) 延时、非首 [Token](../concepts/token.md) 延时、TPS、缓存命中率；
  - **用量指标**：[Token](../concepts/token.md) 总量、模型消耗 TotalToken 数、平均单次请求调用量；
  - **日志能力**：默认开启审计日志（含 Request ID、状态码、延迟、用量等元数据）；推理日志（含完整 Prompt/Response）需手动开启并配置日志投递；
  - **告警体系**：支持基于预置或自定义模板为关键指标（如失败率、TotalToken 数、调用时长）配置阈值告警。

> **注意**：文档 1 中提到“失败次数、失败率、限流错误次数和内容安全拦截次数已移至[模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)页面”，而文档 2 明确将这些指标列为监控详情页核心指标；二者一致，确认该迁移已完成，旧版用量页面不再承载故障类指标。

## 关键参数

| 参数名 | 说明 | 是否支持告警 | 备注 |
|--------|------|--------------|------|
| `调用次数` | 成功 + 失败的总请求次数 | ✅ | RPM/TPM 等衍生指标不支持告警 |
| `失败率` | 失败次数 / 总调用次数 | ✅ | 推荐为关键可用性指标配置告警（见[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)） |
| `模型消耗 TotalToken 数` | 按模型维度聚合的 Token 消耗总量 | ✅ | 预置告警模板专用指标，推荐用于成本突增监控 |
| `首 Token 延时` | 请求发出到首个 Token 返回的耗时 | ✅ | 性能退化核心指标，预置模板已覆盖 |
| `调用时长` | 完整请求响应耗时 | ✅ | 含流式响应总时长 |
| `限流错误次数` | HTTP 429 触发次数 | ✅ | 直接反映配额或吞吐瓶颈 |
| `内容安全错误次数` | 内容安全拦截次数 | ❌ | 仅展示，不可配置告警（见[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)指标表） |
| `非首 Token 延时` | 首 Token 后每 Token 平均生成耗时 | ❌ | 仅用于性能分析，不支持告警 |

## 使用方式

1. **访问路径**：登录百炼控制台 → 左侧导航栏「运维管理」→ 「模型监控」进入概览页；
2. **筛选数据**：
   - 时间范围（支持快捷选择或自定义起止时间）；
   - 推理类型（在线推理 / 批量离线推理 / 批量在线推理）；
   - API Key（仅显示当前业务空间下已创建的 Key）；
3. **查看详情**：
   - 在概览页模型列表点击「查看详情」进入单模型监控页，图表支持按时间精度（分钟/小时/天）切换；
   - 点击指标图表右上角「告警铃铛」可快速为该指标配置告警规则；
4. **配置告警**：
   - 进入「模型告警」页面（`https://bailian.console.aliyun.com/cn-beijing/model/alert`）；
   - 需先完成[监控数据投递](../../raw/model-user-guide/model-monitoring/model-telemetry.md)中云监控服务角色授权；
   - 推荐直接选用预置模板（如“模型调用失败占比1分钟总和大于1%”），填参即用；
5. **日志查看与投递**：
   - 审计日志默认开启，7–30 天内可查；
   - 推理日志需在日志页签点击「开始配置」，完成 SLS 日志库授权与创建（仅北京、新加坡地域支持）；
   - 日志投递是推理日志启用的前提（见[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。

## 限制和注意事项

- **数据延迟与范围**：监控数据延迟约 1 分钟，不作为计费依据；用量统计仅覆盖 2026 年 9 月 1 日后数据，更早记录需查账单（见[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）；
- **地域限制**：美国（弗吉尼亚）地域不展示调用次数；推理日志仅支持北京、新加坡地域；
- **权限隔离**：所有监控数据按业务空间隔离，无法跨空间或按阿里云账号维度汇总；
- **告警依赖项**：创建告警规则前必须完成云监控服务角色授权，否则按钮禁用（见[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）；
- **投递风险**：关闭审计日志投递将同步关闭推理日志投递；关闭期间日志无法补录（见[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）；
- **批量调用标识**：Batch Chat 调用的 API Key ID 在监控明细中为空，需结合推理类型筛选定位。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


