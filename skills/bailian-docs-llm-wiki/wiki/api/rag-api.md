# rag api

RAG API 是阿里云百炼平台提供的知识库全生命周期管理与语义检索/问答服务接口，覆盖知识库创建、文档导入、切片管理、Agent 配置及运行时检索与问答能力。所有接口通过统一的 DashScope 网关提供 HTTPS 服务，采用 API Key 鉴权，并严格遵循 JSON/UTF-8 协议约定。开发者需先在控制台获取业务空间 ID 和 API Key，再按接口分组（知识库管理、数据导入、Agent 管理、运行时服务）调用对应路径。

## 支持的模型/功能

RAG API 支持[多模态](../concepts/multi-modal.md)与结构化知识处理，核心能力包括：

- **知识库类型**：`document`（文档搜索）、`table`（数据查询）、`image`（图片问答）、`multimedia`（音视频搜索），对应 `structureType: unstructured` 或 `structured`；其中 `lite_document_qa`（极速问答）强制要求 `sinkType: BUILT_IN`，`visual_perception_qa` 与 `image_qa` 必须指定 `multimodalEmbeddingModelName`（如 `qwen3-vl-embedding`）[创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。
- **嵌入与重排模型**：支持自定义 `embeddingModelName`（如 `text-embedding-v4`）和 `rerankModelName`（如 `qwen3-rerank`），其配置可在知识库创建或更新时设定，也可在 Agent 配置中全局覆盖 [查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)。
- **Agent 场景与策略**：通过 Agent 管理 API 可创建 `chat`（知识问答）或 `search`（知识检索）场景的 Agent，配置 `agent_model`（如 `qwen3.7-plus`）、`agent_policy`（`turbo`/`agentic`）、混排（`hybrid_rerank`）、知识库路由（`enable_kb_router`）等策略 [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)。
- **运行时服务**：知识检索（`/api/v1/indices/knowledge/search`）支持文本+图片[多模态](../concepts/multi-modal.md)联合检索；知识问答（`/api/v2/apps/knowledge/chat`）为 SSE 流式响应，包含规划、工具调用、生成三阶段输出。

> **注意**：文档 5 中 `knowledgeScene` 列出的 `visual_document_qa` 场景在控制台已下线，仅 API 创建时兼容，但不推荐新用；实际生产应优先使用 `basic_document_qa` 或 `lite_document_qa`。

## 关键参数

- **通用认证**：所有请求必须携带 `Authorization: Bearer <API-Key>` 头，且 Base URL 中 `{workspace_id}` 为必填业务空间 ID（格式如 `llm-xxxxxxxxxxxx`）[概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)。
- **知识库标识**：参数名存在不一致，需特别注意：
  - 知识库 ID 在 `create_v2`、`update`、`delete` 接口中分别命名为 `pipelineId`、`id`、`index_id`；
  - 文档/切片操作中，`delete_file` 使用 `index_id` + `doc_ids`（snake_case），而 `list_file_details` 使用 `indexId` + `pageNumber`（camelCase）[删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)。
- **文件与类目参数**：数据导入接口中，`applyFileUploadLease` 和 `addFile` 的类目字段名为 `category`，而 `listFile`、`addFilesFromAuthorizedOss` 等接口使用 `categoryId`，传错将导致静默忽略或报错 [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)。
- **Agent 运行时参数**：`knowledge/search` 和 `knowledge/chat` 均需 `agent_id`，且 `agent_id` 必须来自已发布（`deployed`）状态的 Agent；`knowledge/chat` 强制要求 `stream: true`，否则请求失败 [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)。

## 使用方式

1. **初始化配置**：从控制台获取 `workspace_id` 和 `API Key`，构造 Base URL `https://{workspace_id}.cn-beijing.maas.aliyuncs.com`。
2. **构建知识库**：
   - 先通过数据导入 API（如 `applyFileUploadLease` → `addFile` → `listCategory`）准备文件与类目；
   - 调用 `/api/v1/indices/rag/index/create_v2` 一步创建知识库并导入，获取 `pipelineId`；
   - 如需追加文档，调用 `/api/v1/indices/rag/index/job/create` 提交导入任务，并用 `/api/v1/indices/rag/index_job/status` 查询进度。
3. **配置与发布 Agent**：
   - 调用 `/api/v1/indices/rag/app/create` 创建 Agent，通过 `/api/v1/indices/rag/app/update` 编辑 `beta` 草稿配置；
   - 调用 `/api/v1/indices/rag/app/deploy` 发布后获得可用 `agent_id`。
4. **运行时调用**：
   - 检索：`POST /api/v1/indices/knowledge/search`，传 `agent_id` + `query`/`images` + 可选 `kb_search_configs`；
   - 问答：`POST /api/v2/apps/knowledge/chat`，传 `agent_id` + 完整 `messages` 历史（含多轮上下文），`Accept: text/event-stream`。

## 限制和注意事项

- **限流规则**：不同接口 QPS 差异显著，例如知识库检索（`/rag/index/retrieve`）上限 2000 QPS，而监控接口（`/rag/index/monitor`）仅 1 QPS；运行时 `knowledge/search` 和 `knowledge/chat` 默认用户维度 25 QPS [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)。
- **不可逆操作**：`delete_index`、`delete_file`、`delete_category`、`delete_chunk` 均为软删除但数据不可恢复，调用前必须确认无业务依赖 [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)。
- **参数格式陷阱**：
  - `get-index-monitor` 的 `startTimestamp`/`endTimestamp` 为**秒级** Unix 时间戳（非毫秒），且建议以字符串格式传递；
  - `applyFileUploadLease` 的 `sizeBytes` 必须传字符串（如 `"1048576"`），传数字将失败；
  - `listCategory` 和 `listFile` 的分页参数为 `maxResult`（单数），传 `maxResults` 会被静默忽略。
- **错误处理**：所有错误响应含 `request_id`，联系支持时必须提供；429（限流）需按 `Retry-After` 头或指数退避（1s/2s/4s）重试，5xx 错误最多重试 3 次 [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)。

## 来源文档

- [概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)
- [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)
- [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)
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
- [切片管理](../../raw/application-api-reference/rag-api/rag-api-chunks.md)
- [新增切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-add-chunk.md)
- [查询切片列表](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-list-chunks.md)
- [删除切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-delete-chunk.md)
- [同步任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs.md)
- [提交导入任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-submit-sync-job.md)
- [查询任务状态](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-get-sync-job-status.md)
- [数据导入](../../raw/application-api-reference/rag-api/rag-api-data-import.md)
- [查询类目列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-category.md)
- [新增类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-category.md)
- [删除类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-category.md)
- [更新切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-update-chunk.md)
- [查询文件列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-file.md)
- [删除文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-file.md)
- [查询文件详情](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-describe-file.md)
- [批量更新文件标签](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-batch-update-tag.md)
- [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)
- [注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)
- [新增连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-connector.md)
- [从 OSS 批量导入](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-oss-import.md)
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
- [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)


