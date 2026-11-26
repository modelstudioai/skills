# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，简称 RAG）是一种将大语言模型（LLM）与外部知识源动态结合的技术范式：在模型生成响应前，先从结构化或非结构化知识库中检索相关片段，并将其作为上下文注入提示词，从而提升回答的准确性、时效性与领域专业性。

在百炼平台中，RAG 不是单一功能模块，而是贯穿模型调用、Agent 构建、应用集成和 API 服务的横切能力底座。它统一由 Knowledge API（原 RAG API）提供底层支撑，上层通过标准化配置项暴露给开发者，无需自行搭建向量数据库或编写检索逻辑。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）开发**：  
  - 新版 Agent（Agent 2.0）和旧版 Flow Agent 均原生支持 RAG。知识库检索结果自动拼接至模型输入上下文（占用 [Token](token.md)），开发者仅需在控制台关联已发布的知识检索服务，选择 `ALWAYS` 或 `ON_DEMAND` 触发模式。  
  - 检索内容可与插件调用、记忆、联网搜索等能力并行协同，例如：“先查知识库中的售后政策，再调用订单查询插件确认用户订单状态”。

- **百炼应用（Website/企微/钉钉/公众号等渠道）**：  
  - 所有渠道集成均基于 RAG 架构。开发者上传 PDF/DOCX/XLSX 等私域文档构建知识库后，在应用配置页开启“知识库增强”，即可让 AI 助手基于企业真实资料作答，无需修改前端代码或重训模型。

- **CLI 与低代码工具链**：  
  - 百炼 CLI 的 `bl rag query` 命令可直接调试检索效果；AppFlow 连接器在构建 AI 助手流时，自动将 RAG 检索节点作为标准处理单元接入，支持与条件分支、消息格式化等组件组合。

- **API 直接调用（Knowledge API）**：  
  - 开发者可通过 `/rag/retrieval/query` 接口独立发起语义检索，获取带分数的文本片段列表；也可调用 `/rag/agent/chat` 发起端到端问答，由平台自动完成检索 + 重排序 + LLM 生成全流程。

## 关键参数和配置

以下参数在不同层级中统一生效，推荐显式配置以保障效果可控：

| 参数名 | 类型 | 默认值 | 说明 | 配置位置 |
|--------|------|--------|------|----------|
| `top_k` | 整数 | `3` | 检索返回的最相关片段数量（影响上下文长度与精度） | 应用配置页 > 知识库 > 检索策略；或 Knowledge API 请求体 `top_k` 字段 |
| `similarity_threshold` | 浮点数（0–1） | `0`（不过滤） | 仅保留相似度 ≥ 该值的片段，避免噪声注入 | 同上；API 请求体 `similarity_threshold` |
| `retrieval_mode` | 字符串 | `"ALWAYS"` | 取值：`"ALWAYS"`（每次必检）、`"ON_DEMAND"`（仅当用户提问含关键词如“政策”“手册”时触发） | 应用配置页；Agent 配置 JSON 中 `retrieval.mode` |
| `rerank_model_name` | 字符串 | `"qwen3-rerank"` | 重排序模型，用于对初检结果二次打分排序（提升 top-1 准确率） | 知识库创建/更新时指定；API 响应中返回实际生效值 |
| `embedding_model_name` | 字符串 | `"text-embedding-v4"` | 向量化模型，决定知识库索引质量（建议与业务场景匹配：通用问答选 `text-embedding-v4`，中文长文档选 `qwen3.7-text-embedding`） | 创建知识库时显式指定，不可变更 |

> ⚠️ 注意：`top_k` 和 `similarity_threshold` 共同控制注入上下文的信息密度——过高易引入噪声，过低可能导致关键信息缺失。生产环境建议从 `top_k=3, similarity_threshold=0.35` 起调优，并结合日志分析 `retrieval_hits` 字段验证召回质量。

## 面向开发者，简洁实用

- ✅ **快速启用**：控制台创建知识库 → 上传文档 → 发布检索服务 → 在应用/Agent 中一键关联 → 完成。全程无代码。
- ✅ **调试友好**：所有 RAG 调用均在百炼控制台「监控日志」中透出原始检索片段、相似度分数、重排序前后顺序，便于归因优化。
- ✅ **模型无关**：RAG 是前置增强层，与所选 LLM（`qwen-max`/`deepseek-v4.1-flash`/`kimi-k3.1-pro` 等）完全解耦，更换模型不影响知识检索逻辑。
- ❌ **不推荐**：手动拼接检索结果到 prompt 字符串中（易超上下文、难维护）；在 Agent 中重复调用 `bl rag query` + `bl model invoke`（应使用内置 RAG 节点，保障原子性与计费一致性）。
- 📌 **最佳实践**：  
  - 文档预处理优先用 ParseX（支持表格/公式/多栏 PDF）；  
  - 高频问答场景可开启 Wiki 抽取（旗舰版知识库），自动生成 FAQ 索引提升首屏命中率；  
  - 对于强时效性需求（如股价、订单状态），RAG 应与插件/联网搜索配合，而非替代。

## 关联主题页

- [getting started](../guides/getting-started.md)
- [rag api](../api/rag-api.md)
- [application use cases](../guides/application-use-cases.md)
- [use cases](../guides/use-cases.md)
- [agent legacy](../guides/agent-legacy.md)
- [token plan best practice](../guides/token-plan-best-practice.md)


