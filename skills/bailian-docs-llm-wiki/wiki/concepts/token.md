# Token

Token 是百炼平台中用于计量模型计算资源消耗的核心计费与性能单位，代表模型在处理输入（Prompt）和生成输出（Response）过程中所消耗的文本/[多模态](multi-modal.md)语义单元数量。一个 Token 通常对应一个子词（subword）、标点、空格或图像/音频中的语义片段，其具体粒度由底层模型分词器（Tokenizer）决定。

## 在百炼平台的不同场景中，这个概念如何使用

- **计费计量**：所有模型调用均按 `TotalToken`（输入 Token 数 + 输出 Token 数）计费。账单 API（`GetBillingTrend` / `GetBillingOverview`）支持按 `BASE_MODEL` 等维度聚合 Token 消耗，是成本分析与预算管控的基础指标。
- **性能监控**：模型监控系统实时统计并展示 `TotalToken 数`，支持配置环比突增告警，帮助识别异常调用（如 Prompt 注入、循环生成）或低效提示工程。
- **API 请求控制**：文本生成类模型（如 `qwen-max`）通过 `parameters.max_tokens` 限制**最大输出 Token 数**，防止无限生成；该参数对视觉/语音生成模型语义不同（如表示分辨率），需按模型类型分别理解。
- **用量配额管理**：API Key 的 QPM（每分钟请求数）限制间接约束 Token 吞吐，而 Token 级细粒度限流（如 per-model TPM）当前由平台后台动态调控，不开放用户配置。
- **审计日志记录**：所有成功/失败调用的审计日志均包含 `input_tokens` 和 `output_tokens` 字段（即使响应为空），可用于精准归因与用量回溯，且**不包含原始 Prompt/Response 内容**，保障数据安全。

## 关键参数和配置

| 参数/字段 | 所属场景 | 说明 |
|-----------|----------|------|
| `parameters.max_tokens` | 模型调用（文本类） | 控制生成响应的最大 Token 数，取值范围通常为 `1–8192`（依模型能力而异），超出将被截断并返回 `truncated` 标志。 |
| `input_tokens` / `output_tokens` | 审计日志、监控指标 | 只读字段，由平台自动计算并返回，不可写入请求。文本模型中二者均为整数；[多模态](multi-modal.md)模型中可能为浮点（如音频时长映射为等效 Token）。 |
| `TotalToken 数` | 账单与监控 | 计费与监控口径统一为 `input_tokens + output_tokens`，四舍五入到整数，精确到个位。 |

> ⚠️ 注意：  
> - `max_tokens` **仅限制输出长度**，不影响输入 Token 计数；超长 Prompt 将直接触发 `400 Bad Request`（`InputTooLong` 错误），而非被截断。  
> - 嵌入模型（`text-embedding-v3`）不返回 `output_tokens`（因其无“生成”行为），但 `input_tokens` 仍计入总消耗。  
> - [异步任务](asynchronous-task.md)（如图像生成）的 Token 统计在任务完成时一次性上报，轮询查询中间状态不产生 Token 计量。

## 面向开发者，简洁实用

- ✅ **必查**：调用后检查响应中的 `usage.input_tokens` 和 `usage.output_tokens`（Python SDK 中为 `response.usage.input_tokens`），用于本地用量校验与缓存策略（如预估成本）。  
- ✅ **必监**：在模型监控中为 `TotalToken 数` 配置「7日同比上涨 >50%」告警，快速发现 Prompt 泄露、重试风暴或恶意刷量。  
- ✅ **必算**：估算成本时，以 `1,000 Tokens ≈ ¥0.005` 为基准（以官网最新定价页为准），结合 `max_tokens` 设置合理上限，避免意外超支。  
- ❌ **勿混淆**：`DASHSCOPE_API_KEY` 是身份凭证，与 Token 无关；`Token` 是资源度量单位，不是认证凭据。  
- ❌ **勿硬编码**：`max_tokens` 应根据业务场景动态设置（如摘要设 `512`，代码补全设 `2048`），避免全局固定高值。

## 关联主题页

- [preparations](../api/preparations.md)
- [model experience](../guides/model-experience.md)
- [model monitoring](../guides/model-monitoring.md)
- [more about models](../api/more-about-models.md)
- [billing api](../api/billing-api.md)


