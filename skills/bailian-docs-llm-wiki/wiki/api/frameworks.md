# frameworks

百炼平台提供对主流 AI 开发框架的原生集成支持，重点覆盖 LlamaIndex 和 Spring AI Alibaba 两大生态，帮助开发者快速构建 RAG、智能体、工作流等生产级应用。所有集成均通过官方 SDK 封装，统一使用 `DASHSCOPE_API_KEY` 认证，并深度对接百炼云端知识库、大模型服务与文档智能能力。

## 支持的模型/功能

- **大模型调用**：支持全部百炼文本生成模型（如 `qwen-max`、`qwen-plus`），可通过 `DashScope` 或 OpenAI-like 封装调用；[使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md) 提供两种方式的完整示例。
- **Embedding 模型**：支持 `text-embedding-v1`/`v2`/`v3`，其中 `v3` 在 CMTEB Retrieval 任务上达 73.23 分；[使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md) 明确列出各版本评估指标。
- **Rerank 模型**：默认使用 `gte-rerank`，也支持 `gte-rerank-hybrid`；[DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md) 文档说明其参数与返回格式。
- **文档解析与切分**：`DashScopeParse` 支持 PDF/DOCX/DOC 智能解析（基于 Document Mind），`DashScopeJsonNodeParser` 基于解析结果进行语义切分；二者需配合使用，详见 [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md) 和 [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)。
- **云端知识库管理**：`DashScopeCloudIndex` + `DashScopeCloudRetriever` 实现全托管式索引构建与检索，支持向量+文本混合检索、重排、分数过滤；[通过 DashScopeCloudIndex 构建云端知识库](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md) 给出端到端流程。

> **注意**：文档 1 中声明“不支持自定义文档切分方式或自定义嵌入模型”，但文档 3 和文档 6 明确支持通过 `DashScopeEmbedding` 和 `DashScopeJsonNodeParser` 自定义 embedding 模型与切分逻辑。该矛盾源于场景差异——文档 1 描述的是 *0代码云端RAG方案* 的限制，而文档 3/6 面向 *代码集成开发者*，后者完全支持自定义。实际开发中应以文档 3/6 为准。

## 关键参数

| 组件 | 参数 | 类型 | 默认值 | 说明 |
|------|------|------|--------|------|
| `DashScopeLLM` | `model_name` | string | — | 必填，如 `"qwen-max"`；见 [选择模型](raw/model-user-guide/get-started-with-models/models.md) |
| `DashScopeEmbedding` | `model_name` | string | `"text-embedding-v2"` | 可选值：`"text-embedding-v1"`/`"v2"`/`"v3"` |
| `DashScopeRerank` | `top_n`, `model` | int, string | `5`, `"gte-rerank"` | `model` 可选 `"gte-rerank-hybrid"`（文档 7） |
| `DashScopeCloudRetriever` | `dense_similarity_top_k`, `enable_reranking`, `rerank_top_n` | int, bool, int | `100`, `True`, `5` | 控制召回数量与重排行为（文档 7） |
| `DashScopeJsonNodeParser` | `chunk_size`, `separator` | int, string | `500`, `" \|,\|，\|。\|？\|！\|\n\|\?\|!"` | 中文分隔符已预置，可按需调整（文档 6） |

## 使用方式

1. **环境准备**  
   - 设置 `DASHSCOPE_API_KEY`（必填）和 `DASHSCOPE_WORKSPACE_ID`（子空间必填）为环境变量；
   - 安装对应 SDK：LlamaIndex 用户按需安装 `llama-index-llms-dashscope`、`llama-index-embeddings-dashscope` 等（见各文档 `pip install` 命令）；Spring AI Alibaba 用户引入 `spring-ai-alibaba-starter-dashscope`（文档 8/9/10）。

2. **LlamaIndex 集成路径**  
   - **本地索引**：用 `DashScopeEmbedding` + `VectorStoreIndex.from_documents()` 构建本地向量库（文档 3）；  
   - **云端索引**：用 `DashScopeParse` 解析文件 → `DashScopeCloudIndex.from_documents()` 创建云端知识库 → `as_retriever()` 获取 `DashScopeCloudRetriever`（文档 11）；  
   - **RAG 编排**：组合 `DashScopeLLM`、`DashScopeRerank`、`SimilarityPostprocessor` 等构建 query engine（文档 1）。

3. **Spring AI Alibaba 集成路径**  
   - 调用大模型应用：配置 `APP_ID` + `DASHSCOPE_API_KEY`，使用 `DashScopeAgent`（文档 9）；  
   - 检索知识库：配置 `INDEX_NAME` + `AI_DASHSCOPE_API_KEY`，使用 `DashScopeDocumentRetriever`（文档 10）。

## 限制和注意事项

- **文件解析限制**：`DashScopeParse` 仅对 PDF/DOC/DOCX 进行智能解析，其他格式（TXT/MD/PPT等）仅原样上传（文档 11）；单文件 ≤100MB 且 ≤1000 页（文档 5）。
- **业务空间依赖**：所有云端操作（`DashScopeCloudIndex`、`DashScopeCloudRetriever`）均强制要求 `DASHSCOPE_WORKSPACE_ID`，未配置将报错（文档 11）。
- **模型兼容性**：OpenAI-like 封装仅支持百炼的文本生成模型（非多模态），且需显式设置 `is_chat_model=True`（文档 2）。
- **重排模型差异**：`gte-rerank-hybrid`（文档 7）与 `gte-rerank`（文档 4）为不同模型，前者支持混合检索结果重排，后者仅支持纯向量结果；二者不可混用。
- **API Key 环境变量名不一致**：Spring AI Alibaba 示例中推荐使用 `AI_DASHSCOPE_API_KEY`（文档 10），而 LlamaIndex 文档统一使用 `DASHSCOPE_API_KEY`（文档 2/3/4）。建议统一采用 `DASHSCOPE_API_KEY` 以避免混淆。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)
- [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)
- [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)
- [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)
- [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)
- [DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)
- [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)
- [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)


