# frameworks

百炼平台提供对主流 AI 开发框架的原生集成支持，重点覆盖 LlamaIndex 和 Spring AI Alibaba 两大生态，帮助开发者快速构建 RAG、智能体、工作流等生产级应用。所有集成均通过官方 SDK 封装，统一使用 `DASHSCOPE_API_KEY`（或 `AI_DASHSCOPE_API_KEY`）进行认证，并深度对接百炼的云端知识库、大模型服务与文档智能能力。

## 支持的模型/功能

- **大模型调用**：支持全部百炼文本生成模型（如 `qwen-max`、`qwen-plus`），可通过 LlamaIndex 的 `DashScope` 或 `OpenAILike` LLM 封装器调用；Spring AI Alibaba 则通过 `DashScopeAgent` 调用已发布的智能体/工作流应用 [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)。
- **Embedding 模型**：支持 `text-embedding-v1`/`v2`/`v3`，其中 `v3` 在 CMTEB Retrieval 任务上达 73.23 分，推荐用于高精度语义检索 [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)。
- **重排序（Rerank）**：提供 `gte-rerank` 和 `gte-rerank-hybrid` 模型，用于对初始检索结果进行语义精排，提升 Top-K 相关性。
- **文档解析与切分**：`DashScopeParse` 支持 PDF/DOCX/DOC 智能解析（基于文档智能 DocMind），`DashScopeJsonNodeParser` 提供基于通义文本切分模型的结构化分块能力。
- **云端知识库管理**：`DashScopeCloudIndex` 实现端到端的“上传→解析→切分→索引→检索”闭环，无需本地向量存储 [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)。
- **Java 生态集成**：Spring AI Alibaba 提供 `DashScopeAgent`（调用大模型应用）和 `DashScopeDocumentRetriever`（检索知识库）两类核心组件，适配 Spring Boot 3.x + JDK 17+。

> **注意**：文档 1 明确指出“本方案将知识库部署在云端，使用默认的智能文档切分与官方向量模型，**不支持自定义文档切分方式或自定义嵌入模型**”，而文档 7 和文档 6 却分别提供了 `DashScopeJsonNodeParser` 和 `DashScopeEmbedding` 的自定义配置能力。实际开发中，若需完全自定义切分逻辑或 Embedding 模型，应避免使用 `DashScopeCloudIndex.from_documents()` 的全自动流程，转而采用 `DashScopeParse` + `DashScopeJsonNodeParser` + `VectorStoreIndex` 的组合方式构建本地索引。

## 关键参数

| 组件 | 参数名 | 类型 | 默认值 | 说明 |
|--------|---------|------|---------|------|
| `DashScopeLLM` | `model_name` | string | — | 必填，如 `"qwen-max"`；完整列表见 [选择模型](raw/model-user-guide/get-started-with-models/models.md) |
| `DashScopeEmbedding` | `model_name` | string | `"text-embedding-v2"` | 推荐显式指定，`v3` 效果最优 |
| `DashScopeRerank` | `top_n`, `model` | int, string | `5`, `"gte-rerank"` | `model` 可选 `"gte-rerank-hybrid"`（混合稠密/稀疏检索） |
| `DashScopeCloudRetriever` | `dense_similarity_top_k`, `enable_reranking`, `rerank_top_n` | int, bool, int | `100`, `True`, `5` | 控制召回数量与重排行为；`rerank_min_score` 可过滤低分节点 |
| `DashScopeJsonNodeParser` | `chunk_size`, `overlap_size`, `separator` | int, int, string | `500`, `100`, `" \|,\|，\|。\|？\|！\|\n\|\?\|\!"` | 中文场景建议保留默认分隔符 |

## 使用方式

### LlamaIndex 集成（Python）
1. **安装依赖**：
   ```bash
   # 基础 + 大模型
   pip install llama-index-core llama-index-llms-dashscope
   # Embedding
   pip install llama-index-embeddings-dashscope
   # 文档解析与云端索引
   pip install llama-index-readers-dashscope llama-index-indices-managed-dashscope
   ```

2. **全局设置（可选）**：
   ```python
   from llama_index.core import Settings
   from llama_index.llms.dashscope import DashScope
   from llama_index.embeddings.dashscope import DashScopeEmbedding

   Settings.llm = DashScope(model_name="qwen-plus")
   Settings.embed_model = DashScopeEmbedding(model_name="text-embedding-v3")
   ```

3. **典型流程**：
   - 解析文件：`DashScopeParse().load_data(file_path=["a.pdf"])`
   - 切分文本：`DashScopeJsonNodeParser().parse_nodes(documents)`
   - 构建索引：`VectorStoreIndex.from_documents(..., embed_model=...)`（本地） 或 `DashScopeCloudIndex.from_documents(...)`（云端）
   - 检索问答：`index.as_query_engine(...).query("问题")`

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
         # agent: { app-id: ${APP_ID} }  # 调用应用时启用
         # workspace-id: ${WORKSPACE_ID}  # 子空间时启用
   ```

3. **核心调用**：
   - 调用大模型应用：注入 `DashScopeAgent`，调用 `agent.call(new Prompt(...))`
   - 检索知识库：使用 `DashScopeDocumentRetriever` 作为 `DocumentRetriever`，结合 `ChatClient` 构建 RAG 流程。

## 限制和注意事项

- **文件解析限制**：`DashScopeParse` 仅对 PDF/DOC/DOCX 进行智能解析（提取表格、公式、版面结构），TXT/MD/PPT 等格式仅原样上传，不解析 [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)。
- **业务空间强制要求**：`DashScopeCloudIndex` 和 `DashScopeCloudRetriever` **必须**配置 `DASHSCOPE_WORKSPACE_ID` 环境变量，否则初始化失败；Spring AI Alibaba 对知识库检索也要求 `AI_DASHSCOPE_WORKSPACE_ID`（子空间场景）。
- **模型兼容性**：`OpenAILike` 封装仅支持百炼的文本生成模型（非多模态），且需显式设置 `is_chat_model=True`；`DashScope` 封装支持全部模型类型。
- **超时与重试**：`DashScopeParse` 默认 `max_timeout=3600` 秒，大文件解析可能超时；`DashScopeJsonNodeParser` 默认 `try_count_limit=10`，网络波动时可能触发重试。
- **知识库名称唯一性**：`DashScopeCloudIndex` 创建时若名称已存在，会报错而非覆盖，需手动清理或改名。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
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


