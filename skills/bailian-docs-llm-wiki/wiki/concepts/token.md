# Token

Token 是百炼平台中用于计量模型输入与输出文本（及多模态内容）处理规模的基本单位，1 个 token 通常对应一个子词（subword）或字符级单元；其实际长度取决于模型分词器（Tokenizer），例如 Qwen 系列模型中英文平均约 1 token ≈ 0.75 个单词，中文约 1–2 字/词。Token 是平台资源配额、计费、限流与监控的核心计量基准。

## 在百炼平台的不同场景中，这个概念如何使用

- **资源配额与计费（Token Plan）**：Token 消耗量是 Token Plan 的核心度量维度。`personal`、`team`、`coding` 等计划均定义了日/秒级的总 token 配额上限（如 `team` plan 默认支持 100 万 tokens/日），超出将触发 `429 Too Many Requests` 或 `403 Forbidden`。`max_tokens` 参数可显式限制单次响应 token 数，但不得突破 plan 的硬上限。

- **模型调用与推理**：所有同步/异步模型请求（如 `/v1/chat/completions`、`/v1/coding/completions`、文生图任务）均按实际消耗的 input tokens + output tokens 计费与统计。多模态模型（如 `qwen-vl-plus`）中，图像 token 当前不单独计费，仅文本部分计入 token 总量。

- **可观测性与监控**：`model monitoring` 提供细粒度 token 统计指标，包括 `input_tokens_total`、`output_tokens_total`、`total_tokens_per_request` 等，支持按小时/天、模型、API Key 等维度聚合分析，用于容量规划与成本归因。

- **安全与隔离**：临时 API Key（通过 `/api/v1/tokens` 生成）继承父 Key 的 token 配额权限，其调用产生的 token 消耗计入原账号或子空间配额；子业务空间内调用也严格按空间绑定的 token plan 执行，实现费用与用量隔离。

## 关键参数和配置

- `max_tokens`（请求体参数，可选）：控制模型生成的最大输出 token 数。若未设置，则使用模型默认值；若设置，将覆盖 plan 默认上限（但不能超过 plan 允许的硬上限）。  
- `X-Qwen-Plan`（HTTP Header，推荐）或 `plan`（JSON Body 字段）：声明本次请求归属的 Token Plan，直接决定 token 配额生效策略。  
- 监控查询参数：`metrics` 中可指定 `["input_tokens_total", "output_tokens_total"]` 等 token 相关指标；`group_by` 支持按 `model` 或 `api_key` 分组查看 token 分布。  
- 注意：`temperature`、`top_p` 等采样参数虽不直接控制 token 数，但高随机性可能延长生成过程，间接增加 output token 消耗，需在性能调优时协同考量。

## 面向开发者，简洁实用

- ✅ 始终检查响应头 `X-DashScope-Token-Usage`（如存在），它以 JSON 形式返回本次请求精确的 `"input_tokens"` 和 `"output_tokens"`，是调试与验证 token 消耗的黄金依据。  
- ✅ 在生产环境避免硬编码 `max_tokens`；建议结合业务预期长度动态设置，并预留 10%–20% buffer 防止截断。  
- ✅ 监控告警应至少配置 `total_tokens_per_request > N`（如 N=8192）和 `input_tokens_total 日环比突增 > 200%`，及时发现 prompt 异常或攻击行为。  
- ❌ 不要假设 token 数 = 字符数或字数——务必使用百炼官方 SDK（如 `dashscope.Tokenizer`）或调用 `/v1/tokenize` 接口（如开放）进行准确预估。  
- ❌ 不要复用跨 plan 的 API Key 进行 token 敏感操作（如批量微调数据预处理），配额冲突将导致静默失败或降级。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [token plan api](../api/token-plan-api.md)
- [model monitoring](../guides/model-monitoring.md)
- [more about models](../api/more-about-models.md)


