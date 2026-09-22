# knowledge base

知识库（Knowledge Base）是百炼平台 RAG 能力的核心载体，用于结构化存储、向量化索引和语义化检索非结构化/半结构化数据。它支持文档、表格、图片、音视频等多种数据类型，并通过检索服务与问答服务对外提供可编程的 API 接口。知识库与业务空间强绑定，所有操作均需在已开通服务的账号下进行。

## 支持的模型与功能

- **嵌入模型**：默认使用 `text-embedding-v4`（中英文通用），创建知识库时选定且不可更改；[创建知识库](raw/application-user-guide/knowledge-base/rag-knowledge-base.md) 文档明确说明该配置项位于“索引设置”步骤。
- **重排（Rerank）模型**：支持 `qwen3-rerank`（纯文本）、`qwen3-vl-rerank`（多模态）等，可在知识检索或知识问答服务中为单个知识库独立启用；[知识检索](raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md) 文档指出其影响“排序后最终返回的切片总数量”。
- **生成模型**：问答服务支持 Qwen 系列（如 `qwen3.6-plus`）、DeepSeek 等，通过控制台或 API 指定；[知识问答](raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md) 文档详细列出模型选择与参数配置方式。
- **核心功能**：
  - 多源数据接入（OSS、飞书、钉钉、语雀、SharePoint、MySQL 等）；
  - 智能切片（按标题、长度、页、正则等）与元数据抽取；
  - 标签过滤、Query 改写、多知识库联合路由与混排；
  - Playground 交互式调试、CLI 命令行检索、Agent Skill 集成。

> **注意**：文档 25《知识库API指南》明确限定“知识库相关功能在中国站仅支持**华北2（北京）**地域，在国际站仅支持**新加坡**地域”，而其他多篇文档（如文档 22 快速开始、文档 27 知识检索）未提及地域限制，实际调用前必须确认地域合规性，否则 API 将返回 404 或权限错误。

## 关键参数

| 参数类别 | 参数名 | 取值范围 | 说明 | 配置位置 |
|----------|--------|----------|------|-----------|
| **切片** | 最大分段长度 | 10–6000 token | 影响检索单元粒度，过短丢失上下文，过长混杂主题 | [导入数据](raw/application-user-guide/knowledge-base/data-connection-overview/documents.md) 的索引设置 |
| **检索** | `top_k`（初步召回） | 向量/关键词：1–100 | 控制各阶段初步召回切片数，影响精度与延迟 | [知识检索](raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md) 独立配置 |
| **检索** | 最大召回数量 | 1–20 | 混排后最终返回的切片总数，问答服务中亦同此限制 | [知识问答](raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md) 独立配置 |
| **检索** | 相似度阈值 | 0.01–1.0 | 过滤低分切片，值越高结果越精确但可能漏召 | 同上 |
| **标签** | 单标签长度 | ≤32 字符 | 仅支持中文、英文字母、数字、`_`、`-`；多值需拆分为多个字符串 | [文件自动打标](raw/application-user-guide/knowledge-base/best-practices/auto-tag.md) 文档强调格式约束 |

## 使用方式

- **控制台快速验证**：通过 [Playground](raw/application-user-guide/knowledge-base/playground.md) 选择知识库并输入问题，实时查看检索切片与模型回答，适合效果调优。
- **API 集成**：
  - **底层检索**：`POST /api/v1/indices/rag/index/retrieve`，需传 `index_id`、`query`、`top_k`；适用于单库直查。
  - **应用级检索**：`POST /api/v1/indices/knowledge/search`，传 `agent_id`（检索服务 ID）与 `query`，由服务配置驱动多库路由与混排。
  - **流式问答**：`POST /api/v2/apps/knowledge/chat`，传 `agent_id` 与消息历史，支持携带工具调用历史实现多轮上下文复用；[多轮对话](raw/application-user-guide/knowledge-base/best-practices/multi-turn-chat.md) 文档详述了 SSE 流中提取历史的方法。
- **命令行工具**：使用 `bailian-cli`：
  - `bl knowledge search --agent-id <id> --query "xxx"`（推荐，走检索服务）
  - `bl knowledge chat --agent-id <id> --message "xxx"`（流式问答）
- **Agent 集成**：支持 CLI、MCP Server、Skill 包三种方式，[快速配置到 Agent](raw/application-user-guide/knowledge-base/integration/agent-cli.md) 文档提供 `npx skills add` 一键安装指令及凭证配置说明。

## 限制和注意事项

- **容量硬限**：单业务空间最多 50 个知识库、单知识库最多 100,000 文档、单次上传最多 50 个文件；超限时需申请工单扩容（见[容量与限制](raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)）。
- **免费额度规则**：所有用户享 720 小时标准版免费额度，但**仅抵扣规格费用，不包含模型调用费用**；老用户额度有效期至 2026 年 2 月 3 日，新用户为开通后 30 天内有效（见[知识库计费说明](raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)）。
- **关键不可变项**：切片方式与最大分段长度在知识库创建时确定，**创建后不可更改**；若需调整，必须重建知识库并重新导入数据（见[切片与向量化](raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)）。
- **日志与监控**：检索日志默认投递至 SLS，需手动开通监控配置并授权角色 `AliyunServiceRoleForSFMAccessSLS`；关闭开关仅停止新日志投递，历史日志仍计费（见[知识库日志与监控](raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-log-monitoring.md)）。
- **安全与删除**：知识库、文档、切片删除均为**永久清除且不可恢复**；删除知识库将立即停止计费，但需注意关联的 SLS LogStore 需手动删除以终止日志计费。

## 来源文档

- [更新日志](../../raw/application-user-guide/knowledge-base/changelog.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-log-monitoring.md)
- [参考](../../raw/application-user-guide/knowledge-base/reference.md)
- [快速配置到 Agent](../../raw/application-user-guide/knowledge-base/integration/agent-cli.md)
- [应用集成](../../raw/application-user-guide/knowledge-base/integration.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)
- [第三方平台接入](../../raw/application-user-guide/knowledge-base/integration/third-party.md)
- [使用 CLI](../../raw/application-user-guide/knowledge-base/integration/cli.md)
- [服务渠道](../../raw/application-user-guide/knowledge-base/integration/channels.md)
- [多轮对话：正确传递工具调用历史](../../raw/application-user-guide/knowledge-base/best-practices/multi-turn-chat.md)
- [文件自动打标：用大模型生成文档标签](../../raw/application-user-guide/knowledge-base/best-practices/auto-tag.md)
- [知识服务](../../raw/application-user-guide/knowledge-base/service.md)
- [最佳实践](../../raw/application-user-guide/knowledge-base/best-practices.md)
- [接入 AgentScope](../../raw/application-user-guide/knowledge-base/best-practices/knowledge-as-memory.md)
- [数据集](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-connection.md)
- [数据接入](../../raw/application-user-guide/knowledge-base/data-connection-overview.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)
- [文档管理与解析](../../raw/application-user-guide/knowledge-base/data-connection-overview/documents.md)
- [切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)
- [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-sync-guide.md)
- [Playground](../../raw/application-user-guide/knowledge-base/playground.md)
- [快速开始](../../raw/application-user-guide/knowledge-base/quickstart.md)
- [核心概念](../../raw/application-user-guide/knowledge-base/concepts.md)
- [创建知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [容量与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)


