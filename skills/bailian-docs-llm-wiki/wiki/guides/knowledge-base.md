# knowledge base

知识库（Knowledge Base）是百炼平台 RAG 能力的核心载体，用于组织文档、切片、嵌入向量与索引配置，对外提供可控、可扩展的检索与问答能力。它支持多模态数据接入与场景化检索策略，是构建企业私有知识服务的基础单元。

## 支持的模型/功能

知识库本身不直接运行大模型，但其检索与问答能力深度依赖以下模型与功能组件：

- **嵌入模型**：创建知识库时指定，默认为 `text-embedding-v4`，用于将切片文本转为语义向量；该配置创建后不可更改，详见[切片与向量化](raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)。
- **重排（Rerank）模型**：在检索服务中配置，如 `qwen3-rerank`（纯文本）、`qwen3-vl-rerank`（多模态），用于对初步召回结果进行精排；全局或单知识库独立启用。
- **生成模型**：在问答服务中选择（如 `qwen3.6-plus`），负责基于检索结果生成自然语言回答。
- **多模态能力**：图片问答类型知识库默认启用 Qwen-VL 解析与多模态 Embedding；音视频搜索类型自动集成语音转写与时间戳定位。

知识库类型决定底层处理链路：
- **文档搜索**：支持向量 + 关键词混合检索，适用 PDF/DOCX/MD 等格式；
- **数据查询**：基于 NL2SQL 的表格数据检索，对接 CSV/Excel/RDS；
- **图片问答**：以视觉 Embedding 为主，支持图文混排理解；
- **音视频搜索**：依赖语音转写与片段定位，非纯文本语义匹配。

> **注意**：文档 1 和文档 27 对知识库类型的命名存在细微差异——文档 1 使用“数据查询”，文档 27 使用“数据知识库”；实际功能一致，以控制台和 API 文档中的“数据查询”为准。

## 关键参数

所有关键参数均在知识库创建或服务配置阶段设定，部分参数创建后不可修改：

| 参数 | 取值范围 | 默认值 | 说明 | 是否可变 |
|------|----------|--------|------|----------|
| **最大分段长度** | 10–6000 token | 600 | 切片内容长度上限，影响召回粒度与上下文完整性 | ❌ 创建后不可改（见[切片与向量化](raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)） |
| **切片方式** | 智能切分 / 按长度 / 按页 / 按标题 / 按正则 / 按符号 | 智能切分 | 决定检索单元边界，直接影响召回质量 | ❌ 创建后不可改（见[文档管理与解析](raw/application-user-guide/knowledge-base/data-connection-overview/documents.md)） |
| **向量模型** | `text-embedding-v4` 等 | `text-embedding-v4` | 用于文本语义向量化，创建知识库时选定 | ❌ 不可更改 |
| **Metadata 抽取** | 开/关 | 关 | 启用后可配置最多 5 个字段（如 `product_name`, `author`），用于结构化过滤 | ❌ 创建后无法补配，需新建知识库（见[创建知识库](raw/application-user-guide/knowledge-base/rag-knowledge-base.md)） |
| **标签过滤** | 字符串数组 | — | 检索时按 `tags` 字段筛选文档范围，支持多值 OR 逻辑 | ✅ 运行时动态传参（API 或控制台配置） |

此外，检索服务与问答服务中可配置独立参数：
- `top_k`（1–100）：向量/关键词初步召回数量；
- `similarity_threshold`（0.01–1.0）：过滤低分切片；
- `max_retrieved_nodes`（1–20）：最终返回切片数；
- `query_rewrite`：开启后自动优化用户输入（适用于多轮对话模糊查询）。

## 使用方式

知识库可通过控制台、API、CLI 或第三方平台三种主要方式使用：

- **控制台快速验证**：  
  使用 [Playground](raw/application-user-guide/knowledge-base/playground.md) 选择知识库并输入问题，实时查看检索切片与模型回答；或在知识库详情页直接使用“知识检索”/“知识问答”调试入口。

- **API 集成**：  
  - 底层检索：调用 `/api/v1/indices/rag/index/retrieve`（单库直查，无重排）；  
  - 应用级联合检索：调用 `/api/v1/indices/knowledge/search`（需 `agent_id`，由检索服务驱动）；  
  - 流式问答：调用 `/api/v2/apps/knowledge/chat`（SSE 响应，含 `tool_calls` 历史）。  
  所有接口均需 `Authorization: Bearer <API-Key>` 鉴权，且仅支持中国站华北2（北京）及国际站新加坡地域（见[知识库API指南](raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)）。

- **CLI 与第三方接入**：  
  使用 `bailian-cli` 命令（如 `bl knowledge search --agent-id <id>`）快速调试；支持通过 MCP 协议接入 Qoder/Claude Code 等 Agent，或通过 REST API 接入 Dify、Coze、LangChain 等平台（见[第三方平台接入](raw/application-user-guide/knowledge-base/integration/third-party.md)）。

## 限制和注意事项

- **容量限制**：单知识库最多支持 100,000 个文档；单文件上限为 150 MB（PDF/DOCX）或 512 MB（音视频）；切片内容长度上限 6000 字符（见[容量与限制](raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)）。
- **地域与权限约束**：知识库功能仅在中国站（华北2）和国际站（新加坡）可用；子账号需被授予 `AliyunBailianDataFullAccess` 权限并加入对应业务空间（见[知识库API指南](raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)）。
- **不可逆操作**：  
  - 删除文档或切片后不可恢复；  
  - Metadata 抽取配置仅能在创建知识库时设置，创建后无法追加（必须重建知识库）；  
  - 切片方式与最大分段长度在导入数据时锁定，后续无法调整。
- **同步与更新行为**：通过数据集同步的文件（OSS/飞书/钉钉等）以独立副本形式存储，源文件删除不影响百炼副本；但源文件更新需等待下一次同步周期（最短 1 分钟）才生效（见[知识库定时数据同步指南](raw/application-user-guide/knowledge-base/data-connection-overview/data-sync-guide.md)）。
- **多轮对话注意事项**：RAG 服务无状态，若未显式传递 `tool_calls` 与 `tool` 返回结果，模型无法复用历史检索结果，将导致重复检索与答案不一致（见[多轮对话：正确传递工具调用历史](raw/application-user-guide/knowledge-base/best-practices/multi-turn-chat.md)）。

## 来源文档

- [创建知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [容量与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [参考](../../raw/application-user-guide/knowledge-base/reference.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-log-monitoring.md)
- [应用集成](../../raw/application-user-guide/knowledge-base/integration.md)
- [快速配置到 Agent](../../raw/application-user-guide/knowledge-base/integration/agent-cli.md)
- [服务渠道](../../raw/application-user-guide/knowledge-base/integration/channels.md)
- [第三方平台接入](../../raw/application-user-guide/knowledge-base/integration/third-party.md)
- [使用 CLI](../../raw/application-user-guide/knowledge-base/integration/cli.md)
- [最佳实践](../../raw/application-user-guide/knowledge-base/best-practices.md)
- [多轮对话：正确传递工具调用历史](../../raw/application-user-guide/knowledge-base/best-practices/multi-turn-chat.md)
- [文件自动打标：用大模型生成文档标签](../../raw/application-user-guide/knowledge-base/best-practices/auto-tag.md)
- [接入 AgentScope](../../raw/application-user-guide/knowledge-base/best-practices/knowledge-as-memory.md)
- [知识服务](../../raw/application-user-guide/knowledge-base/service.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)
- [数据接入](../../raw/application-user-guide/knowledge-base/data-connection-overview.md)
- [数据集](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-connection.md)
- [切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)
- [文档管理与解析](../../raw/application-user-guide/knowledge-base/data-connection-overview/documents.md)
- [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-sync-guide.md)
- [Playground](../../raw/application-user-guide/knowledge-base/playground.md)
- [开始使用](../../raw/application-user-guide/knowledge-base/rag-start-using.md)
- [快速开始](../../raw/application-user-guide/knowledge-base/rag-start-using/quickstart.md)
- [核心概念](../../raw/application-user-guide/knowledge-base/rag-start-using/concepts.md)


