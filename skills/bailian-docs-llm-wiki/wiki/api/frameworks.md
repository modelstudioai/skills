# frameworks

百炼平台提供对主流 AI 开发框架的深度集成支持，当前重点覆盖 LlamaIndex 和 Spring AI Alibaba 两大生态。开发者可基于这些框架快速构建 RAG 应用、调用大模型服务、管理云端知识库或集成智能体/工作流应用，无需从零实现底层能力。所有集成均通过官方 SDK 封装，统一使用 DashScope API Key 认证，并与百炼控制台的业务空间、知识库、应用等资源模型对齐。

## 支持的模型/功能

- **大模型调用**：支持全部百炼文本生成模型（如 `qwen-max`、`qwen-plus`），可通过 LlamaIndex 的 `DashScope` 或 `OpenAILike` LLM 封装调用；Spring AI Alibaba 则通过 `DashScopeAgent` 调用已部署的[智能体应用](raw/application-user-guide/llm-application/single-agent-application.md)或[工作流应用](raw/application-user-guide/llm-application/workflow-application.md)。
- **Embedding 模型**：支持 `text-embedding-v1`/`v2`/`v3`，其中 `v3` 在 CMTEB Retrieval 任务上达 73.23 分，推荐用于高精度语义检索 [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)。
- **文档解析与切分**：`DashScopeParse` 提供 PDF/DOCX/DOC 智能解析（基于文档智能 DocMind），`DashScopeJsonNodeParser` 提供基于通义文本切分模型的细粒度分块能力，二者需配合使用。
- **云端知识库服务**：`DashScopeCloudIndex` 支持一键上传本地文件、云端智能切分与向量索引构建；`DashScopeCloudRetriever` 提供稠密/稀疏混合检索与重排能力。
- **重排（Rerank）**：`DashScopeRerank` 集成 `gte-rerank` 系列模型，用于对初检结果进行语义相关性精排 [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)。

> **注意**：文档 1 明确指出“本方案将知识库部署在云端，使用默认的智能文档切分与官方向量模型，**不支持自定义文档切分方式或自定义嵌入模型**”，而文档 5 和文档 3 分别提供了 `DashScopeJsonNodeParser` 和 `DashScopeEmbedding` 的自定义能力。这表明：**云端知识库（DashScopeCloudIndex）本身不开放自定义切分/Embedding，但开发者可完全绕过该服务，使用 DashScopeParse + DashScopeJsonNodeParser + DashScopeEmbedding 在本地构建全自定义 RAG 流程**。

## 关键参数

| 组件 | 关键参数 | 说明 | 默认值 |
|--------|-----------|------|---------|
| `DashScope` (LLM) | `model_name` | 指定调用的大模型，如 `"qwen-max"` | — |
| `DashScopeEmbedding` | `model_name` | 指定 Embedding 模型，如 `"text-embedding-v3"` | `"text-embedding-v2"` |
| `DashScopeCloudIndex.from_documents()` | `name` | 云端知识库名称，需全局唯一 | — |
| `DashScopeCloudRetriever` | `dense_similarity_top_k`, `sparse_similarity_top_k` | 向量/文本检索召回数量 | `100` |
| | `enable_reranking`, `rerank_model_name`, `rerank_top_n` | 是否启用重排、重排模型及返回数量 | `True`, `"gte-rerank-hybrid"`, `5` |
| `DashScopeRerank` | `model`, `top_n` | 重排模型名与返回 Top-N 数量 | `"gte-rerank"`, `3` |
| `DashScopeJsonNodeParser` | `chunk_size`, `overlap_size`, `separator` | 分块大小、重叠长度、切分符正则表达式 | `500`, `100`, `" \|,\|，\|。\|？\|！|\n|\?|\!"` |

## 使用方式

1. **环境准备**：  
   - 获取并配置 `DASHSCOPE_API_KEY`（必需），部分场景还需 `DASHSCOPE_WORKSPACE_ID`（子业务空间时必需）[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。  
   - 安装对应框架 SDK（如 `pip install llama-index-llms-dashscope llama-index-embeddings-dashscope`）。

2. **LlamaIndex 典型流程**：  
   - 解析：`DashScopeParse` 读取 PDF/DOCX 文件 → 生成结构化 `Document` 对象。  
   - 切分：`DashScopeJsonNodeParser` 对解析结果进行语义分块（非必需，若用 `DashScopeCloudIndex` 则由云端自动完成）。  
   - 向量化：`DashScopeEmbedding` 为文本块生成向量 → `VectorStoreIndex.from_documents()` 构建本地索引；或 `DashScopeCloudIndex.from_documents()` 直接构建云端索引。  
   - 检索与生成：`index.as_query_engine()` 或 `index.as_retriever()` 构建引擎，传入用户查询，结合 `DashScopeRerank` 后处理，最终由 `DashScope` LLM 生成回答。

3. **Spring AI Alibaba 典型流程**：  
   - 添加 `spring-ai-alibaba-starter-dashscope` 依赖。  
   - 在 `application.yml` 中配置 `spring.ai.dashscope.api-key` 和 `spring.ai.dashscope.agent.app-id`（调用应用）或 `spring.ai.dashscope.workspace-id`（操作知识库）。  
   - 使用 `DashScopeAgent` 调用预置应用；或使用 `DashScopeDocumentRetriever` 检索云端知识库，并通过 `DocumentRetrievalAdvisor` 注入上下文至 `ChatClient` [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。

## 限制和注意事项

- **文件限制**：`DashScopeParse` 仅支持 `.pdf`、`.doc`、`.docx` 的智能解析，单文件 ≤100MB 且 ≤1000 页；其他格式（如 TXT、PPTX）仅原样上传，不解析 [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)。  
- **云端知识库约束**：`DashScopeCloudIndex` 构建的知识库强制使用百炼默认切分策略与 `text-embedding-v2` 嵌入模型，**不支持自定义**；如需完全控制，必须采用本地索引方案 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。  
- **业务空间要求**：所有云端操作（`DashScopeCloudIndex`、`DashScopeCloudRetriever`、Spring AI Alibaba 知识库检索）均**强依赖 `DASHSCOPE_WORKSPACE_ID` 环境变量**，未配置将直接报错，IDE 用户需手动注入该变量。  
- **模型兼容性**：`OpenAILike` 封装仅支持百炼的[文本生成类模型](raw/model-api-reference/qwen-api-reference.md)，不支持多模态或语音模型；`DashScope` 封装支持全部文本生成模型及部署后的私有模型。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)
- [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)
- [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)
- [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)
- [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)
- [DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)
- [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)


