# rag api

RAG API 是百炼平台提供的知识库管理与检索服务接口，支持知识库的全生命周期管理（创建、更新、删除、监控）、文档与切片的精细化操作、数据导入、以及基于知识库的语义检索与智能问答。所有接口均通过 HTTPS 提供，采用统一的 API Key 鉴权机制和 JSON 数据格式。

## 支持的模型/功能

RAG API 支持多种知识处理能力，覆盖结构化与非结构化数据场景：

- **知识库类型**：`document`（文档搜索）、`table`（数据查询）、`image`（图片问答）、`multimedia`（音视频搜索），由 `knowledgeType` 字段指定；其底层结构由 `structureType`（`unstructured` 或 `structured`）决定。
- **嵌入模型**：支持 `text-embedding-v3`、`text-embedding-v4`、`qwen3.7-text-embedding` 等文本嵌入模型；多模态场景需指定 `multimodalEmbeddingModelName`（如 `qwen3-vl-embedding`）[原文标题](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。
- **重排序模型**：默认使用 `qwen3-rerank`，可通过 `rerankModelName` 自定义，并支持 `rerankMinScore`（最低分数阈值）和 `rerankTopN`（返回数量）等参数控制结果质量 [原文标题](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)。
- **检索与问答**：提供两类运行时服务：
  - **知识检索**（`/api/v1/indices/knowledge/search`）：跨知识库联合语义检索，支持文本+图片多模态输入，策略由预发布的 Agent 实例（`agent_id`）承载 [原文标题](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)。
  - **知识问答**（`/api/v2/apps/knowledge/chat`）：SSE 流式问答，包含规划、工具调用、生成三阶段，需传入完整对话历史并启用 `stream=true`。

## 关键参数

RAG API 的核心参数设计强调一致性与场景适配，但存在命名不一致问题，需特别注意：

- **ID 字段命名不统一**：
  - 知识库 ID 在多数接口中为 `indexId`（如 `/list/index/file/details`、`/chunklist`），但在 `delete_index` 接口中为 `index_id`，在 `update_index` 中为 `id` [原文标题](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)。
  - 文件 ID 在 `delete_document` 中为 `doc_ids`（snake_case），而在 `list_file_details` 中为 `doc_id`（snake_case），但在 `add_chunk` 中为 `dataId`（camelCase）。
- **必填字段校验差异**：
  - `create_index_v2` 要求 `docIds`（数组）作为文件导入参数，但错误提示中却显示 `file_ids`，易引发混淆 [原文标题](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。
- **时间戳格式**：
  - `get_index_monitor` 接口明确要求 `startTimestamp` 和 `endTimestamp` 为**秒级** Unix 时间戳（字符串或整数均可），而其他多数接口（如 `list_documents`）使用毫秒级时间戳，开发者需严格区分 [原文标题](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)。
- **限流维度**：
  - 知识库管理接口（如 `create_v2`、`list`）按 QPS 限流；
  - 检索与问答接口（`/knowledge/search`、`/knowledge/chat`）按用户维度限流（每 10 秒最多 10 次）；
  - `get_index_monitor` 接口 QPS 上限仅为 1，属高成本监控接口，应谨慎调用。

> **注意**：`delete_document` 接口的请求体参数名是 `index_id` 和 `doc_ids`（snake_case），若误传 `IndexId` 或 `indexId`（camelCase），将返回 `Index.InvalidParameter` 错误，而非清晰的参数名提示。请严格遵循文档示例中的参数命名。

## 使用方式

### 1. 基础配置
- **Base URL**：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com`，其中 `{workspace_id}`（如 `llm-xxxxxxxxxxxx`）需从[业务空间管理](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)页面获取。
- **认证**：所有请求必须携带 `Authorization: Bearer <API-Key>` Header，API Key 通过[控制台 API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key)获取 [原文标题](../../raw/application-api-reference/rag-api/rag-api-authentication.md)。
- **Content-Type**：POST 请求需设置 `Content-Type: application/json`。

### 2. 典型工作流
1. **准备数据**：通过数据导入接口（`/api/v1/connector/dash/...`）上传文件、创建类目、管理数据集。
2. **构建知识库**：调用 `create_index_v2` 一步创建知识库并导入文件；或先 `create_index`，再 `submit_sync_job` 追加导入。
3. **管理内容**：使用文档管理（`list_documents`, `delete_document`）和切片管理（`list_chunks`, `update_chunk`, `delete_chunk`）接口进行细粒度操作。
4. **发布服务**：通过 Agent 管理 API（`create`, `update`, `deploy`）创建并发布 `search` 或 `chat` 场景的 Agent，获取 `agent_id`。
5. **运行时调用**：使用 `agent_id` 调用 `/knowledge/search` 或 `/knowledge/chat` 执行检索或问答。

### 3. 错误处理
- 所有错误响应均为标准 JSON 格式，含 `error.code`、`error.message` 和 `request_id`。
- 遇到 `429 Too Many Requests` 时，应遵循重试策略：优先读取 `Retry-After` Header，否则采用 1s/2s/4s 指数退避 [原文标题](../../raw/application-api-reference/rag-api/rag-api-errors.md)。
- `5xx` 错误建议重试最多 3 次；`504 Gateway Timeout` 可直接重试 2 次。

## 限制和注意事项

- **硬性限制**：
  - 单次 `delete_chunk` 最多删除 10 个切片；单次 `batchUpdateFileTag` 最多处理 20 个文件。
  - `list_documents` 和 `list_chunks` 的 `page_size` 上限分别为 100 和 100；`get_index_monitor` 的 `endTimestamp` 不得超过 `startTimestamp + 30 天`。
  - `add_chunk` 对切片内容长度要求为 **10–6000 字符**，超出将报错。

- **关键注意事项**：
  - **不可逆操作**：`delete_index`、`delete_document`、`delete_chunk`、`delete_category`、`delete_file` 均为永久删除，无回收站机制，调用前务必二次确认。
  - **权限隔离**：RAM 子账号需被授予 `AliyunBailianDataFullAccess` 权限并加入目标业务空间，否则无法调用任何 RAG 接口。
  - **Agent 生命周期**：`agent_config` 仅允许修改 `beta` 草稿版本；已发布版本（如 `1`, `2`）只能修改 `agent_version_desc`，如需更新配置，必须先 `update` 草稿再 `deploy` 发布新版本 [原文标题](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)。
  - **数据一致性**：`delete_file` 仅删除数据中心的原始文件，**不会**自动移除已导入知识库的文档及切片；如需同步清理，必须额外调用 `delete_document`。

- **性能与安全**：
  - API Key 应存储于环境变量（如 `BAILIAN_API_KEY`），严禁硬编码或提交至代码仓库。
  - 生产环境建议为每个应用分配独立 API Key，便于追踪与轮转。
  - 检索超时（`RETRIEVAL_TIMEOUT`）常见于 `top_k` 过大或重排模型过重，建议降低 `top_k` 或选用更轻量的重排模型。

## 来源文档

- [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)
- [RAG API 错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)
- [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)
- [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md)
- [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)
- [更新知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)
- [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)
- [获取知识库监控数据](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)
- [文档管理](../../raw/application-api-reference/rag-api/rag-api-documents.md)
- [概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)
- [查询文件详情列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-file-details.md)
- [删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)
- [切片管理](../../raw/application-api-reference/rag-api/rag-api-chunks.md)
- [新增切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-add-chunk.md)
- [查询切片列表](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-list-chunks.md)
- [更新切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-update-chunk.md)
- [删除切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-delete-chunk.md)
- [同步任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs.md)
- [查询文档列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-documents.md)
- [提交导入任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-submit-sync-job.md)
- [查询任务状态](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-get-sync-job-status.md)
- [数据导入](../../raw/application-api-reference/rag-api/rag-api-data-import.md)
- [查询类目列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-category.md)
- [删除类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-category.md)
- [新增类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-category.md)
- [查询文件详情](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-describe-file.md)
- [批量更新文件标签](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-batch-update-tag.md)
- [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)
- [注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)
- [从 OSS 批量导入](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-oss-import.md)
- [新增数据集](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-connector.md)
- [查询数据集](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-get-connector.md)
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
- [查询文件列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-file.md)
- [删除文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-file.md)
- [查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)


