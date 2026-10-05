# knowledge base

知识库（Knowledge Base）是阿里云百炼平台 RAG（[检索增强生成](../concepts/rag.md)）能力的核心载体，用于结构化存储、向量化索引和高效检索企业私有文档、表格、图片等多模态数据。它通过解析、切片、嵌入与索引构建完整处理链路，并支持通过控制台 Playground 快速验证、API/CLI 集成到应用，以及与 Agent 框架深度协同。所有知识库均运行在业务空间内，资源隔离、权限可控。

## 支持的模型与功能

知识库本身不直接运行大模型，但其检索与问答服务深度集成以下模型能力：

- **嵌入模型（Embedding）**：默认使用 `text-embedding-v4`，支持中英文语义向量生成；创建知识库时选定，**创建后不可更改** [创建知识库](../../raw/application-user-guide/knowledge-base/data-connection-overview/rag-knowledge-base.md)。
- **重排模型（Rerank）**：支持 `qwen3-rerank`（纯文本）、`qwen3-vl-rerank`（多模态）等，用于对初步召回结果进行精排，提升相关性 [知识检索](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-retrieval.md)。
- **生成模型（LLM）**：问答服务支持 `qwen3.6-plus` 等 Qwen 系列模型，可配置 `temperature`、`enable_thinking` 等参数 [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)。

核心功能覆盖全生命周期：
- **多源接入**：支持上传文件、同步 OSS/飞书/钉钉/语雀/SharePoint，以及连接 MySQL/PostgreSQL/PolarDB-X 数据库 [数据集](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-connection.md)。
- **多模态支持**：除标准文档搜索外，还提供数据查询（NL2SQL）、图片问答（多模态 Embedding）、音视频搜索（转写+定位）等专用知识库类型 [创建知识库](../../raw/application-user-guide/knowledge-base/data-connection-overview/rag-knowledge-base.md)。
- **服务化输出**：提供两种标准化服务——**知识检索服务**（返回原始切片）和**知识问答服务**（返回带引用的自然语言回答），均支持多知识库联合、权重配置与独立参数调优 [知识服务](../../raw/application-user-guide/knowledge-base/service.md)。

> **注意**：文档 5 中提及“新版 Connector 已上线，旧版数据连接需在 2026 年 9 月 30 日前完成迁移”，而文档 28（更新日志）最新日期为 2026-07-27，表明该迁移要求仍为当前有效策略，开发者应优先采用新版 Connector 接入智能体场景。

## 关键参数

关键参数贯穿知识库创建、索引构建与服务调用各环节，直接影响检索质量与性能：

- **切片参数**（导入时配置，**创建后不可更改**）：
  - `切片方式`：默认 `智能切分`；其他选项包括按长度、按页、按标题、按正则、按符号切分 [切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)。
  - `最大分段长度`：默认 600 token，范围 10–6000；需根据文档类型调整（如 FAQ 推荐 256，长报告推荐 2048）[RAG效果优化](../../raw/application-user-guide/knowledge-base/best-practices/rag-optimization.md)。

- **检索服务参数**（可动态调整）：
  - `初步向量检索 TopK` / `初步关键词检索 TopK`：范围 1–100，控制初筛召回数量。
  - `相似度阈值`：范围 0.01–1.0，过滤低分切片；值越高越精确，但可能漏召。
  - `最大召回数量`：最终返回切片数，范围 1–20。
  - `混排模型`：启用 `qwen3-rerank` 等可显著提升排序质量 [知识检索](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-retrieval.md)。

- **问答服务参数**：
  - `检索模式`：`极速`（单轮）或 `多轮智能检索`（Agentic，自动 Query 改写与路由）。
  - `生成控制`：`拒答`（不足证据时拒绝回答）、`防泄漏`（防止原文直泄）、`引用`（标注来源）等 [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)。

## 使用方式

### 控制台快速上手
1. **创建知识库**：进入 [知识管理](https://bailian.console.aliyun.com/cn-beijing/rag/knowledge/list)，选择类型（如“文档搜索”）与场景（如“基础文档问答”），上传文件并配置索引 [快速开始](../../raw/application-user-guide/knowledge-base/quickstart.md)。
2. **调试验证**：使用 [Playground](https://bailian.console.aliyun.com/cn-beijing/rag/playground) 选择知识库，切换“知识问答”或“知识检索”模式，实时查看结果与引用 [Playground](../../raw/application-user-guide/knowledge-base/playground.md)。
3. **发布服务**：在 [知识检索](https://bailian.console.aliyun.com/cn-beijing/rag/retrieval/list) 或 [知识问答](https://bailian.console.aliyun.com/cn-beijing/rag/qa/list) 页面创建服务，绑定知识库并配置参数，点击“发布”。

### API/CLI 集成
- **底层检索**（单库）：调用 `/api/v1/indices/rag/index/retrieve`，传 `index_id` 和 `query` [快速开始](../../raw/application-user-guide/knowledge-base/quickstart.md)。
- **应用级检索**（多库）：调用 `/api/v1/indices/knowledge/search`，传 `agent_id`（对应已发布的检索服务）和 `query` [服务渠道](../../raw/application-user-guide/knowledge-base/integration/channels.md)。
- **流式问答**：调用 `/api/v2/apps/knowledge/chat`，支持 SSE 流式响应 [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)。
- **CLI 命令**：`bl knowledge search --agent-id <id> --query "xxx"` 或 `bl knowledge chat --agent-id <id> --message "xxx"` [使用 CLI](../../raw/application-user-guide/knowledge-base/integration/cli.md)。

### 第三方与框架接入
- **Agent 框架**：通过 MCP Server 协议接入 Qoder/Claude Code 等客户端；或编写自定义中间件（如 `KnowledgeStudioRAGMiddleware`）在 AgentScope 中实现 static 注入或 agentic 自主检索 [接入 AgentScope](../../raw/application-user-guide/knowledge-base/best-practices/knowledge-as-memory.md)。
- **低代码平台**：Dify/Coze/n8n/LangChain 均可通过 DashScope REST API 或 MCP 接入 [第三方平台接入](../../raw/application-user-guide/knowledge-base/integration/third-party.md)。

## 限制和注意事项

- **地域与规格限制**：知识库功能在中国站仅支持**华北2（北京）**，国际站仅支持**新加坡**；标准版知识库最高并发为 1 QPS，旗舰版按 RCU（1 RCU ≈ 50 QPS）弹性伸缩 [容量与限制](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-specifications.md)。
- **文件与切片约束**：
  - 单文件上限：PDF/DOCX ≤ 150 MB 或 1000 页；图片 ≤ 20 MB；音视频 ≤ 512 MB [容量与限制](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-specifications.md)。
  - 切片参数（方式、长度）在导入时锁定，无法事后修改；若效果不佳，需重建知识库 [切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)。
- **计费与生命周期**：
  - 自 2026 年 1 月 4 日起正式计费，费用含**规格费**（按小时）与**模型调用费**（Embedding/Rerank/LLM）[知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)。
  - 免费额度（720 小时）仅抵扣**标准版**规格费，且老用户有效期至 2026-02-03，新用户仅限开通后 30 天内使用 [知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)。
- **安全与运维**：
  - 删除知识库或文档为**永久操作，不可恢复**；同步规则导入的文件为独立副本，源文件删除不影响百炼中数据 [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-sync-guide.md)。
  - 所有检索调用日志自动投递至 SLS，可用于审计、监控与告警 [知识库日志与监控](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-log-monitoring.md)。

## 来源文档

- [快速开始](../../raw/application-user-guide/knowledge-base/quickstart.md)
- [核心概念](../../raw/application-user-guide/knowledge-base/concepts.md)
- [数据接入](../../raw/application-user-guide/knowledge-base/data-connection-overview.md)
- [Playground](../../raw/application-user-guide/knowledge-base/playground.md)
- [数据集](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-connection.md)
- [创建知识库](../../raw/application-user-guide/knowledge-base/data-connection-overview/rag-knowledge-base.md)
- [文档管理与解析](../../raw/application-user-guide/knowledge-base/data-connection-overview/documents.md)
- [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-sync-guide.md)
- [切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-retrieval.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)
- [知识服务](../../raw/application-user-guide/knowledge-base/service.md)
- [最佳实践](../../raw/application-user-guide/knowledge-base/best-practices.md)
- [多轮对话：正确传递工具调用历史](../../raw/application-user-guide/knowledge-base/best-practices/multi-turn-chat.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/best-practices/rag-optimization.md)
- [接入 AgentScope](../../raw/application-user-guide/knowledge-base/best-practices/knowledge-as-memory.md)
- [应用集成](../../raw/application-user-guide/knowledge-base/integration.md)
- [文件自动打标：用大模型生成文档标签](../../raw/application-user-guide/knowledge-base/best-practices/auto-tag.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/integration/rag-knowledge-base-api-guide.md)
- [快速配置到 Agent](../../raw/application-user-guide/knowledge-base/integration/agent-cli.md)
- [服务渠道](../../raw/application-user-guide/knowledge-base/integration/channels.md)
- [第三方平台接入](../../raw/application-user-guide/knowledge-base/integration/third-party.md)
- [使用 CLI](../../raw/application-user-guide/knowledge-base/integration/cli.md)
- [参考](../../raw/application-user-guide/knowledge-base/reference.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-log-monitoring.md)
- [容量与限制](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-specifications.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)
- [更新日志](../../raw/application-user-guide/knowledge-base/changelog.md)


