# RAG API 与知识库功能对比

本文旨在帮助开发者清晰区分百炼平台中 **RAG API（面向程序化集成的底层能力接口）** 与 **知识库（Knowledge Base，面向场景化服务的统一抽象载体）** 的定位、能力边界与协作关系。二者并非互斥替代方案，而是分层协同的设计：**知识库是 RAG 能力的语义化封装单元，RAG API 是驱动知识库全生命周期与运行时调用的技术底座**。准确理解其差异，是构建稳定、可维护、可扩展 RAG 应用的关键前提。

## 关键维度对比

| 维度 | RAG API | 知识库（Knowledge Base） |
|--------|---------|---------------------------|
| **本质定位** | **能力接口集合**：提供知识管理（创建/更新/删除知识库、文档、切片、数据源）与知识应用（检索、问答、Agent 封装）的标准化 RESTful 接口 | **服务实体单元**：多模态知识的解析、切片、向量化、索引与检索的**逻辑容器**；是 RAG 流程的最小可部署、可配置、可复用的服务实例 |
| **输入格式** | 高度结构化 JSON 请求体，严格依赖参数命名（如 `index_id`、`docIds`、`agent_id`）、大小写与嵌套层级；需显式指定模型名（`embeddingModelName`）、场景类型（`knowledgeScene`）等元信息 | 输入为原始数据（文件/URL/文本），由平台自动完成解析、切片与向量化；用户通过控制台或 API 配置参数（如切片长度、解析方式），但**不直接构造向量或切片内容** |
| **输出格式** | 标准化 JSON 响应（含 `code`/`message`/`data`）；流式问答接口（`/api/v2/apps/knowledge/chat`）强制返回 SSE（`text/event-stream`）事件流，含 `answer`、`references`、`status` 等字段 | 控制台 Playground 直接展示可视化检索结果（高亮切片+引用来源）与自然语言回答；API 输出与 RAG API 一致（因底层复用相同接口），但**知识库本身不产生独立输出格式** |
| **支持模型** | **完全显式可控**：<br>• 嵌入模型：`embeddingModelName`（文本）、`multimodalEmbeddingModelName`（多模态）<br>• 重排模型：`rerankModelName`（知识库级或 Agent 级）<br>• 生成模型：`agent_model`（Agent 配置中指定） | **默认绑定 + 可选增强**：<br>• 嵌入模型：创建时选定且**不可更改**（默认 `text-embedding-v4`）<br>• 重排模型：服务级按需启用（如 `qwen3-rerank`），支持多模态重排<br>• 生成模型：在知识问答服务中绑定（如 `qwen3.6-plus`），非知识库固有属性 |
| **API 端点** | 分散式细粒度接口：<br>• 管理类：`/api/v1/indices/rag/index/create_v2`、`/api/v1/connector/dash/addFile`<br>• 运行类：`/api/v1/indices/knowledge/search`（需 `agent_id`）、`/api/v2/apps/knowledge/chat`（需 `agent_id`） | **无独立端点**；所有操作均通过 RAG API 实现。知识库 ID（`index_id`）是多数接口的必传路径/参数，但**知识库本身不是 API 资源路径**（如不存在 `/api/v1/knowledge_bases/{id}`） |
| **计费方式** | **按调用行为计费**：<br>• 知识库管理操作（创建、删除、导入）：按次计费<br>• 检索/问答调用：按请求次数 + 模型 token 消耗计费<br>• Agent 调用：计入对应 Agent 的资源消耗 | **按资源规格与使用时长计费**：<br>• 知识库实例：按小时计费（标准版 0.03 元/小时，旗舰版按 RCU）<br>• 模型调用费：独立于知识库规格，按实际使用的嵌入/重排/生成模型计费<br>• **免费额度覆盖知识库实例时长与部分 API 调用** |
| **典型场景** | • 自动化知识库流水线（CI/CD 集成）<br>• 多租户动态知识库管理（按需创建/销毁）<br>• 定制化 Agent 编排（混合多个知识库+外部工具）<br>• 与 LangChain/LlamaIndex 等框架深度集成（自定义 Retriever/Agent） | • 快速验证 RAG 效果（Playground 调试）<br>• 构建标准化知识服务（如客服知识库、产品文档中心）<br>• 多库联合检索（通过知识检索服务路由）<br>• 低代码/无代码应用接入（Dify/Coze 插件） |

## 适用场景建议

### ✅ 选择 **RAG API** 当：
- 需要**完全掌控知识工程全流程**：例如，从 OSS 自动拉取日志文件 → 解析为结构化文档 → 按业务标签切片 → 动态创建知识库 → 绑定特定重排模型 → 发布为 Agent → 集成到内部工单系统。
- 构建**高定制化 AI Agent**：需组合多个知识库、外部 API、数据库查询，并通过 `agent_config` 精确配置每一步策略（如 `kb_search_configs` 中为不同知识库设置不同 `top_k` 和 `rerankModelName`）。
- 实现**自动化运维与治理**：批量创建/更新/下线知识库，监控 `index_job/status`，根据错误码（如 `Index.InvalidParameter`）做精细化异常处理。
- 与**开源生态深度耦合**：在 LangChain 中实现 `BailianRetriever`，或在 LlamaIndex 中封装 `BailianIndex`，直接调用底层 `/retrieve` 或 `/search` 接口。

### ✅ 选择 **知识库（Knowledge Base）** 当：
- 追求**开箱即用与快速验证**：上传 PDF/Excel/图片 → 在 Playground 实时测试检索效果与问答质量 → 调整切片长度/相似度阈值 → 导出配置 → 一键发布为服务。
- 构建**标准化、长期运营的知识服务**：如企业内部“政策法规库”、“产品手册库”、“客户服务知识库”，需稳定 SLA、权限隔离、标签管理、定时同步（OSS）与审计日志。
- 需要**多模态统一管理**：同一知识库内混合文档、表格、图片、音视频，并利用 `image_qa` 场景实现图文联合问答，无需分别维护多套 API 调用逻辑。
- 通过**低代码平台交付**：将知识库 ID 注册为 Dify 的 External Tool，或配置为 Coze 的 MCP 插件，让非技术人员也能复用知识能力。

### ⚠️ 注意：二者非二选一，而是协同关系
- **知识库是 RAG API 的核心操作对象**：所有 `index_id`、`docIds`、`agent_id` 均源于知识库的创建与发布流程。
- **RAG API 是知识库能力的唯一技术出口**：无论是控制台点击“发布问答服务”，还是 CLI 执行 `bl knowledge chat`，底层均调用 `/api/v2/apps/knowledge/chat` 等 RAG API。
- **最佳实践是分层使用**：  
  **管理层**（自动化）→ 使用 RAG API 创建/管理知识库；  
  **配置层**（调试优化）→ 通过控制台调整知识库的切片、检索、重排参数；  
  **运行层**（生产调用）→ 通过 RAG API 的 `/knowledge/search` 或 `/knowledge/chat` 接口，传入由知识库发布的 `agent_id` 调用服务。

## 技术选型参考（致开发者）

| 选型考量 | 推荐方案 | 理由 |
|----------|----------|------|
| **是否需要编程控制知识库生命周期？** | RAG API | 知识库本身无 API，所有创建/更新/删除必须通过 RAG API 完成；控制台操作本质是 RAG API 的图形化封装。 |
| **是否需在单次请求中混合多种知识源（文档+表格+图片）？** | RAG API + `multimedia` 知识库 | 仅 RAG API 支持显式指定 `knowledgeScene: multimedia` 并传入 `images` 数组；知识库配置需匹配此场景。 |
| **是否要求切片策略（如最大长度）可动态调整？** | RAG API（新建知识库） | 知识库的切片参数创建后不可变；若需调整，必须调用 RAG API 创建新知识库并重新导入数据。 |
| **是否需对不同知识库应用不同重排模型？** | RAG API（Agent 级配置） | `rerankModelName` 可在 `kb_search_configs` 中为每个知识库单独指定；知识库级重排为全局开关，无法差异化。 |
| **是否追求最低学习成本与最快上线？** | 知识库（控制台 + Playground） | 无需编写代码，5 分钟完成上传→调试→发布；API 文档虽全，但参数校验严格（如 `stream: true` 强制要求），易因细节出错。 |
| **是否需与现有 DevOps 流水线集成？** | RAG API | 支持 CI/CD 自动化（如 GitHub Actions 调用 `curl` 创建知识库），知识库无原生自动化接口。 |

> **关键提醒**：  
> - **不要绕过 Agent 直接调用底层 `/retrieve`**：`/api/v1/indices/rag/index/retrieve` 返回原始切片，无重排、无 Query 改写、无多库路由，效果远低于 `/knowledge/search`。  
> - **`agent_id` 是运行时唯一入口**：无论使用知识库还是 RAG API，生产环境调用检索/问答必须传 `agent_id`（来自 Agent 发布接口），而非 `index_id`。  
> - **计费解耦，需统筹规划**：知识库实例费用（按小时）与 API 调用费用（按次/token）独立计算，高并发问答场景需同时评估两者成本。  

通过本对比，开发者可依据自身项目阶段（POC/量产）、团队能力（全栈/低代码）、系统架构（微服务/单体）与运维需求（自动化/人工），做出清晰、可持续的技术决策。

## 被对比主题页

- [rag api](../api/rag-api.md)
- [knowledge base](../guides/knowledge-base.md)


