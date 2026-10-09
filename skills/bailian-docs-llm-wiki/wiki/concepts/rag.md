# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，简称 RAG）是一种将大语言模型（LLM）的生成能力与外部知识源的精准检索能力相结合的技术范式。它通过在模型推理前动态检索相关上下文片段，并将其注入提示词（prompt），使模型能在私有、实时或领域专属知识基础上生成更准确、可溯源、低幻觉的回答。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台中，RAG 不是独立功能模块，而是贯穿多个核心能力的**基础增强机制**，其落地形态高度统一于“知识库 + 服务化调用”架构：

- **知识库（Knowledge Base）**：是 RAG 的核心载体。所有非结构化/半结构化数据（PDF、Word、Excel、图片、音视频等）经智能解析、语义切片、向量化索引后，形成可被高效检索的结构化知识源。知识库本身不运行模型，但为后续检索与问答提供底层支撑。

- **知识问答服务（`/api/v2/apps/knowledge/chat`）**：最典型的 RAG 应用场景。用户提问触发三阶段流程：① Query 改写与多路检索（向量+关键词混合）→ ② 召回结果重排（Rerank）→ ③ 将 Top-K 高相关切片拼接进系统提示词，交由绑定的大模型（如 `qwen3.6-plus`）生成最终回答。全程支持流式响应与思考链（`enable_thinking`）输出。

- **智能体应用（Agent）**：RAG 作为内置工具能力深度集成。新版 Agent 2.0 将知识库检索封装为可自主规划调用的 `search_knowledge` 工具；旧版 Agent 则通过预设的“必定调用”策略，在每次生成前自动执行检索。开发者可通过 `rag_options` 参数在 API 调用时动态指定知识库 ID（`pipeline_ids`）、文档过滤条件（`file_ids`, `metadata_filter`, `tags`）等。

- **工作流（Workflow）**：通过“知识库”AI 节点显式接入 RAG。节点配置即定义检索行为（如选择知识库、设置 TopK、启用重排），输出为结构化文本片段，可直接送入下游大模型节点或用于条件判断，实现可控、可编排的增强逻辑。

- **高代码应用 & 第三方框架（LlamaIndex/Spring AI）**：面向专业开发者，提供 SDK 级抽象（如 `DashScopeCloudRetriever`）。开发者可组合 `DashScopeCloudIndex`（云端知识库）与 `DashScopeLLM`，在 Python 中构建端到端 RAG 流程，完全复用百炼的向量化、检索、重排能力，无需自建基础设施。

> ✅ 关键共识：无论哪种场景，RAG 的核心价值始终是——**让大模型“知道它该知道的”，而非“记住所有”**。百炼通过统一的知识库底座和标准化的服务接口，屏蔽了向量数据库、嵌入模型、重排模型等技术细节，使开发者聚焦于业务逻辑。

## 关键参数和配置

RAG 行为由三类参数协同控制，均支持控制台配置与 API 动态传入：

| 类别 | 参数名 | 说明 | 典型取值 | 生效位置 |
|------|--------|------|-----------|------------|
| **检索控制** | `top_k` | 初步向量召回数量（未重排前） | `10`–`100` | `/api/v1/indices/rag/index/retrieve` 请求体；知识库检索服务配置；`rag_options` 中 |
| | `similarity_threshold` | 向量相似度最低阈值，低于则过滤 | `0.3`–`0.8`（浮点） | 知识库检索服务配置；`DashScopeCloudRetriever` 初始化参数 |
| | `rerank_model_name` | 重排模型名称，提升排序精度 | `"qwen3-rerank"`（文本）、`"qwen3-vl-rerank"`（多模态） | 知识库创建/更新时配置；`DashScopeRerank` 构造参数 |
| **生成控制** | `temperature` | 控制生成随机性，影响答案稳定性 | `0.0`（确定）–`1.0`（发散） | 问答服务配置；`/api/v2/apps/knowledge/chat` 请求体；Agent 模型参数 |
| | `enable_thinking` | 开启模型内部推理链（Chain-of-Thought），提升复杂问题处理能力 | `true`/`false` | 问答服务配置；Agent 2.0 参数；`application call` API 参数 |
| **知识源控制** | `pipeline_ids` | 必选：指定一个或多个知识库 ID（即 `agent_id`） | `["pip-xxx"]` | `rag_options` 对象内（API 调用）；工作流知识库节点配置 |
| | `metadata_filter` | 按元数据字段（如 `category: "faq"`）过滤召回结果 | `{"category": "faq"}` | `rag_options`；知识库检索服务高级配置 |

> ⚠️ 注意：  
> - 所有参数均**大小写敏感**，且 `pipeline_ids` 是数组类型，不可传单个字符串；  
> - `similarity_threshold` 与 `top_k` 需权衡：阈值过高易漏召，过低则引入噪声；`top_k` 过大增加重排开销，过小可能丢失关键片段；  
> - 重排模型 (`rerank_model_name`) 一旦在知识库创建时选定，**不可修改**，需谨慎选择。

## 面向开发者，简洁实用

- **快速验证**：用控制台 [Playground](https://bailian.console.aliyun.com/cn-beijing/rag/playground) 直接测试知识库检索与问答效果，无需写一行代码。
- **API 集成**：  
  - 单库检索 → `/api/v1/indices/rag/index/retrieve`（轻量、底层）  
  - 多库联合检索 → `/api/v1/indices/knowledge/search`（需 `agent_id`，策略由服务配置驱动）  
  - 流式问答 → `/api/v2/apps/knowledge/chat`（推荐生产使用，含完整 RAG 链路）  
- **SDK 开发**：优先使用 `DashScopeCloudRetriever`（LlamaIndex）或 `DashScopeAgent`（Spring AI），避免重复造轮子。示例：  
  ```python
  from llama_index.retrievers.dashscope import DashScopeCloudRetriever
  retriever = DashScopeCloudRetriever(
      pipeline_id="pip-xxx",
      top_k=5,
      enable_reranking=True,
      rerank_model_name="qwen3-rerank"
  )
  nodes = retriever.retrieve("如何申请发票？")
  ```
- **避坑指南**：  
  - 知识库 `index_id` ≠ 问答服务 `agent_id`：前者是数据索引 ID，后者是发布后的服务 ID，调用 API 时务必使用 `agent_id`；  
  - 文件上传后需等待 **索引构建完成**（控制台显示“就绪”）才能检索，状态可通过 `/api/v1/indices/rag/index/status` 查询；  
  - 新版 Connector 迁移截止日为 **2026年9月30日**，新项目请直接使用知识库（Knowledge Base）而非旧版“数据连接”。

## 关联主题页

- [knowledge base](../guides/knowledge-base.md)
- [rag api](../api/rag-api.md)
- [llm application](../guides/llm-application.md)
- [application call](../api/application-call.md)
- [application use cases](../guides/application-use-cases.md)
- [frameworks](../api/frameworks.md)


