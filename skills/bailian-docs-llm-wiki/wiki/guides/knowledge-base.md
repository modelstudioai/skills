# knowledge base

阿里云百炼知识库（Knowledge Base）是面向企业私有数据构建的 RAG 核心基础设施，支持文档、表格、图片、音视频等多模态数据的解析、切片、向量化与混合检索，并通过检索服务与问答服务对外提供可集成的 API 能力。其设计目标是将非结构化/半结构化知识转化为可被大模型精准引用的语义索引，兼顾检索精度与生成质量。

## 支持的模型/功能

知识库本身不直接运行大模型，但深度集成以下模型能力以支撑完整 RAG 链路：

- **嵌入模型（Embedding）**：默认使用 `text-embedding-v4`，创建知识库时可选，创建后不可更改；支持中英文语义向量生成，用于向量化阶段 [创建知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。
- **重排模型（Rerank）**：支持 `qwen3-rerank`（纯文本）、`qwen3-vl-rerank`（多模态）等系列模型，在检索服务或问答服务中配置，用于对召回结果进行精排 [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)。
- **生成模型（LLM）**：在知识问答服务中绑定 Qwen 系列模型（如 `qwen3.6-plus`），负责基于检索片段生成自然语言回答，并支持 `temperature`、`enable_thinking` 等参数调优 [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)。
- **解析模型**：提供多种文档解析方式，包括电子文档解析、文档智能解析（OCR+版面恢复）、大模型文档解析、Qwen-VL 解析（图文混排）和音视频解析（语音转写+时间戳定位），按需在创建知识库时选择 [创建知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

核心功能覆盖全生命周期：从数据接入（上传文件、OSS/飞书/钉钉/语雀同步）、文档管理（解析、切片、元数据抽取）、索引构建（向量化、存储），到服务化（知识检索、知识问答、Playground 调试），再到可观测性（日志投递至 SLS）与运维（CLI、API、监控告警）。

> **注意**：文档 4 明确指出“旧版数据连接需在 2026 年 9 月 30 日前完成迁移”，而文档 21 的更新日志仅记录“2026-07-27 RAG 知识库文档上线”，未提及迁移状态。开发者应以文档 4 的迁移截止日期为准，避免依赖已标记为过时的数据连接能力。

## 关键参数

知识库行为由多个层级的参数共同控制，关键参数如下：

- **切片参数**：`最大分段长度`（10–6000 token，默认 600）、`切片方式`（智能切分/按长度/按页/按标题/按正则/按符号）。这些参数在[导入数据](../../raw/application-user-guide/knowledge-base/data-connection-overview/documents.md)时配置，创建后不可更改。
- **检索参数**：
  - `TopK`：底层检索接口的 `top_k`（1–5，常用 3–10）；检索/问答服务中的 `初步向量检索 TopK` 和 `初步关键词检索 TopK`（1–100）；以及最终 `最大召回数量`（1–20）。
  - `相似度阈值`（0.01–1.0）：过滤排序后低分切片，值越高越精确但可能漏检。
  - `Query 改写`：开关控制，提升模糊查询匹配度，适用于多轮对话场景 [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)。
- **标签与元数据**：支持为文档添加字符串标签（单个 ≤32 字符，每文档 ≤100 个），用于 `标签过滤`；支持启用 `Metadata 抽取`，从文档中自动提取结构化信息（如日期、作者）用于精准路由 [文档管理与解析](../../raw/application-user-guide/knowledge-base/data-connection-overview/documents.md)。
- **规格参数**：知识库分为标准版（1 QPS，0.03 元/小时）与旗舰版（50–10,000 QPS 可调，0.2 元/RCU/小时），RCU 是并发能力单位（1 RCU ≈ 50 QPS） [知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)。

## 使用方式

知识库可通过控制台、API、CLI 和第三方渠道快速接入：

- **控制台快速验证**：通过 [Playground](../../raw/application-user-guide/knowledge-base/playground.md) 选择知识库并输入问题，实时查看检索切片与模型回答，适合效果调优。
- **API 集成**：
  - 底层检索：`POST /api/v1/indices/rag/index/retrieve`，指定 `index_id` 和 `query`，返回原始召回结果 [快速开始](../../raw/application-user-guide/knowledge-base/quickstart.md)。
  - 应用级检索：`POST /api/v1/indices/knowledge/search`，传入 `agent_id`，由检索服务统一驱动多库混排 [服务渠道](../../raw/application-user-guide/knowledge-base/integration/channels.md)。
  - 流式问答：`POST /api/v2/apps/knowledge/chat`，返回 SSE 流，需处理 `tool_calls` 历史以支持多轮对话 [多轮对话：正确传递工具调用历史](../../raw/application-user-guide/knowledge-base/best-practices/multi-turn-chat.md)。
- **CLI 调试**：使用 `bl knowledge search --agent-id <id> --query "xxx"` 或 `bl knowledge chat --agent-id <id> --message "xxx"` 快速测试，命令行友好 [使用 CLI](../../raw/application-user-guide/knowledge-base/integration/cli.md)。
- **第三方平台**：支持 Dify（外部知识库）、Coze（MCP/API [插件](../concepts/plugin.md)）、n8n（HTTP Request 节点）、LangChain（自定义 Retriever）等，均基于 DashScope REST API [第三方平台接入](../../raw/application-user-guide/knowledge-base/integration/third-party.md)。

## 限制和注意事项

- **地域与账号限制**：知识库功能在中国站仅支持华北2（北京）地域，国际站仅支持新加坡地域；子账号需被授予 `AliyunBailianDataFullAccess` 权限并加入业务空间才能操作 [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。
- **容量硬限制**：单业务空间最多 50 个知识库；单知识库最多 100,000 个文档；单次上传最多 50 个文件；单文档 PDF/DOCX 最大 150 MB 或 1000 页；图片单图 ≤20 MB；音视频单文件 ≤512 MB [容量与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。
- **关键不可变项**：知识库类型、使用场景、切片策略、嵌入模型在创建后均不可修改，如需调整必须重建知识库 [切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)。
- **数据同步行为**：OSS/飞书/钉钉等外部数据源的同步是“副本式”而非“链接式”，源文件删除不影响百炼平台副本；但同步规则不支持增量删除，仅支持新增与更新 [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-sync-guide.md)。
- **免费额度与计费**：新用户享有 30 天内有效的 720 小时免费额度（仅抵扣标准版规格费），老用户额度统一截至 2026 年 2 月 3 日；删除知识库会永久清除数据且无法恢复，务必谨慎操作 [知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)。

## 来源文档

- [快速开始](../../raw/application-user-guide/knowledge-base/quickstart.md)
- [核心概念](../../raw/application-user-guide/knowledge-base/concepts.md)
- [数据接入](../../raw/application-user-guide/knowledge-base/data-connection-overview.md)
- [数据集](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-connection.md)
- [文档管理与解析](../../raw/application-user-guide/knowledge-base/data-connection-overview/documents.md)
- [切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)
- [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-sync-guide.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)
- [最佳实践](../../raw/application-user-guide/knowledge-base/best-practices.md)
- [多轮对话：正确传递工具调用历史](../../raw/application-user-guide/knowledge-base/best-practices/multi-turn-chat.md)
- [文件自动打标：用大模型生成文档标签](../../raw/application-user-guide/knowledge-base/best-practices/auto-tag.md)
- [接入 AgentScope](../../raw/application-user-guide/knowledge-base/best-practices/knowledge-as-memory.md)
- [应用集成](../../raw/application-user-guide/knowledge-base/integration.md)
- [快速配置到 Agent](../../raw/application-user-guide/knowledge-base/integration/agent-cli.md)
- [服务渠道](../../raw/application-user-guide/knowledge-base/integration/channels.md)
- [第三方平台接入](../../raw/application-user-guide/knowledge-base/integration/third-party.md)
- [Playground](../../raw/application-user-guide/knowledge-base/playground.md)
- [使用 CLI](../../raw/application-user-guide/knowledge-base/integration/cli.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-log-monitoring.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)
- [更新日志](../../raw/application-user-guide/knowledge-base/changelog.md)
- [创建知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [参考](../../raw/application-user-guide/knowledge-base/reference.md)
- [知识服务](../../raw/application-user-guide/knowledge-base/service.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [容量与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)


