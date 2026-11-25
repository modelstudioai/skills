# rag api

RAG API 是百炼平台提供的知识库管理与检索服务接口，统一通过 Knowledge API（原 RAG API）提供知识库 CRUD、文档/切片管理、数据导入、知识检索和知识问答等能力。所有接口均基于 HTTPS 协议，使用 API Key 鉴权，并按业务空间（workspace_id）隔离资源。开发者需先创建业务空间、获取 API Key，并根据具体场景选择对应接口组调用。

## 支持的模型/功能

RAG API 支持多模态与文本混合检索、结构化/非结构化知识库、Wiki 知识图谱生成、以及基于 Agent 的知识问答服务。核心能力包括：

- **知识库类型**：支持 `document`（文档搜索）、`table`（数据查询）、`image`（图片问答）、`multimedia`（音视频搜索）四类知识场景，对应不同 `knowledgeType` 和 `knowledgeScene` 组合 [原文标题](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)；
- **嵌入与重排模型**：可指定 `embeddingModelName`（如 `text-embedding-v4`、`qwen3.7-text-embedding`）和 `rerankModelName`（如 `qwen3-rerank`），知识库创建或更新时配置 [原文标题](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)；
- **Wiki 功能**：旗舰版知识库支持 Wiki 开启与配置，需通过 `wikiEnabled`、`wikiConfig.extraction.synthesisModelId` 等字段控制，且仅限 `basic_document_qa` 场景 [原文标题](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)；
- **Agent 服务**：知识检索（`search`）与知识问答（`chat`）均以 Agent 为运行主体，其策略（如混排、路由、防泄漏）在 `agent_config` 中定义，通过管理 API 创建、更新、发布后获得 `agent_id` 调用运行时接口 [原文标题](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)。

> **注意**：文档 6 中提到 `visual_document_qa` 场景“控制台已不再提供该入口”，但未说明是否仍可通过 API 调用；实际使用应以控制台可用场景为准，避免依赖已下线能力。

## 关键参数

| 参数 | 所属接口 | 说明 | 注意事项 |
|--------|-----------|------|----------|
| `workspace_id` | 全局 | 业务空间 ID，构成 Base URL：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com` | 在控制台[业务空间管理](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)页面查看或创建 |
| `Authorization: Bearer <API-Key>` | 全局 | API 鉴权头 | 必须使用控制台 [API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 获取的有效 Key [原文标题](../../raw/application-api-reference/rag-api/rag-api-authentication.md) |
| `index_id` / `pipelineId` | 知识库/文档/切片相关接口 | 知识库唯一标识 | 多数接口（如 `/delete_file`）使用 snake_case `index_id`，少数（如 `/chunk/create`）使用 camelCase `pipelineId`，传错将返回 `Index.InvalidParameter` [原文标题](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md) |
| `docIds` | `/create_v2`, `/job/create` | 文件 ID 列表 | 参数名严格为 `docIds`（非 `file_ids` 或 `fileIds`），错误命名将被忽略并报错 [原文标题](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md) |
| `agent_id` | `/knowledge/search`, `/knowledge/chat` | 已发布 Agent 实例 ID | 必须先通过 Agent 管理 API 创建并 `deploy`，否则返回 “Agent 未发布” 错误 [原文标题](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md) |

## 使用方式

1. **认证与初始化**：获取 API Key 并设置 `Authorization` Header，构造 Base URL；
2. **知识库生命周期**：
   - 创建：调用 `/api/v1/indices/rag/index/create_v2` 一步完成建库与导入；
   - 管理：通过 `/list`、`/update`、`/delete` 接口操作知识库；
   - 监控：使用 `/monitor` 查询存储用量与 QPS；
3. **文档与切片管理**：
   - 文档：`/files`（列表）、`/list/index/file/details`（详情）、`/delete_file`（删除）；
   - 切片：`/chunklist`（列表）、`/chunk/create`（新增）、`/chunk/update`（更新）、`/chunk/delete`（删除）；
4. **数据导入**：使用 `/connector/dash/` 前缀接口管理类目、文件、数据集，完整流程为：`applyFileUploadLease` → OSS PUT → `addFile`；
5. **运行时服务**：
   - 检索：调用 `/api/v1/indices/knowledge/search`，传 `agent_id` 与 `query`/`images`；
   - 问答：调用 `/api/v2/apps/knowledge/chat`，`stream=true`，传 `input.messages` 与 `parameters.agent_options`；
6. **Agent 管理**：通过 `/api/v1/indices/rag/app/` 前缀接口全生命周期管理 Agent（`create`→`update`→`deploy`→`list`→`get`→`delete`）。

## 限制和注意事项

- **限流规则**：知识库管理接口按 QPS 限流（如 `/retrieve` 为 2000 QPS），知识检索与问答接口按每 10 秒请求数限流（默认 10 次）。超限返回 HTTP `429` 及 `RATE_LIMITED` 或 `THROTTLING.pipelineQPSLimit` 错误码 [原文标题](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)；
- **参数命名不一致**：`index_id`（snake_case）与 `indexId`/`pipelineId`（camelCase）混用，`docIds` 与 `file_ids` 易混淆，务必严格按各接口文档要求传参，否则返回 `InvalidParameter`；
- **不可逆操作**：`/delete` 类接口（知识库、文档、切片、类目、文件）均为永久删除，无回收站，调用前必须确认；
- **时间戳格式**：`/monitor` 接口的 `startTimestamp`/`endTimestamp` 为**秒级 Unix 时间戳**（非毫秒），建议传字符串格式（如 `"1780900000"`）；
- **Agent 版本约束**：`agent_config` 仅允许修改 `beta` 草稿版本；已发布版本只能修改 `agent_version_desc`，如需更新配置，必须先 `update` 草稿再 `deploy` 新版本 [原文标题](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)；
- **Wiki 依赖条件**：开启 Wiki 要求知识库为旗舰版（`enterprise`）且场景为 `basic_document_qa`，降配为标准版时会强制关闭 Wiki，且 `synthesisModelId` 必须在平台白名单内。

## 来源文档

- [概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)
- [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)
- [Knowledge（原RAG） API 错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)
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
- [切片管理](../../raw/application-api-reference/rag-api/rag-api-chunks.md)
- [新增切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-add-chunk.md)
- [查询切片列表](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-list-chunks.md)
- [更新切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-update-chunk.md)
- [删除切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-delete-chunk.md)
- [提交导入任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-submit-sync-job.md)
- [同步任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs.md)
- [查询任务状态](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-get-sync-job-status.md)
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
- [新增数据集](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-connector.md)
- [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)
- [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)
- [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md)
- [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)
- [创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)
- [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)
- [发布 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-deploy.md)
- [删除 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-delete.md)
- [查询 Agent 列表](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-list.md)
- [复制 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-copy.md)
- [查询 Agent 详情](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-get.md)
- [查询数据集](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-get-connector.md)
- [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)


