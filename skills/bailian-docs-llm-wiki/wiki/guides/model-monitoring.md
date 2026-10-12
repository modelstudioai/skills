# model monitoring

百炼平台的 model monitoring 是面向开发者的一套可观测性能力，提供分钟级延迟的模型调用统计、性能指标监控、告警配置及审计/推理日志能力，覆盖用量分析、健康度评估与异常排查全链路。所有监控数据按业务空间隔离，不跨空间聚合；监控指标与计费数据分离，**不作为计费依据**，对账请以费用中心账单为准。核心能力分为用量统计（侧重成本与配额）、实时监控（侧重可用性与性能）、告警与日志（侧重运维响应）三类，需结合使用。

## 支持的模型/功能

- **模型覆盖范围**：  
  - 所有在[模型列表](raw/model-user-guide/model-monitoring/model-usage-statistics.md)中可见的模型（含大语言模型、视觉模型、语音模型、全模态模型、向量模型）均支持用量查看与基础监控；  
  - 但部分模型（如语音/图片/视频生成、三方直连模型）**不支持监控告警功能**，具体以控制台实际可选模型为准（详见 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) 文档说明）；  
  - 调优后的模型（即部署实例）同样支持用量统计，参见 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

- **核心功能模块**：  
  - **用量统计**：按模型 Code、API-Key、时间维度聚合 [Token](../concepts/token.md) 数、图像张数、音频秒数等计费单位，支持分钟/小时/天精度；  
  - **实时监控**：提供调用次数、失败率、首 [Token](../concepts/token.md) 延时、调用时长、限流错误次数（429）等 15+ 指标图表；  
  - **告警管理**：支持基于预置模板或自定义规则为关键指标（如失败率、Total[Token](../concepts/token.md) 数、429 次数）配置阈值告警；  
  - **日志能力**：审计日志默认开启（含 Request ID、状态码、Token 用量等），推理日志需手动开启（含完整 Prompt/Response，上限 128KB）。

> **注意**：文档 1 中称“所有模型均支持查看用量”，而文档 2 明确指出“语音、图片、视频生成及三方直连等部分模型不支持监控告警”。二者无矛盾——**用量统计（文档 1）与监控告警（文档 2）是两套独立能力**，前者覆盖广，后者有模型限制。开发者需根据目标模型在控制台实际界面确认告警支持状态。

## 关键参数

| 参数类别 | 参数名 | 说明 | 是否必填 | 来源 |
|----------|--------|------|-----------|------|
| **告警规则** | 持续时间 | 告警触发需连续满足阈值的分钟数 | 必填 | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| | 告警检查周期 | 检查指标是否超阈值的时间间隔（秒），0 表示立即触发 | 必填 | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| | 模型选择 | 最多可绑定 50 个模型，用于批量监控 | 必填 | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| **用量查询** | 时间范围 | 最大支持查询最近 30 天数据；超 30 天需通过费用中心账单查询 | 限制项 | [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) |
| | 时间精度 | 分钟（≤1 天）、小时（≤7 天）、天（任意跨度） | 精度约束 | [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) |
| **日志投递** | 推理日志地域支持 | 仅北京、新加坡地域可用，其他地域暂不支持 | 限制项 | [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |

## 使用方式

1. **用量查看**：  
   - 访问 [模型用量](https://bailian.console.aliyun.com/cn-beijing/costing-balance/usage-statistics)，选择模型类型页签（如「大语言模型」），设置时间范围与精度；  
   - 使用右侧搜索框输入模型 Code（如 `qwen-plus`）快速定位；  
   - 「概览」页签提供调用成功次数 Top 10 模型卡片，支持下载。

2. **监控与告警配置**：  
   - 进入 [模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)，在模型列表点击「查看详情」进入单模型详情页；  
   - 在指标图表右上角点击 **告警铃铛图标**，快速为该指标创建告警（需已授权云监控服务角色）；  
   - 全量告警规则管理入口：[模型告警页面](https://bailian.console.aliyun.com/cn-beijing/model/alert)，支持模板复用、历史追溯。

3. **日志排查**：  
   - 审计日志：在监控概览页点击模型行「查看日志」，筛选 Request ID 或状态码（如 `429`）定位失败请求；  
   - 推理日志：需先完成 [日志投递](../../raw/model-user-guide/model-monitoring/model-telemetry.md) 配置，在日志页签切换至「推理日志」，查看完整 Prompt/Response。

## 限制和注意事项

- **数据延迟与范围**：  
  - 用量统计延迟约 **1 小时**，监控数据延迟 **分钟级**；  
  - 用量不支持按阿里云账号维度统计，仅限业务空间维度（[如何解决](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）；  
  - 用量数据最多保留 **30 天**，更早数据需导出账单查询。

- **权限与依赖**：  
  - 创建告警规则前，**必须完成云监控服务角色授权**，否则按钮禁用（[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）；  
  - 开启推理日志前，**必须先开启审计日志投递**，且仅支持北京、新加坡地域；  
  - 关闭审计日志投递将**自动关闭推理日志投递**，且关闭期间日志无法补录。

- **计费与告警差异**：  
  - 监控指标（如 `TotalToken 数`）**不作为计费依据**，仅作参考；计费以费用中心账单为准；  
  - “免费额度用完即停”功能开启后，**仅当账户仍有未消耗免费额度时才可开启**；关闭该功能需等待免费额度完全耗尽（[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）。

- **模型特异性**：  
  - 不同模型用量单位不同（Token / 张 / 秒 / 字符），详见 [模型用量统计单位说明](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)；  
  - 非首 Token 延时、RPM、TPM 等指标**不支持配置告警**，仅限预置模板覆盖的指标（如失败率、首 Token 延时）。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


