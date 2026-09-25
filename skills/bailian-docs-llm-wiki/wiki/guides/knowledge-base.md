# knowledge base

知识库（Knowledge Base）是阿里云百炼平台 RAG（[检索增强生成](../concepts/rag.md)）能力的核心载体，用于结构化存储、向量化索引和高效检索企业私有文档、表格、图片及音视频等多模态数据。它通过解析、切片、嵌入与索引构建完整处理链路，并支持通过控制台 Playground 快速验证、API/CLI 集成或多种服务渠道（如 MCP、Agent Skill）接入应用。所有知识库均运行于业务空间内，资源隔离且可精细化配置。

## 支持的模型/功能

- **模型支持**：  
  - 检索阶段：默认使用 `text-embedding-v4` 向量模型（中英文语义兼容），创建后不可更改；重排（Rerank）阶段支持 `qwen3-rerank`（纯文本）、`qwen3-vl-rerank`（多模态）等模型；生成阶段支持 Qwen 系列大模型（如 `qwen3.6-plus`），可在 Playground 或问答服务中切换对比效果 [快速开始](../../raw/application-user-guide/knowledge-base/quickstart.md)。  
  - 多模态能力：图片问答类型知识库依赖 `Qwen-VL` 解析与 `qwen3-vl-rerank` 重排，音视频搜索依赖语音转写与时间戳定位模块。

- **核心功能**：  
  - **多类型知识库**：支持文档搜索（PDF/Word/Markdown）、数据查询（CSV/Excel/MySQL）、图片问答、音视频搜索四类，不同类型对应不同解析与检索方式 [核心概念](../../raw/application-user-guide/knowledge-base/concepts.md)。  
  - **混合检索模式**：向量检索（语义匹配） + 关键词检索（精确匹配），并支持 Query 改写、知识库路由、混排模型精排 [知识检索](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-retrieval.md)。  
  - **生成增强服务**：知识问答服务在检索基础上叠加大模型生成，支持流式响应、引用标注、拒答、防泄漏、多模态回复等控制参数 [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)。  
  - **自动化能力**：支持定时同步（OSS/飞书/钉钉/语雀/SharePoint）、文件自动打标（基于大模型抽取标签）、多轮对话历史传递（避免重复检索）等高级实践 [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-sync-guide.md)。

> **注意**：文档 6 中提及“旧版数据连接需在 2026 年 9 月 30 日前完成迁移”，而文档 28（更新日志）最新日期为 2026-07-27，表明迁移窗口尚未关闭但已临近；开发者应尽快评估并执行 [数据连接迁移](../../raw/application-user-guide/overview/reference-overview/migration.md)。

## 关键参数

| 参数类别 | 参数名 | 取值范围 | 说明 | 配置位置 |
|----------|--------|----------|------|----------|
| **切片** | 最大分段长度 | 10–6000 token | 默认 600，决定单切片最大语义单元大小 | [导入数据](../../raw/application-user-guide/knowledge-base/data-connection-overview/documents.md) 或 [创建知识库](../../raw/application-user-guide/knowledge-base/data-connection-overview/rag-knowledge-base.md) 的索引设置步骤 |
| **检索** | 初步向量 TopK | 1–100 | 向量检索阶段初步召回数量，默认 100 | [知识检索](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-retrieval.md) 或 [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md) 的知识库独立配置 |
| | 相似度阈值 | 0.01–1.0 | 过滤低分切片，值越高结果越精确但可能漏召 | 同上 |
| | 最大召回数量 | 1–20 | 混排或排序后最终返回的切片总数 | 同上 |
| **服务** | 单服务绑定知识库数 | ≤15 | 多库联合检索/问答的上限 | [知识检索](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-retrieval.md) 创建流程 |
| **标签** | 单标签长度 | ≤32 字符 | 标签仅支持中文、英文字母、数字、下划线 `_`、中划线 `-` | [文档管理](../../raw/application-user-guide/knowledge-base/data-connection-overview/documents.md) |

> **注意**：切片方式（智能切分/按长度/按页等）和最大分段长度在知识库创建时配置，**创建后不可更改**；若需调整，必须重建知识库 [切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)。

## 使用方式

- **控制台交互**：  
  - **Playground**：选择知识库后切换“知识问答”或“知识检索”模式，实时调试并查看引用高亮与切片来源 [Playground](../../raw/application-user-guide/knowledge-base/playground.md)。  
  - **服务创建**：在“知识服务”下分别创建**知识检索服务**（配置多库权重、混排模型）和**知识问答服务**（配置模型、提示词、生成控制），发布后获取 `agent_id` 供 API 调用 [知识检索](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-retrieval.md)、[知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)。

- **API/CLI 集成**：  
  - **底层检索**：调用 `/api/v1/indices/rag/index/retrieve`，需传 `index_id` 和 `top_k`，返回原始召回切片（无重排） [快速开始](../../raw/application-user-guide/knowledge-base/quickstart.md)。  
  - **应用级检索**：调用 `/api/v1/indices/knowledge/search`，传 `agent_id` 和 `query`，策略由检索服务配置驱动，推荐生产使用 [服务渠道](../../raw/application-user-guide/knowledge-base/integration/channels.md)。  
  - **流式问答**：调用 `/api/v2/apps/knowledge/chat`，支持 SSE 流式响应，需传 `agent_id` 和消息体 [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)。  
  - **CLI 命令**：`bl knowledge search --agent-id <id> --query "xxx"`（推荐）或 `bl knowledge chat --agent-id <id> --message "xxx"` [使用 CLI](../../raw/application-user-guide/knowledge-base/integration/cli.md)。

- **第三方接入**：  
  - 通过 REST API 接入 Dify、Coze、n8n、LangChain 等平台；  
  - 通过 MCP Server 协议接入 Qoder、Claude Code 等 AI 编码助手；  
  - 通过 Agent Skill 包快速集成至 Claude Code / Cursor / Qoder 等客户端 [第三方平台接入](../../raw/application-user-guide/knowledge-base/integration/third-party.md)、[快速配置到 Agent](../../raw/application-user-guide/knowledge-base/integration/agent-cli.md)。

## 限制和注意事项

- **地域与规格限制**：知识库功能在中国站仅支持**华北2（北京）**，国际站仅支持**新加坡**；标准版知识库固定 1 QPS 并限 100 GB 存储，旗舰版按 RCU（1 RCU ≈ 50 QPS）弹性伸缩，最高 10,000 QPS [容量与限制](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-specifications.md)、[知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)。  
- **文件与切片约束**：单文件最大 150 MB（PDF/DOCX）或 512 MB（音视频）；单知识库最多 100,000 文档；手动新增切片内容限 6000 字，标题限 50 字；切片策略创建后不可修改 [容量与限制](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-specifications.md)。  
- **安全与运维**：  
  - 删除知识库或文档**不可恢复**，且立即停止计费；  
  - 检索日志默认投递至 SLS，需手动开通监控并承担 SLS 存储与流量费用 [知识库日志与监控](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-log-monitoring.md)；  
  - API 调用受 QPS 限制（检索接口上限 2,000 QPS），超限返回 `429`，可工单申请提升 [容量与限制](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-specifications.md)。  
- **计费提醒**：自 2026 年 1 月 4 日起正式计费，提供一次性 720 小时免费额度（仅抵扣标准版规格费），老用户额度有效期至 2026 年 2 月 3 日；资源包购买后一年内有效 [知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)。

## 来源文档

- [快速开始](../../raw/application-user-guide/knowledge-base/quickstart.md)
- [核心概念](../../raw/application-user-guide/knowledge-base/concepts.md)
- [Playground](../../raw/application-user-guide/knowledge-base/playground.md)
- [数据接入](../../raw/application-user-guide/knowledge-base/data-connection-overview.md)
- [文档管理与解析](../../raw/application-user-guide/knowledge-base/data-connection-overview/documents.md)
- [数据集](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-connection.md)
- [创建知识库](../../raw/application-user-guide/knowledge-base/data-connection-overview/rag-knowledge-base.md)
- [知识服务](../../raw/application-user-guide/knowledge-base/service.md)
- [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-sync-guide.md)
- [切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-retrieval.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)
- [最佳实践](../../raw/application-user-guide/knowledge-base/best-practices.md)
- [多轮对话：正确传递工具调用历史](../../raw/application-user-guide/knowledge-base/best-practices/multi-turn-chat.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/best-practices/rag-optimization.md)
- [应用集成](../../raw/application-user-guide/knowledge-base/integration.md)
- [接入 AgentScope](../../raw/application-user-guide/knowledge-base/best-practices/knowledge-as-memory.md)
- [文件自动打标：用大模型生成文档标签](../../raw/application-user-guide/knowledge-base/best-practices/auto-tag.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/integration/rag-knowledge-base-api-guide.md)
- [快速配置到 Agent](../../raw/application-user-guide/knowledge-base/integration/agent-cli.md)
- [服务渠道](../../raw/application-user-guide/knowledge-base/integration/channels.md)
- [使用 CLI](../../raw/application-user-guide/knowledge-base/integration/cli.md)
- [第三方平台接入](../../raw/application-user-guide/knowledge-base/integration/third-party.md)
- [参考](../../raw/application-user-guide/knowledge-base/reference.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-log-monitoring.md)
- [容量与限制](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-specifications.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)
- [更新日志](../../raw/application-user-guide/knowledge-base/changelog.md)


