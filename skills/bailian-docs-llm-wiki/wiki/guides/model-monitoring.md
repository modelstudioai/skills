# model monitoring

阿里云百炼提供两套互补的用量与监控能力：**模型用量**（控制台聚合视图，用于查看调用量、Token 消耗和费用）与**模型监控**（面向指标、告警、日志的可观测体系）。前者侧重成本与免费额度管理，后者侧重性能、错误、安全指标的采集、告警与对话审计，二者共同覆盖从成本控制到线上运维的完整链路。

## 支持的模型与功能范围

- **用量查看**：模型列表中的所有模型均支持查看用量，包括基于它们调优后的自定义模型。详见 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。
- **模型监控**：
  - **普通监控**支持所有模型（含调优后的自定义模型），延迟通常为小时级。
  - **高级监控**支持北京、新加坡、弗吉尼亚地域下的所有模型，可提供分钟级数据洞察。
  - **告警功能**支持北京、新加坡地域下的所有模型。
- 监控可查看调用记录、指标监控与告警（Token、延时、调用时长、RPM、TPM、失败率）、以及 Token 消耗统计。详见 [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

## 用量与费用查看

数据按[业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)维度统计，不支持按阿里云账号维度统计。

- **数据延迟约 1 小时**；不支持查看 30 天以前的统计数据，更早数据需前往「费用与成本」页面查询。
- **时间精度**：支持分钟 / 小时 / 天三种精度。时间跨度超过 1 天时分钟精度不可选，超过 7 天时仅支持按天查看。
- **筛选维度**：仅「大语言模型」页签支持按推理类型（实时推理 / 批量推理）筛选；支持按 API-KEY、模型名称（如 `qwen-plus`）筛选。
- **费用概览**：可查看当前账期总消费、订阅费用、账单趋势（按月/按天，可按产品分类、API Key ID、模型筛选），并可设置**费用告警**。

不同模型的用量统计口径不同：大语言模型 / 全模态 / 向量模型按 **Token**，图像生成按**张**，视频生成按**秒**，语音模型按**秒、字符或 Token**（视模型而定）。完整口径见 [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。

## 免费额度管理

「免费额度」页面提供使用概览（按模型总数、额度充沛、使用超 50%/80%、无免费额度等维度汇总）及「即将用尽 Top 3」列表。

- **免费额度用完即停**：开启后免费额度用尽时服务自动停止（返回 `403 AllocationQuota.FreeTierOnly`），避免产生额度外费用。
- 支持批量开启/关闭、一键开启/关闭所有模型；账号未绑定有效支付方式时批量操作会失败。

> **注意**：「免费额度用完即停」只能在账户仍有未消耗免费额度时开启；一旦开启，需在免费额度完全消耗后才能关闭。控制台免费额度数据为分钟级更新，账单记录按分钟汇总，请以控制台显示数值为准。

## 监控指标与告警

在模型监控列表中点击目标模型操作列的**监控**，可查询 4 类指标：

- **安全**：如 `内容安全错误次数`（输入/输出被内容安全服务拦截）。
- **成本**：如 `平均单次请求调用量`。
- **性能**：`调用时长`、`首 Token 延时`、RPM、TPM、非首 Token 延时等。
- **错误**：`失败次数`、`失败率`，其中**限流错误次数**指因 [429 状态码](https://help.aliyun.com/zh/model-studio/error-code)导致的失败。

**创建告警**（仅限新加坡、华北2（北京）地域）：需先开启高级监控（性能和用量指标监控），再在模型告警页面创建规则。

- **通知方式**：短信、电子邮件、电话、钉钉群机器人、企业微信机器人、Webhook。
- **告警等级**：紧急（电话/短信/邮件）、错误（短信/邮件）、警告（短信/邮件）、普通（邮件），不支持自定义。

## Token 消耗与历史对话

- **历史 Token 消耗**：最近 30 天可在监控页调用统计的「调用量」区域查看；更早数据前往「费用与成本」页面。
- **单次调用 Token 消耗 / 历史对话（模型日志）**：需在「模型监控配置」中依次开通审计日志和推理日志，之后在**日志**页签查看每次调用的输入、输出与用量。开通后从调用到记录存在分钟级延迟。

> **注意**：查看某次调用的 Token 消耗及历史对话（模型日志）功能**目前仅适用于华北2（北京）地域的部分模型**，且仅覆盖特定模型/快照版本（如 qwen3-max、qwen-plus、qwen3-coder 系列、部分开源与三方模型）。详见 [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

## 接入 Grafana 与自建应用

高级监控的指标数据存储在私有 Prometheus 实例中，支持标准 Prometheus HTTP API，可接入 Grafana 或自建应用做可视化分析。

1. 确保已开启高级监控，在模型监控配置中查看 Prometheus 实例详情，按网络环境（公网/VPC）复制 HTTP API 地址。
2. 通过 `GET {HTTP API}/api/v1/query_range?query=<指标名>&start=...&end=...&step=60s` 查询，`Authorization` 需用 `Basic base64Encode(AccessKey:AccessKeySecret)`。

常用指标名包括 `model_call_count`（调用次数）、`model_call_duration`（调用时长均值）、`model_usage`（用量总和）等；可用 `{workspace_id="...",model="qwen-plus"}` 形式追加过滤条件（支持 `user_id`、`apikey_id`、`workspace_id`、`model`、`protocol`、`status_code`、`usage_type` 等 LabelKey）。

> **注意**：`status_code`、`error_code` 仅 `model_call_count` 支持；`usage_type` 仅 `model_usage` 支持。AccessKey 必须与 Prometheus 实例归属同一阿里云账号。

## 生产环境实践建议

- **控制输出长度**：合理设置 `max_tokens` 与限制思考长度以控制费用。
- **按任务选模型**：分类、摘要等简单任务优先用轻量级模型。
- **监控与告警**：通过模型监控跟踪用量趋势并配置告警。
- **优化 Prompt**：简洁清晰的 Prompt 可减少输入 Token 消耗。
- **使用批量推理**：非实时大批量任务用批量推理更具成本优势。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


