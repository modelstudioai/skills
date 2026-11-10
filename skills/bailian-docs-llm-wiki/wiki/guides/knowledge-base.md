# knowledge base

知识库（Knowledge Base）是百炼 RAG 平台的核心数据实体，将文档、切片、嵌入模型与索引配置封装为可复用的检索单元。它支持多模态数据接入与场景化检索策略，对外提供知识检索与问答两种服务形态。知识库本身不直接响应请求，需通过发布的检索服务或问答服务调用。

## 支持的模型/功能

知识库本身不绑定生成模型，但其检索结果会作为上下文输入至问答服务所配置的大模型（如 `qwen3.6-plus`、`qwen3.7-plus`）。检索阶段依赖两类模型：

- **嵌入模型（Embedding Model）**：在创建知识库时选定，用于将切片向量化。默认为 `qwen3.7-text-embedding`，亦可选 `text-embedding-v4`；该配置创建后不可更改 [创建知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。
- **重排模型（Rerank Model）**：在检索服务或问答服务中配置，用于对初步召回结果精排。支持 `qwen3-rerank`（纯文本）、`qwen3-vl-rerank`（多模态）等，可在全局或知识库独立配置中启用 [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)。

知识库类型决定底层能力边界：
- **文档搜索**：支持 PDF/DOCX/MD 等格式，采用向量 + 关键词混合检索；
- **数据查询**：对接 CSV/Excel/RDS，执行 NL2SQL 查询；
- **图片问答**：基于多模态 Embedding，支持图文混排理解；
- **音视频搜索**：依赖语音转写与时间戳定位 [创建知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

> **注意**：控制台已下线「图文并茂回复」使用场景入口；虽 API 仍接受 `visual_document_qa` 取值，但文档明确提示“不建议在新建知识库时使用” [创建知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

## 关键参数

所有关键参数均在创建或配置阶段设定，部分创建后不可修改：

| 参数 | 位置 | 可变性 | 说明 |
|------|------|--------|------|
| **最大分段长度** | 创建知识库 → 索引设置 | ❌ 不可更改 | 范围 10–6000 token，默认 600；直接影响切片粒度与召回精度 [切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md) |
| **切片方式** | 创建知识库 → 索引设置 | ❌ 不可更改 | 包括智能切分、按长度、按页、按标题、正则、符号六种；选择后无法回退 [文档管理与解析](../../raw/application-user-guide/knowledge-base/data-connection-overview/documents.md) |
| **Metadata 抽取** | 创建知识库 → 索引设置 → 开启并配置 | ❌ 创建后不可补配 | 最多 5 个字段，取值支持常量/变量/大模型/正则/关键词；仅创建时配置，后续需重建知识库 [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md) |
| **相似度阈值** | 检索服务 / 问答服务 → 知识库独立配置 | ✅ 可动态调整 | 范围 0.01–1.0；值越高结果越精确，但可能漏召 [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md) |
| **最大召回数量** | 检索服务 / 问答服务 → 全局或知识库独立配置 | ✅ 可动态调整 | 全局上限 20；问答服务中单知识库最大召回数亦为 20，超长文档需拆分或分批处理 [文件自动打标](../../raw/application-user-guide/knowledge-base/best-practices/auto-tag.md) |

## 使用方式

知识库需经“创建 → 导入 → 发布服务”三步方可使用：

1. **创建与导入**  
   在控制台 [**数据接入 → 知识管理**](https://bailian.console.aliyun.com/cn-beijing/rag/knowledge/list) 创建知识库，上传文件（单次 ≤50 个，单文件 ≤150 MB），完成解析与向量化。状态变为“解析完成”即就绪。

2. **发布服务**  
   - **检索服务**：进入 [**知识服务 → 知识检索**](https://bailian.console.aliyun.com/cn-beijing/rag/retrieval/list)，绑定知识库并配置混排、标签过滤等参数，发布后获得 `agent_id`。  
   - **问答服务**：进入 [**知识服务 → 知识问答**](https://bailian.console.aliyun.com/cn-beijing/rag/qa/list)，绑定知识库并配置生成模型、拒答、引用等参数，发布后获得 `agent_id`。

3. **调用方式**  
   - **REST API**：使用 `DASHSCOPE_API_KEY` 鉴权，调用 `/api/v1/indices/knowledge/search`（检索服务）或 `/api/v2/apps/knowledge/chat`（问答服务） [服务渠道](../../raw/application-user-guide/knowledge-base/integration/channels.md)。  
   - **CLI**：`bl knowledge search --agent-id <id> --query "xxx"` 或 `bl knowledge chat --agent-id <id> --message "xxx"` [使用 CLI](../../raw/application-user-guide/knowledge-base/integration/cli.md)。  
   - **第三方平台**：Dify/Coze/n8n/LangChain 均通过 DashScope API 接入，详见 [第三方平台接入](../../raw/application-user-guide/knowledge-base/integration/third-party.md)。

## 限制和注意事项

- **容量限制**：单知识库最多 100,000 文档；单文件上限 150 MB（文档）/ 20 MB（图片）/ 512 MB（音视频）；切片最大长度 6000 字符 [容量与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。  
- **地域限制**：知识库功能仅在中国站（华北2 北京）和国际站（新加坡）可用，其他地域不支持 [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。  
- **不可逆操作**：删除文档或知识库不可恢复；Metadata 抽取、切片方式、最大分段长度等核心配置创建后不可修改，需重建知识库 [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)。  
- **多轮对话陷阱**：RAG Agent 无状态，若未将 `tool_calls` 与返回结果作为历史传入，会导致重复检索。务必传递完整[工具调用](../concepts/tool-calling.md)链路 [多轮对话：正确传递工具调用历史](../../raw/application-user-guide/knowledge-base/best-practices/multi-turn-chat.md)。  
- **同步行为**：通过数据集同步的文件以独立副本形式存储，源文件删除不影响百炼副本；OSS 同步支持增量，但更新检测延迟取决于配置的同步周期（分钟/小时/天） [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-sync-guide.md)。

## 来源文档

- [创建知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [容量与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [参考](../../raw/application-user-guide/knowledge-base/reference.md)
- [应用集成](../../raw/application-user-guide/knowledge-base/integration.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-log-monitoring.md)
- [快速配置到 Agent](../../raw/application-user-guide/knowledge-base/integration/agent-cli.md)
- [第三方平台接入](../../raw/application-user-guide/knowledge-base/integration/third-party.md)
- [服务渠道](../../raw/application-user-guide/knowledge-base/integration/channels.md)
- [使用 CLI](../../raw/application-user-guide/knowledge-base/integration/cli.md)
- [最佳实践](../../raw/application-user-guide/knowledge-base/best-practices.md)
- [多轮对话：正确传递工具调用历史](../../raw/application-user-guide/knowledge-base/best-practices/multi-turn-chat.md)
- [文件自动打标：用大模型生成文档标签](../../raw/application-user-guide/knowledge-base/best-practices/auto-tag.md)
- [接入 AgentScope](../../raw/application-user-guide/knowledge-base/best-practices/knowledge-as-memory.md)
- [知识服务](../../raw/application-user-guide/knowledge-base/service.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)
- [数据接入](../../raw/application-user-guide/knowledge-base/data-connection-overview.md)
- [文档管理与解析](../../raw/application-user-guide/knowledge-base/data-connection-overview/documents.md)
- [数据集](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-connection.md)
- [切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)
- [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-sync-guide.md)
- [开始使用](../../raw/application-user-guide/knowledge-base/rag-start-using.md)
- [Playground](../../raw/application-user-guide/knowledge-base/playground.md)
- [快速开始](../../raw/application-user-guide/knowledge-base/rag-start-using/quickstart.md)
- [核心概念](../../raw/application-user-guide/knowledge-base/rag-start-using/concepts.md)


