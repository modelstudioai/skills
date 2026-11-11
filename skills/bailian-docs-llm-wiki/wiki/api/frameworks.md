# frameworks

百炼平台提供对主流 AI 开发框架的深度集成支持，重点覆盖 LlamaIndex 和 Spring AI Alibaba 两大生态。通过官方适配的 SDK 和插件，开发者可复用框架原生能力，同时无缝接入百炼的云端知识库、大模型服务、智能文档解析与重排等核心能力，显著降低 RAG、Agent 等应用的构建门槛与运维成本。

## 支持的模型与功能

百炼在 LlamaIndex 框架中提供完整能力链支持：
- **大模型调用**：支持 `qwen-max`、`qwen-plus` 等全部文本生成模型，既可通过 `DashScope` 原生封装（推荐），也可通过 `OpenAILike` 兼容模式调用 [选择模型](raw/model-user-guide/get-started-with-models/models.md)；
- **Embedding 模型**：提供 `text-embedding-v1/v2/v3` 三款向量模型，其中 `v3` 在 CMTEB Retrieval 任务上达 73.23 分，为当前最优 [使用 Embedding 模型](raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)；
- **智能文档解析**：`DashScopeParse` 基于“文档智能（Document Mind）”服务，支持 PDF/DOCX/DOC 格式智能化解析（含表格、公式、版面结构识别），其他格式仅原样上传 [DashScopeParse](raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)；
- **文本切分与重排**：`DashScopeJsonNodeParser` 提供语义感知的中文切分能力；`DashScopeRerank` 集成 `gte-rerank` 系列模型，支持混合检索后重排 [DashScopeRerank](raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)；
- **云端知识库管理**：`DashScopeCloudIndex` 与 `DashScopeCloudRetriever` 封装百炼云端索引服务，支持一键构建、增量更新与高并发检索。

Spring AI Alibaba 方面，支持两类核心集成：
- **大模型应用（Agent/Workflow）调用**：通过 `DashScopeAgent` 调用已发布的智能体或工作流应用，支持非流式与流式响应 [使用Spring AI Alibaba集成阿里云百炼大模型应用](raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)；
- **知识库检索**：通过 `DashScopeDocumentRetriever` 或直接 HTTP 调用 RAG API，实现带 `searchFilters`（支持 `_operator: OR` 及嵌套条件）的精准检索 [通过Spring AI Alibaba检索阿里云百炼知识库](raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。

> **注意**：文档 1 明确指出“本方案将知识库部署在云端，使用默认的智能文档切分与官方向量模型，**不支持自定义文档切分方式或自定义嵌入模型**”，而文档 3 和文档 9 分别提供了 `DashScopeEmbedding` 和 `DashScopeJsonNodeParser` 的本地化配置能力。这表明：**云端知识库（DashScopeCloudIndex）强制使用百炼托管的切分与向量化流程，而本地向量索引（VectorStoreIndex）则允许完全自定义 Embedding 和 NodeParser**。

## 关键参数

| 组件 | 关键参数 | 说明 | 默认值 |
|--------|-----------|------|---------|
| `DashScope` (LLM) | `model_name` | 指定调用的大模型，如 `"qwen-max"` | — |
| `DashScopeEmbedding` | `model_name` | 指定 Embedding 模型，如 `"text-embedding-v3"` | — |
| `DashScopeRerank` | `model`, `top_n`, `rerank_min_score` | 排序模型名、返回 Top-N 数量、重排后分数阈值 | `"gte-rerank"`, `3`, `0.0` |
| `DashScopeCloudRetriever` | `dense_similarity_top_k`, `sparse_similarity_top_k`, `enable_reranking`, `rerank_model_name`, `rerank_top_n` | 向量/文本召回数、是否启用重排、重排模型、重排后返回数 | `100`, `100`, `True`, `"gte-rerank-hybrid"`, `5` |
| `DashScopeJsonNodeParser` | `chunk_size`, `overlap_size`, `separator`, `language` | 切分块大小、重叠大小、分隔符正则、语言（`"cn"`/`"en"`） | `500`, `100`, `" \|,\|，\|。\|？\|！\|\n\|\?\|!"`, `"cn"` |

## 使用方式

### LlamaIndex 集成（Python）

1. **安装依赖**（按需组合）：
   ```bash
   pip install llama-index-core
   pip install llama-index-llms-dashscope          # LLM
   pip install llama-index-embeddings-dashscope    # Embedding
   pip install llama-index-readers-dashscope       # DashScopeParse
   pip install llama-index-node-parser-dashscope   # JsonNodeParser
   pip install llama-index-indices-managed-dashscope  # CloudIndex/CloudRetriever
   pip install llama-index-postprocessor-dashscope-rerank  # Rerank
   ```

2. **全局设置（可选）**：
   ```python
   from llama_index.core import Settings
   from llama_index.llms.dashscope import DashScope
   from llama_index.embeddings.dashscope import DashScopeEmbedding

   Settings.llm = DashScope(model_name="qwen-plus")
   Settings.embed_model = DashScopeEmbedding(model_name="text-embedding-v3")
   ```

3. **典型工作流**：
   - 用 `DashScopeParse` 解析本地 PDF/DOCX → 得到结构化 `Document`；
   - 用 `DashScopeJsonNodeParser` 切分 → 得到语义块 `Node`；
   - 用 `DashScopeCloudIndex.from_documents()` 上传并构建云端索引；
   - 用 `DashScopeCloudIndex("my_index").as_retriever()` 初始化检索器，传入 `rerank_top_n=3` 等参数；
   - 最终接入 `query_engine.query()` 完成 RAG。

### Spring AI Alibaba 集成（Java）

1. **添加依赖**（Maven）：
   ```xml
   <dependency>
       <groupId>com.alibaba.cloud.ai</groupId>
       <artifactId>spring-ai-alibaba-starter-dashscope</artifactId>
       <version>1.0.0.2</version>
   </dependency>
   ```

2. **配置环境变量**：
   ```
   DASHSCOPE_API_KEY=your_key
   APP_ID=your_agent_app_id        # Agent/Workflow 应用 ID
   WORKSPACE_ID=your_ws_id         # 可选，子业务空间时必需
   ```

3. **调用示例**：
   - **调用大模型应用**：注入 `DashScopeAgent`，调用 `agent.call(new Prompt("..."))`；
   - **检索知识库**：构造 `DashScopeDocumentRetrieverOptions` 并指定 `indexName`，或直接 HTTP 调用 `/api/v1/indices/rag/index/retrieve`，传入 `index_id` 与 `search_filters`。

## 限制和注意事项

- **文件解析限制**：`DashScopeParse` 仅对 `.pdf`、`.doc`、`.docx` 进行智能化解析（含版面、表格、公式），其余格式（如 `.txt`、`.md`）仅原样上传，不触发智能解析 [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)；
- **云端知识库不可定制**：使用 `DashScopeCloudIndex` 构建的云端知识库，其文档切分策略、Embedding 模型、索引结构均由百炼全托管，**不支持用户自定义**，与本地 `VectorStoreIndex` 的灵活性形成明确区分；
- **API Key 配置一致性**：所有组件均依赖 `DASHSCOPE_API_KEY` 环境变量；Spring AI Alibaba 默认读取 `AI_DASHSCOPE_API_KEY`，需确保环境变量名匹配或在 `application.yml` 中显式映射；
- **业务空间 ID 必填性**：`DashScopeCloudIndex`、`DashScopeCloudRetriever`、`DashScopeParse` 均要求 `DASHSCOPE_WORKSPACE_ID` 环境变量，即使使用默认业务空间也需显式设置为空字符串或有效 ID，否则初始化失败；
- **模型兼容性**：`OpenAILike` 方式仅支持百炼 OpenAI 兼容模式列表中的模型（见 [OpenAI 兼容模式支持的模型列表](https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope#eadfc13038jd5)），不支持全部百炼原生模型。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)
- [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)
- [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)
- [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)
- [DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)
- [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)
- [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)
- [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)


