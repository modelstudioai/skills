# knowledge base

阿里云百炼知识库（Knowledge Base）是面向 RAG 场景的托管式向量检索服务，支持文档、表格、图片、音视频等多模态数据的解析、切片、向量化与联合检索。它提供统一的 API 接口和多种集成方式（REST API、MCP、CLI、Agent Skill），可作为 AI 应用的私有知识记忆体，与大模型协同生成有依据的回答。

## 支持的模型/功能

知识库本身不直接提供生成模型，但深度集成以下模型能力以支撑完整 RAG 链路：

- **嵌入模型（Embedding）**：默认使用 `text-embedding-v4`，创建知识库时可选；该模型决定文本语义向量的质量，直接影响召回精度 [创建知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。
- **重排模型（Rerank）**：支持 `qwen3-rerank`（纯文本）、`qwen3-vl-rerank`（多模态）等系列模型，在检索服务或问答服务中配置，用于对初步召回结果进行精排 [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)。
- **生成模型（Generation）**：问答服务支持绑定 Qwen 系列（如 `qwen3.6-plus`）、DeepSeek 等大模型，负责基于检索片段生成自然语言回答 [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)。

核心功能包括：
- 多源数据接入（OSS、飞书、钉钉、语雀、SharePoint、MySQL 等）；
- 智能切片（智能切分、按页、按标题等）与元数据抽取；
- 单库检索、多库联合检索（含路由与混排）；
- RAG 问答（[流式输出](../concepts/streaming-output.md)、引用标注、拒答/防泄漏控制）；
- 自动打标、定时同步、Playground 交互调试。

> **注意**：文档 21 明确指出知识库 API 在中国站仅支持华北2（北京）地域，在国际站仅支持新加坡地域，其他地域（如德国法兰克福）不支持。而文档 18 的快速开始示例未提及地域限制，实际部署时需严格遵循文档 21 的约束。

## 关键参数

| 参数 | 说明 | 取值范围/默认值 | 文档依据 |
|------|------|----------------|----------|
| `top_k` | 检索返回的切片数量 | 1–20（问答服务）；1–100（检索服务） | [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)、[知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md) |
| `max_chunk_length` | 切片最大 token 数 | 10–6000，默认 600 | [切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md) |
| `similarity_threshold` | 过滤低分切片的相似度阈值 | 0.01–1.0 | [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md) |
| `RCU`（Retrieval Compute Unit） | 旗舰版知识库并发能力单位，1 RCU ≈ 50 QPS | 1–200 | [知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md) |
| `agent_id` | 知识检索/问答服务的唯一标识符，用于 API 调用 | 字符串（如 `aid-xxxxxxxx`） | [服务渠道](../../raw/application-user-guide/knowledge-base/integration/channels.md) |

## 使用方式

### 1. 控制台快速验证
- **Playground**：选择知识库，切换“知识问答”或“知识检索”模式，输入问题实时查看召回与回答效果 [Playground](../../raw/application-user-guide/knowledge-base/playground.md)。
- **API 调试**：在知识问答/检索服务详情页点击“API 调试”，获取 endpoint、`agent_id` 和请求示例。

### 2. API 集成（推荐生产环境）
- **应用级联合检索**（推荐）：调用 `/api/v1/indices/knowledge/search`，传入 `query` 和 `agent_id`，策略由服务端配置驱动。
- **底层单库检索**：调用 `/api/v1/indices/rag/index/retrieve`，传入 `index_id`、`query`、`top_k`，适用于简单直连场景。
- **流式问答**：调用 `/api/v2/apps/knowledge/chat`，设置 `Accept: text/event-stream`，接收 SSE 流式响应。

### 3. 多种客户端接入
- **CLI**：使用 `bailian-cli` 命令行工具快速调试，如 `bl knowledge search --query "xxx" --agent-id <id>` [使用 CLI](../../raw/application-user-guide/knowledge-base/integration/cli.md)。
- **Agent Skill**：为 Claude Code、Qoder 等编码助手安装 `alibabacloud-bailian-rag-knowledgebase` 技能包，自动加载并支持自然语言提问 [快速配置到 Agent](../../raw/application-user-guide/knowledge-base/integration/agent-cli.md)。
- **第三方平台**：Dify、Coze、n8n、LangChain 均可通过 DashScope API 或 MCP 协议接入 [第三方平台接入](../../raw/application-user-guide/knowledge-base/integration/third-party.md)。

## 限制和注意事项

- **容量限制**：单业务空间最多 50 个知识库；单知识库最多 100,000 份文档；单文件上传上限为 150 MB（PDF/DOCX）或 512 MB（音视频）；切片最大长度 6000 token [容量与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。
- **地域与权限**：知识库 API 仅支持北京（中国站）和新加坡（国际站）；子账号需被授予 `AliyunBailianDataFullAccess` 策略并加入对应业务空间才能操作 [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。
- **计费关键点**：费用 = 规格费（标准版 0.03 元/小时，旗舰版 0.2 元/RCU/小时） + 模型调用费（Embedding/Rerank/Generation）；免费额度（720 小时）仅抵扣标准版规格费，不覆盖模型费用 [知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)。
- **配置不可变性**：切片方式、最大分段长度、嵌入模型等在知识库创建后不可更改，需在导入数据时审慎配置 [切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)。
- **日志与监控**：检索日志默认投递至 SLS，需手动开通监控配置；关闭日志开关仅停止新日志投递，历史日志仍计费，需在 SLS 控制台手动删除 LogStore [知识库日志与监控](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-log-monitoring.md)。

## 来源文档

- [更新日志](../../raw/application-user-guide/knowledge-base/changelog.md)
- [参考](../../raw/application-user-guide/knowledge-base/reference.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-log-monitoring.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)
- [应用集成](../../raw/application-user-guide/knowledge-base/integration.md)
- [快速配置到 Agent](../../raw/application-user-guide/knowledge-base/integration/agent-cli.md)
- [第三方平台接入](../../raw/application-user-guide/knowledge-base/integration/third-party.md)
- [使用 CLI](../../raw/application-user-guide/knowledge-base/integration/cli.md)
- [最佳实践](../../raw/application-user-guide/knowledge-base/best-practices.md)
- [多轮对话：正确传递工具调用历史](../../raw/application-user-guide/knowledge-base/best-practices/multi-turn-chat.md)
- [服务渠道](../../raw/application-user-guide/knowledge-base/integration/channels.md)
- [数据接入](../../raw/application-user-guide/knowledge-base/data-connection-overview.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)
- [切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)
- [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-sync-guide.md)
- [Playground](../../raw/application-user-guide/knowledge-base/playground.md)
- [核心概念](../../raw/application-user-guide/knowledge-base/concepts.md)
- [快速开始](../../raw/application-user-guide/knowledge-base/quickstart.md)
- [创建知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [容量与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [数据集](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-connection.md)
- [文档管理与解析](../../raw/application-user-guide/knowledge-base/data-connection-overview/documents.md)
- [文件自动打标：用大模型生成文档标签](../../raw/application-user-guide/knowledge-base/best-practices/auto-tag.md)
- [接入 AgentScope](../../raw/application-user-guide/knowledge-base/best-practices/knowledge-as-memory.md)
- [知识服务](../../raw/application-user-guide/knowledge-base/service.md)


