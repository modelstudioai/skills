# frameworks

百炼平台提供对主流 AI 开发框架的深度集成支持，重点覆盖 LlamaIndex 和 Spring AI Alibaba 两大生态。开发者可通过标准化 SDK 和适配器，将百炼的模型服务、知识库管理、文档解析与重排等能力无缝嵌入现有应用架构，无需从零构建基础设施。所有集成均基于百炼统一的 API Key 认证体系，并支持业务空间（Workspace）隔离。

## 支持的模型与功能

百炼通过官方适配器支持以下核心能力：

- **大语言模型调用**：支持 `qwen-max`、`qwen-plus`、`qwen-turbo` 等全部百炼文本生成模型，既可通过 DashScope 原生 SDK（[使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)），也可通过 OpenAI 兼容模式接入（需配置 `api_base="https://dashscope.aliyuncs.com/compatible-mode/v1"`）。
- **Embedding 模型**：提供 `text-embedding-v1`/`v2`/`v3` 三款向量模型，其中 `v3` 在 CMTEB Retrieval 任务上达 73.23 分，为当前最优；支持全局设置 `Settings.embed_model` 或按需实例化（[使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)）。
- **智能文档解析（DashScopeParse）**：基于“文档智能（Document Mind）”服务，支持 `.pdf`、`.docx`、`.doc` 文件的结构化解析（如标题、段落、表格识别），其他格式（如 `.txt`、`.md`）仅原样上传（[DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)）。
- **云端知识库管理（DashScopeCloudIndex）**：支持在百炼平台托管索引，自动完成文档切分、向量化与混合检索（稠密+稀疏），并提供 `DashScopeCloudRetriever` 进行高效召回（[通过 DashScopeCloudIndex 构建云端知识库](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)）。
- **重排（Rerank）与切分（JsonNodeParser）**：`DashScopeRerank`（模型 `gte-rerank`/`gte-rerank-hybrid`）用于结果精排；`DashScopeJsonNodeParser` 专为 `DashScopeParse` 的 JSON 输出设计，支持按中文标点自定义切分粒度。

> **注意**：文档 1 明确指出“本方案不支持自定义文档切分方式或自定义嵌入模型”，但文档 6 和文档 3 分别提供了 `DashScopeJsonNodeParser` 和可选 `model_name` 的 `DashScopeEmbedding`，表明自定义能力实际存在。此处以具体 SDK 参数为准，即**自定义切分与嵌入模型是支持的，但需显式调用对应组件而非通过 `DashScopeCloudIndex.from_documents()` 默认流程**。

## 关键参数

| 组件 | 关键参数 | 说明 | 默认值 |
|--------|-----------|------|---------|
| `DashScopeLLM` | `model_name` | 指定调用的百炼大模型 | `"qwen-plus"` |
| `DashScopeEmbedding` | `model_name` | 指定 Embedding 模型 | `"text-embedding-v2"` |
| `DashScopeParse` | `result_type`, `category_id` | 解析结果格式（固定为 `DASHSCOPE_DOCMIND`）、目标类目 ID | `ResultType.DASHSCOPE_DOCMIND`, `"default"` |
| `DashScopeCloudRetriever` | `dense_similarity_top_k`, `enable_reranking`, `rerank_top_n` | 向量召回数量、是否启用重排、重排后返回数量 | `100`, `True`, `5` |
| `DashScopeRerank` | `model`, `top_n` | 重排模型、返回 Top-K 结果 | `"gte-rerank"`, `3` |
| `DashScopeJsonNodeParser` | `chunk_size`, `separator` | 文本块大小、切分符正则表达式 | `500`, `" \|,\|，\|。\|？\|！\|\n\|\?\|\!"` |

## 使用方式

### LlamaIndex 集成
1. **安装依赖**：根据所需组件安装对应包，例如：
   ```bash
   pip install llama-index-llms-dashscope  # 大模型
   pip install llama-index-embeddings-dashscope  # Embedding
   pip install llama-index-readers-dashscope  # DashScopeParse
   pip install llama-index-indices-managed-dashscope  # CloudIndex
   ```
2. **认证配置**：通过环境变量设置 `DASHSCOPE_API_KEY`（必需）和 `DASHSCOPE_WORKSPACE_ID`（子业务空间时必需）。
3. **代码示例**：
   - 使用 `DashScopeCloudIndex` 构建云端知识库（见 [文档 8](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)）；
   - 使用 `DashScopeEmbedding` + `VectorStoreIndex` 构建本地向量索引（见 [文档 3](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)）；
   - 将 `DashScopeRerank` 作为 `node_postprocessors` 注入 `query_engine`（见 [文档 1](../../raw/application-api-reference/frameworks/llamaindex.md)）。

### Spring AI Alibaba 集成
1. **添加依赖**：在 `pom.xml` 中引入 `spring-ai-alibaba-starter-dashscope`（见 [文档 11](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)）。
2. **配置参数**：在 `application.yml` 中设置 `spring.ai.dashscope.api-key` 和 `spring.ai.dashscope.agent.app-id`（调用应用时）或 `spring.ai.dashscope.workspace-id`（跨业务空间检索时）。
3. **调用方式**：
   - 调用大模型应用：注入 `DashScopeAgent`，传入 `appId` 和用户消息（见 [文档 11](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)）；
   - 检索知识库：使用 `DashScopeDocumentRetriever` 并配置 `indexName` 和 `searchFilters`（见 [文档 10](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)）。

## 限制和注意事项

- **文件限制**：`DashScopeParse` 仅支持 `.pdf`、`.docx`、`.doc` 的智能解析，单文件 ≤100MB 且 ≤1000 页；其他格式（如 `.txt`）仅上传不解析（[DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)）。
- **业务空间强制要求**：`DashScopeCloudIndex` 和 `DashScopeCloudRetriever` 必须配置 `DASHSCOPE_WORKSPACE_ID` 环境变量，否则初始化失败（[文档 8](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)）。
- **模型兼容性**：OpenAI 兼容模式仅支持百炼的**文本生成类模型**（如 `qwen-*`），不支持 Embedding 或 Rerank 模型（[使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)）。
- **Spring Boot 版本约束**：Spring AI Alibaba 要求 JDK 17+ 和 Spring Boot 3.x（[文档 9](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md) 和 [文档 10](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)）。
- **RAG API 地址不可混用**：Spring AI Alibaba SDK 的 `/api/v1/indices/pipeline/{pipeline_id}/retrieve` 与直调 RAG API 的 `/api/v1/indices/rag/index/retrieve` 是两个独立入口，**不能将后者 URL 配置为 SDK 的 `baseUrl`**（[文档 10](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)）。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)
- [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)
- [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)
- [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)
- [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)
- [DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)
- [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)
- [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)


