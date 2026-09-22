# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）与外部知识源动态结合的技术范式：在生成回答前，先从结构化或非结构化知识库中检索相关片段，再将检索结果与用户问题一并输入 LLM 进行上下文感知的推理与生成。该方法显著提升模型在私域、专业、时效性场景下的事实准确性、可解释性与可控性，是百炼平台支撑企业级 AI 应用的核心能力底座。

## 在百炼平台的不同场景中，这个概念如何使用

RAG 在百炼中不是单一功能，而是贯穿数据接入、服务编排与应用交付的横切能力，按使用深度分为三层：

- **API 直接调用层**：通过 `RAG API`（`/v1/knowledge_bases/{kb_id}/retrieve_and_answer`）实现端到端“检索+生成”一体化调用。适用于需完全自主控制请求链路的开发者，如构建定制客服后端、嵌入现有系统工作流。
  
- **知识库服务层**：以 `Knowledge Base` 为统一载体，支持文档（PDF/DOCX/TXT）、表格（CSV/JSONL）、多模态（图片/音视频元数据）等多源数据接入，并自动完成智能切片、向量化（默认 `text-embedding-v4`）、混合检索（稠密+关键词）、重排序（`qwen3-rerank`）及问答生成（可选 `qwen3.6-plus` 等模型）。所有操作可通过控制台 Playground 快速验证，或通过 `/api/v1/indices/knowledge/search` 等标准化接口集成。

- **低代码应用层**：在 `Application Use Cases` 中，RAG 作为可配置模块嵌入百炼智能体（Agent）——开发者在应用配置页启用知识库，设置“必定调用”或“按需调用”，即可让网站悬浮窗、企业微信机器人、钉钉机器人等渠道自动获得私域知识增强能力，无需编写检索逻辑。

此外，`Frameworks` 层提供对 LlamaIndex 和 Spring AI Alibaba 的原生集成，支持混合部署模式：既可直接复用百炼云端知识库（`DashScopeCloudIndex`），也可在本地构建向量索引（`VectorStoreIndex`）并调用百炼 Embedding/LLM/Rerank 模型，满足合规、延迟或定制化切分等特殊需求。

## 关键参数和配置

以下参数直接影响 RAG 效果与性能，开发者应根据场景权衡调整：

| 参数名 | 作用域 | 默认值 | 取值范围 | 说明 |
|--------|--------|--------|----------|------|
| `top_k` | 检索召回数 | `3`（RAG API）<br>`100`（Framework） | `1–100` | 控制初步检索返回的切片数量；值过小易漏召，过大增加 LLM 上下文负担。建议从 `5–10` 起调优。 |
| `enable_rerank` / `enable_reranking` | 检索精排 | `false`（RAG API）<br>`True`（Framework） | `true` / `false` | 启用 cross-encoder 重排序，显著提升相关性但增加约 200–500ms 延迟；高精度场景（如合同审查）建议开启。 |
| `rerank_top_n` / `max_retrieved_count` | 最终返回数 | `5`（Framework）<br>`1–20`（知识库问答） | `1–20` | 重排后实际送入 LLM 的切片数，也是最终响应中 `retrieved_chunks` 的最大长度。 |
| `similarity_threshold` | 相似度过滤 | 无默认（需显式设） | `0.01–1.0` | 过滤低分切片，避免噪声干扰生成；建议初值设 `0.3–0.5`，结合业务效果微调。 |
| `chunk_size` | 切片粒度 | `500`（Framework）<br>控制台默认 `512` token | `10–6000` token | 影响检索单元语义完整性：过短丢失上下文（如拆断表格），过长混杂无关主题；技术文档推荐 `256–512`，法律文本可设 `1024+`。 |
| `knowledge_base_id` | 知识源绑定 | — | 必填字符串 | 所有 RAG 调用必须指定，需提前通过 `/v1/knowledge_bases` 创建获取；Agent 场景中通过 `agent_id` 间接关联。 |

> ⚠️ 注意：`chunk_size`、嵌入模型（`text-embedding-v4`）、重排模型（`qwen3-rerank`）等关键配置在知识库创建时即固化，不可修改；如需变更，需重建知识库。

## 面向开发者，简洁实用

- **快速验证**：用控制台 Playground 输入问题，实时查看 `retrieved_chunks` 原始内容与 `answer` 生成结果，5 分钟内确认知识覆盖效果。
- **生产集成**：
  - 优先使用 `POST /v1/knowledge_bases/{kb_id}/retrieve_and_answer`（一体式）而非分步调用，减少网络往返；
  - 对延迟敏感场景（如实时客服），关闭 `enable_rerank` 并将 `top_k` 设为 `3–5`；
  - 对准确性要求高场景（如内部知识助手），开启重排 + `rerank_top_n=5` + `similarity_threshold=0.4` 组合；
  - 使用 `bailian-cli` 命令行工具（`bl knowledge search --agent-id <id> --query "xxx"`）进行自动化测试与 CI 集成。
- **避坑提示**：
  - 知识库仅支持华北2（北京）和新加坡地域，跨地域调用必失败；
  - 单次请求超时为 60 秒，若知识库规模大或启用重排，请预留足够缓冲；
  - 免费额度仅抵扣知识库规格费用，**不包含模型调用 token 成本**，需单独预算；
  - 文档上传单文件 ≤100 MB，切片总数建议 ≤100 万，超限将触发限流或失败。

## 关联主题页

- [rag api](../api/rag-api.md)
- [knowledge base](../guides/knowledge-base.md)
- [application use cases](../guides/application-use-cases.md)
- [frameworks](../api/frameworks.md)
- [more about models](../api/more-about-models.md)


