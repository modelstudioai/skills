# model monitoring

百炼平台的 model monitoring 是面向生产环境的模型可观测性能力，提供分钟级延迟的调用统计、性能指标监控、告警配置及审计/推理日志能力，帮助开发者实时掌握模型健康度、排查异常并控制成本。该功能按业务空间隔离，数据不跨空间共享，且监控数据仅作观测参考，**不作为计费依据**（计费以账单为准）[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。用量统计与监控告警能力分别承载在两个独立控制台页面，需结合使用以实现完整闭环。

## 支持的模型/功能

- **支持范围**：所有在百炼模型列表中可调用的模型（含基于其调优后的部署模型）均支持用量查看与基础监控 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)；但**语音、图片、视频生成及三方直连等部分模型不支持监控告警功能**，具体支持情况需在控制台实时确认 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
- **核心功能模块**：
  - **用量统计**：按模型 Code、API-Key、时间维度（分钟/小时/天）聚合调用次数、Token 总量、图像张数、视频秒数等，支持 TOP10 模型排行与详情下钻。
  - **实时监控**：提供调用次数、失败率、首 Token 延时、调用时长、限流错误次数（429）、内容安全拦截次数等 15+ 指标图表，支持按推理类型（实时/批量）和 API-Key 筛选。
  - **告警管理**：支持基于预置或自定义模板为关键指标（如失败率 >1%、TotalToken 数突增）配置阈值告警，通知渠道包括邮箱等。
  - **日志能力**：审计日志默认开启（含 Request ID、状态码、Token 用量、延时，不含 Prompt/Response）；推理日志需手动开启并投递至 SLS，记录完整 Prompt/Response（上限 128KB）。

> **注意**：文档 1 中称“所有模型均支持查看用量”，而文档 2 明确指出“语音、图片、视频生成及三方直连等部分模型不支持监控告警”。二者无矛盾——用量统计（计量）与监控告警（可观测性）是解耦能力，但开发者需注意：**不支持监控告警的模型，其用量虽可查，但无法配置失败率、延时等运行时告警**。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `Time Range` | 用量统计支持最长查询 **30 天内**数据；监控图表默认保留最近数据，无明确历史上限，但审计日志仅支持查询 **最近 30 天** | [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md), [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `Time Precision` | 用量页支持分钟/小时/天精度（跨度 >1 天禁用分钟精度，>7 天仅支持天）；监控详情页才支持时间精度筛选 | [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) |
| `Free Tier Stop` | 「免费额度用完即停」开关：开启后额度耗尽返回 `403 AllocationQuota.FreeTierOnly`；**仅能在仍有未消耗额度时开启，关闭需待额度完全耗尽后操作** | [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) |
| `Alert Check Period` | 告警检查周期最小单位为 **秒**（默认 60 秒），填 `0` 表示触发即告警；持续时间以**分钟**为单位填写 | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `Token` | 统计单位依模型类型而异：大语言/全模态/向量模型按 Token；视觉模型按图像张数或视频秒数；语音模型按秒/字符/Token（视具体模型而定） | [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) |

## 使用方式

1. **访问入口**：
   - 用量统计：[模型用量](https://bailian.console.aliyun.com/cn-beijing/costing-balance/usage-statistics)
   - 监控告警：[模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry) → 运维管理 > 模型监控
   - 告警规则：[模型告警](https://bailian.console.aliyun.com/cn-beijing/model/alert)
   - 日志：监控概览页 → 模型列表点击「查看日志」

2. **快速上手**：
   - 在监控概览页，点击目标模型的 **查看详情** 进入监控详情页，图表中带蓝色铃铛图标（✅）的指标可一键配置告警；
   - 在用量页，使用右上角搜索框输入模型 Code（如 `qwen-plus`）快速定位用量；
   - 首次配置告警前，**必须先完成云监控服务角色授权**（入口在监控概览页左上方「模型监控投递」），否则创建按钮置灰 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)；
   - 开启推理日志需先开启审计日志投递，并确保地域为北京或新加坡（其他地域暂不支持）。

3. **推荐实践**：
   - 为 `模型消耗 TotalToken 数` 配置环比突增告警（防成本失控）；
   - 为 `调用失败率` 和 `限流错误次数` 配置告警（保障可用性）；
   - 结合「免费额度用完即停」开关与用量趋势图，主动管理试用期资源 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

## 限制和注意事项

- **数据延迟**：用量统计延迟约 **1 小时**；监控数据延迟为 **分钟级**；审计日志查询最长支持 **30 天**，用量统计不支持查询 **30 天以前**数据。
- **权限与地域限制**：
  - 推理日志仅支持 **北京、新加坡** 地域；
  - 监控与告警按**业务空间**隔离，不可跨空间查看或配置；
  - 批量操作（如批量开关「免费额度用完即停」）需账号已绑定有效支付方式，否则失败。
- **告警依赖项**：
  - 告警规则创建前必须完成**云监控服务角色授权**，授权后将自动开通云监控、SLS 及 Prometheus（按实际用量计费）；
  - 仅指标表中标注“可配置告警”的指标（如失败率、TotalToken 数）支持告警，`RPM`、`TPM`、`内容安全错误次数` 等不支持 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
- **日志风险提示**：
  - 关闭审计日志投递将**同步关闭推理日志投递**，且关闭期间日志**无法补录**；
  - SLS 侧禁止删除百炼创建的日志库或修改索引，否则导致投递失败；
  - 推理日志中 Prompt/Response 超过 128KB 将被截断，需通过原始 API 调用日志获取完整内容。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


