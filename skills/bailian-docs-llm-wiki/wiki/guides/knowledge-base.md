# knowledge base

阿里云百炼知识库（Knowledge Base）是面向企业私有数据构建 RAG（[检索增强生成](../concepts/rag.md)）能力的核心服务，支持文档、表格、图片、音视频等多模态数据的接入、解析、切片、向量化与索引构建，并提供可配置的检索与问答服务。开发者可通过控制台快速创建，或通过 API/CLI/MCP 等方式集成至自有应用或 AI Agent 框架。

## 支持的模型/功能

知识库本身不直接运行大模型，但深度集成以下模型能力以支撑完整 RAG 链路：

- **嵌入模型（Embedding）**：默认使用 `text-embedding-v4`，支持中英文语义向量生成；创建知识库时选定，**创建后不可更改** [切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)。
- **重排模型（Rerank）**：支持 `qwen3-rerank`（纯文本）、`qwen3-vl-rerank`（多模态）等，用于对初步召回结果进行精排；可在[知识检索](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-retrieval.md)或[知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)服务中按需启用。
- **生成模型（LLM）**：问答阶段支持 Qwen 系列模型（如 `qwen3.6-plus`），在[知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)服务中配置，影响回答质量与引用准确性。
- **解析模型**：提供“大模型文档解析”和“Qwen-VL 解析”选项，适用于非标格式或图文混排文档，详见[创建知识库](../../raw/application-user-guide/knowledge-base/data-connection-overview/rag-knowledge-base.md)。

功能上覆盖全生命周期管理：从数据接入（上传文件、OSS/语雀/钉钉同步）、结构化解析、智能切片、向量化索引，到可配置的单库/多库联合检索、带引用的流式问答，以及日志监控与容量治理。

## 关键参数

核心参数按配置层级划分，部分仅在特定场景生效：

| 参数类别 | 参数名 | 取值范围 | 说明 | 配置位置 |
|----------|--------|----------|------|-----------|
| **切片** | 最大分段长度 | 10–6000 token | 影响切片粒度与上下文完整性 | [导入数据](../../raw/application-user-guide/knowledge-base/data-connection-overview/documents.md) 或 [创建知识库](../../raw/application-user-guide/knowledge-base/data-connection-overview/rag-knowledge-base.md) 的索引设置页 |
| **检索** | 初步向量检索 TopK | 1–100 | 向量召回阶段返回的切片数 | [知识检索](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-retrieval.md) 或 [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md) 的知识库独立配置 |
| **检索** | 相似度阈值 | 0.01–1.0 | 过滤低分切片，值越高越严格 | 同上 |
| **检索** | 最大召回数量 | 1–20 | 最终返回给下游（模型或用户）的切片总数 | 同上；注意此为全局上限，非单库上限 |
| **问答** | `temperature` | 0.0–1.0 | 控制生成答案的随机性 | [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md) 服务模型设置 |
| **服务** | RCU（旗舰版） | 1–200 | 检索并发能力单位，1 RCU ≈ 50 QPS | [知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md) |

> **注意**：切片方式（智能切分/按长度/按页等）和最大分段长度在知识库创建或文档导入时配置，**创建后不可更改**，需在初始配置阶段审慎选择 [切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)。

## 使用方式

### 控制台快速验证
1. **创建知识库**：进入 [知识管理](https://bailian.console.aliyun.com/cn-beijing/rag/knowledge/list)，选择“文档搜索”类型与“基础文档问答”场景，上传 PDF/MD 等文件，系统自动完成解析、切片与索引 [快速开始](../../raw/application-user-guide/knowledge-base/quickstart.md)。
2. **Playground 调试**：在 [Playground](https://bailian.console.aliyun.com/cn-beijing/rag/playground) 中选择知识库，切换“知识问答”模式输入问题，实时查看检索切片与模型回答，支持模型对比与引用高亮 [Playground](../../raw/application-user-guide/knowledge-base/playground.md)。
3. **发布服务**：在 [知识服务 → 知识检索](https://bailian.console.aliyun.com/cn-beijing/rag/retrieval/list) 或 [知识服务 → 知识问答](https://bailian.console.aliyun.com/cn-beijing/rag/qa/list) 中创建服务，绑定知识库并配置参数，发布后获得唯一 `agent_id`。

### API/CLI 集成
- **底层检索（单库）**：调用 `/api/v1/indices/rag/index/retrieve`，需传 `index_id` 和 `query`，返回原始切片列表（无重排）。
- **应用级检索（多库）**：调用 `/api/v1/indices/knowledge/search`，传 `agent_id` 和 `query`，策略由服务配置驱动，推荐生产使用 [服务渠道](../../raw/application-user-guide/knowledge-base/integration/channels.md)。
- **流式问答**：调用 `/api/v2/apps/knowledge/chat`，SSE 流式返回回答与引用 [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)。
- **CLI 快速调试**：`bl knowledge search --agent-id <id> --query "xxx"` 或 `bl knowledge chat --agent-id <id> --message "xxx"` [使用 CLI](../../raw/application-user-guide/knowledge-base/integration/cli.md)。

### 第三方与框架接入
- **Agent 框架**：通过 MCP Server 接入 Qoder/Claude Code 等客户端；或通过自定义中间件（如 `KnowledgeStudioRAGMiddleware`）接入 AgentScope [接入 AgentScope](../../raw/application-user-guide/knowledge-base/best-practices/knowledge-as-memory.md)。
- **低代码平台**：Dify/Coze/n8n 等支持通过外部知识库或 HTTP 请求对接 DashScope API [第三方平台接入](../../raw/application-user-guide/knowledge-base/integration/third-party.md)。

## 限制和注意事项

- **地域限制**：知识库功能在中国站仅支持 **华北2（北京）**，国际站仅支持 **新加坡**，其他地域（如德国法兰克福）不支持 [知识库API指南](../../raw/application-user-guide/knowledge-base/integration/rag-knowledge-base-api-guide.md)。
- **容量硬限**：
  - 单业务空间最多 50 个知识库；
  - 单知识库最多 100,000 个文档；
  - 单次上传最多 50 个文件，PDF/DOCX 单文件 ≤ 150 MB 或 1000 页 [容量与限制](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-specifications.md)。
- **免费额度**：所有用户享一次性 720 小时免费额度，**仅抵扣标准版知识库规格费用，不包含模型调用费用**；老用户额度有效期截至 2026 年 2 月 3 日，新用户为开通后 30 天内有效 [知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)。
- **数据同步行为**：OSS/飞书/钉钉等来源的同步规则会将文件作为**独立副本**存储于百炼平台，源文件删除不影响副本，需手动删除 [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-sync-guide.md)。
- **API 限流**：检索类接口 QPS 上限为 2,000，超出返回 `429`；若需更高配额，须通过工单申请 [容量与限制](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-specifications.md)。

## 来源文档

- [快速开始](../../raw/application-user-guide/knowledge-base/quickstart.md)
- [Playground](../../raw/application-user-guide/knowledge-base/playground.md)
- [核心概念](../../raw/application-user-guide/knowledge-base/concepts.md)
- [数据接入](../../raw/application-user-guide/knowledge-base/data-connection-overview.md)
- [创建知识库](../../raw/application-user-guide/knowledge-base/data-connection-overview/rag-knowledge-base.md)
- [文档管理与解析](../../raw/application-user-guide/knowledge-base/data-connection-overview/documents.md)
- [数据集](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-connection.md)
- [切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)
- [知识服务](../../raw/application-user-guide/knowledge-base/service.md)
- [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-sync-guide.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-retrieval.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)
- [最佳实践](../../raw/application-user-guide/knowledge-base/best-practices.md)
- [多轮对话：正确传递工具调用历史](../../raw/application-user-guide/knowledge-base/best-practices/multi-turn-chat.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/best-practices/rag-optimization.md)
- [文件自动打标：用大模型生成文档标签](../../raw/application-user-guide/knowledge-base/best-practices/auto-tag.md)
- [快速配置到 Agent](../../raw/application-user-guide/knowledge-base/integration/agent-cli.md)
- [接入 AgentScope](../../raw/application-user-guide/knowledge-base/best-practices/knowledge-as-memory.md)
- [服务渠道](../../raw/application-user-guide/knowledge-base/integration/channels.md)
- [第三方平台接入](../../raw/application-user-guide/knowledge-base/integration/third-party.md)
- [使用 CLI](../../raw/application-user-guide/knowledge-base/integration/cli.md)
- [参考](../../raw/application-user-guide/knowledge-base/reference.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-log-monitoring.md)
- [容量与限制](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-specifications.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)
- [更新日志](../../raw/application-user-guide/knowledge-base/changelog.md)
- [应用集成](../../raw/application-user-guide/knowledge-base/integration.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/integration/rag-knowledge-base-api-guide.md)


