# frameworks

百炼平台提供面向主流 AI 开发框架的深度集成能力，重点支持 LlamaIndex 和 Spring AI Alibaba 两大生态，覆盖模型调用、Embedding、文档解析、向量索引、重排序、RAG 检索与智能体应用集成等全链路能力。所有集成均基于 DashScope 统一 API 层，开发者可复用百炼的模型服务、知识库管理与推理优化能力，无需自行部署底层基础设施。

## 支持的模型/功能

百炼通过框架适配器提供以下核心能力：

- **大语言模型（LLM）调用**：支持 `qwen-plus`、`qwen-max` 等全部文本生成模型，既可通过 OpenAI 兼容模式（`api_base="https://dashscope.aliyuncs.com/compatible-mode/v1"`）调用，也可通过原生 DashScope 封装调用 [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)。
- **Embedding 模型**：提供 `text-embedding-v1`/`v2`/`v3` 三款向量模型，其中 `text-embedding-v3` 在 CMTEB Retrieval 任务上达 73.23 分，为当前最优 [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)。
- **文档智能解析（DashScopeParse）**：基于“文档智能（Document Mind）”服务，支持 PDF/DOCX/DOC 格式智能化解析（含版面分析、表格识别），其他格式（TXT/MD/PPT/XLS 等）仅原样上传 [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)。
- **文本重排序（Rerank）**：集成 `gte-rerank` 和 `gte-rerank-hybrid` 模型，支持对检索结果进行语义精排 [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)。
- **云端知识库管理（DashScopeCloudIndex）**：在百炼平台侧完成文档上传、智能切分、向量化索引构建与托管，支持增删改查操作 [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)。
- **Spring 生态集成**：提供 `spring-ai-alibaba-starter-dashscope`，支持调用百炼大模型应用（Agent 1.0 / 工作流）及检索云端知识库 [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)。

> **注意**：文档 7 明确说明“只有 PDF、DOC、DOCX 文件会进行智能化解析”，而文档 5 的 Note 中仅列出 `.doc`/`.docx`/`.pdf` 三种格式，但文档 7 的说明更完整且包含明确限制条件（100MB/1000页），应以文档 7 为准。

## 关键参数

| 组件 | 关键参数 | 说明 | 默认值 |
|--------|-----------|------|---------|
| `DashScope` (LLM) | `model_name` | 模型名称，如 `"qwen-max"` | — |
| `DashScopeEmbedding` | `model_name` | 向量模型名，如 `"text-embedding-v2"` | — |
| `DashScopeRerank` | `model`, `top_n`, `return_documents` | 排序模型、返回数量、是否返回原文 | `"gte-rerank"`, `3`, `False` |
| `DashScopeCloudRetriever` | `dense_similarity_top_k`, `enable_reranking`, `rerank_model_name`, `rerank_top_n` | 向量召回数、是否启用重排、重排模型、重排后返回数 | `100`, `True`, `"gte-rerank-hybrid"`, `5` |
| `DashScopeJsonNodeParser` | `chunk_size`, `overlap_size`, `separator`, `language` | 切分块大小、重叠长度、分隔符、语言 | `500`, `100`, `" \|,\|，\|。\|？\|！\|\n\|\?\|\!"`, `"cn"` |

## 使用方式

### LlamaIndex 集成（推荐 Python 场景）

1. **安装依赖**（按需选择）：
   ```bash
   # LLM 调用（OpenAI 兼容）
   pip install llama-index-core llama-index-llms-openai-like
   # LLM 调用（原生 DashScope）
   pip install llama-index-core llama-index-llms-dashscope
   # Embedding
   pip install llama-index-core llama-index-embeddings-dashscope
   # 文档解析与切分
   pip install llama-index-core llama-index-readers-dashscope llama-index-node-parser-dashscope
   # 云端知识库
   pip install llama-index-core llama-index-indices-managed-dashscope
   ```

2. **环境配置**（必需）：
   ```bash
   export DASHSCOPE_API_KEY=your_api_key
   export DASHSCOPE_WORKSPACE_ID=your_workspace_id  # 云端知识库/解析必需
   ```

3. **代码示例**（全局设置 + 按需实例化）：
   ```python
   from llama_index.core import Settings
   from llama_index.llms.dashscope import DashScope
   from llama_index.embeddings.dashscope import DashScopeEmbedding
   from llama_index.postprocessor.dashscope_rerank import DashScopeRerank

   # 全局默认 LLM 和 Embedding
   Settings.llm = DashScope(model_name="qwen-max")
   Settings.embed_model = DashScopeEmbedding(model_name="text-embedding-v3")

   # 构建带重排的检索引擎
   query_engine = index.as_query_engine(
       node_postprocessors=[DashScopeRerank(top_n=3)]
   )
   ```

### Spring AI Alibaba 集成（推荐 Java/Spring Boot 场景）

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
         # workspace-id: ${WORKSPACE_ID}  # 如需子空间
         agent:
           app-id: ${APP_ID}  # 调用 Agent 应用时必需
   ```

3. **调用方式**：
   - 调用大模型应用：注入 `DashScopeAgent`，传入 `Prompt` 和 `DashScopeAgentOptions.withAppId()`。
   - 检索知识库：使用 `DashScopeDocumentRetriever` 并配置 `indexName` 与 `searchFilters`（支持 `_operator: OR` 嵌套条件）[通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。

## 限制和注意事项

- **文件解析限制**：DashScopeParse 仅对 PDF/DOC/DOCX 进行智能解析；单文件 ≤100MB 或 ≤1000 页；一次最多上传 200 个文件 [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)。
- **业务空间强依赖**：所有云端知识库操作（`DashScopeCloudIndex`、`DashScopeParse`、`DashScopeCloudRetriever`）均需显式配置 `DASHSCOPE_WORKSPACE_ID` 环境变量，IDE 中需手动注入 [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)。
- **模型兼容性**：OpenAI 兼容模式仅支持文本生成类模型（如 `qwen-plus`），不支持 Embedding、Rerank 或解析类服务；调用非生成类服务必须使用对应 DashScope 原生封装。
- **Spring AI Alibaba 版本约束**：知识库 `SearchFilters` 的嵌套 `_conditions` 功能已在 `1.1.2.3` 版本验证，低版本可能不支持 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。
- **HTTP 直调 RAG API**：若选择直接调用 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/indices/rag/index/retrieve`，必须使用 `index_id`（非 `indexName`）且需显式传入 `AI_DASHSCOPE_WORKSPACE_ID`，该地址**不可**作为 `DashScopeApi` 的 `baseUrl` 配置 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。

## 来源文档

- [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)
- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)
- [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)
- [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)
- [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)
- [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)
- [DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)
- [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)


