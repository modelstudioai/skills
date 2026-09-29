# frameworks

百炼平台提供对主流 AI 开发框架的原生集成支持，重点覆盖 LlamaIndex 和 Spring AI Alibaba 两大生态，帮助开发者快速构建 RAG、智能体、工作流等生产级应用。所有集成均基于百炼统一的 API 认证体系（`DASHSCOPE_API_KEY`）和业务空间管理模型，支持云端知识库托管、向量索引、重排序、文档解析等关键能力。

## 支持的模型/功能

- **大模型调用**：通过 `DashScope` 或 `OpenAILike` 封装调用百炼全量文本生成模型（如 `qwen-max`、`qwen-plus`），支持流式/非流式响应；[使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md) 提供两种兼容模式的完整示例。
- **Embedding 模型**：支持 `text-embedding-v1`/`v2`/`v3`，其中 `v3` 在 CMTEB Retrieval 任务上达 73.23 分；可通过 `DashScopeEmbedding` 直接构建本地向量索引。
- **Rerank 模型**：提供 `gte-rerank` 和 `gte-rerank-hybrid`，用于对检索结果进行语义重排序；[DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md) 支持 `top_n` 和 `rerank_min_score` 等精细控制。
- **文档解析与切分**：
  - `DashScopeParse` 调用阿里云“文档智能（Document Mind）”服务，支持 PDF/DOCX/DOC 格式智能化解析（含版面分析、表格识别），其他格式仅原样上传；[DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md) 明确限定单文件 ≤100MB 且 ≤1000 页。
  - `DashScopeJsonNodeParser` 对 `DashScopeParse` 输出的 JSON 结构化结果进行智能切分，支持中文标点与换行符作为分隔符。
- **云端知识库服务**：`DashScopeCloudIndex` 和 `DashScopeCloudRetriever` 实现知识库的创建、增删文档及向量/稀疏混合检索；[通过 DashScopeCloudIndex 构建云端知识库](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md) 支持 `dense_similarity_top_k` 和 `sparse_similarity_top_k` 双通道召回。

> **注意**：[通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) 中声明“不支持自定义文档切分方式或自定义嵌入模型”，但该限制仅适用于其示例中使用的 `DashScopeCloudIndex` 托管模式；若采用 `DashScopeEmbedding` + `VectorStoreIndex` 的本地索引模式，则完全支持自定义切分与 Embedding 模型（见 [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)）。

## 关键参数

| 组件 | 参数名 | 类型 | 默认值 | 说明 |
|--------|--------|------|--------|------|
| `DashScopeLLM` | `model_name` | string | — | 必填，如 `"qwen-max"`；完整列表见 [选择模型](raw/model-user-guide/get-started-with-models/models.md) |
| `DashScopeEmbedding` | `model_name` | string | `"text-embedding-v2"` | 推荐使用 `v3` 获取最佳检索效果 |
| `DashScopeRerank` | `model`, `top_n`, `rerank_min_score` | string, int, float | `"gte-rerank"`, `3`, `0.0` | `rerank_min_score` 仅在 `enable_reranking=True` 时生效（见 `DashScopeCloudRetriever`） |
| `DashScopeCloudRetriever` | `dense_similarity_top_k`, `sparse_similarity_top_k`, `enable_reranking`, `rerank_model_name` | int, int, bool, string | `100`, `100`, `True`, `"gte-rerank-hybrid"` | 混合检索核心参数；`rerank_model_name` 支持 `gte-rerank-hybrid`（推荐）和 `gte-rerank` |

## 使用方式

### LlamaIndex 集成
1. **安装依赖**：根据组件选择安装包，例如：
   ```bash
   pip install llama-index-llms-dashscope  # 大模型
   pip install llama-index-embeddings-dashscope  # Embedding
   pip install llama-index-postprocessor-dashscope-rerank  # Rerank
   pip install llama-index-indices-managed-dashscope  # 云端知识库
   ```
2. **认证配置**：设置环境变量 `DASHSCOPE_API_KEY`；若使用子业务空间，还需设置 `DASHSCOPE_WORKSPACE_ID`。
3. **代码初始化**：
   - 全局设置（推荐）：
     ```python
     from llama_index.core import Settings
     from llama_index.llms.dashscope import DashScope
     from llama_index.embeddings.dashscope import DashScopeEmbedding
     Settings.llm = DashScope(model_name="qwen-plus")
     Settings.embed_model = DashScopeEmbedding(model_name="text-embedding-v3")
     ```
   - 局部实例化（按需）：
     ```python
     from llama_index.postprocessor.dashscope_rerank import DashScopeRerank
     reranker = DashScopeRerank(top_n=5, model="gte-rerank-hybrid")
     ```

### Spring AI Alibaba 集成
1. **添加 Maven 依赖**：引入 `spring-ai-alibaba-starter-dashscope`（版本 `1.0.0.2`）。
2. **配置 `application.yml`**：
   ```yaml
   spring:
     ai:
       dashscope:
         api-key: ${DASHSCOPE_API_KEY}  # 或 ${AI_DASHSCOPE_API_KEY}
         # workspace-id: ${WORKSPACE_ID}  # 子空间时启用
         agent:
           app-id: ${APP_ID}  # 智能体/工作流应用ID
   ```
3. **调用服务**：
   - 调用大模型应用：注入 `DashScopeAgent` 并调用 `agent.call()`。
   - 检索知识库：使用 `DashScopeDocumentRetriever` 与 `ChatClient` 组合实现 RAG（见 [通过Spring AI Alibaba检索知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)）。

## 限制和注意事项

- **文件解析限制**：`DashScopeParse` 仅对 PDF/DOC/DOCX 进行智能化解析，TXT/MD/PPT 等格式仅原样上传；单文件 ≤100MB 且 ≤1000 页；一次最多上传 200 个文件（见 [DashScopeCloudIndex 文档](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)）。
- **业务空间强制要求**：所有云端操作（`DashScopeCloudIndex`、`DashScopeCloudRetriever`、Spring AI Alibaba 的知识库检索）均**必须**配置 `DASHSCOPE_WORKSPACE_ID`，否则抛出 `ValueError`（见 [DashScopeCloudIndex 文档](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md) 和 [Spring AI Alibaba 知识库文档](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)）。
- **API Key 环境变量命名差异**：
  - LlamaIndex 生态统一使用 `DASHSCOPE_API_KEY`；
  - Spring AI Alibaba 示例中同时存在 `DASHSCOPE_API_KEY`（[调用大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)）和 `AI_DASHSCOPE_API_KEY`（[检索知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)），实际均可通过 `System.getenv()` 读取，但建议统一使用 `DASHSCOPE_API_KEY` 避免混淆。
- **模型兼容性**：`OpenAILike` 封装仅支持百炼的文本生成模型（不支持 Embedding/Rerank），而 `DashScope` 封装支持全部模型类型（见 [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)）。

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


