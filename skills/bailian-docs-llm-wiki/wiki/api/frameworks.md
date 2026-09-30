# frameworks

百炼平台提供对主流 AI 开发框架的深度集成支持，重点覆盖 LlamaIndex 和 Spring AI Alibaba 两大生态，帮助开发者快速构建 RAG、智能体、工作流等生产级应用。所有集成均基于百炼统一的模型服务、知识库与应用管理能力，无需自行维护基础设施。

## 支持的模型与功能

百炼通过官方适配器支持以下核心能力：

- **大语言模型（LLM）调用**：支持 `qwen-max`、`qwen-plus`、`qwen-turbo` 等全部百炼文本生成模型，可通过 `DashScope` 或 OpenAI-like 封装两种方式接入 [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)。
- **Embedding 模型**：提供 `text-embedding-v1`/`v2`/`v3` 三款向量模型，其中 `text-embedding-v3` 在 CMTEB Retrieval 任务上达 73.23 分，为当前最优 [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)。
- **重排序（Rerank）**：集成 `gte-rerank` 和 `gte-rerank-hybrid` 模型，用于提升检索结果相关性 [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)。
- **文档解析与切分**：`DashScopeParse` 支持 PDF/DOCX/DOC 智能解析（基于文档智能 DocMind），`DashScopeJsonNodeParser` 提供基于通义文本切分模型的语义分块能力 [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md) 和 [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)。
- **云端知识库托管**：`DashScopeCloudIndex` 实现文件上传、智能切分、向量化索引与检索一体化，支持直接复用百炼控制台创建的知识库 [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)。

> **注意**：文档 1 明确指出“本方案将知识库部署在云端，使用默认的智能文档切分与官方向量模型，**不支持自定义文档切分方式或自定义嵌入模型**”，而文档 6 的 `DashScopeJsonNodeParser` 和文档 3 的 `DashScopeEmbedding` 均允许自定义切分逻辑与 embedding 模型。该矛盾表明：**云端知识库（DashScopeCloudIndex）托管模式强制使用百炼内置处理链，而本地索引（VectorStoreIndex + DashScopeEmbedding）模式才支持完全自定义**。开发者需根据部署形态选择对应方案。

## 关键参数

| 组件 | 参数名 | 类型 | 默认值 | 说明 |
|--------|---------|------|---------|------|
| `DashScopeLLM` | `model_name` | string | — | 必填，如 `"qwen-max"`；完整列表见 [选择模型](raw/model-user-guide/get-started-with-models/models.md) |
| `DashScopeEmbedding` | `model_name` | string | `"text-embedding-v2"` | 可选值：`"text-embedding-v1"`/`"v2"`/`"v3"` |
| `DashScopeRerank` | `top_n`, `model` | int, string | `5`, `"gte-rerank"` | `model` 可选 `"gte-rerank"` 或 `"gte-rerank-hybrid"` |
| `DashScopeCloudRetriever` | `dense_similarity_top_k`, `enable_reranking`, `rerank_top_n` | int, bool, int | `100`, `True`, `5` | 控制向量召回数量与重排行为；`rerank_min_score` 用于过滤低分节点（仅 rerank 启用时生效） |
| `DashScopeParse` | `category_id`, `workspace` | string, string | `"default"`, `None` | `category_id` 对应控制台「应用数据」→「文件」类目ID；`workspace` 为业务空间ID |

## 使用方式

### LlamaIndex 生态
1. **安装依赖**：按需安装对应模块，例如：
   ```bash
   pip install llama-index-llms-dashscope  # LLM
   pip install llama-index-embeddings-dashscope  # Embedding
   pip install llama-index-postprocessor-dashscope-rerank  # Rerank
   pip install llama-index-indices-managed-dashscope  # CloudIndex
   ```
2. **初始化组件**（以 CloudIndex 为例）：
   ```python
   from llama_index.indices.managed.dashscope import DashScopeCloudIndex
   os.environ["DASHSCOPE_WORKSPACE_ID"] = "your_workspace_id"
   index = DashScopeCloudIndex("my_first_index")  # 复用已有云端知识库
   retriever = index.as_retriever(dense_similarity_top_k=10)
   nodes = retriever.retrieve("阿里云百炼手机有哪些？")
   ```
3. **全局设置（可选）**：统一配置默认 LLM 或 Embedding：
   ```python
   from llama_index.core import Settings
   from llama_index.llms.dashscope import DashScope
   Settings.llm = DashScope(model_name="qwen-plus")
   ```

### Spring AI Alibaba 生态
1. **添加 Maven 依赖**：
   ```xml
   <dependency>
       <groupId>com.alibaba.cloud.ai</groupId>
       <artifactId>spring-ai-alibaba-starter-dashscope</artifactId>
       <version>1.0.0.2</version>
   </dependency>
   ```
2. **配置 `application.yml`**：
   ```yaml
   spring:
     ai:
       dashscope:
         api-key: ${DASHSCOPE_API_KEY}
         # workspace-id: ${WORKSPACE_ID}  # 子空间时启用
         agent:
           app-id: ${APP_ID}  # 调用智能体/工作流应用
   ```
3. **Java 调用示例**：
   - 调用大模型应用：注入 `DashScopeAgent` 并执行 `agent.call(prompt)`
   - 检索知识库：使用 `DashScopeDocumentRetriever` 集成到 `ChatClient` 的 `DocumentRetrievalAdvisor` 中 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。

## 限制和注意事项

- **文件解析限制**：`DashScopeParse` 仅对 `.pdf`、`.doc`、`.docx` 进行智能解析；其他格式（如 `.txt`、`.md`）仅原样上传，不触发文档结构识别 [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)。
- **环境变量要求**：所有 DashScope 组件均依赖 `DASHSCOPE_API_KEY`；若使用非默认业务空间，**必须**设置 `DASHSCOPE_WORKSPACE_ID`（LlamaIndex）或 `AI_DASHSCOPE_WORKSPACE_ID`（Spring AI Alibaba），且二者环境变量名不同，需按框架分别配置。
- **Python 版本兼容性**：所有 `llama-index-*` 包要求 `python>=3.9,<=3.12`，超出范围可能导致安装失败或运行异常。
- **云端知识库不可定制性**：如前所述，`DashScopeCloudIndex` 托管模式下无法替换嵌入模型、切分策略或解析引擎，其能力边界由百炼平台统一定义，与本地 `VectorStoreIndex` + `DashScopeEmbedding` 方案存在本质差异。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)
- [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)
- [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)
- [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)
- [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)
- [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)
- [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)


