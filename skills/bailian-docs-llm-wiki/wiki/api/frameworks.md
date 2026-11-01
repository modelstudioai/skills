# frameworks

阿里云百炼平台提供对主流 AI 开发框架的深度集成支持，当前重点覆盖 LlamaIndex 和 Spring AI Alibaba 两大生态。通过官方适配的 SDK 和插件，开发者可快速将百炼的模型服务、知识库管理、RAG 检索增强等能力嵌入现有应用架构，无需从零实现底层对接逻辑。所有集成均基于标准 API 协议，并严格遵循各框架的扩展规范。

## 支持的模型与功能

百炼在 LlamaIndex 生态中提供全链路组件支持：
- **大模型调用**：支持 `DashScope`（推荐，全模型覆盖）和 `OpenAILike`（兼容 OpenAI 接口）两种方式调用 `qwen-max`、`qwen-plus` 等全部文本生成模型 [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)；
- **向量嵌入**：提供 `text-embedding-v1/v2/v3` 系列 Embedding 模型，支持通过 `DashScopeEmbedding` 组件构建本地向量索引 [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)；
- **智能文档解析**：`DashScopeParse` 基于“文档智能（Document Mind）”服务，支持 PDF/DOCX/DOC 格式文件的结构化解析（其他格式仅原样上传）；
- **云端知识库管理**：`DashScopeCloudIndex` 实现知识库的创建、文档上传、智能切分与索引构建，`DashScopeCloudRetriever` 提供开箱即用的检索器 [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)；
- **重排序（Rerank）**：`DashScopeRerank` 集成 `gte-rerank` 系列模型，用于对初步检索结果进行语义精排；
- **文本切分**：`DashScopeJsonNodeParser` 专为 `DashScopeParse` 的 JSON 输出设计，提供中文友好的智能分块能力。

Spring AI Alibaba 方面，支持两类核心集成：
- **大模型应用调用**：通过 `DashScopeAgent` 调用已发布的智能体（Agent 1.0）或工作流（Workflow）应用 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)；
- **知识库检索**：支持 SDK 封装的 `DashScopeDocumentRetriever` 或直接 HTTP 调用 RAG API 进行知识库检索 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。

> **注意**：文档 1 明确指出“本方案将知识库部署在云端，使用默认的智能文档切分与官方向量模型，不支持自定义文档切分方式或自定义嵌入模型”，而文档 6 和文档 2 分别提供了 `DashScopeJsonNodeParser` 和 `DashScopeEmbedding` 用于自定义切分与嵌入。这表明：**云端知识库（DashScopeCloudIndex）强制使用百炼托管的切分与嵌入流程；而本地向量索引（VectorStoreIndex）则完全支持自定义**。开发者需根据部署模式选择对应组件。

## 关键参数

| 组件 | 关键参数 | 说明 | 默认值 |
|--------|----------|------|--------|
| `DashScopeEmbedding` | `model_name` | Embedding 模型名称 | `"text-embedding-v2"` |
| `DashScopeRerank` | `model`, `top_n`, `rerank_min_score` | 排序模型、返回数量、分数阈值 | `"gte-rerank"`, `3`, `0.0` |
| `DashScopeCloudRetriever` | `dense_similarity_top_k`, `enable_reranking`, `rerank_model_name` | 向量召回数、是否启用重排、重排模型 | `100`, `True`, `"gte-rerank-hybrid"` |
| `DashScopeJsonNodeParser` | `chunk_size`, `overlap_size`, `separator` | 分块大小、重叠大小、分隔符正则 | `500`, `100`, `" \|,\|，\|。\|？\|！\|\n\|\?\|\!"` |
| Spring AI Alibaba (`DashScopeDocumentRetriever`) | `indexName`, `searchFilters` | 知识库名称、字段过滤条件 | — | 

## 使用方式

### LlamaIndex 集成
1. **安装依赖**：按需安装对应组件包，例如 `pip install llama-index-embeddings-dashscope llama-index-indices-managed-dashscope`；
2. **配置凭证**：设置环境变量 `DASHSCOPE_API_KEY`（必选），若使用子业务空间还需设置 `DASHSCOPE_WORKSPACE_ID`；
3. **初始化组件**：直接实例化或通过 `Settings` 全局配置，例如 `Settings.embed_model = DashScopeEmbedding(model_name="text-embedding-v3")`；
4. **构建流程**：组合使用 `DashScopeParse` → `DashScopeJsonNodeParser` → `VectorStoreIndex`（本地索引）或 `DashScopeCloudIndex`（云端索引）→ `DashScopeRerank`（后处理）。

### Spring AI Alibaba 集成
1. **添加 Maven 依赖**：引入 `spring-ai-alibaba-starter-dashscope`；
2. **配置凭证与 ID**：在 `application.yml` 中配置 `spring.ai.dashscope.api-key`、`spring.ai.dashscope.agent.app-id` 及可选的 `workspace-id`；
3. **声明式调用**：
   - 应用调用：注入 `DashScopeAgent` 并调用 `agent.call()`；
   - 知识库检索：配置 `DashScopeDocumentRetrieverOptions` 并注入 `DocumentRetriever`，结合 `DocumentRetrievalAdvisor` 实现 RAG 流程。

## 限制和注意事项

- **文件解析限制**：`DashScopeParse` 仅对 `.pdf`、`.doc`、`.docx` 文件执行智能解析（提取文本、表格、布局等），其余格式（如 `.txt`、`.md`）仅原样上传，不进行内容理解 [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)；
- **云端知识库约束**：`DashScopeCloudIndex` 构建的知识库强制使用百炼平台的文档切分策略与嵌入模型，**不支持用户指定 `embed_model` 或自定义切分逻辑**，此为平台托管服务的设计特性；
- **环境变量命名差异**：Spring AI Alibaba 文档（文档 9、11）要求使用 `AI_DASHSCOPE_API_KEY` 和 `AI_DASHSCOPE_WORKSPACE_ID`，而 LlamaIndex 文档（文档 1-8）统一使用 `DASHSCOPE_API_KEY` 和 `DASHSCOPE_WORKSPACE_ID`。跨框架开发时需注意环境变量隔离；
- **版本兼容性**：`DashScopeCloudIndex` 和 `DashScopeCloudRetriever` 要求 Python 3.9–3.12；Spring AI Alibaba 要求 JDK 17+、Spring Boot 3 GA+，且不同 SAA 版本对 RAG 功能支持有差异（如嵌套 `SearchFilters` 在 1.1.2.3 版本验证）。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)
- [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)
- [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)
- [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)
- [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)
- [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)
- [DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)


