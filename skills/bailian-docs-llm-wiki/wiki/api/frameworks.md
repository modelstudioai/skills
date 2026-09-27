# frameworks

百炼平台提供多套主流 AI 开发框架的官方集成支持，重点覆盖 LlamaIndex 和 Spring AI Alibaba 两大生态。通过标准化 SDK 和适配器，开发者可快速将百炼的 Embedding、大模型、文档解析、重排、云端知识库等能力嵌入到 RAG、Agent、知识检索等应用中，无需自行封装 HTTP 请求或管理底层协议。

## 支持的模型与功能

百炼在框架集成中提供以下核心能力：

- **Embedding 模型**：支持 `text-embedding-v1`/`v2`/`v3`，其中 `text-embedding-v3` 在 CMTEB (Retrieval task) 上达 73.23 分，为当前最优 [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)；  
- **大语言模型（LLM）**：支持全部百炼文本生成模型（如 `qwen-plus`、`qwen-max`），既可通过 OpenAI-like 兼容模式调用，也可通过原生 DashScope 封装调用 [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)；  
- **文档智能解析（Parse）**：基于“文档智能（Document Mind）”服务，支持 PDF/DOCX/DOC 等格式的结构化解析，但仅对 PDF/DOC/DOCX 执行智能化解析，其余格式（如 TXT、MD）仅原样上传 [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)；  
- **文本重排（Rerank）**：提供 `gte-rerank` 和 `gte-rerank-hybrid` 模型，用于对初检结果进行语义精排；  
- **云端知识库管理**：通过 `DashScopeCloudIndex` 实现文件上传、智能切分、向量索引构建与托管检索，支持增量更新与跨应用复用；  
- **Spring 生态集成**：支持通过 Spring AI Alibaba 调用百炼大模型应用（Agent/Workflow）及云端知识库，适用于 Java 企业级开发场景。

> **注意**：文档中关于 `DashScopeParse` 支持格式的描述存在不一致。[DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md) 明确说明“目前只支持 .doc、.docx、.pdf”，而 [通过 DashScopeCloudIndex...](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md) 则称支持 “PDF、DOC、DOCX、TXT、MD、PPT、PPTX、XLS、XLSX”，并补充说明“**只有 PDF、DOC、DOCX 文件会进行智能化解析，其他类型的文件只原样上传到云端，不进行解析**”。该补充说明更准确，应以之为准。

## 关键参数

| 组件 | 参数名 | 类型 | 默认值 | 说明 |
|--------|---------|------|---------|------|
| `DashScopeEmbedding` | `model_name` | string | — | 必填，取值为 `text-embedding-v1`/`v2`/`v3` |
| `DashScope` (LLM) | `model_name` | string | — | 必填，如 `qwen-plus`、`qwen-max` |
| `DashScopeRerank` | `model` | string | `gte-rerank` | 可选 `gte-rerank` 或 `gte-rerank-hybrid`（后者仅在 `DashScopeCloudRetriever` 中支持） |
| `DashScopeCloudRetriever` | `enable_reranking` | bool | `True` | 是否启用重排；若设为 `False`，则忽略 `rerank_model_name` 等重排参数 |
| `DashScopeCloudRetriever` | `rerank_model_name` | string | `gte-rerank-hybrid` | 注意：`gte-rerank-hybrid` 仅在 `DashScopeCloudRetriever` 中可用，`DashScopeRerank` 独立使用时仅支持 `gte-rerank` |
| `DashScopeJsonNodeParser` | `language` | string | `cn` | 接受 `"cn"`（中文）、`"en"`（英文）、`"any"`；`"any"` 模式性能显著下降 |

## 使用方式

### LlamaIndex 集成（Python）

1. **安装依赖**（按需组合）：
   ```bash
   pip install llama-index-core
   # Embedding
   pip install llama-index-embeddings-dashscope
   # LLM（二选一）
   pip install llama-index-llms-dashscope          # 原生方式
   pip install llama-index-llms-openai-like       # OpenAI 兼容方式
   # 文档解析与切分
   pip install llama-index-readers-dashscope
   pip install llama-index-node-parser-dashscope
   # 云端知识库
   pip install llama-index-indices-managed-dashscope
   # 重排
   pip install llama-index-postprocessor-dashscope-rerank
   ```

2. **环境配置**（必需）：
   ```bash
   export DASHSCOPE_API_KEY=your_api_key
   export DASHSCOPE_WORKSPACE_ID=your_workspace_id  # 如使用非默认业务空间
   ```

3. **典型流程示例**（RAG）：
   - 使用 `DashScopeParse` 解析本地 PDF/DOCX → 得到 `Document` 对象；
   - 使用 `DashScopeJsonNodeParser` 切分（可选，云端自动切分时可跳过）；
   - 调用 `DashScopeCloudIndex.from_documents()` 上传并构建云端索引；
   - 用 `DashScopeCloudIndex("my_index").as_retriever()` 初始化检索器；
   - 配合 `DashScopeRerank` 后处理器或直接启用 `enable_reranking=True` 进行重排；
   - 最终接入 `Settings.llm = DashScope(model_name="qwen-max")` 完成 RAG 流水线。

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
         api-key: ${DASHSCOPE_API_KEY}  # 或 ${AI_DASHSCOPE_API_KEY}（知识库场景）
         # workspace-id: ${WORKSPACE_ID}  # 可选
         agent:
           app-id: ${APP_ID}            # Agent/Workflow 应用 ID
   ```

3. **调用方式**：
   - **调用大模型应用**：注入 `DashScopeAgent`，传入 `Prompt` 和 `DashScopeAgentOptions.withAppId(...)`；
   - **检索知识库**：使用 `DashScopeDocumentRetriever` + `DocumentRetrievalAdvisor`，自动完成检索+上下文注入+大模型生成。

## 限制和注意事项

- **文件解析限制**：`DashScopeParse` 单文件上限为 **100 MB 或 1000 页**，一次最多上传 **200 个文件**；仅 PDF/DOC/DOCX 触发智能解析，TXT/MD/PPT 等格式仅原样上传 [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)；  
- **云端知识库依赖业务空间**：`DashScopeCloudIndex` 和 `DashScopeCloudRetriever` **必须配置 `DASHSCOPE_WORKSPACE_ID`**，否则初始化失败；IDE 用户需手动将该变量注入运行环境；  
- **重排模型差异**：独立使用的 `DashScopeRerank` 仅支持 `gte-rerank`；而 `DashScopeCloudRetriever` 支持 `gte-rerank-hybrid`（混合稠密+稀疏信号），效果更优，但不可在 `DashScopeRerank` 中直接指定；  
- **Spring AI Alibaba 环境变量命名不统一**：LLM 应用调用推荐用 `DASHSCOPE_API_KEY`，而知识库检索示例中使用 `AI_DASHSCOPE_API_KEY`；建议在工程中统一映射或通过 `@Value("${DASHSCOPE_API_KEY:${AI_DASHSCOPE_API_KEY}}")` 兼容；  
- **LlamaIndex 版本兼容性**：所有百炼 LlamaIndex 包要求 `python>=3.9,<=3.12`，且需匹配 `llama-index-core` 主版本（建议使用最新稳定版）。

## 来源文档

- [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)
- [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)
- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)
- [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)
- [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)
- [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)
- [DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)


