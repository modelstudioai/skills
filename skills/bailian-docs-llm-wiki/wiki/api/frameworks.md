# frameworks

百炼平台提供对主流 AI 开发框架的原生集成支持，重点覆盖 LlamaIndex 和 Spring AI Alibaba 两大生态，帮助开发者快速构建 RAG、智能体、工作流等生产级应用。所有集成均通过官方 SDK 封装，统一使用 DashScope API Key 认证，并与百炼控制台的业务空间、知识库、应用等资源深度联动。

## 支持的模型与功能

- **大模型调用**：支持通过 `DashScope`（推荐）或 `OpenAILike`（兼容模式）两种方式调用百炼全部文本生成模型，如 `qwen-max`、`qwen-plus` 等；完整模型列表及规格请参考 [选择模型](raw/model-user-guide/get-started-with-models/models.md)。  
- **Embedding 模型**：提供 `text-embedding-v1`/`v2`/`v3` 三款向量模型，其中 `v3` 在 CMTEB Retrieval 任务上达 73.23 分，为当前最优；[使用 Embedding 模型](raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md) 文档详细说明了性能指标与调用方式。  
- **重排序（Rerank）**：集成 `gte-rerank` 和 `gte-rerank-hybrid` 模型，用于对检索结果进行语义精排，提升 RAG 回答准确性。  
- **文档解析与切分**：`DashScopeParse` 调用阿里云“文档智能（Document Mind）”服务，支持 PDF/DOCX/DOC 格式智能化解析；`DashScopeJsonNodeParser` 基于解析结果进行高质量文本切分，支持自定义分隔符与中英文语言识别。  
- **云端知识库管理**：`DashScopeCloudIndex` 和 `DashScopeCloudRetriever` 提供端到端的云端知识库构建、索引与检索能力，无需本地向量存储，自动完成智能切分、嵌入与索引。  
- **Java 生态支持**：`Spring AI Alibaba` 提供 `DashScopeAgent`（调用智能体/工作流应用）和 `DashScopeDocumentRetriever`（检索知识库）两类核心组件，无缝对接 Spring Boot 3.x 应用。

> **注意**：文档 1 明确指出“本方案将知识库部署在云端，使用默认的智能文档切分与官方向量模型，不支持自定义文档切分方式或自定义嵌入模型”，而文档 6 和文档 3 分别提供了 `DashScopeJsonNodeParser` 和 `DashScopeEmbedding` 的自定义能力——这表明**自定义能力仅适用于本地索引路径（如 `VectorStoreIndex`），不适用于 `DashScopeCloudIndex` 云端路径**。开发者需根据部署模式（本地 vs 云端）选择对应组件。

## 关键参数

| 组件 | 关键参数 | 说明 | 默认值 |
|--------|-----------|------|---------|
| `DashScope` LLM | `model_name` | 指定调用的大模型名称 | — |
| `DashScopeEmbedding` | `model_name` | 指定 Embedding 模型，如 `"text-embedding-v2"` | `"text-embedding-v2"` |
| `DashScopeRerank` | `top_n`, `model` | 返回重排后 Top-N 结果；支持 `"gte-rerank"` 或 `"gte-rerank-hybrid"` | `3`, `"gte-rerank"` |
| `DashScopeCloudRetriever` | `dense_similarity_top_k`, `enable_reranking`, `rerank_top_n` | 向量召回数、是否启用重排、重排后返回数 | `100`, `True`, `5` |
| `DashScopeJsonNodeParser` | `chunk_size`, `overlap_size`, `separator`, `language` | 切分粒度、重叠长度、分隔符正则、语言（`"cn"`/`"en"`/`"any"`） | `500`, `100`, `" \|,\|，\|。\|？\|！\|\n\|\?\|\!"`, `"cn"` |

## 使用方式

### LlamaIndex 集成（Python）

1. **安装依赖**（按需组合）：
   ```bash
   pip install llama-index-core
   pip install llama-index-llms-dashscope           # LLM
   pip install llama-index-embeddings-dashscope     # Embedding
   pip install llama-index-postprocessor-dashscope-rerank  # Rerank
   pip install llama-index-readers-dashscope        # Parse
   pip install llama-index-node-parser-dashscope    # JsonNodeParser
   pip install llama-index-indices-managed-dashscope # CloudIndex/Retriever
   ```

2. **全局配置（可选）**：
   ```python
   from llama_index.core import Settings
   from llama_index.llms.dashscope import DashScope
   from llama_index.embeddings.dashscope import DashScopeEmbedding

   Settings.llm = DashScope(model_name="qwen-plus")
   Settings.embed_model = DashScopeEmbedding(model_name="text-embedding-v3")
   ```

3. **典型流程**（以云端 RAG 为例）：
   - 使用 `DashScopeParse` 解析本地 PDF/DOCX → `DashScopeCloudIndex.from_documents()` 构建云端知识库 → `index.as_retriever()` 获取 `DashScopeCloudRetriever` → 调用 `retriever.retrieve()` 检索。
   - 全流程示例见 [通过LlamaIndex API构建RAG应用](raw/application-api-reference/frameworks/llamaindex.md)。

### Spring AI Alibaba 集成（Java）

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
           app-id: ${APP_ID}  # 智能体/工作流应用ID
   ```

3. **调用方式**：
   - 调用应用：注入 `DashScopeAgent`，调用 `agent.call(new Prompt(...))`；
   - 检索知识库：注入 `DashScopeApi`，构造 `DashScopeDocumentRetriever` 并集成至 `ChatClient` 的 `DocumentRetrievalAdvisor`。详情参见 [通过Spring AI Alibaba检索阿里云百炼知识库](raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。

## 限制和注意事项

- **文件限制**：`DashScopeParse` 仅对 PDF/DOC/DOCX 进行智能化解析；单文件 ≤100 MB 且 ≤1000 页；一次最多上传 200 个文件。其他格式（如 TXT、PPTX）仅原样上传，不解析。  
- **业务空间强制要求**：所有云端操作（`DashScopeCloudIndex`、`DashScopeCloudRetriever`、Spring AI Alibaba 的知识库/应用调用）均**必须配置 `DASHSCOPE_WORKSPACE_ID` 环境变量**，否则初始化失败（见文档 7 和文档 10）。  
- **API Key 环境变量名差异**：LlamaIndex 示例多使用 `DASHSCOPE_API_KEY`，而 Spring AI Alibaba 文档 11 明确要求使用 `AI_DASHSCOPE_API_KEY`；实际使用时需按所选 SDK 文档配置对应变量名，避免认证失败。  
- **模型兼容性**：`OpenAILike` 方式仅支持百炼的文本生成模型（非所有模型），且不支持流式响应等高级特性；生产环境推荐优先使用原生 `DashScope` SDK。  
- **重排模型参数一致性**：`DashScopeRerank`（文档 4）默认 `model="gte-rerank"`，而 `DashScopeCloudRetriever`（文档 9）默认 `rerank_model_name="gte-rerank-hybrid"`；二者模型能力不同，混用时需显式对齐参数，否则效果不可预期。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)
- [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)
- [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)
- [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)
- [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)
- [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)
- [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)
- [DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)


