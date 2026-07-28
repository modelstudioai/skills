# model monitoring

阿里云百炼提供两套互补的用量与运行观测能力：**模型用量**页面按[业务空间](../concepts/workspace.md)统计各模型的调用量、Token 消耗与费用概览；**模型监控**则聚焦运行时指标（延时、失败率、RPM/TPM 等）、调用日志与主动告警，并支持通过 Prometheus HTTP API 接入 Grafana 或自建应用。两者结合可覆盖成本管理、性能观测与故障排查的完整链路。

## 支持范围

- **用量统计**：模型列表中的所有模型均支持查看用量，包括基于它们调优后的自定义模型，详见[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)。
- **普通监控**：支持所有模型（含调优后的自定义模型），数据延迟为**小时级**。
- **高级监控**：支持北京、上海、新加坡、弗吉尼亚地域下的所有模型，提供**分钟级**数据洞察（收费功能）。
- **告警功能**：支持北京、新加坡、弗吉尼亚地域。
- **推理日志（请求/响应记录）**：仅适用于北京、新加坡、弗吉尼亚地域的**部分模型**（如 qwen3-max、qwen-plus 系列、qwen-flash、qwen-turbo、qwen3-coder 系列、部分 Qwen3 开源模型及 deepseek-v3.1/v3.2 等）；不支持的模型界面会提示"当前模型暂不支持日志"。

## 查看模型用量与免费额度

在控制台**模型用量**页面按[业务空间](../concepts/workspace.md)维度查看（不支持按阿里云账号维度统计；如需账号级 Token 总量，需在账单详情页导出账单查看）。关键规则：

- 数据延迟约 **1 小时**；不支持查看 **30 天以前**的数据，更早数据到费用与成本页面查询。
- 时间精度支持分钟/小时/天：跨度超 1 天不可选分钟，超 7 天仅支持按天。
- 仅「大语言模型」页签支持按推理类型（实时推理/批量推理）筛选；支持按 API-KEY 筛选。
- 统计单位随模型类型不同：文本/深度思考/视觉理解/全模态/向量模型按 **Token**，图像生成按**张**，视频生成按**秒**，语音模型按秒、字符或 Token（视模型而定）。

免费额度页面可查看各模型免费额度剩余量与过期时间，并可单个或批量切换**免费额度用完即停**开关（开启后额度用尽时返回 403 错误 `AllocationQuota.FreeTierOnly`）。

> **注意**：「免费额度用完即停」只能在仍有未消耗免费额度时开启；开启后若要关闭，需等免费额度完全消耗后才能操作。

## 监控模型运行

系统自动采集主账号下所有[业务空间](../concepts/workspace.md)的模型调用数据，按"模型 + 业务空间"维度生成[模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)列表。默认业务空间成员可查看所有业务空间数据；子业务空间成员仅能查看当前空间。

点击操作列**监控**可查看 4 类指标：

| 类别 | 示例指标 |
| --- | --- |
| 安全 | 内容安全错误次数（被内容安全服务拦截） |
| 成本 | 平均单次请求调用量、Token 消耗 |
| 性能 | 调用时长、首 Token 延时、非首 Token 延时、RPM、TPM |
| 错误 | 失败次数、失败率、[限流](../concepts/rate-limit.md)错误次数（429） |

调用统计支持按 API-KEY、推理类型、时间范围与时间精度（分钟/小时）筛选，失败次数图表可点击**失败详情**定位失败原因。

## 查看 Token 消耗与历史对话（日志）

- **历史 Token 消耗**：监控详情页调用量区域可查最近 30 天；更早数据到费用与成本页面查询。
- **单次调用 Token 消耗 / 请求与响应内容**：需先在**模型监控配置**中开通审计日志和推理日志，随后在**日志**页签查看每次实时推理调用的 Request ID、调用时长、状态码、错误码、用量、请求和响应。
- 推理日志从调用发生到可查询存在**分钟级**延迟；普通监控用量汇总为**小时级**延迟，高峰期可能达 1-2 小时。
- **仅记录开启推理日志后**的调用，开通前的历史调用无法补录追溯。

## 建立主动告警

针对静默失败（超时、Token 消耗突增等）可设置主动告警，步骤：

1. 在模型监控配置中开启**高级监控**（性能和用量指标监控）。
2. 在模型告警页面创建告警规则，选择模型和监控模板。

通知方式支持短信、邮件、电话、钉钉群机器人、企业微信机器人及 Webhook。告警等级固定为四级（不支持自定义）：紧急（电话/短信/邮件）、错误（短信/邮件）、警告（短信/邮件）、普通（邮件）。

## 接入 Grafana 与自建应用

高级监控数据存储在私有 Prometheus 实例中，支持标准 Prometheus HTTP API。使用方式：

1. 开启高级监控后，在模型监控配置中获取 Prometheus 实例的 HTTP API 地址（区分公网/VPC）。
2. 以 `Authorization: Basic base64(AccessKey:AccessKeySecret)` 鉴权调用 `query_range` 等接口，AccessKey 必须与 Prometheus 实例归属同一阿里云账号。

```
GET {HTTP API}/api/v1/query_range?query=model_usage{workspace_id="llm-xxxx",model="qwen-plus"}&start=2025-11-20T00:00:00Z&end=2025-11-20T23:59:59Z&step=60s
```

可用指标包括 `model_call_count`、`model_call_duration`（含 p50/p99）、`model_first_token_duration`、`model_generation_duration_per_token`、`model_usage`、`model_tps_per_request`（仅高级监控）等；过滤条件（LabelKey）支持 `user_id`、`apikey_id`（-1 表示控制台调用）、`workspace_id`、`model`、`protocol`（HTTP/SSE/WS）、`sub_protocol`（DEFAULT/ASYNC）。

> **注意**：TPS（`model_tps_per_request`）与非首包时长呈倒数关系（TPS ≈ 1 ÷ 非首包时长均值），且 TPS [限流](../concepts/rate-limit.md)按请求维度，区别于 TPM 的按账号维度[限流](../concepts/rate-limit.md)；排查响应慢时应结合首 Token 延时、非首 Token 延时与输入 Token 量综合分析。

## 成本控制建议

按[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)的生产环境建议：

- 合理设置 `max_tokens` 并限制思考长度，控制单次输出成本。
- 简单任务（分类、摘要）优先选轻量级模型。
- 通过[模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)配置用量告警，及时发现异常消耗。
- 优化 Prompt 减少输入 Token；非实时大批量任务改用批量推理。

## 限制和注意事项

- 用量数据按业务空间统计，账号级汇总需导出账单。
- 用量统计数据延迟约 1 小时，且仅保留 30 天。
- 高级监控为收费功能，且有地域限制；推理日志仅覆盖部分模型。
- 告警等级与通知渠道映射固定，不支持自定义新增或修改。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)


