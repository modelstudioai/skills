# knowledge base

阿里云百炼知识库（Knowledge Base）是面向 RAG 场景的托管式向量检索服务，支持文档、表格、图片、音视频等多模态数据的解析、切片、向量化与联合检索，并可与大模型深度集成实现问答、多轮对话与智能记忆。其核心能力围绕“索引构建—检索召回—生成增强”链路展开，提供控制台可视化配置与完备的 API/CLI/MCP/Agent 多通道接入能力。

## 支持的模型与功能

知识库本身不直接提供生成模型，但深度集成百炼平台的 Embedding 与 Rerank 模型，并支持绑定 Qwen 系列大模型用于问答生成：

- **Embedding 模型**：默认 `text-embedding-v4`（中英文通用），创建知识库时选定且不可更改，详见 [创建知识库](raw/application-user-guide/knowledge-base/rag-knowledge-base.md)；
- **Rerank 模型**：支持 `qwen3-rerank`（文本）、`qwen3-vl-rerank`（多模态）等，可在[知识检索](raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)或[知识问答](raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)的服务配置中为单库或全局启用；
- **生成模型**：问答服务支持 `qwen3.6-plus`、`deepseek` 等模型，通过控制台或 API 配置，影响回答质量与引用准确性。

核心功能包括：
- 多源数据接入（OSS、飞书、钉钉、语雀、SharePoint、MySQL 等），支持定时同步；
- 六种切片策略（智能切分、按长度/页/标题/正则/符号），最大分段长度支持 10–6000 token；
- 标签过滤、元数据抽取、Query 改写、多知识库路由与混排；
- Playground 交互式调试、日志服务（SLS）全链路监控、CLI 命令行快速验证。

> **注意**：文档 26 明确指出知识库 API 在中国站**仅支持华北2（北京）地域**，国际站仅支持新加坡，其他地域（如德国法兰克福）不支持——该限制在控制台 UI 中无显式提示，需开发者主动校验。

## 关键参数

以下参数直接影响检索效果与资源消耗，需根据场景合理配置：

| 参数类别 | 参数名 | 取值范围 | 说明 |
|----------|--------|----------|------|
| **切片** | 最大分段长度 | 10–6000 token | 默认 600；过短丢失上下文，过长引入噪声；[切片与向量化](raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)中配置且不可变 |
| **检索** | `top_k`（初步召回） | 1–100 | 向量/关键词阶段各召回数量，非最终返回数；[知识检索](raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)中可独立设置 |
| **检索** | 最大召回数量 | 1–20 | 排序后最终返回切片数，受 Rerank 模型能力约束；[知识问答](raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)中上限为 20 |
| **检索** | 相似度阈值 | 0.01–1.0 | 过滤低分切片，值越高越严格，可能漏召；建议从 0.3 开始调优 |
| **服务** | RCU（旗舰版） | 1–200 | 1 RCU ≈ 支撑 50 QPS；估算公式：`ceil(峰值 QPS ÷ 50)`；[知识库计费说明](raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)中明确定义 |

## 使用方式

知识库可通过多种方式快速集成，推荐路径如下：

1. **快速验证**：使用控制台 [Playground](raw/application-user-guide/knowledge-base/playground.md)，选择知识库并切换“知识问答”模式，实时查看检索+生成效果；
2. **应用集成**：
   - **REST API**：调用 `/api/v1/indices/knowledge/search`（应用级联合检索）或 `/api/v1/indices/rag/index/retrieve`（单库底层检索），需 `Authorization: Bearer <API-Key>`；
   - **CLI**：`bl knowledge search --query "xxx" --agent-id <aid-xxx>`（推荐）或已弃用的 `bl knowledge retrieve`；
   - **MCP Server**：供 Qoder/Claude Code 等 Agent 直接调用，配置 URL 与 `DASHSCOPE_API_KEY` 即可；
   - **第三方平台**：Dify/Coze/n8n/LangChain 均通过 DashScope API 接入，[第三方平台接入](raw/application-user-guide/knowledge-base/integration/third-party.md)提供完整示例代码；
3. **Agent 深度集成**：
   - 通过 [Agent Skill](raw/application-user-guide/knowledge-base/integration/agent-cli.md) 快速安装至 Claude Code/Qoder 等客户端；
   - 在 [AgentScope](raw/application-user-guide/knowledge-base/best-practices/knowledge-as-memory.md) 中编写自定义中间件，支持 `static`（注入 system prompt）与 `agentic`（暴露 `search_knowledge` 工具）双模式。

## 限制和注意事项

- **容量硬限**：单业务空间最多 50 个知识库、单知识库最多 100,000 文档、单次上传最多 50 个文件；超限时需申请工单提升（见 [容量与限制](raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)）；
- **免费额度规则**：720 小时免费额度**仅抵扣标准版知识库规格费用**，不覆盖模型调用费、SLS 日志费或 ADB-PG 存储费；老用户额度统一于 2026 年 2 月 3 日到期，新用户 30 天内有效；
- **关键行为风险**：
  - 删除知识库或文档将**永久清除数据且无法恢复**（见 [知识库计费说明](raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)）；
  - 关闭 SLS 检索日志开关仅停止新日志投递，历史日志仍计费，需手动删除 LogStore 彻底停费；
- **技术约束**：
  - 切片策略与向量化模型在知识库创建时锁定，后续不可修改；
  - 知识问答服务最大召回数为 20，超长文档（切片 >20）需拆分或分批打标（见 [文件自动打标](raw/application-user-guide/knowledge-base/best-practices/auto-tag.md)）；
  - 多轮对话必须显式传递 `tool_calls` 与工具返回结果，否则模型无法复用历史检索（见 [多轮对话](raw/application-user-guide/knowledge-base/best-practices/multi-turn-chat.md)）。

## 来源文档

- [更新日志](../../raw/application-user-guide/knowledge-base/changelog.md)
- [参考](../../raw/application-user-guide/knowledge-base/reference.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-log-monitoring.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)
- [应用集成](../../raw/application-user-guide/knowledge-base/integration.md)
- [快速配置到 Agent](../../raw/application-user-guide/knowledge-base/integration/agent-cli.md)
- [服务渠道](../../raw/application-user-guide/knowledge-base/integration/channels.md)
- [使用 CLI](../../raw/application-user-guide/knowledge-base/integration/cli.md)
- [第三方平台接入](../../raw/application-user-guide/knowledge-base/integration/third-party.md)
- [多轮对话：正确传递工具调用历史](../../raw/application-user-guide/knowledge-base/best-practices/multi-turn-chat.md)
- [最佳实践](../../raw/application-user-guide/knowledge-base/best-practices.md)
- [文件自动打标：用大模型生成文档标签](../../raw/application-user-guide/knowledge-base/best-practices/auto-tag.md)
- [接入 AgentScope](../../raw/application-user-guide/knowledge-base/best-practices/knowledge-as-memory.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)
- [知识服务](../../raw/application-user-guide/knowledge-base/service.md)
- [数据接入](../../raw/application-user-guide/knowledge-base/data-connection-overview.md)
- [数据集](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-connection.md)
- [文档管理与解析](../../raw/application-user-guide/knowledge-base/data-connection-overview/documents.md)
- [切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)
- [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-sync-guide.md)
- [Playground](../../raw/application-user-guide/knowledge-base/playground.md)
- [核心概念](../../raw/application-user-guide/knowledge-base/concepts.md)
- [快速开始](../../raw/application-user-guide/knowledge-base/quickstart.md)
- [创建知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [容量与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)


