# knowledge base

知识库（Knowledge Base）是阿里云百炼平台 RAG（[检索增强生成](../concepts/rag.md)）能力的核心载体，用于组织、索引和检索企业私有文档、表格、图片及音视频等[多模态](../concepts/multi-modal.md)数据。它将原始内容经解析、切片、向量化后构建可检索的语义索引，并通过检索服务或问答服务对外提供结构化查询与自然语言回答能力。知识库本身不直接执行生成，而是作为大模型的“外部记忆”参与推理链路。

## 支持的模型/功能

知识库支持多种数据类型与检索模式，对应不同模型与处理能力：

- **知识库类型**：分为**文档搜索**（PDF/Word/Markdown 等，向量+关键词混合检索）、**数据查询**（CSV/Excel/RDS，NL2SQL）、**图片问答**（[多模态](../concepts/multi-modal.md) Embedding）、**音视频搜索**（语音转写+片段定位）四类。其中文档搜索为最常用类型，[创建知识库](raw/application-user-guide/knowledge-base/rag-knowledge-base.md)时需明确选择。
- **嵌入模型**：默认使用 `text-embedding-v4`，支持中英文语义向量化；创建后不可更改，详见[切片与向量化](raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)。
- **重排（Rerank）模型**：支持 `qwen3-rerank`（纯文本）、`qwen3-vl-rerank`（[多模态](../concepts/multi-modal.md)）等，用于对初步召回结果精排；可在[知识检索](raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)或[知识问答](raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)的服务配置中启用。
- **生成模型**：问答服务中可自由选用 Qwen 系列（如 `qwen3.6-plus`）、DeepSeek 等大模型，通过提示词与参数控制回答风格。

> **注意**：文档 29 中将“数据知识库”列为独立类型，但文档 2 明确说明其对应“数据查询”知识库类型，且该类型无“使用场景”选项；二者术语一致，无实质矛盾，但建议以文档 2 的四分类为准。

## 关键参数

以下参数在知识库创建或服务配置阶段设定，直接影响检索质量与性能：

- **切片方式**：默认 `智能切分`，亦支持按长度、页、标题、正则、符号切分；最大分段长度范围 10–6000 token，默认 600；创建后不可修改，见[文档管理](raw/application-user-guide/knowledge-base/data-connection-overview/documents.md)。
- **检索 TopK**：初步向量/关键词检索阶段召回数量（1–100），排序后最终返回数量（1–20），均在[知识检索](raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)或[知识问答](raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)的独立配置中设置。
- **相似度阈值**：0.01–1.0，用于过滤低分切片；值越高结果越精确但可能漏召。
- **Query 改写**：开关控制，适用于多轮对话中补全省略上下文（如将“手机X1”改写为“请提供产品库中所有在售版本的手机X1及其参数信息”），在知识库独立配置中启用。
- **标签与元数据**：支持导入时或导入后为文档添加标签（用于过滤）及抽取元数据（如 `{"key": "name", "value": "手机X1"}`），提升检索精准度，详见[RAG效果优化](raw/application-user-guide/knowledge-base/rag-optimization.md)。

## 使用方式

知识库可通过控制台、API、CLI 或第三方平台集成：

- **控制台快速验证**：使用 [Playground](raw/application-user-guide/knowledge-base/playground.md) 选择知识库并输入问题，实时查看检索切片与模型回答；或在知识库详情页直接调试检索/问答。
- **API 集成**：
  - 底层单库检索：调用 `/api/v1/indices/rag/index/retrieve`（需 `index_id`），返回原始召回切片；
  - 应用级联合检索：调用 `/api/v1/indices/knowledge/search`（需 `agent_id`），由检索服务配置驱动权重、路由与混排；
  - 流式问答：调用 `/api/v2/apps/knowledge/chat`，支持 SSE 返回。
- **CLI 工具**：`bl knowledge search --agent-id <id> --query "xxx"` 或 `bl knowledge chat --agent-id <id> --message "xxx"`，适合本地调试。
- **第三方接入**：支持 Dify（External Knowledge）、Coze（MCP/API 插件）、n8n（HTTP 节点）、LangChain（自定义 Retriever）等，基础均为 DashScope API，详见[第三方平台接入](raw/application-user-guide/knowledge-base/integration/third-party.md)。

## 限制和注意事项

- **地域限制**：知识库功能仅在中国站（华北2 北京）和国际站（新加坡）可用，其他地域不支持，见[知识库API指南](raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。
- **容量上限**：单知识库最多 100,000 文档；单次上传最多 50 个文件；PDF 单文件 ≤150 MB 或 1000 页；切片内容长度上限 6000 字；详见[容量与限制](raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。
- **计费说明**：自 2026 年 1 月 4 日起计费，含规格费（标准版 0.03 元/小时，旗舰版按 RCU 计费）与模型调用费；免费额度仅抵扣标准版规格费，720 小时内有效，过期自动转后付费，见[知识库计费说明](raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)。
- **关键约束**：切片与向量化配置创建后不可更改；删除知识库或文档将**永久清除数据且无法恢复**；标签仅支持中文、英文字母、数字、下划线 `_`、中划线 `-`，单个标签 ≤64 字符。

## 来源文档

- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [创建知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [更新日志](../../raw/application-user-guide/knowledge-base/changelog.md)
- [容量与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [参考](../../raw/application-user-guide/knowledge-base/reference.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-log-monitoring.md)
- [快速配置到 Agent](../../raw/application-user-guide/knowledge-base/integration/agent-cli.md)
- [应用集成](../../raw/application-user-guide/knowledge-base/integration.md)
- [服务渠道](../../raw/application-user-guide/knowledge-base/integration/channels.md)
- [第三方平台接入](../../raw/application-user-guide/knowledge-base/integration/third-party.md)
- [使用 CLI](../../raw/application-user-guide/knowledge-base/integration/cli.md)
- [最佳实践](../../raw/application-user-guide/knowledge-base/best-practices.md)
- [多轮对话：正确传递工具调用历史](../../raw/application-user-guide/knowledge-base/best-practices/multi-turn-chat.md)
- [文件自动打标：用大模型生成文档标签](../../raw/application-user-guide/knowledge-base/best-practices/auto-tag.md)
- [接入 AgentScope](../../raw/application-user-guide/knowledge-base/best-practices/knowledge-as-memory.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)
- [知识服务](../../raw/application-user-guide/knowledge-base/service.md)
- [数据接入](../../raw/application-user-guide/knowledge-base/data-connection-overview.md)
- [文档管理与解析](../../raw/application-user-guide/knowledge-base/data-connection-overview/documents.md)
- [数据集](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-connection.md)
- [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-sync-guide.md)
- [切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)
- [Playground](../../raw/application-user-guide/knowledge-base/playground.md)
- [快速开始](../../raw/application-user-guide/knowledge-base/rag-start-using/quickstart.md)
- [开始使用](../../raw/application-user-guide/knowledge-base/rag-start-using.md)
- [核心概念](../../raw/application-user-guide/knowledge-base/rag-start-using/concepts.md)


