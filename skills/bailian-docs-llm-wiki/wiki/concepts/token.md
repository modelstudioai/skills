# Token 计量与管理

Token 计量与管理是百炼平台对大模型调用中输入（prompt）与输出（completion）文本进行标准化量化、实时统计、成本归因与资源调控的核心机制。它既是计费结算的原子单位，也是性能监控、限流控制和成本优化的关键依据。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型调用（基础 API / RAG 问答）**：每次请求的 `input_tokens`（Prompt 长度）与 `output_tokens`（生成内容长度）由平台自动解析并累加，计入对应模型的用量统计与账单；RAG 场景中，向量化（embedding）、重排序（rerank）、最终问答（LLM generation）各阶段均独立计量 Token，例如启用 `enable_rerank=true` 会额外触发一次 cross-encoder 模型调用，产生独立 Token 消耗。

- **Agent 运行（Managed Agents / Flow Agent）**：Agent 内部所有 LLM 节点（如规划、工具调用、总结）均按实际输入/输出 Token 精确计费；知识库检索中的 `top_k` 参数直接影响 rerank 阶段 Token 消耗——`top_k=50` 比 `top_k=10` 多消耗约 5 倍 rerank Token；多知识库挂载时，Token 消耗呈线性叠加。

- **模型生产（微调与部署）**：微调任务的训练数据量（以 Token 计）、验证集评估 Token 数影响训练时长与费用；部署后，`lora`/`mu`/`ptu_v2` 等部署模式均以实际服务调用的 `TotalToken` 为计费或配额依据；PTU（预置吞吐）容量单位 `kTPM`（千 Token/分钟）直接绑定 Token 生成速率上限。

- **监控与告警**：`模型消耗 TotalToken 数` 是核心可观测指标，支持分钟级聚合、趋势分析与阈值告警（如“单日 TotalToken 超 1000 万触发告警”），但不用于实时限流——限流基于 RPM/TPM 等策略，Token 用量仅作事后归因与成本审计。

- **计费与账单**：Token 是模型类服务的最小计费单元，费用 = 实际消耗 Token 数 × 对应模型单价（如 `qwen-plus` ¥0.02/1K tokens）；所有 Token 消耗均遵循“免费额度优先抵扣 → 资源包次之 → 后付费兜底”规则，且在 Billing API 中以 `model_type=text-generation` 等维度聚合呈现。

## 关键参数和配置

| 参数 | 所属场景 | 说明 | 开发者操作建议 |
|------|----------|------|----------------|
| `input_tokens` / `output_tokens` | 所有模型 API 响应（含 RAG `/query`） | 响应体 `usage` 字段中返回，精确到整数；`total_tokens = input_tokens + output_tokens` | 必须解析响应中的 `usage` 字段进行本地用量校验；避免依赖字符串长度估算（编码差异导致偏差）。 |
| `top_k` | RAG API、知识库配置 | 控制检索返回片段数，直接影响 rerank 模型 Token 消耗（近似正比关系） | 生产环境建议设为 `3–10`；高精度需求可设 `20`，避免盲目设 `50` 导致 rerank 成本激增。 |
| `max_length`（微调） / `max_tokens`（推理） | 微调超参、API 请求体 | 限制模型最大生成长度，硬性约束 `output_tokens` 上限 | 微调时合理设置 `max_length` 防止 OOM；推理时显式传 `max_tokens` 避免意外长输出推高费用。 |
| `kTPM`（PTU 容量） | 模型部署（`plan=ptu`） | 预置吞吐单位，1 kTPM = 1000 Tokens/分钟；决定服务最大并发生成能力 | 根据 QPS × 平均响应 Token 数预估所需 kTPM，预留 20% 余量应对峰值。 |
| `free quota`（免费额度） | 全局账户级 | 按模型类型分配（如 `qwen-turbo` 100 万 tokens/月），自动抵扣，不可结转 | 在控制台「费用中心 > 免费额度」查看实时余额；额度耗尽前及时采购资源包或开通后付费。 |

## 面向开发者，简洁实用

- ✅ **必做**：所有模型调用后，务必检查响应 `usage` 字段，记录 `total_tokens` 并关联业务请求 ID，用于成本归因与异常排查。  
- ✅ **必控**：在 RAG 和 Agent 中，将 `top_k`、`max_tokens`、`max_length` 等参数设为显式、合理值，禁用无限制生成。  
- ✅ **必查**：通过「模型监控 > 用量统计」页面按天/小时下钻查看 Token 消耗分布，识别高消耗模型或异常请求（如 prompt 过长、循环生成）。  
- ⚠️ **注意**：Token 计量基于模型 tokenizer 实际分词结果，非字符数或字节数；中文、emoji、特殊符号的 Token 占用需以平台实际返回 `usage` 为准。  
- 💡 **优化提示**：压缩 prompt（移除冗余说明、用占位符替代长上下文）、启用流式响应（早发现截断）、复用 ParseX 解析结果（避免重复解析）均可显著降低 Token 消耗。

## 关联主题页

- [agent billing](../guides/agent-billing.md)
- [rag api](../api/rag-api.md)
- [model monitoring](../guides/model-monitoring.md)
- [billing api](../api/billing-api.md)
- [model production](../api/model-production.md)


