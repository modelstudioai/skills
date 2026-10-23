# knowledge base

知识库（Knowledge Base）是百炼 RAG 平台的核心数据实体，将原始文档、切片、嵌入向量与索引配置统一组织，对外提供检索与问答能力。它支持多类型数据源（文档、表格、图片、音视频）和多种接入方式（控制台、API、CLI、MCP、第三方平台），是构建企业私有知识服务的基础单元。所有知识库均运行在业务空间（Workspace）隔离环境中，需配合检索服务或问答服务对外暴露能力。

## 支持的模型/功能

知识库本身不直接调用大模型，但其检索与问答能力深度依赖以下模型与功能组件：

- **嵌入模型（Embedding）**：创建知识库时指定，默认为 `text-embedding-v4`，用于将切片文本转为语义向量。该模型中英文兼容，创建后不可更改 [创建知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。
- **重排模型（Rerank）**：在检索服务或问答服务中配置，用于对初步召回结果进行精排。支持 `qwen3-rerank`（纯文本）、`qwen3-vl-rerank`（多模态）等，可按场景选择“问答模式”或“相似模式” [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)。
- **生成模型（LLM）**：在问答服务中指定，如 `qwen3.6-plus`，负责基于检索结果生成自然语言回答，并支持 `temperature`、`enable_thinking` 等参数调优 [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)。
- **多模态能力**：图片问答、音视频搜索等知识库类型依赖 Qwen-VL 等视觉语言模型进行解析与理解，相关能力在创建时即绑定 [创建知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

> **注意**：文档 2 中明确指出“知识库相关功能在中国站仅支持华北2（北京）地域，在国际站仅支持新加坡地域”，而文档 22 的 REST API 示例中 Endpoint 域名固定为 `cn-beijing.maas.aliyuncs.com`，二者一致；但文档 19（AgentScope 接入）示例代码中使用了 `{workspaceId}.cn-beijing.maas.aliyuncs.com`，未体现国际站适配逻辑，开发者需自行根据地域切换域名前缀。

## 关键参数

知识库的关键行为由以下参数控制，分为创建期与运行期两类：

- **创建期参数（不可变）**：
  - `知识库类型`：`文档搜索`/`数据查询`/`图片问答`/`音视频搜索`，决定底层数据处理链路；
  - `使用场景`（仅文档搜索类）：`基础文档问答`/`图文并茂回复`/`视觉理解`/`极速问答`，影响默认检索与生成策略；
  - `向量模型`：如 `text-embedding-v4`，创建后锁定；
  - `切片方式` 与 `最大分段长度`（10–6000 token）：在导入数据时配置，创建后不可更改 [切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)。

- **运行期参数（可动态调整）**：
  - `Query 改写`：开关控制，提升多轮对话中查询的完整性；
  - `TopK`：`初步向量检索 TopK`（1–100）与 `初步关键词检索 TopK`（1–100），控制召回广度；
  - `相似度阈值`（0.01–1.0）：过滤低分切片，值越高越严格；
  - `标签过滤`：通过字符串数组（如 `["产品_阿里云百炼", "难度_入门"]`）实现精准范围控制 [文件自动打标](../../raw/application-user-guide/knowledge-base/best-practices/auto-tag.md)；
  - `混排模型` 与 `混排模型模式`：全局生效，决定多知识库结果的融合排序逻辑。

## 使用方式

知识库需通过服务层（检索服务/问答服务）或直连接口对外提供能力，不支持裸知识库直接调用：

- **控制台快速验证**：在 Playground 中选择知识库，切换“知识检索”或“知识问答”模式，实时调试 [Playground](../../raw/application-user-guide/knowledge-base/playground.md)。
- **API 集成**：
  - 单知识库底层检索：调用 `/api/v1/indices/rag/index/retrieve`，需传 `index_id` 和 `query`，返回原始召回结果（无重排）；
  - 应用级联合检索：调用 `/api/v1/indices/knowledge/search`，传 `agent_id`（对应检索服务 ID），策略由服务配置驱动；
  - RAG 问答：调用 `/api/v2/apps/knowledge/chat`，流式 SSE 响应，需传 `agent_id`（对应问答服务 ID） [服务渠道](../../raw/application-user-guide/knowledge-base/integration/channels.md)。
- **CLI 调试**：使用 `bl knowledge search --agent-id <id>` 或 `bl knowledge chat --agent-id <id>` 快速验证，已弃用 `bl knowledge retrieve` [使用 CLI](../../raw/application-user-guide/knowledge-base/integration/cli.md)。
- **第三方平台**：Dify、Coze、n8n、LangChain 等均可通过 REST API 或 MCP 协议接入，核心是构造带 `Authorization: Bearer <API-Key>` 的 HTTP 请求 [第三方平台接入](../../raw/application-user-guide/knowledge-base/integration/third-party.md)。

## 限制和注意事项

- **地域与权限限制**：知识库功能仅在中国站（华北2 北京）和国际站（新加坡）可用；子账号需被授予 `AliyunBailianDataFullAccess` 策略并加入目标业务空间，否则无法操作 [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。
- **容量硬限制**：单业务空间最多 50 个知识库；单知识库最多 100,000 个文档；单次上传最多 50 个文件；切片最大长度 6000 token；问答服务最大召回数量为 20 [容量与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。
- **配置不可变性**：知识库类型、使用场景、切片方式、最大分段长度、向量模型等创建后不可修改，如需调整必须重建知识库 [容量与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。
- **计费与生命周期**：自 2026 年 1 月 4 日起正式计费，费用含规格费（标准版 0.03 元/小时，旗舰版按 RCU 计费）与模型调用费；删除知识库将**永久清除数据且不可恢复**，务必谨慎 [知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)。
- **同步与更新**：OSS 等外部数据源支持增量同步，但同步后的文件在百炼平台内为独立副本，源文件删除不影响副本；同步周期最短为一分钟，但钉钉同步会快速消耗 API 配额 [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-sync-guide.md)。

## 来源文档

- [创建知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [开始使用](../../raw/application-user-guide/knowledge-base/rag-start-using.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [容量与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [核心概念](../../raw/application-user-guide/knowledge-base/rag-start-using/concepts.md)
- [快速开始](../../raw/application-user-guide/knowledge-base/rag-start-using/quickstart.md)
- [Playground](../../raw/application-user-guide/knowledge-base/playground.md)
- [数据接入](../../raw/application-user-guide/knowledge-base/data-connection-overview.md)
- [数据集](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-connection.md)
- [文档管理与解析](../../raw/application-user-guide/knowledge-base/data-connection-overview/documents.md)
- [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-sync-guide.md)
- [知识服务](../../raw/application-user-guide/knowledge-base/service.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)
- [最佳实践](../../raw/application-user-guide/knowledge-base/best-practices.md)
- [多轮对话：正确传递工具调用历史](../../raw/application-user-guide/knowledge-base/best-practices/multi-turn-chat.md)
- [文件自动打标：用大模型生成文档标签](../../raw/application-user-guide/knowledge-base/best-practices/auto-tag.md)
- [接入 AgentScope](../../raw/application-user-guide/knowledge-base/best-practices/knowledge-as-memory.md)
- [应用集成](../../raw/application-user-guide/knowledge-base/integration.md)
- [快速配置到 Agent](../../raw/application-user-guide/knowledge-base/integration/agent-cli.md)
- [服务渠道](../../raw/application-user-guide/knowledge-base/integration/channels.md)
- [使用 CLI](../../raw/application-user-guide/knowledge-base/integration/cli.md)
- [第三方平台接入](../../raw/application-user-guide/knowledge-base/integration/third-party.md)
- [参考](../../raw/application-user-guide/knowledge-base/reference.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-log-monitoring.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)
- [更新日志](../../raw/application-user-guide/knowledge-base/changelog.md)
- [切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)


