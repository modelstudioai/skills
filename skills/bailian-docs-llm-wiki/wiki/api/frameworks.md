# frameworks

百炼平台提供对主流 AI 开发框架的深度集成支持，重点覆盖 LlamaIndex 和 Spring AI Alibaba 两大生态。开发者可基于这些框架快速构建 RAG 应用、调用云端大模型与 Embedding 服务、管理知识库索引，并实现与百炼智能体/工作流应用的对接。所有集成均通过官方适配器封装，屏蔽底层 API 差异，聚焦业务逻辑。

## 支持的模型与功能

- **大模型（LLM）**：支持 `qwen-max`、`qwen-plus` 等全部百炼文本生成模型，可通过 `DashScope` 或 OpenAI-like 封装调用 [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)。
- **Embedding 模型**：支持 `text-embedding-v1`/`v2`/`v3`，其中 `v3` 在 CMTEB Retrieval 任务上达 73.23 分，为当前最优 [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)。
- **重排（Rerank）模型**：默认使用 `gte-rerank`，也支持 `gte-rerank-hybrid`，用于提升检索结果相关性排序质量 [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)。
- **文档解析与切分**：`DashScopeParse` 调用文档智能（DocMind）服务解析 PDF/DOCX/DOC；`DashScopeJsonNodeParser` 基于语义结构对解析结果进行高质量切分。
- **云端知识库服务**：`DashScopeCloudIndex` 与 `DashScopeCloudRetriever` 提供端到端的云端索引构建、文档上传、智能切分、向量/稀疏检索及重排能力。

> **注意**：文档 1 明确指出“本方案将知识库部署在云端，使用默认的智能文档切分与官方向量模型，**不支持自定义文档切分方式或自定义嵌入模型**”，而文档 3 和文档 6 分别提供了本地化 Embedding 和 NodeParser 的完整控制能力。二者定位不同：前者为全托管 SaaS 模式，后者为可定制 SDK 模式，需按场景选择。

## 关键参数

| 组件 | 参数 | 类型 | 默认值 | 说明 |
|------|------|------|--------|------|
| `DashScopeLLM` | `model_name` | string | — | 必填，如 `"qwen-plus"`；完整列表见[选择模型](raw/model-user-guide/get-started-with-models/models.md) |
| `DashScopeEmbedding` | `model_name` | string | `"text-embedding-v2"` | 推荐使用 `v3` 获取最佳检索效果 |
| `DashScopeRerank` | `top_n`, `model` | int, string | `5`, `"gte-rerank"` | `top_n` 控制返回结果数；`model` 可选 `gte-rerank-hybrid`（文档 10） |
| `DashScopeCloudRetriever` | `dense_similarity_top_k`, `enable_reranking`, `rerank_top_n` | int, bool, int | `100`, `True`, `5` | 向量召回数、是否启用重排、重排后返回数（文档 10） |
| `DashScopeJsonNodeParser` | `chunk_size`, `separator` | int, string | `500`, `" \|,\|，\|。\|？\|！\|\n\|\?\|!"` | 中文推荐保留默认分隔符集 |

## 使用方式

### LlamaIndex 生态
1. **安装依赖**：根据组件选择安装包，例如：
   ```bash
   pip install llama-index-llms-dashscope          # LLM
   pip install llama-index-embeddings-dashscope    # Embedding
   pip install llama-index-postprocessor-dashscope-rerank  # Rerank
   pip install llama-index-indices-managed-dashscope       # CloudIndex
   ```
2. **初始化与调用**：
   - 全局设置（推荐）：`Settings.llm = DashScope(model_name="qwen-plus")`
   - 按需实例化：`retriever = DashScopeCloudRetriever("my_index")`
   - 构建 RAG 流程：`index.as_query_engine(node_postprocessors=[DashScopeRerank(top_n=3)])`

### Spring AI Alibaba 生态
1. **添加 Maven 依赖**：
   ```xml
   <dependency>
       <groupId>com.alibaba.cloud.ai</groupId>
       <artifactId>spring-ai-alibaba-starter-dashscope</artifactId>
       <version>1.0.0.2</version>
   </dependency>
   ```
2. **配置 `application.yml`**：
   ```yaml
   spring:
     ai:
       dashscope:
         api-key: ${DASHSCOPE_API_KEY}
         agent:
           app-id: ${APP_ID}  # 调用智能体/工作流时必需
         # workspace-id: ${WORKSPACE_ID}  # 子空间时必需
   ```
3. **Java 调用**：
   - 非流式：`agent.call(new Prompt(message))`
   - RAG 检索：注入 `DashScopeDocumentRetriever` 并绑定至 `ChatClient`

## 限制和注意事项

- **文件解析限制**：`DashScopeParse` 仅对 PDF/DOC/DOCX 进行智能解析；TXT/MD/PPT 等格式仅原样上传，不触发 DocMind（文档 7）。
- **文件规格上限**：单个文件 ≤ 100MB 且 ≤ 1000 页；一次上传最多 200 个文件（文档 7）。
- **环境变量要求**：所有 DashScope 组件均依赖 `DASHSCOPE_API_KEY`；若使用非默认业务空间，**必须**配置 `DASHSCOPE_WORKSPACE_ID`（文档 5、7、10）。
- **Python 版本兼容性**：所有 LlamaIndex 相关包要求 `python>=3.9,<=3.12`（文档 4、5、6、10）。
- **Spring Boot 版本要求**：Spring AI Alibaba 仅支持 Spring Boot 3.x + JDK 17+（文档 8、9）。
- **云端知识库不可定制性**：如文档 1 所述，`DashScopeCloudIndex` 方案**不支持自定义文档切分逻辑或替换嵌入模型**，如需完全控制，请改用 `DashScopeEmbedding` + `VectorStoreIndex` 本地构建方案 [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)
- [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)
- [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)
- [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)
- [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)
- [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)
- [DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)
- [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)


