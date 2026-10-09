# model monitoring

百炼平台提供面向生产环境的模型调用可观测能力，覆盖分钟级监控指标、审计日志、推理日志及告警配置。所有监控数据按业务空间隔离，仅反映当前选中空间内的调用行为，不作为计费依据（计费请以费用中心账单为准）。该能力适用于模型服务稳定性保障、性能退化排查与用量成本治理等核心运维场景。

## 支持的模型与功能

- **支持范围**：所有在模型列表中可见的模型（含调优后模型）均支持基础监控与用量统计；但语音、图片、视频生成及三方直连类模型部分不支持监控告警，具体以控制台实时展示为准 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
- **核心功能**：
  - **监控指标**：调用次数、失败次数、失败率、调用时长、首 [Token](../concepts/token.md) 延时、限流错误次数、模型消耗 Total[Token](../concepts/token.md) 数等（共14项），其中9项支持配置告警 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)；
  - **日志能力**：审计日志（默认开启，含 Request ID、状态码、[Token](../concepts/token.md) 用量等，不含 Prompt/Response）；推理日志（需手动开启，含完整 Prompt/Response，仅北京和新加坡地域可用）；
  - **用量统计**：按模型、API-Key、时间粒度（分钟/小时/天）聚合 Token、图像张数、视频秒数等，数据延迟约 1 小时 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

> **注意**：文档 1 中称“监控数据按业务空间隔离”，而文档 2 在“查看模型用量”小节明确说明“数据按[业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)维度统计，不支持按阿里云账号维度统计”，二者一致；但文档 2 的常见问题中又指出“可在账单详情页面按阿里云账号查 Token 总用量”，该口径属于计费系统范畴，与监控平台的数据隔离逻辑不冲突，开发者应区分「可观测数据」与「计费数据」两个域。

## 关键参数

| 参数 | 说明 | 取值范围/约束 |
|------|------|----------------|
| **时间精度** | 监控图表支持的时间粒度 | 概览页支持自定义时间范围；详情页额外支持分钟级精度（仅限模型监控详情页） [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| **API-Key 筛选** | 仅展示当前业务空间下已创建且未删除的 API-Key | 列表显示 ID 与描述；若 Key 已删除，描述为空 |
| **告警检查周期** | 告警规则触发检测频率 | 必填，单位为秒，默认 60 秒，必须为 ≥0 的整数（0 表示即时触发） |
| **持续时间** | 告警触发需满足阈值的最短连续时长 | 必填，单位为分钟 |
| **统计周期（模板）** | 预置告警模板中指标计算的时间窗口 | 1~10080 分钟（即 1 分钟至 7 天） |

## 使用方式

1. **访问入口**：登录百炼控制台 → 左侧导航栏 **运维管理 > 模型监控**（概览页）或 **费用与成本 > 模型用量**；
2. **快速配置告警**：
   - 在模型监控详情页图表中点击支持告警的指标旁的蓝色/红色铃铛图标，打开侧边面板一键配置；
   - 或前往 **模型告警页面**（`/cn-beijing/model/alert`）→ **告警规则** 页签，使用预置模板（如“模型调用失败占比1分钟总和大于1%”）创建规则；
3. **开启日志投递**（用于长期留存或对接自有系统）：
   - 审计日志投递：需先授权日志服务角色、开通 SLS、创建日志库；
   - 推理日志投递：**必须先开启审计日志投递**，否则不可配置；
   - 监控数据投递：需授权云监控服务角色并创建 Prometheus 实例（仅支持云监控 Prometheus，不支持自建） [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)；
4. **用量分析**：在[模型用量](https://bailian.console.aliyun.com/cn-beijing/costing-balance/usage-statistics)页选择模型类型、时间范围、API-Key 后，直接查看表格与趋势图；点击单行“查看详情”进入模型粒度用量分析。

## 限制和注意事项

- **数据延迟**：监控图表数据延迟 **分钟级**；模型用量数据延迟 **约 1 小时**；审计日志查询最长支持 **30 天**；推理日志仅限北京、新加坡地域 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)、[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)；
- **告警能力限制**：
  - 仅预置模板所列指标（如失败率、TotalToken 数、首 Token 延时等）可配置告警；非预置指标（如 RPM、TPM、缓存命中率）不展示告警铃铛，无法配置 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)；
  - 创建告警规则前**必须完成云监控服务角色授权**，否则按钮禁用；
- **日志投递风险**：
  - 关闭审计日志投递将**自动关闭推理日志投递**，且关闭期间日志**无法补录**；
  - 不得在 SLS 侧删除百炼创建的日志库，否则导致投递失败；
  - SLS 侧不支持修改索引，修改将导致查询失败；
- **免费额度联动**：“免费额度用完即停”功能开启后，额度耗尽将返回 `403 AllocationQuota.FreeTierOnly` 错误；该功能**仅能在仍有未消耗额度时开启**，关闭操作需待额度完全耗尽后方可执行。

## 来源文档

- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)
- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)


