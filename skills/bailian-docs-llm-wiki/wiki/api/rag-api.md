# rag api

RAG API 是阿里云百炼平台提供的知识库全生命周期管理与语义检索/问答服务接口集合，覆盖知识库创建、文档导入、切片管理、联合检索及智能问答等核心能力。所有接口通过统一的业务空间 Endpoint 提供服务，采用 API Key 鉴权，请求与响应均为 UTF-8 编码的 JSON 格式。开发者可通过该 API 实现知识库的自动化构建、动态更新与生产级集成。

## 支持的模型/功能

RAG API 本身不直接暴露大语言模型（LLM）调用，而是通过 **Agent 封装**提供上层能力：
- **知识检索**：通过 `/api/v1/indices/knowledge/search` 接口执行跨知识库联合语义检索，支持文本+图片多模态查询，底层混排策略（如 `qwen3-rerank`）、向量模型（如 `text-embedding-v4`）和路由模型均在 Agent 配置中定义，[知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md) 接口仅需传入 `agent_id` 和 `query`。
- **知识问答**：通过 `/api/v2/apps/knowledge/chat` 接口实现流式问答，支持规划→工具调用→生成三阶段输出，依赖已发布的 `chat` 场景 Agent，其 `agent_model`（如 `qwen3.7-plus`）和安全策略（防泄漏、拒答等）由 [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md) API 配置。
- **知识库管理**：支持 `unstructured`（文档搜索）、`structured`（数据查询）、`image`（图片问答）、`multimedia`（音视频搜索）四类知识库，每类对应不同嵌入与解析模型（如 `qwen3-vl-embedding` 用于视觉场景），详见 [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。

> **注意**：文档 6 中 `knowledgeScene` 列出的 `visual_document_qa` 场景在控制台已下线，但 API 仍兼容；实际部署应优先使用 `document` + `visual_perception_qa` 或 `image_qa` 组合，并确保 `multimodalEmbeddingModelName` 已正确指定。

## 关键参数

- **全局必需**：`Authorization: Bearer <API-Key>` 请求头，以及 Base URL 中的 `{workspace_id}`（业务空间 ID）。API Key 获取方式见 [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)。
- **知识库操作**：`id`（知识库 ID，即 `pipelineId`）为通用标识符；创建时 `sourceType` 决定参数分支（`DATA_CENTER_FILE` 要求 `docIds`，`DATA_CENTER_CATEGORY` 要求 `categoryIds`）；更新时参数名为 `id`（非 `index_id`），删除时却为 `index_id` —— 命名不一致需特别注意。
- **检索与问答**：运行时接口强依赖 `agent_id`（由 Agent 管理 API 创建并发布），且 `knowledge/chat` 必须设置 `stream: true`，否则失败；`knowledge/search` 的 `kb_search_configs` 支持按 `doc_id`、`tags` 等字段过滤，语法详见 [知识库 SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。
- **数据导入**：文件上传流程分三步：`applyFileUploadLease`（获取预签名 URL）→ OSS PUT → `addFile`（注册），其中 `sizeBytes` 必须传字符串（如 `"1048576"`），`category` 字段名在 `applyFileUploadLease` 和 `addFile` 中为 `category`，但在 `listFile` 中为 `categoryId`，存在命名冲突。

## 使用方式

1. **初始化**：从控制台获取 API Key 和业务空间 ID，拼接 Base URL：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com`。
2. **构建知识库**：
   - （可选）通过数据导入 API 管理类目与文件：`listCategory` → `addCategory` → `applyFileUploadLease` → OSS PUT → `addFile`。
   - 调用 `create_v2` 一步创建知识库并导入，或先 `createIndex` 再 `submitSyncJob` 追加。
3. **配置服务**：使用 Agent 管理 API（`/api/v1/indices/rag/app/`）创建 `search` 或 `chat` 场景 Agent，配置 `kb_search_configs`、`agent_model` 等，再 `deploy` 发布。
4. **运行时调用**：
   - 检索：`POST /api/v1/indices/knowledge/search`，传 `agent_id` 与 `query`。
   - 问答：`POST /api/v2/apps/knowledge/chat`，传 `agent_id` 与 `messages` 历史（平台不维护会话状态）。
5. **监控与维护**：通过 `get-index-monitor` 查询存储/QPS，`list-chunks` 检查切片，`delete-document` 清理过期内容。

## 限制和注意事项

- **限流规则**：知识库管理接口按 QPS 限流（如 `retrieve` 接口上限 2000 QPS），而知识检索/问答接口按“每 10 秒请求数”限流（默认 10 次），超限返回 `429` 及 `RATE_LIMITED` 错误码，需按 `Retry-After` 头或指数退避重试，详见 [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)。
- **不可逆操作**：`delete-index`、`delete-document`、`delete-chunk`、`delete-category` 均为软删除但数据不可恢复，调用前必须确认业务无依赖。
- **参数命名陷阱**：
  - 知识库删除接口要求 `index_id`，而更新接口要求 `id`，文档 9 与文档 8 明确标注了此差异；
  - 数据导入接口中 `applyFileUploadLease` 和 `addFile` 的类目字段为 `category`，但 `listFile` 为 `categoryId`，文档 31 与文档 27 分别强调了这一点。
- **错误处理**：所有错误响应结构统一，含 `error.code`（如 `INVALID_PARAMETER`）、`error.message` 和 `request_id`，排查问题必须提供后者；`504 RETRIEVAL_TIMEOUT` 错误建议降低 `top_k` 或更换更小的重排模型，而非重试。

## 来源文档

- [概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)
- [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)
- [RAG API 错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)
- [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)
- [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md)
- [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)
- [查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)
- [更新知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)
- [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)
- [获取知识库监控数据](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)
- [文档管理](../../raw/application-api-reference/rag-api/rag-api-documents.md)
- [查询文档列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-documents.md)
- [查询文件详情列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-file-details.md)
- [删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)
- [新增切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-add-chunk.md)
- [切片管理](../../raw/application-api-reference/rag-api/rag-api-chunks.md)
- [查询切片列表](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-list-chunks.md)
- [更新切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-update-chunk.md)
- [删除切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-delete-chunk.md)
- [同步任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs.md)
- [查询任务状态](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-get-sync-job-status.md)
- [提交导入任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-submit-sync-job.md)
- [数据导入](../../raw/application-api-reference/rag-api/rag-api-data-import.md)
- [查询类目列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-category.md)
- [新增类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-category.md)
- [删除类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-category.md)
- [查询文件列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-file.md)
- [查询文件详情](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-describe-file.md)
- [删除文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-file.md)
- [批量更新文件标签](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-batch-update-tag.md)
- [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)
- [注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)
- [新增数据集](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-connector.md)
- [从 OSS 批量导入](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-oss-import.md)
- [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)
- [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)
- [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md)
- [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)
- [创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)
- [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)
- [发布 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-deploy.md)
- [删除 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-delete.md)
- [查询 Agent 列表](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-list.md)
- [查询 Agent 详情](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-get.md)
- [复制 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-copy.md)
- [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)
- [查询数据集](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-get-connector.md)


