# frameworks

百炼平台提供面向主流 AI 开发框架的深度集成支持，重点覆盖 LlamaIndex 和 Spring AI Alibaba 两大生态。通过官方适配的 SDK 和插件，开发者可快速将百炼的大模型服务、Embedding 模型、智能文档解析、云端知识库检索与重排等能力嵌入现有应用架构，无需从零实现底层对接逻辑。

## 支持的模型与功能

百炼在 LlamaIndex 生态中提供全栈式组件支持：
- **大模型（LLM）**：支持 `qwen-plus`、`qwen-max` 等全部文本生成模型，可通过 [DashScope](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md) 或 OpenAI 兼容模式调用；
- **Embedding 模型**：提供 `text-embedding-v1`/`v2`/`v3` 三代模型，其中 `text-embedding-v3` 在 CMTEB Retrieval 任务上达 73.23 分，为当前最优 [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)；
- **智能文档解析**：`DashScopeParse` 基于“文档智能（Document Mind）”服务，支持 PDF/DOCX/DOC 格式智能化解析（非结构化内容提取），其他格式仅原样上传 [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)；
- **检索增强组件**：包括 `DashScopeRerank`（支持 `gte-rerank` 和 `gte-rerank-hybrid`）、`DashScopeCloudRetriever`（云端向量+全文混合检索）、`DashScopeJsonNodeParser`（配合 DashScopeParse 进行语义切分）；
- **云端知识库管理**：`DashScopeCloudIndex` 封装了从本地[文件上传](../concepts/file-upload.md)、云端智能切分、索引构建到检索引擎初始化的完整生命周期。

Spring AI Alibaba 则聚焦于企业级 Java 应用集成，支持两类核心场景：
- 调用百炼已发布的**大模型应用**（仅限 Agent 1.0 和工作流应用）；
- 检索百炼**云端知识库**（支持 `searchFilters` 多条件过滤，含 `_operator: OR` 及嵌套 `_conditions`）。

> **注意**：文档 9 明确说明“只有 PDF、DOC、DOCX 文件会进行智能化解析，其他类型的文件只原样上传到云端，不进行解析”，而文档 4 的 `DashScopeParse` 描述中未强调此限制，实际以文档 9 为准。

## 关键参数

| 组件 | 关键参数 | 说明 |
|--------|-----------|------|
| `DashScopeEmbedding` | `model_name` | 必填，值为 `text-embedding-v1`/`v2`/`v3`；默认无 fallback，需显式指定 |
| `DashScopeRerank` | `model`, `top_n`, `rerank_min_score` | `model` 默认 `gte-rerank`，但 `DashScopeCloudRetriever` 默认使用 `gte-rerank-hybrid`；`rerank_min_score` 仅在 `enable_reranking=True` 时生效 |
| `DashScopeCloudRetriever` | `dense_similarity_top_k`, `sparse_similarity_top_k`, `enable_reranking`, `rerank_model_name` | `rerank_model_name` 默认 `gte-rerank-hybrid`，与 `DashScopeRerank` 的默认值不同，需注意一致性 |
| `DashScopeJsonNodeParser` | `chunk_size`, `overlap_size`, `separator`, `language` | `language` 接受 `"cn"`/`"en"`/`"any"`，`"any"` 模式性能显著下降，生产环境应明确指定 |
| Spring AI Alibaba | `app-id`, `api-key`, `workspace-id`, `indexName` | `workspace-id` 在子业务空间场景下为必填项；`indexName` 用于 SDK 检索，而 HTTP 直调 RAG API 需传 `index_id` |

## 使用方式

### LlamaIndex 集成（Python）

1. **安装依赖**：按需安装对应组件，例如：
   ```bash
   pip install llama-index-core llama-index-llms-dashscope  # LLM
   pip install llama-index-embeddings-dashscope              # Embedding
   pip install llama-index-readers-dashscope                 # DashScopeParse
   pip install llama-index-indices-managed-dashscope       # DashScopeCloudIndex
   ```

2. **配置认证**：通过环境变量设置 `DASHSCOPE_API_KEY`（必需）和 `DASHSCOPE_WORKSPACE_ID`（子空间必需）。

3. **代码示例**：
   - 使用 `DashScopeCloudIndex` 构建云端知识库并检索：
     ```python
     from llama_index.indices.managed.dashscope import DashScopeCloudIndex
     index = DashScopeCloudIndex("my_first_index")
     retriever = index.as_retriever(dense_similarity_top_k=50)
     nodes = retriever.retrieve("阿里云百炼手机有哪些？")
     ```
   - 使用 `DashScopeEmbedding` 构建本地向量索引：
     ```python
     from llama_index.embeddings.dashscope import DashScopeEmbedding
     from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
     index = VectorStoreIndex.from_documents(
         documents,
         embed_model=DashScopeEmbedding(model_name="text-embedding-v3")
     )
     ```

### Spring AI Alibaba 集成（Java）

1. **添加 Maven 依赖**：引入 `spring-ai-alibaba-starter-dashscope`（版本 ≥ 1.0.0.2）。

2. **配置参数**：在 `application.yml` 中声明：
   ```yaml
   spring:
     ai:
       dashscope:
         agent:
           app-id: ${APP_ID}  # 调用应用时必需
         api-key: ${AI_DASHSCOPE_API_KEY}
         # workspace-id: ${AI_DASHSCOPE_WORKSPACE_ID}  # 子空间必需
   ```

3. **代码示例**：
   - 调用大模型应用：
     ```java
     @GetMapping("/bailian/agent/call")
     public String call(@RequestParam String message) {
         return agent.call(new Prompt(message, DashScopeAgentOptions.builder().withAppId(appId).build())).getResult().getOutput().getText();
     }
     ```
   - 检索知识库（带过滤）：
     ```java
     Map<String, Object> orGroup = Map.of("_operator", "OR",
         "_conditions", List.of(
             Map.of("department", "Corporate"),
             Map.of("document_type", Map.of("like", "%Policy%"))
         ));
     DashScopeDocumentRetrieverOptions opts = DashScopeDocumentRetrieverOptions.builder()
         .indexName("测试知识库").searchFilters(List.of(orGroup)).build();
     DocumentRetriever retriever = new DashScopeDocumentRetriever(dashscopeApi, opts);
     ```

## 限制和注意事项

- **文件解析限制**：`DashScopeParse` 仅对 PDF/DOC/DOCX 执行智能解析（如表格识别、版面还原），TXT/MD/PPT 等格式仅作原始文本上传，且单文件 ≤100MB 或 1000 页 [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)。
- **业务空间依赖**：所有云端组件（`DashScopeCloudIndex`、`DashScopeCloudRetriever`、Spring AI Alibaba 的知识库检索）均强依赖 `DASHSCOPE_WORKSPACE_ID` 环境变量，未配置将直接报错；而 LlamaIndex 的 `DashScope` LLM 和 `DashScopeEmbedding` 可不依赖该变量。
- **模型兼容性**：OpenAI 兼容模式仅支持百炼的**文本生成类模型**（如 `qwen-plus`），不支持 Embedding、Rerank 或 Parse 等专用模型，相关能力必须使用百炼原生 SDK [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)。
- **Spring AI Alibaba 版本要求**：知识库 `searchFilters` 的嵌套 OR 条件在 Spring AI Alibaba 1.1.2.3 版本验证通过，低版本可能不支持 `_conditions` 数组嵌套语法。
- **重试与超时**：`DashScopeJsonNodeParser` 默认 `try_count_limit=10`，`DashScopeParse` 默认 `max_timeout=3600` 秒，长文档解析需预留足够时间。

## 来源文档

- [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)
- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)
- [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)
- [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)
- [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)
- [DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)
- [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)
- [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)


