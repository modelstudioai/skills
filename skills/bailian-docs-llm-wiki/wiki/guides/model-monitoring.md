# model monitoring

百炼平台的 model monitoring 是面向生产环境的模型调用可观测性能力，提供分钟级延迟的实时监控、多维指标分析、告警配置及日志审计功能。它与模型用量统计（计费依据）分离，数据仅供运维排查与性能优化参考；所有监控数据按业务空间隔离，不跨空间聚合。核心能力覆盖调用健康度、性能瓶颈、异常突增等典型运维场景。

## 支持的模型/功能

- **支持范围**：绝大多数百炼内置模型（文本生成、深度思考、视觉理解、全模态、向量模型等）均支持基础监控；但语音、图片/视频生成及三方直连类模型部分能力受限，具体以控制台实际展示为准 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
- **核心功能模块**：
  - **监控概览与详情**：查看整体调用规模（总次数、失败率、平均时长）、单模型细粒度指标趋势；
  - **审计日志**：默认开启，记录 Request ID、模型、[Token](../concepts/token.md) 用量、状态码、首 [Token](../concepts/token.md) 延时等元数据，**不含 Prompt/Response**；
  - **推理日志**：需手动开启并配置日志投递，记录完整 Prompt/Response 及中间步骤，当前仅支持北京、新加坡地域 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)；
  - **告警管理**：支持基于预置或自定义模板为关键指标配置告警规则，如失败率、限流次数、Total[Token](../concepts/token.md) 数等；
  - **数据投递**：可将监控指标投递至云监控 Prometheus 实例，或将日志投递至 SLS 日志库，用于长期留存或对接自有运维系统。

> **注意**：文档 1 中提到“失败次数、失败率、限流错误次数已移至[模型监控](raw/model-user-guide/model-monitoring/model-telemetry.md)页面”，而文档 2 明确说明这些指标属于 `model-telemetry.md` 范畴，二者一致；但文档 1 的标题“模型用量”易引发混淆，实际该文档主体描述的是**计费用量**，其内容与 `model-telemetry.md` 所述的**非计费监控**属不同体系 —— 前者用于对账（[模型用量 (raw/model-user-guide/model-monitoring/model-usage-statistics.md)](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)），后者用于运维（[监控告警 (raw/model-user-guide/model-monitoring/model-telemetry.md)](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。

## 关键参数

| 参数名 | 含义 | 是否支持告警 | 说明 |
|--------|------|----------------|------|
| `调用次数` | 模型被调用的总次数 | ✅ | 随业务波动，可用于容量规划 |
| `失败次数` / `失败率` | 请求失败数及占比 | ✅ | 排查可用性问题的首要指标 |
| `限流错误次数`（429） | 触发限流的请求次数 | ✅ | 直接反映配额或吞吐瓶颈 |
| `调用时长` | 端到端响应时间 | ✅ | 衡量整体服务延迟 |
| `首 Token 延时` | 首 Token 返回耗时 | ✅ | 关键性能指标，影响用户体验 |
| `模型消耗 TotalToken 数` | 按模型维度汇总的 Token 总量 | ✅ | **推荐用于成本突增告警**，见[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md) |
| `非首 Token 延时` | 后续 Token 平均生成耗时 | ❌ | 不支持告警配置 |
| `RPM` / `TPM` | 每分钟请求数 / Token 数 | ❌ | 仅作观察，不可配置告警 |

## 使用方式

1. **访问入口**：登录百炼控制台 → 左侧导航栏 **运维管理 > 模型监控**（[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）。
2. **快速筛选**：
   - 时间范围（支持分钟/小时/天级精度，仅详情页可用）；
   - 推理类型（在线推理、Batch File、Batch Chat）；
   - API Key（仅显示当前业务空间下已创建的 Key）。
3. **配置告警**：
   - 在监控图表中点击支持告警的指标旁的 **铃铛图标**，快速创建规则；
   - 或进入 [模型告警页面](https://bailian.console.aliyun.com/cn-beijing/model/alert) → **告警规则** 页签，使用预置模板（如“模型调用失败占比1分钟总和大于1%”）一键创建；
   - **前提**：需先在“数据投递”中完成云监控服务角色授权（否则创建按钮禁用）[监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
4. **查看日志**：
   - 审计日志：默认可用，支持按 Request ID、状态码（200/4XX/5XX）、时间范围（最长30天）筛选；
   - 推理日志：需先开启审计日志投递 → 在日志页签点击“开始配置” → 授权 SLS 角色并指定日志库 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

## 限制和注意事项

- **数据延迟与范围**：监控数据延迟约 1 分钟，**不作为计费依据**；计费用量请以 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md) 页面或账单为准。
- **地域限制**：推理日志仅支持北京、新加坡地域；美国（弗吉尼亚）地域在用量统计中暂不展示调用次数。
- **告警能力限制**：仅表中明确标注 ✅ 的指标支持告警；`内容安全错误次数`、`RPM`、`TPM` 等指标虽可见，但无法配置告警 [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。
- **权限与依赖**：
  - 开启告警需先授权云监控服务角色（自动开通云监控、SLS、Prometheus）；
  - 开启推理日志必须先开启审计日志投递，且关闭审计投递将同步关闭推理投递；
  - SLS 日志库禁止删除或修改索引，否则导致投递失败。
- **模型兼容性**：语音、视频生成等部分模型的监控能力不完整，控制台中若某模型无监控图表或指标缺失，即表示不支持。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [监控告警](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


