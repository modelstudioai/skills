# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）与外部知识源动态结合的技术范式：在生成回答前，先从结构化或非结构化知识库中检索相关片段，并将其作为上下文注入模型提示（Prompt），从而提升回答的准确性、时效性与事实一致性。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台，RAG 不是单一功能，而是贯穿多层级、多形态的**可组合能力链路**，开发者可根据需求选择不同抽象层级的实现方式：

- **零代码应用集成（推荐入门）**：在「应用管理」中创建智能体应用后，直接关联已构建的「知识库」（支持 PDF/DOCX/TXT 等格式），并设置调用策略为「必定调用」。该模式全自动完成文档解析（`DashScopeParse`）、语义切分（`DashScopeJsonNodeParser`）、向量嵌入（`text-embedding-v3`）、混合检索（稠密+重排）与 Prompt 注入，适用于网站、微信公众号、企业微信等渠道的 AI 助手快速上线。

- **代码级 RAG 开发（LlamaIndex 集成）**：通过 `llama-index-indices-managed-dashscope` 构建云端知识库，或使用 `llama-index-readers-dashscope` + `llama-index-node-parser-dashscope` 实现本地可控流程。支持显式指定 Embedding 模型（如 `text-embedding-v3`）、重排模型（`gte-rerank-hybrid`）及召回参数（如 `dense_similarity_top_k=100`, `rerank_top_n=5`），适合需定制切分逻辑、评估指标或混合私有向量库的场景。

- **实时音视频/多模态 RAG（进阶）**：在 AOQ 或 WebRTC 场景中，可将用户语音转文本后的 query 送入 `DashScopeCloudRetriever` 检索知识库，再将结果拼接至 LLM 提示中生成语音回复；万相3.0 视频生成亦支持将检索到的图文参考（如产品手册截图、FAQ 文本）作为 `reference_images` 或 `reference_texts` 输入，实现“基于知识的多模态生成”。

- **第三方模型 RAG（兼容模式）**：调用 DeepSeek、Kimi、MiMo 等三方模型时，仍可通过百炼统一向量引擎完成检索，再将检索结果以 `context` 字段注入 `messages` 中的 system 或 user 角色，无需修改模型原生接口。

## 关键参数和配置

RAG 效果高度依赖以下关键参数，均支持运行时动态控制：

| 组件 | 参数名 | 说明 | 推荐值 | 生效位置 |
|--------|---------|------|----------|-------------|
| **知识库检索** | `dense_similarity_top_k` | 向量召回的原始片段数（未重排） | `50–200`（高召回保覆盖） | `DashScopeCloudRetriever` / AppFlow 知识库配置 |
| | `enable_reranking` | 是否启用语义重排（必开以提升精度） | `True` | 同上 |
| | `rerank_top_n` | 重排后返回给 LLM 的 Top-N 片段数 | `3–5`（平衡信息量与 prompt 长度） | 同上 |
| **重排序模型** | `model` | 重排模型名 | `"gte-rerank-hybrid"`（中文更强） | `DashScopeRerank` |
| | `rerank_min_score` | 过滤低相关性片段的阈值 | `0.3–0.5`（避免噪声注入） | 同上 |
| **Embedding 模型** | `model_name` | 嵌入模型版本 | `"text-embedding-v3"`（CMTEB 73.23 分，当前最优） | `DashScopeEmbedding` / 知识库后台 |
| **生成阶段** | `temperature` | 控制 LLM 输出稳定性 | `0.1–0.3`（客服/问答类场景） | LLM 请求 `extra_body` 或 `messages` 中 system 提示 |
| | `max_tokens` | 限制总输出长度（含检索内容） | 根据渠道约束设（如微信 ≤ 2048） | LLM 请求顶层参数 |

> ⚠️ 注意：所有 RAG 相关参数均**不依赖模型原生支持**——即使调用 [OpenAI 兼容接口](openai-compatibility.md)的三方模型，也可通过百炼侧统一注入检索结果。关键在于将检索得到的 `documents` 正确组织为 ChatML 格式的 `messages`（例如：`{"role": "system", "content": "参考知识：\n" + "\n".join(documents)}`）。

## 面向开发者，简洁实用

- ✅ **首选方案**：用 `DashScopeCloudIndex` + `DashScopeCloudRetriever` 构建云端知识库，免运维、自动更新、开箱即用。
- ✅ **调试技巧**：开启 `return_documents: true`（Rerank）或 `debug: true`（AppFlow 日志），查看实际检索到的片段及其相关性分数。
- ✅ **性能优化**：高频调用时对检索结果启用 `cache_control: {"type": "ephemeral"}`，降低向量计算成本；突发流量叠加 `X-DashScope-Queue-Enable: true` 防雪崩。
- ❌ **避坑提醒**：不要在 Prompt 中硬编码知识片段——应始终通过 `messages` 动态注入；避免 `chunk_size > 1000` 导致语义断裂；`text-embedding-v1/v2` 已下线，请立即升级至 `v3`。

## 关联主题页

- [use cases](../guides/use-cases.md)
- [frameworks](../api/frameworks.md)
- [application use cases](../guides/application-use-cases.md)
- [vector and sort](../api/vector-and-sort.md)


