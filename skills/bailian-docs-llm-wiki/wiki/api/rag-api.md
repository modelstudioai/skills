# rag api

RAG API 是阿里云百炼平台提供的知识库管理与检索服务接口，支持知识库全生命周期管理、文档导入、切片操作、跨库语义检索及基于知识的智能问答。所有接口通过 DashScope 网关统一提供 HTTPS 服务，采用 API Key 鉴权，并按业务空间（`{workspace_id}`）隔离资源。开发者可通过该 API 构建端到端的 RAG 应用，无需依赖控制台人工操作。

## 支持的模型/功能

RAG API 提供三类核心能力：**知识库管理**（创建、更新、删除、监控）、**数据导入与同步**（类目/[文件管理](../concepts/file-management.md)、OSS 批量导入、连接器配置）以及**知识检索与问答**（联合语义检索、SSE 流式问答）。  
- **知识库类型**支持 `document`（文档搜索）、`table`（数据查询）、`image`（图片问答）、`multimedia`（音视频搜索），对应不同 `knowledgeType` 和 `knowledgeScene` 组合，如 `visual_perception_qa` 需配合 `multimodalEmbeddingModelName` 指定多模态向量模型 [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。  
- **检索与问答**依赖预发布的 Agent 实例：知识检索调用 `/api/v1/indices/knowledge/search`，知识问答调用 `/api/v2/apps/knowledge/chat`，二者均需传入 `agent_id` 并在控制台完成发布 [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)。  
- **Agent 管理**提供完整生命周期 API（创建、更新、发布、复制、删除），支持 `chat` 和 `search` 两类场景，其 `agent_config` 定义了模型、策略、混排、路由等关键行为 [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)。

> **注意**：文档 6 明确要求 `knowledgeScene` 为 `lite_document_qa` 时 `sinkType` 必须为 `BUILT_IN`，但文档 7 的响应示例中 `sinkType` 字段未出现且无默认值说明；实际使用应以创建接口的强制校验为准。

## 关键参数

- **认证参数**：所有请求必须携带 `Authorization: Bearer <API-Key>` 头，API Key 在控制台 [API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 获取 [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)。  
- **路径参数**：Base URL 为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com`，其中 `{workspace_id}` 是业务空间 ID，在控制台 [业务空间管理](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 查看 [概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)。  
- **请求体命名不一致**：知识库管理接口普遍使用 `snake_case`（如 `index_id`, `doc_ids`），而切片管理接口（如 `/list/index/file/details`）和部分 Agent 接口使用 `camelCase`（如 `indexId`, `pageNumber`），需严格按各接口文档约定传参 [删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)。  
- **Agent 相关参数**：运行时接口（`/knowledge/search`, `/knowledge/chat`）仅需 `agent_id` 和 `query`/`images`；复杂策略（如多库权重、混排模型）必须在 Agent 的 `agent_config` 中预先配置并发布，不在运行时请求中暴露 [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)。

## 使用方式

1. **初始化**：获取 `workspace_id` 和 API Key，构造 Base URL。  
2. **构建知识库**：调用 `/api/v1/indices/rag/index/create_v2` 创建知识库并导入初始文档；或先创建后通过 `/api/v1/indices/rag/index/job/create` 追加导入 [提交导入任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-submit-sync-job.md)。  
3. **管理数据源**：使用 `/api/v1/connector/dash/` 前缀接口管理类目、文件、连接器；上传文件需三步：申请租约 → OSS PUT 上传 → 注册文件 [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)。  
4. **配置 Agent**：调用 `/api/v1/indices/rag/app/` 系列接口创建、更新、发布 Agent，获取 `agent_id`。  
5. **运行时调用**：  
   - 检索：`POST /api/v1/indices/knowledge/search`，传 `agent_id` 和 `query`；  
   - 问答：`POST /api/v2/apps/knowledge/chat`，`stream` 必须为 `true`，`messages` 包含完整对话历史 [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)。  

## 限制和注意事项

- **限流规则**：知识库管理接口按 QPS 限流（如 `/rag/index/retrieve` 为 2000 QPS），知识检索与问答接口按每 10 秒请求数限流（默认 10 次） [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)。超限返回 `429`，应遵循 `Retry-After` 头或指数退避重试。  
- **不可逆操作**：删除知识库（`/rag/index/delete`）、删除文档（`/rag/index/delete_file`）、删除类目（`/deleteCategory`）均为软删除但数据不可恢复，调用前务必确认 [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)。  
- **参数兼容性**：`sizeBytes` 在上传租约接口中必须传字符串（如 `"1048576"`），传数字将失败；`startTimestamp`/`endTimestamp` 在监控接口中为秒级时间戳，支持字符串或整数格式 [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)。  
- **错误处理**：所有错误响应结构统一，含 `error.code`、`error.message` 和 `request_id`；`4xx` 错误通常不建议重试，`5xx` 和 `429` 应按重试策略处理 [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)。

## 来源文档

- [概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)
- [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)
- [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)
- [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)
- [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md)
- [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)
- [查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)
- [更新知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)
- [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)
- [查询文档列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-documents.md)
- [文档管理](../../raw/application-api-reference/rag-api/rag-api-documents.md)
- [获取知识库监控数据](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)
- [删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)
- [查询文件详情列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-file-details.md)
- [切片管理](../../raw/application-api-reference/rag-api/rag-api-chunks.md)
- [更新切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-update-chunk.md)
- [新增切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-add-chunk.md)
- [删除切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-delete-chunk.md)
- [查询切片列表](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-list-chunks.md)
- [同步任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs.md)
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
- [提交导入任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-submit-sync-job.md)
- [查询任务状态](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-get-sync-job-status.md)
- [查询 Agent 列表](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-list.md)
- [复制 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-copy.md)
- [删除 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-delete.md)
- [查询 Agent 详情](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-get.md)


