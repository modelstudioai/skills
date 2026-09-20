# frameworks

百炼平台提供多框架集成能力，支持主流 LLM 应用开发框架（如 LlamaIndex、Spring AI Alibaba）快速对接百炼的模型服务、Embedding、Rerank、文档解析与云端知识库等能力。开发者可基于统一 API Key 和业务空间 ID，按需组合使用各类组件构建 RAG、Agent 或知识检索应用。

## 支持的模型/功能

百炼通过适配器封装，为不同框架提供标准化接入：

- **大语言模型（LLM）调用**：支持 `qwen-plus`、`qwen-max` 等全部文本生成模型，可通过 OpenAI-like 兼容模式或原生 DashScope 封装调用 [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)。
- **Embedding 模型**：提供 `text-embedding-v1`/`v2`/`v3` 三款向量模型，其中 `text-embedding-v3` 在 CMTEB Retrieval 任务上达 73.23 分，为当前最优 [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)。
- **Rerank 模型**：默认使用 `gte-rerank`，也支持 `gte-rerank-hybrid`，用于对检索结果重排序 [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)。
- **文档解析与切分**：`DashScopeParse` 支持 PDF/DOC/DOCX/TXT 等格式智能解析；`DashScopeJsonNodeParser` 基于通义文本切分模型实现语义感知分块，**专为配合 DashScopeParse 输出设计** [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)。
- **云端知识库服务**：`DashScopeCloudIndex` + `DashScopeCloudRetriever` 提供端到端云端索引构建与检索能力，支持自动解析、智能切分、混合检索（稠密+稀疏）及可选 Rerank [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)。

> **注意**：文档中关于 `DashScopeParse` 支持格式存在矛盾——[DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md) 明确限定仅支持 `.doc`/`.docx`/`.pdf`（≤100MB/1000页），而 [通过 DashScopeCloudIndex...](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md) 表述为支持 PDF/DOC/DOCX/TXT/MD/PPT/PPTX/XLS/XLSX，并注明“只有 PDF/DOC/DOCX 会进行智能化解析”。实际以 `DashScopeParse` 文档为准：非 PDF/DOC/DOCX 文件仅原样上传，不触发智能解析流程。

## 关键参数

| 组件 | 参数名 | 类型 | 默认值 | 说明 |
|--------|--------|------|--------|------|
| `DashScopeRerank` | `model` | string | `gte-rerank` | 可选值：`gte-rerank`, `gte-rerank-hybrid` |
| `DashScopeRerank` | `top_n` | int | `5` | 返回重排后 top-N 结果；若大于候选数则返回全部 |
| `DashScopeCloudRetriever` | `dense_similarity_top_k` / `sparse_similarity_top_k` | int | `100` | 向量/文本检索召回数量 |
| `DashScopeCloudRetriever` | `enable_reranking` | bool | `True` | 是否启用 Rerank 后处理 |
| `DashScopeCloudRetriever` | `rerank_model_name` | string | `gte-rerank-hybrid` | 与 `DashScopeRerank` 的 `model` 参数语义一致，但默认值不同 |
| `DashScopeJsonNodeParser` | `chunk_size` / `overlap_size` | int | `500` / `100` | 分块大小与重叠长度，影响语义连贯性 |
| `DashScopeParse` | `workspace` / `category_id` | string | `None` / `"default"` | 必须显式传入 `workspace`（或设环境变量 `DASHSCOPE_WORKSPACE_ID`）才能使用；`category_id` 决定文件归类 |

## 使用方式

### LlamaIndex 集成
1. **安装依赖**：按需安装对应模块，例如：
   ```bash
   pip install llama-index-core llama-index-llms-dashscope  # LLM
   pip install llama-index-embeddings-dashscope              # Embedding
   pip install llama-index-postprocessor-dashscope-rerank    # Rerank
   pip install llama-index-readers-dashscope                 # Parse
   pip install llama-index-indices-managed-dashscope         # Cloud Index
   ```
2. **配置认证**：设置环境变量 `DASHSCOPE_API_KEY`；若使用非默认业务空间，还需设置 `DASHSCOPE_WORKSPACE_ID`。
3. **初始化组件**：直接实例化对应类（如 `DashScope(model_name="qwen-max")`），或通过 `Settings` 全局注入。
4. **构建流水线**：典型 RAG 流程为 `DashScopeParse → DashScopeJsonNodeParser → DashScopeCloudIndex → DashScopeCloudRetriever → DashScopeRerank → DashScope`。

### Spring AI Alibaba 集成
- **LLM 应用调用**：适用于已发布的智能体或工作流应用，需配置 `APP_ID`、`DASHSCOPE_API_KEY`（推荐）及可选 `WORKSPACE_ID` [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)。
- **知识库检索（RAG）**：通过 `DashScopeDocumentRetriever` 关联预建知识库（`INDEX_NAME`），结合 `ChatClient` 实现[检索增强生成](../concepts/rag.md)，API Key 环境变量名为 `AI_DASHSCOPE_API_KEY` [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。

## 限制和注意事项

- **Python 版本约束**：所有 `llama-index-*` 扩展包要求 `python>=3.9,<=3.12`，超出范围可能导致安装失败或运行异常。
- **文件解析限制**：`DashScopeParse` 仅对 `.pdf`/`.doc`/`.docx` 进行智能解析，其他格式（如 `.txt`/`.md`）仅做原始内容上传，不执行版面分析或结构识别。
- **云端知识库依赖**：`DashScopeCloudIndex` 和 `DashScopeCloudRetriever` **必须指定 `DASHSCOPE_WORKSPACE_ID`**（环境变量或参数传入），否则初始化失败；该 ID 不可省略，即使使用主账号空间。
- **模型兼容性**：OpenAI-like 方式仅支持百炼的文本生成模型（如 `qwen-plus`），不支持 Embedding 或 Rerank 模型；后者需使用专用封装（如 `DashScopeEmbedding`、`DashScopeRerank`）。
- **重试与超时**：`DashScopeParse` 默认 `max_timeout=3600` 秒，大文件或高并发场景下建议显式调大；`DashScopeJsonNodeParser` 默认 `try_count_limit=10`，网络不稳定时可适度增加。

## 来源文档

- [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)
- [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)
- [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)
- [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)
- [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)
- [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)
- [DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)
- [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)
- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)


