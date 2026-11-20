# frameworks

阿里云百炼平台提供多套主流 AI 开发框架的官方集成支持，重点覆盖 LlamaIndex 和 Spring AI Alibaba 两大生态。开发者可基于这些框架快速构建 RAG 应用、调用大模型服务、管理云端知识库及嵌入式检索能力，无需从零实现底层基础设施。所有集成均通过标准化 SDK 封装，统一使用 DashScope API Key 进行鉴权。

## 支持的模型与功能

百炼在框架层支持以下核心能力：

- **大模型调用**：通过 `DashScope` 或 `OpenAILike` LLM 封装，调用全部百炼文本生成模型（如 `qwen-max`、`qwen-plus`），支持流式/非流式响应。详见 [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)。
- **Embedding 模型**：提供 `text-embedding-v1`/`v2`/`v3` 等多版本向量模型，兼容 MTEB/CMTEB 评估标准，适用于构建本地向量索引。[使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md) 文档列出了各模型的量化指标。
- **文档智能解析**：`DashScopeParse` 支持 PDF/DOCX/DOC 格式文件的结构化解析（基于文档智能 DocMind 服务），但仅对这三类格式执行智能化解析；其余格式（如 TXT、MD）仅原样上传，不进行语义切分或布局识别。
- **云端知识库管理**：`DashScopeCloudIndex` 实现端到端云端知识库构建（含上传、智能切分、索引）、检索与更新，支持 `DashScopeCloudRetriever` 进行稠密/稀疏混合检索及重排。
- **重排序（Rerank）**：`DashScopeRerank` 集成 `gte-rerank` 系列模型，用于对初检结果进行语义相关性重打分与截断。
- **Spring 生态集成**：`Spring AI Alibaba` 提供 `DashScopeAgent`（调用百炼应用）和 `DashScopeDocumentRetriever`（检索知识库）两类核心组件，深度适配 Spring Boot 3.x + JDK 17+ 环境。

> **注意**：文档 1 明确指出“本方案将知识库部署在云端，使用默认的智能文档切分与官方向量模型，**不支持自定义文档切分方式或自定义嵌入模型**”，而文档 5 的 `DashScopeJsonNodeParser` 和文档 3 的 `DashScopeEmbedding` 均允许用户指定切分策略与 embedding 模型。该矛盾表明：**云端知识库（DashScopeCloudIndex）强制使用百炼托管的切分与 embedding 流程，不可替换；而本地向量索引（VectorStoreIndex）则完全开放自定义能力**。

## 关键参数

| 组件 | 参数名 | 类型 | 默认值 | 说明 |
|--------|---------|------|---------|------|
| `DashScopeCloudRetriever` | `dense_similarity_top_k` | `int` | `100` | 向量检索召回数量 |
| `DashScopeCloudRetriever` | `enable_reranking` | `bool` | `True` | 是否启用重排（默认开启） |
| `DashScopeCloudRetriever` | `rerank_model_name` | `str` | `gte-rerank-hybrid` | 重排模型，支持 `gte-rerank-hybrid` / `gte-rerank` |
| `DashScopeRerank` | `top_n` | `int` | `3` | 重排后返回的 top 文档数 |
| `DashScopeJsonNodeParser` | `chunk_size` | `int` | `500` | 文本块大小（字符数） |
| `DashScopeJsonNodeParser` | `separator` | `str` | `" \|,\|，\|。\|？\|！\|\n\|\?\|\!"` | 中文常用分隔符正则表达式 |

## 使用方式

### LlamaIndex 集成（Python）

1. **安装依赖**  
   ```bash
   # 基础 + 大模型
   pip install llama-index-core llama-index-llms-dashscope
   # 或 OpenAI 兼容模式
   pip install llama-index-llms-openai-like
   # Embedding
   pip install llama-index-embeddings-dashscope
   # 文档解析与云端索引
   pip install llama-index-readers-dashscope llama-index-indices-managed-dashscope
   ```

2. **初始化 LLM/Embedding**（全局设置或实例化）  
   ```python
   from llama_index.llms.dashscope import DashScope
   from llama_index.embeddings.dashscope import DashScopeEmbedding

   Settings.llm = DashScope(model_name="qwen-plus")
   Settings.embed_model = DashScopeEmbedding(model_name="text-embedding-v3")
   ```

3. **构建云端知识库**（需配置 `DASHSCOPE_WORKSPACE_ID`）  
   ```python
   from llama_index.readers.dashscope import DashScopeParse
   from llama_index.indices.managed.dashscope import DashScopeCloudIndex

   documents = DashScopeParse().load_data(file_path=["./docs/sample.pdf"])
   index = DashScopeCloudIndex.from_documents(documents, name="my_kb")
   ```

4. **检索与 RAG**  
   ```python
   retriever = index.as_retriever()
   nodes = retriever.retrieve("产品参数有哪些？")

   # 或结合重排
   from llama_index.postprocessor.dashscope_rerank import DashScopeRerank
   postprocessor = DashScopeRerank(top_n=3, model="gte-rerank")
   reranked = postprocessor.postprocess_nodes(nodes, query_str="产品参数")
   ```

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
         # workspace-id: ${WORKSPACE_ID} # 可选
         agent:
           app-id: ${APP_ID} # 调用应用时必需
   ```

3. **调用知识库检索**（使用 `DashScopeDocumentRetriever`）  
   ```java
   DashScopeDocumentRetrieverOptions opts = DashScopeDocumentRetrieverOptions.builder()
       .indexName("测试知识库")
       .searchFilters(List.of(Map.of("_operator", "OR", "_conditions", List.of(...))))
       .build();
   DocumentRetriever retriever = new DashScopeDocumentRetriever(dashscopeApi, opts);
   ```

## 限制和注意事项

- **文件解析限制**：`DashScopeParse` 仅对 `.pdf`、`.doc`、`.docx` 文件执行智能解析（提取表格、标题、段落结构等），其他格式（如 `.txt`、`.md`）仅做原始文本上传，**不进行任何语义切分或格式还原**。单文件上限为 100MB 或 1000 页，一次最多上传 200 个文件。
- **业务空间强依赖**：所有云端操作（`DashScopeCloudIndex`、`DashScopeCloudRetriever`、Spring AI Alibaba 的知识库检索）**必须配置 `DASHSCOPE_WORKSPACE_ID`**。若未设置，运行时将抛出明确异常（见文档 6 和 7），而非静默降级。
- **模型选择约束**：`DashScopeCloudIndex` 构建的云端知识库**固定使用百炼托管的 embedding 模型与切分策略，无法通过参数覆盖**；如需自定义切分或 embedding，请改用 `VectorStoreIndex` + `DashScopeEmbedding` 构建本地索引（见 [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)）。
- **Spring AI Alibaba 版本兼容性**：知识库检索的 `searchFilters` 嵌套语法（如 `_operator: OR`）在 `1.1.2.3` 版本验证通过，低版本可能不支持。建议始终使用文档 11 所标注的已验证版本。
- **API Key 配置方式**：所有 SDK 均优先读取环境变量 `DASHSCOPE_API_KEY`。若同时配置了 `AI_DASHSCOPE_API_KEY`（Spring AI Alibaba 示例中使用），需确保与 SDK 期望的变量名一致，否则鉴权失败。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)
- [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)
- [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)
- [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)
- [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)
- [DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)
- [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)
- [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)


