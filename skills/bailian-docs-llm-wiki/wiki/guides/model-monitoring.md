# model monitoring

百炼平台围绕"模型调用量与运行状态"提供两套互补能力：**模型用量**按[业务空间](../concepts/workspace.md)汇总[计费](../concepts/billing.md)用量（[Token](../concepts/token.md)/张/秒），用于成本核算；**模型监控**提供分钟级运行指标、调用日志、[Token](../concepts/token.md) 追踪与主动告警，用于稳定性保障。前者数据延迟约 1 小时且统计口径偏账单，后者普通监控同样为小时级、高级监控可达分钟级。详见[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)与[模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

## 适用范围与支持的模型

- **用量统计**：模型列表中的所有模型均支持查看用量，包括基于它们调优后的自定义模型，统计粒度见下表。
- **模型监控**：
  - 普通监控支持所有地域的所有模型（含调优后的自定义模型）。
  - 高级监控支持北京、新加坡、弗吉尼亚地域下的所有模型。
  - 告警功能仅支持北京、新加坡地域下的所有模型。
- **日志/历史对话**：仅适用于华北2（北京）地域的部分模型，详见后文支持清单。

## 用量统计单位

不同模型的用量统计口径与[计费](../concepts/billing.md)维度如下（详见[模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)）：

| 模型类型 | 统计单位 | [计费](../concepts/billing.md)说明 |
| --- | --- | --- |
| 大语言模型（文本生成/深度思考/视觉理解） | [Token](../concepts/token.md) | 按输入和输出对应的 [Token](../concepts/token.md) 数[计费](../concepts/billing.md) |
| 视觉模型·图像生成 | 张 | 按成功生成的图像张数[计费](../concepts/billing.md) |
| 视觉模型·视频生成 | 秒 | 按成功生成的视频秒数[计费](../concepts/billing.md) |
| 语音模型（TTS/ASR/音视频翻译等） | 秒、字符或 [Token](../concepts/token.md) | 视模型而定，可能按时长、字符数或 [Token](../concepts/token.md) 数 |
| 全模态模型 | [Token](../concepts/token.md) | 文本与其他模态均按 [Token](../concepts/token.md) 数[计费](../concepts/billing.md) |
| 向量模型 | [Token](../concepts/token.md) | 按输入文本的 Token 数[计费](../concepts/billing.md) |

> **注意**：用量数据按**[业务空间](../concepts/workspace.md)**维度统计，**不支持按阿里云账号维度统计**。如需账号级 Token 总量，需用主账号在费用与成本页面导出账单查看。

## 查看用量与费用概览

### 模型用量页

进入**模型用量**页面，选择模型类型页签（如"大语言模型"）和统计时间范围，页面汇总该推理类型下所有已调用模型的用量。关键限制：

- 数据延迟约 1 小时。
- 不支持查看 **30** 天以前的统计数据，更早数据需到费用与成本页面查询。
- 仅"大语言模型"页签支持按推理类型（实时推理 / 批量推理）筛选；空间下从未产生批量推理用量时下拉框只显示"实时推理"。
- 可在右侧搜索框输入模型名称（如 `qwen-plus`）筛选具体模型。

### 费用概览页

费用概览页提供：费用卡片（当前账期总消费金额、订阅购买费用、账单费用，可跳转明细）、账单趋势图表（按月或按天、可按产品分类/[API Key](../concepts/api-key.md) ID/模型筛选）、以及费用告警设置入口。

### 免费额度管理

在**免费额度**页面可查看各模型免费额度使用情况，并提供**免费额度用完即停**开关：

- 开启后，免费额度用尽时服务自动停止，返回 `403 AllocationQuota.FreeTierOnly`，避免产生免费额度以外的费用。
- 仅在账户内仍有未消耗的免费额度时才能开启；关闭需等免费额度完全消耗后进行。
- 控制台免费额度数据分钟级更新，以控制台显示为准。

## 监控模型运行

系统自动采集主账号下所有[业务空间](../concepts/workspace.md)内的模型调用数据，列表按"模型 + [业务空间](../concepts/workspace.md)"维度生成，新模型在首次数据同步完成后自动加入列表（普通监控延迟通常为小时级，高级监控为分钟级）。

**监控数据看板**汇总：模型总量、总调用次数、总失败次数、平均调用时长、平均首包时长。

**模型监控表格**列出各模型的模型 Code、[业务空间](../concepts/workspace.md)、调用总量、调用失败量、失败率、平均调用时长、平均首包时长（除模型 Code、[业务空间](../concepts/workspace.md)外均可排序），操作列提供**监控**、**日志**入口。

> 默认[业务空间](../concepts/workspace.md)成员可查看所有[业务空间](../concepts/workspace.md)的模型调用情况；子[业务空间](../concepts/workspace.md)成员仅能查看当前空间数据，无法切换查看其他业务空间。

进入目标模型的**监控**详情页后，可查看 4 类监控指标：

- **安全**：识别违规内容，如内容安全错误次数。
- **成本**：评估成本效益，如平均单次请求调用量。
- **性能**：观察性能变化，如调用时长、首 Token 延时、RPM、TPM、非首 Token 延时。
- **错误**：判断稳定性，如失败次数、失败率、限流错误次数（429）、内容安全错误次数。

调用统计页签支持按 API-KEY、推理类型、时间范围、时间精度（分钟/小时）筛选；失败次数图表可点击"失败详情"查看失败明细。

## 查看 Token 消耗

模型监控提供三个层次的成本管理能力（详见[模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)）：

- **汇总**：按业务空间维度汇总历史 Token 消耗，可按时间范围和 [API Key](../concepts/api-key.md) 筛选；调用统计页签的"调用量"区域可查看最近 30 天的 Token 消耗。
- **追踪**：记录每一次模型调用的 Token 消耗（需开通推理日志，仅北京地域部分模型）。
- **告警**：设置 Token 消耗阈值，异常消耗时立即告警。

更早的用量需在费用与成本页面查询。

## 查看历史对话（模型日志）

该功能仅适用于华北2（北京）地域的部分模型，是故障排查和内容审计的关键工具。

**步骤一：开通日志**——主账号（或拥有足够权限的子账号）在模型监控（北京）页面点击右上角"模型监控配置"，依次开通审计日志和推理日志。开通后系统开始记录每次调用的输入与输出，存在分钟级延迟；停止记录只需关闭推理日志。

**步骤二：查看历史对话**——在列表中找到目标模型，点击操作列"日志"，日志页签展示实时推理调用记录，"请求和响应"字段分别对应输入与输出，"用量"字段为本次调用的 Token 消耗。

**支持请求和响应记录的模型清单**（节选）：

- 千问 Max：qwen3-max 及快照版本、qwen-max
- 千问 Plus：qwen3.7-plus / qwen3.6-plus / qwen3.5-plus / qwen-plus 及各自快照版本
- 千问 Flash：qwen3.5-flash、qwen-flash 及快照版本
- 千问 Turbo：qwen-turbo
- 千问 Coder：qwen3-coder-flash、qwen3-coder-plus 及快照版本
- 开源模型：qwen3-235b-a22b 系列、qwen3-30b-a3b 系列、qwen3-next-80b-a3b 系列、qwen3-coder-480b-a35b-instruct 等
- 三方模型：deepseek-v3.1、deepseek-v3.2、deepseek-v3.2-exp

## 建立主动告警

该功能仅适用于新加坡和华北2（北京）地域，用于发现超时、Token 消耗突增等静默失败。

**步骤一：开启高级监控**——主账号（或子账号）在模型监控（北京或新加坡）页面点击"模型监控配置"，在高级监控区域手动开启"性能和用量指标监控"。

**步骤二：创建告警规则**——在模型告警页面点击"创建告警规则"，选择要监控的模型和监控模板后创建。

- **通知方式**：短信、电子邮件、电话、钉钉群机器人、企业微信机器人、Webhook。
- **告警等级**（不可自定义新增或修改）：
  - 紧急（CRITICAL）：电话、短信、邮件
  - 错误（ERROR）：短信、邮件
  - 警告（WARNING）：短信、邮件
  - 普通（INFO）：邮件

## 接入 Grafana 与自建应用

高级监控的指标数据存储在私有 Prometheus 实例中，支持标准 Prometheus HTTP API，可接入 Grafana 或自建应用。

**步骤一：获取数据源 HTTP API 地址**——确保已开启高级监控，在模型监控（北京/弗吉尼亚/新加坡）页面点击"模型监控配置"，在云监控 Prometheus 实例右侧"查看详情"，根据客户端网络环境（公网或 VPC）复制对应 HTTP API 地址。

**步骤二：调用 HTTP API**——使用 Basic 认证（`AccessKey:AccessKeySecret` Base64 编码），AccessKey 需与 Prometheus 实例归属同一阿里云账号。查询示例：

```
GET {HTTP_API}/api/v1/query_range?query=model_usage&start=2025-11-20T00:00:00Z&end=2025-11-20T23:59:59Z&step=60s
Accept: application/json
Content-Type: application/json
Authorization: Basic base64Encode(AccessKey:AccessKeySecret)
```

可通过 `{}` 包裹过滤条件，如 `model_usage{workspace_id="xxx",model="qwen-plus"}`。

**主要监控指标**：`model_call_count`（调用次数）、`model_call_duration[_total/_p50/_p99]`（调用时长）、`model_first_token_duration[_total/_p50/_p99]`（首包时长）、`model_generation_duration_per_token[_total/_p50/_p99]`（非首包时长）、`model_usage`（用量总和）。

**支持的过滤条件（LabelKey）**：`user_id`、`apikey_id`（-1 表示控制台调用）、`workspace_id`、`model`、`protocol`（HTTP/SSE/WS）、`sub_protocol`（DEFAULT/ASYNC）、`status_code`、`error_code`（仅 `model_call_count` 支持）、`usage_type`（仅 `model_usage` 支持，如 total_tokens/input_tokens/output_tokens/cache_tokens/image_tokens/audio_tokens/video_tokens/image_count/audio_count/video_count/duration/characters/audio_tts/times）。

**接入 Grafana**：在 Grafana 中添加 Prometheus 数据源，填入上述 HTTP API 地址与 Basic 认证信息即可（以 Grafana 10.x 为例，其他版本参考 Grafana 官方文档）。

## 生产环境用量管理建议

- **控制模型输出长度**：合理限制思考长度并设置 `max_tokens`，控制单次生成最大长度。
- **按任务选型**：分类、摘要等简单任务优先用成本更低的轻量级模型。
- **监控与告警**：通过模型监控监控用量趋势并配置告警。
- **优化 Prompt**：简洁清晰的 Prompt 既提升质量又减少输入 Token。
- **使用批量推理**：非实时、大批量任务用批量推理通常更具成本优势。

## Token 与推理类型说明

- **Token**：大模型处理输入输出的单位。经验值：1 个汉字约 1.5-2 个 Token，1 个英文字母约 0.25 个 Token，1 个英文单词约 1.3 个 Token。每个模型都有最大输入/输出 Token 限制，超出会请求失败。
- **实时推理**：对模型的所有直接和间接调用，包括 API 调用、模型广场、百炼应用（智能体/工作流）的测试态和发布态、Assistant API、应用调用、Prompt 反馈优化、模型[评测](../concepts/evaluation.md)等。
- **批量推理**：通过 OpenAI 兼容-Batch（文件输入）接口以离线方式进行的大规模数据处理。

## 来源文档

- [模型用量](../../raw/model-user-guide/model-monitoring/model-usage-statistics.md)
- [模型监控](../../raw/model-user-guide/model-monitoring/model-telemetry.md)






