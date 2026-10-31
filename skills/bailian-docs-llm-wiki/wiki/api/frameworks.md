# frameworks

阿里云百炼平台提供对主流 AI 开发框架的深度集成支持，当前重点覆盖 LlamaIndex 和 Spring AI Alibaba 两大生态。通过官方适配的 SDK 和插件，开发者可快速将百炼的大模型服务、向量检索、知识库管理、智能文档解析等能力嵌入到现有应用架构中，无需从零实现底层对接逻辑。所有集成均基于百炼统一的 API 认证与计费体系，确保安全与可观测性。

## 支持的模型/功能

百炼在框架集成中提供以下核心能力：

- **大模型调用**：支持全部百炼文本生成模型（如 `qwen-max`、`qwen-plus`），可通过 `DashScope` 或 `OpenAILike` 两种方式接入 LlamaIndex；Spring AI Alibaba 则通过 `DashScopeAgent` 调用已发布的智能体或工作流应用 [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)。
- **Embedding 模型**：提供 `text-embedding-v1`/`v2`/`v3` 等多代向量模型，支持在 LlamaIndex 中构建本地向量索引，MTEB 检索任务得分最高达 73.23（`v3`）[使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)。
- **智能文档解析与切分**：`DashScopeParse` 支持 PDF/DOCX/DOC 格式智能化解析（基于 Document Mind），`DashScopeJsonNodeParser` 提供基于通义模型的语义切分能力，二者配合可替代传统规则切分 [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)。
- **云端知识库服务**：`DashScopeCloudIndex` 和 `DashScopeCloudRetriever` 封装了百炼云端知识库的创建、上传、索引与检索全流程，支持稠密/稀疏混合检索、Rerank 重排及字段过滤 [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)。
- **Rerank 排序**：`DashScopeRerank` 集成 `gte-rerank` 系列模型，用于对初始检索结果进行语义相关性重排序，提升 RAG 回答质量 [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)。

> **注意**：文档 1 明确指出“本方案将知识库部署在云端，使用默认的智能文档切分与官方向量模型，**不支持自定义文档切分方式或自定义嵌入模型**”，而文档 6 和文档 3 分别提供了 `DashScopeJsonNodeParser` 和 `DashScopeEmbedding` 的自定义能力。该矛盾表明：**云端知识库（DashScopeCloudIndex）强制使用百炼托管的切分与向量化流程；而本地向量索引（VectorStoreIndex）则允许完全自定义**。开发者需根据部署模式选择对应组件。

## 关键参数

| 组件 | 关键参数 | 说明 | 默认值 |
|--------|-----------|------|---------|
| `DashScope` (LLM) | `model_name` | 指定调用的百炼大模型，如 `"qwen-max"` | — |
| `DashScopeEmbedding` | `model_name` | 指定 Embedding 模型，如 `"text-embedding-v3"` | `"text-embedding-v2"` |
| `DashScopeRerank` | `model`, `top_n` | 排序模型名（`"gte-rerank"`）、返回 Top-K 结果数 | `"gte-rerank"`, `3` |
| `DashScopeCloudRetriever` | `dense_similarity_top_k`, `enable_reranking`, `rerank_top_n` | 向量召回数、是否启用重排、重排后返回数 | `100`, `True`, `5` |
| `DashScopeJsonNodeParser` | `chunk_size`, `separator` | 文本块大小、切分分隔符正则表达式 | `500`, `" \|,\|，\|。\|？\|！\|\n\|\?\|!"` |

## 使用方式

### LlamaIndex 生态
1. **安装依赖**：按需安装对应模块，例如：
   ```bash
   pip install llama-index-llms-dashscope  # LLM
   pip install llama-index-embeddings-dashscope  # Embedding
   pip install llama-index-indices-managed-dashscope  # 云端知识库
   ```
2. **配置认证**：设置环境变量 `DASHSCOPE_API_KEY`（必选），`DASHSCOPE_WORKSPACE_ID`（操作非默认业务空间时必选）。
3. **代码集成**：
   - 全局设置：`Settings.llm = DashScope(model_name="qwen-plus")`
   - 构建索引：`index = VectorStoreIndex.from_documents(..., embed_model=DashScopeEmbedding(...))`
   - 云端检索：`retriever = DashScopeCloudIndex("my_index").as_retriever()`

### Spring AI Alibaba 生态
1. **添加 Maven 依赖**：引入 `spring-ai-alibaba-starter-dashscope`。
2. **配置参数**：在 `application.yml` 中设置 `spring.ai.dashscope.api-key` 和 `spring.ai.dashscope.agent.app-id`。
3. **调用服务**：
   - 调用应用：注入 `DashScopeAgent`，调用 `agent.call(new Prompt(...))`
   - 检索知识库：使用 `DashScopeDocumentRetriever` 并配置 `indexName` 和 `searchFilters` [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。

## 限制和注意事项

- **文件解析限制**：`DashScopeParse` 仅对 `.pdf`、`.doc`、`.docx` 进行智能化解析；其他格式（如 `.txt`、`.md`）仅原样上传，不触发文档结构识别 [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)。
- **云端知识库不可定制**：如前所述，`DashScopeCloudIndex` 强制使用百炼托管的切分与向量化逻辑，无法替换为自定义 `NodeParser` 或 `Embedding` 模型。
- **业务空间强依赖**：所有涉及 `DashScopeCloudIndex`、`DashScopeCloudRetriever` 或 Spring AI Alibaba 的子空间操作，均**必须显式配置 `DASHSCOPE_WORKSPACE_ID`**，否则会报错或操作默认空间。
- **模型兼容性**：`OpenAILike` 方式仅支持百炼的文本生成类模型（即 `qwen-*` 系列），不支持 `text-embedding-*` 或 `gte-rerank-*` 等专用模型；后者需使用对应专用 SDK（如 `DashScopeEmbedding`、`DashScopeRerank`）。
- **Python 版本约束**：所有 `dashscope` 相关 LlamaIndex 插件要求 `python>=3.9,<=3.12`，超出范围可能导致安装失败或运行异常。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)
- [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)
- [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)
- [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)
- [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)
- [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)
- [DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)
- [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)


