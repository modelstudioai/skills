# frameworks

百炼平台提供对主流 AI 开发框架的原生集成支持，重点覆盖 LlamaIndex 和 Spring AI Alibaba 两大生态。开发者可基于这些框架快速构建 RAG 应用、调用大模型服务、管理云端知识库及检索增强流程，无需从零实现底层能力。所有集成均通过官方 SDK 封装，统一使用 DASHSCOPE_API_KEY 进行鉴权。

## 支持的模型与功能

- **大模型（LLM）**：支持全部百炼文本生成模型（如 `qwen-max`、`qwen-plus`），可通过 `DashScope` 或 OpenAI-like 封装调用；[使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md) 提供两种方式的完整示例。
- **Embedding 模型**：支持 `text-embedding-v1`/`v2`/`v3`，其中 `v3` 在 CMTEB Retrieval 任务上达 73.23 分，为当前最优；[使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md) 明确列出各模型评估指标。
- **Rerank 模型**：默认使用 `gte-rerank`，也支持 `gte-rerank-hybrid`；[DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md) 文档说明其参数与返回格式。
- **文档解析与切分**：`DashScopeParse` 调用文档智能（DocMind）服务解析 PDF/DOCX/DOC；`DashScopeJsonNodeParser` 基于语义进行智能切分；二者需配合使用，[DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md) 明确限定仅 PDF/DOCX/DOC 支持智能化解析。
- **云端知识库服务**：`DashScopeCloudIndex` 实现知识库的创建、更新与检索；`DashScopeCloudRetriever` 提供向量+全文混合检索及重排能力。

> **注意**：[通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) 中声明“不支持自定义文档切分方式或自定义嵌入模型”，但 [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md) 和 [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md) 均明确支持自定义切分逻辑与 Embedding 模型选择。该矛盾源于前者特指“云端知识库默认流程”，后者面向本地索引构建——实际开发中，自定义能力完全可用。

## 关键参数

| 组件 | 参数名 | 类型 | 默认值 | 说明 |
|--------|---------|------|---------|------|
| `DashScopeLLM` | `model_name` | string | — | 必填，如 `"qwen-plus"`；详见[选择模型](raw/model-user-guide/get-started-with-models/models.md) |
| `DashScopeEmbedding` | `model_name` | string | `"text-embedding-v2"` | 可选，推荐 `v3` 获取最佳检索效果 |
| `DashScopeRerank` | `model`, `top_n` | string, int | `"gte-rerank"`, `3` | `top_n` 控制返回结果数，超限则返回全部候选 |
| `DashScopeCloudRetriever` | `dense_similarity_top_k`, `sparse_similarity_top_k`, `enable_reranking` | int, int, bool | `100`, `100`, `True` | 混合检索召回数及是否启用重排；`rerank_min_score` 仅在 `enable_reranking=True` 时生效 |
| `DashScopeJsonNodeParser` | `chunk_size`, `overlap_size`, `separator` | int, int, string | `500`, `100`, `" \|,\|，\|。\|？\|！\|\n\|\?\|\!"` | 中文分隔符已预置，`language="cn"` 为默认且最优配置 |

## 使用方式

### LlamaIndex 集成
1. **安装依赖**：根据组件选择安装包，例如：
   ```bash
   pip install llama-index-llms-dashscope  # LLM
   pip install llama-index-embeddings-dashscope  # Embedding
   pip install llama-index-postprocessor-dashscope-rerank  # Rerank
   pip install llama-index-indices-managed-dashscope  # 云端知识库
   ```
2. **全局设置（可选）**：统一配置默认模型
   ```python
   from llama_index.core import Settings
   from llama_index.llms.dashscope import DashScope
   from llama_index.embeddings.dashscope import DashScopeEmbedding
   Settings.llm = DashScope(model_name="qwen-plus")
   Settings.embed_model = DashScopeEmbedding(model_name="text-embedding-v3")
   ```
3. **构建云端 RAG 流程**（三步）：
   - 用 `DashScopeParse` 解析本地文件 → `Documents`
   - 用 `DashScopeCloudIndex.from_documents()` 上传并建索引
   - 用 `index.as_query_engine()` 或 `index.as_retriever()` 构建查询入口，注入 `DashScopeRerank` 等后处理器。

### Spring AI Alibaba 集成
1. **添加 Maven 依赖**：引入 `spring-ai-alibaba-starter-dashscope`
2. **配置环境变量**：`DASHSCOPE_API_KEY`（必需）、`APP_ID`（调用应用时）、`WORKSPACE_ID`（子空间时）
3. **调用方式**：
   - **大模型应用**：注入 `DashScopeAgent`，通过 `agent.call(new Prompt(...))` 触发
   - **知识库检索**：配置 `DashScopeDocumentRetriever` 并绑定至 `DocumentRetrievalAdvisor`，由 `ChatClient` 自动注入上下文

## 限制和注意事项

- **文件解析限制**：`DashScopeParse` 仅对 `.pdf`、`.doc`、`.docx` 执行智能化解析（含版面分析、表格识别等），其他格式（如 `.txt`、`.md`）仅原样上传，不解析结构；单文件 ≤100MB 或 ≤1000页；一次最多上传 200 个文件。
- **业务空间强依赖**：所有云端操作（`DashScopeCloudIndex`、`DashScopeCloudRetriever`、Spring AI Alibaba 的知识库检索）均需显式配置 `DASHSCOPE_WORKSPACE_ID` 环境变量，IDE 中需手动注入，否则报错。
- **API Key 安全**：严禁硬编码 `DASHSCOPE_API_KEY`；必须通过环境变量（如 `os.getenv("DASHSCOPE_API_KEY")`）或配置中心注入。
- **模型兼容性**：OpenAI-like 封装仅支持百炼的文本生成类模型（非多模态、非 Function Calling），具体列表见[OpenAI 兼容模式支持的模型列表](https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope#eadfc13038jd5)。
- **Spring Boot 版本要求**：Spring AI Alibaba 要求 Spring Boot 3.x + JDK 17+；低版本不兼容。

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


