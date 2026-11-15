# frameworks

百炼平台提供多框架集成能力，支持主流 AI 开发框架（如 LlamaIndex、Spring AI Alibaba）快速对接大模型服务、Embedding、文档解析、云端知识库检索与重排等能力。开发者可基于统一 API Key 和业务空间配置，复用百炼的模型服务与数据处理基础设施，避免重复建设向量索引、文档切分、RAG 编排等模块。

## 支持的模型与功能

百炼在框架集成中覆盖以下核心能力：

- **大模型调用**：支持 `qwen-plus`、`qwen-max` 等全部文本生成模型，可通过 OpenAI-like 兼容模式或原生 DashScope 封装调用 [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)。
- **Embedding 模型**：提供 `text-embedding-v1`/`v2`/`v3` 三款向量模型，均通过 MTEB/CMTEB 评测验证，其中 `text-embedding-v3` 在 CMTEB Retrieval 任务上达 73.23 分 [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)。
- **文档智能解析**：`DashScopeParse` 支持 PDF/DOC/DOCX 智能解析（含版面分析、表格识别），其他格式（TXT/MD/PPT/XLS 等）仅原样上传 [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)。
- **云端知识库服务**：`DashScopeCloudIndex` 实现端到端云端索引构建与管理；`DashScopeCloudRetriever` 提供向量+文本混合检索、内置重排（`gte-rerank-hybrid`）、过滤与阈值控制 [DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)。
- **重排模型**：`DashScopeRerank` 集成 `gte-rerank` 系列模型，支持对初检结果进行语义精排 [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)。
- **Spring 生态集成**：`Spring AI Alibaba` 提供 `DashScopeAgent`（调用百炼应用）和 `DashScopeDocumentRetriever`（检索知识库）两类核心组件，适配 Spring Boot 3.x + JDK 17+ [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)。

> **注意**：文档 5 和文档 6 均指出“本方案将知识库部署在云端，使用默认的智能文档切分与官方向量模型，不支持自定义文档切分方式或自定义嵌入模型”，但文档 4 的 `DashScopeJsonNodeParser` 明确用于对 `DashScopeParse` 解析结果进行自定义切分。这表明：**云端知识库（DashScopeCloudIndex）本身不开放切分逻辑，但开发者可在本地解析后、上传前使用 `DashScopeJsonNodeParser` 进行预处理**。实际使用时需按场景选择——纯云端托管用 `DashScopeCloudIndex`；需精细控制切分则先用 `DashScopeParse` + `DashScopeJsonNodeParser` 生成自定义 Nodes，再调用 `VectorStoreIndex.from_documents()` 构建本地索引。

## 关键参数

| 组件 | 关键参数 | 默认值 | 说明 |
|--------|-----------|---------|------|
| `DashScope` (LLM) | `model_name` | — | 必填，如 `"qwen-max"`；完整列表见 [选择模型](raw/model-user-guide/get-started-with-models/models.md) |
| `DashScopeEmbedding` | `model_name` | `"text-embedding-v2"` | 可选 `"text-embedding-v1"`/`"v2"`/`"v3"` |
| `DashScopeParse` | `category_id`, `workspace` | `"default"`, `None` | `category_id` 决定文件归类，影响后续检索过滤；`workspace` 用于非默认业务空间 |
| `DashScopeJsonNodeParser` | `chunk_size`, `separator`, `language` | `500`, `" \|,\|，\|。\|？\|！\|\n\|\?\|\!"`, `"cn"` | `language="any"` 性能下降明显，生产环境建议显式指定 `"cn"` 或 `"en"` |
| `DashScopeCloudRetriever` | `dense_similarity_top_k`, `enable_reranking`, `rerank_model_name` | `100`, `True`, `"gte-rerank-hybrid"` | 混合检索时 `dense_similarity_top_k` 与 `sparse_similarity_top_k` 共同控制召回规模；重排模型必须启用 `enable_reranking=True` 才生效 |
| `DashScopeRerank` | `model`, `top_n` | `"gte-rerank"`, `3` | `model` 仅支持 `"gte-rerank"`（文档 8），但 `DashScopeCloudRetriever` 支持 `"gte-rerank-hybrid"`（文档 11），二者模型能力不同，不可混用 |

## 使用方式

### 1. 环境准备
- 获取 API Key 并设为环境变量 `DASHSCOPE_API_KEY`（[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)）。
- 如使用非默认业务空间，需额外设置 `DASHSCOPE_WORKSPACE_ID`。
- 安装对应框架包（以 LlamaIndex 为例）：
  ```bash
  pip install llama-index-core
  pip install llama-index-llms-dashscope        # LLM
  pip install llama-index-embeddings-dashscope  # Embedding
  pip install llama-index-readers-dashscope     # Parse/CloudIndex
  pip install llama-index-indices-managed-dashscope  # CloudIndex/Retriever
  pip install llama-index-postprocessor-dashscope-rerank  # Rerank
  ```

### 2. 典型工作流（LlamaIndex）
```python
# 步骤1：解析文档（PDF/DOCX 智能解析）
from llama_index.readers.dashscope import DashScopeParse
documents = DashScopeParse(category_id="cate_xxx").load_data(file_path=["doc.pdf"])

# 步骤2：构建云端知识库（自动切分+索引）
from llama_index.indices.managed.dashscope import DashScopeCloudIndex
index = DashScopeCloudIndex.from_documents(documents, name="my_index")

# 步骤3：初始化检索器（混合检索+重排）
retriever = index.as_retriever(
    dense_similarity_top_k=50,
    sparse_similarity_top_k=50,
    enable_reranking=True,
    rerank_model_name="gte-rerank-hybrid"
)

# 步骤4：检索
nodes = retriever.retrieve("阿里云百炼手机有哪些型号？")
```

### 3. Spring AI Alibaba（Java）
- 在 `application.yml` 中配置：
  ```yaml
  spring:
    ai:
      dashscope:
        api-key: ${AI_DASHSCOPE_API_KEY}
        # workspace-id: ${AI_DASHSCOPE_WORKSPACE_ID}  # 可选
  ```
- 使用 `DashScopeDocumentRetriever` 检索知识库（支持 `searchFilters` 字段过滤）：
  ```java
  DashScopeDocumentRetrieverOptions options = DashScopeDocumentRetrieverOptions.builder()
      .indexName("测试知识库")
      .searchFilters(List.of(Map.of("_operator", "OR", "_conditions", List.of(
          Map.of("department", "Corporate"),
          Map.of("document_type", Map.of("like", "%Policy%"))
      ))))
      .build();
  DocumentRetriever retriever = new DashScopeDocumentRetriever(dashscopeApi, options);
  ```

## 限制和注意事项

- **文件解析限制**：`DashScopeParse` 仅对 PDF/DOC/DOCX 进行智能解析（含 OCR、表格、公式），TXT/MD/PPT/XLS 等格式仅原样上传，不提取结构化内容 [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)。
- **尺寸与数量限制**：单个文件 ≤ 100 MB 且 ≤ 1000 页；一次 `load_data` 最多处理 200 个文件（文档 5）。
- **Python 版本约束**：所有 `llama-index-*dashscope*` 包要求 `python>=3.9,<=3.12`（文档 3、4、5、8、11），超范围版本可能引发兼容性问题。
- **重排模型差异**：`DashScopeRerank`（独立组件）仅支持 `gte-rerank`，而 `DashScopeCloudRetriever` 内置支持 `gte-rerank-hybrid`（融合稠密+稀疏特征）。二者不可互换，需按组件文档选用。
- **Spring AI Alibaba 环境变量名不一致**：LlamaIndex 生态统一用 `DASHSCOPE_API_KEY`，但 Spring AI Alibaba 示例中推荐使用 `AI_DASHSCOPE_API_KEY`（文档 10）。若混用框架，需确保环境变量名匹配对应 SDK 的读取逻辑。

## 来源文档

- [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)
- [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)
- [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)
- [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)
- [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)
- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)
- [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)
- [DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)


