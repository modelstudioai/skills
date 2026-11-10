# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）的生成能力与外部知识源的精准检索能力相结合的技术范式。它通过在模型推理前动态检索相关上下文片段，并将其作为提示的一部分输入模型，从而显著提升回答的事实准确性、领域专业性和私域知识覆盖能力，同时降低幻觉风险。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台中，RAG 不是独立服务，而是贯穿于知识管理、服务编排与应用集成的核心能力，具体体现为以下三类实践路径：

- **知识库驱动的问答服务**：通过创建文档/表格/图片/音视频类型的知识库，完成数据导入、切片、向量化与索引构建；再发布「知识问答」服务（`knowledge/chat`），系统自动将检索结果注入 LLM 提示词，实现基于私域知识的自然语言问答。适用于客服助手、产品文档解读等场景。

- **检索优先的服务调用**：发布「知识检索」服务（`knowledge/search`），仅执行语义召回（不触发生成），返回结构化切片列表（含 `content`、`score`、`metadata` 等字段）。开发者可自行组合后续逻辑（如多源融合、规则过滤、自定义 Prompt 编排），适合需精细控制上下文注入流程的高级 RAG 应用。

- **智能体（Agent）中的 RAG [工具调用](tool-calling.md)**：在百炼智能体应用中，将已发布的知识库服务注册为工具（Tool），配置调用策略（如「必定调用」或「按需触发」）。Agent 可根据对话状态自主决定是否检索、检索哪些知识库，并将结果用于多步推理或工具协同，支撑复杂业务流程（如合同条款比对+法条引用+风险提示）。

所有场景均统一依赖 RAG API 网关（`https://{workspace_id}.cn-beijing.maas.aliyuncs.com`），通过 `agent_id` 调用，无需感知底层嵌入/重排/生成模型的具体调度细节。

## 关键参数和配置

RAG 行为由知识库创建期与服务运行期两类参数共同决定，开发者应重点关注以下可调项：

| 参数 | 所属层级 | 说明 | 推荐值范围 | 是否可动态修改 |
|------|----------|------|-------------|----------------|
| `retrieval_top_k` | 运行期（服务/Agent 配置） | 单次检索最大召回切片数 | `3–5`（平衡精度与噪声） | ✅ 是（通过服务配置页或 `agent_config` 更新） |
| `similarity_threshold` | 运行期（服务/Agent 配置） | 向量相似度过滤阈值，低于此值的切片被丢弃 | `0.3–0.7`（默认 `0.5`） | ✅ 是 |
| `max_chunk_length` | 创建期（知识库索引设置） | 切片最大 token 长度，直接影响召回粒度 | `10–6000`（默认 `600`） | ❌ 否（需重建知识库） |
| `chunking_strategy` | 创建期（知识库索引设置） | 切片方式（智能/按长度/按页/按标题/正则/符号） | 根据文档结构选择 | ❌ 否 |
| `embedding_model` | 创建期（知识库配置） | 向量化模型，决定语义表征质量 | `qwen3.7-text-embedding`（默认）、`text-embedding-v4` | ❌ 否 |
| `rerank_model` | 运行期（服务/Agent 配置） | 对初检结果重排序，支持多模态精排 | `qwen3-rerank`（文本）、`qwen3-vl-rerank`（图文） | ✅ 是 |

> ⚠️ 注意：`retrieval_top_k` 和 `similarity_threshold` 在 API 调用中不直接透传，必须通过控制台或 RAG API 的 Agent 更新接口（`/api/v1/agents/{agent_id}/update`）配置 `agent_config` 生效；CLI 与框架集成（LlamaIndex/Spring AI）也需通过对应 SDK 的 `agent_id` 绑定方式间接控制。

## 面向开发者，简洁实用

- **快速起步**：用 CLI 一行命令验证 RAG 效果  
  ```bash
  bl knowledge chat --agent-id <your_agent_id> --message "Qwen3.7 支持哪些多模态能力？"
  ```

- **API 调用要点**：  
  - 请求头必带 `Authorization: Bearer <API-Key>`；  
  - 请求体只需 `{"messages": [{"role": "user", "content": "问题"}]}`，无需手动拼接 context；  
  - 流式响应需监听 `event: message` 和 `event: chunk` 事件。

- **调试建议**：  
  - 先用 `knowledge/search` 接口单独测试检索质量，确认 `content` 与 `score` 符合预期；  
  - 若问答效果不佳，优先调低 `similarity_threshold`（放宽召回）或增加 `retrieval_top_k`（提供更多上下文），而非直接调整 LLM 参数；  
  - 多知识库场景下，确保各库 `knowledgeScene`（如 `basic_document_qa`）与实际用途匹配，避免策略错配。

- **避坑提示**：  
  - 知识库创建后，`embedding_model` 和 `chunking_strategy` 不可更改——务必在首次创建时审慎选择；  
  - `agent_id` 是服务唯一标识，发布新版本后旧 ID 自动失效，需及时更新调用方配置；  
  - 控制台「图文并茂回复」场景已下线，新建知识库请勿使用 `visual_document_qa`。

## 关联主题页

- [rag api](../api/rag-api.md)
- [knowledge base](../guides/knowledge-base.md)
- [application use cases](../guides/application-use-cases.md)
- [use cases](../guides/use-cases.md)
- [frameworks](../api/frameworks.md)


