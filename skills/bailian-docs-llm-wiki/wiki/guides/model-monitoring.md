# model monitoring

百炼平台的 model monitoring 是面向生产环境的模型调用可观测性能力，提供分钟级延迟的实时监控、多维告警与审计/推理日志能力，帮助开发者快速定位性能退化、失败突增、成本异常等典型问题。该能力按业务空间隔离，数据不作为计费依据，需结合[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)进行对账。核心功能覆盖调用统计、性能指标、告警配置与日志追溯四个层次。

## 支持的模型/功能

- **支持范围**：全部百炼平台内置模型（含文本生成、视觉理解、语音合成、全模态、向量模型等）均支持基础监控；但语音、图片、视频生成及三方直连类模型部分功能受限，具体以控制台实际展示为准（详见[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)说明）。
- **核心功能模块**：
  - **调用统计**：调用次数、失败次数、失败率、限流错误次数（429）、内容安全拦截次数；
  - **性能指标**：调用时长、首 Token 延时、非首 Token 延时、缓存命中量/率；
  - **用量指标**：Token 总量、模型消耗 TotalToken 数（预置告警模板专用）、平均单次请求调用量；
  - **日志能力**：默认开启审计日志（含 Request ID、状态码、用量、延时等元数据）；推理日志（含完整 Prompt/Response）需手动开启，且仅支持北京、新加坡地域（见[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。

> **注意**：文档 1 中“失败次数、失败率、限流错误次数和内容安全拦截次数已移至[模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)页面”与文档 2 的功能描述一致，但文档 1 的表格中将“内容安全错误次数”列为监控指标却标注“不支持告警”，而文档 2 的指标表明确其“不支持告警”，二者无矛盾；但文档 1 提到“批量离线推理和批量在线推理不展示调用次数”，而文档 2 的监控详情页未明确排除批量推理的指标采集——实践中批量推理调用在监控图表中可被统计（如调用次数、失败率），但部分细分维度（如 API Key）可能为空（参见[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)常见问题）。

## 关键参数

| 参数名 | 含义 | 是否支持告警 | 说明 |
|--------|------|----------------|------|
| `调用次数` | 模型被成功/失败调用的总次数 | ✅ | 可用于容量规划或突增检测 |
| `失败率` | 失败次数 / 总调用次数 | ✅ | 推荐配置阈值告警（如 >1%），保障可用性 |
| `模型消耗 TotalToken 数` | 按模型维度聚合的 Token 消耗总量 | ✅ | 预置告警模板专用指标，推荐配环比突增告警以控制 Token 成本 |
| `首 Token 延时` | 请求发起到返回首个 Token 的耗时 | ✅ | 关键性能指标，建议配置阈值（如 >10 秒）告警 |
| `调用时长` | 完整请求响应耗时 | ✅ | 用于端到端性能诊断 |
| `限流错误次数` | HTTP 429 触发次数 | ✅ | 直接反映配额瓶颈 |
| `非首 Token 延时` | 首 Token 后每 Token 平均生成耗时 | ❌ | 仅用于分析，不可配置告警 |
| `缓存命中率` | 缓存命中 Token 数 / 输入 Token 数 | ❌ | 仅用于优化上下文复用效率评估 |

## 使用方式

1. **访问入口**：登录百炼控制台 → 左侧导航栏 **运维管理 > 模型监控**（[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。
2. **查看概览**：在概览页筛选时间、推理类型、API Key，快速查看总调用次数、失败次数、平均调用时长等卡片数据。
3. **深入分析**：
   - 点击模型列表中的 **查看详情** 进入模型监控详情页，查看分组图表（调用统计 & 性能）；
   - 点击 **查看日志** 进入审计日志页签，支持按 Request ID、状态码（200/4XX/5XX）、时间范围（最长 30 天）筛选；
   - 如需 Prompt/Response 调试，切换至 **推理日志** 页签并完成[日志投递](../../raw/model-user-guide/model-monitoring/model-telemetry.md)配置（需先授权 SLS 角色并创建日志库）。
4. **配置告警**：
   - 在监控图表上点击支持告警的指标旁的 **铃铛图标**，快速创建规则；
   - 或进入 [模型告警页面](https://bailian.console.aliyun.com/cn-beijing/model/alert) → **告警规则** 页签，使用预置模板（如“模型调用失败占比1分钟总和大于1%”）创建；
   - 创建前必须完成[监控数据投递](../../raw/model-user-guide/model-monitoring/model-telemetry.md)的云监控服务角色授权。

## 限制和注意事项

- **数据延迟与范围**：监控数据延迟约 1 分钟，不作为计费依据；用量数据（如 Token）以[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)页面为准，该页面支持查询 2026 年 9 月 1 日起的数据。
- **地域与模型限制**：美国（弗吉尼亚）地域暂不展示模型调用次数；推理日志仅支持北京、新加坡地域；语音/图片/视频生成等部分模型的监控能力受限（见[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。
- **告警依赖项**：创建告警规则前，必须完成云监控服务角色授权（否则按钮禁用）；授权后将自动开通云监控、SLS 及 Prometheus，相关产品按实际用量计费。
- **日志投递风险**：关闭审计日志投递将同步关闭推理日志投递；关闭期间日志无法补录；SLS 日志库不可删除，否则导致投递失败。
- **用量优化提示**：为控制 Token 成本，应合理设置 `max_tokens`、选择轻量级模型、优化 Prompt，并通过监控告警及时发现用量异常（参见[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)的应用于生产环境建议）。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


