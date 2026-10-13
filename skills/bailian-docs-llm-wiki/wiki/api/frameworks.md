# frameworks

百炼平台提供多套主流 AI 开发框架的深度集成支持，重点覆盖 LlamaIndex 和 Spring AI Alibaba 两大生态，帮助开发者快速构建 RAG、智能体、知识库检索等生产级应用。所有集成均基于百炼统一的模型服务、向量引擎与知识库管理能力，无需自行维护基础设施。

## 支持的模型/功能

百炼通过官方适配器支持以下核心能力：

- **大模型调用**：LlamaIndex 中可通过 `DashScope`（推荐）或 `OpenAILike`（兼容模式）两种方式调用全部百炼文本生成模型（如 `qwen-max`、`qwen-plus`），详见 [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)。
- **Embedding 模型**：支持 `text-embedding-v1`/`v2`/`v3` 三款嵌入模型，其中 `v3` 在 CMTEB Retrieval 任务上达 73.23 分，为当前最优；需配合 `llama-index-embeddings-dashscope` 使用。
- **文档解析与切分**：`DashScopeParse` 提供 PDF/DOCX/DOC 格式的智能解析（基于文档智能 DocMind），`DashScopeJsonNodeParser` 则对解析结果进行语义化切分，二者需协同使用；其他格式（如 TXT、MD）仅原样上传，不触发智能解析 [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)。
- **重排序（Rerank）**：`DashScopeRerank` 集成 `gte-rerank` 和 `gte-rerank-hybrid` 模型，用于对检索结果进行语义精排，提升相关性。
- **云端知识库管理**：`DashScopeCloudIndex` 和 `DashScopeCloudRetriever` 封装了从本地文件上传、云端智能切分、向量索引构建到检索的全链路，知识库部署在百炼平台侧，免运维。
- **Spring 生态集成**：`Spring AI Alibaba` 提供 `DashScopeAgent`（调用智能体/工作流应用）和 `DashScopeDocumentRetriever`（检索知识库）两类核心组件，完整支持 Spring Boot 3.x + JDK 17+ 环境。

> **注意**：文档 1 明确指出“本方案将知识库部署在云端，使用默认的智能文档切分与官方向量模型，**不支持自定义文档切分方式或自定义嵌入模型**”，而文档 11 和 4 均展示了在 LlamaIndex 中显式指定 `text-embedding-v2` 等模型的能力。该矛盾源于场景差异——文档 1 描述的是 *零代码 RAG 应用* 的限制，而文档 4/11 针对的是 *代码集成开发* 场景，后者完全支持自定义 Embedding 模型与切分逻辑。

## 关键参数

| 组件 | 关键参数 | 说明 | 默认值 |
|--------|-----------|------|---------|
| `DashScopeLLM` | `model_name` | 指定调用的大模型名称（如 `"qwen-max"`） | — |
| `DashScopeEmbedding` | `model_name` | 指定嵌入模型（`"text-embedding-v3"` 推荐） | — |
| `DashScopeRerank` | `model`, `top_n`, `rerank_min_score` | 模型名、返回 Top-N 结果数、重排后分数阈值 | `"gte-rerank"`, `3`, `0.0` |
| `DashScopeCloudRetriever` | `dense_similarity_top_k`, `enable_reranking`, `rerank_top_n` | 向量召回数、是否启用重排、重排后返回数 | `100`, `True`, `5` |
| `DashScopeJsonNodeParser` | `chunk_size`, `overlap_size`, `separator`, `language` | 切分块大小、重叠长度、分隔符、语言（`"cn"` 必选） | `500`, `100`, `" \|,\|，\|。\|？\|！\|\n\|\?\|!"`, `"cn"` |

## 使用方式

### LlamaIndex 集成（Python）

1. **安装依赖**（按需选择）：
   ```bash
   pip install llama-index-core
   pip install llama-index-llms-dashscope           # 大模型
   pip install llama-index-embeddings-dashscope     # Embedding
   pip install llama-index-readers-dashscope        # 文档解析
   pip install llama-index-node-parser-dashscope    # 文档切分
   pip install llama-index-indices-managed-dashscope # 云端知识库
   pip install llama-index-postprocessor-dashscope-rerank # 重排
   ```

2. **全局配置（可选）**：
   ```python
   from llama_index.core import Settings
   from llama_index.llms.dashscope import DashScope
   from llama_index.embeddings.dashscope import DashScopeEmbedding

   Settings.llm = DashScope(model_name="qwen-plus")
   Settings.embed_model = DashScopeEmbedding(model_name="text-embedding-v3")
   ```

3. **构建云端 RAG 流程**（关键步骤）：
   - 用 `DashScopeParse` 解析 PDF/DOCX → `Documents`
   - 用 `DashScopeJsonNodeParser` 切分 → `Nodes`
   - 用 `DashScopeCloudIndex.from_documents()` 上传并建索引
   - 用 `index.as_retriever()` 获取 `DashScopeCloudRetriever` 实例执行检索

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
         workspace-id: ${WORKSPACE_ID}  # 可选，子空间时必填
         agent:
           app-id: ${APP_ID}            # 调用智能体时必填
   ```

3. **核心调用**：
   - 智能体应用：注入 `DashScopeAgent`，调用 `agent.call(new Prompt(...))`
   - 知识库检索：使用 `DashScopeDocumentRetriever` 配合 `ChatClient` 的 `DocumentRetrievalAdvisor`

## 限制和注意事项

- **文件解析限制**：`DashScopeParse` 仅对 `.pdf`、`.doc`、`.docx` 执行智能解析（OCR、版面分析、公式识别等），其余格式（TXT、MD、PPTX 等）仅做原始文本提取，且单文件 ≤100MB 或 ≤1000 页 [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)。
- **业务空间强制要求**：所有 `DashScopeCloudIndex` / `DashScopeCloudRetriever` / `DashScopeParse` 操作均**必须配置 `DASHSCOPE_WORKSPACE_ID` 环境变量**，未配置将直接报错（文档 11 明确要求，而文档 5/6 仅标注为“可选”）。
- **API Key 环境变量名不一致**：LlamaIndex 示例普遍使用 `DASHSCOPE_API_KEY`，但 Spring AI Alibaba 文档 9 要求使用 `AI_DASHSCOPE_API_KEY`；开发者需按框架规范设置，不可混用。
- **模型兼容性**：`OpenAILike` 方式仅支持百炼的 *文本生成类模型*（如 `qwen-*`），不支持 `text-embedding-*` 或 `gte-rerank` 等专用模型，后者必须使用对应专用适配器（如 `DashScopeEmbedding`、`DashScopeRerank`）。
- **知识库更新**：`DashScopeCloudIndex` 支持运行时增量插入（`index._insert(documents)`）和删除（`index.delete_ref_doc([...])`），但暂不支持对已索引文档内容的原地更新。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)
- [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)
- [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)
- [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)
- [DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)
- [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)
- [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)
- [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)


