# 检索增强生成（RAG）

检索增强生成（Retrieval-Augmented Generation，RAG）是指大模型在生成回答前，先从外部知识库检索相关内容并拼接进上下文，从而补充私有数据、最新信息，提升回答的准确性并降低幻觉。它是阿里云百炼平台知识库、智能问答与多种应用场景的核心底层能力。

## 在百炼平台的使用场景

百炼围绕 RAG 提供从建库到问答、从控制台到 API、从云端到本地的多条落地路径：

- **云端知识库（控制台）**：基于百炼知识库能力构建 RAG，先创建知识库（选类型、配数据源与索引参数），再关联到智能体或工作流应用。工作流应用中把「知识库」节点接在开始节点后，用内置变量 `query` 作输入，输出 `result` 传给大模型节点。知识库功能仅在中国站 **华北2（北京）** 地域开通使用。
- **知识检索与知识问答服务**：平台在知识库之上提供两类独立服务。知识检索支持多知识库联合检索（最多 15 个），流水线为 Query 改写 → 向量+关键词混合检索 → Rerank 精排 → 加权返回；知识问答基于大模型结合检索生成自然语言回答，提供极速（单轮）与多轮智能（Agentic 规划搜索）两种模式，支持拒答、防泄漏、引用来源展示。
- **HTTP REST API（DashScope 应用网关）**：知识检索接口 `POST /api/v1/indices/knowledge/search` 适合自定义生成流程（拿到排序切片后自行拼 [prompt](../guides/prompt.md) 调模型）；知识问答接口 `POST /api/v2/apps/knowledge/chat` 通过 SSE 流式返回规划、工具调用、生成三阶段，适合开箱即用。二者用 API Key Bearer 鉴权，Base URL 为 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com`，默认 25 QPS。
- **开源框架集成**：LlamaIndex（Python）用于读取本地文件上传建云端知识库并构建 RAG 应用；Spring AI Alibaba（Java）用于集成智能体/工作流应用并检索百炼知识库。均以 [API Key 鉴权](api-key.md)。
- **本地知识库 RAG**：检索在本地执行、生成调用通义千问 API，适合需要灵活切分与自选嵌入模型的场景。
- **应用接入渠道**：RAG 应用可通过 AppFlow 接入网站、企业微信、微信公众号、钉钉等渠道，为回答覆盖私域问题。

## RAG 流水线与底层模型

一次典型 RAG 调用可拆为三阶段，每阶段对应可优化的环节与模型：

1. **建立索引**：文档切分（智能切分）、Meta 信息抽取、生成向量。文本向量推荐 text-embedding-v4（Qwen3-Embedding 系列），支持 2048/1536/1024/768/512 等多种维度；多模态检索用 qwen3-vl-embedding / multimodal-embedding-v1。
2. **检索召回**：向量检索 + 关键词检索混合，再经 Rerank 精排。排序模型推荐 qwen3-rerank（文本，支持 100+ 语种）与 qwen3-vl-rerank（多模态），`gte-rerank` 将于 2026-05-30 下线。
3. **生成答案**：将召回切片与用户提问一并送入大模型（如 qwen-max、qwen3.6-plus/qwen3.7-plus 等）生成回答。

## 关键参数与配置

云端知识库侧：

- **相似度阈值**：仅语义相似度高于阈值的切片才被召回，阈值过高会导致全部被过滤（如调到 0.60 可能无召回）。
- **召回片段数 / 最大召回数量（TopK/K）**：取值 1–20，复杂问题可适当增大以补全答案，但会增加 Token 消耗，推荐「按拼装长度」策略。
- **权重**：多知识库召回时按信息源重要性分配，**仅在同类型知识库之间生效**。
- **Meta 信息抽取**：以 key-value 附加到切片，提升检索准确性并降低 Token 消耗；支持常量、变量、大模型、正则、关键词五种取值方式。**知识库创建后无法再配置 metadata 抽取**。
- **智能切分 / 多轮对话改写**：均在创建知识库时配置，创建时未开启则后续无法补开（除非重建）。
- 检索服务全局参数：知识库路由、混排模型（qwen3-rerank / qwen3-rerank(hybrid) / qwen3-vl-rerank）、混排模式（问答/相似/自定义）；每库可独立配置向量/关键词 TopK（1–100）、排序模型、相似度阈值、标签过滤。

LlamaIndex 侧关键参数：

- `Settings.llm = DashScope(model_name="qwen-max")`：生成回答调用的大模型。
- `similarity_top_k`：返回相似度最高的检索结果数（示例 5）。
- `similarity_cutoff`：过滤检索结果的最低相似度阈值（示例 0.4）。
- `top_n`：重排后返回的结果数（示例 1）。
- 后处理 `node_postprocessors`：`SimilarityPostprocessor`（按阈值过滤）、`DashScopeRerank(model="gte-rerank")`（重排）、`response_mode="tree_summarize"`（响应聚合方式）。

本地 RAG 侧关键参数：模型选择、温度、最大回复长度、携带上下文轮数；召回片段数、相似度阈值（为 0 时不剔除）；嵌入模型默认用百炼 embedding API，也可换本地 GTE 向量模型；受限流约束，单文件建议不超过 100 MB。

## 效果优化建议

RAG 效果由建立索引、检索召回、生成答案三阶段共同决定。建议先建立至少 100 组问题的评估基线（覆盖事实型/比较型/教程型/分析型），再针对失败用例（大模型打分 < 4）逐项诊断：

- 检索无效 → 补充知识、优化排版、统一实体、开启多轮对话改写；
- 召回不相关 → 标签过滤、元数据结构化搜索；
- 切片不完整 → 智能切分 + 人工修正；
- 重排不佳 → 调整相似度阈值与召回片段数；
- 模型理解有误 → 更换为参数更多的商业模型。

## 关联主题页

- [knowledge base](../guides/knowledge-base.md)
- [frameworks](../api/frameworks.md)
- [knowledge](../api/knowledge.md)
- [application use cases](../guides/application-use-cases.md)
- [use cases](../guides/use-cases.md)
- [vector and sort](../api/vector-and-sort.md)


