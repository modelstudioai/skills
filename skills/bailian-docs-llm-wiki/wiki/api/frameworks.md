# frameworks

百炼平台提供对主流 AI 开发框架的原生集成支持，重点覆盖 LlamaIndex 和 Spring AI Alibaba 两大生态，帮助开发者快速构建 RAG、智能体、工作流等生产级应用。所有集成均通过官方 SDK 封装，统一使用 DashScope API Key 认证，并与百炼云端知识库、大模型服务及文档智能能力深度协同。

## 支持的模型/功能

- **LlamaIndex 集成**：完整支持 `DashScopeLLM`（大模型）、`DashScopeEmbedding`（向量模型）、`DashScopeParse`（文档解析）、`DashScopeJsonNodeParser`（智能切分）、`DashScopeRerank`（重排序）及 `DashScopeCloudIndex`/`DashScopeCloudRetriever`（云端知识库管理）等组件。  
- **Spring AI Alibaba 集成**：支持调用百炼[智能体应用](raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)和[工作流应用](raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)，以及检索[云端知识库](raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。  
- **Embedding 模型**：明确支持 `text-embedding-v1`、`v2`、`v3` 三款模型，其中 `v3` 在 MTEB（Retrieval task）和 CMTEB（Retrieval task）两项关键指标上分别达 55.41 和 73.23，为当前最优 [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)。  
- **重排序模型**：默认使用 `gte-rerank`，亦支持 `gte-rerank-hybrid`（仅限 `DashScopeCloudRetriever`）[DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)。

> **注意**：文档 1 明确指出“本方案将知识库部署在云端，使用默认的智能文档切分与官方向量模型，**不支持自定义文档切分方式或自定义嵌入模型**”，而文档 6 的 `DashScopeJsonNodeParser` 和文档 2 的 `DashScopeEmbedding` 均提供了对应能力。该矛盾表明：**云端知识库（`DashScopeCloudIndex`）强制使用百炼托管的切分与嵌入流程；若需完全自定义，必须采用本地索引（如 `VectorStoreIndex` + `DashScopeEmbedding`）**。详见 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。

## 关键参数

| 组件 | 关键参数 | 说明 |
|--------|-----------|------|
| `DashScopeLLM` | `model_name`（如 `"qwen-max"`） | 必填，指定调用的大模型；完整列表见 [选择模型](raw/model-user-guide/get-started-with-models/models.md) |
| `DashScopeEmbedding` | `model_name`（如 `"text-embedding-v3"`） | 必填，影响向量质量与检索效果 |
| `DashScopeRerank` | `top_n`, `model`（`"gte-rerank"` 或 `"gte-rerank-hybrid"`） | 控制返回结果数量与重排策略 |
| `DashScopeCloudRetriever` | `dense_similarity_top_k`, `sparse_similarity_top_k`, `enable_reranking`, `rerank_top_n`, `rerank_min_score` | 全面控制混合检索（向量+文本）与重排后过滤逻辑 |
| `DashScopeParse` | `category_id`, `workspace`, `result_type` | 决定文档解析类目、业务空间及输出格式（如 `DASHSCOPE_DOCMIND`） |
| `DashScopeJsonNodeParser` | `chunk_size`, `overlap_size`, `separator`, `language` | 定义文本切分粒度与规则，**仅适用于 `DashScopeParse` 输出的 JSON 结构化文本** |

## 使用方式

1. **环境准备**：  
   - 获取并配置 `DASHSCOPE_API_KEY`（必需），部分场景还需 `DASHSCOPE_WORKSPACE_ID`（子业务空间）或 `AI_DASHSCOPE_API_KEY`（Spring AI Alibaba）。  
   - 安装对应 SDK（如 `pip install llama-index-llms-dashscope llama-index-embeddings-dashscope` 或 Maven 引入 `spring-ai-alibaba-starter-dashscope`）。

2. **LlamaIndex 典型流程**：  
   - 解析：`DashScopeParse` 处理 PDF/DOCX/TXT → 生成结构化 `Document`；  
   - 切分：`DashScopeJsonNodeParser` 对解析结果按语义切片；  
   - 向量化：`DashScopeEmbedding` 生成向量 → 构建 `VectorStoreIndex`（本地）或 `DashScopeCloudIndex`（云端）；  
   - 检索：`DashScopeCloudRetriever` 或 `index.as_retriever()` 执行混合检索 + `DashScopeRerank` 重排；  
   - 生成：`DashScopeLLM` 调用大模型合成答案。

3. **Spring AI Alibaba 典型流程**：  
   - 应用集成：配置 `app-id` + `DASHSCOPE_API_KEY` → 使用 `DashScopeAgent` 调用智能体/工作流；  
   - 知识库检索：配置 `INDEX_NAME` + `AI_DASHSCOPE_API_KEY` → 使用 `DashScopeDocumentRetriever` 实现 RAG，自动注入上下文至 `ChatClient`。

## 限制和注意事项

- **文件限制**：`DashScopeParse` 仅支持 `.doc`/`.docx`/`.pdf`/`.txt`/`.md`/`.ppt`/`.pptx`/`.xls`/`.xlsx`，单文件 ≤100MB 且 ≤1000 页；**仅 PDF/DOC/DOCX 进行智能解析，其余格式仅原样上传** [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)。  
- **云端知识库约束**：`DashScopeCloudIndex` 强制使用百炼托管的文档切分与向量模型，**不开放自定义切分逻辑或嵌入模型选择**，与本地 `VectorStoreIndex` 方案存在根本性差异。  
- **API Key 配置**：Spring AI Alibaba 文档（文档 11）要求环境变量名为 `AI_DASHSCOPE_API_KEY`，而 LlamaIndex 文档（文档 2/3/4/5/7/8）统一使用 `DASHSCOPE_API_KEY`；两者不可混用，需按框架严格区分。  
- **业务空间依赖**：所有云端操作（`DashScopeCloudIndex`, `DashScopeCloudRetriever`, `Spring AI Alibaba` 知识库检索）均需显式配置 `DASHSCOPE_WORKSPACE_ID` 或 `AI_DASHSCOPE_WORKSPACE_ID`，否则默认指向主账号空间。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)
- [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)
- [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)
- [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)
- [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)
- [DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)
- [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)
- [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)


