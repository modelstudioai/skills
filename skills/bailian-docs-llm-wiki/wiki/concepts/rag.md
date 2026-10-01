# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）的生成能力与外部知识源的精准检索能力深度融合的技术范式。它通过在模型推理前动态检索相关上下文片段，并将其作为提示的一部分注入生成过程，从而显著提升回答的事实准确性、领域专业性与私有知识覆盖能力。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台中，RAG 不是独立功能，而是贯穿多个能力层的**基础增强机制**，其使用方式因场景而异，但核心逻辑统一：**检索 → 注入 → 生成**。

- **知识库问答（最典型场景）**  
  通过控制台「知识库问答」模板或 `/api/v2/apps/knowledge/chat` 接口调用，系统自动完成：用户问题 → 向量+关键词混合检索 → 重排精筛 → 将 TopK 切片拼接为 `context` → 注入到 Qwen 系列模型（如 `qwen3.6-plus`）的 [prompt](../guides/prompt.md) 中 → 流式生成带引用标注的回答。全程无需编码，支持多模态（图文联合检索）与多库路由。

- **智能体（Agent 2.0）应用**  
  RAG 作为“工具”被显式集成：在 Agent 配置中启用知识库工具，或通过 `rag_options` 参数（API 调用时）指定 `pipeline_ids`、`tags` 或 `metadata_filter`，实现按需、精准、可审计的私有知识调用。Agent 的规划链路可自主决定是否触发检索，支持“先思考→再检索→后生成”的闭环。

- **工作流（Workflow）应用**  
  通过拖拽「知识库节点」接入 RAG 能力，可与其他节点（如大模型、条件判断、API）编排组合。例如：用户提问 → 意图分类 → 若属产品咨询 → 触发知识库检索 → 将结果传给大模型润色输出。检索参数（TopK、阈值等）可在节点内独立配置。

- **低代码/零代码集成（如企业微信、网站助手）**  
  在 AppFlow 连接流中开启「引用知识」开关，选择已发布知识库并设置调用策略（`必定调用` 或 `按需调用`），即可将 RAG 能力一键嵌入第三方平台，无需修改前端或后端逻辑。

- **高代码应用与第三方框架（LangChain/Dify/Coze）**  
  通过调用底层 RAG API（如 `/api/v1/indices/rag/index/retrieve` 获取原始切片，或 `/api/v1/indices/knowledge/search` 调用多库联合检索服务），开发者可完全自定义检索逻辑、上下文组装策略与生成提示，实现深度定制。

> ✅ 关键区别：知识库问答是开箱即用的 RAG 封装；Agent/Workflow 是 RAG 的可编程集成；API 层则是 RAG 的原子能力暴露。

## 关键参数和配置

RAG 效果由**检索侧**与**生成侧**参数协同控制，需分层配置：

| 类别 | 参数名 | 说明 | 配置位置 | 典型取值 |
|------|--------|------|----------|----------|
| **检索控制（知识库级）** | `top_k` | 最终返回的最相关切片数量 | 知识库服务配置 / `rag_options` / 工作流知识库节点 | `3`–`10`（默认 `5`） |
| | `similarity_threshold` | 相似度过滤下限（0.01–1.0） | 知识库服务配置 / `rag_options` | `0.3`–`0.6`（过低易召回噪声） |
| | `rerank_model_name` | 重排模型（提升相关性） | 创建知识库或 Agent 配置时指定 | `qwen3-rerank`, `qwen3-vl-rerank` |
| | `query_rewrite` | 是否启用查询改写（优化语义表达） | 知识库服务配置 | `true`/`false` |
| **生成控制（应用级）** | `temperature` | 控制生成多样性（影响答案严谨性） | 应用模型参数 / API `parameters.temperature` | `0.1`–`0.5`（RAG 场景推荐低值） |
| | `system_prompt` | 显式指令模型“基于以下检索内容回答，不可编造” | 智能体/工作流系统提示词 | 必须包含引用约束（如“仅依据提供的上下文作答”） |
| | `enable_thinking` | 开启模型深度推理（提升对长上下文的理解） | Agent 应用参数 / API `enable_thinking` | `true`（配合 RAG 可提升答案结构化程度） |
| **高级路由（多库场景）** | `knowledge_routing` | 启用大模型自动选择知识库 | 知识库服务配置 | `true`（需多库且标签清晰） |
| | `tags` / `metadata_filter` | 按元数据精准限定检索范围 | `rag_options` / 知识库节点配置 | `["product_v2", "internal_only"]` |

> ⚠️ 注意：`max_tokens`（生成长度）不宜过大，避免模型在冗余上下文中迷失；`temperature=0` 与 `similarity_threshold` 高值搭配，可获得最确定、最忠实于检索结果的回答。

## 面向开发者，简洁实用

- **快速验证**：直接使用 [RAG Playground](https://bailian.console.aliyun.com/cn-beijing/rag/playground)，上传文档 → 创建知识库 → 切换「知识问答」模式，实时观察检索切片与生成结果，5 分钟完成效果调优。
- **API 集成首选路径**：  
  ```bash
  # 1. 检索（获取原始切片）
  curl -X POST https://dashscope.aliyuncs.com/api/v1/indices/rag/index/retrieve \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -d '{"index_id":"idx_abc123","query":"Qwen3 支持哪些嵌入模型？","top_k":5}'

  # 2. 问答（端到端 RAG，流式响应）
  curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/knowledge/chat \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"agent_id":"agt_xyz789","input":{"messages":[{"role":"user","content":"Qwen3 支持哪些嵌入模型？"}]},"stream":true}'
  ```
- **调试黄金法则**：  
  - 若答案不准确 → 检查 `similarity_threshold` 是否过低，或 `rerank_model_name` 是否未启用；  
  - 若答案无引用 → 确认 `system_prompt` 中明确要求“基于以下内容回答”，且未被其他提示覆盖；  
  - 若检索为空 → 检查知识库状态（是否完成解析/向量化）、文件格式兼容性（PDF/TXT/DOCX）、以及 `query_rewrite` 是否误改写了关键术语。
- **生产建议**：  
  - 对敏感业务，开启 `enable_anti_leak`（防信息泄露）；  
  - 多库场景优先用 `knowledge_routing` + 清晰 `tags`，而非硬编码 `pipeline_ids`；  
  - 流式接口务必设 `stream=true`，否则请求失败（当前强制要求）。

## 关联主题页

- [start using](../guides/start-using.md)
- [rag api](../api/rag-api.md)
- [knowledge base](../guides/knowledge-base.md)
- [llm application](../guides/llm-application.md)
- [application call](../api/application-call.md)
- [application use cases](../guides/application-use-cases.md)


