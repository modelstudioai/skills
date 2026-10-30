# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）的生成能力与外部知识库的精准检索能力相结合的技术范式。它通过在模型推理前动态检索相关文档片段，并将其作为上下文注入提示（prompt），显著提升回答的事实准确性、领域专业性与私域知识覆盖能力，同时降低幻觉风险。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台中，RAG 不是独立功能模块，而是贯穿多个核心能力的**横切增强机制**，其落地形态因使用场景而异：

- **Agent 场景（推荐首选）**：  
  RAG 作为 `agent context` 的关键子模块（`context.rag`），与 Memory、Connector 等协同工作。调用 `/v1/agents/{agent_id}/chat` 时，只需传入 `context.rag = { "knowledge_base_id": "kb-xxx", "top_k": 3 }`，平台即自动完成：向量化查询 → 多路召回 → 重排序（默认 `qwen3-rerank`）→ 注入 top-k 片段至 LLM 上下文。支持与 `memory` 联动——若开启 `auto_memory_summary`，RAG 结果可被自动摘要并写入[长期记忆](long-term-memory.md)。

- **RAG API 原生服务场景**：  
  通过 `knowledge/search`（纯检索）或 `knowledge/chat`（检索+生成）接口直接调用。知识库需预先创建（`create_v2`），指定 `embeddingModelName`（如 `text-embedding-v4`）和 `rerankModelName`（如 `qwen3-rerank`）。该路径适合需要细粒度控制检索流程（如自定义分词、混合检索、多知识库路由）的高级用户。

- **应用集成场景（SaaS 渠道 & 本地部署）**：  
  - **企业微信/钉钉/网站等渠道嵌入**：在 AppFlow 配置智能体时，勾选“启用知识库”并设置“相似度阈值”（建议 0.3–0.6）、“召回片段数”（3–5），即可零代码启用 RAG；所有对话请求自动触发知识检索与增强。  
  - **本地 RAG 部署**：通过 `local_rag.zip` 启动的服务，支持完全自主的文档切分、本地 embedding（如 `gte-chinese-large`）、向量存储与检索逻辑，适用于数据不出域、需深度定制的场景。

> ✅ 统一前提：所有 RAG 使用均依赖已构建的知识库（`pipelineId`），且知识库内容需经百炼解析引擎处理为结构化切片（chunk），方可被高效检索。

## 关键参数和配置

| 参数位置 | 参数名 | 类型 | 默认值 | 说明 |
|----------|--------|------|--------|------|
| **Agent 调用** | `context.rag.knowledge_base_id` | string | — | 必填，知识库唯一标识（`pipelineId`） |
| | `context.rag.top_k` | integer | `3` | 检索返回的最高相关性片段数量（范围：1–10） |
| | `context.rag.reorder` | boolean | `false` | 是否按重排序模型分数重新排列结果（`true` 时忽略原始 score 顺序） |
| **知识库创建（RAG API）** | `embeddingModelName` | string | `text-embedding-v4` | 文本嵌入模型，影响检索语义质量 |
| | `rerankModelName` | string | `qwen3-rerank` | 重排序模型，用于对初检结果精细化打分 |
| | `hybrid_rerank` | boolean | `false` | 是否启用混合重排（如关键词+向量混排） |
| **应用集成（AppFlow / 本地 RAG）** | `similarity_threshold` | float | `0.0` | 相似度过滤阈值（0.0–1.0），低于此值的片段不参与生成 |
| | `top_k`（本地 RAG） | integer | `3` | 本地部署中显式配置的召回数量 |

⚠️ 注意事项：  
- 单次请求总上下文（含 RAG 片段、历史消息、Memory 内容等）不得超过 **128 KB**，超限返回 `400 Bad Request`；  
- RAG 片段默认按 `score` 降序排列，但 LLM 实际接收顺序由 `context.rag.reorder` 控制；  
- 知识库文件解析耗时受大小影响（>50MB 易超时），生产环境建议单文件 ≤50MB；  
- `similarity_threshold` 是抑制噪声的关键开关，调试阶段可设为 `0.0` 全量召回，上线后务必调高至 `0.3–0.6`。

## 面向开发者，简洁实用

- **快速上手 Agent RAG**：  
  ```json
  POST /v1/agents/agt-xxx/chat
  {
    "messages": [{"role": "user", "content": "我们的产品支持哪些支付方式？"}],
    "context": {
      "rag": {
        "knowledge_base_id": "kb-yyy",
        "top_k": 3
      }
    }
  }
  ```

- **验证 RAG 是否生效**：  
  查看响应中的 `usage.context_tokens`（非 `prompt_tokens`）是否显著增加；流式响应中，`delta.content` 开头若出现“根据知识库…”等引用提示，表明 RAG 已介入。

- **调试技巧**：  
  - 先用 `knowledge/search` 接口单独测试查询，确认 `kb-xxx` 能召回预期文档；  
  - 在 Agent 中临时关闭 `context.memory` 和 `context.connector`，聚焦验证 RAG 独立效果；  
  - 启用 SLS 日志节点（AppFlow）或检查 `context.rag` 字段的 `retrieved_chunks` 数组，直接观测检索结果。

RAG 的本质是“让模型知道它该知道的”，而非“让它记住一切”。在百炼，你只需专注知识库建设与业务问题定义，其余——检索、排序、注入、生成——均由平台可靠协同完成。

## 关联主题页

- [agent context](../guides/agent-context.md)
- [rag api](../api/rag-api.md)
- [use cases](../guides/use-cases.md)
- [application use cases](../guides/application-use-cases.md)


