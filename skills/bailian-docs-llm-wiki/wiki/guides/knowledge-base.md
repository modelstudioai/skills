# knowledge base

知识库（Knowledge Base）是阿里云百炼平台 RAG（[检索增强生成](../concepts/rag.md)）能力的核心载体，用于结构化存储、向量化索引和高效检索企业私有文档、表格、图片及音视频等多模态数据。它通过解析、切片、嵌入与索引构建完整检索链路，并支持与大模型协同生成带依据的自然语言回答。所有知识库均运行在业务空间（Workspace）内，实现资源隔离与权限管控。

## 支持的模型/功能

知识库本身不直接运行大模型，但深度集成多种模型能力以支撑检索与生成全流程：

- **嵌入模型（Embedding）**：默认使用 `text-embedding-v4`，支持中英文语义向量生成；创建知识库时选定，创建后不可更改 [创建知识库](../../raw/application-user-guide/knowledge-base/data-connection-overview/rag-knowledge-base.md)。
- **重排模型（Rerank）**：支持 `qwen3-rerank`（纯文本）、`qwen3-vl-rerank`（多模态）等，用于对初步召回结果进行精排，提升相关性 [知识检索](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-retrieval.md)。
- **生成模型（LLM）**：问答服务支持绑定 `qwen3.6-plus` 等 Qwen 系列模型，控制台 Playground 与 API 均可切换对比效果 [Playground](../../raw/application-user-guide/knowledge-base/playground.md)。
- **多模态模型**：图片问答、音视频搜索类型知识库依赖 `Qwen-VL` 或专用音视频解析模型，实现图文理解与语音转写+定位 [创建知识库](../../raw/application-user-guide/knowledge-base/data-connection-overview/rag-knowledge-base.md)。

> **注意**：文档 3 中提及“新版 Connector 已上线，旧版数据连接需在 2026 年 9 月 30 日前完成迁移”，而文档 7 的导航页仍列出旧版 `data-connection.md`。实际开发应以新版 Connector 为准，旧版数据集功能已进入迁移过渡期。

## 关键参数

知识库行为由多个层级参数共同决定，主要分为三类：

| 参数类别 | 典型参数 | 取值范围 | 说明 |
|----------|----------|----------|------|
| **索引构建期** | 最大分段长度 | 10–6000 token | 决定切片粒度，默认 600；过短丢失上下文，过长混杂主题 [切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md) |
| | 切片方式 | 智能切分 / 按长度 / 按页 / 按标题等 | 影响切片边界合理性，智能切分适用于大多数场景 [文档管理与解析](../../raw/application-user-guide/knowledge-base/data-connection-overview/documents.md) |
| | 向量模型 | `text-embedding-v4` 等 | 创建时选定，不可修改，直接影响语义匹配精度 |
| **检索服务期** | 初步向量检索 TopK | 1–100 | 向量阶段召回数量，影响召回广度与延迟 [知识检索](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-retrieval.md) |
| | 相似度阈值 | 0.01–1.0 | 过滤低分切片，值越高越精确但可能漏召 |
| | 最大召回数量 | 1–20 | 最终返回切片总数，问答服务上限为 20 [容量与限制](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-specifications.md) |
| **生成服务期** | `temperature` | 0.0–1.0 | 控制回答随机性，调试时建议从 0.3 开始调整 [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md) |
| | `enable_thinking` | true / false | 启用模型内部推理链，提升复杂问题处理能力 |

## 使用方式

### 1. 控制台快速验证
- **Playground**：选择知识库，切换“知识问答”或“知识检索”模式，实时调试并查看引用高亮与命中文档卡片 [Playground](../../raw/application-user-guide/knowledge-base/playground.md)。
- **知识库详情页**：上传文件 → 配置切片与索引 → 查看切片详情 → 手动启用/禁用切片，适合精细化管理 [文档管理与解析](../../raw/application-user-guide/knowledge-base/data-connection-overview/documents.md)。

### 2. API 集成
- **底层检索**（单库）：调用 `/api/v1/indices/rag/index/retrieve`，传入 `index_id` 和 `query`，返回原始召回结果（无重排）。
- **应用级检索**（多库联合）：调用 `/api/v1/indices/knowledge/search`，传入 `agent_id`（对应知识检索服务），策略由服务配置驱动，推荐生产环境使用 [服务渠道](../../raw/application-user-guide/knowledge-base/integration/channels.md)。
- **流式问答**：调用 `/api/v2/apps/knowledge/chat`，支持 SSE 流式响应，需传入 `agent_id` 与消息历史 [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)。

### 3. CLI 与第三方工具
- **CLI**：`bl knowledge search --agent-id <id> --query "xxx"` 或 `bl knowledge chat --agent-id <id> --message "xxx"`，适合脚本与本地调试 [使用 CLI](../../raw/application-user-guide/knowledge-base/integration/cli.md)。
- **第三方平台**：Dify、Coze、n8n、LangChain 等均可通过 DashScope REST API 接入，LangChain 示例代码见 [第三方平台接入](../../raw/application-user-guide/knowledge-base/integration/third-party.md)。

## 限制和注意事项

- **地域与规格限制**：知识库功能仅在中国站（华北2 北京）和国际站（新加坡）可用；标准版知识库最高并发为 1 QPS，旗舰版按 RCU 计费，1 RCU ≈ 50 QPS [知识库API指南](../../raw/application-user-guide/knowledge-base/integration/rag-knowledge-base-api-guide.md)。
- **文件与切片约束**：单文件最大 150 MB（文档）或 512 MB（音视频）；单次上传最多 50 个文件；切片内容长度上限 6000 字，标题上限 50 字；切片策略创建后不可修改 [容量与限制](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-specifications.md)。
- **计费与生命周期**：自 2026 年 1 月 4 日起正式计费，提供 720 小时免费额度（仅抵扣标准版规格费）；删除知识库将**永久清除数据且不可恢复**，务必谨慎操作 [知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)。
- **安全与审计**：所有检索调用自动投递至日志服务（SLS），字段含 `request_id`、`pipeline_id`（知识库 ID）、`response_body.data.nodes[]`（召回切片）等，可用于用量统计、错误排查与召回审计 [知识库日志与监控](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-log-monitoring.md)。

## 来源文档

- [快速开始](../../raw/application-user-guide/knowledge-base/quickstart.md)
- [核心概念](../../raw/application-user-guide/knowledge-base/concepts.md)
- [数据集](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-connection.md)
- [创建知识库](../../raw/application-user-guide/knowledge-base/data-connection-overview/rag-knowledge-base.md)
- [文档管理与解析](../../raw/application-user-guide/knowledge-base/data-connection-overview/documents.md)
- [Playground](../../raw/application-user-guide/knowledge-base/playground.md)
- [数据接入](../../raw/application-user-guide/knowledge-base/data-connection-overview.md)
- [切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-retrieval.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)
- [最佳实践](../../raw/application-user-guide/knowledge-base/best-practices.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/best-practices/rag-optimization.md)
- [多轮对话：正确传递工具调用历史](../../raw/application-user-guide/knowledge-base/best-practices/multi-turn-chat.md)
- [文件自动打标：用大模型生成文档标签](../../raw/application-user-guide/knowledge-base/best-practices/auto-tag.md)
- [接入 AgentScope](../../raw/application-user-guide/knowledge-base/best-practices/knowledge-as-memory.md)
- [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-sync-guide.md)
- [应用集成](../../raw/application-user-guide/knowledge-base/integration.md)
- [快速配置到 Agent](../../raw/application-user-guide/knowledge-base/integration/agent-cli.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/integration/rag-knowledge-base-api-guide.md)
- [服务渠道](../../raw/application-user-guide/knowledge-base/integration/channels.md)
- [知识服务](../../raw/application-user-guide/knowledge-base/service.md)
- [使用 CLI](../../raw/application-user-guide/knowledge-base/integration/cli.md)
- [参考](../../raw/application-user-guide/knowledge-base/reference.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-log-monitoring.md)
- [容量与限制](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-specifications.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)
- [第三方平台接入](../../raw/application-user-guide/knowledge-base/integration/third-party.md)
- [更新日志](../../raw/application-user-guide/knowledge-base/changelog.md)


