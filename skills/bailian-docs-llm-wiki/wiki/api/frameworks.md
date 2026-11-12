# frameworks

阿里云百炼平台提供对主流 AI 开发框架的深度集成支持，重点覆盖 LlamaIndex 和 Spring AI Alibaba 两大生态。通过官方适配的 SDK 和插件，开发者可便捷地调用百炼的大模型服务、知识库检索、文档解析、嵌入向量生成等能力，无需自行维护底层基础设施。所有集成均基于百炼统一的 API Key 认证体系，并与控制台中的业务空间（Workspace）模型保持一致。

## 支持的模型/功能

百炼在 LlamaIndex 框架中提供以下核心能力模块：

- **大模型调用**：支持 `DashScope`（原生百炼模型）和 `OpenAILike`（OpenAI 兼容模式）两种封装方式，覆盖 `qwen-max`、`qwen-plus` 等全部文本生成模型 [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)。
- **嵌入模型（Embedding）**：提供 `text-embedding-v1/v2/v3` 系列模型，支持中文语义检索优化，其中 `text-embedding-v3` 在 CMTEB 检索任务上达 73.23 分 [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)。
- **智能文档解析**：`DashScopeParse` 基于“文档智能（DocMind）”服务，支持 PDF/DOCX/TXT 等格式的结构化解析（仅 PDF/DOC/DOCX 启用智能解析） [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)。
- **云端知识库管理**：`DashScopeCloudIndex` 实现从本地文件上传、云端智能切分、索引构建到检索引擎初始化的一站式流程 [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)。
- **重排序（Rerank）**：`DashScopeRerank` 集成 `gte-rerank` 系列模型，用于对初始检索结果进行语义精排 [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)。
- **文本切分**：`DashScopeJsonNodeParser` 对 `DashScopeParse` 的 JSON 输出进行高质量分块，支持按中文标点及换行符自定义切分逻辑 [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)。

Spring AI Alibaba 方面，支持两类集成：
- 调用百炼已发布的 **智能体应用（Agent 1.0）和工作流应用** [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)；
- 直接 **检索百炼云端知识库**，支持 `searchFilters` 多条件过滤 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。

> **注意**：文档 1 明确指出“本方案将知识库部署在云端，使用默认的智能文档切分与官方向量模型，不支持自定义文档切分方式或自定义嵌入模型”，而文档 5 和文档 8 分别提供了 `DashScopeJsonNodeParser` 和 `DashScopeEmbedding` 以支持自定义切分与嵌入。这表明：**云端知识库（DashScopeCloudIndex）本身不开放自定义切分/嵌入，但开发者可通过 LlamaIndex 本地索引路径（如 `VectorStoreIndex.from_documents` + `DashScopeEmbedding`）完全掌控切分与嵌入流程**。

## 关键参数

| 组件 | 关键参数 | 说明 | 默认值 |
|--------|-----------|------|---------|
| `DashScopeLLM` | `model_name` | 指定调用的百炼大模型，如 `"qwen-max"` | — |
| `DashScopeEmbedding` | `model_name` | 指定嵌入模型，如 `"text-embedding-v3"` | — |
| `DashScopeCloudIndex.from_documents()` | `name` | 云端知识库名称（需全局唯一） | — |
| `DashScopeCloudRetriever` / `index.as_retriever()` | `dense_similarity_top_k`, `sparse_similarity_top_k` | 向量/文本检索召回数量 | `100` |
| | `enable_reranking`, `rerank_model_name`, `rerank_top_n` | 是否启用重排、重排模型、返回节点数 | `True`, `"gte-rerank-hybrid"`, `5` |
| `DashScopeRerank` | `top_n`, `model` | 重排后返回 Top-N 结果、重排模型 | `3`, `"gte-rerank"` |
| `DashScopeJsonNodeParser` | `chunk_size`, `overlap_size`, `separator` | 分块大小、重叠大小、切分符正则表达式 | `500`, `100`, `" \|,\|，\|。\|？\|！\|\n\|\?\|!"` |

## 使用方式

### LlamaIndex（Python）

1. **安装依赖**（按需组合）：
   ```bash
   pip install llama-index-core
   pip install llama-index-llms-dashscope          # 大模型
   pip install llama-index-embeddings-dashscope    # 嵌入
   pip install llama-index-readers-dashscope       # 文档解析
   pip install llama-index-indices-managed-dashscope  # 云端知识库
   pip install llama-index-postprocessor-dashscope-rerank  # 重排
   pip install llama-index-node-parser-dashscope   # 文本切分
   ```

2. **环境配置**（必须）：
   ```bash
   export DASHSCOPE_API_KEY=your_api_key
   export DASHSCOPE_WORKSPACE_ID=your_workspace_id  # 如使用非默认业务空间
   ```

3. **典型流程**（云端 RAG）：
   - 用 `DashScopeParse` 解析本地文件 → `documents`
   - 用 `DashScopeCloudIndex.from_documents(documents, "my_index")` 构建云端知识库
   - 用 `DashScopeCloudIndex("my_index").as_query_engine(...)` 创建带重排的查询引擎
   - 调用 `query_engine.query("问题")`

> **注意**：文档 6 中 `DashScopeCloudIndex.from_documents()` 示例代码未显式传入 `workspace_id`，但其前提条件明确要求 `DASHSCOPE_WORKSPACE_ID` 必须通过环境变量设置；而文档 11 的 `DashScopeCloudRetriever` 构造函数直接接受 `index_name` 字符串，且示例中亦通过 `os.environ` 设置 `WORKSPACE_ID`。二者行为一致，**`workspace_id` 必须由环境变量注入，不可通过构造参数覆盖**。

### Spring AI Alibaba（Java）

1. **添加依赖**（Maven）：
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
         # workspace-id: ${WORKSPACE_ID}  # 可选
         agent:
           app-id: ${APP_ID}  # 调用应用时必需
   ```

3. **调用方式**：
   - **调用大模型应用**：注入 `DashScopeAgent`，调用 `agent.call(prompt)`
   - **检索知识库**：配置 `DashScopeDocumentRetriever` 并注入 `DocumentRetrievalAdvisor`

## 限制和注意事项

- **文件限制**：`DashScopeParse` 仅对 PDF/DOC/DOCX 进行智能解析；单文件 ≤100MB 或 1000 页；一次上传 ≤200 个文件 [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)。
- **云端知识库不可定制**：`DashScopeCloudIndex` 使用百炼托管的切分与嵌入策略，不支持用户指定切分规则或嵌入模型 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。
- **业务空间强依赖**：所有云端操作（`DashScopeCloudIndex`、`DashScopeCloudRetriever`、Spring AI Alibaba 知识库检索）均需正确配置 `DASHSCOPE_WORKSPACE_ID`，否则报错。
- **模型兼容性**：`OpenAILike` 封装仅支持百炼的文本生成模型（非所有模型），完整列表见 [OpenAI 兼容模式支持的模型列表](https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope#eadfc13038jd5)。
- **Spring Boot 版本要求**：Spring AI Alibaba 要求 Spring Boot 3.x + JDK 17+，HTTP 直调 RAG API 需 Spring Framework 6.1+（即 Spring Boot 3.2+）[通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)
- [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)
- [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)
- [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)
- [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)
- [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)
- [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)


