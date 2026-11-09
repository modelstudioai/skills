# knowledge base

知识库（Knowledge Base）是百炼平台 RAG 能力的核心载体，将文档、切片、嵌入模型与索引配置封装为可复用的逻辑单元，对外提供检索与问答能力。它支持多模态数据类型与多种检索范式，既可通过控制台低代码配置，也支持全 API 自动化集成。知识库并非静态文档集合，而是包含解析、切片、向量化、元数据抽取与索引构建的完整处理链路。

## 支持的模型/功能

知识库本身不直接运行大模型，但其能力深度依赖以下模型与功能协同：

- **嵌入模型**：创建知识库时选定，如 `text-embedding-v4`（默认），决定语义向量质量；该配置不可变，详见[创建知识库](raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。
- **重排（Rerank）模型**：在检索服务中配置，如 `qwen3-rerank`（纯文本）、`qwen3-vl-rerank`（多模态），用于对召回结果精排；未启用时仅做基础向量+关键词混合排序 [知识检索](raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)。
- **生成模型**：绑定于问答服务，如 `qwen3.6-plus`，负责基于检索结果生成自然语言回答 [知识问答](raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)。
- **多模态能力**：图片问答类型知识库依赖 Qwen-VL 等视觉语言模型解析图文混排内容；音视频搜索则调用语音转写与时间戳定位模型。

功能上，知识库支持四类核心类型，对应不同数据形态与检索逻辑：
- **文档搜索**：PDF/DOCX/MD 等非结构化文档，采用向量 + 关键词混合检索；
- **数据查询**：CSV/Excel/RDS 表格，通过 NL2SQL 实现自然语言查表；
- **图片问答**：商品图/设计稿，以多模态 Embedding 为基础，支持图文联合理解；
- **音视频搜索**：录屏/培训视频，经语音转写与片段定位后检索。

> **注意**：文档 27 中“数据知识库”与文档 1 中“数据查询”为同一概念，但术语不一致；实际功能与配置入口均以文档 1 的“数据查询”为准，建议统一使用该术语。

## 关键参数

所有关键参数均在创建或配置阶段设定，部分参数创建后不可修改：

- **切片策略**：包括切片方式（智能切分/按长度/按页/按标题等）与最大分段长度（10–6000 token，默认 600）。该配置在导入数据时确定，创建后不可更改 [切片与向量化](raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)。
- **Metadata 抽取**：在创建知识库的“索引设置”中开启，最多定义 5 个字段（英文+下划线），取值方法支持常量、变量（`file_name`）、大模型抽取、正则或关键词搜索；知识库创建后无法补配，需重建 [创建知识库](raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。
- **标签（Tags）**：用于文档级过滤，单个标签 ≤32 字符，每篇文档最多 100 个；可在导入时批量添加，或导入后通过“更多 → 标签”单独编辑 [文档管理与解析](raw/application-user-guide/knowledge-base/data-connection-overview/documents.md)。
- **检索服务参数**：包括全局的“最大召回数量”（1–20）、“混排模型模式”（问答/相似），以及知识库独立的“相似度阈值”（0.01–1.0）、“初步向量检索 TopK”（1–100）等 [知识检索](raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)。

## 使用方式

知识库需通过服务层（检索服务或问答服务）对外暴露能力，不支持直接调用知识库 ID：

- **控制台快速验证**：使用 Playground 选择知识库，切换“知识问答”或“知识检索”模式，实时调试效果 [Playground](raw/application-user-guide/knowledge-base/playground.md)。
- **API 集成**：
  - 单知识库底层检索：调用 `/api/v1/indices/rag/index/retrieve`，需传 `index_id` 和 `query`，返回原始切片（无重排）；
  - 应用级联合检索：调用 `/api/v1/indices/knowledge/search`，传 `agent_id`（检索服务 ID），由服务配置驱动多库权重、路由与混排 [服务渠道](raw/application-user-guide/knowledge-base/integration/channels.md)；
  - RAG 问答：调用 `/api/v2/apps/knowledge/chat`，流式返回带引用的回答 [知识问答](raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)。
- **CLI 与 Agent 集成**：`bl knowledge search --agent-id <id>` 或通过 Agent Skill（如 Claude Code）自动加载，无需硬编码凭证 [使用 CLI](raw/application-user-guide/knowledge-base/integration/cli.md)。

## 限制和注意事项

- **地域限制**：知识库 API 仅在中国站（华北2 北京）和国际站（新加坡）可用，其他地域（如德国法兰克福）不支持 [知识库API指南](raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。
- **容量上限**：单知识库最多 100,000 文档；单文件上限为 PDF/DOCX 150 MB 或 1000 页，图片 ≤20 MB，音视频 ≤512 MB；切片最大长度 6000 token [容量与限制](raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。
- **不可变配置**：知识库创建后，切片方式、最大分段长度、嵌入模型、Metadata 抽取模板均不可修改，需新建知识库并重新导入 [文档管理与解析](raw/application-user-guide/knowledge-base/data-connection-overview/documents.md)。
- **标签与 Metadata 差异**：标签用于粗粒度过滤（如 `产品_X`），Metadata 用于细粒度结构化筛选（如 `{"product_version": "v2.1"}`）；两者均需在请求中显式指定（`tags` 或 `metadata_filter`），不会自动生效 [RAG效果优化](raw/application-user-guide/knowledge-base/rag-optimization.md)。
- **同步行为**：通过数据集同步的文件（OSS/飞书等）在百炼平台内为独立副本，源文件删除不影响已同步内容；但更新需等待下一次同步周期触发 [知识库定时数据同步指南](raw/application-user-guide/knowledge-base/data-connection-overview/data-sync-guide.md)。

## 来源文档

- [创建知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [容量与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [参考](../../raw/application-user-guide/knowledge-base/reference.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-log-monitoring.md)
- [应用集成](../../raw/application-user-guide/knowledge-base/integration.md)
- [快速配置到 Agent](../../raw/application-user-guide/knowledge-base/integration/agent-cli.md)
- [服务渠道](../../raw/application-user-guide/knowledge-base/integration/channels.md)
- [第三方平台接入](../../raw/application-user-guide/knowledge-base/integration/third-party.md)
- [使用 CLI](../../raw/application-user-guide/knowledge-base/integration/cli.md)
- [最佳实践](../../raw/application-user-guide/knowledge-base/best-practices.md)
- [接入 AgentScope](../../raw/application-user-guide/knowledge-base/best-practices/knowledge-as-memory.md)
- [多轮对话：正确传递工具调用历史](../../raw/application-user-guide/knowledge-base/best-practices/multi-turn-chat.md)
- [文件自动打标：用大模型生成文档标签](../../raw/application-user-guide/knowledge-base/best-practices/auto-tag.md)
- [知识服务](../../raw/application-user-guide/knowledge-base/service.md)
- [数据接入](../../raw/application-user-guide/knowledge-base/data-connection-overview.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)
- [数据集](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-connection.md)
- [文档管理与解析](../../raw/application-user-guide/knowledge-base/data-connection-overview/documents.md)
- [切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)
- [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-sync-guide.md)
- [快速开始](../../raw/application-user-guide/knowledge-base/rag-start-using/quickstart.md)
- [Playground](../../raw/application-user-guide/knowledge-base/playground.md)
- [开始使用](../../raw/application-user-guide/knowledge-base/rag-start-using.md)
- [核心概念](../../raw/application-user-guide/knowledge-base/rag-start-using/concepts.md)


