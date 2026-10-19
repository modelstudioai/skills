# model monitoring

百炼平台的 model monitoring 是面向开发者的一套可观测性能力，提供分钟级延迟的模型调用统计、性能指标监控、告警配置及审计/推理日志支持，覆盖用量分析、健康度评估与异常排查全链路。该能力按业务空间隔离，数据不跨空间共享，且所有监控数据仅作运维参考，**不作为计费依据**（计费以账单为准）[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。模型用量统计与监控告警功能相互补充：前者聚焦资源消耗与成本视角，后者侧重服务稳定性与性能表现。

## 支持的模型/功能

- **支持范围**：所有在百炼模型列表中可见的模型（含基于其调优后的部署模型）均支持用量查看与基础监控 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)；  
- **监控能力差异**：语音、图片、视频生成及三方直连等部分模型**不支持监控告警功能**，具体支持情况需以控制台实时展示为准 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)；  
- **核心功能模块**：
  - **用量统计**：按模型 Code、API-Key、时间粒度（分钟/小时/天）聚合调用次数、Token 总量、图像张数、视频秒数等，支持免费额度使用概览与“用完即停”开关管理；
  - **监控图表**：提供调用次数、失败率、调用时长、首 Token 延时、限流错误次数（429）、内容安全拦截次数等 15+ 指标，支持多维度筛选；
  - **告警配置**：支持为调用次数、失败率、失败次数、调用时长、首 Token 延时、模型消耗 TotalToken 数、限流错误次数等关键指标配置阈值告警（详见下文“关键参数”）；
  - **日志能力**：审计日志默认开启（记录 Request ID、状态码、Token 用量、延时等，不含 Prompt/Response）；推理日志需手动开启并完成日志投递配置，用于记录完整 Prompt/Response 及中间步骤。

> **注意**：文档 1 中称“所有模型均支持查看用量”，而文档 2 明确指出“语音、图片、视频生成及三方直连等部分模型不支持监控告警”。二者无直接矛盾——用量统计（文档 1）与监控告警（文档 2）是两个独立能力，但开发者需注意：**不支持监控告警的模型，其性能类指标（如首 Token 延时、失败率）在控制台将不可见或不可配置告警**，仅用量数据仍可查。

## 关键参数

| 参数名 | 说明 | 是否支持告警 | 备注 |
|--------|------|--------------|------|
| `调用次数` | 模型被调用总次数 | ✅ | 支持预置模板“1分钟总和大于500” |
| `失败次数` / `失败率` | 调用失败绝对值或占比 | ✅ | 排查可用性问题首选指标；预置模板覆盖失败率 >1% 场景 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `模型消耗 TotalToken 数` | 按模型维度统计的 Token 消耗总量 | ✅ | **推荐为该指标配置环比突增告警以控制 Token 成本** [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `调用时长` | 请求到响应的总耗时 | ✅ | 预置模板阈值为 >60 秒 |
| `首 Token 延时` | 首个 Token 返回延迟 | ✅ | 预置模板阈值为 >10 秒；排查首包性能退化核心指标 |
| `限流错误次数`（429） | 触发限流的请求次数 | ✅ | 预置模板覆盖“1分钟总和大于10”场景 |
| `非首 Token 延时` | 后续 Token 平均生成耗时 | ❌ | 不支持告警配置 |
| `RPM` / `TPM` / `TPS` | 每分钟请求数/Token数/每秒输出Token数 | ❌ | 仅展示，不可告警 |
| `缓存命中率` | 缓存命中 Token 占输入 Token 比例 | ❌ | 仅展示，不可告警 |

- **告警检查周期**：最小支持 60 秒（0 表示触发即告警），单位为秒，必须为不小于 0 的整数；
- **持续时间**：告警触发需满足阈值条件的连续时长（单位：分钟），必填；
- **统计周期**（告警模板）：合法范围 1~10080 分钟（即 7 天），影响阈值计算窗口。

## 使用方式

1. **访问入口**：
   - 用量统计：[模型用量](https://bailian.console.aliyun.com/cn-beijing/costing-balance/usage-statistics) 页面（按模型类型页签切换）；
   - 监控告警：[模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry) → 概览页，或直接进入某模型详情页；
   - 告警规则管理：[模型告警页面](https://bailian.console.aliyun.com/cn-beijing/model/alert)；
   - 日志：监控概览页 → “查看日志” 或导航至日志页签。

2. **快速配置告警**：
   - 在模型监控详情页任一支持告警的指标图表上点击 **蓝色/红色告警铃铛**，打开侧边面板一键配置；
   - 或前往告警规则页签，选择预置模板（如“模型调用失败占比1分钟总和大于1%”），填写模型、持续时间、通知对象后创建。

3. **开启推理日志**（需完整调试）：
   - 前置条件：已授权日志服务角色、开通 SLS、创建日志库，并**已开启审计日志投递**；
   - 操作路径：日志页签 → 切换至“推理日志” → 点击“开始配置”完成投递设置；
   - **注意**：推理日志仅在北京、新加坡地域支持，其他地域暂不可用 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

4. **用量优化实践**（生产环境建议）：
   - 控制 `max_tokens` 与思考长度，避免冗余输出；
   - 对简单任务选用轻量模型而非大模型；
   - 结合用量趋势与告警，及时识别异常调用模式。

## 限制和注意事项

- **数据延迟**：用量统计数据延迟约 **1 小时**；监控指标延迟为 **分钟级**；审计日志最长支持查询 **30 天内**数据 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)；
- **时间范围限制**：用量统计不支持查看 **30 天以前**的数据；更早数据需通过[费用与成本](https://billing-cost.console.aliyun.com/finance/expense-report/expense-detail-by-instance)页面查询；
- **权限与地域限制**：
  - 推理日志仅支持北京、新加坡地域；
  - 监控数据投递仅支持云监控 Prometheus 实例（不支持自建 Prometheus）；
  - 日志投递关闭后，**关闭期间产生的日志无法补录至 SLS**，请谨慎操作 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)；
- **计费说明**：
  - 监控与告警规则本身**免费使用**，但依赖的云监控、SLS、Prometheus 产品按实际用量计费；
  - 免费额度“用完即停”功能**仅在仍有未消耗额度时可开启**；开启后若需关闭，须待额度完全耗尽 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)；
- **移动端限制**：阿里云 App **暂不支持**查看免费额度与模型用量数据，仅 PC 端控制台可用 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


