# rag api

RAG API 是百炼平台提供的知识库管理与检索服务接口，支持开发者以编程方式完成知识库的创建、文档导入、切片管理、语义检索及知识问答等全流程操作。所有接口均通过 HTTPS 提供，采用统一的鉴权机制与 JSON 通信格式，适用于构建企业级智能知识服务。

## 支持的模型/功能

RAG API 支持多类知识库场景与模型能力：
- **知识库类型**：`document`（文档搜索）、`table`（数据查询）、`image`（图片问答）、`multimedia`（音视频搜索），需与 `structureType`（`unstructured`/`structured`）和 `knowledgeScene`（如 `basic_document_qa`、`visual_perception_qa`、`image_qa`）严格匹配 [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。
- **嵌入模型**：支持指定 `embeddingModelName`（如 `text-embedding-v4`）和 `multimodalEmbeddingModelName`（如 `qwen3-vl-embedding`），后者在 `knowledgeScene` 为 `image_qa` 或 `visual_perception_qa` 时为必填项 [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。
- **重排模型**：知识库可配置 `rerankModelName`（如 `qwen3-rerank`），并在检索时通过 `rerankTopN`、`rerankMinScore` 等参数控制结果过滤与排序 [查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)。
- **运行时服务**：提供两类核心运行时能力——跨知识库联合检索（`/api/v1/indices/knowledge/search`）与基于知识库的流式问答（`/api/v2/apps/knowledge/chat`），二者均依赖预先创建并发布的 RAG Agent 实例 [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)。

> **注意**：文档中 `knowledgeScene` 的取值存在不一致描述。[创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md) 明确列出 `lite_document_qa`、`visual_perception_qa`、`basic_table_qa` 等枚举值，但同文件又提及 `visual_document_qa`（图文并茂回复）已从控制台移除；而 [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md) 和 [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md) 文档未定义该字段，仅强调需在控制台发布服务。开发者应以控制台实际可用选项及 `create_index` 接口文档为准，避免使用已废弃的场景值。

## 关键参数

RAG API 参数命名存在不一致，需特别注意：
- **命名风格混用**：知识库管理接口普遍使用 `snake_case`（如 `index_id`, `doc_ids`），而部分接口（如 `/list/index/file/details`、`/chunklist`）使用 `camelCase`（如 `indexId`, `pageNumber`, `pageNum`）。例如，`删除文档` 接口要求 `index_id`，传 `IndexId` 或 `indexId` 均会返回 `Index.InvalidParameter` 错误 [删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)；`查询文件详情列表` 则明确要求 `indexId`、`pageNumber` [查询文件详情列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-file-details.md)。
- **必填与默认行为**：`创建知识库并导入` 接口的 `docIds` 为必填，但错误提示中参数名显示为 `file_ids`，易引发混淆 [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)；`提交导入任务` 接口若不传 `sourceType`，将默认导入整个数据中心，存在高风险 [提交导入任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-submit-sync-job.md)。
- **特殊格式要求**：`获取知识库监控数据` 接口的时间戳必须为**秒级** Unix 时间戳（非毫秒），且建议以字符串格式传入（如 `"1780900000"`） [获取知识库监控数据](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)；`申请上传租约` 接口的 `sizeBytes` 必须传字符串（如 `"1048576"`），传数字将失败 [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)。

## 使用方式

1. **认证与端点**：所有请求需携带 `Authorization: Bearer <API-Key>` Header，并使用业务空间 ID 拼接 Base URL：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com`。API Key 在 [控制台 API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 获取 [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)。
2. **知识库生命周期**：
   - 创建：调用 `/api/v1/indices/rag/index/create_v2` 一步完成知识库创建与初始文档导入 [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。
   - 管理：通过 `/api/v1/indices/rag/index/update` 修改元信息，`/api/v1/indices/rag/index/delete` 永久删除（不可逆） [更新知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)、[删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)。
   - 导入：对已有知识库追加文档，需先调用 `/api/v1/indices/rag/index/job/create` 提交任务，再用 `/api/v1/indices/rag/index_job/status` 查询进度 [提交导入任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-submit-sync-job.md)、[查询任务状态](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-get-sync-job-status.md)。
3. **运行时调用**：
   - **检索**：调用 `/api/v1/indices/knowledge/search`，需提供在控制台创建并发布的 `agent_id` 及检索意图（`query` 或 `images`） [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)。
   - **问答**：调用 `/api/v2/apps/knowledge/chat`，同样需 `agent_id`，且 `stream` 必须为 `true`，`messages` 需包含完整对话历史 [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)。
4. **Agent 管理**：运行时服务依赖 RAG Agent。需先用管理 API（如 `/api/v1/indices/rag/app/create`）创建 Agent，配置 `kb_search_configs` 等策略，再通过 `/api/v1/indices/rag/app/deploy` 发布，获取 `agent_id` 后方可调用运行时接口 [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)。

## 限制和注意事项

- **限流规则**：接口 QPS 限制严格，例如 `检索` 接口上限为 2000 QPS，而 `获取监控数据` 仅为 1 QPS [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)。运行时服务（`knowledge/search` 和 `knowledge/chat`）默认用户维度 25 QPS [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)。超限返回 HTTP `429`，需按 `Retry-After` 头或指数退避重试。
- **不可逆操作**：`删除知识库`、`删除文档`、`删除切片`、`删除类目`、`删除文件` 等操作均为永久性删除，无回收站机制，调用前务必确认 [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)、[删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)、[删除切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-delete-chunk.md)、[删除类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-category.md)、[删除文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-file.md)。
- **状态码与错误处理**：所有接口返回统一 JSON 结构，含 `error.code`（如 `INVALID_PARAMETER`, `KB_NOT_FOUND`）和 `request_id`。HTTP `504 RETRIEVAL_TIMEOUT` 错误建议降低 `top_k` 或切换更小的重排模型 [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)。
- **数据一致性**：`新增切片` 接口仅支持 `document`、`table`、`image` 类型知识库，不支持 `multimedia`；`查询切片列表` 中 `docId` 过滤在 `document` 和 `multimedia` 库中为必填，在 `table` 和 `image` 库中无需传入 [新增切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-add-chunk.md)、[查询切片列表](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-list-chunks.md)。

## 来源文档

- [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)
- [概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)
- [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)
- [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)
- [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md)
- [查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)
- [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)
- [更新知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)
- [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)
- [获取知识库监控数据](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)
- [查询文档列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-documents.md)
- [文档管理](../../raw/application-api-reference/rag-api/rag-api-documents.md)
- [查询文件详情列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-file-details.md)
- [删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)
- [新增切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-add-chunk.md)
- [切片管理](../../raw/application-api-reference/rag-api/rag-api-chunks.md)
- [查询切片列表](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-list-chunks.md)
- [更新切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-update-chunk.md)
- [删除切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-delete-chunk.md)
- [查询任务状态](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-get-sync-job-status.md)
- [同步任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs.md)
- [提交导入任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-submit-sync-job.md)
- [新增类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-category.md)
- [数据导入](../../raw/application-api-reference/rag-api/rag-api-data-import.md)
- [删除类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-category.md)
- [查询文件列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-file.md)
- [删除文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-file.md)
- [批量更新文件标签](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-batch-update-tag.md)
- [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)
- [注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)
- [从 OSS 批量导入](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-oss-import.md)
- [新增连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-connector.md)
- [查询连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-get-connector.md)
- [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)
- [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)
- [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)
- [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md)
- [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)
- [创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)
- [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)
- [发布 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-deploy.md)
- [删除 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-delete.md)
- [查询 Agent 列表](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-list.md)
- [查询 Agent 详情](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-get.md)
- [复制 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-copy.md)
- [查询类目列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-category.md)
- [查询文件详情](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-describe-file.md)


