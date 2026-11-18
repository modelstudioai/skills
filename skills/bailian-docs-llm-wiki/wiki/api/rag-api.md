# rag api

RAG API 是阿里云百炼平台提供的知识增强型服务接口，支持通过编程方式管理知识库、导入文档、执行语义检索及调用知识问答能力。所有接口均基于 DashScope 网关提供 HTTPS 服务，采用统一的业务空间（`{workspace_id}`）和 API Key 鉴权机制，适用于构建企业级 RAG 应用。

## 支持的模型/功能

RAG API 提供三类核心能力：**知识库管理**（CRUD、切片、检索）、**数据导入**（类目/文件/OSS 批量管理）和**知识问答与检索**（运行时服务）。  
- **知识库类型**支持 `document`（文档搜索）、`table`（数据查询）、`image`（图片问答）、`multimedia`（音视频搜索），对应不同 `knowledgeType` 与 `knowledgeScene` 组合（如 `visual_perception_qa` 要求指定 `multimodalEmbeddingModelName`）[创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。  
- **嵌入与重排模型**可自定义：`embeddingModelName`（如 `text-embedding-v4`）、`rerankModelName`（如 `qwen3-rerank`），部分场景（如 `lite_document_qa`）强制要求 `sinkType: BUILT_IN`。  
- **Agent 封装能力**：通过 Agent 管理 API 创建 `chat` 或 `search` 场景的智能体，其 `agent_config` 定义模型（`qwen3.7-plus`）、策略（`turbo`/`agentic`）、混排配置等，并需发布后方可被 [`knowledge/search`](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md) 和 [`knowledge/chat`](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md) 运行时接口调用。

## 关键参数

- **通用认证**：所有请求必须携带 `Authorization: Bearer <API-Key>` 头，Base URL 为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com`。API Key 在[控制台 API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key)获取 [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)。  
- **知识库标识**：使用 `pipelineId`（即 `index_id` 或 `id`，注意各接口命名不一致：`createIndex` 返回 `data.pipelineId`，`updateIndex` 请求体用 `id`，`deleteIndex` 用 `index_id`）[更新知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)。  
- **文件与切片关联**：文档 ID 字段名存在差异——知识库管理接口（如 `listDocuments`）用 `index_id`，而数据导入接口（如 `listFile`）用 `categoryId`；切片操作中 `docId` 为可选过滤字段，但文档搜索类知识库必传 [查询切片列表](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-list-chunks.md)。  
- **Agent 调用必需项**：运行时接口 `knowledge/search` 和 `knowledge/chat` 必须传 `agent_id`（来自已发布的 Agent），且 `knowledge/chat` 强制要求 `stream: true` 并完整传递 `messages` 历史 [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)。  

> **注意**：`query` 参数在 `knowledge/search` 接口中为条件必填（纯图搜时可为空串），但若未传 `images` 且 `query` 为空，将返回 `InvalidParameter` 错误；而 `knowledge/chat` 的 `input.messages` 中 `content` 支持字符串或 ContentPart 数组，多模态需显式构造 `[{"type":"text","text":"..."},{"type":"image_url","image_url":{"url":"..."}}]` 结构。

## 使用方式

1. **准备环境**：获取业务空间 ID（`{workspace_id}`）和 API Key，确认 RAM 子账号已获 `AliyunBailianDataFullAccess` 权限。  
2. **构建知识库**：  
   - 调用 `/api/v1/indices/rag/index/create_v2` 创建知识库（指定 `structureType`, `knowledgeType`, `embeddingModelName` 等）；  
   - 通过数据导入接口（如 `/api/v1/connector/dash/applyFileUploadLease` → OSS PUT → `/api/v1/connector/dash/addFile`）上传文件；  
   - 或直接提交导入任务 `/api/v1/indices/rag/index/job/create` 关联已有文件。  
3. **管理内容**：使用 `/api/v1/indices/rag/index/chunk/*` 接口增删改查切片，注意 `chunkMode`（`h1`~`h5`/`length`/`regex`）影响分片逻辑。  
4. **发布 Agent**：调用 `/api/v1/indices/rag/app/create` → `/api/v1/indices/rag/app/update`（编辑 `beta` 草稿）→ `/api/v1/indices/rag/app/deploy` 获取 `agent_id`。  
5. **运行时调用**：  
   - 检索：`POST /api/v1/indices/knowledge/search`，传 `agent_id` + `query`/`images` + 可选 `kb_search_configs`；  
   - 问答：`POST /api/v2/apps/knowledge/chat`，传 `agent_id` + `messages` + `stream: true`。  

## 限制和注意事项

- **限流规则**：知识库管理接口按 QPS 限流（如 `/rag/index/retrieve` 为 2000 QPS），知识检索/问答接口按每 10 秒请求数限流（默认 10 次）[限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)。超限返回 HTTP `429`，建议按 `Retry-After` 头或指数退避重试。  
- **不可逆操作**：删除知识库（`/rag/index/delete`）、文档（`/rag/index/delete_file`）、切片（`/rag/index/chunk/delete`）均为软删除但数据不可恢复，调用前务必确认依赖关系 [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)。  
- **参数兼容性**：  
  - 数据导入接口（如 `/api/v1/connector/dash/listFile`）使用 `maxResult`（单数），传 `maxResults` 会被静默忽略；  
  - 文件详情查询 `/api/v1/indices/rag/list/index/file/details` 使用 camelCase（`pageNumber`），而知识库列表 `/api/v1/indices/rag/index/list` 使用 snake_case（`page_number`）；  
  - `knowledge/chat` 不保存对话状态，每次请求需传完整 `messages` 历史，避免超出模型上下文窗口。  
- **错误处理**：所有错误响应含 `request_id`，联系支持时必须提供；业务错误码（如 `KB_NOT_FOUND`、`RETRIEVAL_TIMEOUT`）需结合 HTTP 状态码判断，`504` 超时建议降低 `top_k` 或切换更小重排模型 [RAG API 错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)。

## 来源文档

- [概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)
- [RAG API 错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)
- [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)
- [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md)
- [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)
- [查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)
- [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)
- [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)
- [更新知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)
- [文档管理](../../raw/application-api-reference/rag-api/rag-api-documents.md)
- [查询文档列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-documents.md)
- [查询文件详情列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-file-details.md)
- [删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)
- [切片管理](../../raw/application-api-reference/rag-api/rag-api-chunks.md)
- [新增切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-add-chunk.md)
- [查询切片列表](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-list-chunks.md)
- [更新切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-update-chunk.md)
- [删除切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-delete-chunk.md)
- [同步任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs.md)
- [提交导入任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-submit-sync-job.md)
- [查询任务状态](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-get-sync-job-status.md)
- [获取知识库监控数据](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)
- [数据导入](../../raw/application-api-reference/rag-api/rag-api-data-import.md)
- [删除类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-category.md)
- [查询文件列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-file.md)
- [查询类目列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-category.md)
- [查询文件详情](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-describe-file.md)
- [新增类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-category.md)
- [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)
- [注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)
- [删除文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-file.md)
- [批量更新文件标签](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-batch-update-tag.md)
- [新增数据集](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-connector.md)
- [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)
- [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)
- [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)
- [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md)
- [从 OSS 批量导入](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-oss-import.md)
- [创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)
- [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)
- [发布 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-deploy.md)
- [删除 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-delete.md)
- [查询 Agent 列表](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-list.md)
- [查询 Agent 详情](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-get.md)
- [复制 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-copy.md)
- [查询数据集](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-get-connector.md)
- [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)


