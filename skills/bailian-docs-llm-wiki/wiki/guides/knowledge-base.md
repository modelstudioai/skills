# knowledge base

阿里云百炼知识库（Knowledge Base）是 RAG（[检索增强生成](../concepts/rag.md)）能力的核心载体，用于结构化管理非结构化/半结构化数据（文档、表格、图片、音视频），并提供[向量化](../concepts/embedding.md)索引、语义检索与大模型问答服务。它支持通过控制台快速创建、Playground 交互调试、API/CLI/MCP 多渠道集成，并可与 AgentScope、Dify 等第三方框架深度对接。

## 支持的模型/功能

知识库本身不直接运行大模型，而是作为数据层与模型层协同工作：  
- **嵌入模型**：默认使用 `text-embedding-v4` 进行[向量化](../concepts/embedding.md)，创建后不可更改；多模态场景可选 `qwen3-vl-rerank` 等重排模型 [切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)。  
- **重排模型（Rerank）**：支持 `qwen3-rerank`（纯文本）、`qwen3-vl-rerank`（多模态）等，用于对初步召回结果精排，提升相关性 [知识检索](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-retrieval.md)。  
- **生成模型**：问答服务中可自由切换 Qwen 系列模型（如 `qwen3.6-plus`），支持配置 `temperature`、`enable_thinking` 等参数 [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)。  
- **核心功能**：包括文档解析（OCR/版面恢复/大模型理解）、智能切片、混合检索（向量+关键词）、标签过滤、元数据抽取、Query 改写、多轮智能检索（Agentic 模式）及图文并茂回复等。

> **注意**：文档 5 和文档 19 对“按标题切分”的适用场景描述存在差异——文档 5 称其适用于“用标题划分独立主题的文档”，而文档 19 补充强调“Markdown 按标题切分”；实际应以 Markdown 等具备显式标题层级的格式为首选，PDF 扫描件等无结构文档不适用该方式。

## 关键参数

所有关键参数均在创建或配置阶段设定，部分创建后不可修改：  
- **切片参数**：`最大分段长度`（10–6000 token，默认 600）、`切片方式`（智能切分/按长度/按页/按标题/正则/符号），创建后不可更改 [切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)。  
- **检索参数**：`初步向量检索 TopK`（1–100）、`相似度阈值`（0.01–1.0）、`最大召回数量`（1–20）、`Query 改写`（开/关），可在知识检索/问答服务中为单个知识库独立配置 [知识检索](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-retrieval.md)。  
- **服务参数**：知识检索服务最多绑定 15 个知识库，问答服务同样上限为 15 个；服务名称 ≤ 40 字符，描述 ≤ 200 字符 [容量与限制](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-specifications.md)。  
- **标签与元数据**：标签为字符串数组，单个标签 ≤ 32 字符，每文档 ≤ 100 个；元数据用于结构化过滤，需在文档列表中手动配置 [RAG效果优化](../../raw/application-user-guide/knowledge-base/best-practices/rag-optimization.md)。

## 使用方式

开发者可通过三类路径接入：  
- **控制台快速验证**：在 [Playground](../../raw/application-user-guide/knowledge-base/playground.md) 中选择知识库、切换问答/检索模式，实时查看引用高亮与切片来源，适合效果调优。  
- **API 集成**：  
  - 单库底层检索：`POST /api/v1/indices/rag/index/retrieve`，需传 `index_id` 和 `query`；  
  - 应用级联合检索：`POST /api/v1/indices/knowledge/search`，只需 `agent_id` 和 `query`，策略由服务配置驱动；  
  - 流式问答：`POST /api/v2/apps/knowledge/chat`，返回 SSE 事件，需传 `agent_id` 和消息历史 [服务渠道](../../raw/application-user-guide/knowledge-base/integration/channels.md)。  
- **命令行与工具链**：使用 `bailian-cli` 命令（如 `bl knowledge search --agent-id <id> --query "xxx"`）进行本地调试；或通过 MCP Server 接入 Qoder/Claude Code 等 AI 编码助手 [使用 CLI](../../raw/application-user-guide/knowledge-base/integration/cli.md)。

## 限制和注意事项

- **地域与规格限制**：知识库功能仅在中国站（华北2 北京）和国际站（新加坡）可用；标准版知识库限 1 QPS 并发，旗舰版按 RCU 计费（1 RCU ≈ 50 QPS），单业务空间最多 50 个知识库 [容量与限制](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-specifications.md)。  
- **文件与切片约束**：单文件上限 150 MB（文档）或 512 MB（音视频）；单知识库最多 100,000 文档；切片内容长度上限 6000 字，标题上限 50 字；切片策略创建后不可修改 [文档管理与解析](../../raw/application-user-guide/knowledge-base/data-connection-overview/documents.md)。  
- **计费与生命周期**：自 2026 年 1 月 4 日起正式计费，费用含规格费（标准版 0.03 元/小时，旗舰版按 RCU）和模型调用费；免费额度（720 小时）仅抵扣标准版规格费，且老用户额度有效期截至 2026 年 2 月 3 日 [知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)。  
- **安全与审计**：所有检索请求自动投递至 SLS 日志服务，字段包含 `request_id`、`pipeline_id`（知识库 ID）、`latency`、`response_code` 等，可用于问题排查与用量分析 [知识库日志与监控](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-log-monitoring.md)。

## 来源文档

- [快速开始](../../raw/application-user-guide/knowledge-base/quickstart.md)
- [Playground](../../raw/application-user-guide/knowledge-base/playground.md)
- [核心概念](../../raw/application-user-guide/knowledge-base/concepts.md)
- [数据接入](../../raw/application-user-guide/knowledge-base/data-connection-overview.md)
- [创建知识库](../../raw/application-user-guide/knowledge-base/data-connection-overview/rag-knowledge-base.md)
- [数据集](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-connection.md)
- [切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)
- [知识服务](../../raw/application-user-guide/knowledge-base/service.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-retrieval.md)
- [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-sync-guide.md)
- [最佳实践](../../raw/application-user-guide/knowledge-base/best-practices.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/best-practices/rag-optimization.md)
- [多轮对话：正确传递工具调用历史](../../raw/application-user-guide/knowledge-base/best-practices/multi-turn-chat.md)
- [文件自动打标：用大模型生成文档标签](../../raw/application-user-guide/knowledge-base/best-practices/auto-tag.md)
- [接入 AgentScope](../../raw/application-user-guide/knowledge-base/best-practices/knowledge-as-memory.md)
- [应用集成](../../raw/application-user-guide/knowledge-base/integration.md)
- [快速配置到 Agent](../../raw/application-user-guide/knowledge-base/integration/agent-cli.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/integration/rag-knowledge-base-api-guide.md)
- [文档管理与解析](../../raw/application-user-guide/knowledge-base/data-connection-overview/documents.md)
- [服务渠道](../../raw/application-user-guide/knowledge-base/integration/channels.md)
- [使用 CLI](../../raw/application-user-guide/knowledge-base/integration/cli.md)
- [第三方平台接入](../../raw/application-user-guide/knowledge-base/integration/third-party.md)
- [参考](../../raw/application-user-guide/knowledge-base/reference.md)
- [容量与限制](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-specifications.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)
- [更新日志](../../raw/application-user-guide/knowledge-base/changelog.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-log-monitoring.md)


