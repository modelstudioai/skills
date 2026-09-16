# frameworks

百炼平台提供对主流 AI 开发框架的深度集成支持，当前重点覆盖 LlamaIndex 和 Spring AI Alibaba 两大生态。通过官方适配的 SDK 和插件，开发者可快速将百炼的模型服务、知识库、智能文档解析等能力嵌入现有工作流，无需从零构建基础设施。所有集成均基于标准 API 封装，保持框架原生体验的同时，复用百炼的云端算力与数据管理能力。

## 支持的模型/功能

百炼在框架层提供以下核心能力模块：

- **大语言模型（LLM）调用**：支持 `qwen-max`、`qwen-plus` 等全系列百炼文本生成模型，可通过 `DashScope` 或 `OpenAILike` 两种方式接入 LlamaIndex；Spring AI Alibaba 则通过 `DashScopeAgent` 调用智能体/工作流应用，或通过 `DashScopeApi` 驱动 RAG 流程 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。
- **嵌入模型（Embedding）**：提供 `text-embedding-v1`/`v2`/`v3` 三款向量模型，已在 MTEB、CMTEB 等权威评测中验证效果，适用于构建本地向量索引 [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)。
- **重排序模型（Rerank）**：集成 `gte-rerank` 及 `gte-rerank-hybrid`，用于对初步检索结果进行语义精排，提升相关性。
- **智能文档解析与切分**：`DashScopeParse` 支持 PDF/DOCX/DOC 格式智能化解析（提取结构化文本、表格、公式等），`DashScopeJsonNodeParser` 提供基于通义模型的语义切分能力，替代传统规则切分 [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)。
- **云端知识库服务**：`DashScopeCloudIndex` 和 `DashScopeCloudRetriever` 实现端到端云端知识库构建与检索，自动完成文档上传、智能切分、向量化、索引构建与混合检索（稠密+稀疏）。

> **注意**：文档 1 明确指出“本方案将知识库部署在云端，使用默认的智能文档切分与官方向量模型，**不支持自定义文档切分方式或自定义嵌入模型**”，而文档 5 和文档 2 分别提供了 `DashScopeJsonNodeParser` 和 `DashScopeEmbedding` 用于**本地**自定义切分与嵌入。二者适用场景不同，非矛盾，但需注意部署模式差异。

## 关键参数

| 组件 | 参数名 | 类型 | 默认值 | 说明 |
|--------|---------|------|---------|------|
| `DashScopeEmbedding` | `model_name` | string | `text-embedding-v2` | 可选值：`text-embedding-v1`/`v2`/`v3`，影响向量质量与延迟 |
| `DashScopeRerank` | `top_n`, `model` | int, string | `5`, `gte-rerank` | `model` 可选 `gte-rerank-hybrid`（文档 8）；`top_n` 控制返回结果数 |
| `DashScopeCloudRetriever` | `dense_similarity_top_k`, `sparse_similarity_top_k`, `enable_reranking` | int, int, bool | `100`, `100`, `True` | 混合检索召回数量及是否启用重排；`rerank_min_score`（float, `0.0`）用于后置分数过滤 |
| `DashScopeJsonNodeParser` | `chunk_size`, `overlap_size`, `separator` | int, int, string | `500`, `100`, `" \|,\|，\|。\|？\|！\|\n\|\?\|\!"` | 控制文本切分粒度与边界识别逻辑 |

## 使用方式

### LlamaIndex 集成（推荐 Python 生态）

1. **安装依赖**  
   ```bash
   # 基础 + LLM
   pip install llama-index-core llama-index-llms-dashscope
   # Embedding
   pip install llama-index-embeddings-dashscope
   # 文档解析与云端索引
   pip install llama-index-readers-dashscope llama-index-indices-managed-dashscope
   # 重排
   pip install llama-index-postprocessor-dashscope-rerank
   ```

2. **全局配置（可选）**  
   ```python
   from llama_index.core import Settings
   from llama_index.llms.dashscope import DashScope
   from llama_index.embeddings.dashscope import DashScopeEmbedding

   Settings.llm = DashScope(model_name="qwen-plus")
   Settings.embed_model = DashScopeEmbedding(model_name="text-embedding-v3")
   ```

3. **典型流程**  
   - 本地构建索引：用 `DashScopeParse` 解析文件 → `DashScopeJsonNodeParser` 切分 → `VectorStoreIndex.from_documents()` 构建向量库  
   - 云端构建索引：用 `DashScopeParse` 解析 → `DashScopeCloudIndex.from_documents()` 直接创建云端知识库  
   - 检索增强：`index.as_query_engine()` 配置 `SimilarityPostprocessor` + `DashScopeRerank` 后处理器  

### Spring AI Alibaba 集成（推荐 Java 生态）

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
         # workspace-id: ${WORKSPACE_ID} # 子空间时启用
         agent:
           app-id: ${APP_ID} # 调用智能体/工作流
   ```

3. **Java 调用示例**  
   - 调用大模型应用：注入 `DashScopeAgent`，调用 `agent.call(new Prompt(...))`  
   - 检索知识库：使用 `DashScopeDocumentRetriever` + `DocumentRetrievalAdvisor` 构建 RAG 流程 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)

## 限制和注意事项

- **文件解析限制**：`DashScopeParse` 仅对 `.pdf`、`.docx`、`.doc` 进行**智能化解析**（提取结构、表格等），其他格式（如 `.txt`、`.md`）仅原样上传，不触发智能处理 [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)。
- **业务空间强依赖**：所有云端操作（`DashScopeCloudIndex`、`DashScopeCloudRetriever`、Spring AI Alibaba 的知识库检索）**必须配置 `DASHSCOPE_WORKSPACE_ID`**，且该 ID 需与目标知识库/应用所属空间一致；未配置将直接报错（文档 7、8、10、11 均强调此点）。
- **Python 版本要求**：所有 `llama-index-*` 插件要求 `python>=3.9,<=3.12`（文档 4、5、6、7、8 明确声明），超出范围可能引发兼容性问题。
- **API Key 安全**：严禁硬编码 `DASHSCOPE_API_KEY`，必须通过环境变量（如 `os.environ["DASHSCOPE_API_KEY"]`）或配置中心注入，Spring 生态推荐使用 `${DASHSCOPE_API_KEY}` 占位符 [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)
- [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)
- [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)
- [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)
- [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)
- [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)
- [DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)
- [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)


