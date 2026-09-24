# Token

Token 是百炼平台中用于计量模型输入与输出文本单元的最小计费与配额控制单位。它并非严格等同于自然语言中的“词”或“字”，而是由模型 tokenizer 对原始文本进行分词（tokenization）后生成的整数 ID 序列，其数量直接决定 API 调用的资源消耗、费用结算与额度占用。

## 在百炼平台的不同场景中，这个概念如何使用

- **配额与计费（Token Plan）**：Token 是 `plan` 配额机制的核心计量维度。每次调用（如 `/v1/chat/completions`）的实际 `input_tokens + output_tokens` 消耗，将实时扣减所选 Token Plan（如 `team`、`coding`）的当日额度，并按标准计费规则计费。未显式指定 `plan` 时，系统按账户默认 plan 执行配额检查。

- **可观测性与监控（Model Monitoring）**：`TotalToken 数` 是用量统计与性能告警的关键指标。控制台「模型用量」页面按模型、API Key、时间粒度聚合 Token 消耗；「模型监控」支持对 `TotalToken 数`、`429 限流次数` 等 Token 相关指标配置阈值告警，辅助成本优化与稳定性治理。

- **评测与评估（Model Evaluation / AgentEval）**：在模型评测任务中，被评测模型的推理调用（`EvaluationSet → model inference`）和裁判模型的评分调用（`LLM Grader`）均按实际消耗 Token 计费；AgentEval 的 Trace 数据中，每个大模型调用 Span 明确记录 `input_tokens` 和 `output_tokens`，用于分析质量-成本权衡。

- **开发调试与预估（Tokenize API）**：通过 `/v1/tokenize` 接口可提前获取文本的 `input_tokens` 数量，用于预判单次请求是否超限（如 `personal` Plan 单次上限为 32k），避免因超限返回 `400 Bad Request` 或 `429 Too Many Requests`。

- **异步与多模态任务**：图像/视频/语音类异步模型虽不以 Token 为主要输出形式，但其 [prompt](../guides/prompt.md) 输入部分仍按文本 Token 计量；多模态模型（如 `qwen-vl-plus`）的文本输入、OCR 结果、描述文本等均参与 Token 计算。

## 关键参数和配置

- `plan`（字符串，必填）：指定 Token 配额策略，取值为 `"personal"`、`"team"` 或 `"coding"`；影响单次上限（32k / 64k / 16k）、日额度及计费单价。
- `max_tokens`（整数，可选）：限制模型输出最大 Token 数，是控制成本与延迟最直接的参数；建议根据业务需求显式设置，避免无约束生成导致超额消耗。
- `input_tokens` / `output_tokens`（只读）：由服务端在 `/v1/tokenize` 或完整调用响应中返回，不可手动设置；实际计费与配额扣减以服务端统计为准。
- `stream=true`：流式响应不影响 Token 总量计算，`input_tokens + output_tokens` 仍为完整会话总消耗。

> ⚠️ 注意：`plan=free` 已废弃（v2.3.0+ 返回 400）；`plan` 参数不参与缓存，相同请求可能因额度耗尽而失败；Token 计算逻辑由目标模型的 tokenizer 决定，不同模型（如 `qwen-max` vs `qwen2-7b-instruct`）对同一文本的 Token 数可能不同。

## 面向开发者，简洁实用

- ✅ **务必显式传 `plan`**：避免依赖默认值，确保配额行为可预期；多业务线建议用不同 plan 隔离额度。
- ✅ **用 `/v1/tokenize` 预估再调用**：尤其在长 Prompt 或高并发场景，预防超限失败。
- ✅ **设 `max_tokens`**：输出长度可控 = 成本可控；结合业务逻辑设定合理上限（如摘要 ≤ 512，代码补全 ≤ 2048）。
- ✅ **监控 `TotalToken 数` + `429 次数`**：二者联动可快速定位是配额不足（429 高 + TotalToken 接近上限）还是突发流量（429 高 + TotalToken 未达上限）。
- ❌ **不要硬编码永久 API Key**：前端调用请用临时 Token（`expire_in_seconds` ≤ 300），避免密钥泄露导致 Token 被恶意刷爆。
- ❌ **不要假设 Token 数跨模型一致**：测试阶段需用目标模型实测 `tokenize`，而非仅参考文档示例。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [agenteval](../guides/agenteval.md)
- [model monitoring](../guides/model-monitoring.md)
- [model evaluation introduction](../guides/model-evaluation-introduction.md)
- [more about models](../api/more-about-models.md)


