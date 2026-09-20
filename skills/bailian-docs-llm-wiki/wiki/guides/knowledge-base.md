# knowledge base

阿里云百炼知识库（Knowledge Base）是 RAG（[检索增强生成](../concepts/rag.md)）能力的核心载体，提供文档解析、智能切片、向量化索引、多模态检索与大模型问答一体化服务。它支持从本地文件、OSS、语雀、飞书等数据源接入结构化与非结构化数据，并通过统一 API 或低代码服务配置对外提供可集成的检索与问答能力。

## 支持的模型/功能

知识库本身不直接运行大模型，但深度集成以下模型能力以支撑完整 RAG 链路：

- **嵌入模型**：默认使用 `text-embedding-v4`（中英文语义向量模型），创建知识库时选定且不可更改；[创建知识库](raw/application-user-guide/knowledge-base/data-connection-overview/rag-knowledge-base.md)中明确说明该参数为创建时固定项。
- **重排（Rerank）模型**：支持 `qwen3-rerank`（纯文本）、`qwen3-vl-rerank`（多模态）等，可在[知识检索](raw/application-user-guide/knowledge-base/service/rag-knowledge-retrieval.md)或[知识问答](raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)服务中按需启用，用于对召回结果进行精排。
- **生成模型**：问答阶段支持 Qwen 系列模型（如 `qwen3.6-plus`），在[知识问答](raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)服务配置中选择，支持调节 `temperature` 与 `enable_thinking` 等参数。
- **多模态能力**：图片知识库依赖 `Qwen-VL` 解析与 `qwen3-vl-rerank` 重排；音视频知识库依赖语音转写与时间戳定位模型，详见[核心概念](raw/application-user-guide/knowledge-base/concepts.md)中对知识库类型的定义。

> **注意**：文档 4 与文档 3 对“知识库类型”的描述存在细微差异：文档 4 将“图片问答”列为独立类型，而文档 3 归类为“图片知识库”，二者实质一致，但术语应以文档 4 的控制台实际选项为准。

## 关键参数

所有关键参数均在知识库创建或服务配置阶段设定，部分参数创建后不可修改：

- **切片参数**：`最大分段长度`（10–6000 token，默认 600）、`切片方式`（智能切分/按长度/按页/按标题等），在[导入数据](raw/application-user-guide/knowledge-base/data-connection-overview/documents.md)步骤中配置，**创建后不可更改**。
- **检索服务参数**：`知识库路由`（开/关）、`混排模型`（如 `qwen3-rerank`）、`最大召回数量`（1–20）、各知识库独立的 `初步向量检索 TopK`（1–100）与 `相似度阈值`（0.01–1.0），详见[知识检索](raw/application-user-guide/knowledge-base/service/rag-knowledge-retrieval.md)。
- **问答服务参数**：`检索模式`（极速/多轮智能检索）、`拒答`/`防泄漏`/`引用`等生成控制开关，以及 `文件预解析` 模式（全文引用/切片检索），详见[知识问答](raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)。

## 使用方式

知识库可通过控制台、API、CLI 或第三方平台三种主要路径接入：

- **控制台快速验证**：通过 [Playground](raw/application-user-guide/knowledge-base/playground.md) 实时调试单库或多库的检索与问答效果，适合效果调优与质量验收。
- **API 集成**：
  - 底层单库检索：`POST /api/v1/indices/rag/index/retrieve`，需传 `index_id` 和 `query`；
  - 应用级联合检索：`POST /api/v1/indices/knowledge/search`，需传 `agent_id`（对应已发布的检索服务），策略由服务配置驱动；
  - 流式问答：`POST /api/v2/apps/knowledge/chat`，返回 SSE 事件，详见[服务渠道](raw/application-user-guide/knowledge-base/integration/channels.md)。
- **CLI 与第三方**：`bl knowledge search` 和 `bl knowledge chat` 命令分别调用检索与问答服务；Dify、Coze、n8n、LangChain 等平台可通过 REST API 或 MCP 协议接入，具体示例见[第三方平台接入](raw/application-user-guide/knowledge-base/integration/third-party.md)。

## 限制和注意事项

- **地域与规格限制**：知识库功能仅在中国站（华北2 北京）和国际站（新加坡）可用；标准版知识库限 1 QPS，旗舰版按 RCU（1 RCU ≈ 50 QPS）弹性伸缩，详见[容量与限制](raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-specifications.md)。
- **文件与切片约束**：单文件最大 150 MB（PDF/DOCX）或 512 MB（音视频）；单知识库最多 100,000 文档；切片内容上限 6000 字，标题上限 50 字；所有切片配置在导入时锁定，不可事后修改。
- **计费与生命周期**：自 2026 年 1 月 4 日起正式计费，费用含规格费（按小时）与模型调用费；免费额度（720 小时）仅抵扣标准版规格费，且老用户额度有效期截至 2026 年 2 月 3 日；删除知识库将**永久清除数据且不可恢复**，详见[知识库计费说明](raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)。
- **数据同步时效性**：OSS、飞书、钉钉等外部数据源通过[知识库定时数据同步指南](raw/application-user-guide/knowledge-base/data-connection-overview/data-sync-guide.md)自动拉取，最小同步周期为 1 分钟，但同步后仍需等待解析与索引构建完成方可检索。

## 来源文档

- [快速开始](../../raw/application-user-guide/knowledge-base/quickstart.md)
- [Playground](../../raw/application-user-guide/knowledge-base/playground.md)
- [核心概念](../../raw/application-user-guide/knowledge-base/concepts.md)
- [创建知识库](../../raw/application-user-guide/knowledge-base/data-connection-overview/rag-knowledge-base.md)
- [数据集](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-connection.md)
- [数据接入](../../raw/application-user-guide/knowledge-base/data-connection-overview.md)
- [文档管理与解析](../../raw/application-user-guide/knowledge-base/data-connection-overview/documents.md)
- [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-sync-guide.md)
- [切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)
- [知识服务](../../raw/application-user-guide/knowledge-base/service.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-retrieval.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)
- [最佳实践](../../raw/application-user-guide/knowledge-base/best-practices.md)
- [多轮对话：正确传递工具调用历史](../../raw/application-user-guide/knowledge-base/best-practices/multi-turn-chat.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/best-practices/rag-optimization.md)
- [文件自动打标：用大模型生成文档标签](../../raw/application-user-guide/knowledge-base/best-practices/auto-tag.md)
- [应用集成](../../raw/application-user-guide/knowledge-base/integration.md)
- [接入 AgentScope](../../raw/application-user-guide/knowledge-base/best-practices/knowledge-as-memory.md)
- [快速配置到 Agent](../../raw/application-user-guide/knowledge-base/integration/agent-cli.md)
- [服务渠道](../../raw/application-user-guide/knowledge-base/integration/channels.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/integration/rag-knowledge-base-api-guide.md)
- [第三方平台接入](../../raw/application-user-guide/knowledge-base/integration/third-party.md)
- [使用 CLI](../../raw/application-user-guide/knowledge-base/integration/cli.md)
- [参考](../../raw/application-user-guide/knowledge-base/reference.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-log-monitoring.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)
- [容量与限制](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-specifications.md)
- [更新日志](../../raw/application-user-guide/knowledge-base/changelog.md)


