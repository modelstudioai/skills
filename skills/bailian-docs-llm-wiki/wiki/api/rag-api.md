# rag api

RAG API 是百炼平台提供的知识库管理与检索服务接口，支持通过编程方式创建、更新、查询知识库，导入文档，执行语义检索，并调用知识问答能力。所有接口均基于 HTTPS 协议，采用统一的鉴权机制和 JSON 数据格式，适用于构建企业级 RAG 应用。

## 支持的模型/功能

RAG API 提供三类核心能力：**知识库管理**（CRUD、切片操作）、**数据导入**（文件上传、类目管理、OSS 批量导入）和**知识检索与问答**（跨库检索、SSE 流式问答）。  
- **知识库类型**支持 `document`（文档搜索）、`table`（数据查询）、`image`（图片问答）和 `multimedia`（音视频搜索），需与 `structureType`（`unstructured`/`structured`）及 `knowledgeScene`（如 `basic_document_qa`、`image_qa`）匹配使用 [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。  
- **嵌入模型**可通过 `embeddingModelName`（如 `text-embedding-v4`）和 `multimodalEmbeddingModelName`（如 `qwen3-vl-embedding`）显式指定，后者在 `image_qa` 或 `visual_perception_qa` 场景下为必填 [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。  
- **重排序模型**默认为 `qwen3-rerank`，可在知识库创建或更新时配置 `rerankModelName`，并支持 `rerankMinScore` 阈值过滤低分切片 [查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)。  
- **Agent 管理**提供全生命周期 API（创建、更新、发布、删除），用于封装检索/问答策略，其 `agent_config` 中可配置 `agent_model`（如 `qwen3.7-plus`）、`agent_policy`（`turbo`/`agentic`）等参数 [创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)。

> **注意**：文档中 `knowledgeScene` 的取值存在不一致描述——[创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md) 提到 `visual_document_qa` 已被控制台移除，但未明确禁止 API 调用；实际使用时应优先选用 `basic_document_qa` 或 `lite_document_qa`，避免兼容性风险。

## 关键参数

| 参数名 | 位置 | 必填 | 类型 | 说明 |
|--------|------|------|------|------|
| `Authorization` | Header | 是 | string | `Bearer <API-Key>`，从[控制台 API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key)获取 [认证方式](../../raw/application-api-reference/rag-api/rag-api-authentication.md) |
| `workspace_id` | Base URL | 是 | string | 业务空间 ID，格式如 `llm-xxxxxxxxxxxx`，在[业务空间管理](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)查看 [API 概览](../../raw/application-api-reference/rag-api/rag-api-overview.md) |
| `index_id` / `pipelineId` | Body | 是 | string | 知识库 ID，创建后返回的 `data.id` 或 `data.pipelineId`；注意不同接口命名差异（如删除知识库用 `index_id`，而新增切片用 `pipelineId`） [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md) |
| `docIds` | Body | 是 | array<string> | 文件 ID 列表，用于创建知识库或提交导入任务；参数名固定为 `docIds`，非 `file_ids` 或 `fileIds` [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md) |
| `agent_id` | Body | 是 | string | Agent 实例 ID，需先通过 Agent 管理 API 创建并发布，再用于 [`knowledge/search`](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md) 或 [`knowledge/chat`](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md) [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md) |

> **注意**：参数命名风格不统一——知识库管理接口多用 `snake_case`（如 `index_id`, `doc_ids`），而切片/Agent 接口多用 `camelCase`（如 `indexId`, `pipelineId`, `agent_id`）。请求体字段缺失时，错误信息中的参数名可能与实际要求不符（如 `Index.InvalidParameter` 提示 `IndexId` 缺失，但正确参数名为 `index_id`），需以文档为准 [删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)。

## 使用方式

1. **准备凭证**：在百炼控制台获取 API Key，并确保 RAM 子账号已绑定 `AliyunBailianDataFullAccess` 权限 [认证方式](../../raw/application-api-reference/rag-api/rag-api-authentication.md)。  
2. **构造请求**：Base URL 为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com`；所有 POST 请求需设置 `Content-Type: application/json`，GET 请求参数通过 query string 传递 [API 概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)。  
3. **典型流程**：  
   - **创建知识库**：调用 `/api/v1/indices/rag/index/create_v2`，传入 `name`、`structureType`、`docIds` 等 [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。  
   - **追加文档**：调用 `/api/v1/indices/rag/index/job/create` 提交导入任务，再用 `/api/v1/indices/rag/index_job/status` 查询进度 [提交导入任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-submit-sync-job.md)。  
   - **执行检索**：先创建并发布 Agent（`search` 场景），再调用 `/api/v1/indices/knowledge/search`，传入 `agent_id` 和 `query` [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)。  
   - **发起问答**：调用 `/api/v2/apps/knowledge/chat`，`stream` 必须为 `true`，`input.messages` 需包含完整对话历史 [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)。  

## 限制和注意事项

- **限流策略**：各接口 QPS 上限不同，例如检索接口为 2000 QPS，而获取监控数据仅 1 QPS；超限返回 `429 Too Many Requests`，需按 `Retry-After` 头或指数退避重试 [限流策略](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)。  
- **不可逆操作**：删除知识库、文档、切片、文件或类目均为永久性操作，无回收站机制，调用前必须确认 [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)。  
- **文件上传流程**：需三步完成——先调用 `/api/v1/connector/dash/applyFileUploadLease` 获取租约，再 PUT 上传至 OSS，最后调用 `/api/v1/connector/dash/addFile` 注册；`sizeBytes` 必须传字符串格式（如 `"1048576"`） [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)。  
- **Agent 版本管理**：仅 `beta` 草稿版本允许修改 `agent_config`；已发布版本只能更新 `agent_version_desc`，如需配置变更，须先 `update` 草稿再 `deploy` 发布新版本 [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)。  
- **错误处理**：失败响应含 `request_id`，排查问题时必须提供；HTTP 状态码 `200` 不代表业务成功（如数据导入接口失败时仍返回 `200`，需检查 `status` 字段） [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)。

## 来源文档

- [认证方式](../../raw/application-api-reference/rag-api/rag-api-authentication.md)
- [API 概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)
- [限流策略](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)
- [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)
- [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)
- [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md)
- [更新知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)
- [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)
- [查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)
- [查询文档列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-documents.md)
- [查询文件详情列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-file-details.md)
- [文档管理](../../raw/application-api-reference/rag-api/rag-api-documents.md)
- [删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)
- [新增切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-add-chunk.md)
- [切片管理](../../raw/application-api-reference/rag-api/rag-api-chunks.md)
- [更新切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-update-chunk.md)
- [删除切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-delete-chunk.md)
- [查询切片列表](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-list-chunks.md)
- [同步任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs.md)
- [提交导入任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-submit-sync-job.md)
- [查询任务状态](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-get-sync-job-status.md)
- [数据导入](../../raw/application-api-reference/rag-api/rag-api-data-import.md)
- [查询类目列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-category.md)
- [查询文件列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-file.md)
- [查询文件详情](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-describe-file.md)
- [删除文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-file.md)
- [批量更新文件标签](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-batch-update-tag.md)
- [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)
- [注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)
- [从 OSS 批量导入](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-oss-import.md)
- [新增类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-category.md)
- [查询连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-get-connector.md)
- [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)
- [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)
- [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)
- [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md)
- [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)
- [创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)
- [新增连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-connector.md)
- [发布 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-deploy.md)
- [删除 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-delete.md)
- [查询 Agent 列表](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-list.md)
- [查询 Agent 详情](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-get.md)
- [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)
- [复制 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-copy.md)
- [获取知识库监控数据](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)
- [删除类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-category.md)


