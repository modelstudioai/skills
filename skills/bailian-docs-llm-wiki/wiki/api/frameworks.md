# frameworks

百炼平台提供对主流 AI 开发框架的原生集成支持，重点覆盖 LlamaIndex 和 Spring AI Alibaba 两大生态。开发者可基于这些框架快速构建 RAG 应用、调用大模型、管理知识库及集成智能体/工作流应用，无需从零实现底层能力。所有集成均通过官方 SDK 封装，统一使用 `DASHSCOPE_API_KEY` 认证，并与百炼控制台的业务空间、知识库、应用等资源深度协同。

## 支持的模型与功能

- **大模型（LLM）调用**：支持全部百炼文本生成模型（如 `qwen-max`、`qwen-plus`），可通过 LlamaIndex 的 `DashScope` 或 `OpenAILike` 封装调用；Spring AI Alibaba 则通过 `DashScopeAgent` 调用已部署的[智能体应用（Agent 1.0）](raw/application-user-guide/llm-application/single-agent-application.md)或[工作流应用](raw/application-user-guide/llm-application/workflow-application.md)。
- **Embedding 模型**：支持 `text-embedding-v1`/`v2`/`v3`，其中 `v3` 在 CMTEB Retrieval 任务上达 73.23 分，推荐用于高精度语义检索 [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)。
- **重排序（Rerank）**：提供 `gte-rerank` 和 `gte-rerank-hybrid` 模型，用于对向量检索结果进行语义精排，提升 Top-K 相关性。
- **文档解析与切分**：`DashScopeParse` 基于“文档智能（Document Mind）”服务，支持 PDF/DOCX/DOC 格式智能化解析；`DashScopeJsonNodeParser` 对解析结果进行规则+模型驱动的中文切分，支持自定义分隔符与重叠策略。
- **云端知识库管理**：`DashScopeCloudIndex` 实现知识库的创建、增删文档及索引更新；`DashScopeCloudRetriever` 提供稠密/稀疏混合检索、重排开关、分数阈值过滤等生产级参数控制。

## 关键参数

| 组件 | 参数名 | 类型 | 默认值 | 说明 |
|--------|---------|------|---------|------|
| `DashScopeLLM` | `model_name` | string | — | 必填，如 `"qwen-max"`；完整列表见[选择模型](raw/model-user-guide/get-started-with-models/models.md) |
| `DashScopeEmbedding` | `model_name` | string | `"text-embedding-v2"` | 推荐显式指定，`v3` 为当前最优 [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md) |
| `DashScopeRerank` | `top_n`, `model` | int, string | `5`, `"gte-rerank"` | `top_n` 控制返回节点数；`model` 可选 `gte-rerank-hybrid`（混合检索重排） |
| `DashScopeCloudRetriever` | `dense_similarity_top_k`, `sparse_similarity_top_k` | int | `100`, `100` | 分别控制向量/关键词召回数量；`enable_reranking=True` 时生效 |
| `DashScopeCloudRetriever` | `rerank_min_score` | float | `0.0` | 仅当 `enable_reranking=True` 时生效，过滤重排后低于该分的节点 |
| `DashScopeJsonNodeParser` | `chunk_size`, `separator` | int, string | `500`, `" \|,\|，\|。\|？\|！\|\n\|\?\|!"` | 中文场景建议保留默认分隔符，避免切碎语义单元 |

> **注意**：`DashScopeCloudIndex` 的 `from_documents()` 方法在[通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)中明确要求必须设置 `DASHSCOPE_WORKSPACE_ID` 环境变量，而[通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)示例代码中未体现该约束，实际部署时需补全，否则初始化失败。

## 使用方式

### LlamaIndex 集成
1. **安装依赖**：按组件选择安装，例如：
   ```bash
   pip install llama-index-llms-dashscope  # LLM
   pip install llama-index-embeddings-dashscope  # Embedding
   pip install llama-index-postprocessor-dashscope-rerank  # Rerank
   pip install llama-index-indices-managed-dashscope  # CloudIndex
   ```
2. **认证配置**：设置环境变量 `DASHSCOPE_API_KEY`；若使用子业务空间，**必须**设置 `DASHSCOPE_WORKSPACE_ID`。
3. **核心调用模式**：
   - LLM：`DashScope(model_name="qwen-plus")` 或全局 `Settings.llm = ...`
   - Embedding：`DashScopeEmbedding(model_name="text-embedding-v3")`
   - Rerank：`DashScopeRerank(top_n=3, model="gte-rerank-hybrid")`
   - 云端知识库：`DashScopeCloudIndex("my_index").as_retriever(...)`  
   完整示例见 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。

### Spring AI Alibaba 集成
1. **添加 Maven 依赖**：引入 `spring-ai-alibaba-starter-dashscope`（版本 `1.0.0.2`）。
2. **配置参数**：在 `application.yml` 中声明 `spring.ai.dashscope.api-key` 和 `spring.ai.dashscope.agent.app-id`（调用应用时）或 `spring.ai.dashscope.workspace-id`（操作子空间知识库时）。
3. **调用方式**：
   - 调用应用：注入 `DashScopeAgent`，传入 `Prompt` 和 `DashScopeAgentOptions.withAppId(...)`
   - 检索知识库：使用 `DashScopeDocumentRetriever` + `DocumentRetrievalAdvisor` 构建 `ChatClient`，自动注入上下文 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。

## 限制和注意事项

- **文件解析限制**：`DashScopeParse` 仅对 PDF/DOC/DOCX 进行智能化解析（提取结构化文本、表格、公式），其他格式（TXT/MD/PPT等）仅原样上传，不解析 [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)。
- **云端知识库能力边界**：`DashScopeCloudIndex` 方案**不支持自定义文档切分逻辑或嵌入模型**，其切分与向量化由百炼平台统一完成；如需完全自控，应选用本地知识库方案 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。
- **环境变量一致性**：LlamaIndex 示例多使用 `DASHSCOPE_API_KEY`，而 Spring AI Alibaba 文档中知识库示例使用 `AI_DASHSCOPE_API_KEY`；为简化维护，**统一推荐使用 `DASHSCOPE_API_KEY`**，并在 Spring Boot 配置中映射：`spring.ai.dashscope.api-key: ${DASHSCOPE_API_KEY}`。
- **Python 版本兼容性**：所有 LlamaIndex 相关组件要求 `python>=3.9,<=3.12`，超出范围可能导致安装失败或运行异常 [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)
- [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)
- [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)
- [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)
- [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)
- [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)
- [DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)
- [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)


