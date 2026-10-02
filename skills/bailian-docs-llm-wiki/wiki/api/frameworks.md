# frameworks

百炼平台提供对主流 AI 开发框架的原生集成支持，重点覆盖 LlamaIndex 和 Spring AI Alibaba 两大生态，帮助开发者快速构建 RAG、智能体、工作流等生产级应用。所有集成均基于百炼统一的 API Key 认证体系和业务空间（Workspace）隔离机制，支持云端知识库管理、模型调用、嵌入向量化与重排序等核心能力。

## 支持的模型/功能

- **大模型（LLM）**：通过 `DashScope` 或 `OpenAILike` 封装调用百炼全量文本生成模型（如 `qwen-max`、`qwen-plus`），支持同步/流式响应、系统提示词配置及 Agent 工作流集成 [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)。
- **Embedding 模型**：提供 `text-embedding-v1`/`v2`/`v3` 三款官方 Embedding 模型，支持 MTEB/CMTEB 高分检索任务，适用于本地向量索引构建 [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)。
- **Rerank 模型**：集成 `gte-rerank` 及 `gte-rerank-hybrid`，用于对初检结果进行语义重排序，提升 Top-K 相关性 [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)。
- **文档解析与切分**：`DashScopeParse` 调用阿里云“文档智能（DocMind）”服务，支持 PDF/DOCX/DOC 等格式的结构化解析；`DashScopeJsonNodeParser` 基于解析结果进行智能文本切分，适配中文语义边界 [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)。
- **云端知识库服务**：`DashScopeCloudIndex` 和 `DashScopeCloudRetriever` 提供端到端云端知识库构建与检索能力，含自动切分、向量索引、混合检索（稠密+稀疏）、重排与阈值过滤 [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)。
- **Spring 生态集成**：`Spring AI Alibaba` 支持 Java 应用无缝接入百炼大模型应用（Agent 1.0 / 工作流）和知识库 RAG 服务，提供 `DashScopeAgent` 和 `DashScopeDocumentRetriever` 标准接口 [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)。

> **注意**：文档 1 明确指出“本方案将知识库部署在云端，使用默认的智能文档切分与官方向量模型，**不支持自定义文档切分方式或自定义嵌入模型**”，而文档 6 的 `DashScopeJsonNodeParser` 和文档 3 的 `DashScopeEmbedding` 均明确支持本地自定义切分与嵌入模型。该矛盾表明：**云端知识库（DashScopeCloudIndex）强制使用百炼托管的切分与嵌入流程，而本地索引（VectorStoreIndex + DashScopeEmbedding）才支持完全自定义**。开发者需根据部署模式选择对应能力。

## 关键参数

| 组件 | 参数名 | 类型 | 默认值 | 说明 |
|--------|---------|------|---------|------|
| `DashScopeLLM` | `model_name` | string | — | 必填，如 `"qwen-max"`；完整列表见 [选择模型](raw/model-user-guide/get-started-with-models/models.md) |
| `DashScopeEmbedding` | `model_name` | string | `"text-embedding-v2"` | 推荐使用 `v3`（CMTEB Retrieval 73.23 分） |
| `DashScopeRerank` | `top_n`, `model` | int, string | `5`, `"gte-rerank"` | `model` 可选 `"gte-rerank-hybrid"`（需 `enable_reranking=True`） |
| `DashScopeCloudRetriever` | `dense_similarity_top_k`, `sparse_similarity_top_k`, `rerank_top_n`, `rerank_min_score` | int, int, int, float | `100`, `100`, `5`, `0.0` | 控制召回数量与重排后过滤阈值；`rerank_min_score` 仅在 `enable_reranking=True` 时生效 |
| `DashScopeJsonNodeParser` | `chunk_size`, `overlap_size`, `separator` | int, int, string | `500`, `100`, `" \|,\|，\|。\|？\|！\|\n\|\?\|\!"` | 中文场景建议保留默认分隔符集 |

## 使用方式

1. **环境准备**  
   - 获取并配置 `DASHSCOPE_API_KEY`（必需）与 `DASHSCOPE_WORKSPACE_ID`（若使用子业务空间）；
   - 安装对应组件依赖（如 `pip install llama-index-llms-dashscope` 或 `spring-ai-alibaba-starter-dashscope`）。

2. **LlamaIndex 集成示例**  
   ```python
   # 全局设置（可选）
   from llama_index.core import Settings
   from llama_index.llms.dashscope import DashScope
   from llama_index.embeddings.dashscope import DashScopeEmbedding
   Settings.llm = DashScope(model_name="qwen-plus")
   Settings.embed_model = DashScopeEmbedding(model_name="text-embedding-v3")

   # 构建本地向量索引
   from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
   documents = SimpleDirectoryReader("./docs").load_data()
   index = VectorStoreIndex.from_documents(documents)

   # 或构建云端知识库（需 workspace_id）
   from llama_index.indices.managed.dashscope import DashScopeCloudIndex
   index = DashScopeCloudIndex.from_documents(documents, name="my_kb")
   ```

3. **Spring AI Alibaba 集成示例**  
   - `application.yml` 配置：
     ```yaml
     spring:
       ai:
         dashscope:
           api-key: ${DASHSCOPE_API_KEY}
           # workspace-id: ${WORKSPACE_ID} # 可选
     ```
   - Java 中注入 `DashScopeAgent` 或 `DashScopeDocumentRetriever`，通过 `ChatClient` 自动注入 RAG 流程。

## 限制和注意事项

- **文件限制**：`DashScopeParse` 仅对 `.pdf`、`.docx`、`.doc` 进行智能解析；其他格式（如 `.txt`、`.md`）仅原样上传，不触发 DocMind 解析 [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)。
- **规格限制**：单个文档 ≤ 100MB 且 ≤ 1000 页；一次上传最多 200 个文件；`DashScopeParse` 并发数由 `num_workers` 控制，默认为 4。
- **业务空间强依赖**：所有云端操作（`DashScopeCloudIndex`、`DashScopeCloudRetriever`、`Spring AI Alibaba` 知识库检索）均要求显式配置 `DASHSCOPE_WORKSPACE_ID`，否则报错；IDE 用户需手动将变量注入运行环境。
- **模型兼容性**：`OpenAILike` 封装仅支持百炼的 [文本生成类模型](raw/model-api-reference/qwen-api-reference.md)，不支持多模态或语音模型；`DashScope` 封装支持全部文本生成模型及部署模型。
- **重排模型差异**：`DashScopeRerank` 默认 `model="gte-rerank"`，而 `DashScopeCloudRetriever` 默认 `rerank_model_name="gte-rerank-hybrid"`；二者效果不同，不可混用参数名。

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


