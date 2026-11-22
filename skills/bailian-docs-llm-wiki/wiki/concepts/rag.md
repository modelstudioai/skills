# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，简称 RAG）是一种将外部知识检索与大语言模型生成能力深度融合的技术范式。它通过在模型推理前动态检索相关知识片段，并将其作为上下文注入提示（Prompt），显著提升回答的准确性、时效性与领域专业性，同时降低幻觉风险。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台中，RAG 不是单一功能，而是贯穿多个服务层级的**核心增强机制**，支持以下典型落地方式：

- **RAG API 服务**：面向开发者提供端到端私有知识问答能力。您可上传文档（PDF/DOCX/TXT 等）→ 自动解析切片 → 向量化索引 → 语义检索 → 注入 LLM 生成。适用于客服问答、技术文档助手、内部知识中枢等场景，所有环节均可通过 `/v1/knowledge/query` 等标准接口编排调用。

- **智能体（Agent）应用**：在 Agent 编排中，RAG 作为 `context.rag` 模块被声明式启用。当用户提问时，平台自动触发知识库检索，将 top_k 个高相关片段注入模型上下文。支持“必定调用”或“按需调用”两种策略，适配强约束（如制度问答）与轻量交互（如闲聊辅助）不同需求。

- **本地化 RAG 部署**：满足数据不出域要求。您可在本地运行 ParseX 解析 + 向量检索模块（如基于 Chroma 或 Milvus），仅将检索结果和 query 发送至百炼 API 进行生成。全程无需上传原始文档，敏感数据完全保留在本地环境。

- **[多模态](multi-modal.md)与结构化增强**：结合 `vector and sort` 能力，RAG 可扩展至图像、视频等[多模态](multi-modal.md)内容检索；借助 `more` 提供的 `searchFilters`，还能在语义召回后叠加字段级过滤（如 `{"department": "HR", "effective_date": {"gte": "2024-01-01"}}`），实现“语义+结构”双重精准匹配。

## 关键参数和配置

RAG 行为由以下关键参数控制，均支持运行时动态指定（API）或控制台可视化配置（Agent）：

| 参数 | 所属模块 | 类型 | 默认值 | 说明 |
|------|----------|------|--------|------|
| `knowledge_id` / `knowledge_base_id` | RAG API / Agent Context | string | — | 知识库唯一标识，需提前创建并处于 `active` 状态 |
| `top_k` | RAG API (`top_k`) / Agent (`rag.top_k`) | integer | `3` | 检索返回的最相关文本切片数量，范围 1–10；值过大会增加 token 开销，过小可能遗漏关键信息 |
| `retrieval_strategy` | RAG API | string | `"hybrid"` | 检索模式：`"hybrid"`（关键词+向量融合召回，推荐）、`"vector_only"`（纯语义） |
| `score_threshold` | Agent Context (`rag.score_threshold`) | float | `0.3` | 相似度阈值，低于此值的片段将被丢弃；建议设为 `0.2–0.5`，避免噪声注入 |
| `searchFilters` | RAG API / [more](../api/more.md) 扩展 | object array | — | 结构化过滤条件，支持字段等值、范围、模糊、标签等，用于精准限定检索范围（如 `[{ "doc_type": "policy" }]`） |

> ⚠️ 注意：  
> - 切片长度（chunk size）由平台固定为 **512 token**，不可配置；  
> - 嵌入模型固定为 `text-embedding-v3`（RAG API）或可选 `qwen3.7-text-embedding`（自定义向量场景），不支持用户替换；  
> - 所有检索结果默认按相关性降序排列，无需额外排序参数。

## 面向开发者，简洁实用

- ✅ **快速起步**：用 RAG API 三步完成集成：① 创建知识库 → ② 上传文档并触发同步 → ③ 调用 `/v1/knowledge/query` 发起问答。cURL 示例见 [RAG API 概览](raw/application-api-reference/rag-api/rag-api-overview.md)。  
- ✅ **调试技巧**：首次调用时，设置 `top_k=5` 并打印 `retrieved_chunks` 字段（响应中 `debug_info.retrieved_chunks`），直观验证检索质量；若结果不相关，优先检查文档格式、`score_threshold` 是否过低或 `searchFilters` 是否误排除。  
- ✅ **性能优化**：对高并发场景，启用流式响应（`stream=true`）降低首字延迟；对长文档问答，确保 `query` ≤ 2048 字符，避免截断——必要时前端做预处理摘要。  
- ✅ **安全合规**：使用 `more` 提供的临时 [Token](token.md)（`/api/v1/tokens`）替代永久 API Key 供前端调用；结构化过滤（`searchFilters`）可天然实现权限隔离（如按 `tenant_id` 过滤）。  
- ❌ **避坑提醒**：知识库状态非 `active` 时请求必失败；`query` 含 `\x00` 等控制字符将静默失败；`gte`/`lte` 等操作符仅对 Schema 中明确定义为 `double` 或 `date` 类型的字段生效。

## 关联主题页

- [rag api](../api/rag-api.md)
- [vector and sort](../api/vector-and-sort.md)
- [application use cases](../guides/application-use-cases.md)
- [agent context](../guides/agent-context.md)
- [more](../api/more.md)


