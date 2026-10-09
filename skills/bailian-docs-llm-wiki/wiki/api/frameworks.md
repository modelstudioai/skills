# frameworks

百炼平台提供对主流 AI 开发框架的深度集成支持，重点覆盖 LlamaIndex 和 Spring AI Alibaba 两大生态，帮助开发者快速构建 RAG、智能体、工作流等生产级应用。所有集成均通过官方 SDK 封装，统一使用 `DASHSCOPE_API_KEY` 认证，并与百炼云端知识库、大模型服务及文档智能能力无缝协同。

## 支持的模型/功能

- **大模型调用**：支持全部百炼文本生成模型（如 `qwen-max`、`qwen-plus`），可通过 `DashScope` 或 OpenAI-like 封装两种方式接入 LlamaIndex；Spring AI Alibaba 则通过 `DashScopeAgent` 调用已部署的[智能体应用](raw/application-user-guide/llm-application/single-agent-application.md)和[工作流应用](raw/application-user-guide/llm-application/workflow-application.md)。
- **Embedding 模型**：支持 `text-embedding-v1`/`v2`/`v3`，其中 `v3` 在 CMTEB Retrieval 任务上达 73.23 分，为当前最优 [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)。
- **重排序模型**：提供 `gte-rerank` 和 `gte-rerank-hybrid`，用于检索后结果精排，`gte-rerank-hybrid` 为 `DashScopeCloudRetriever` 默认启用模型 [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)。
- **文档解析与切分**：`DashScopeParse` 支持 PDF/DOCX/DOC 智能解析（基于文档智能 DocMind），`DashScopeJsonNodeParser` 基于通义文本切分模型实现语义分块，二者需配合使用 [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)。
- **云端知识库管理**：`DashScopeCloudIndex` 封装知识库创建、文档上传、索引构建全流程；`DashScopeCloudRetriever` 提供稠密/稀疏混合检索、自动重排、分数阈值过滤等能力 [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)。

> **注意**：文档 1 明确指出“本方案将知识库部署在云端，使用默认的智能文档切分与官方向量模型，**不支持自定义文档切分方式或自定义嵌入模型**”，而文档 11 和文档 3 中的 `DashScopeJsonNodeParser` 与 `DashScopeEmbedding` 均允许用户显式指定切分策略和 embedding 模型。该矛盾表明：**云端知识库（`DashScopeCloudIndex`）强制使用平台预设能力，而本地向量索引（`VectorStoreIndex`）才支持完全自定义**。开发者应根据部署模式区分能力边界。

## 关键参数

| 组件 | 关键参数 | 说明 | 默认值 |
|--------|-----------|------|---------|
| `DashScopeLLM` | `model_name` | 指定调用的大模型，如 `"qwen-max"` | — |
| `DashScopeEmbedding` | `model_name` | 指定 embedding 模型，如 `"text-embedding-v3"` | `"text-embedding-v2"` |
| `DashScopeRerank` | `model`, `top_n`, `rerank_min_score` | 排序模型名、返回 top 数量、重排后最低分数阈值 | `"gte-rerank"`, `5`, `0.0` |
| `DashScopeCloudRetriever` | `dense_similarity_top_k`, `sparse_similarity_top_k`, `enable_reranking`, `rerank_model_name` | 向量/文本召回数、是否启用重排、重排模型名 | `100`, `100`, `True`, `"gte-rerank-hybrid"` |
| `DashScopeJsonNodeParser` | `chunk_size`, `overlap_size`, `separator`, `language` | 分块大小、重叠大小、分隔符正则、语言（`"cn"`/`"en"`） | `500`, `100`, `" \|,\|，\|。\|？\|！\|\n\|\?\|\!"`, `"cn"` |

## 使用方式

1. **环境准备**  
   - 获取 API Key 并配置为环境变量 `DASHSCOPE_API_KEY`（文档 2、3、4、5、7、11 均要求）；  
   - 若使用子业务空间，必须配置 `DASHSCOPE_WORKSPACE_ID`（文档 5、7、11 明确强调）；  
   - 安装对应 SDK：LlamaIndex 生态需 `pip install llama-index-llms-dashscope` 等，Spring AI Alibaba 需添加 `spring-ai-alibaba-starter-dashscope` 依赖（文档 8、9、10）。

2. **LlamaIndex 集成示例**  
   ```python
   # 全局设置（可选）
   from llama_index.core import Settings
   from llama_index.llms.dashscope import DashScope
   from llama_index.embeddings.dashscope import DashScopeEmbedding
   
   Settings.llm = DashScope(model_name="qwen-plus")
   Settings.embed_model = DashScopeEmbedding(model_name="text-embedding-v3")
   
   # 构建云端知识库（自动解析+索引）
   from llama_index.indices.managed.dashscope import DashScopeCloudIndex
   index = DashScopeCloudIndex.from_documents(documents, name="my_index")
   
   # 构建检索器（混合检索+重排）
   retriever = index.as_retriever(
       dense_similarity_top_k=50,
       enable_reranking=True,
       rerank_model_name="gte-rerank"
   )
   ```

3. **Spring AI Alibaba 集成示例**  
   - 应用调用：配置 `application.yml` 中 `spring.ai.dashscope.agent.app-id`，注入 `DashScopeAgent` 实例调用；  
   - 知识库检索：使用 `DashScopeDocumentRetriever` 指定 `INDEX_NAME`，结合 `DocumentRetrievalAdvisor` 注入 ChatClient（文档 10）。

## 限制和注意事项

- **文件解析限制**：`DashScopeParse` 仅对 `.pdf`、`.docx`、`.doc` 进行智能解析；其他格式（如 `.txt`、`.md`）仅原样上传，不触发文档结构识别 [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)。
- **云端知识库不可定制**：如文档 1 所述，云端知识库强制使用平台默认切分与 embedding 模型，无法替换；若需自定义，必须采用本地 `VectorStoreIndex` + `DashScopeEmbedding` 方案 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。
- **业务空间强依赖**：所有 `DashScopeCloud*` 组件（`DashScopeCloudIndex`、`DashScopeCloudRetriever`）均要求 `DASHSCOPE_WORKSPACE_ID` 环境变量，缺失将直接报错（文档 5、7、11 均明确校验）。
- **Spring AI Alibaba 环境变量差异**：Spring 生态使用 `AI_DASHSCOPE_API_KEY`（文档 10）而非通用的 `DASHSCOPE_API_KEY`（文档 2、3、4、5、7、11），需按框架分别配置。
- **模型兼容性**：OpenAI-like 封装仅支持百炼的[文本生成类模型](raw/model-api-reference/qwen-api-reference.md)，不支持 embedding 或 rerank 模型（文档 2）。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)
- [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)
- [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)
- [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)
- [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)
- [DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)
- [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)
- [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)


