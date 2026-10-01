# knowledge base

阿里云百炼知识库（Knowledge Base）是 RAG（[检索增强生成](../concepts/rag.md)）能力的核心载体，提供文档、表格、图片、音视频等多模态数据的解析、切片、向量化、索引构建与语义检索服务。它既可作为独立检索单元使用，也可与大模型深度集成，支撑知识问答、智能客服、Agent 记忆等场景。所有知识库均运行在业务空间（Workspace）内，资源隔离、权限可控。

## 支持的模型/功能

知识库本身不直接调用生成模型，但其检索结果可被多种模型消费；同时，知识库的构建与检索流程依赖多个专用模型：

- **嵌入模型（Embedding）**：默认使用 `text-embedding-v4`，用于将文本切片转为向量，支持中英文混合语义匹配。该模型在创建知识库时选定且不可更改，详见[创建知识库](raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。
- **重排模型（Rerank）**：如 `qwen3-rerank`（纯文本）、`qwen3-vl-rerank`（多模态），用于对初步召回结果进行精排，提升相关性。可在[知识检索](raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)或[知识问答](raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)的服务配置中按知识库独立启用。
- **解析模型**：支持 `电子文档解析`、`文档智能解析`（OCR+版面恢复）、`大模型文档解析` 和 `Qwen-VL 解析`，适配不同格式文档。选择逻辑见[创建知识库](raw/application-user-guide/knowledge-base/rag-knowledge-base.md)的“选择解析方式”章节。
- **生成模型**：知识问答服务支持绑定 Qwen 系列模型（如 `qwen3.6-plus`），通过 `/api/v2/apps/knowledge/chat` 接口调用，实现流式回答与引用标注。

核心功能覆盖全链路：从文件上传、自动解析、智能切片、向量化索引，到单库检索、多库联合检索（知识检索服务）、带引用的自然语言问答（知识问答服务），以及 Playground 交互式调试。

## 关键参数

知识库行为由多个层级参数共同决定，需按用途区分配置位置：

- **切片参数**（创建时固定）：`切片方式`（智能切分/按长度/按页等）、`最大分段长度`（10–6000 token，默认 600）。这些在[导入数据](raw/application-user-guide/knowledge-base/data-connection-overview/documents.md)步骤中配置，创建后不可修改。
- **检索参数**（服务级可调）：
  - `初步向量检索 TopK` / `初步关键词检索 TopK`：控制各通道初步召回数量（1–100）；
  - `相似度阈值`（0.01–1.0）：过滤低分切片；
  - `最大召回数量`（1–20）：最终返回切片数；
  - `Query 改写`：开关控制是否对用户输入进行语义优化；
  - `标签过滤`：按文档 `tags` 字符串数组精确限定检索范围。
- **服务级高级参数**：
  - `知识库路由`：开启后由大模型自动判断应查询哪些知识库（多库联合场景）；
  - `混排模型`：对多库结果统一重排，支持 `qwen3-rerank(hybrid)` 等模式；
  - `排序模型模式`：`问答模式`（优先匹配回答能力）或 `相似模式`（优先匹配语义）。

> **注意**：`最大分段长度` 的单位是 token，而非字符或字节；不同嵌入模型对 token 的计数方式可能略有差异，实际切片 token 数以系统解析结果为准。

## 使用方式

知识库可通过控制台、API、CLI 及第三方框架多种方式接入：

- **控制台快速验证**：进入 [Playground](https://bailian.console.aliyun.com/cn-beijing/rag/playground)，选择知识库并切换“知识问答”或“知识检索”模式，实时查看检索切片与模型回答，适合效果调优与问题排查。
- **API 集成**：
  - 底层单库检索：`POST /api/v1/indices/rag/index/retrieve`，需传 `index_id`、`query`、`top_k`，返回原始召回节点；
  - 应用级联合检索：`POST /api/v1/indices/knowledge/search`，需传 `agent_id`（对应知识检索服务 ID），检索策略由服务配置驱动；
  - RAG 问答：`POST /api/v2/apps/knowledge/chat`，SSE 流式响应，支持多轮对话历史传递。
- **CLI 调试**：使用 `bl knowledge search --agent-id <检索服务ID>` 或 `bl knowledge chat --agent-id <问答服务ID>`，命令简洁，适合本地脚本与 Agent 集成。
- **第三方平台**：支持 Dify（外部知识库）、Coze（MCP/API 插件）、n8n（HTTP 节点）、LangChain（自定义 Retriever）等，基础均为调用上述 DashScope API，详见[第三方平台接入](raw/application-user-guide/knowledge-base/integration/third-party.md)。

## 限制和注意事项

- **地域与账号限制**：知识库功能在中国站仅支持华北2（北京）地域，在国际站仅支持新加坡地域；子账号需具备 `AliyunBailianDataFullAccess` 权限并加入目标业务空间，详见[知识库API指南](raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。
- **容量硬限**：单业务空间最多 50 个知识库；单知识库最多 100,000 个文档；单次上传最多 50 个文件；切片内容长度上限 6000 字；标签单个最多 32 字符。超出需拆分知识库或申请工单扩容。
- **免费额度与计费**：新用户享 720 小时标准版免费额度（30 天内有效），老用户额度截至 2026 年 2 月 3 日；2026 年 1 月 4 日起正式计费，费用含规格费（标准版 0.03 元/小时，旗舰版按 RCU 计费）与模型调用费。删除知识库将永久清除数据且无法恢复。
- **同步与更新**：OSS 等外部数据源支持定时同步（一分钟/一小时/一天），但同步后需等待解析与向量化完成才可检索；源文件删除不影响百炼平台副本，需手动清理。
- **切片不可变性**：切片策略（方式、长度）在知识库创建时锁定，后续无法修改。若需调整，必须新建知识库并重新导入数据。

> **注意**：文档 1 中提到的 CLI 命令 `bl knowledge retrieve` 在文档 18 中已明确标注为“已弃用”，推荐改用 `bl knowledge search --agent-id` 调用已发布的检索服务，以获得重排等高级能力。

## 来源文档

- [快速开始](../../raw/application-user-guide/knowledge-base/quickstart.md)
- [核心概念](../../raw/application-user-guide/knowledge-base/concepts.md)
- [数据接入](../../raw/application-user-guide/knowledge-base/data-connection-overview.md)
- [数据集](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-connection.md)
- [文档管理与解析](../../raw/application-user-guide/knowledge-base/data-connection-overview/documents.md)
- [切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)
- [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-sync-guide.md)
- [知识服务](../../raw/application-user-guide/knowledge-base/service.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)
- [最佳实践](../../raw/application-user-guide/knowledge-base/best-practices.md)
- [多轮对话：正确传递工具调用历史](../../raw/application-user-guide/knowledge-base/best-practices/multi-turn-chat.md)
- [文件自动打标：用大模型生成文档标签](../../raw/application-user-guide/knowledge-base/best-practices/auto-tag.md)
- [应用集成](../../raw/application-user-guide/knowledge-base/integration.md)
- [接入 AgentScope](../../raw/application-user-guide/knowledge-base/best-practices/knowledge-as-memory.md)
- [服务渠道](../../raw/application-user-guide/knowledge-base/integration/channels.md)
- [快速配置到 Agent](../../raw/application-user-guide/knowledge-base/integration/agent-cli.md)
- [第三方平台接入](../../raw/application-user-guide/knowledge-base/integration/third-party.md)
- [使用 CLI](../../raw/application-user-guide/knowledge-base/integration/cli.md)
- [参考](../../raw/application-user-guide/knowledge-base/reference.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-log-monitoring.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)
- [更新日志](../../raw/application-user-guide/knowledge-base/changelog.md)
- [创建知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [容量与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [Playground](../../raw/application-user-guide/knowledge-base/playground.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)


