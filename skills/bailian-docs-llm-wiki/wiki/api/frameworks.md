# frameworks

百炼平台提供对主流 AI 开发框架的原生集成支持，重点覆盖 LlamaIndex 和 Spring AI Alibaba 两大生态，帮助开发者快速构建 RAG、智能体、工作流等生产级应用。所有集成均基于百炼统一的 API 认证体系（`DASHSCOPE_API_KEY`）和业务空间隔离机制，支持云端知识库管理、模型调用、文档解析与重排等核心能力。

## 支持的模型/功能

- **LlamaIndex 集成**：完整支持 `DashScopeLLM`（大模型）、`DashScopeEmbedding`（向量模型）、`DashScopeParse`（文档解析）、`DashScopeJsonNodeParser`（智能切分）、`DashScopeRerank`（语义重排）及 `DashScopeCloudIndex`（云端知识库索引）等组件。  
  - 大模型：支持 `qwen-max`、`qwen-plus`、`qwen-turbo` 等全系列文本生成模型，详见 [选择模型](raw/model-user-guide/get-started-with-models/models.md)。  
  - Embedding 模型：支持 `text-embedding-v1`/`v2`/`v3`，其中 `v3` 在 CMTEB Retrieval 任务上达 73.23 分，为当前最优 [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)。  
  - 重排模型：默认 `gte-rerank`，也支持 `gte-rerank-hybrid`（需通过 `DashScopeCloudRetriever` 启用）[DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)。  

- **Spring AI Alibaba 集成**：支持两类核心场景：  
  - 调用已部署的百炼大模型应用（仅限 Agent 1.0 和工作流应用）[使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)；  
  - 检索百炼云端知识库（RAG），自动注入上下文并调用 `qwen-max` 生成回答 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。  

> **注意**：文档 1 明确指出“云端知识库不支持自定义文档切分方式或自定义嵌入模型”，而文档 4 和 6 中 `DashScopeEmbedding` 与 `DashScopeJsonNodeParser` 均允许用户在本地流程中显式指定模型和切分策略。二者适用场景不同：前者为全托管云端索引（`DashScopeCloudIndex`），后者为自主可控的本地索引构建流程，无矛盾。

## 关键参数

| 组件 | 参数名 | 类型 | 默认值 | 说明 |
|--------|---------|------|---------|------|
| `DashScopeLLM` | `model_name` | string | — | 必填，如 `"qwen-plus"`；完整列表见 [选择模型](raw/model-user-guide/get-started-with-models/models.md) |
| `DashScopeEmbedding` | `model_name` | string | `"text-embedding-v2"` | 推荐使用 `v3` 提升检索质量 |
| `DashScopeRerank` | `model`, `top_n` | string, int | `"gte-rerank"`, `3` | `top_n` 控制返回结果数，超过候选数时返回全部 |
| `DashScopeCloudRetriever` | `dense_similarity_top_k`, `enable_reranking`, `rerank_top_n` | int, bool, int | `100`, `True`, `5` | `rerank_top_n` 仅在 `enable_reranking=True` 时生效 |
| `DashScopeParse` | `category_id`, `workspace` | string, string | `"default"`, `None` | `category_id` 需从控制台「应用数据 > 文件」获取，未设置则走默认类目 |

## 使用方式

1. **环境准备**：  
   - 获取并配置 `DASHSCOPE_API_KEY`（必需），部分功能还需 `DASHSCOPE_WORKSPACE_ID`（子空间场景）；  
   - 安装对应依赖，例如 LlamaIndex 组件需 `pip install llama-index-llms-dashscope`，Spring AI Alibaba 需 `spring-ai-alibaba-starter-dashscope`（Maven）。

2. **典型流程（LlamaIndex）**：  
   - 解析：用 `DashScopeParse` 上传并解析 PDF/DOCX/TXT（≤100MB/1000页）；  
   - 切分：用 `DashScopeJsonNodeParser` 对解析结果按中文标点智能切片；  
   - 向量化：用 `DashScopeEmbedding` 生成向量，存入 `VectorStoreIndex` 或上传至云端 `DashScopeCloudIndex`；  
   - 检索：通过 `as_query_engine()` 或 `as_retriever()` 构建引擎，集成 `SimilarityPostprocessor` 与 `DashScopeRerank` 后处理。

3. **典型流程（Spring AI Alibaba）**：  
   - 配置 `application.yml` 中 `spring.ai.dashscope.agent.app-id` 或 `spring.ai.dashscope.api-key`；  
   - 使用 `DashScopeAgent` 调用智能体/工作流应用，或 `DashScopeDocumentRetriever` 检索知识库；  
   - 流式响应通过 `Flux<ChatResponse>` 实现，非流式直接获取 `AssistantMessage.getText()`。

## 限制和注意事项

- **文件限制**：`DashScopeParse` 仅对 PDF/DOC/DOCX 进行智能解析，其余格式（如 TXT、MD）仅原样上传，不提取结构化内容 [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)。  
- **云端知识库约束**：`DashScopeCloudIndex` 构建的云端知识库强制使用百炼默认切分与向量模型，不开放自定义入口；若需完全可控流程，请使用本地 `VectorStoreIndex + DashScopeEmbedding` 方案 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。  
- **API 兼容性**：`OpenAILike` 封装仅支持百炼的文本生成模型（如 `qwen-plus`），**不支持 embedding 或 rerank 模型**，调用前请确认模型类型 [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)。  
- **业务空间要求**：所有云端操作（`DashScopeCloudIndex`、`DashScopeCloudRetriever`、Spring AI Alibaba 的知识库检索）均强依赖 `DASHSCOPE_WORKSPACE_ID`，未配置将报错，且 IDE 环境需手动注入该变量。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)
- [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)
- [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)
- [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)
- [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)
- [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)
- [DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)
- [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)


