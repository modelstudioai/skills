# rag api

RAG API 是阿里云百炼平台提供的知识库全生命周期管理与语义检索/问答能力的编程接口，覆盖知识库创建、文档导入、切片管理、监控、Agent 配置及运行时调用。所有接口通过 DashScope 网关统一提供服务，基于业务空间（`workspace_id`）和 API Key 进行鉴权与路由。开发者可通过该 API 实现知识库自动化构建、策略化检索与可集成的智能问答。

## 支持的模型/功能

RAG API 本身不直接暴露大模型推理能力，而是通过 **Agent 配置**与 **知识库元数据**间接绑定模型与向量能力：
- **嵌入模型**：在创建知识库（`/api/v1/indices/rag/index/create_v2`）时通过 `embeddingModelName`（如 `text-embedding-v4`）或 `multimodalEmbeddingModelName`（如 `qwen3-vl-embedding`）指定，影响向量化质量 [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。
- **重排序模型**：知识库级配置 `rerankModelName`（如 `qwen3-rerank`），用于检索后结果精排；全局混排策略则在 Agent 的 `hybrid_rerank` 中定义 [查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)。
- **问答/检索模型**：由 Agent 的 `agent_model` 字段控制（如 `qwen3.7-plus`），在创建或更新 Agent 时配置，决定最终生成阶段的 LLM [创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)。
- **核心功能分三类**：
  - **知识库管理**：CRUD 知识库、文档、切片（`/api/v1/indices/rag/...`）；
  - **数据导入**：类目/文件/连接器管理（`/api/v1/connector/dash/...`）；
  - **运行时服务**：知识检索（`/api/v1/indices/knowledge/search`）与知识问答（`/api/v2/apps/knowledge/chat`），需先发布 Agent。

> **注意**：文档 34 和文档 35 均指出知识检索与问答接口属于 DashScope 应用网关体系，其 Base URL 与 OpenAPI 一致，但鉴权方式、限流策略（默认 25 QPS）及参数结构（如 `agent_id`）与知识库管理接口有本质差异，不可混用。

## 关键参数

| 参数名 | 所属接口 | 必填 | 类型 | 说明 |
|--------|----------|------|------|------|
| `workspace_id` | 全局 | 是 | string | 业务空间 ID，格式如 `llm-xxxxxxxxxxxx`，拼入 Base URL 构成 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com` [概览](../../raw/application-api-reference/rag-api/rag-api-overview.md) |
| `Authorization: Bearer <API-Key>` | 全局 | 是 | header | API Key 鉴权凭证，需在控制台 [API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 获取 [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md) |
| `docIds` | `/create_v2`, `/job/create` | 是 | array<string> | 文件 ID 列表，用于批量导入；注意参数名是 `docIds`，非 `file_ids` 或 `fileIds` [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md) |
| `index_id` / `indexId` | 多个接口 | 是 | string | 知识库 ID，但命名不一致：删除知识库用 `index_id`（snake_case），而查询切片列表用 `indexId`（camelCase）；传错将返回 `Index.InvalidParameter` [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)、[查询切片列表](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-list-chunks.md) |
| `agent_id` | `/knowledge/search`, `/knowledge/chat` | 是 | string | 已发布 Agent 的唯一标识，必须通过 Agent 管理 API 创建并发布后获得，非知识库 ID [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md) |

## 使用方式

1. **准备环境**：获取 `workspace_id`（控制台 > 业务空间管理）和 `API-Key`（控制台 > API Key 页面），设置环境变量 `BAILIAN_API_KEY`。
2. **构建知识库**：
   - （可选）调用数据导入接口（如 `/api/v1/connector/dash/addCategory`）准备类目；
   - 调用 `/api/v1/indices/rag/index/create_v2` 创建知识库并导入文件，获取 `pipelineId`（即知识库 ID）；
   - 或先创建空知识库，再通过 `/api/v1/indices/rag/index/job/create` 追加导入。
3. **配置运行时服务**：
   - 调用 Agent 管理 API（如 `/api/v1/indices/rag/app/create`）创建 Agent，绑定知识库并配置 `agent_config`；
   - 调用 `/api/v1/indices/rag/app/deploy` 发布 Agent，获取 `agent_id`。
4. **发起检索/问答**：
   - **检索**：`POST /api/v1/indices/knowledge/search`，传 `agent_id` 和 `query`/`images`；
   - **问答**：`POST /api/v2/apps/knowledge/chat`，传 `agent_id`、`messages` 及 `stream=true`（强制流式）。

所有请求使用 HTTPS + JSON，GET 接口参数通过 query string 传递（如 `/list?page_number=1`），POST 接口参数在 request body 中。

## 限制和注意事项

- **限流**：知识库管理接口有严格 QPS 限制，例如检索（`/rag/index/retrieve`）上限为 2000 QPS，而获取监控数据（`/rag/index/monitor`）仅 1 QPS；数据导入接口普遍为 10 QPS [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)。超出时返回 HTTP `429`，需按 `Retry-After` 头或指数退避重试。
- **不可逆操作**：删除知识库（`/delete`）、删除文档（`/delete_file`）、删除切片（`/chunk/delete`）均为永久删除，无回收站，调用前必须确认 [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)。
- **参数命名不一致**：多个接口存在 snake_case 与 camelCase 混用问题。例如：
  - 删除文档接口要求 `index_id` 和 `doc_ids`（snake_case）；
  - 查询切片列表接口要求 `indexId` 和 `pageNum`（camelCase）；
  - 传错名称（如 `IndexId`）将导致 `Index.InvalidParameter` 错误 [删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)。
- **Agent 版本管理**：`agent_config` 仅允许修改 `beta` 草稿版本；已发布版本只能修改描述（`agent_version_desc`），如需更新配置，必须先 `update` 草稿再 `deploy` 新版本 [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)。
- **文件上传流程**：三步式（申请租约 → OSS PUT 上传 → 注册文件），其中 `applyFileUploadLease` 的 `sizeBytes` 必须传字符串（如 `"1048576"`），`addFile` 的 `category` 参数名非 `categoryId`，需特别注意 [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)、[注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)。

## 来源文档

- [概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)
- [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)
- [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)
- [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)
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
- [查询切片列表](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-list-chunks.md)
- [更新切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-update-chunk.md)
- [删除切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-delete-chunk.md)
- [同步任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs.md)
- [提交导入任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-submit-sync-job.md)
- [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md)
- [查询任务状态](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-get-sync-job-status.md)
- [查询类目列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-category.md)
- [新增类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-category.md)
- [新增切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-add-chunk.md)
- [数据导入](../../raw/application-api-reference/rag-api/rag-api-data-import.md)
- [查询文件详情](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-describe-file.md)
- [删除类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-category.md)
- [删除文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-file.md)
- [批量更新文件标签](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-batch-update-tag.md)
- [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)
- [从 OSS 批量导入](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-oss-import.md)
- [新增连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-connector.md)
- [查询连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-get-connector.md)
- [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)
- [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)
- [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)
- [查询文件列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-file.md)
- [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)
- [创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)
- [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)
- [发布 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-deploy.md)
- [删除 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-delete.md)
- [查询 Agent 列表](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-list.md)
- [查询 Agent 详情](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-get.md)
- [复制 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-copy.md)
- [注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)
- [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md)


