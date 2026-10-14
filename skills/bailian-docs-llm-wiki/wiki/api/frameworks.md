# frameworks

百炼平台提供多套主流 AI 开发框架的深度集成支持，重点覆盖 LlamaIndex 和 Spring AI Alibaba 两大生态，帮助开发者快速构建 RAG 应用、知识库检索服务及大模型智能体。所有集成均基于百炼统一的 API Key 认证与业务空间（Workspace）隔离机制，支持云端向量索引、智能文档解析、重排序及模型调用等核心能力。

## 支持的模型与功能

- **大模型（LLM）**：通过 `DashScope` 或 `OpenAILike` 封装调用百炼全量文本生成模型，如 `qwen-max`、`qwen-plus` 等，详见 [选择模型](raw/model-user-guide/get-started-with-models/models.md)；[使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md) 文档明确区分了两种调用方式的适用场景与依赖差异。
- **Embedding 模型**：支持 `text-embedding-v1`/`v2`/`v3`，其中 `v3` 在 CMTEB Retrieval 任务上达 73.23 分，为当前最优；可通过 `DashScopeEmbedding` 直接嵌入本地文档并构建 `VectorStoreIndex`。
- **重排序（Rerank）模型**：提供 `gte-rerank` 和 `gte-rerank-hybrid`，用于对初检结果进行语义精排；[DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md) 支持 `top_n`、`rerank_min_score` 等关键过滤参数。
- **文档解析与切分**：`DashScopeParse` 调用阿里云“文档智能（Document Mind）”服务，支持 PDF/DOCX/DOC 格式智能解析（非结构化内容提取）；`DashScopeJsonNodeParser` 基于解析结果进行中文敏感的语义切分（支持自定义分隔符与重叠），二者需配合使用。
- **云端知识库服务**：`DashScopeCloudIndex` 实现端到端云端知识库构建（含上传、解析、切分、索引），`DashScopeCloudRetriever` 提供稠密/稀疏混合检索与可选重排能力；该能力与 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) 中描述的方案一致，但后者强调“默认智能切分与官方向量模型”，且明确不支持自定义切分或嵌入模型。

> **注意**：文档 1 明确声明“不支持自定义文档切分方式或自定义嵌入模型”，而文档 6（`DashScopeJsonNodeParser`）和文档 3（`DashScopeEmbedding`）均提供对应自定义能力。此矛盾源于场景划分：文档 1 描述的是 *开箱即用的云端 RAG 方案*（`DashScopeCloudIndex`），而文档 3/6 面向 *本地索引构建流程*。开发者应根据部署模式（云端 vs 本地）选择对应组件。

- **Spring 生态支持**：`Spring AI Alibaba` 提供 `DashScopeDocumentRetriever`（知识库检索）与 `DashScopeAgent`（大模型应用调用）两类核心抽象，完整支持 JDK 17+ 与 Spring Boot 3.x，适用于 Java 企业级 RAG 和 Agent 工程。

## 关键参数

| 组件 | 参数名 | 类型 | 默认值 | 说明 |
|--------|--------|------|--------|------|
| `DashScopeEmbedding` | `model_name` | string | `"text-embedding-v2"` | 必填，指定 Embedding 模型版本 |
| `DashScopeRerank` | `top_n`, `model` | int, string | `5`, `"gte-rerank"` | 控制返回数量与重排模型 |
| `DashScopeCloudRetriever` | `dense_similarity_top_k`, `sparse_similarity_top_k`, `enable_reranking`, `rerank_top_n` | int, bool, int | `100`, `100`, `True`, `5` | 混合检索召回数、是否启用重排及重排后返回数 |
| `DashScopeJsonNodeParser` | `chunk_size`, `overlap_size`, `separator` | int, int, string | `500`, `100`, `" \|,\|，\|。\|？\|！\|\n\|\?\|\!"` | 切分粒度与中文分隔符策略 |

## 使用方式

1. **环境准备**  
   - 获取 API Key 并配置为环境变量 `DASHSCOPE_API_KEY`（部分 Spring 场景使用 `AI_DASHSCOPE_API_KEY`）；  
   - 若使用子业务空间，必须配置 `DASHSCOPE_WORKSPACE_ID`（LlamaIndex）或 `AI_DASHSCOPE_WORKSPACE_ID`（Spring AI Alibaba）；  
   - 安装对应框架包（如 `llama-index-llms-dashscope`, `spring-ai-alibaba-starter-dashscope`）。

2. **LlamaIndex 集成示例**  
   - **调用大模型**：`Settings.llm = DashScope(model_name="qwen-plus")` 或 `OpenAILike(api_base="https://dashscope.aliyuncs.com/compatible-mode/v1")`；  
   - **构建本地向量索引**：`VectorStoreIndex.from_documents(documents, embed_model=DashScopeEmbedding(...))`；  
   - **构建云端知识库**：`DashScopeCloudIndex.from_documents(documents, name="my_index")`；  
   - **检索增强**：组合 `SimilarityPostprocessor` + `DashScopeRerank` 或直接使用 `DashScopeCloudRetriever`。

3. **Spring AI Alibaba 集成示例**  
   - **知识库检索**：注入 `DashScopeDocumentRetriever`，通过 `DocumentRetrievalAdvisor` 自动注入上下文；  
   - **大模型应用调用**：初始化 `DashScopeAgent`，传入 `appId` 调用已部署的智能体或工作流应用；  
   - 配置项集中于 `application.yml`，如 `spring.ai.dashscope.agent.app-id`。

## 限制和注意事项

- **文件解析限制**：`DashScopeParse` 仅对 PDF/DOC/DOCX 进行智能解析（提取逻辑结构），TXT/MD/PPT 等格式仅原样上传；单文件 ≤100MB 且 ≤1000 页；一次最多上传 200 个文件。
- **云端知识库约束**：`DashScopeCloudIndex` 构建的知识库强制使用百炼默认切分策略与向量模型，无法替换（见 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)）；若需完全自定义，应采用本地 `VectorStoreIndex` + `DashScopeEmbedding` 方案。
- **API 兼容性**：`OpenAILike` 封装仅支持百炼的文本生成类模型（如 `qwen-*`），不支持多模态或语音模型；其 `api_base` 必须为 `https://dashscope.aliyuncs.com/compatible-mode/v1`。
- **环境变量命名差异**：LlamaIndex 统一使用 `DASHSCOPE_API_KEY` 和 `DASHSCOPE_WORKSPACE_ID`；Spring AI Alibaba 在知识库场景使用 `AI_DASHSCOPE_API_KEY`/`AI_DASHSCOPE_WORKSPACE_ID`，在大模型应用调用场景使用 `DASHSCOPE_API_KEY`/`WORKSPACE_ID` —— 开发者需按框架文档严格配置，避免因变量名错误导致认证失败。

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
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)


