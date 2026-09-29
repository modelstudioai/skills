# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）与外部知识源动态结合的技术范式：在生成回答前，先从结构化或非结构化知识库中检索相关片段，再将检索结果与用户查询一并输入模型，从而提升回答的准确性、时效性与可溯源性。它有效缓解了大模型幻觉、知识陈旧和领域适配难等问题，是百炼平台构建可信企业级 AI 应用的核心技术底座。

## 在百炼平台的不同场景中，这个概念如何使用

RAG 在百炼中不是单一功能，而是贯穿多个层级的**可组合能力体系**，开发者可根据需求选择不同抽象粒度：

- **开箱即用的知识库服务（推荐新手/业务快速上线）**  
  通过控制台或 RAG API 创建 `knowledge_base`，上传 PDF/Word/Excel/Markdown 等文档，平台自动完成解析、语义切片、向量化与索引构建。调用 `/v1/knowledge_bases/{kb_id}/qa` 即可获得流式、带引用的问答结果。适用于智能客服、内部知识助手等场景。

- **应用层 RAG 增强（低代码集成）**  
  在百炼「智能体应用」中绑定已创建的知识库，并配置调用策略（`必定调用` 或 `按需调用`）。无需修改代码，即可为网站悬浮窗、微信公众号、企业微信机器人等渠道的对话自动注入私域知识，实现“模型能力 + 业务知识”的无缝融合。

- **框架级自定义 RAG（面向开发者深度控制）**  
  通过 LlamaIndex 或 Spring AI Alibaba 集成 `DashScopeCloudIndex` / `DashScopeCloudRetriever`，灵活组合：  
  - 文档解析（`DashScopeParse` 支持版面分析与表格识别）  
  - 切分策略（`DashScopeJsonNodeParser` 按中文标点/换行智能分段）  
  - 混合召回（向量 + 关键词双通道，`dense_similarity_top_k` + `sparse_similarity_top_k`）  
  - 重排序（`DashScopeRerank` 使用 `gte-rerank-hybrid` 提升 Top-K 相关性）  
  适合需要定制切分逻辑、多源异构数据融合或本地索引管理的高级场景。

- **跨模态 RAG 扩展（前沿探索）**  
  百炼支持 `image`、`multimedia` 类型知识库，配合 `qwen3-vl-embedding` 等多模态嵌入模型，可实现图文混合检索、音视频内容问答等创新用例，已在文档转视频、视觉问答等场景落地验证。

## 关键参数和配置

| 参数名 | 所属模块 | 说明 | 典型值 | 注意事项 |
|--------|----------|------|--------|----------|
| `knowledge_base_id` | 知识库 API / 应用配置 | 知识库唯一标识 | `"kb-xxx"` | 必填；需确保与 API Key 同属一个 `workspace_id` |
| `retrieval_strategy` | 知识库 API | 检索模式 | `"hybrid"`（默认）、`"vector_only"`、`"keyword_only"` | `hybrid` 同时触发向量与关键词召回，精度更高但延迟略增 |
| `top_k` / `dense_similarity_top_k` / `sparse_similarity_top_k` | 知识库 API / LlamaIndex | 返回最相关片段数 | `3`（API 默认）、`100`（LlamaIndex 默认） | 过高易引入噪声，建议 `3–10` 用于问答，`50–100` 用于重排序前召回 |
| `enable_rerank` / `enable_reranking` | 知识库 API / LlamaIndex | 是否启用语义重排序 | `true`（默认） | 强烈建议开启，`gte-rerank-hybrid` 在中文检索任务上效果最优 |
| `stream` | 知识库问答 API | 是否流式返回响应 | `true`（推荐） | 仅 `/v1/knowledge_bases/{kb_id}/qa` 支持；流式可降低首字延迟，便于前端渲染 |
| `model_id` / `model_name` | 全局 | 生成模型与嵌入模型选择 | `"qwen-plus"`、`"text-embedding-v3"` | 生成模型影响回答质量，嵌入模型直接影响检索召回率；`text-embedding-v3` 在 CMTEB 检索基准上达 73.23 分 |

> ⚠️ 注意：所有 RAG 调用均依赖 `workspace_id` 隔离，务必确保 API Key、知识库、Agent、应用均在同一业务空间下；跨区域调用需匹配 Endpoint 地域（如 `cn-beijing.maas.aliyuncs.com`）。

## 面向开发者，简洁实用

- **起步最快**：控制台新建知识库 → 上传文件 → 等待状态变 `active` → 调用 `/qa` 接口，5 分钟验证效果。  
- **调试必做**：用控制台 [Playground](../../raw/application-user-guide/knowledge-base/playground.md) 实时测试检索质量，观察 `retrieved_chunks` 内容是否相关、是否覆盖关键信息。  
- **性能优化**：若延迟敏感，可设 `retrieval_strategy=vector_only` + `enable_rerank=false`，牺牲少量精度换取更快响应；生产环境建议保留 `hybrid` + `rerank` 组合。  
- **避坑提示**：  
  - PDF 必须是文本型（非扫描图），否则需 OCR 预处理；  
  - 单文档切片超 10,000 片会被截断，大文档请提前分卷；  
  - 知识库更新后索引约 1–2 分钟生效，勿立即重试；  
  - Agent 必须「发布」后才能调用 `/knowledge/search` 或 `/chat`，未发布返回 `Agent 未发布` 错误。  

RAG 的本质是让大模型“有据可依”。在百炼，你只需聚焦业务知识本身——解析、索引、检索、生成，全部交由平台可靠执行。

## 关联主题页

- [knowledge base](../guides/knowledge-base.md)
- [rag api](../api/rag-api.md)
- [frameworks](../api/frameworks.md)
- [application use cases](../guides/application-use-cases.md)
- [use cases](../guides/use-cases.md)


