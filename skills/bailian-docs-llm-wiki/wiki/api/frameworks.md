# frameworks

百炼平台提供对主流 AI 开发框架的深度集成支持，重点覆盖 LlamaIndex 和 Spring AI Alibaba 两大生态，帮助开发者快速构建 RAG、智能体、工作流等生产级应用。所有集成均基于百炼统一的 API-KEY 认证体系，支持模型调用、嵌入向量化、文档解析、云端知识库管理及重排序等全链路能力。

## 支持的模型/功能

百炼通过官方适配器支持以下核心能力：

- **大语言模型（LLM）调用**：支持 `qwen-plus`、`qwen-max` 等全部文本生成模型，既可通过 OpenAI 兼容模式（`api_base="https://dashscope.aliyuncs.com/compatible-mode/v1"`）调用，也可使用原生 `DashScope` 封装 [使用百炼大模型 (raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)。
- **Embedding 模型**：提供 `text-embedding-v1`/`v2`/`v3` 三款向量模型，其中 `v3` 在 MTEB（Retrieval task）和 CMTEB（Retrieval task）两项关键指标上分别达 55.41 和 73.23，为当前最优 [使用 Embedding 模型 (raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)。
- **文档解析与切分**：`DashScopeParse` 支持 PDF/DOCX/TXT 等格式的智能解析（依赖“文档智能”服务），`DashScopeJsonNodeParser` 基于通义文本切分模型进行语义块划分，二者需配合使用。
- **云端知识库服务**：`DashScopeCloudIndex` 实现文件上传、智能解析、自动切分、向量索引构建与托管；`DashScopeCloudRetriever` 提供稠密/稀疏混合检索、GTE-Rerank 重排序等能力 [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务 (raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)。
- **Java 生态集成**：Spring AI Alibaba 提供 `DashScopeAgent`（调用智能体/工作流应用）和 `DashScopeDocumentRetriever`（检索知识库）两类核心组件，完整支持非流式与流式响应。

> **注意**：文档 2 中提到“不支持自定义文档切分方式或自定义嵌入模型”，但文档 6 和文档 3 明确提供了 `DashScopeJsonNodeParser` 和 `DashScopeEmbedding` 的自定义能力。该限制仅适用于 *通过百炼控制台 0 代码构建 RAG* 的场景，LlamaIndex 编程方式下完全支持自定义。

## 关键参数

| 组件 | 关键参数 | 说明 | 默认值 |
|--------|-----------|------|---------|
| `DashScope` (LLM) | `model_name`, `api_key` | 必填；`model_name` 需从[选择模型](raw/model-user-guide/get-started-with-models/models.md)中选取 | — |
| `DashScopeEmbedding` | `model_name` | 支持 `text-embedding-v1`/`v2`/`v3` | `text-embedding-v2` |
| `DashScopeRerank` | `model`, `top_n`, `rerank_min_score` | `model` 仅支持 `gte-rerank`；`rerank_min_score` 仅在 `enable_reranking=True` 时生效 | `gte-rerank`, `3`, `0.0` |
| `DashScopeCloudRetriever` | `dense_similarity_top_k`, `sparse_similarity_top_k`, `enable_reranking`, `rerank_model_name` | 混合检索+重排组合；`rerank_model_name` 支持 `gte-rerank-hybrid` 和 `gte-rerank` | `100`, `100`, `True`, `gte-rerank-hybrid` |
| `DashScopeParse` | `result_type`, `workspace`, `category_id` | `category_id` 决定文件归类，未设置则使用默认类目；PDF/DOCX 才触发智能解析 | `ResultType.DASHSCOPE_DOCMIND`, `None`, `"default"` |

## 使用方式

### LlamaIndex 集成（Python）

1. **安装依赖**（按需选择）：
   ```bash
   # 基础
   pip install llama-index-core
   # LLM：OpenAI 兼容模式
   pip install llama-index-llms-openai-like
   # LLM：原生 DashScope
   pip install llama-index-llms-dashscope
   # Embedding
   pip install llama-index-embeddings-dashscope
   # 文档解析
   pip install llama-index-readers-dashscope
   # 云端知识库
   pip install llama-index-indices-managed-dashscope
   # 重排序
   pip install llama-index-postprocessor-dashscope-rerank
   ```

2. **环境准备**：
   ```bash
   export DASHSCOPE_API_KEY=your_api_key
   export DASHSCOPE_WORKSPACE_ID=your_workspace_id  # 云端知识库必需
   ```

3. **典型组合示例（RAG）**：
   - 用 `DashScopeParse` 解析本地 PDF → `DashScopeCloudIndex.from_documents()` 构建云端知识库；
   - 用 `DashScopeEmbedding` + `VectorStoreIndex` 构建本地向量库；
   - 用 `DashScopeRerank` 对 `SimpleRetriever` 结果重排；
   - 全局设置 `Settings.llm` 和 `Settings.embed_model` 统一注入。

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
         # workspace-id: ${WORKSPACE_ID}  # 可选
         agent:
           app-id: ${APP_ID}  # 调用智能体/工作流必需
   ```

3. **调用方式**：
   - 智能体/工作流：注入 `DashScopeAgent`，调用 `.call(new Prompt(...))`；
   - 知识库检索：注入 `DashScopeApi`，构造 `DashScopeDocumentRetriever` 并注入 `ChatClient` 的 `DocumentRetrievalAdvisor`。

## 限制和注意事项

- **文件解析限制**：`DashScopeParse` 仅对 PDF、DOC、DOCX 进行智能解析；其他格式（如 TXT、MD）仅原样上传，不执行结构化提取 [DashScopeParse (raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)。单文件 ≤100MB 且 ≤1000 页，单次上传 ≤200 个文件。
- **业务空间强依赖**：所有云端知识库操作（`DashScopeCloudIndex`、`DashScopeCloudRetriever`）必须配置 `DASHSCOPE_WORKSPACE_ID`，否则抛出 `ValueError`；而 `DashScopeParse` 在未指定 `workspace` 时可降级至默认空间。
- **模型兼容性**：OpenAI 兼容模式仅支持文本生成类模型（如 `qwen-plus`），不支持 `text-embedding-*` 或 `gte-rerank` 等专用模型；后者必须使用对应原生封装器。
- **Spring AI Alibaba 应用类型限制**：仅支持集成 *智能体应用（Agent 1.0）* 和 *工作流应用*，不支持直接调用基础大模型 API 或知识库原生检索接口 [使用Spring AI Alibaba集成阿里云百炼大模型应用 (raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)。
- **重排序模型一致性**：`DashScopeRerank`（独立后处理器）与 `DashScopeCloudRetriever` 中的 `rerank_model_name` 参数虽同属 GTE-Rerank 系列，但前者仅支持 `gte-rerank`，后者额外支持 `gte-rerank-hybrid`，二者不可混用。

## 来源文档

- [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)
- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)
- [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)
- [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)
- [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)
- [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)
- [DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)


