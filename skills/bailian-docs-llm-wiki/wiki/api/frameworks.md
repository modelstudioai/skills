# frameworks

百炼平台提供对主流 AI 开发框架的原生集成支持，重点覆盖 LlamaIndex 和 Spring AI Alibaba 两大生态。开发者可基于这些框架快速构建 RAG 应用、知识库检索服务及智能体工作流，无需从零实现底层模型调用、向量索引或文档解析逻辑。所有集成均通过官方 SDK 封装，统一使用 `DASHSCOPE_API_KEY` 认证，并与百炼控制台中的业务空间、知识库、应用等资源深度协同。

## 支持的模型与功能

- **大模型（LLM）**：支持全部百炼文本生成模型（如 `qwen-max`、`qwen-plus`），可通过 `DashScope` 或 OpenAI-like 兼容接口调用 [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)。
- **Embedding 模型**：支持 `text-embedding-v1`/`v2`/`v3`，其中 `v3` 在 CMTEB Retrieval 任务上达 73.23 分，为当前最优 [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)。
- **重排序（Rerank）模型**：提供 `gte-rerank` 和 `gte-rerank-hybrid`，用于对检索结果进行语义精排 [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)。
- **文档解析与切分**：`DashScopeParse` 支持 PDF/DOCX/DOC 智能解析（基于 Document Mind），`DashScopeJsonNodeParser` 提供基于通义模型的语义切分能力 [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)。
- **云端知识库管理**：`DashScopeCloudIndex` 实现文件上传、智能切分、向量索引构建与托管；`DashScopeCloudRetriever` 提供稠密/稀疏混合检索与重排能力 [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)。
- **Spring 生态集成**：`spring-ai-alibaba-starter-dashscope` 支持非流式/流式调用百炼智能体应用与知识库 RAG 服务 [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)。

> **注意**：文档 1 明确指出“本方案将知识库部署在云端，使用默认的智能文档切分与官方向量模型，**不支持自定义文档切分方式或自定义嵌入模型**”，而文档 4 和文档 6 分别提供了 `DashScopeEmbedding` 和 `DashScopeJsonNodeParser` 的自定义配置能力。该矛盾表明：**云端知识库（DashScopeCloudIndex）强制使用平台预置策略，而本地索引（VectorStoreIndex）才支持完全自定义 Embedding 与切分**。

## 关键参数

| 组件 | 参数名 | 类型 | 默认值 | 说明 |
|--------|--------|------|--------|------|
| `DashScopeEmbedding` | `model_name` | string | `text-embedding-v2` | 必填，取值见[支持的模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)表格 |
| `DashScopeRerank` | `top_n`, `model` | int, string | `5`, `gte-rerank` | `top_n` 控制返回结果数；`model` 可选 `gte-rerank` 或 `gte-rerank-hybrid` |
| `DashScopeCloudRetriever` | `dense_similarity_top_k`, `enable_reranking`, `rerank_top_n` | int, bool, int | `100`, `True`, `5` | `dense_similarity_top_k` 控制向量召回数；`rerank_top_n` 是重排后最终返回数，二者不可混淆 |
| `DashScopeJsonNodeParser` | `chunk_size`, `overlap_size`, `separator` | int, int, string | `500`, `100`, `" \|,\|，\|。\|？\|！\|\n\|\?\|!"` | `separator` 为正则表达式，需注意转义 |

## 使用方式

1. **环境准备**  
   - 获取 `DASHSCOPE_API_KEY` 并设为环境变量（[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)）；
   - 若使用子业务空间，还需设置 `DASHSCOPE_WORKSPACE_ID`；
   - 安装对应 SDK（如 `pip install llama-index-llms-dashscope llama-index-embeddings-dashscope`）。

2. **LlamaIndex 集成示例**  
   ```python
   from llama_index.llms.dashscope import DashScope
   from llama_index.embeddings.dashscope import DashScopeEmbedding
   from llama_index.indices.managed.dashscope import DashScopeCloudIndex

   # 全局设置（可选）
   Settings.llm = DashScope(model_name="qwen-max")
   Settings.embed_model = DashScopeEmbedding(model_name="text-embedding-v3")

   # 构建云端知识库
   index = DashScopeCloudIndex.from_documents(documents, name="my_kb")
   retriever = index.as_retriever(rerank_top_n=3)
   ```

3. **Spring AI Alibaba 集成示例**  
   - `pom.xml` 添加 `spring-ai-alibaba-starter-dashscope` 依赖；
   - `application.yml` 配置 `spring.ai.dashscope.api-key` 和 `spring.ai.dashscope.agent.app-id`；
   - 使用 `DashScopeAgent` 调用智能体，或 `DashScopeDocumentRetriever` 检索知识库 [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)。

## 限制和注意事项

- **文件解析限制**：`DashScopeParse` 仅对 `.pdf`/`.docx`/`.doc` 进行智能解析，其他格式（如 `.txt`, `.md`）仅原样上传，不触发 Document Mind [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)。
- **云端知识库不可定制**：如前所述，`DashScopeCloudIndex` 强制使用平台预置的切分与嵌入策略，无法替换为自定义模型或规则。
- **API Key 环境变量名不一致**：LlamaIndex 文档普遍使用 `DASHSCOPE_API_KEY`，但 Spring AI Alibaba 的知识库示例（文档 10）要求 `AI_DASHSCOPE_API_KEY`。实际使用时需按 SDK 要求配置，避免因变量名错误导致认证失败。
- **Python 版本约束**：所有 LlamaIndex 相关组件（`dashscopeparse`, `dashscopererank`, `dashscopecloudindex`）明确要求 `python>=3.9,<=3.12`，超出范围可能引发兼容性问题。

## 来源文档

- [通过LlamaIndex API构建RAG应用](../../raw/application-api-reference/frameworks/llamaindex.md)
- [使用百炼大模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopellm-in-llamaindex.md)
- [DashScopeRerank](../../raw/application-api-reference/frameworks/llamaindex/dashscopererank.md)
- [使用 Embedding 模型](../../raw/application-api-reference/frameworks/llamaindex/dashscopeembedding-in-llamaindex.md)
- [DashScopeParse](../../raw/application-api-reference/frameworks/llamaindex/dashscopeparse.md)
- [DashScopeJsonNodeParser](../../raw/application-api-reference/frameworks/llamaindex/dashscopejsonnodeparser.md)
- [通过 DashScopeCloudIndex（DashScopeCloudRetriever）构建阿里云百炼云端知识库并使用云端知识索引服务](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)
- [DashScopeCloudRetriever](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudretriever.md)
- [使用Spring AI Alibaba集成阿里云百炼大模型应用](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-llm-application.md)
- [通过Spring AI Alibaba检索阿里云百炼知识库](../../raw/application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)
- [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)


