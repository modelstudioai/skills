# frameworks

百炼平台提供对主流 AI 开发框架的原生集成支持，重点覆盖 LlamaIndex 和 Spring AI Alibaba 两大生态，帮助开发者快速构建 RAG、智能体、工作流等生产级应用。所有集成均基于百炼统一的 API 认证体系（`DASHSCOPE_API_KEY`）和业务空间隔离机制，支持云端知识库管理、模型调用、嵌入向量化及重排序等核心能力。

## 支持的模型/功能

- **大模型调用**：支持通过 `DashScope` 和 `OpenAILike` 两种方式接入百炼全部文本生成模型（如 `qwen-max`、`qwen-plus`），详见 [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)。
- **Embedding 模型**：提供 `text-embedding-v1`/`v2`/`v3` 三款官方 Embedding 模型，支持 MTEB/CMTEB 高分检索任务，适用于本地向量索引构建。
- **文档解析与切分**：`DashScopeParse` 支持 PDF/DOCX/DOC 智能解析（基于 Document Mind），`DashScopeJsonNodeParser` 提供基于通义文本切分模型的细粒度分块能力，二者可组合使用实现端到端文档处理流水线。
- **云端知识库服务**：`DashScopeCloudIndex` 封装百炼云端知识库的创建、更新与检索逻辑；`DashScopeCloudRetriever` 提供稠密/稀疏混合检索、重排序（`gte-rerank-hybrid`）、分数阈值过滤等高级参数控制。
- **重排序模型**：`DashScopeRerank` 集成 GTE-Rerank 系列模型，支持对初始检索结果进行语义级精排，提升 RAG 回答相关性。
- **Spring 生态支持**：`Spring AI Alibaba` 提供 `DashScopeAgent`（调用智能体/工作流应用）和 `DashScopeDocumentRetriever`（检索知识库）两类核心组件，适配 Spring Boot 3.x + JDK 17+ 环境。

> **注意**：文档 1 明确指出“本方案将知识库部署在云端，使用默认的智能文档切分与官方向量模型，**不支持自定义文档切分方式或自定义嵌入模型**”，而文档 4 和文档 3 分别提供了 `DashScopeJsonNodeParser` 和 `DashScopeEmbedding` 的自定义能力。这意味着：**云端知识库（`DashScopeCloudIndex`）强制使用百炼托管的切分与向量化流程；若需完全自定义，必须采用本地向量索引（`VectorStoreIndex`）模式**。该矛盾已在文档 6 中得到印证——其明确区分了“基于本地文件构建云端知识库”（依赖 `DashScopeParse`）与“直接使用云端知识库”两种路径。

## 关键参数

| 组件 | 参数名 | 类型 | 默认值 | 说明 |
|--------|---------|------|---------|------|
| `DashScopeCloudRetriever` | `dense_similarity_top_k` | `int` | `100` | 向量检索召回数量 |
| `DashScopeCloudRetriever` | `enable_reranking` | `bool` | `True` | 是否启用重排序（默认开启） |
| `DashScopeCloudRetriever` | `rerank_model_name` | `str` | `gte-rerank-hybrid` | 重排模型，支持 `gte-rerank-hybrid` 和 `gte-rerank` |
| `DashScopeCloudRetriever` | `rerank_top_n` | `int` | `5` | 重排后返回的节点数 |
| `DashScopeRerank` | `top_n` | `int` | `3` | 重排后返回的 top 文档数（与上者语义一致，但作用域不同） |
| `DashScopeJsonNodeParser` | `chunk_size` | `int` | `500` | 文本块大小（字符数） |
| `DashScopeJsonNodeParser` | `separator` | `str` | `" \|,\|，\|。\|？\|！\|\n\|\?\|\!"` | 中文常用分隔符正则表达式 |

## 使用方式

1. **环境准备**  
   - 设置环境变量：`DASHSCOPE_API_KEY`（必填），`DASHSCOPE_WORKSPACE_ID`（子空间场景必填）。
   - 安装对应包（以 LlamaIndex 为例）：
     ```bash
     pip install llama-index-core
     pip install llama-index-llms-dashscope  # 大模型
     pip install llama-index-embeddings-dashscope  # Embedding
     pip install llama-index-readers-dashscope  # DashScopeParse
     pip install llama-index-indices-managed-dashscope  # DashScopeCloudIndex
     pip install llama-index-postprocessor-dashscope-rerank  # 重排序
     ```

2. **典型流程（LlamaIndex）**  
   - **文档解析**：用 `DashScopeParse` 加载 PDF/DOCX 文件 → 获得结构化 `Document` 对象。  
   - **切分与索引**：  
     - *云端*：`DashScopeCloudIndex.from_documents(...)` 自动完成切分、向量化、索引上传；  
     - *本地*：`VectorStoreIndex.from_documents(..., embed_model=DashScopeEmbedding(...))`。  
   - **检索增强**：`index.as_query_engine(..., node_postprocessors=[SimilarityPostprocessor(), DashScopeRerank()])` 构建 RAG 引擎。  
   - **查询执行**：`query_engine.query("问题")` 返回带来源的结构化响应。

3. **典型流程（Spring AI Alibaba）**  
   - 在 `application.yml` 中配置 `spring.ai.dashscope.api-key` 和 `app-id`（应用调用）或 `index-name`（知识库检索）。  
   - 使用 `DashScopeAgent` 调用已发布的大模型应用（仅限 Agent 1.0 / 工作流）；  
   - 使用 `DashScopeDocumentRetriever` 集成 `DocumentRetrievalAdvisor` 实现知识库驱动的 ChatClient。

## 限制和注意事项

- **文件格式与大小限制**：`DashScopeParse` 仅对 `.pdf`、`.docx`、`.doc` 进行智能解析；单文件 ≤100MB 且 ≤1000 页；其他格式（如 TXT/PPTX）仅原样上传，不解析 [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)。
- **云端知识库不可定制**：`DashScopeCloudIndex` 强制使用百炼托管的文档切分与向量化逻辑，不开放自定义切分器或 Embedding 模型选项 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。
- **业务空间强依赖**：所有云端操作（`DashScopeCloudIndex`、`DashScopeCloudRetriever`、`Spring AI Alibaba` 知识库检索）均需显式配置 `DASHSCOPE_WORKSPACE_ID`，否则报错。
- **模型兼容性**：`OpenAILike` 方式仅支持百炼的文本生成模型（非多模态），且需使用 `is_chat_model=True`；`DashScope` 方式支持全部文本生成模型及部署模型。
- **Spring AI Alibaba 应用类型限制**：仅支持集成智能体应用（Agent 1.0）和工作流应用，不支持对话应用或提示词应用 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)
- [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)
- [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)
- [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)
- [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)
- [DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)
- [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)
- [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)


