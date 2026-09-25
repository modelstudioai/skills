# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）的生成能力与外部知识源的精准检索能力相结合的技术范式。它通过在生成前动态检索相关上下文片段，并将其注入提示词（Prompt），使模型能在私有、实时或结构化知识约束下输出更准确、可溯源、低幻觉的响应。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台中，RAG 不是单一功能，而是贯穿多个产品层级的**核心增强机制**，具体体现为以下四类协同场景：

- **知识库服务（Knowledge Base）**：RAG 的标准化落地形态。用户上传文档/表格/图片/音视频后，平台自动完成解析→智能切片→向量化→索引构建；调用时，系统执行混合检索（向量 + 关键词）→重排精筛→拼接高相关切片→注入大模型生成，支持流式响应、引用标注与拒答控制。

- **LLM 应用（LLM Application）**：RAG 作为可编排的“能力节点”嵌入应用逻辑。在智能体（Agent 2.0）中，知识库被抽象为工具，由模型自主决策是否调用；在工作流（Workflow）中，可通过“知识库检索”或“知识库问答”节点显式接入，与其他 AI 节点（如意图识别、参数提取）串联；在高代码应用中，通过 MCP 协议调用已发布的 RAG Agent 实例。

- **API 集成（RAG API）**：提供面向生产环境的 RAG 服务接口。开发者可调用 `/api/v2/apps/knowledge/chat` 发起端到端问答，或调用 `/api/v1/indices/knowledge/search` 仅执行检索，所有请求均基于预发布的 `agent_id`，实现模型、检索策略与知识源的解耦部署。

- **框架集成（Frameworks）**：面向熟悉 LlamaIndex/Spring AI 的开发者，提供 `DashScopeCloudRetriever` 等 SDK 组件，屏蔽底层向量索引与 API 封装细节，支持在本地代码中直接复用百炼云端知识库与重排能力，快速构建定制化 RAG 应用。

> ✅ 共同特点：所有场景均默认启用**混合检索**（语义向量 + 精确关键词）、**两级排序**（初检 TopK → 重排精筛）和**生成可控性**（引用标注、防泄漏、拒答开关）。

## 关键参数和配置

RAG 行为由三类关键参数协同控制，均支持在控制台或 API 中配置：

| 类别 | 参数名 | 说明 | 典型取值 | 配置位置 |
|--------|--------|------|-----------|------------|
| **检索控制** | `dense_similarity_top_k` | 向量初检召回数量（影响召回广度与延迟） | `10–100`（默认 `100`） | 知识库服务配置页 / `DashScopeCloudRetriever` SDK |
| | `rerank_top_n` | 重排后最终返回给大模型的切片数（影响生成精度与 token 开销） | `1–20`（默认 `5`） | 同上；API 中对应 `max_retrieved_results` |
| | `similarity_threshold` | 过滤低分切片的相似度阈值（避免噪声注入） | `0.3–0.8`（默认 `0.4`） | 知识库服务配置页 |
| **切片与索引** | `chunk_size` | 单切片最大 token 数（决定语义单元粒度） | `10–6000`（默认 `600`） | 创建知识库时设定（不可变） |
| | `chunk_overlap` | 相邻切片重叠 token 数（缓解边界信息丢失） | `50–200`（默认 `100`） | `DashScopeJsonNodeParser` SDK 或本地切分工具 |
| **生成增强** | `enable_citation` | 是否在生成结果中标注引用来源（显示切片 ID 与原文高亮） | `true` / `false`（默认 `true`） | 知识问答服务配置页 / API 请求体 |
| | `enable_refusal` | 是否启用拒答策略（对无依据问题返回“无法回答”） | `true` / `false`（默认 `true`） | 同上 |

> ⚠️ 注意：`chunk_size` 和 `chunk_overlap` 在知识库创建时固化，修改需重建知识库；其他参数均可运行时动态调整。

## 面向开发者，简洁实用

- **快速验证**：直接使用控制台 Playground，选择知识库 → 切换“知识问答”模式，输入问题即可查看检索切片、引用高亮与生成结果，无需写一行代码。
- **API 调用最小集**：
  ```bash
  curl -X POST "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v2/apps/knowledge/chat" \
    -H "Authorization: Bearer {API_KEY}" \
    -H "Content-Type: application/json" \
    -d '{
          "agent_id": "your_agent_id",
          "query": "阿里云百炼的RAG支持哪些文件类型？",
          "enable_citation": true,
          "rerank_top_n": 3
        }'
  ```
- **SDK 推荐路径**：  
  - 新项目 → 用 `DashScopeCloudRetriever`（免运维，直接复用百炼索引）  
  - 需深度定制 → 用 `DashScopeEmbedding` + `DashScopeParse` 构建本地 `VectorStoreIndex`  
- **调试黄金法则**：  
  1. 若结果不准，先查 **Playground 中的检索切片** —— 若切片不相关，问题在知识库质量（切片/嵌入）；  
  2. 若切片相关但生成错误，再查 **生成参数与系统提示词** —— 检查 `system_prompt` 是否覆盖了检索内容空间；  
  3. 勿跳过 `similarity_threshold` 调优 —— 过低引入噪声，过高导致漏召，建议从 `0.5` 起步测试。

## 关联主题页

- [knowledge base](../guides/knowledge-base.md)
- [llm application](../guides/llm-application.md)
- [rag api](../api/rag-api.md)
- [frameworks](../api/frameworks.md)
- [application support](../guides/application-support.md)
- [application use cases](../guides/application-use-cases.md)


