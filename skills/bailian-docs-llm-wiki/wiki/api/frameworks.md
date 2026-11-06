# frameworks

百炼平台提供多种主流 AI 开发框架的原生集成支持，重点覆盖 LlamaIndex 和 Spring AI Alibaba 两大生态，帮助开发者快速构建 RAG 应用、知识库检索系统及大模型智能体。所有集成均基于百炼统一的 API Key 认证与业务空间管理机制，支持云端文档解析、向量索引、重排、检索与生成全链路能力。

## 支持的模型/功能

- **LlamaIndex 生态**：完整支持 `DashScopeParse`（智能文档解析）、`DashScopeCloudIndex`（云端知识库索引）、`DashScopeCloudRetriever`（云端检索器）、`DashScopeRerank`（GTE-Rerank 系列重排模型）、`DashScopeJsonNodeParser`（语义切分）及 `DashScopeEmbedding`（text-embedding-v1/v2/v3）等组件。其中，`text-embedding-v3` 在 CMTEB 检索任务上达 73.23 分，为当前最优 [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)。
- **Spring AI Alibaba（SAA）生态**：支持两类核心集成：① 通过 `DashScopeAgent` 调用百炼大模型应用（仅限 Agent 1.0 与工作流应用）；② 通过 `DashScopeDocumentRetriever` 或直调 RAG API 检索百炼知识库，支持 `searchFilters` 多条件组合（如 OR 嵌套）[通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。
- **统一模型调用层**：LlamaIndex 可通过 `DashScope` LLM 类或 `OpenAILike` 封装调用全部百炼文本生成模型（如 `qwen-max`, `qwen-plus`），费用与输入上限详见 [选择模型](raw/model-user-guide/get-started-with-models/models.md) [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)。

## 关键参数

| 组件 | 关键参数 | 说明 |
|--------|-----------|------|
| `DashScopeParse` | `result_type`, `category_id`, `workspace` | `result_type=ResultType.DASHSCOPE_DOCMIND` 启用智能解析；`category_id` 必须显式传入以匹配应用数据类目（默认类目不生效）；`workspace` 需与 `DASHSCOPE_WORKSPACE_ID` 一致。 |
| `DashScopeCloudIndex` | `name`, `workspace_id` | `name` 为知识库唯一标识；`workspace_id` 必须通过环境变量或显式参数传入，否则初始化失败。 |
| `DashScopeCloudRetriever` | `dense_similarity_top_k`, `enable_reranking`, `rerank_model_name`, `rerank_top_n` | 默认启用重排（`enable_reranking=True`），模型为 `gte-rerank-hybrid`；`rerank_top_n=5` 控制最终返回节点数。 |
| `DashScopeRerank` | `model`, `top_n` | `model` 支持 `gte-rerank`（v1）与 `gte-rerank-v2`（v2），注意文档 1 中示例使用 `gte-rerank-v2`，而文档 9 参数说明仅列出 `gte-rerank` > **注意**：文档 1 与文档 9 对支持模型的描述存在不一致，实际应以 [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md) 官方 API 文档为准。 |
| `DashScopeEmbedding` | `model_name` | 推荐使用 `text-embedding-v3`（CMTEB 检索分 73.23），性能显著优于 v1/v2。 |

## 使用方式

1. **环境准备**：  
   - 获取并配置 `DASHSCOPE_API_KEY`（必选）与 `DASHSCOPE_WORKSPACE_ID`（必选，非默认业务空间时需显式设置）；  
   - Python 项目安装对应包（如 `pip install llama-index-indices-managed-dashscope`）；  
   - Spring Boot 项目添加 `spring-ai-alibaba-starter-dashscope` 依赖。

2. **LlamaIndex 典型流程**：  
   - 解析：用 `DashScopeParse` 上传并解析 PDF/DOCX（仅此两类支持智能解析），其他格式仅原样上传；  
   - 索引：用 `DashScopeCloudIndex.from_documents()` 构建云端知识库；  
   - 检索：`index.as_retriever()` 初始化 `DashScopeCloudRetriever`，支持稠密/稀疏混合检索与重排；  
   - 生成：结合 `DashScope` LLM 或 `OpenAILike` 封装完成 RAG 回答。

3. **Spring AI Alibaba 典型流程**：  
   - 配置 `application.yml` 中 `spring.ai.dashscope.agent.app-id` 与 `api-key`；  
   - 使用 `DashScopeAgent` 调用智能体/工作流应用；  
   - 使用 `DashScopeDocumentRetriever` + `DocumentRetrievalAdvisor` 实现知识库检索增强问答。

## 限制和注意事项

- **文件解析限制**：`DashScopeParse` 仅对 `.pdf`、`.doc`、`.docx` 进行智能解析（OCR+结构识别），`.txt`、`.md` 等格式仅原样上传，不触发智能切分 [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)。单文件 ≤100MB 且 ≤1000 页。
- **知识库部署模式**：云端知识库方案（`DashScopeCloudIndex`）**不支持自定义文档切分方式或自定义嵌入模型**，若需完全控制切分逻辑与 embedding 模型，请参考本地知识库方案 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)。
- **业务空间强依赖**：所有云端操作（索引、检索、解析）均强制要求 `DASHSCOPE_WORKSPACE_ID`，未配置将直接报错（如 `ValueError: DASHSCOPE_WORKSPACE_ID 未设置`），且 IDE 环境需手动注入该变量。
- **模型兼容性**：`DashScopeRerank` 的 `model` 参数在不同文档中存在版本差异（`gte-rerank` vs `gte-rerank-v2`），建议以运行时实际可用模型列表为准，避免硬编码过时名称。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)
- [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)
- [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)
- [DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)
- [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)
- [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)
- [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)
- [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)


