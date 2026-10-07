# knowledge base

知识库（Knowledge Base）是阿里云百炼平台 RAG（[检索增强生成](../concepts/rag.md)）能力的核心载体，用于结构化存储、向量化索引和语义化检索企业私有文档、表格、图片及音视频等多模态数据。它通过解析、切片、嵌入与索引构建统一检索底座，并支持通过检索服务（纯召回）或问答服务（召回+大模型生成）两种方式对外提供能力。所有知识库均运行在业务空间内，实现资源隔离与权限管控。

## 支持的模型/功能

知识库本身不直接绑定大模型，但其检索与问答能力深度依赖以下模型组件：

- **嵌入模型（Embedding）**：默认使用 `text-embedding-v4`，支持中英文混合语义向量化；创建知识库时选定后不可更改，详见[切片与向量化](raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)。
- **重排模型（Rerank）**：支持 `qwen3-rerank`（纯文本）、`qwen3-vl-rerank`（多模态）等，用于对初步召回结果进行精排；可在[知识检索](raw/application-user-guide/knowledge-base/service/rag-knowledge-retrieval.md)或[知识问答](raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)的服务配置中按知识库独立启用。
- **生成模型（LLM）**：问答服务中可自由切换 Qwen 系列模型（如 `qwen3.6-plus`），通过控制台或 API 配置 `temperature`、`enable_thinking` 等参数；Playground 中也支持实时对比不同模型的回答效果，参见[Playground](raw/application-user-guide/knowledge-base/playground.md)。

功能上，知识库支持四类核心类型：
- **文档搜索**：处理 PDF/Word/Markdown 等非结构化文档，采用向量+关键词混合检索；
- **数据查询**：对接 CSV/Excel/RDS 表格，执行 NL2SQL 查询；
- **图片问答**：基于多模态 Embedding 实现以图搜图与图文问答；
- **音视频搜索**：通过语音转写与时间戳定位实现内容片段检索。

> **注意**：文档 5 明确指出“面向智能体（Agent）场景的新版 [Connector](raw/application-user-guide/overview.md) 已上线”，并要求旧版数据连接器于 2026 年 9 月 30 日前完成迁移。这意味着当前知识库的数据接入能力正经历架构演进，新项目应优先评估新版 Connector 兼容性。

## 关键参数

关键参数分层配置，影响检索精度、性能与成本：

| 参数类别 | 参数名 | 取值范围 | 说明 |
|----------|--------|----------|------|
| **切片** | 最大分段长度 | 10–6000 token | 默认 600；决定单切片语义完整性，过短易丢失上下文，过长易混入噪声；创建后不可修改，详见[切片与向量化](raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)。 |
| **检索** | 初步向量 TopK / 关键词 TopK | 1–100 | 控制各路召回数量；增大可提升召回率但增加重排开销。 |
| | 相似度阈值 | 0.01–1.0 | 过滤低分切片；值越高结果越精确但可能漏召。 |
| | 最大召回数量 | 1–20 | 混排后最终返回的切片总数，直接影响生成阶段上下文长度。 |
| **规格** | 知识库规格 | 标准版 / 旗舰版 | 标准版固定 1 QPS、含 720 小时免费额度；旗舰版按 RCU（1 RCU ≈ 50 QPS）弹性伸缩，计费为 0.2 元/RCU/小时，详见[知识库计费说明](raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)。 |

## 使用方式

知识库可通过控制台、API、CLI 或第三方平台三种路径接入：

- **控制台快速验证**：  
  1. 在[知识管理](https://bailian.console.aliyun.com/cn-beijing/rag/knowledge/list)创建知识库（推荐从[快速开始](raw/application-user-guide/knowledge-base/quickstart.md)指引操作）；  
  2. 在[Playground](https://bailian.console.aliyun.com/cn-beijing/rag/playground)中选择知识库并切换“知识问答”模式，实时调试检索与生成效果；  
  3. 创建[知识检索](https://bailian.console.aliyun.com/cn-beijing/rag/retrieval/list)或[知识问答](https://bailian.console.aliyun.com/cn-beijing/rag/qa/list)服务，绑定知识库并发布。

- **程序化集成**：  
  - **REST API**：使用 `DASHSCOPE_API_KEY` 鉴权，调用 `/api/v1/indices/knowledge/search`（应用级联合检索）或 `/api/v2/apps/knowledge/chat`（流式问答）；  
  - **CLI 命令**：`bl knowledge search --agent-id <检索服务ID>` 或 `bl knowledge chat --agent-id <问答服务ID>`，适合脚本与本地调试；  
  - **第三方平台**：Dify/Coze/n8n/LangChain 等均可通过 DashScope API 接入，LangChain 示例见[第三方平台接入](raw/application-user-guide/knowledge-base/integration/third-party.md)。

- **Agent 场景**：  
  支持 MCP 协议（如 Qoder/Claude Code），或通过自定义中间件（如 AgentScope 的 `KnowledgeStudioRAGMiddleware`）注入静态检索或自主工具调用能力，详见[接入 AgentScope](raw/application-user-guide/knowledge-base/best-practices/knowledge-as-memory.md)。

## 限制和注意事项

- **地域与规格限制**：知识库功能仅在中国站（华北2 北京）和国际站（新加坡）可用；标准版知识库上限为 50 个/业务空间，旗舰版需工单申请扩容；单次上传文件数上限为 50 个，单文件最大 150 MB（PDF/DOCX）或 512 MB（音视频），详见[容量与限制](raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-specifications.md)。

- **配置不可变性**：切片方式（智能切分/按长度/按页等）与最大分段长度在导入数据时配置，**创建后不可更改**；若需调整，必须重建知识库并重新导入数据。

- **数据同步行为**：OSS/飞书/钉钉等外部数据源的定时同步规则，会将文件作为**独立副本**存储于百炼平台；源文件删除**不会**自动同步删除副本，需手动清理，详见[知识库定时数据同步指南](raw/application-user-guide/knowledge-base/data-connection-overview/data-sync-guide.md)。

- **计费与生命周期**：自 2026 年 1 月 4 日起正式计费；免费额度仅抵扣标准版规格费用，且老用户额度有效期截至 2026 年 2 月 3 日；未开通服务的知识库数据将于 2026 年 6 月 30 日被永久删除，务必及时开通，参见[知识库计费说明](raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)。

- **安全与合规**：API Key 必须通过环境变量（`DASHSCOPE_API_KEY`）或阿里云 CLI 安全配置，**严禁硬编码或明文输出**；知识库删除操作不可逆，删除后数据无法恢复。

## 来源文档

- [快速开始](../../raw/application-user-guide/knowledge-base/quickstart.md)
- [核心概念](../../raw/application-user-guide/knowledge-base/concepts.md)
- [Playground](../../raw/application-user-guide/knowledge-base/playground.md)
- [数据接入](../../raw/application-user-guide/knowledge-base/data-connection-overview.md)
- [数据集](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-connection.md)
- [创建知识库](../../raw/application-user-guide/knowledge-base/data-connection-overview/rag-knowledge-base.md)
- [文档管理与解析](../../raw/application-user-guide/knowledge-base/data-connection-overview/documents.md)
- [切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)
- [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-sync-guide.md)
- [知识服务](../../raw/application-user-guide/knowledge-base/service.md)
- [最佳实践](../../raw/application-user-guide/knowledge-base/best-practices.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-retrieval.md)
- [文件自动打标：用大模型生成文档标签](../../raw/application-user-guide/knowledge-base/best-practices/auto-tag.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/best-practices/rag-optimization.md)
- [多轮对话：正确传递工具调用历史](../../raw/application-user-guide/knowledge-base/best-practices/multi-turn-chat.md)
- [应用集成](../../raw/application-user-guide/knowledge-base/integration.md)
- [接入 AgentScope](../../raw/application-user-guide/knowledge-base/best-practices/knowledge-as-memory.md)
- [服务渠道](../../raw/application-user-guide/knowledge-base/integration/channels.md)
- [快速配置到 Agent](../../raw/application-user-guide/knowledge-base/integration/agent-cli.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/integration/rag-knowledge-base-api-guide.md)
- [第三方平台接入](../../raw/application-user-guide/knowledge-base/integration/third-party.md)
- [使用 CLI](../../raw/application-user-guide/knowledge-base/integration/cli.md)
- [参考](../../raw/application-user-guide/knowledge-base/reference.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)
- [容量与限制](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-specifications.md)
- [更新日志](../../raw/application-user-guide/knowledge-base/changelog.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-log-monitoring.md)


