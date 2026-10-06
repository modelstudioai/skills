# frameworks

阿里云百炼平台提供对主流 AI 开发框架的原生集成支持，重点覆盖 LlamaIndex 和 Spring AI Alibaba 两大生态，帮助开发者快速构建 RAG、智能体、工作流等生产级应用。所有集成均基于百炼统一的模型服务、知识库与应用管理能力，无需自行部署底层基础设施。

## 支持的模型与功能

百炼通过官方适配器支持以下核心能力：

- **大语言模型（LLM）调用**：支持 `qwen-max`、`qwen-plus`、`qwen-turbo` 等全部百炼文本生成模型，可通过 `DashScope` 或 OpenAI-like 封装方式接入 [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)。
- **Embedding 模型**：提供 `text-embedding-v1`/`v2`/`v3` 三款向量模型，其中 `v3` 在 CMTEB Retrieval 任务上达 73.23 分，为当前最优 [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)。
- **重排序（Rerank）**：集成 `gte-rerank` 和 `gte-rerank-hybrid` 模型，支持对检索结果进行语义精排 [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)。
- **文档解析与切分**：通过 `DashScopeParse` 调用文档智能（DocMind）服务，支持 PDF/DOCX/DOC 格式智能解析；配合 `DashScopeJsonNodeParser` 实现基于通义文本切分模型的高质量 chunking。
- **云端知识库托管**：`DashScopeCloudIndex` 提供端到端的云端索引构建、更新与检索能力，自动完成文档上传、解析、切分、向量化与索引存储，无需本地向量数据库 [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)。
- **Java 生态支持**：Spring AI Alibaba 提供 `DashScopeAgent`（调用智能体/工作流应用）和 `DashScopeDocumentRetriever`（检索知识库）两个核心组件，深度集成 Spring Boot 生命周期与响应式编程模型。

> **注意**：文档 1 明确指出“本方案将知识库部署在云端，使用默认的智能文档切分与官方向量模型，**不支持自定义文档切分方式或自定义嵌入模型**”，而文档 6 和 3 分别提供了 `DashScopeJsonNodeParser` 和 `DashScopeEmbedding` 的自定义能力——这表明**自定义切分与嵌入仅适用于本地索引场景（如 `VectorStoreIndex`），不适用于 `DashScopeCloudIndex` 托管模式**。

## 关键参数

| 组件 | 参数名 | 类型 | 默认值 | 说明 |
|--------|---------|------|---------|------|
| `DashScope` (LLM) | `model_name` | string | — | 必填，如 `"qwen-max"`；完整列表见 [选择模型](raw/model-user-guide/get-started-with-models/models.md) |
| `DashScopeEmbedding` | `model_name` | string | `"text-embedding-v2"` | 推荐使用 `v3` 获取最佳检索效果 |
| `DashScopeRerank` | `top_n`, `model` | int, string | `5`, `"gte-rerank"` | `model` 可选 `"gte-rerank-hybrid"`（文档 4 vs 文档 8） |
| `DashScopeCloudRetriever` | `dense_similarity_top_k`, `enable_reranking`, `rerank_top_n` | int, bool, int | `100`, `True`, `5` | 控制召回数量与重排行为；`rerank_top_n` 优先级高于全局 `top_n`（文档 8） |
| `DashScopeJsonNodeParser` | `chunk_size`, `overlap_size`, `separator` | int, int, string | `500`, `100`, `" \|,\|，\|。\|？\|！\|\n\|\?\|!"` | 中文分隔符已预设，`language="cn"` 为默认且推荐值 |

## 使用方式

### LlamaIndex 集成（Python）

1. **安装依赖**  
   ```bash
   # 基础
   pip install llama-index-core
   # 按需安装模块（不可全装）
   pip install llama-index-llms-dashscope          # LLM
   pip install llama-index-embeddings-dashscope     # Embedding
   pip install llama-index-postprocessor-dashscope-rerank  # Rerank
   pip install llama-index-readers-dashscope        # DashScopeParse
   pip install llama-index-node-parser-dashscope    # JsonNodeParser
   pip install llama-index-indices-managed-dashscope # CloudIndex/CloudRetriever
   ```

2. **全局配置（推荐）**  
   ```python
   from llama_index.core import Settings
   from llama_index.llms.dashscope import DashScope
   from llama_index.embeddings.dashscope import DashScopeEmbedding

   Settings.llm = DashScope(model_name="qwen-plus")
   Settings.embed_model = DashScopeEmbedding(model_name="text-embedding-v3")
   ```

3. **云端知识库典型流程**  
   - 使用 `DashScopeParse` 解析本地 PDF/DOCX → `DashScopeCloudIndex.from_documents()` 构建云端索引 → `index.as_retriever()` 获取 `DashScopeCloudRetriever` → `retriever.retrieve(query)` 检索。

### Spring AI Alibaba 集成（Java）

1. **添加 Maven 依赖**  
   ```xml
   <dependency>
       <groupId>com.alibaba.cloud.ai</groupId>
       <artifactId>spring-ai-alibaba-starter-dashscope</artifactId>
       <version>1.0.0.2</version>
   </dependency>
   ```

2. **配置 `application.yml`**  
   ```yaml
   spring:
     ai:
       dashscope:
         api-key: ${DASHSCOPE_API_KEY}
         # agent:
         #   app-id: ${APP_ID}           # 调用应用时启用
         # workspace-id: ${WORKSPACE_ID} # 子空间时启用
   ```

3. **代码调用**  
   - 调用应用：注入 `DashScopeAgent`，调用 `.call(new Prompt(...))`  
   - 检索知识库：使用 `DashScopeDocumentRetriever` + `DocumentRetrievalAdvisor` 构建 `ChatClient`

## 限制和注意事项

- **文件解析限制**：`DashScopeParse` 仅对 PDF/DOC/DOCX 进行智能解析（提取表格、公式、版面结构），TXT/MD/PPT 等格式仅原样上传，不解析 [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)。
- **云端知识库不可定制**：`DashScopeCloudIndex` 托管模式下，**不支持自定义切分逻辑、嵌入模型或索引结构**，所有处理由百炼后台统一执行（文档 1）。
- **业务空间强制要求**：使用 `DashScopeCloudIndex` 或 `DashScopeCloudRetriever` 时，`DASHSCOPE_WORKSPACE_ID` 环境变量**必须显式设置**，IDE 需手动配置（文档 7）。
- **模型兼容性**：OpenAI-like 封装仅支持百炼的**文本生成类模型**（如 `qwen-*`），不支持多模态、语音等模型（文档 2）。
- **Spring AI Alibaba 环境变量差异**：LlamaIndex 推荐 `DASHSCOPE_API_KEY`，而 Spring AI Alibaba 示例中使用 `AI_DASHSCOPE_API_KEY`（文档 11），两者均可生效，但需保持项目内一致。

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


