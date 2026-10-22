# frameworks

百炼平台提供对主流 AI 开发框架的深度集成支持，重点覆盖 LlamaIndex 和 Spring AI Alibaba 两大生态，帮助开发者快速构建 RAG、智能体、知识库检索等生产级应用。所有集成均基于百炼统一的 API Key 认证体系和云端模型服务能力，无需自行部署基础设施。

## 支持的模型与功能

百炼通过官方适配器（Adapter）为 LlamaIndex 提供完整能力链路：  
- **大模型调用**：支持 `qwen-max`、`qwen-plus` 等全部文本生成模型，可通过 `DashScope` 或 `OpenAILike` 两种方式接入（[使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)）。  
- **Embedding 模型**：提供 `text-embedding-v1/v2/v3` 三款嵌入模型，其中 `v3` 在 CMTEB 检索任务上达 73.23 分，推荐用于高精度向量检索（[使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)）。  
- **文档解析与切分**：`DashScopeParse` 调用文档智能（DocMind）服务，支持 PDF/DOCX/TXT 等格式的结构化解析；`DashScopeJsonNodeParser` 基于通义文本切分模型实现语义感知分块（[DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)、[DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)）。  
- **云端知识库管理**：`DashScopeCloudIndex` 实现文件上传、智能切分、向量索引构建与更新；`DashScopeCloudRetriever` 提供稠密/稀疏混合检索、重排（Rerank）及过滤能力（[DashScopeCloudIndex（DashScopeCloudRetriever）](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)）。  
- **重排模型**：`DashScopeRerank` 集成 `gte-rerank` 和 `gte-rerank-hybrid`，支持对初检结果进行语义级精排（[DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)）。  

Spring AI Alibaba 方面，支持两类核心场景：  
- **调用百炼大模型应用**：集成智能体（Agent 1.0）和工作流（Workflow）应用，通过 `DashScopeAgent` 实现非流式/流式调用（[使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)）。  
- **检索百炼知识库**：通过 `DashScopeDocumentRetriever` 或直接 HTTP 调用 RAG API，支持 `searchFilters` 多条件组合过滤（[通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)）。

> **注意**：文档 1 明确指出“本方案将知识库部署在云端，使用默认的智能文档切分与官方向量模型，**不支持自定义文档切分方式或自定义嵌入模型**”，而文档 5 和文档 11 分别提供了 `DashScopeJsonNodeParser` 和 `DashScopeEmbedding` 的自定义能力。该矛盾表明：**云端知识库（DashScopeCloudIndex）强制使用百炼托管的切分与嵌入流程，而本地索引（VectorStoreIndex）允许完全自定义**。开发者需根据部署模式选择对应组件。

## 关键参数

| 组件 | 关键参数 | 说明 | 默认值 |
|--------|----------|------|--------|
| `DashScope` (LLM) | `model_name` | 指定调用的大模型名称，如 `"qwen-max"` | — |
| `DashScopeEmbedding` | `model_name` | 指定嵌入模型，如 `"text-embedding-v3"` | — |
| `DashScopeRerank` | `model`, `top_n`, `rerank_min_score` | 排序模型名、返回数量、分数阈值 | `"gte-rerank"`, `3`, `0.0` |
| `DashScopeCloudRetriever` | `dense_similarity_top_k`, `sparse_similarity_top_k`, `enable_reranking`, `rerank_top_n` | 向量/文本召回数、是否启用重排、重排后返回数 | `100`, `100`, `True`, `5` |
| `DashScopeParse` | `result_type`, `workspace`, `category_id` | 解析结果类型、业务空间 ID、类目 ID | `DASHSCOPE_DOCMIND`, `None`, `"default"` |
| `DashScopeJsonNodeParser` | `chunk_size`, `overlap_size`, `separator` | 切块大小、重叠大小、分隔符正则 | `500`, `100`, `" \|,\|，\|。\|？\|！\|\n\|\?\|!"` |

## 使用方式

### LlamaIndex 集成
1. **安装依赖**：按需安装对应模块，例如：
   ```bash
   pip install llama-index-llms-dashscope  # LLM
   pip install llama-index-embeddings-dashscope  # Embedding
   pip install llama-index-indices-managed-dashscope  # 云端知识库
   ```
2. **配置认证**：设置环境变量 `DASHSCOPE_API_KEY`（必选），`DASHSCOPE_WORKSPACE_ID`（子业务空间时必选）。
3. **初始化组件**：
   - 全局设置（推荐）：
     ```python
     from llama_index.core import Settings
     from llama_index.llms.dashscope import DashScope
     from llama_index.embeddings.dashscope import DashScopeEmbedding
     Settings.llm = DashScope(model_name="qwen-plus")
     Settings.embed_model = DashScopeEmbedding(model_name="text-embedding-v3")
     ```
   - 局部实例化（按需覆盖）：
     ```python
     retriever = DashScopeCloudRetriever("my_index", dense_similarity_top_k=50)
     ```

### Spring AI Alibaba 集成
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
         api-key: ${AI_DASHSCOPE_API_KEY}  # 注意：Spring AI Alibaba 使用 AI_DASHSCOPE_API_KEY
         # workspace-id: ${AI_DASHSCOPE_WORKSPACE_ID}
   ```
3. **注入并调用**：
   - 调用应用：`DashScopeAgent` + `app-id`
   - 检索知识库：`DashScopeDocumentRetriever` + `indexName` 或 `RestClient` 直调 RAG API。

## 限制和注意事项

- **文件解析限制**：`DashScopeParse` 仅对 PDF/DOC/DOCX 进行智能化解析，其他格式（如 TXT、PPTX）仅原样上传，不执行结构化解析（[DashScopeCloudIndex（DashScopeCloudRetriever）](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)）。单文件上限为 100MB 或 1000 页，一次最多上传 200 个文件。
- **云端知识库不可定制**：如前所述，`DashScopeCloudIndex` 强制使用百炼托管的文档切分与嵌入流程，无法替换为自定义逻辑（[通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)）。
- **业务空间 ID 必须显式配置**：在 Spring AI Alibaba 中，即使使用默认业务空间，HTTP 直调 RAG API 也必须提供 `AI_DASHSCOPE_WORKSPACE_ID`（[通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)）；而 LlamaIndex 的 `DashScopeCloudIndex` 在未设 `workspace_id` 时可回退至主账号空间。
- **模型兼容性**：`OpenAILike` 封装仅支持百炼的文本生成模型（非多模态），且需严格匹配 `api_base="https://dashscope.aliyuncs.com/compatible-mode/v1"`（[使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)）。
- **Python 版本要求**：所有 LlamaIndex 百炼适配器均要求 `python>=3.9,<=3.12`（见文档 3、4、5、6、7）。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)
- [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)
- [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)
- [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)
- [DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)
- [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)
- [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)
- [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)


