# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，简称 RAG）是一种将大语言模型（LLM）与外部知识源动态结合的推理范式：系统在生成回答前，先从私有或结构化知识库中检索相关片段，再将检索结果作为上下文注入模型提示（[prompt](../guides/prompt.md)），从而提升回答的准确性、时效性与事实一致性。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台，RAG 不是独立功能模块，而是贯穿多个能力层的**核心增强机制**，具体体现为：

- **知识库问答（KB QA）**：最典型的应用。用户提问后，平台自动执行「向量检索 →（可选）重排 → 注入上下文 → 调用 LLM 生成」全流程。控制台中选择「知识库问答」模板、API 调用 `/v1/knowledge/query` 或 SDK 的 `KnowledgeBase.chat()` 均默认启用完整 RAG 流程。

- **智能体（Agent）工作流**：RAG 作为可插拔工具被集成进 Agent 决策链。例如，在 AppFlow 中配置「知识库检索」节点，或通过 `tools` 声明 `knowledge_retrieval` 工具，由模型自主判断是否调用、何时调用、调用哪个知识库。

- **多模态 RAG**：支持跨模态检索增强，如上传 PDF 文档 + 配套产品图片，提问“图中红框部件的安装步骤是什么？”，系统可联合检索文本切片与图像语义特征，生成图文一致的回答。

- **本地化 RAG（Hybrid RAG）**：开发者可在本地完成文档解析、切片与嵌入（如使用 ModelScope 的 `gte-chinese-large`），仅将检索结果和原始 query 发送给百炼 API 进行生成，实现数据不出域+模型能力复用。

- **零代码应用构建**：控制台创建「知识库问答」应用时，RAG 已预置为默认推理模式；无需编写代码，上传文档即自动启用检索增强。

> ⚠️ 注意：百炼 RAG 服务由平台统一引擎托管，**不支持替换底层检索或生成组件**（如自定义向量数据库或外部 LLM）。所有检索策略、重排模型、生成模型均需从平台提供的选项中配置。

## 关键参数和配置

RAG 效果高度依赖以下可调参数，按作用层级分类：

| 类别 | 参数名 | 取值范围 | 说明 | 生效位置 |
|--------|--------|----------|------|-----------|
| **检索控制** | `top_k` | 1–10（API 默认 3）<br>1–20（控制台默认 5） | 返回最相关切片数量；增大可提升召回率，但可能引入噪声并增加 token 开销 | API `/v1/knowledge/query`、控制台知识库服务配置、AppFlow 知识库节点 |
| | `similarity_threshold` | 0.01–1.0（推荐 0.3–0.7） | 过滤低相似度切片；值过高易漏召，过低易引入无关内容 | 控制台知识库配置、AppFlow 知识库节点 |
| | `enable_rerank` | `true` / `false`（默认 `false`） | 启用 `qwen3-rerank` 等重排模型精筛结果，提升相关性，延迟略增 | API `/v1/knowledge/query`、控制台知识库服务配置 |
| **生成增强** | `temperature` | 0.0–2.0（默认 0.8） | 控制生成随机性；RAG 场景建议设为 0.1–0.5 以提升答案稳定性 | 所有生成接口（`parameters.temperature`） |
| | `enable_thinking` | `true` / `false` | 启用思考链（Chain-of-Thought），帮助模型更严谨地整合检索内容与问题逻辑 | 控制台/SDK 的 `parameters.enable_thinking` |
| **混合策略** | `retrieval_mode` | `always`（必定调用）、`on_demand`（按需调用） | 控制是否强制触发检索；`on_demand` 由模型自主判断是否需要知识库，适合混合通用问答与私域问答 | AppFlow 知识库节点、控制台应用配置 |

> ✅ 最佳实践：生产环境建议固定 `top_k=5` + `similarity_threshold=0.45` + `enable_rerank=true` 组合，并将 `temperature` 设为 `0.3`，兼顾精度、鲁棒性与成本。

## 面向开发者，简洁实用

- **快速验证**：直接使用控制台 [Playground](https://bailian.console.aliyun.com/cn-beijing/rag/playground) → 选择知识库 → 切换「知识问答」模式，实时调试检索与生成效果，无需部署。
- **API 集成**：调用 `POST /v1/knowledge/query`，只需传 `knowledge_base_id` 和 `query`，其他参数均为可选；响应中 `retrieved_chunks` 字段明确返回所用上下文，便于审计与调试。
- **SDK 推荐**：Python 使用 `dashscope 1.20.0+`，调用 `KnowledgeBase.chat(query="...", top_k=5, enable_rerank=True)`；Node.js 使用 `@alibabacloud/dashscope 1.15.0+`，方法同名。
- **避坑提示**：
  - 切片（chunk）内容不可修改，更新文档需删除后重新上传；
  - 知识库规格影响 QPS：标准版限 1 QPS，高并发请选用旗舰版（按 RCU 计费）；
  - 所有 RAG 请求默认启用敏感词过滤与内容安全审核，不可关闭；
  - 多知识库并行检索需在 API 中显式传入多个 `knowledge_base_id` 数组（部分 SDK 尚未支持，建议优先用控制台或 REST API）。

RAG 是百炼平台连接私有知识与大模型能力的“神经中枢”。合理配置检索与生成参数，即可在零代码、低代码、全代码三种路径下，稳定交付可信、可控、可解释的 AI 应用。

## 关联主题页

- [start using](../guides/start-using.md)
- [knowledge base](../guides/knowledge-base.md)
- [rag api](../api/rag-api.md)
- [use cases](../guides/use-cases.md)
- [application use cases](../guides/application-use-cases.md)
- [application support](../guides/application-support.md)


