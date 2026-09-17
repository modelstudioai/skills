# frameworks

百炼平台提供对主流 AI 开发框架的原生集成支持，重点覆盖 LlamaIndex 和 Spring AI Alibaba 两大生态，帮助开发者快速构建 RAG、智能体、工作流等生产级应用。所有集成均通过官方 SDK 封装，统一使用 `DASHSCOPE_API_KEY` 认证，并深度对接百炼云端能力（如文档智能解析、向量索引、重排模型、知识库管理）。开发者可按需选择本地处理或云端托管模式。

## 支持的模型与功能

- **大语言模型（LLM）**：支持全部百炼文本生成模型（如 `qwen-max`、`qwen-plus`），可通过 `DashScope` 或 OpenAI 兼容模式（`OpenAILike`）调用 [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)。
- **Embedding 模型**：支持 `text-embedding-v1`/`v2`/`v3`，其中 `v3` 在 CMTEB Retrieval 任务上达 73.23 分，为当前最优 [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)。
- **重排模型（Rerank）**：提供 `gte-rerank` 和 `gte-rerank-hybrid`，支持在检索后对候选结果进行语义精排 [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)。
- **文档解析与切分**：`DashScopeParse` 调用文档智能（DocMind）服务，支持 PDF/DOCX/DOC；`DashScopeJsonNodeParser` 基于 JSON 结构化输出进行智能切分，二者需配合使用 [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md) 和 [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)。
- **云端知识库服务**：`DashScopeCloudIndex` 和 `DashScopeCloudRetriever` 封装百炼云端知识库全生命周期管理（上传、解析、索引、检索），默认启用智能切分与官方向量模型，不支持自定义切分逻辑或嵌入模型 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。

> **注意**：文档 1 明确声明“不支持自定义文档切分方式或自定义嵌入模型”，但文档 7 的示例代码中 `DashScopeCloudIndex.from_documents()` 接口未体现该限制，实际行为以文档 1 为准——云端知识库能力由百炼平台统一管控，本地自定义能力仅适用于 `VectorStoreIndex` 等本地索引路径。

## 关键参数

| 组件 | 参数名 | 类型 | 默认值 | 说明 |
|--------|---------|------|---------|------|
| `DashScopeLLM` | `model_name` | string | — | 必填，如 `"qwen-max"`；完整列表见 [选择模型](raw/model-user-guide/get-started-with-models/models.md) |
| `DashScopeEmbedding` | `model_name` | string | `"text-embedding-v2"` | 可选，推荐 `v3` 获取最佳检索效果 |
| `DashScopeRerank` | `top_n`, `model` | int, string | `5`, `"gte-rerank"` | `top_n` 控制返回结果数；`model` 支持 `gte-rerank`/`gte-rerank-hybrid` |
| `DashScopeCloudRetriever` | `dense_similarity_top_k`, `enable_reranking`, `rerank_top_n` | int, bool, int | `100`, `True`, `5` | 向量召回数、是否启用重排、重排后返回数；`rerank_min_score` 可过滤低分节点 |
| `DashScopeJsonNodeParser` | `chunk_size`, `separator` | int, string | `500`, `" \|,\|，\|。\|？\|！\|\n\|\?\|!"` | 中文场景建议保留默认分隔符，避免破坏语义单元 |

## 使用方式

1. **安装依赖**（以 LlamaIndex 为例）：
   ```bash
   # 基础核心
   pip install llama-index-core
   # 按需安装组件（不可混用同功能多包）
   pip install llama-index-llms-dashscope          # LLM
   pip install llama-index-embeddings-dashscope    # Embedding
   pip install llama-index-postprocessor-dashscope-rerank  # Rerank
   pip install llama-index-readers-dashscope       # DashScopeParse
   pip install llama-index-node-parser-dashscope   # JsonNodeParser
   pip install llama-index-indices-managed-dashscope  # CloudIndex/CloudRetriever
   ```

2. **环境配置**（必需）：
   ```bash
   export DASHSCOPE_API_KEY=your_api_key_here
   export DASHSCOPE_WORKSPACE_ID=your_workspace_id  # 云端操作必需
   ```

3. **典型流程**：
   - **本地 RAG**：`SimpleDirectoryReader` → `VectorStoreIndex(from_documents(..., embed_model=DashScopeEmbedding))` → `as_query_engine()`
   - **云端 RAG**：`DashScopeParse` → `DashScopeCloudIndex.from_documents()` → `as_query_engine()`（自动启用重排与过滤）[通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)
   - **Spring Boot 集成**：添加 `spring-ai-alibaba-starter-dashscope` 依赖，配置 `application.yml` 中 `spring.ai.dashscope.*` 属性，注入 `DashScopeAgent` 或 `DashScopeDocumentRetriever` [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)

## 限制和注意事项

- **文件限制**：`DashScopeParse` 仅对 PDF/DOC/DOCX 进行智能解析（提取表格、公式、版式），其他格式（TXT/MD/PPT等）仅原样上传；单文件 ≤100MB 且 ≤1000 页 [DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)。
- **业务空间强依赖**：所有云端操作（`DashScopeCloudIndex`、`DashScopeCloudRetriever`、`Spring AI Alibaba` 知识库检索）必须配置 `DASHSCOPE_WORKSPACE_ID`，否则初始化失败 [DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)。
- **模型兼容性**：`OpenAILike` 方式仅支持百炼的文本生成模型（不支持 embedding/rerank），且需显式设置 `is_chat_model=True`；`DashScope` 封装支持全部模型类型 [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)。
- **Spring AI Alibaba 差异**：其知识库检索模块（`DashScopeDocumentRetriever`）默认使用 `qwen-max` 生成答案，而 LlamaIndex 的 `DashScopeCloudIndex.as_query_engine()` 默认使用 `qwen-max` 但允许通过 `Settings.llm` 全局覆盖 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)
- [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)
- [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)
- [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)
- [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)
- [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)
- [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)
- [DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)


