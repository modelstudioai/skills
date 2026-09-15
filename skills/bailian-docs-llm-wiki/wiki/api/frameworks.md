# frameworks

阿里云百炼平台提供对主流 AI 开发框架的深度集成支持，重点覆盖 LlamaIndex 和 Spring AI Alibaba 两大生态，帮助开发者快速构建 RAG 应用、知识库检索服务及大模型智能体。所有集成均基于百炼统一的 API 认证体系（`DASHSCOPE_API_KEY`）和可选的业务空间隔离能力，支持云端托管与本地开发协同。

## 支持的模型/功能

- **LlamaIndex 集成**：完整支持 `DashScopeLLM`（文本生成）、`DashScopeEmbedding`（[向量嵌入](../concepts/embedding.md)）、`DashScopeParse`（智能文档解析）、`DashScopeRerank`（语义重排）、`DashScopeCloudIndex`/`DashScopeCloudRetriever`（云端知识库索引与检索）等组件。  
  - Embedding 模型支持 `text-embedding-v1`/`v2`/`v3`，其中 `v3` 在 CMTEB Retrieval 任务上达 73.23 分 [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)；  
  - Rerank 模型默认为 `gte-rerank`，也支持 `gte-rerank-hybrid` [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)；  
  - 文档解析支持 PDF/DOCX/TXT 等 9 种格式，但仅 PDF/DOC/DOCX 启用智能解析（如版式还原、表格识别），其余格式仅原样上传 [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)。  

- **Spring AI Alibaba 集成**：支持两类核心场景：  
  - 调用已部署的百炼大模型应用（仅限智能体应用 Agent 1.0 和工作流应用）；  
  - 检索百炼云端知识库（需提前创建知识库，支持自动上下文注入与 `qwen-max` 默认模型生成）[通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。

> **注意**：文档 1 明确指出“本方案将知识库部署在云端，使用默认的智能文档切分与官方向量模型，**不支持自定义文档切分方式或自定义嵌入模型**”，而文档 5 和文档 7 中 `DashScopeJsonNodeParser` 和 `DashScopeEmbedding` 均允许自定义切分逻辑与 embedding 模型。该矛盾表明：**云端知识库（`DashScopeCloudIndex`）强制使用百炼托管的切分与向量化流程，而本地 LlamaIndex 流程（`VectorStoreIndex` + `DashScopeEmbedding`）才支持完全自定义**。

## 关键参数

| 组件 | 关键参数 | 说明 |
|--------|-----------|------|
| `DashScopeLLM` | `model_name` | 必填，如 `"qwen-max"`、`"qwen-plus"`；完整列表见 [选择模型](raw/model-user-guide/get-started-with-models/models.md) |
| `DashScopeEmbedding` | `model_name` | 必填，如 `"text-embedding-v3"`；影响向量质量与检索效果 |
| `DashScopeRerank` | `top_n`, `model` | `top_n` 控制返回结果数；`model` 可选 `"gte-rerank"` 或 `"gte-rerank-hybrid"` |
| `DashScopeCloudRetriever` | `dense_similarity_top_k`, `enable_reranking`, `rerank_top_n` | 分别控制向量召回数量、是否启用重排、重排后返回节点数；默认 `dense_similarity_top_k=100`, `rerank_top_n=5` |
| `DashScopeParse` | `category_id`, `workspace` | `category_id` 影响文档归类与后续检索范围；`workspace` 用于多业务空间隔离 |

## 使用方式

1. **环境准备**：  
   - 获取 `DASHSCOPE_API_KEY` 并配置为环境变量（文档 2、4、6、8、10、11 均要求）；  
   - 若使用子业务空间，必须配置 `DASHSCOPE_WORKSPACE_ID`（文档 4、6、8、10、11 明确强调）；  
   - 安装对应依赖包，例如 `llama-index-llms-dashscope`、`llama-index-embeddings-dashscope`、`spring-ai-alibaba-starter-dashscope` 等。

2. **典型流程（LlamaIndex）**：  
   - 解析本地文件 → `DashScopeParse`；  
   - 构建云端知识库 → `DashScopeCloudIndex.from_documents()`；  
   - 初始化检索器 → `index.as_retriever()`；  
   - 查询并后处理 → `retriever.retrieve()` + `DashScopeRerank` 等 node postprocessor。

3. **典型流程（Spring AI Alibaba）**：  
   - 配置 `application.yml` 中 `spring.ai.dashscope.agent.app-id` 和 `api-key`；  
   - 使用 `DashScopeAgent` 调用智能体应用；  
   - 或配置 `DashScopeDocumentRetriever` + `DocumentRetrievalAdvisor` 实现 RAG 检索 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。

## 限制和注意事项

- **文件解析限制**：`DashScopeParse` 单文件上限为 100MB 或 1000 页，一次上传最多 200 个文件；仅 PDF/DOC/DOCX 触发智能解析，其余格式仅存储不解析 [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)。  
- **模型调用兼容性**：`OpenAILike` 封装仅支持百炼的文本生成模型（如 `qwen-plus`），**不支持 embedding 或 rerank 模型**；需调用后者必须使用原生 `DashScopeEmbedding` 或 `DashScopeRerank` [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)。  
- **业务空间强依赖**：所有云端操作（`DashScopeCloudIndex`、`DashScopeCloudRetriever`、Spring AI Alibaba 的知识库检索）均**必须配置 `DASHSCOPE_WORKSPACE_ID`**，否则初始化失败（文档 4、6、11 明确报错提示）。  
- **知识库更新机制**：`DashScopeCloudIndex` 支持 `index._insert()` 增量插入和 `index.delete_ref_doc()` 删除，但**不支持直接修改已有文档内容**，需删除后重传。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)
- [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)
- [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)
- [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)
- [DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)
- [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)
- [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)


