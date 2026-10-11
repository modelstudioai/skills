# knowledge base

阿里云百炼知识库（Knowledge Base）是面向 RAG 场景的托管式向量检索服务，支持文档、表格、图片、音视频等多模态数据的解析、切片、向量化与联合检索。它提供统一 API 接口和多种集成方式（REST API、MCP、CLI、Agent Skill），可作为智能体的记忆体或独立检索/问答服务接入业务系统。知识库能力深度集成于百炼平台，与大模型生成链路协同优化。

## 支持的模型/功能

知识库本身不直接调用生成模型，但其检索结果可被多种模型消费，并依赖嵌入与重排模型完成语义处理：

- **嵌入模型**：创建知识库时指定，默认为 `text-embedding-v4`，用于将切片转为向量；该配置创建后不可更改 [创建知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。
- **重排（Rerank）模型**：在检索服务或问答服务中按需启用，如 `qwen3-rerank`（纯文本）、`qwen3-vl-rerank`（多模态），支持“问答模式”与“相似模式”两种排序逻辑 [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)。
- **生成模型**：知识问答服务支持绑定 Qwen 系列模型（如 `qwen3.6-plus`），用于基于召回切片生成自然语言回答 [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)。

核心功能包括：
- 多模态知识库类型（文档搜索、数据查询、图片问答、音视频搜索）；
- 智能切片策略（智能切分、按页、按标题等）与手动切片管理；
- 标签过滤、元数据抽取、Query 改写等高级检索控制；
- 多知识库联合检索（路由 + 混排）与多轮智能问答（Agentic 检索）；
- 与 AgentScope、Dify、Coze、n8n 等第三方框架的标准化对接能力 [第三方平台接入](../../raw/application-user-guide/knowledge-base/integration/third-party.md)。

> **注意**：文档 28 明确指出知识库 API 在中国站仅支持华北2（北京）地域，在国际站仅支持新加坡地域；而其他多篇文档（如文档 8、24）的示例 endpoint 均使用 `cn-beijing`，未提及其他地域兼容性。若开发者尝试在法兰克福等非支持地域调用，将失败。请严格遵循 [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md) 的地域约束。

## 关键参数

以下参数在知识库生命周期各阶段起关键作用：

| 参数 | 位置 | 取值范围 | 说明 |
|------|------|----------|------|
| `top_k` | 底层检索接口、知识库独立配置 | 1–100（召回阶段） / 1–20（最终返回） | 控制初步召回数量（向量/关键词）及最终返回切片数；最大召回数量上限为 20 [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md) |
| `similarity_threshold` | 知识库独立配置、全局检索配置 | 0.01–1.0 | 过滤排序后低分切片；值越高精度越高，但可能漏召 [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md) |
| `chunk_max_length` | 导入数据 → 索引设置 | 10–6000 token | 切片最大长度；默认 600，创建后不可更改 [切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md) |
| `RCU`（Retrieval Compute Unit） | 规格配置（旗舰版） | 1–200 | 衡量并发检索能力，1 RCU ≈ 支撑 50 QPS；变配按小时分段计费 [知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md) |
| `tags` | 文档标签、检索请求参数 | 单个 ≤32 字符，每文档 ≤100 个 | 用于精准过滤检索范围；支持 `字段名_值` 结构化表达 [文件自动打标](../../raw/application-user-guide/knowledge-base/best-practices/auto-tag.md) |

## 使用方式

知识库可通过控制台快速验证，也可通过 API/SDK 集成至生产环境：

- **控制台快速验证**：使用 [Playground](../../raw/application-user-guide/knowledge-base/playground.md) 选择知识库并输入问题，实时查看检索切片与模型回答；或在知识库详情页直接进行“知识检索”或“知识问答”测试。
- **API 直接调用**：
  - *底层单库检索*：`POST /api/v1/indices/rag/index/retrieve`，需传 `index_id`、`query`、`top_k`；返回原始召回结果，**不包含重排** [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)。
  - *应用级联合检索*：`POST /api/v1/indices/knowledge/search`，传 `agent_id`（检索服务 ID），由服务配置驱动多库路由与混排 [服务渠道](../../raw/application-user-guide/knowledge-base/integration/channels.md)。
  - *流式问答*：`POST /api/v2/apps/knowledge/chat`，传 `agent_id` 与消息历史，支持传递工具调用历史实现多轮上下文复用 [多轮对话：正确传递工具调用历史](../../raw/application-user-guide/knowledge-base/best-practices/multi-turn-chat.md)。
- **命令行与 SDK**：
  - CLI：`bl knowledge search --agent-id <aid-xxx>`（推荐）或已弃用的 `bl knowledge retrieve --index-id <idx-xxx>` [使用 CLI](../../raw/application-user-guide/knowledge-base/integration/cli.md)。
  - Python SDK：需配置 `ALIBABA_CLOUD_ACCESS_KEY_ID`、`ALIBABA_CLOUD_ACCESS_KEY_SECRET` 和 `WORKSPACE_ID` 环境变量，并使用 `alibabacloud_bailian20231229` 客户端 [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。

## 限制和注意事项

- **容量硬限**：单业务空间最多 50 个知识库；单知识库最多 100,000 份文档；单次上传最多 50 个文件；切片最大长度 6000 token；最大召回数量 20 [容量与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。
- **地域与权限约束**：API 调用仅限北京（中国站）或新加坡（国际站）；子账号需具备 `AliyunBailianDataFullAccess` 策略并加入对应业务空间 [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。
- **计费关键点**：
  - 计费从知识库成功创建开始，**删除即永久停止计费**，但数据不可恢复 [知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)；
  - 免费额度（720 小时）**仅抵扣标准版规格费用**，不覆盖模型调用或旗舰版 RCU 费用；
  - 若选用自购 ADB-PG 作为向量存储，需额外支付 ADB-PG 费用。
- **行为注意事项**：
  - 切片策略、嵌入模型在知识库创建后**不可修改**，需重建知识库才能调整；
  - 删除文档或知识库均为**不可逆操作**，无回收站机制；
  - 日志服务（SLS）开通后，关闭“检索日志”开关仅停止新日志投递，历史日志仍计费，需手动删除 LogStore 彻底停费 [知识库日志与监控](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-log-monitoring.md)。

## 来源文档

- [更新日志](../../raw/application-user-guide/knowledge-base/changelog.md)
- [参考](../../raw/application-user-guide/knowledge-base/reference.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-log-monitoring.md)
- [应用集成](../../raw/application-user-guide/knowledge-base/integration.md)
- [第三方平台接入](../../raw/application-user-guide/knowledge-base/integration/third-party.md)
- [快速配置到 Agent](../../raw/application-user-guide/knowledge-base/integration/agent-cli.md)
- [服务渠道](../../raw/application-user-guide/knowledge-base/integration/channels.md)
- [多轮对话：正确传递工具调用历史](../../raw/application-user-guide/knowledge-base/best-practices/multi-turn-chat.md)
- [最佳实践](../../raw/application-user-guide/knowledge-base/best-practices.md)
- [使用 CLI](../../raw/application-user-guide/knowledge-base/integration/cli.md)
- [接入 AgentScope](../../raw/application-user-guide/knowledge-base/best-practices/knowledge-as-memory.md)
- [知识服务](../../raw/application-user-guide/knowledge-base/service.md)
- [文件自动打标：用大模型生成文档标签](../../raw/application-user-guide/knowledge-base/best-practices/auto-tag.md)
- [数据接入](../../raw/application-user-guide/knowledge-base/data-connection-overview.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)
- [数据集](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-connection.md)
- [文档管理与解析](../../raw/application-user-guide/knowledge-base/data-connection-overview/documents.md)
- [切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)
- [Playground](../../raw/application-user-guide/knowledge-base/playground.md)
- [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-sync-guide.md)
- [核心概念](../../raw/application-user-guide/knowledge-base/concepts.md)
- [创建知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [快速开始](../../raw/application-user-guide/knowledge-base/quickstart.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [容量与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)


