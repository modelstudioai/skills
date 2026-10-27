# rag api

RAG API 是阿里云百炼平台提供的知识库全生命周期管理与检索问答服务接口，覆盖知识库创建、文档导入、切片管理、联合检索及智能问答等核心能力。所有接口通过 DashScope 网关统一提供，基于业务空间（workspace_id）隔离资源，并采用标准 API Key 鉴权。开发者可通过 RESTful 方式集成，无需依赖控制台操作。

## 支持的模型/功能

RAG API 支持多模态与文本混合检索、结构化/非结构化知识库、多种[向量嵌入](../concepts/embedding.md)与重排模型，并提供完整的 Agent 管理能力：

- **嵌入模型**：支持 `text-embedding-v4` 等文本嵌入模型；图片/图文场景需显式指定 `multimodalEmbeddingModelName`（如 `qwen3-vl-embedding`），详见[创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。
- **重排模型**：默认使用 `qwen3-rerank`，可在知识库配置中自定义 `rerankModelName` 与 `rerankMinScore`，响应中亦可查得当前配置（见[查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)示例）。
- **知识库类型**：支持 `document`（文档搜索）、`table`（数据查询）、`image`（图片问答）、`multimedia`（音视频搜索）四类，对应不同 `knowledgeType` 与 `knowledgeScene` 组合，且需匹配 `structureType`（`unstructured` 或 `structured`）。
- **Agent 能力**：通过 Agent 管理 API（`/api/v1/indices/rag/app/`）创建、更新、发布 `chat` 或 `search` 场景的 RAG 实体，其 `agent_config` 控制模型（如 `qwen3.7-plus`）、策略（`turbo`/`agentic`）、安全开关（防泄漏、引用标注）及知识库路由等高级行为，详见[Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)。

> **注意**：文档 5 中 `knowledgeScene` 列出的 `visual_document_qa` 场景在控制台已下线，仅 API 可用；而文档 41 的 `agent_config` 结构说明中未明确 `search` 场景下 `kb_router_model` 的白名单要求，实际调用需确保该模型已在平台启用，否则发布失败。

## 关键参数

| 参数名 | 所属接口 | 说明 | 示例值 |
|--------|----------|------|--------|
| `workspace_id` | 全局 | 业务空间 ID，构成 Base URL 主机名，格式如 `llm-xxxxxxxxxxxx` | `llm-abcd1234efgh` |
| `Authorization: Bearer <API-Key>` | 全局 | 必填请求头，API Key 从[控制台获取](../../raw/application-api-reference/rag-api/rag-api-authentication.md) | `Bearer sk-xxx` |
| `pipelineId` / `indexId` / `index_id` | 多接口 | 知识库 ID，命名不一致：`/chunk/create` 用 `pipelineId`，`/list/file/details` 用 `indexId`，`/delete_file` 用 `index_id`（snake_case） | `your-kb-id` |
| `docIds` | `/create_v2`, `/job/create` | 文件 ID 列表，参数名固定为 `docIds`（非 `file_ids` 或 `fileIds`），传错将被忽略并报错 | `["file_xxx"]` |
| `agent_id` | `/knowledge/search`, `/knowledge/chat` | Agent 实例 ID，由 Agent 管理 API 创建并发布后获得，是运行时调用的必需凭证 | `aid-xxxxxxxxxxxxxxxx` |
| `search_filters` | `/knowledge/search` | 知识库级过滤条件，支持 `tags` 和自定义 `meta` 字段，以 JSON 数组形式传入，总大小 ≤ 80KB | `[{"tags": ["v2"]}]` |

## 使用方式

1. **认证与端点**：  
   设置 `Authorization` 请求头，并拼接 Base URL：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com`。所有接口均使用 HTTPS，请求/响应为 UTF-8 编码 JSON。

2. **知识库与数据流**：  
   - **创建与导入**：调用 `/api/v1/indices/rag/index/create_v2` 一步完成知识库创建与文件导入（需 `docIds`）；或先创建空库，再用 `/api/v1/indices/rag/index/job/create` 追加导入。  
   - **文档管理**：通过 `/api/v1/indices/rag/index/files`（GET）或 `/api/v1/indices/rag/list/index/file/details`（POST）查询文档；用 `/api/v1/indices/rag/index/delete_file` 删除文档（注意 `index_id` 命名）。  
   - **切片管理**：使用 `/api/v1/indices/rag/index/chunk/create` 新增切片（支持 `content`/`title`/`image_urls`）；`/api/v1/indices/rag/index/chunklist` 查询切片（注意 `docId` 过滤逻辑因知识库类型而异）。

3. **检索与问答**：  
   - **知识检索**：调用 `/api/v1/indices/knowledge/search`，传 `agent_id` 与 `query`（或 `images`），可选 `kb_search_configs` 指定各知识库过滤条件。  
   - **知识问答**：调用 `/api/v2/apps/knowledge/chat`，必须设置 `stream: true`，`input.messages` 传完整对话历史，`parameters.agent_options.agent_id` 指定已发布 Agent。

4. **Agent 生命周期**：  
   先用 `/app/create` 创建 Agent（`draft` 状态），通过 `/app/update` 修改 `beta` 配置，再用 `/app/deploy` 发布为正式版本（`agent_version` 自增），最后在运行时 API 中使用 `agent_id`。

## 限制和注意事项

- **限流规则**：知识库管理接口中，`/rag/index/retrieve`（检索）QPS 上限为 2000，而 `/rag/index/monitor`（监控）仅为 1 QPS；数据导入接口 `/describeFile` 为 10 QPS。超出返回 `429`，建议按 `Retry-After` 头或指数退避（1s/2s/4s）重试 [原文标题](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)。
- **参数命名不一致**：多个接口存在命名差异——知识库 ID 在 `/chunk/create` 中为 `pipelineId`，在 `/update` 中为 `id`，在 `/delete_file` 中为 `index_id`；文件 ID 列表统一为 `docIds`，但错误提示中可能显示 `file_ids`。务必以各接口文档定义为准。
- **不可逆操作**：删除知识库（`/delete`）、文档（`/delete_file`）、切片（`/chunk/delete`）或类目（`/deleteCategory`）均为软/硬删除，数据无法恢复，调用前须确认无业务依赖。
- **文件上传三步法**：导入本地文件需严格遵循流程：① `/applyFileUploadLease` 获取租约（`sizeBytes` 必须为字符串）→ ② PUT 到 OSS 预签名 URL → ③ `/addFile` 注册（注意 `category` 字段名，非 `categoryId`）[原文标题](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)。
- **Agent 版本约束**：`agent_config` 仅允许修改 `beta` 草稿版本；已发布版本只能通过 `/app/update` 修改 `agent_version_desc`，如需更新配置，必须先改草稿再 `/app/deploy` [原文标题](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)。

## 来源文档

- [概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)
- [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)
- [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)
- [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)
- [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)
- [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md)
- [查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)
- [更新知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)
- [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)
- [获取知识库监控数据](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)
- [文档管理](../../raw/application-api-reference/rag-api/rag-api-documents.md)
- [查询文件详情列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-file-details.md)
- [删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)
- [查询文档列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-documents.md)
- [新增切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-add-chunk.md)
- [切片管理](../../raw/application-api-reference/rag-api/rag-api-chunks.md)
- [查询切片列表](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-list-chunks.md)
- [更新切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-update-chunk.md)
- [删除切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-delete-chunk.md)
- [提交导入任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-submit-sync-job.md)
- [查询任务状态](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-get-sync-job-status.md)
- [数据导入](../../raw/application-api-reference/rag-api/rag-api-data-import.md)
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
- [同步任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs.md)
- [查询类目列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-category.md)
- [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)
- [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)
- [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md)
- [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)
- [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)
- [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)
- [创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)
- [删除 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-delete.md)
- [发布 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-deploy.md)
- [查询 Agent 列表](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-list.md)
- [查询 Agent 详情](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-get.md)
- [复制 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-copy.md)
- [查询连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-get-connector.md)


