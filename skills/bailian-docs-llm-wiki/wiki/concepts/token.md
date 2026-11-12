# Token

Token 是百炼平台对模型输入与输出内容进行细粒度计量的基本单位，用于计费、资源调度、性能监控和容量规划。它并非固定字符数，而是由模型 tokenizer 实际切分出的语言单元（如子词、标点、控制符等），同一段文本在不同模型下产生的 Token 数可能不同。

## 在百炼平台的不同场景中，这个概念如何使用

- **实时推理与批量调用**：所有文本生成、对话、代码补全等请求均按实际消耗的输入 Token 和输出 Token 分别计费；Batch 调用单价为实时推理的 50%，但 Token 计量逻辑完全一致。
- **向量与排序服务**：Embedding 模型按输入文本总 Token 数计费（支持单次最多 128,000 Token）；Rerank 模型按 `query + documents` 的总 Token 数计费（文档数 × 平均每文档 Token 数）。
- **知识库（RAG）**：向量化阶段（Query/Document）和重排序（Rerank）阶段均产生独立 Token 消耗，且多知识库并行查询会导致 Token 费用线性叠加。
- **模型训练与部署**：训练费用 = 总训练 Token 数 × 训练轮数；部署计费中的吞吐预留（TPM）以每分钟可处理的 Token 数（kTPM）为单位，输入/输出 TPM 分开报价。
- **监控与用量分析**：`模型消耗 TotalToken 数` 是核心用量指标，支持告警配置，用于识别成本突增或异常调用；监控数据中的 Token 统计与账单计费结果一致，但存在约 1–2 分钟延迟。

## 关键参数和配置

- **Token 计量方式**：输入 Token 与输出 Token 独立计费，免费额度为二者共用总额度；思考模式（Chain-of-Thought）、缓存命中、Batch 调用等均不改变 Token 实际数量，仅影响单价或折扣系数。
- **TPM（Tokens Per Minute）**：吞吐预留的核心单位，1 kTPM = 1,000 Tokens/分钟；输入按万TPM（10 kTPM）报价，输出按千TPM（1 kTPM）报价；长输入或缓存命中会折算实际占用的 kTPM 容量。
- **阶梯计费触发**：部分模型（如 `qwen3.7-plus`）按单次请求**输入 Token 总量**分档定价，该次请求所有 Token 均按最高档单价结算。
- **地域因子影响**：同一模型在不同地域的 Token 单价不同（如 `qwen3.8-max` 华北2为 ¥12/百万输入 Token，美国弗吉尼亚为 ¥14.988），且免费额度仅限华北2（北京）生效。
- **异步任务计量**：异步接口（如 `text-embedding-async-v1`、生图/生视频）按任务实际完成时的 Token 消耗结算，费用出账略有延迟，需注意预算控制边界。

## 面向开发者，简洁实用

- ✅ **务必校验 Token 数**：调用前使用 SDK 的 `count_tokens()` 方法（如 DashScope Python SDK 的 `dashscope.get_tokenizer().count_tokens(text)`）预估消耗，避免超预算。
- ✅ **优化输入结构**：精简 Prompt、移除冗余空格/注释、合理设置 `max_tokens`，可直接降低输出 Token 成本；知识库检索中调低 `topk_vector` 可减少 Rerank 阶段 Token 消耗。
- ✅ **善用缓存与 Batch**：对重复或相似输入启用上下文缓存（显式/隐式），或改用 Batch 接口，可显著摊薄单 Token 成本。
- ⚠️ **注意免费额度边界**：免费额度**仅抵扣实时推理调用产生的 Token 费用**，不覆盖模型训练、部署、吞吐预留、Agent 运行时、ParseX 解析等任何其他计费项。
- ⚠️ **警惕 Token 放大风险**：Flow Agent 中多路径触发同一模型节点、挂载多个知识库、未关闭 Rerank 等，均会导致 Token 消耗非线性增长——建议通过 `/usage/summary` API 或控制台「用量」页面定期核查明细。

## 关联主题页

- [test 1](../guides/test-1.md)
- [agent billing](../guides/agent-billing.md)
- [vector and sort](../api/vector-and-sort.md)
- [billing api](../api/billing-api.md)
- [model monitoring](../guides/model-monitoring.md)


