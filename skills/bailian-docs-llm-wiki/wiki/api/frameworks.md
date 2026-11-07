# frameworks

阿里云百炼平台提供多套主流 AI 开发框架的官方集成支持，重点覆盖 LlamaIndex 和 Spring AI Alibaba 两大生态。开发者可基于这些框架快速构建 RAG 应用、知识库检索服务及大模型智能体，无需从零实现底层能力（如文档解析、向量索引、重排序、应用编排等），直接复用百炼托管的云端服务。所有集成均通过标准化 SDK 封装，与原生框架 API 兼容。

## 支持的模型/功能

百炼在框架层提供以下核心能力：

- **大模型调用**：支持全部百炼文本生成模型（如 `qwen-max`、`qwen-plus`），可通过 `DashScope` 或 OpenAI-like 封装两种方式接入 LlamaIndex；Spring AI Alibaba 则通过 `DashScopeAgent` 调用已发布的智能体或工作流应用 [通过 Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)。
- **Embedding 模型**：提供 `text-embedding-v1`/`v2`/`v3` 等多代嵌入模型，支持 MTEB/CMTEB 高分指标，适用于本地向量索引构建 [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)。
- **文档智能解析**：通过 `DashScopeParse` 调用“文档智能（Document Mind）”服务，支持 PDF/DOCX/DOC 格式深度解析（含表格、公式、版面结构），其他格式仅原样上传 [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)。
- **云端知识库管理**：`DashScopeCloudIndex` 实现文件上传、智能切分、向量索引与检索一体化，支持在百炼控制台可视化管理 [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)。
- **重排序（Rerank）**：集成 `gte-rerank` 系列模型，支持对初始检索结果进行语义级精排，提升相关性 [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)。
- **文本切分**：`DashScopeJsonNodeParser` 专为 `DashScopeParse` 的 JSON 输出设计，提供基于中文标点与语义的智能分块能力 [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)。

> **注意**：文档 1 明确指出“本方案将知识库部署在云端，使用默认的智能文档切分与官方向量模型，**不支持自定义文档切分方式或自定义嵌入模型**”，而文档 7 的 `DashScopeJsonNodeParser` 和文档 3 的 `DashScopeEmbedding` 均允许自定义切分策略与嵌入模型。该矛盾表明：**云端知识库（DashScopeCloudIndex）强制使用百炼托管的切分与嵌入流程；若需完全自定义，必须采用本地索引（VectorStoreIndex + DashScopeEmbedding）模式**。

## 关键参数

| 组件 | 关键参数 | 说明 | 默认值 |
|------|----------|------|--------|
| `DashScopeLLM` | `model_name` | 指定调用的大模型名称，如 `"qwen-max"` | — |
| `DashScopeEmbedding` | `model_name` | 指定嵌入模型，如 `"text-embedding-v3"` | `"text-embedding-v2"` |
| `DashScopeRerank` | `top_n`, `model` | 返回重排后 Top-K 结果；模型支持 `gte-rerank` | `top_n=3`, `model="gte-rerank"` |
| `DashScopeCloudRetriever` | `dense_similarity_top_k`, `enable_reranking`, `rerank_top_n` | 控制向量召回数量、是否启用重排、重排后返回数量 | `100`, `True`, `5` |
| `DashScopeJsonNodeParser` | `chunk_size`, `separator` | 分块大小与中文分隔符正则表达式 | `500`, `" \|,\|，\|。\|？\|！\|\n\|\?\|!"` |

## 使用方式

### LlamaIndex 集成（Python）

1. **安装依赖**：按需安装对应模块，例如：
   ```bash
   pip install llama-index-core llama-index-llms-dashscope  # 大模型
   pip install llama-index-embeddings-dashscope              # 嵌入
   pip install llama-index-indices-managed-dashscope         # 云端知识库
   ```

2. **配置认证**：设置环境变量 `DASHSCOPE_API_KEY`（必需），`DASHSCOPE_WORKSPACE_ID`（子业务空间必需）。

3. **代码示例**：
   - 本地向量索引：使用 `DashScopeEmbedding` + `VectorStoreIndex.from_documents()`。
   - 云端知识库：使用 `DashScopeCloudIndex.from_documents()` 构建，再通过 `as_query_engine()` 或 `as_retriever()` 初始化引擎。
   - 后处理：链式组合 `SimilarityPostprocessor`（阈值过滤）与 `DashScopeRerank`（重排）。

### Spring AI Alibaba 集成（Java）

1. **添加依赖**：在 `pom.xml` 中引入 `spring-ai-alibaba-starter-dashscope`。

2. **配置参数**：在 `application.yml` 中设置 `spring.ai.dashscope.api-key` 和 `spring.ai.dashscope.agent.app-id`（调用应用时）或 `spring.ai.dashscope.workspace-id`（操作子空间知识库时）。

3. **代码示例**：
   - 调用大模型应用：注入 `DashScopeAgent`，调用 `agent.call()`。
   - 检索知识库：使用 `DashScopeDocumentRetriever` 配合 `DocumentRetrievalAdvisor`，支持 `searchFilters` 进行字段级条件过滤 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。

## 限制和注意事项

- **文件限制**：`DashScopeParse` 仅对 `.pdf`/`.doc`/`.docx` 执行智能解析，其他格式（如 `.txt`、`.md`）仅原样上传；单文件 ≤100MB 且 ≤1000 页 [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)。
- **业务空间依赖**：所有云端操作（`DashScopeCloudIndex`、`DashScopeCloudRetriever`、Spring AI Alibaba 的知识库检索）均**强依赖 `DASHSCOPE_WORKSPACE_ID`**，未配置将报错。
- **模型兼容性**：OpenAI-like 封装仅支持百炼的**文本生成类模型**（如 `qwen-*`），不支持 embedding 或 rerank 模型；后者必须使用原生 DashScope SDK。
- **知识库更新**：`DashScopeCloudIndex` 当前不支持增量更新文档的原子操作（如 `index._insert()` 仅为实验性接口，文档 6 注明“支持更多参数设置”但未提供稳定 API），建议全量重建索引。
- **Spring AI Alibaba 版本要求**：知识库检索的 `searchFilters` 嵌套语法已在 `1.1.2.3` 版本验证，低版本可能存在兼容问题 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)
- [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)
- [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)
- [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)
- [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)
- [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)
- [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)
- [DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)


