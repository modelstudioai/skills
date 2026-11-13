# frameworks

阿里云百炼平台提供多套主流 AI 开发框架的官方集成支持，重点覆盖 LlamaIndex 和 Spring AI Alibaba 两大生态。通过标准化 SDK、适配器和云原生组件（如 `DashScopeCloudIndex`、`DashScopeDocumentRetriever`），开发者可快速构建 RAG 应用、调用大模型服务或检索云端知识库，无需从零实现底层能力。所有集成均基于百炼统一的 API 认证与计费体系。

## 支持的模型/功能

- **大模型调用**：支持全部百炼文本生成模型（如 `qwen-max`、`qwen-plus`），可通过 `DashScope` 或 OpenAI-like 封装两种方式接入 LlamaIndex [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)。
- **Embedding 模型**：提供 `text-embedding-v1`/`v2`/`v3` 三款向量模型，其中 `v3` 在 CMTEB Retrieval 任务上达 73.23 分，推荐用于高精度语义检索 [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)。
- **重排（Rerank）模型**：默认启用 `gte-rerank`，支持 `gte-rerank-hybrid`；适用于对初步检索结果进行语义精排 [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)。
- **文档解析与切分**：`DashScopeParse` 支持 PDF/DOCX/TXT 等 9 种格式智能解析（仅 PDF/DOC/DOCX 启用文档结构识别）；`DashScopeJsonNodeParser` 提供基于通义文本切分模型的细粒度分块能力 [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)。
- **云端知识库服务**：`DashScopeCloudIndex` 封装百炼云端索引全生命周期管理（上传、解析、建索引、检索），支持自动智能切分与官方向量模型，但**不支持自定义切分逻辑或嵌入模型** [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)。
- **Spring 生态集成**：`Spring AI Alibaba` 提供 `DashScopeAgent`（调用百炼应用）和 `DashScopeDocumentRetriever`（检索知识库）两类核心组件，支持非流式/流式调用及 `SearchFilters` 条件过滤 [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)。

> **注意**：文档 1 明确声明“不支持自定义文档切分方式或自定义嵌入模型”，而文档 3 和文档 10 分别提供了本地化 Embedding 和 NodeParser 的完整示例。二者适用场景不同：前者为纯云端托管方案（免运维），后者为本地可控方案（需自行部署依赖）。开发者应根据数据敏感性、定制化需求与运维能力选择路径。

## 关键参数

| 组件 | 参数名 | 类型 | 默认值 | 说明 |
|--------|--------|------|--------|------|
| `DashScopeLLM` | `model_name` | string | — | 必填，如 `"qwen-max"`；详见[选择模型](raw/model-user-guide/get-started-with-models/models.md) |
| `DashScopeEmbedding` | `model_name` | string | `"text-embedding-v2"` | 推荐使用 `v3` 提升检索质量 |
| `DashScopeRerank` | `model`, `top_n` | string, int | `"gte-rerank"`, `3` | `top_n` 控制返回结果数，超限则返回全部候选 |
| `DashScopeCloudRetriever` | `dense_similarity_top_k`, `enable_reranking`, `rerank_top_n` | int, bool, int | `100`, `True`, `5` | `dense_similarity_top_k` 影响向量召回数量；`rerank_top_n` 是重排后最终返回数 |
| `DashScopeJsonNodeParser` | `chunk_size`, `separator` | int, string | `500`, `" \|,\|，\|。\|？\|！\|\n\|\?\|!"` | `separator` 支持正则表达式，中文场景建议保留 `\n` 和标点 |

## 使用方式

### LlamaIndex 集成（Python）
1. **安装依赖**：按需安装对应模块，例如：
   ```bash
   pip install llama-index-llms-dashscope  # 大模型
   pip install llama-index-embeddings-dashscope  # Embedding
   pip install llama-index-indices-managed-dashscope  # 云端知识库
   ```
2. **配置认证**：设置环境变量 `DASHSCOPE_API_KEY`（必填）和 `DASHSCOPE_WORKSPACE_ID`（子空间时必填）。
3. **初始化组件**：
   - 云端知识库：`index = DashScopeCloudIndex("my_index_name")`
   - 本地向量索引：`index = VectorStoreIndex.from_documents(documents, embed_model=DashScopeEmbedding(model_name="text-embedding-v3"))`
   - 检索引擎：`query_engine = index.as_query_engine(node_postprocessors=[DashScopeRerank(top_n=3)])`

### Spring AI Alibaba 集成（Java）
1. **添加依赖**：在 `pom.xml` 中引入 `spring-ai-alibaba-starter-dashscope`。
2. **配置参数**：在 `application.yml` 中设置 `spring.ai.dashscope.api-key` 和 `spring.ai.dashscope.agent.app-id`（调用应用时）或 `spring.ai.dashscope.document-retriever.index-name`（检索知识库时）。
3. **调用服务**：
   - 调用应用：注入 `DashScopeAgent` 并执行 `agent.call(new Prompt("问题"))`。
   - 检索知识库：通过 `DashScopeDocumentRetriever` 配置 `searchFilters` 实现字段级条件过滤，再交由 `DocumentRetrievalAdvisor` 自动注入上下文 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。

## 限制和注意事项

- **文件解析限制**：`DashScopeParse` 仅对 PDF、DOC、DOCX 文件执行智能解析（提取表格、标题、段落结构）；TXT/MD/PPT 等格式仅原样上传，不解析语义结构 [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)。
- **云端知识库约束**：`DashScopeCloudIndex` 构建的知识库强制使用百炼默认的智能文档切分策略与官方向量模型，无法替换为自定义切分器或第三方 Embedding 模型 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。
- **业务空间要求**：所有云端操作（`DashScopeCloudIndex`、`DashScopeCloudRetriever`、Spring AI Alibaba 子空间调用）均需显式配置 `DASHSCOPE_WORKSPACE_ID` 环境变量，IDE 中需额外确认该变量已加载至运行时上下文。
- **模型兼容性**：OpenAI-like 封装仅支持百炼的文本生成类模型（如 `qwen-*`），不支持 `qwen-audio`、`qwen-vl` 等多模态模型；多模态场景请直接使用 DashScope 原生 SDK。
- **HTTP 直调 RAG API**：若选择绕过 Spring AI Alibaba SDK 直接调用 RAG API，必须使用 `workspace_id` 拼接完整 URL（如 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/indices/rag/index/retrieve`），且请求体需传 `index_id` 而非 `indexName` —— 二者不可混用 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)
- [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)
- [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)
- [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)
- [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)
- [DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)
- [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)


