# frameworks

阿里云百炼平台提供对主流 AI 开发框架的原生支持，重点覆盖 LlamaIndex 和 Spring AI Alibaba 两大生态。通过官方适配的 SDK 和插件，开发者可快速集成百炼的大模型服务、知识库检索、文档解析与重排等能力，无需自行封装底层 API。所有框架集成均基于百炼统一的认证体系（API Key + 可选 Workspace ID），并复用平台已有的数据管理与模型调度能力。

## 支持的模型/功能

百炼在框架层提供以下核心能力：

- **大模型调用**：支持全部百炼文本生成模型（如 `qwen-max`、`qwen-plus`），可通过 `DashScope` 或 OpenAI-like 封装两种方式接入 LlamaIndex；Spring AI Alibaba 则通过 `DashScopeAgent` 调用智能体/工作流应用 [通过Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)。
- **Embedding 模型**：提供 `text-embedding-v1`/`v2`/`v3` 系列向量模型，支持 MTEB/CMTEB 高分指标，适用于构建本地向量索引 [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)。
- **文档解析与切分**：`DashScopeParse` 支持 PDF/DOCX/DOC 智能解析（基于 Document Mind），`DashScopeJsonNodeParser` 提供基于通义文本切分模型的语义分块能力。
- **云端知识库服务**：`DashScopeCloudIndex` 实现文件上传、智能切分、向量索引与检索一体化；`DashScopeCloudRetriever` 提供稠密/稀疏混合检索与 GTE-Rerank 重排 [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)。
- **RAG 检索增强**：Spring AI Alibaba 提供 `DashScopeDocumentRetriever` SDK 及 RAG API 直调能力，支持 `searchFilters` 多条件过滤与嵌套逻辑。

> **注意**：文档 1 明确指出“本方案将知识库部署在云端，使用默认的智能文档切分与官方向量模型，不支持自定义文档切分方式或自定义嵌入模型”，而文档 6 和文档 3 分别提供了 `DashScopeJsonNodeParser` 和 `DashScopeEmbedding` 用于本地自定义切分与向量化。二者适用场景不同：前者为全托管云端知识库（零配置），后者为完全可控的本地 RAG 流程，不存在矛盾，但需按需选择。

## 关键参数

| 组件 | 参数名 | 类型 | 默认值 | 说明 |
|--------|---------|------|---------|------|
| `DashScopeLLM` | `model_name` | string | — | 必填，如 `"qwen-max"`；完整列表见 [选择模型](raw/model-user-guide/get-started-with-models/models.md) |
| `DashScopeEmbedding` | `model_name` | string | `"text-embedding-v2"` | 推荐使用 `v3`（CMTEB Retrieval 73.23 分） |
| `DashScopeRerank` | `model` | string | `"gte-rerank"` | 支持 `"gte-rerank-hybrid"`（文档 8）和 `"gte-rerank"`（文档 4） |
| `DashScopeCloudRetriever` | `dense_similarity_top_k` | int | `100` | 向量召回数量；`sparse_similarity_top_k` 同理 |
| `DashScopeCloudRetriever` | `enable_reranking` | bool | `True` | 是否启用重排；若关闭，`rerank_*` 参数无效 |
| `DashScopeCloudRetriever` | `rerank_min_score` | float | `0.0` | 仅在 `enable_reranking=True` 时生效，过滤低分节点 |
| `DashScopeJsonNodeParser` | `chunk_size` / `overlap_size` | int | `500` / `100` | 影响切分粒度与上下文连贯性 |

## 使用方式

### LlamaIndex 集成（推荐 Python 生态）

1. **安装依赖**  
   根据所需能力安装对应包（非全量）：
   ```bash
   # 基础
   pip install llama-index-core
   # 大模型
   pip install llama-index-llms-dashscope  # 或 llama-index-llms-openai-like
   # Embedding
   pip install llama-index-embeddings-dashscope
   # 文档解析
   pip install llama-index-readers-dashscope
   # 云端知识库
   pip install llama-index-indices-managed-dashscope
   # 重排
   pip install llama-index-postprocessor-dashscope-rerank
   ```

2. **全局设置（可选）**  
   ```python
   from llama_index.core import Settings
   from llama_index.llms.dashscope import DashScope
   from llama_index.embeddings.dashscope import DashScopeEmbedding

   Settings.llm = DashScope(model_name="qwen-plus")
   Settings.embed_model = DashScopeEmbedding(model_name="text-embedding-v3")
   ```

3. **典型流程示例**  
   - 本地 RAG：`SimpleDirectoryReader` → `VectorStoreIndex.from_documents(..., embed_model=DashScopeEmbedding)`  
   - 云端 RAG：`DashScopeParse` → `DashScopeCloudIndex.from_documents()` → `index.as_query_engine(..., node_postprocessors=[DashScopeRerank()])`  
   - 混合检索：`DashScopeCloudRetriever` 初始化时同时配置 `dense_similarity_top_k` 和 `sparse_similarity_top_k`。

### Spring AI Alibaba 集成（推荐 Java/Spring 生态）

1. **添加 Maven 依赖**  
   ```xml
   <dependency>
       <groupId>com.alibaba.cloud.ai</groupId>
       <artifactId>spring-ai-alibaba-starter-dashscope</artifactId>
       <version>1.0.0.2</version>
   </dependency>
   ```

2. **配置 `application.yml`**  
   ```yaml
   spring:
     ai:
       dashscope:
         api-key: ${DASHSCOPE_API_KEY}
         # workspace-id: ${WORKSPACE_ID}  # 子空间必填
         agent:
           app-id: ${APP_ID}  # 智能体/工作流应用ID
   ```

3. **Java 代码调用**  
   - 调用应用：注入 `DashScopeAgent`，传入 `Prompt` 和 `DashScopeAgentOptions.withAppId()`  
   - 检索知识库：使用 `DashScopeDocumentRetriever` + `DocumentRetrievalAdvisor`，支持 `searchFilters` 条件过滤 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。

## 限制和注意事项

- **环境要求**：所有 LlamaIndex 组件要求 Python 3.9–3.12；Spring AI Alibaba 要求 JDK 17+、Spring Boot 3.x。
- **文件限制**：`DashScopeParse` 仅对 PDF/DOC/DOCX 进行智能解析，其他格式（TXT/MD/PPT 等）仅原样上传；单文件 ≤100MB 且 ≤1000 页 [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)。
- **业务空间强制依赖**：`DashScopeCloudIndex`、`DashScopeCloudRetriever`、`DashScopeDocumentRetriever` 均需配置 `DASHSCOPE_WORKSPACE_ID` 环境变量，否则初始化失败（文档 7、8、11 均明确强调）。
- **API Key 配置方式**：LlamaIndex 组件优先读取 `DASHSCOPE_API_KEY` 环境变量；Spring AI Alibaba 默认读取 `DASHSCOPE_API_KEY`（文档 10）或 `AI_DASHSCOPE_API_KEY`（文档 11），二者不兼容，需统一配置。
- **模型兼容性**：OpenAI-like 封装仅支持百炼的文本生成模型（不支持 embedding/rerank），详见 [OpenAI 兼容模式支持的模型列表](https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope#eadfc13038jd5)。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)
- [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)
- [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)
- [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)
- [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)
- [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)
- [DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)
- [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)


