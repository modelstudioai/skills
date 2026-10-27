# knowledge base

知识库（Knowledge Base）是百炼平台 RAG 能力的核心载体，用于组织文档、切片、嵌入向量与索引配置，对外提供检索与问答服务。它支持多类型数据源（文档、表格、图片、音视频）和多种使用场景，通过解析、切片、向量化与索引构建完整处理链路，并可与大模型深度协同生成可信回答。

## 支持的模型/功能

知识库本身不直接运行大模型，但其检索与问答能力深度依赖以下模型和服务：

- **嵌入模型**：默认使用 `text-embedding-v4`，支持中英文语义向量生成；创建知识库时选定，不可更改 [创建知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。
- **重排（Rerank）模型**：全局或知识库级可选 `qwen3-rerank`（纯文本）、`qwen3-vl-rerank`（多模态），用于对召回结果精排 [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)。
- **生成模型**：问答服务中可自由选择 `qwen3.6-plus` 等模型，控制 `temperature` 与 `enable_thinking` 参数 [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)。
- **多模态能力**：图片问答类型依赖 Qwen-VL 解析与多模态 Embedding；音视频搜索依赖语音转写与片段定位模型 [创建知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

> **注意**：文档 29 中将“数据知识库”列为独立类型，但文档 1 明确将其归类为“知识库类型”下的“数据查询”，且文档 29 的“典型场景”描述（如“订单数据、库存报表”）与文档 1 的“数据查询”说明完全一致。此处以文档 1 的四分类（文档搜索 / 数据查询 / 图片问答 / 音视频搜索）为准，文档 29 的“数据知识库”属术语不统一，应视为同义表述。

## 关键参数

| 参数 | 取值范围 | 默认值 | 说明 |
|--------|-----------|---------|------|
| **最大分段长度** | 10–6000 token | 600 | 影响切片语义完整性；过短易丢失上下文，过长混杂主题 [切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md) |
| **初步向量检索 TopK** | 1–100 | 100 | 向量检索阶段初步召回数量，影响后续重排质量 [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md) |
| **相似度阈值** | 0.01–1.0 | — | 过滤低分切片；值越高精度越高，但可能漏召 [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md) |
| **最大召回数量** | 1–20 | 5 | 最终返回切片总数（经重排后）；自动打标等场景需调至 20 [文件自动打标](../../raw/application-user-guide/knowledge-base/best-practices/auto-tag.md) |
| **RCU（旗舰版）** | 1–200 | — | 检索并发能力单位，1 RCU ≈ 支撑 50 QPS；按需配置 [知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md) |

## 使用方式

### 控制台快速上手
1. **创建知识库**：进入 [数据接入 → 知识管理](https://bailian.console.aliyun.com/cn-beijing/rag/knowledge/list)，选择类型（如“文档搜索”）与场景（如“基础文档问答”），上传文件并保持默认索引设置 [快速开始](../../raw/application-user-guide/knowledge-base/rag-start-using/quickstart.md)。
2. **调试验证**：在 Playground 中选择知识库，切换“知识问答”模式输入问题，实时查看检索切片与模型回答 [Playground](../../raw/application-user-guide/knowledge-base/playground.md)。
3. **发布服务**：
   - **检索服务**：在 [知识服务 → 知识检索](https://bailian.console.aliyun.com/cn-beijing/rag/retrieval/list) 创建，绑定多个知识库并配置权重、混排模型；
   - **问答服务**：在 [知识服务 → 知识问答](https://bailian.console.aliyun.com/cn-beijing/rag/qa/list) 创建，配置生成模型与检索策略（极速/多轮智能）。

### API 与集成
- **底层检索**：调用 `/api/v1/indices/rag/index/retrieve`，直连单知识库，返回原始向量+关键词结果（无重排）[知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)。
- **应用级检索**：调用 `/api/v1/indices/knowledge/search`，传入 `agent_id`，由检索服务配置驱动多库路由、混排与过滤 [服务渠道](../../raw/application-user-guide/knowledge-base/integration/channels.md)。
- **CLI 快速验证**：`bl knowledge search --query "问题" --agent-id <检索服务ID>` [使用 CLI](../../raw/application-user-guide/knowledge-base/integration/cli.md)。
- **第三方接入**：Dify/Coze/n8n/LangChain 均通过 DashScope REST API 接入，核心为 `Authorization: Bearer <API-Key>` 鉴权 [第三方平台接入](../../raw/application-user-guide/knowledge-base/integration/third-party.md)。

## 限制和注意事项

- **容量限制**：单业务空间最多 50 个知识库；单知识库最多 10 万文档；单次上传最多 50 个文件（总大小≤150 MB/文件）[容量与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。
- **配置不可变性**：切片方式、最大分段长度、嵌入模型等在知识库创建或导入时确定，**创建后不可修改**，需重建知识库 [切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)。
- **地域与权限**：知识库 API 仅支持华北2（北京）与中国站；子账号需 `AliyunBailianDataFullAccess` 权限并加入业务空间 [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。
- **免费额度规则**：720 小时免费额度仅抵扣**标准版**知识库规格费用，不覆盖模型调用费；老用户额度统一截止于 2026 年 2 月 3 日 [知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)。
- **删除风险**：删除知识库或文档将**永久清除数据且不可恢复**，操作前务必确认 [容量与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。

## 来源文档

- [创建知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [容量与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [参考](../../raw/application-user-guide/knowledge-base/reference.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-log-monitoring.md)
- [更新日志](../../raw/application-user-guide/knowledge-base/changelog.md)
- [快速配置到 Agent](../../raw/application-user-guide/knowledge-base/integration/agent-cli.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)
- [应用集成](../../raw/application-user-guide/knowledge-base/integration.md)
- [服务渠道](../../raw/application-user-guide/knowledge-base/integration/channels.md)
- [使用 CLI](../../raw/application-user-guide/knowledge-base/integration/cli.md)
- [第三方平台接入](../../raw/application-user-guide/knowledge-base/integration/third-party.md)
- [最佳实践](../../raw/application-user-guide/knowledge-base/best-practices.md)
- [文件自动打标：用大模型生成文档标签](../../raw/application-user-guide/knowledge-base/best-practices/auto-tag.md)
- [多轮对话：正确传递工具调用历史](../../raw/application-user-guide/knowledge-base/best-practices/multi-turn-chat.md)
- [接入 AgentScope](../../raw/application-user-guide/knowledge-base/best-practices/knowledge-as-memory.md)
- [知识服务](../../raw/application-user-guide/knowledge-base/service.md)
- [数据接入](../../raw/application-user-guide/knowledge-base/data-connection-overview.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)
- [数据集](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-connection.md)
- [文档管理与解析](../../raw/application-user-guide/knowledge-base/data-connection-overview/documents.md)
- [切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)
- [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-sync-guide.md)
- [开始使用](../../raw/application-user-guide/knowledge-base/rag-start-using.md)
- [快速开始](../../raw/application-user-guide/knowledge-base/rag-start-using/quickstart.md)
- [Playground](../../raw/application-user-guide/knowledge-base/playground.md)
- [核心概念](../../raw/application-user-guide/knowledge-base/rag-start-using/concepts.md)


