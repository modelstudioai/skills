# model monitoring

百炼平台的 model monitoring 是面向生产环境的模型调用可观测性能力，提供分钟级延迟的用量统计、多维度性能指标监控、细粒度告警配置及审计/推理日志支持。该能力按业务空间隔离，数据不跨空间共享，且所有监控数据仅作运维参考，**不作为计费依据**（计费以账单为准）。核心目标是帮助开发者及时发现调用异常、性能退化与成本突增问题。

## 支持的模型/功能

- **覆盖模型范围**：所有在[模型列表](https://bailian.console.aliyun.com/cn-beijing/model/list)中可选的模型均支持基础用量查看与监控图表展示，包括大语言模型、视觉模型、语音模型、全模态模型和向量模型；但部分模型（如语音、图片、视频生成及三方直连模型）**不支持监控告警功能**，具体需在控制台实时确认 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
- **核心功能模块**：
  - **用量统计**：按模型 Code、API-Key、时间范围（最长30天）、推理类型（仅大语言模型支持区分实时/批量）聚合展示调用次数、[Token](../concepts/token.md)量、图像张数等，数据延迟约1小时 [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。
  - **性能监控**：支持调用次数、失败率、调用时长、首 [Token](../concepts/token.md) 延时、限流错误次数（429）等15+指标的实时图表化呈现，其中10项支持告警配置。
  - **日志能力**：审计日志默认开启（含 Request ID、状态码、[Token](../concepts/token.md) 用量等），推理日志需手动开启并依赖日志投递至 SLS，记录完整 Prompt/Response（长度上限128K）。
  - **告警体系**：基于预置或自定义模板配置规则，支持通知邮箱、短信等渠道；告警触发依赖云监控服务角色授权 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

> **注意**：文档1中“免费额度用完即停”功能描述为“返回403错误：AllocationQuota.FreeTierOnly”，但该错误码未在文档2的[错误码](raw/model-api-reference/preparations/error-code.md)引用路径中明确列出；实际生产中应以控制台返回的 HTTP 状态码及 `X-Error-Code` 响应头为准，避免硬编码匹配此字符串。

## 关键参数

| 参数名 | 说明 | 是否必填 | 备注 |
|--------|------|----------|------|
| `时间范围` | 支持快捷选择（1h/6h/1d/7d）或自定义，最长30天 | 是 | 模型用量页面不支持查询30天以前数据；审计日志最长支持30天查询 |
| `推理类型` | 仅「大语言模型」页签支持筛选「实时推理」或「批量推理」 | 否 | 若空间无批量推理历史，下拉框仅显示「实时推理」 |
| `API-Key` | 按 API Key ID 筛选调用来源 | 否 | 仅展示当前业务空间下已创建且未删除的 API-Key |
| `告警检查周期` | 单位为秒，默认60秒，必须为 ≥0 的整数（0 表示触发即告警） | 是 | 配置前需确保已授权云监控服务角色，否则按钮禁用 |
| `持续时间` | 告警触发需连续满足阈值的分钟数 | 是 | 例如设为5，表示指标连续5分钟超阈值才触发告警 |
| `统计周期`（告警模板） | 单位为分钟，合法范围1~10080（即7天） | 是 | 预置模板中均为1分钟统计周期 |

## 使用方式

1. **访问入口**：
   - 用量统计：[模型用量](https://bailian.console.aliyun.com/cn-beijing/costing-balance/usage-statistics)
   - 监控与告警：[模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry) → [模型告警](https://bailian.console.aliyun.com/cn-beijing/model/alert)
   - 日志：监控概览页 → 模型列表点击「查看日志」

2. **快速配置告警**：
   - 在模型监控详情页，对支持告警的指标（如「失败率」「模型消耗 TotalToken 数」）点击图表上的蓝色铃铛图标，直接打开告警规则配置侧边面板；
   - 优先选用预置模板（如「模型调用失败占比1分钟总和大于1%」），填入模型、通知对象即可生效；
   - 控制 Token 成本建议为「模型消耗 TotalToken 数」配置环比突增告警，保障可用性建议为「调用失败率」配阈值告警 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

3. **启用推理日志**：
   - 先完成[日志投递](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)配置（授权 SLS 角色 + 创建日志库）；
   - 切换至日志页面 → 推理日志页签 → 点击「开始配置」；
   - **注意**：仅北京和新加坡地域支持，其他地域暂不可用。

## 限制和注意事项

- **数据延迟与精度**：用量统计延迟约1小时；监控图表数据为分钟级聚合，但「模型用量」页面不支持按分钟精度查看超过1天的数据，超过7天仅支持按天查看。
- **地域与功能限制**：推理日志仅支持北京、新加坡地域；语音/视觉/视频生成等部分模型不支持告警配置，需以控制台实时展示为准。
- **权限与依赖**：
  - 创建告警规则前**必须授权云监控服务角色**，否则按钮不可点击；
  - 开启推理日志**必须先开启审计日志投递**，关闭审计日志投递将同步关闭推理日志投递；
  - 所有投递功能（监控至 Prometheus、日志至 SLS）开通后，将自动启用对应阿里云产品（云监控、SLS、Prometheus），按实际用量计费。
- **日志截断与安全**：推理日志中 Prompt/Response 超过128K会被截断；审计日志**不包含任何 Prompt 或 Response 内容**，仅用于调用链路追踪。
- **费用关联性**：监控数据不参与计费，用量以[费用中心账单](https://billing-cost.console.aliyun.com/)为准；免费额度使用情况可在[免费额度页面](https://bailian.console.aliyun.com/cn-beijing/costing-balance/free-quota)查看，但该页面数据分钟级更新，需手动刷新同步 [原文标题](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


