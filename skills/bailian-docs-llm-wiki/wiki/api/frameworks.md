# frameworks

百炼平台提供对主流 AI 开发框架的原生集成支持，重点覆盖 LlamaIndex 和 Spring AI Alibaba 两大生态。通过官方适配的 SDK 和插件，开发者可快速将百炼的大模型服务、知识库检索、文档解析与重排等能力嵌入现有工作流，无需从零实现底层对接逻辑。所有集成均基于百炼统一的 API 认证体系（`DASHSCOPE_API_KEY`）和业务空间隔离机制。

## 支持的模型/功能

- **大模型调用**：支持全部百炼文本生成模型（如 `qwen-max`、`qwen-plus`），可通过 LlamaIndex 的 `DashScope` 或 `OpenAILike` 封装调用；Spring AI Alibaba 则通过 `DashScopeAgent` 集成智能体/工作流应用 [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)。
- **Embedding 模型**：提供 `text-embedding-v1`/`v2`/`v3` 三款向量模型，支持在 LlamaIndex 中构建本地向量索引 [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)。
- **文档解析与切分**：`DashScopeParse` 支持 PDF/DOCX/TXT 等格式的智能解析（依赖“文档智能”服务）；`DashScopeJsonNodeParser` 提供基于通义文本切分模型的语义化分块能力，专为 `DashScopeParse` 输出设计 [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)。
- **云端知识库与检索**：`DashScopeCloudIndex` 实现云端知识库的创建、更新与检索；`DashScopeCloudRetriever` 提供稠密/稀疏混合检索、重排（`gte-rerank`）、分数过滤等高级参数控制 [DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)。
- **重排（Rerank）**：`DashScopeRerank` 集成 `gte-rerank` 系列模型，用于对初筛结果进行语义级精排 [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)。

> **注意**：文档 1 明确指出“本方案将知识库部署在云端，使用默认的智能文档切分与官方向量模型，**不支持自定义文档切分方式或自定义嵌入模型**”，而文档 4 和文档 11 分别提供了自定义 Embedding 模型和自定义文本切分的能力。这表明：**云端知识库（DashScopeCloudIndex）强制使用百炼托管的切分与向量化流程，而本地索引（VectorStoreIndex）则完全支持自定义**。开发者需根据部署模式选择对应能力。

## 关键参数

| 组件 | 关键参数 | 说明 | 默认值 |
|--------|-----------|------|---------|
| `DashScope` (LLM) | `model_name` | 指定调用的百炼大模型名称 | `"qwen-plus"` |
| `DashScopeEmbedding` | `model_name` | 指定 Embedding 模型版本 | `"text-embedding-v2"` |
| `DashScopeCloudRetriever` | `dense_similarity_top_k`, `sparse_similarity_top_k` | 向量/文本检索召回数量 | `100` |
| | `enable_reranking`, `rerank_model_name` | 是否启用重排及重排模型 | `True`, `"gte-rerank-hybrid"` |
| | `rerank_top_n`, `rerank_min_score` | 重排后返回数量与最低分数阈值 | `5`, `0.0` |
| `DashScopeRerank` | `top_n`, `model` | 重排返回 Top-N 结果、模型名 | `3`, `"gte-rerank"` |
| `DashScopeJsonNodeParser` | `chunk_size`, `overlap_size`, `separator` | 分块大小、重叠长度、分割符正则 | `500`, `100`, `" \|,\|，\|。\|？\|！\|\n\|\?\|!"` |

## 使用方式

1. **环境准备**：配置 `DASHSCOPE_API_KEY`（必需）和 `DASHSCOPE_WORKSPACE_ID`（仅当使用非默认业务空间时必需）到环境变量。
2. **安装依赖**：
   - LlamaIndex：按需安装 `llama-index-llms-dashscope`、`llama-index-embeddings-dashscope`、`llama-index-indices-managed-dashscope` 等子包；
   - Spring AI Alibaba：添加 `spring-ai-alibaba-starter-dashscope` 依赖。
3. **初始化客户端**：
   - LlamaIndex：直接实例化 `DashScope()`、`DashScopeEmbedding()` 或 `DashScopeCloudIndex("my_index")`；
   - Spring AI Alibaba：通过 `application.yml` 配置 `spring.ai.dashscope.agent.app-id` 和 `api-key`，注入 `DashScopeAgent` 或 `DashScopeDocumentRetriever`。
4. **调用链路**：
   - 本地 RAG：`SimpleDirectoryReader` → `DashScopeParse` → `DashScopeJsonNodeParser` → `VectorStoreIndex` → `query_engine.query()`；
   - 云端 RAG：`DashScopeParse` → `DashScopeCloudIndex.from_documents()` → `index.as_query_engine()`；
   - 应用集成：Spring Boot Controller 调用 `DashScopeAgent.call()` 或 `DashScopeDocumentRetriever.retrieve()`。

## 限制和注意事项

- **文件限制**：`DashScopeParse` 仅对 PDF/DOC/DOCX 进行智能解析，其他格式（如 TXT、MD）仅原样上传；单文件 ≤100MB 且 ≤1000 页 [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)。
- **业务空间强依赖**：`DashScopeCloudIndex` 和 `DashScopeCloudRetriever` **必须**配置 `DASHSCOPE_WORKSPACE_ID`，否则初始化失败；而 `DashScope` 和 `DashScopeEmbedding` 可在无 workspace ID 下运行。
- **模型兼容性**：`DashScopeRerank` 当前仅支持 `gte-rerank` 系列模型，`gte-rerank-hybrid` 仅在 `DashScopeCloudRetriever` 中可用，二者参数命名不一致（`top_n` vs `rerank_top_n`），需按组件分别查阅。
- **Spring AI Alibaba 环境变量差异**：文档 9 要求 `DASHSCOPE_API_KEY`，而文档 10 要求 `AI_DASHSCOPE_API_KEY`，实际使用中应以 `application.yml` 中引用的变量名（`${AI_DASHSCOPE_API_KEY}`）为准，避免混淆。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)
- [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)
- [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)
- [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)
- [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)
- [DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)
- [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)
- [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)


