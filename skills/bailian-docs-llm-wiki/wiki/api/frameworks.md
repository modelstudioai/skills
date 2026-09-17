# frameworks

百炼平台提供多框架集成能力，支持主流 AI 开发框架（如 LlamaIndex、Spring AI Alibaba）快速对接大模型服务、Embedding 服务、文档解析、云端知识库检索与重排序等能力。开发者可基于业务场景选择原生 SDK 或框架封装层，实现 RAG、Agent、知识库问答等应用的高效构建。

## 支持的模型/功能

百炼在框架集成中覆盖以下核心能力：

- **大模型调用**：支持 `qwen-plus`、`qwen-max` 等文本生成模型，可通过 OpenAI-like 兼容接口或原生 DashScope 接口调用；完整模型列表见 [选择模型](raw/model-user-guide/get-started-with-models/models.md)。  
- **Embedding 模型**：提供 `text-embedding-v1`/`v2`/`v3` 三款向量模型，其中 `text-embedding-v3` 在 CMTEB Retrieval 任务上达 73.23 分，为当前最优 [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)。  
- **文档智能解析（DashScopeParse）**：基于“文档智能（Document Mind）”服务，支持 PDF/DOC/DOCX 的结构化解析（其他格式仅原样上传），单文件 ≤100MB 且 ≤1000 页 [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)。  
- **云端知识库管理（DashScopeCloudIndex）**：支持在百炼云端自动完成文档上传、智能切分、索引构建与检索，无需本地向量存储 [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)。  
- **重排序（Rerank）**：提供 `gte-rerank` 和 `gte-rerank-hybrid` 模型，用于对初检结果进行语义精排，提升检索相关性 [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)。

> **注意**：文档 3 明确指出“本方案将知识库部署在云端，使用默认的智能文档切分与官方向量模型，**不支持自定义文档切分方式或自定义嵌入模型**”，而文档 5 的 `DashScopeJsonNodeParser` 提供了基于通义实验室模型的切分能力——二者定位不同：前者为全托管云端服务（不可定制），后者为可本地集成的切分组件，开发者需按需选用。

## 关键参数

| 组件 | 关键参数 | 说明 | 默认值 |
|--------|-----------|------|---------|
| `DashScope` (LLM) | `model_name` | 指定调用的大模型名称，如 `"qwen-max"` | — |
| `DashScopeEmbedding` | `model_name` | 指定 Embedding 模型，如 `"text-embedding-v2"` | — |
| `DashScopeParse` | `category_id`, `workspace` | 类目 ID（影响解析策略）、业务空间 ID | `"default"`, `None` |
| `DashScopeJsonNodeParser` | `chunk_size`, `separator`, `language` | 切块大小、分隔符正则、语言（`"cn"`/`"en"`） | `500`, `" \|,\|，\|。\|？\|！\|\n\|\?\|!"`, `"cn"` |
| `DashScopeCloudRetriever` | `dense_similarity_top_k`, `enable_reranking`, `rerank_model_name` | 向量召回数、是否启用重排、重排模型名 | `100`, `True`, `"gte-rerank-hybrid"` |
| `DashScopeRerank` | `model`, `top_n` | 重排模型、返回 Top-N 结果数 | `"gte-rerank"`, `3` |

## 使用方式

### LlamaIndex 集成
1. **安装依赖**：按需安装对应模块，例如：
   ```bash
   pip install llama-index-core llama-index-llms-dashscope  # LLM
   pip install llama-index-embeddings-dashscope              # Embedding
   pip install llama-index-readers-dashscope                 # DashScopeParse
   pip install llama-index-indices-managed-dashscope         # CloudIndex
   ```
2. **配置认证**：设置环境变量 `DASHSCOPE_API_KEY`（必选），`DASHSCOPE_WORKSPACE_ID`（子空间时必选）。
3. **初始化组件**：
   - LLM：`DashScope(model_name="qwen-plus")`
   - Embedding：`DashScopeEmbedding(model_name="text-embedding-v3")`
   - 解析+索引：`DashScopeParse()` → `DashScopeCloudIndex.from_documents()`
   - 检索：`index.as_retriever()` 或直接 `DashScopeCloudRetriever("my_index")`

### Spring AI Alibaba 集成
1. **添加 Maven 依赖**：引入 `spring-ai-alibaba-starter-dashscope`（版本 `1.0.0.2`）。
2. **配置参数**：在 `application.yml` 中设置 `spring.ai.dashscope.api-key` 和 `spring.ai.dashscope.agent.app-id`（调用应用时）或 `spring.ai.dashscope.workspace-id`（跨空间时）。
3. **调用方式**：
   - 调用大模型应用：注入 `DashScopeAgent`，传入 `Prompt` 和 `DashScopeAgentOptions.withAppId()`。
   - 检索知识库：使用 `DashScopeDocumentRetriever` 构建 `DocumentRetriever`，结合 `ChatClient` 与 `DocumentRetrievalAdvisor` 实现 RAG 流程。

## 限制和注意事项

- **文件解析限制**：`DashScopeParse` 仅对 PDF/DOC/DOCX 进行智能化解析；TXT/MD/PPT 等格式仅原样上传，不提取结构信息 [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)。  
- **环境兼容性**：所有 LlamaIndex 相关包要求 Python 版本 `>=3.9, <=3.12`；Spring AI Alibaba 要求 JDK 17+ 和 Spring Boot 3.x。  
- **API Key 配置**：必须通过环境变量（如 `DASHSCOPE_API_KEY`）或显式传参设置密钥，硬编码存在安全风险；Spring AI Alibaba 文档 10 中使用 `AI_DASHSCOPE_API_KEY`，而文档 9 使用 `DASHSCOPE_API_KEY`——**实际应以百炼控制台生成的密钥为准，推荐统一使用 `DASHSCOPE_API_KEY`**，避免因环境变量名不一致导致认证失败。  
- **云端知识库依赖**：`DashScopeCloudIndex` 和 `DashScopeCloudRetriever` 必须配置 `DASHSCOPE_WORKSPACE_ID`，否则初始化失败（文档 7 明确抛出 `ValueError`）。  
- **模型能力边界**：OpenAI-like 方式仅支持百炼的**文本生成类模型**，不支持 Embedding、Rerank 或解析类服务 [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)。

## 来源文档

- [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)
- [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)
- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)
- [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)
- [DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)
- [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)
- [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)
- [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)


