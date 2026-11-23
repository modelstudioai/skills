# frameworks

百炼平台提供对主流 AI 开发框架的深度集成支持，当前重点覆盖 LlamaIndex 和 Spring AI Alibaba 两大生态。通过官方适配的 SDK 和插件，开发者可复用框架原生能力（如文档解析、向量索引、检索增强、智能体编排），同时无缝对接百炼的云端模型服务、知识库管理与 RAG 基础设施。所有集成均基于标准 API 封装，不依赖私有协议。

## 支持的模型与功能

百炼在框架中提供以下核心能力模块：

- **大模型调用**：支持全部百炼文本生成模型（如 `qwen-max`、`qwen-plus`），可通过 `DashScope` 或 OpenAI-like 封装两种方式接入 LlamaIndex；Spring AI Alibaba 则通过 `DashScopeAgent` 调用已部署的智能体应用或工作流应用 [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)。
- **Embedding 模型**：提供 `text-embedding-v1`/`v2`/`v3` 系列嵌入模型，支持 MTEB/CMTEB 高分评估，适用于构建本地向量索引 [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)。
- **智能文档解析**：`DashScopeParse` 基于“文档智能（Document Mind）”服务，支持 PDF/DOCX/DOC 格式智能化解析（含版面分析、表格识别），其他格式仅原样上传 [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)。
- **云端知识库与检索**：`DashScopeCloudIndex` 和 `DashScopeCloudRetriever` 实现端到端云端知识库构建与检索，内置智能切分、向量索引、混合检索（稠密+稀疏）及重排能力，无需自建向量数据库。
- **重排（Rerank）**：`DashScopeRerank` 提供 `gte-rerank` 系列模型，用于对初检结果进行语义级精排，提升 Top-K 相关性 [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)。
- **文本切分**：`DashScopeJsonNodeParser` 专为 `DashScopeParse` 解析结果设计，支持按中文标点与换行符智能分块，可配置 chunk_size、overlap 及语言模式。

> **注意**：文档 1 明确指出“本方案将知识库部署在云端，使用默认的智能文档切分与官方向量模型，**不支持自定义文档切分方式或自定义嵌入模型**”，而文档 6 和文档 3 分别提供了 `DashScopeJsonNodeParser` 和 `DashScopeEmbedding` 用于本地自定义切分与嵌入。二者适用场景不同——前者面向云端全托管知识库，后者面向本地索引构建，不存在功能冲突，但需根据部署模式明确选择。

## 关键参数

| 组件 | 关键参数 | 说明 | 默认值 |
|--------|-----------|------|---------|
| `DashScope` (LLM) | `model_name` | 指定调用的百炼模型，如 `"qwen-max"` | — |
| `DashScopeEmbedding` | `model_name` | 指定嵌入模型，如 `"text-embedding-v2"` | `"text-embedding-v2"` |
| `DashScopeCloudIndex.from_documents()` | `name` | 云端知识库名称 | — |
| `DashScopeCloudRetriever` | `dense_similarity_top_k`, `sparse_similarity_top_k` | 向量/关键词召回数量 | `100` |
| | `enable_reranking`, `rerank_top_n` | 是否启用重排及返回数量 | `True`, `5` |
| | `rerank_model_name` | 重排模型，支持 `"gte-rerank-hybrid"`（推荐）和 `"gte-rerank"` | `"gte-rerank-hybrid"` |
| `DashScopeRerank` | `top_n` | 重排后返回的 Top 文档数 | `3` |
| `DashScopeJsonNodeParser` | `chunk_size`, `overlap_size`, `separator` | 分块大小、重叠长度、切分符正则 | `500`, `100`, `" \|,\|，\|。\|？\|！\|\n\|\?\|\!"` |

## 使用方式

### LlamaIndex 集成（Python）

1. **安装依赖**：按需安装对应组件，例如：
   ```bash
   pip install llama-index-core llama-index-llms-dashscope  # LLM
   pip install llama-index-embeddings-dashscope              # Embedding
   pip install llama-index-readers-dashscope                 # DashScopeParse
   pip install llama-index-indices-managed-dashscope         # DashScopeCloudIndex
   ```

2. **初始化与调用**：
   - 全局设置（可选）：
     ```python
     from llama_index.core import Settings
     from llama_index.llms.dashscope import DashScope
     Settings.llm = DashScope(model_name="qwen-plus")
     ```
   - 构建云端知识库：
     ```python
     from llama_index.indices.managed.dashscope import DashScopeCloudIndex
     index = DashScopeCloudIndex.from_documents(documents, name="my_kb")
     ```
   - 构建本地向量索引：
     ```python
     from llama_index.embeddings.dashscope import DashScopeEmbedding
     from llama_index.core import VectorStoreIndex
     index = VectorStoreIndex.from_documents(
         documents,
         embed_model=DashScopeEmbedding(model_name="text-embedding-v3")
     )
     ```

### Spring AI Alibaba 集成（Java）

1. **添加依赖**（`pom.xml`）：
   ```xml
   <dependency>
       <groupId>com.alibaba.cloud.ai</groupId>
       <artifactId>spring-ai-alibaba-starter-dashscope</artifactId>
       <version>1.0.0.2</version>
   </dependency>
   ```

2. **配置参数**（`application.yml`）：
   ```yaml
   spring:
     ai:
       dashscope:
         agent:
           app-id: ${APP_ID}  # 智能体/工作流应用ID
         api-key: ${DASHSCOPE_API_KEY}
         # workspace-id: ${WORKSPACE_ID}  # 子空间时必填
   ```

3. **调用应用或知识库**：
   - 调用大模型应用：注入 `DashScopeAgent` 并调用 `agent.call(prompt)`。
   - 检索知识库：使用 `DashScopeDocumentRetriever` 配合 `DocumentRetrievalAdvisor`，支持 `searchFilters` 过滤 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。

## 限制和注意事项

- **文件解析限制**：`DashScopeParse` 仅对 `.pdf`、`.docx`、`.doc` 进行智能化解析；`.txt`、`.md` 等格式仅原样上传，不提取结构化内容（见文档 7）。
- **云端知识库约束**：使用 `DashScopeCloudIndex` 时，文档切分、嵌入、索引均由百炼云端自动完成，**不开放自定义切分逻辑或嵌入模型替换**（见文档 1）。
- **环境变量要求**：所有百炼 SDK 均依赖 `DASHSCOPE_API_KEY`；若使用子业务空间，必须配置 `DASHSCOPE_WORKSPACE_ID`（文档 7、文档 10、文档 8 均强调此点）。
- **模型兼容性**：OpenAI-like 封装仅支持百炼的文本生成模型（非多模态、非推理专用模型），完整支持列表以 [OpenAI 兼容模式支持的模型列表](https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope#eadfc13038jd5) 为准（见文档 2）。
- **重排模型差异**：`DashScopeRerank`（文档 4）默认模型为 `gte-rerank`，而 `DashScopeCloudRetriever`（文档 10）默认为 `gte-rerank-hybrid`，后者融合了稠密与稀疏信号，效果更优，建议优先使用后者。

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


