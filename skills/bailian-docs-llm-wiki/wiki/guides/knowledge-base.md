# knowledge base

阿里云百炼知识库（Knowledge Base）是 RAG（[检索增强生成](../concepts/rag.md)）能力的核心载体，用于结构化管理非结构化/半结构化数据（文档、表格、图片、音视频等），并提供向量化索引、语义检索与大模型问答服务。它支持通过控制台快速创建、Playground 交互调试、API/CLI/MCP 等多渠道集成，并可与 AgentScope、Dify、Coze 等第三方框架深度对接。

## 支持的模型与功能

知识库本身不直接运行大模型，但其检索与问答服务深度集成以下模型能力：

- **嵌入模型**：默认使用 `text-embedding-v4`（中英文通用），创建后不可更改；支持自定义选择，详见[切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)。
- **重排（Rerank）模型**：支持 `qwen3-rerank`（纯文本）、`qwen3-vl-rerank`（多模态）等，用于精排召回结果，配置于检索服务或问答服务的知识库独立参数中。
- **生成模型**：问答服务支持绑定 Qwen 系列模型（如 `qwen3.6-plus`），通过提示词、`temperature`、`enable_thinking` 等参数调控生成行为，详见[知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)。

核心功能包括：
- 多类型数据接入（文档搜索、数据查询、图片问答、音视频搜索）
- 智能解析（OCR、版面恢复、大模型结构理解）
- 可配置切片策略（智能切分、按页、按标题等）
- 向量 + 关键词混合检索、多轮智能检索（Agentic）、Query 改写
- 标签过滤、元数据抽取、拒答与防泄漏等生成控制
- 全链路日志投递至 SLS，支持审计与监控

> **注意**：文档 5 明确指出“面向智能体（Agent）场景的新版 [Connector](raw/application-user-guide/overview.md) 已上线”，而旧版“数据连接”（即当前知识库所用的数据集）需在 2026 年 9 月 30 日前完成迁移。这意味着当前知识库依赖的数据接入层存在明确的演进路径和生命周期约束，开发者应关注迁移计划。

## 关键参数

知识库及关联服务的关键参数分为三类，均在控制台配置界面或 API 请求体中显式指定：

| 参数类别 | 示例参数 | 取值范围 | 说明 |
|----------|----------|----------|------|
| **索引构建期** | `最大分段长度` | 10–6000 token | 决定切片粒度，默认 600；过短丢失上下文，过长混杂主题，详见[切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)。 |
| **检索服务期** | `初步向量检索 TopK`<br>`相似度阈值`<br>`最大召回数量` | 1–100<br>0.01–1.0<br>1–20 | 控制召回广度与精度：`TopK` 影响初筛规模，`相似度阈值` 过滤低质结果，`最大召回数量` 限定最终返回条数。 |
| **问答服务期** | `temperature`<br>`enable_thinking`<br>`文件预解析` | 0.0–1.0<br>布尔值<br>布尔值 | 调控生成稳定性、推理能力与多模态输入支持，直接影响回答质量与安全性。 |

所有参数均支持通过 API 动态配置，例如创建问答服务时通过 `parameters.agent_options` 传入 `agent_id`，或调用检索接口时在请求体中指定 `top_k` 和 `query`。

## 使用方式

### 1. 控制台快速上手
- **创建**：进入 [知识管理](https://bailian.console.aliyun.com/cn-beijing/rag/knowledge/list)，选择“文档搜索”类型与“基础文档问答”场景，上传 PDF/Word/MD 文件，系统自动完成解析、切片、向量化。
- **调试**：在 [Playground](https://bailian.console.aliyun.com/cn-beijing/rag/playground) 中选择知识库，切换“知识问答”或“知识检索”模式，实时验证效果。
- **发布服务**：在 [知识检索](https://bailian.console.aliyun.com/cn-beijing/rag/retrieval/list) 或 [知识问答](https://bailian.console.aliyun.com/cn-beijing/rag/qa/list) 页面创建服务，绑定知识库并配置参数后“发布”。

### 2. API 集成
- **底层检索**（单库）：调用 `/api/v1/indices/rag/index/retrieve`，需 `index_id`、`query`、`top_k`，返回原始切片数组。
- **应用级检索**（多库联合）：调用 `/api/v1/indices/knowledge/search`，仅需 `query` 和 `agent_id`（对应已发布的检索服务），策略由服务配置驱动。
- **流式问答**：调用 `/api/v2/apps/knowledge/chat`，支持 SSE 流式响应，需 `agent_id` 与消息体，详见[知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)。

### 3. CLI 与第三方接入
- **CLI**：`bl knowledge search --query "xxx" --agent-id <id>` 或 `bl knowledge chat --message "xxx" --agent-id <id>`，适合本地调试与脚本调度。
- **第三方平台**：Dify/Coze/n8n/LangChain 均通过调用上述 REST API 接入；AgentScope 则通过自定义中间件调用知识检索 API，实现 `static`（注入 system prompt）与 `agentic`（暴露 `search_knowledge` 工具）两种模式，详见[接入 AgentScope](../../raw/application-user-guide/knowledge-base/best-practices/knowledge-as-memory.md)。

## 限制和注意事项

- **地域限制**：知识库功能在中国站仅支持**华北2（北京）**，国际站仅支持**新加坡**，其他地域（如德国法兰克福）不支持 [知识库API指南](../../raw/application-user-guide/knowledge-base/integration/rag-knowledge-base-api-guide.md)。
- **容量上限**：
  - 单业务空间最多 50 个知识库；
  - 单知识库最多 100,000 个文档；
  - 单次上传最多 50 个文件，PDF/DOCX 单文件 ≤ 150 MB 或 1000 页；
  - 问答服务单次最多召回 20 个切片（影响自动打标等实践的完整性）[文件自动打标](../../raw/application-user-guide/knowledge-base/best-practices/auto-tag.md)。
- **配置不可变性**：切片方式与最大分段长度在导入数据时配置，**创建后不可更改**，需谨慎选择 [切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)。
- **计费与免费额度**：自 2026 年 1 月 4 日起正式计费，提供 720 小时一次性免费额度（仅抵扣标准版规格费），老用户额度有效期至 2026 年 2 月 3 日，新用户为开通后 30 天 [知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)。
- **安全与合规**：删除知识库或文档为**永久操作且不可恢复**；API Key 属于敏感凭证，严禁硬编码或明文输出，应通过环境变量或阿里云 CLI 安全配置 [快速配置到 Agent](../../raw/application-user-guide/knowledge-base/integration/agent-cli.md)。

## 来源文档

- [快速开始](../../raw/application-user-guide/knowledge-base/quickstart.md)
- [Playground](../../raw/application-user-guide/knowledge-base/playground.md)
- [核心概念](../../raw/application-user-guide/knowledge-base/concepts.md)
- [数据接入](../../raw/application-user-guide/knowledge-base/data-connection-overview.md)
- [数据集](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-connection.md)
- [创建知识库](../../raw/application-user-guide/knowledge-base/data-connection-overview/rag-knowledge-base.md)
- [切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)
- [文档管理与解析](../../raw/application-user-guide/knowledge-base/data-connection-overview/documents.md)
- [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-sync-guide.md)
- [知识服务](../../raw/application-user-guide/knowledge-base/service.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)
- [最佳实践](../../raw/application-user-guide/knowledge-base/best-practices.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/best-practices/rag-optimization.md)
- [多轮对话：正确传递工具调用历史](../../raw/application-user-guide/knowledge-base/best-practices/multi-turn-chat.md)
- [文件自动打标：用大模型生成文档标签](../../raw/application-user-guide/knowledge-base/best-practices/auto-tag.md)
- [接入 AgentScope](../../raw/application-user-guide/knowledge-base/best-practices/knowledge-as-memory.md)
- [应用集成](../../raw/application-user-guide/knowledge-base/integration.md)
- [快速配置到 Agent](../../raw/application-user-guide/knowledge-base/integration/agent-cli.md)
- [服务渠道](../../raw/application-user-guide/knowledge-base/integration/channels.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/integration/rag-knowledge-base-api-guide.md)
- [使用 CLI](../../raw/application-user-guide/knowledge-base/integration/cli.md)
- [第三方平台接入](../../raw/application-user-guide/knowledge-base/integration/third-party.md)
- [参考](../../raw/application-user-guide/knowledge-base/reference.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-log-monitoring.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)
- [容量与限制](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-specifications.md)
- [更新日志](../../raw/application-user-guide/knowledge-base/changelog.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-retrieval.md)


