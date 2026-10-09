# rag api

RAG API 是百炼平台提供的面向开发者的一套知识库管理与检索服务接口，覆盖知识库生命周期管理、文档与切片操作、数据导入、Agent 管理及运行时检索/问答等核心能力。所有接口均基于 HTTPS 协议，统一使用 `Authorization: Bearer <API-Key>` 鉴权，并通过业务空间 ID（`{workspace_id}`）路由到对应实例。开发者可据此构建端到端的 RAG 应用。

## 支持的模型/功能

RAG API 本身不直接暴露大语言模型调用，但深度集成以下模型能力：
- **嵌入模型（Embedding）**：支持指定 `embeddingModelName`（如 `text-embedding-v4`）和 `multimodalEmbeddingModelName`（如 `qwen3-vl-embedding`），用于知识库向量化；具体可用模型列表需参考控制台或 [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md) 文档。
- **重排序模型（Rerank）**：知识库配置中可设置 `rerankModelName`（如 `qwen3-rerank`），影响检索结果精排质量。
- **问答与检索模型**：知识问答（`/api/v2/apps/knowledge/chat`）和知识检索（`/api/v1/indices/knowledge/search`）服务由 Agent 封装，其底层模型（如 `qwen3.7-plus`）在 [创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md) 时通过 `agent_model` 字段指定。
- **解析模型**：文件上传阶段支持多种解析器（`parser`），如 `DOCMIND_DIGITAL`、`DASH_QWEN_VL_PARSER`，决定非结构化内容的提取精度。

> **注意**：文档中提及的 `visual_document_qa` 场景虽在 [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md) 中被列为可选值，但明确注明“控制台已不再提供该入口”，建议避免在新项目中使用。

## 关键参数

- **认证参数**：所有请求必须携带 `Authorization: Bearer <API-Key>` Header，API Key 通过 [认证方式](../../raw/application-api-reference/rag-api/rag-api-authentication.md) 获取。
- **业务空间标识**：Base URL 中的 `{workspace_id}`（如 `llm-xxxxxxxxxxxx`）是必需路径组成部分，不可省略。
- **知识库 ID**：多数操作（如更新、删除、查询文档）需传 `index_id` 或 `indexId`，但命名不一致——`delete_file` 接口强制要求 `snake_case`（`index_id`），而 `list_file_details` 和 `update_index` 要求 `camelCase`（`indexId` 或 `id`），详见各接口文档。
- **Agent 标识**：运行时接口（`knowledge/search`、`knowledge/chat`）依赖 `agent_id`，该 ID 由 Agent 管理 API（如 [发布 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-deploy.md)）生成并返回，不可自行构造。
- **文件与切片标识**：`docIds`（非 `fileIds`）、`chunkId`（取自 `node.metadata._id`）、`leaseId` 等 ID 字段均为字符串类型，需严格按文档示例传递。

## 使用方式

1. **准备凭证**：在百炼控制台获取 API Key，并确认 RAM 子账号已授予 `AliyunBailianDataFullAccess` 权限。
2. **选择路径前缀**：根据操作类型选用 Base URL 下的三组路径：
   - 知识库管理：`/api/v1/indices/`
   - 数据导入：`/api/v1/connector/dash/`
   - 知识问答/检索：`/api/v2/apps/knowledge/`（问答）或 `/api/v1/indices/knowledge/`（检索）
3. **执行典型流程**：
   - **新建知识库**：调用 `/api/v1/indices/rag/index/create_v2`，传入 `name`、`structureType`、`docIds` 等。
   - **追加文档**：先通过 `/api/v1/connector/dash/applyFileUploadLease` 申请租约并上传 OSS，再用 `/api/v1/connector/dash/addFile` 注册，最后调用 `/api/v1/indices/rag/index/job/create` 导入。
   - **管理 Agent**：用 `/api/v1/indices/rag/app/create` 创建 Agent，`/api/v1/indices/rag/app/update` 编辑配置，`/api/v1/indices/rag/app/deploy` 发布后获得 `agent_id`。
   - **运行时调用**：用发布的 `agent_id` 向 `/api/v2/apps/knowledge/chat`（流式）或 `/api/v1/indices/knowledge/search` 发起请求。
4. **处理响应**：检查 `status_code` 和 `code` 字段（如 `Success` 或 `Index.InvalidParameter`），失败时务必提供 `request_id` 用于排查。

## 限制和注意事项

- **限流策略**：接口 QPS 差异显著，例如检索（`/rag/index/retrieve`）上限为 2000 QPS，而监控接口（`/rag/index/monitor`）仅 1 QPS；知识问答/检索运行时接口默认用户维度 25 QPS。超限返回 HTTP `429`，需按 `Retry-After` 头或指数退避重试（见 [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)）。
- **参数命名陷阱**：
  - `create_index` 接口请求体字段为 `docIds`，但错误提示中显示 `file_ids`；
  - `delete_file` 接口参数名是 `index_id` 和 `doc_ids`（snake_case），而 `list_file_details` 是 `indexId` 和 `pageNumber`（camelCase）；
  - `applyFileUploadLease` 的 `sizeBytes` 必须为字符串（如 `"1048576"`），传数字会失败。
- **不可逆操作警告**：删除知识库（`/rag/index/delete`）、删除文档（`/rag/index/delete_file`）、删除类目（`/connector/dash/deleteCategory`）均永久清除数据且无法恢复，调用前必须二次确认。
- **Agent 生命周期约束**：`agent_config` 仅允许修改 `beta` 草稿版本；已发布版本只能更新描述（`agent_version_desc`），如需改配置，必须先 `update` 草稿再 `deploy` 新版本（见 [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)）。
- **文件状态依赖**：知识库中的文档状态（如 `FINISH`）需通过 `/rag/index_job/status` 查询，直接调用检索接口可能因索引未就绪而返回空结果。

## 来源文档

- [认证方式](../../raw/application-api-reference/rag-api/rag-api-authentication.md)
- [API 概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)
- [限流策略](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)
- [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)
- [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md)
- [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)
- [查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)
- [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)
- [更新知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)
- [文档管理](../../raw/application-api-reference/rag-api/rag-api-documents.md)
- [获取知识库监控数据](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)
- [查询文件详情列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-file-details.md)
- [查询文档列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-documents.md)
- [删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)
- [切片管理](../../raw/application-api-reference/rag-api/rag-api-chunks.md)
- [新增切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-add-chunk.md)
- [查询切片列表](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-list-chunks.md)
- [更新切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-update-chunk.md)
- [删除切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-delete-chunk.md)
- [同步任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs.md)
- [查询任务状态](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-get-sync-job-status.md)
- [提交导入任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-submit-sync-job.md)
- [数据导入](../../raw/application-api-reference/rag-api/rag-api-data-import.md)
- [查询类目列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-category.md)
- [删除类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-category.md)
- [新增类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-category.md)
- [查询文件列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-file.md)
- [查询文件详情](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-describe-file.md)
- [批量更新文件标签](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-batch-update-tag.md)
- [删除文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-file.md)
- [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)
- [注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)
- [从 OSS 批量导入](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-oss-import.md)
- [查询连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-get-connector.md)
- [新增连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-connector.md)
- [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)
- [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)
- [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)
- [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md)
- [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)
- [创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)
- [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)
- [发布 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-deploy.md)
- [删除 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-delete.md)
- [查询 Agent 详情](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-get.md)
- [查询 Agent 列表](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-list.md)
- [复制 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-copy.md)


