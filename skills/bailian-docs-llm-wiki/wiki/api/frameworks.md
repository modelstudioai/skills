# frameworks

百炼平台提供对主流 AI 开发框架的原生集成支持，重点覆盖 LlamaIndex 和 Spring AI Alibaba 两大生态，帮助开发者快速构建 RAG 应用、知识库检索服务及大模型智能体。所有集成均基于百炼统一的 API Key 认证与业务空间（Workspace）隔离机制，支持云端文档解析、向量索引、重排序、[检索增强生成](../concepts/rag.md)等全链路能力。

## 支持的模型/功能

- **LlamaIndex 集成**：完整支持 `DashScopeParse`（文档智能解析）、`DashScopeEmbedding`（文本嵌入）、`DashScopeRerank`（语义重排序）、`DashScopeLLM`（大模型调用）及 `DashScopeCloudIndex`/`DashScopeCloudRetriever`（云端知识库管理与检索）。其中 `DashScopeParse` 支持 PDF/DOCX/DOC 格式智能化解析（非结构化内容提取），而 TXT/MD/PPT 等格式仅原样上传 [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)。
- **Embedding 模型**：当前支持 `text-embedding-v1`、`text-embedding-v2`、`text-embedding-v3` 三款模型，评估指标 MTEB 和 CMTEB 均随版本递增，`v3` 在 Retrieval 任务上表现最优 [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)。
- **Rerank 模型**：默认使用 `gte-rerank`，亦支持 `gte-rerank-hybrid`（见 `DashScopeCloudRetriever` 参数说明），适用于对初步检索结果进行精细化语义排序。
- **大模型调用**：支持两种方式——`DashScope` 原生封装（推荐用于全功能支持）和 `OpenAILike` 兼容模式（适配 OpenAI SDK 习惯）[使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)。
- **Spring AI Alibaba 集成**：提供 `spring-ai-alibaba-starter-dashscope` Starter，支持两类核心场景：调用已部署的百炼大模型应用（Agent 1.0 / 工作流应用）和检索百炼知识库（RAG）[Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)。

> **注意**：文档 6 明确指出“只有 PDF、DOC、DOCX 文件会进行智能化解析，其他类型的文件只原样上传到云端”，但文档 1 的前提条件中仅列出 `.txt`、`.docx`、`.pdf` 为支持格式，且未提及其他格式（如 PPT/XLS）；而文档 6 的说明更全面，应以文档 6 为准。

## 关键参数

| 组件 | 关键参数 | 默认值 | 说明 |
|--------|-----------|---------|------|
| `DashScopeParse` | `result_type`, `category_id`, `workspace` | `ResultType.DASHSCOPE_DOCMIND`, `default`, `None` | `category_id` 决定上传类目，未设置则使用默认类目；`workspace` 必须配置才能操作云端资源 [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md) |
| `DashScopeEmbedding` | `model_name` | — | 必填，取值为 `text-embedding-v1`/`v2`/`v3` |
| `DashScopeRerank` | `model`, `top_n`, `return_documents` | `gte-rerank`, `3`, `False` | `model` 当前仅支持 `gte-rerank`（文档 3），但 `DashScopeCloudRetriever` 支持 `gte-rerank-hybrid`（文档 11），存在模型列表不一致 |
| `DashScopeCloudRetriever` | `dense_similarity_top_k`, `enable_reranking`, `rerank_model_name`, `rerank_top_n` | `100`, `True`, `gte-rerank-hybrid`, `5` | 启用重排后，`rerank_top_n` 控制最终返回节点数；`rerank_min_score` 可过滤低分结果 |
| `DashScopeJsonNodeParser` | `chunk_size`, `overlap_size`, `separator`, `language` | `500`, `100`, `" \|,\|，\|。\|？\|！\|\n\|\?\|!"`, `cn` | 专用于切分 `DashScopeParse` 输出的 JSON 文本，`language=cn` 为中文分词优化 |

> **注意**：`DashScopeRerank` 文档（文档 3）声称仅支持 `gte-rerank`，而 `DashScopeCloudRetriever` 文档（文档 11）明确列出 `gte-rerank-hybrid` 为可选 `rerank_model_name`。该差异表明 `gte-rerank-hybrid` 是 `DashScopeCloudRetriever` 特有高级能力，非独立 `DashScopeRerank` 组件所支持，开发者应根据使用场景选择组件。

## 使用方式

1. **环境准备**：  
   - 获取并配置 `DASHSCOPE_API_KEY`（必需）及 `DASHSCOPE_WORKSPACE_ID`（必需，用于云端操作）；
   - 安装对应 Python 包（如 `llama-index-embeddings-dashscope`、`llama-index-postprocessor-dashscope-rerank`）或 Maven 依赖（如 `spring-ai-alibaba-starter-dashscope`）。

2. **LlamaIndex 典型流程**：  
   - 解析：用 `DashScopeParse` 上传并解析本地 PDF/DOCX 文件；  
   - 切分（可选）：对解析结果用 `DashScopeJsonNodeParser` 进行语义切分；  
   - 嵌入：用 `DashScopeEmbedding` 生成向量，构建本地 `VectorStoreIndex`；  
   - 云端索引：用 `DashScopeCloudIndex.from_documents()` 将文档直接同步至百炼云端并自动建索引；  
   - 检索：用 `DashScopeCloudIndex.as_retriever()` 或 `DashScopeCloudRetriever` 初始化检索器，支持稠密/稀疏混合检索与重排。

3. **Spring AI Alibaba 典型流程**：  
   - 配置 `application.yml` 中 `spring.ai.dashscope.api-key` 和 `app-id`（应用调用）或 `indexName`（知识库检索）；  
   - 使用 `DashScopeAgent` 调用预设大模型应用；  
   - 使用 `DashScopeDocumentRetriever` 结合 `DocumentRetrievalAdvisor` 实现 RAG 流程，支持 `searchFilters` 字段级条件过滤 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。

## 限制和注意事项

- **文件限制**：`DashScopeParse` 仅支持单文件 ≤100MB 且 ≤1000 页；一次上传最多 200 个文件；TXT/MD/PPT/XLS 等格式不解析，仅存储 [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)。
- **云端知识库限制**：文档 1 明确指出“使用默认的智能文档切分与官方向量模型，不支持自定义文档切分方式或自定义嵌入模型”，即 `DashScopeCloudIndex` 为黑盒服务，无法替换底层切分逻辑或 embedding 模型 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。
- **业务空间强制要求**：所有云端操作（`DashScopeCloudIndex`、`DashScopeCloudRetriever`、Spring AI Alibaba 的知识库检索）均需正确配置 `DASHSCOPE_WORKSPACE_ID`，否则初始化失败；Spring AI Alibaba 的 HTTP 直调 RAG API 更是**必须显式传入 `workspace_id`**，即使使用默认空间 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。
- **模型兼容性**：`OpenAILike` 方式虽便捷，但部分百炼特有功能（如流式响应元数据、特定 stop token 控制）可能缺失，生产环境建议优先使用原生 `DashScope` 封装 [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)
- [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)
- [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)
- [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)
- [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)
- [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)
- [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)
- [DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)


