# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，简称 RAG）是一种将大语言模型（LLM）的生成能力与外部知识源的精准检索能力相结合的技术范式。它通过在模型推理前动态检索相关上下文片段，并将其作为提示词的一部分输入模型，从而显著提升回答的事实准确性、领域专业性和时效性，同时降低幻觉风险。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台，RAG 不是单一功能模块，而是贯穿模型服务、应用构建与知识管理全链路的核心能力范式，具体体现为以下三类实践路径：

- **API 级直接调用**：通过 `RAG API`（`/v1/knowledge/query`）端到端完成知识库检索 + LLM 生成。开发者传入 `knowledge_id` 和 `query`，可选指定 `model`（如 `qwen-plus`）触发生成，平台自动执行文档切片召回、重排（`enable_rerank=true`）、上下文拼接与答案合成，返回带引用片段的答案。

- **应用层低代码编排**：在 `LLM Application` 中，RAG 以标准化节点形式嵌入工作流（Workflow）或智能体（Agent）：
  - 工作流中，组合「知识库节点」（配置 `topK=3`、相似度阈值）与「大模型节点」，实现可控的 RAG 链路；
  - Agent 应用（尤其 Agent 2.0）将知识库作为内置工具，支持 `list_tools` 自动发现与 `on_system_prompt` 静态注入两种调用模式，模型自主决定是否及何时检索。

- **知识基础设施即服务**：`Knowledge Base` 是 RAG 的底层支撑，提供企业级知识库全生命周期管理——从多格式文档（PDF/DOCX/Excel/图片等）解析、智能切片（按段落/标题/固定 token）、向量化（默认 `text-embedding-v4`）、混合检索（向量+关键词），到联合多库路由与混排。所有上层 RAG 调用均依赖此统一知识底座。

此外，在 `Application Use Cases`（如企业微信/钉钉/网站 AI 助手）和 `Frameworks`（LlamaIndex/Spring AI Alibaba 集成）中，RAG 均作为默认推荐架构落地，确保业务场景开箱即用、安全可控。

## 关键参数和配置

RAG 效果高度依赖以下关键参数，需根据场景权衡精度、延迟与成本：

| 参数名 | 所属层级 | 说明 | 推荐取值 | 注意事项 |
|--------|----------|------|-----------|----------|
| `top_k` / `topK` | 检索层 | 召回最相关知识片段数量 | **3–5**（问答场景）；≤20（知识库服务上限） | 过高易引入噪声；`RAG API` 中最大为 50，但知识库服务限制为 20 |
| `similarity_threshold` | 检索层 | 相似度过滤阈值（0.01–1.0） | **0.3–0.7**（默认 0.5） | 值越高越严格，可提升精准度但可能漏召 |
| `enable_rerank` | 检索层 | 是否启用重排模型精排初筛结果 | **true**（推荐） | 启用后消耗双倍 token 配额；支持 `qwen3-rerank`（文本）或 `qwen3-vl-rerank`（多模态） |
| `model` | 生成层 | 指定用于答案生成的大模型 | `qwen-plus`（平衡）、`qwen3.5-plus`（最新稳定版） | `RAG API` 中不传则仅返回检索结果；工作流/Agent 中需显式配置 |
| `temperature` | 生成层 | 控制生成随机性 | **0.1–0.5**（客服/问答等确定性场景建议偏低） | 生产环境避免设为 0（部分模型如 `qwen-max` 可能返回空响应） |
| `chunk_size` | 知识库层 | 文档切片最大长度（token） | **500–600**（中文语义连贯性优先） | 创建知识库后不可修改；过小导致语义碎片化，过大降低召回精度 |

> ⚠️ **重要约束**：  
> - 所有 RAG 请求必须指定正确的 `DASHSCOPE_WORKSPACE_ID`（若使用子空间）；  
> - 知识库功能仅支持 **华北2（北京）** 地域；  
> - 单次请求 `input.messages` 总长度上限为 32768 token，含检索片段拼接后的完整 [prompt](../guides/prompt.md)。

## 面向开发者，简洁实用

- **快速验证**：直接使用控制台 [Playground](https://bailian.console.aliyun.com/cn-beijing/rag/playground)，选择知识库 → 切换「知识问答」模式 → 输入问题，实时查看召回片段与模型回答，无需写一行代码。  
- **API 集成**：优先使用 `RAG API`（`/v1/knowledge/query`），而非手动拼接检索+LLM调用；它已封装向量检索、重排、上下文截断、[prompt](../guides/prompt.md) 构造等全部逻辑。  
- **框架开发**：LlamaIndex 用户推荐 `DashScopeCloudRetriever` + `DashScopeLLM` 组合，设置 `enable_reranking=True` 和 `rerank_min_score=0.3` 即可获得生产级 RAG 流程。  
- **避坑指南**：  
  - 不要依赖模型内置 system [prompt](../guides/prompt.md)，所有 RAG 上下文必须显式拼入 `input.messages`；  
  - 文件上传接口（如 `/v1/documents`）必须用 `multipart/form-data`，单文件 ≤100 MB；  
  - 微信公众号未认证时，被动回复严格限时 5 秒，务必提前完成认证。  

RAG 的本质是“让模型知道它该知道的”，而非“让它记住一切”。在百炼平台，你只需聚焦业务知识与用户问题，其余——检索、排序、生成、引用——均由平台可靠交付。

## 关联主题页

- [start using](../guides/start-using.md)
- [rag api](../api/rag-api.md)
- [llm application](../guides/llm-application.md)
- [knowledge base](../guides/knowledge-base.md)
- [application use cases](../guides/application-use-cases.md)
- [frameworks](../api/frameworks.md)


