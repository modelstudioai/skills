# frameworks

百炼平台提供对主流 AI 开发框架的深度集成支持，重点覆盖 LlamaIndex 和 Spring AI Alibaba 两大生态。通过官方适配的 SDK 和插件，开发者可快速将百炼的大模型、Embedding、Rerank、文档解析与云端知识库等能力嵌入现有应用架构，无需从零实现底层服务对接。

## 支持的模型/功能

百炼在框架层提供以下核心能力模块：

- **大语言模型（LLM）**：支持 `qwen-plus`、`qwen-max` 等全部文本生成模型，既可通过 OpenAI 兼容模式调用（需配置 `api_base="https://dashscope.aliyuncs.com/compatible-mode/v1"`），也可通过原生 DashScope 封装调用 [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)。
- **Embedding 模型**：提供 `text-embedding-v1`/`v2`/`v3` 三款向量模型，其中 `text-embedding-v3` 在 CMTEB Retrieval 任务上达 73.23 分，为当前最优 [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)。
- **Rerank 模型**：支持 `gte-rerank` 和 `gte-rerank-hybrid`，用于对检索结果进行语义重排序，提升 RAG 准确率 [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)。
- **文档智能解析（DocMind）**：通过 `DashScopeParse` 对 PDF/DOCX/TXT 等格式进行结构化解析，仅 PDF/DOC/DOCX 支持智能化解析，其余格式仅原样上传 [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)。
- **云端知识库服务**：支持基于 `DashScopeCloudIndex` 构建全托管知识库，并通过 `DashScopeCloudRetriever` 进行稠密/稀疏混合检索与重排 [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)。

> **注意**：文档 2 明确指出“本方案将知识库部署在云端，使用默认的智能文档切分与官方向量模型，**不支持自定义文档切分方式或自定义嵌入模型**”，而文档 11 中 `DashScopeParse` 的说明称其“支持 PDF、DOC、DOCX、TXT、MD、PPT、PPTX、XLS、XLSX 格式”，但紧接着强调“**只有 PDF、DOC、DOCX 文件会进行智能化解析，其他类型的文件只原样上传到云端，不进行解析**”。二者一致，但需注意该限制对非结构化数据处理路径的实际影响。

## 关键参数

| 组件 | 参数名 | 类型 | 默认值 | 说明 |
|--------|---------|------|---------|------|
| `DashScopeEmbedding` | `model_name` | string | `text-embedding-v2` | 可选 `text-embedding-v1`/`v2`/`v3`；推荐 `v3`（CMTEB Retrieval 73.23） |
| `DashScopeRerank` | `model` | string | `gte-rerank` | 支持 `gte-rerank` 和 `gte-rerank-hybrid`；后者融合稠密/稀疏信号 |
| `DashScopeCloudRetriever` | `dense_similarity_top_k` | int | `100` | 向量检索召回数量 |
|  | `sparse_similarity_top_k` | int | `100` | 文本检索召回数量 |
|  | `rerank_model_name` | string | `gte-rerank-hybrid` | 推荐用于混合检索场景 |
| `DashScopeJsonNodeParser` | `chunk_size` | int | `500` | 文本切分块大小（配合 `DashScopeParse` 使用） |
|  | `separator` | string | `" \|,\|，\|。\|？\|！\|\n\|\?\|\!"` | 中文分隔符正则表达式 |

## 使用方式

### LlamaIndex 生态
1. **安装依赖**：按需安装对应组件，例如：
   ```bash
   pip install llama-index-core llama-index-llms-dashscope  # LLM
   pip install llama-index-embeddings-dashscope              # Embedding
   pip install llama-index-postprocessor-dashscope-rerank    # Rerank
   pip install llama-index-readers-dashscope                 # Parse
   pip install llama-index-indices-managed-dashscope         # Cloud Index
   ```
2. **全局设置（可选）**：统一配置默认模型：
   ```python
   from llama_index.core import Settings
   from llama_index.llms.dashscope import DashScope
   from llama_index.embeddings.dashscope import DashScopeEmbedding
   Settings.llm = DashScope(model_name="qwen-max")
   Settings.embed_model = DashScopeEmbedding(model_name="text-embedding-v3")
   ```
3. **构建云端 RAG 应用**：参考 [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md) 的完整流程，包含 `DashScopeParse` → `DashScopeCloudIndex` → `DashScopeCloudRetriever` → `DashScopeRerank` 链路。

### Spring AI Alibaba 生态
1. **添加 Maven 依赖**：引入 `spring-ai-alibaba-starter-dashscope`（版本 `1.0.0.2` 或更高）。
2. **配置环境变量**：`DASHSCOPE_API_KEY`、`APP_ID`（应用集成）、`AI_DASHSCOPE_API_KEY`（知识库检索）、`WORKSPACE_ID`（子空间必需）。
3. **两种集成路径**：
   - **应用集成**：使用 `DashScopeAgent` 调用已发布的智能体或工作流应用 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)；
   - **知识库检索**：使用 `DashScopeDocumentRetriever` 或直调 RAG API 实现检索增强问答 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。

## 限制和注意事项

- **文件解析限制**：`DashScopeParse` 仅对 `.pdf`、`.doc`、`.docx` 执行智能解析（如表格识别、公式提取、版面还原），其余格式（如 `.txt`、`.md`）仅做原始文本上传，不触发 DocMind 引擎 [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)。
- **业务空间强制要求**：所有云端操作（`DashScopeCloudIndex`、`DashScopeCloudRetriever`、Spring AI Alibaba 的知识库检索）均**必须配置 `DASHSCOPE_WORKSPACE_ID`**，即使使用主账号默认空间；IDE 用户需手动将该变量注入运行环境 [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)。
- **模型兼容性**：OpenAI 兼容模式仅支持百炼的**文本生成类模型**（如 `qwen-plus`），不支持 Embedding、Rerank 或解析类服务；调用前务必核对 [OpenAI 兼容模式支持的模型列表](https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope#eadfc13038jd5)。
- **Spring AI Alibaba 版本约束**：知识库 `SearchFilters` 的嵌套 `_conditions` 功能已在 `1.1.2.3` 版本验证，低版本可能不支持复杂过滤语法 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。

## 来源文档

- [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)
- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)
- [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)
- [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)
- [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)
- [DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)
- [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)
- [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)


