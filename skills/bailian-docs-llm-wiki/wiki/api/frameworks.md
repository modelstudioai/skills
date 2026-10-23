# frameworks

百炼平台提供对主流 AI 开发框架的深度集成支持，重点覆盖 LlamaIndex 和 Spring AI Alibaba 两大生态。通过官方适配的 SDK 和插件，开发者可复用框架原生能力，同时无缝接入百炼的云端模型服务、知识库管理与 RAG 基础设施，显著降低私域知识应用的构建门槛。所有集成均基于标准 API 协议，不强制绑定特定部署模式。

## 支持的模型与功能

百炼在框架层提供三类核心能力：**大语言模型（LLM）调用**、**嵌入（Embedding）模型服务**和**重排序（Rerank）模型服务**，全部通过标准化接口封装。

- **LLM 调用**：支持 `qwen-max`、`qwen-plus` 等全量百炼文本生成模型。可通过 `DashScope`（原生）或 `OpenAILike`（兼容 OpenAI 接口）两种方式集成至 LlamaIndex；Spring AI Alibaba 则通过 `DashScopeAgent` 调用已发布的智能体/工作流应用 [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)。
- **Embedding 模型**：提供 `text-embedding-v1`/`v2`/`v3` 三个版本，其中 `v3` 在 CMTEB Retrieval 任务上达 73.23 分，为当前最优。模型通过 `DashScopeEmbedding` 封装，支持全局 `Settings.embed_model` 设置或局部传参 [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)。
- **Rerank 模型**：默认提供 `gte-rerank`，高级版支持 `gte-rerank-hybrid`。用于对向量检索结果进行语义精排，提升相关性 [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)。

此外，百炼还提供：
- **文档智能解析（DashScopeParse）**：对 PDF/DOCX 等格式执行结构化提取，输出 JSON 化逻辑树；
- **云端知识库索引（DashScopeCloudIndex）**：自动完成文档上传、智能切分、向量化与索引构建；
- **知识库检索器（DashScopeCloudRetriever）**：支持稠密/稀疏混合检索及重排，可独立使用或作为 LlamaIndex 的 `as_retriever()` 后端。

> **注意**：文档 1 明确指出“云端知识库不支持自定义文档切分方式或自定义嵌入模型”，而文档 11 的 `DashScopeJsonNodeParser` 和文档 2 的 `DashScopeEmbedding` 均允许用户在本地处理切分与嵌入——二者适用场景不同：前者用于**本地 RAG 流程**，后者用于**云端知识库托管流程**，不可混用。

## 关键参数

各组件关键参数如下，需根据实际效果调整：

| 组件 | 参数名 | 类型 | 默认值 | 说明 |
|--------|---------|------|---------|------|
| `DashScopeCloudIndex.as_query_engine()` | `similarity_top_k` | `int` | `5` | 向量检索召回数量（文档 1） |
| | `similarity_cutoff` | `float` | `0.4` | 检索结果最低相似度阈值（文档 1） |
| `DashScopeRerank` | `top_n` | `int` | `3` | 重排后返回的 Top-N 结果数（文档 3） |
| | `model` | `str` | `"gte-rerank"` | 可选 `"gte-rerank"` 或 `"gte-rerank-hybrid"`（文档 3） |
| `DashScopeCloudRetriever` | `dense_similarity_top_k` / `sparse_similarity_top_k` | `int` | `100` | 分别控制向量/关键词召回数（文档 6） |
| | `enable_reranking` | `bool` | `True` | 是否启用重排（文档 6） |
| `DashScopeJsonNodeParser` | `chunk_size` / `overlap_size` | `int` | `500` / `100` | 文本切块大小与重叠（文档 11） |

## 使用方式

### LlamaIndex 集成（Python）

1. **安装依赖**：  
   ```bash
   pip install llama-index-core llama-index-llms-dashscope llama-index-embeddings-dashscope \
              llama-index-postprocessor-dashscope-rerank llama-index-indices-managed-dashscope \
              llama-index-readers-dashscope
   ```

2. **配置认证**：  
   设置环境变量 `DASHSCOPE_API_KEY`；若使用子业务空间，还需设置 `DASHSCOPE_WORKSPACE_ID`（文档 5、6、10）。

3. **典型流程**：  
   - 本地 RAG：`DashScopeParse` → `DashScopeJsonNodeParser` → `VectorStoreIndex`（文档 10、11、2）；  
   - 云端 RAG：`DashScopeParse` → `DashScopeCloudIndex.from_documents()` → `index.as_query_engine()`（文档 1、5）；  
   - 混合增强：在 `query_engine` 中组合 `SimilarityPostprocessor` 与 `DashScopeRerank`（文档 1）。

### Spring AI Alibaba 集成（Java）

1. **添加依赖**（Maven）：  
   ```xml
   <dependency>
       <groupId>com.alibaba.cloud.ai</groupId>
       <artifactId>spring-ai-alibaba-starter-dashscope</artifactId>
       <version>1.0.0.2</version>
   </dependency>
   ```

2. **配置认证**：  
   在 `application.yml` 中设置 `spring.ai.dashscope.api-key`（推荐使用 `AI_DASHSCOPE_API_KEY` 环境变量）；子空间需额外配置 `workspace-id`（文档 8、9）。

3. **调用方式**：  
   - 调用大模型应用：注入 `DashScopeAgent`，传入 `app-id`（文档 8）；  
   - 检索知识库：使用 `DashScopeDocumentRetriever` 并配置 `indexName` 与 `searchFilters`（文档 9）。

## 限制和注意事项

- **文件解析限制**：`DashScopeParse` 仅对 PDF/DOC/DOCX 执行智能解析，其他格式（如 TXT、MD）仅原样上传，不解析结构（文档 5）。单文件上限 100MB 或 1000 页，单次上传最多 200 个文件（文档 5）。
- **云端知识库约束**：使用 `DashScopeCloudIndex` 构建的云端知识库，其文档切分策略与嵌入模型由百炼统一管理，**不支持用户自定义**（文档 1）。若需完全控制切分逻辑或嵌入模型，请采用本地 RAG 方案（文档 1、11、2）。
- **环境兼容性**：所有 Python SDK 要求 `python>=3.9,<=3.12`（文档 3、5、6、10、11）；Spring AI Alibaba 要求 `JDK 17+` 与 `Spring Boot 3.x`（文档 8、9）。
- **API Key 配置**：LlamaIndex 相关组件统一读取 `DASHSCOPE_API_KEY`；Spring AI Alibaba 默认读取 `AI_DASHSCOPE_API_KEY`（文档 8、9），二者**不可混用**，需按框架要求分别配置。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)
- [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)
- [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)
- [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)
- [DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)
- [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)
- [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)
- [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)


