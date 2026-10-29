# frameworks

百炼平台提供多套主流 AI 开发框架的官方集成支持，重点覆盖 LlamaIndex 和 Spring AI Alibaba 两大生态。开发者可通过标准化 SDK 和适配器，将百炼的大模型服务、知识库检索、文档解析与重排等能力无缝嵌入现有应用架构，无需从零实现底层基础设施。

## 支持的模型与功能

百炼在框架集成中提供以下核心能力：

- **大模型调用**：支持全部百炼文本生成模型（如 `qwen-max`、`qwen-plus`），既可通过 `DashScope` 原生封装调用，也兼容 OpenAI-like 接口（需配置 `api_base="https://dashscope.aliyuncs.com/compatible-mode/v1"`）[使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)。
- **Embedding 模型**：提供 `text-embedding-v1`/`v2`/`v3` 三款向量模型，其中 `v3` 在 CMTEB Retrieval 任务上达 73.23 分，为当前最优 [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)。
- **文档智能解析**：`DashScopeParse` 基于“文档智能（Document Mind）”服务，支持 PDF/DOCX/DOC 格式智能化解析（含版面分析、表格识别），其他格式仅原样上传 [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)。
- **云端知识库索引与检索**：`DashScopeCloudIndex` 封装百炼云端知识库全生命周期管理（上传、切分、索引、检索），默认启用智能切分与官方向量模型，不支持自定义切分逻辑或嵌入模型 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。
- **重排（Rerank）与后处理**：`DashScopeRerank` 提供 `gte-rerank` 系列模型，支持对初始检索结果进行语义重排序；`DashScopeJsonNodeParser` 可对 `DashScopeParse` 输出的 JSON 结构化结果进行高质量文本切分。

> **注意**：文档 1 明确声明“不支持自定义文档切分方式或自定义嵌入模型”，但文档 7 的示例代码中 `DashScopeCloudIndex.from_documents()` 调用未显式指定嵌入模型，且文档 3 中 `DashScopeEmbedding` 明确支持传入 `model_name` 参数。该矛盾表明：**云端知识库（`DashScopeCloudIndex`）强制使用百炼托管的嵌入模型，而本地向量索引（`VectorStoreIndex`）才支持自定义 `DashScopeEmbedding` 实例**。开发者应依据部署模式（云端 vs 本地）选择对应组件。

## 关键参数

| 组件 | 关键参数 | 说明 | 默认值 |
|--------|----------|------|--------|
| `DashScope` (LLM) | `model_name` | 模型名称，如 `"qwen-max"` | — |
| `DashScopeEmbedding` | `model_name` | 向量模型名称，如 `"text-embedding-v3"` | `"text-embedding-v2"` |
| `DashScopeCloudIndex` | `name` | 云端知识库名称（全局唯一） | — |
| `DashScopeCloudRetriever` | `dense_similarity_top_k`, `sparse_similarity_top_k` | 向量/文本召回数量 | `100` |
| | `enable_reranking`, `rerank_model_name` | 是否启用重排及模型名 | `True`, `"gte-rerank-hybrid"` |
| `DashScopeRerank` | `top_n` | 重排后返回的 Top 文档数 | `3` |
| `DashScopeJsonNodeParser` | `chunk_size`, `overlap_size`, `separator` | 切分粒度与分隔符 | `500`, `100`, `" \|,\|，\|。\|？\|！\|\n\|\?\|\!"` |

## 使用方式

### LlamaIndex 集成
1. **安装依赖**：根据组件选择安装包，例如：
   ```bash
   pip install llama-index-llms-dashscope          # LLM
   pip install llama-index-embeddings-dashscope   # Embedding
   pip install llama-index-readers-dashscope      # DashScopeParse
   pip install llama-index-indices-managed-dashscope  # DashScopeCloudIndex
   ```
2. **配置认证**：设置环境变量 `DASHSCOPE_API_KEY`；若使用子业务空间，还需设置 `DASHSCOPE_WORKSPACE_ID`。
3. **初始化组件**：
   - 本地向量索引：`VectorStoreIndex.from_documents(..., embed_model=DashScopeEmbedding(model_name="text-embedding-v3"))`
   - 云端知识库：`index = DashScopeCloudIndex("my_index")`，再调用 `index.as_retriever()` 获取检索器。
4. **构建 RAG 流程**：组合 `DashScopeParse`（解析）→ `DashScopeJsonNodeParser`（切分）→ `DashScopeCloudIndex`（索引）→ `DashScopeRerank`（重排）→ `DashScope`（生成）。

### Spring AI Alibaba 集成
1. **添加 Maven 依赖**：引入 `spring-ai-alibaba-starter-dashscope`（版本 `1.0.0.2` 或更高）。
2. **配置参数**：在 `application.yml` 中设置 `spring.ai.dashscope.api-key` 和 `spring.ai.dashscope.agent.app-id`（调用应用时）或 `spring.ai.dashscope.workspace-id`（操作知识库时）。
3. **调用方式**：
   - **大模型应用**：注入 `DashScopeAgent`，通过 `agent.call(new Prompt(...))` 调用智能体或工作流应用。
   - **知识库检索**：使用 `DashScopeDocumentRetriever` 配置 `indexName` 和 `searchFilters`，并集成至 `DocumentRetrievalAdvisor`。

## 限制和注意事项

- **文件解析限制**：`DashScopeParse` 仅对 PDF/DOC/DOCX 进行智能化解析；其他格式（TXT/MD/PPT/XLS 等）仅原样上传，不提取结构化内容 [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)。
- **云端知识库约束**：`DashScopeCloudIndex` 强制使用百炼托管的文档切分与向量模型，不开放自定义选项；单文件上限 100MB 或 1000 页，单次上传最多 200 个文件。
- **业务空间依赖**：所有云端操作（`DashScopeCloudIndex`、`DashScopeCloudRetriever`、Spring AI Alibaba 的知识库检索）均要求显式配置 `DASHSCOPE_WORKSPACE_ID` 环境变量，IDE 中需手动注入，否则初始化失败。
- **模型兼容性**：OpenAI-like 封装仅支持百炼的**文本生成类模型**（如 `qwen-plus`），不支持 `text-embedding-*` 等非生成类模型；后者必须使用 `DashScopeEmbedding` 原生封装。
- **Spring AI Alibaba 版本要求**：知识库嵌套 `searchFilters` 功能已在 `1.1.2.3` 版本验证，低版本可能不支持 `_operator: OR` 语法。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)
- [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)
- [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)
- [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)
- [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)
- [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)
- [DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)
- [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)


