# rag api

RAG API 是百炼平台提供的知识增强服务接口集合，支持知识库全生命周期管理、文档与切片操作、数据导入、检索及问答等核心能力。所有接口通过统一的业务空间 Endpoint 提供服务，采用 API Key 鉴权，遵循 RESTful 设计规范与标准化 JSON 响应格式。

## 支持的模型/功能

RAG API 提供两类核心能力：**知识管理**（含知识库、文档、切片、数据源）与**知识应用**（含检索、问答、Agent 管理）。

- **知识库类型**：支持 `document`（文档搜索）、`table`（数据查询）、`image`（图片问答）、`multimedia`（音视频搜索），需与 `structureType`（`unstructured`/`structured`）及 `knowledgeScene`（如 `basic_document_qa`、`image_qa`）严格匹配 [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。
- **向量模型**：可通过 `embeddingModelName`（如 `text-embedding-v4`）和 `multimodalEmbeddingModelName`（如 `qwen3-vl-embedding`）显式指定嵌入模型；重排序模型由 `rerankModelName`（如 `qwen3-rerank`）控制，配置在知识库或 Agent 层级。
- **Agent 能力**：通过 [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md) 创建、更新、发布 `chat` 或 `search` 场景的智能体，其 `agent_config` 封装模型（`agent_model`）、策略（`agent_policy`）、安全（`enable_anti_leak`）及检索配置（`kb_search_configs`），是运行时 `knowledge/chat` 和 `knowledge/search` 的前置依赖 [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)。
- **多模态支持**：`image_qa` 和 `visual_perception_qa` 场景强制要求 `multimodalEmbeddingModelName`；知识问答接口支持多模态输入（文本+图片 URL 数组），知识检索接口支持 `query` 与 `images` 同时传入实现联合检索 [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)。

> **注意**：文档 6 明确 `knowledgeScene` 为 `lite_document_qa` 时 `sinkType` 必须为 `BUILT_IN`，但文档 7 的响应示例中 `sinkType` 字段未出现，且未说明默认值。实际使用请以创建接口文档为准，避免依赖响应字段推断。

## 关键参数

| 参数名 | 所属接口 | 类型 | 说明 | 注意事项 |
|--------|----------|------|------|----------|
| `index_id` | `/api/v1/indices/rag/index/delete`, `/api/v1/indices/rag/index/files` | string | 知识库 ID（即 `pipelineId`） | 文档管理类接口统一用 `snake_case`（如 `index_id`, `doc_ids`），而切片管理类接口用 `camelCase`（如 `indexId`, `docId`）[删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md) |
| `docIds` | `/api/v1/indices/rag/index/create_v2`, `/api/v1/indices/rag/index/job/create` | array<string> | 文件 ID 列表 | 参数名固定为 `docIds`（非 `fileIds` 或 `documentIds`），传错将被忽略并返回 `Index.InvalidParameter` [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md) |
| `agent_id` | `/api/v1/indices/knowledge/search`, `/api/v2/apps/knowledge/chat` | string | 已发布 Agent 的唯一标识 | 必须先通过 Agent 管理 API 创建并发布，否则返回 “Agent 未发布” 错误；`agent_id` 由管理 API 返回，不可自行构造 [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md) |
| `category` | `/api/v1/connector/dash/addFile`, `/api/v1/connector/dash/applyFileUploadLease` | string | 类目 ID | 参数名为 `category`（非 `categoryId`），与 `listFile` 等接口不一致，易出错 [注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md) |
| `stream` | `/api/v2/apps/knowledge/chat` | boolean | 是否启用 SSE 流式响应 | **必须为 `true`**，当前版本不支持非流式模式，设为 `false` 或省略将导致请求失败 [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md) |

## 使用方式

### 1. 基础准备
- 获取业务空间 ID（`workspace_id`）和 API Key，配置 Base URL：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com`。
- 所有请求必须携带 `Authorization: Bearer <API-Key>` 和 `Content-Type: application/json`（POST 请求）。

### 2. 典型工作流
1. **数据准备**：  
   - 创建类目 → 上传文件（`applyFileUploadLease` → OSS PUT → `addFile`）→ 查询文件详情。
2. **知识库构建**：  
   - 创建知识库并导入（`create_v2`）或先创建后追加（`job/create`）→ 监控状态（`index_job/status`）。
3. **能力封装**：  
   - 创建 Agent（`app/create`）→ 配置 `agent_config`（含 `kb_search_configs`）→ 发布（`app/deploy`）→ 获取 `agent_id`。
4. **运行时调用**：  
   - 知识检索：`POST /api/v1/indices/knowledge/search`，传 `agent_id` + `query`/`images`。  
   - 知识问答：`POST /api/v2/apps/knowledge/chat`，传 `agent_id` + `messages`（完整历史），`Accept: text/event-stream`。

### 3. 请求示例（知识检索）
```bash
curl -X POST "https://llm-xxxxxxxxxxxx.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search" \
  -H "Authorization: Bearer $BAILIAN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "aid-xxxxxxxxxxxxxxxx",
    "query": "推荐一件适合秋冬的运动夹克"
  }'
```

## 限制和注意事项

- **限流策略**：知识库管理接口 QPS 差异大，检索接口上限为 2000 QPS，而 `get-index-monitor` 仅 1 QPS；知识检索与问答运行时接口默认用户维度 25 QPS [限流策略](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)。超限返回 `429`，需按 `Retry-After` 头或指数退避重试。
- **不可逆操作**：删除知识库、文档、切片、类目、文件均为软/硬删除，**无法恢复**，调用前务必确认 [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)。
- **参数命名不一致**：`index_id`（文档管理）、`indexId`（切片管理）、`id`（更新知识库）、`pipelineId`（新增切片）混用，需严格对照各接口文档，错误命名将导致 `400 InvalidParameter`。
- **状态码语义**：部分数据导入接口（如 `listCategory`）失败时 HTTP 状态码仍为 `200`，需检查响应体 `status` 字段（如 `400`）和 `code` 字段（如 `InvalidParameter`）判断真实结果 [查询类目列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-category.md)。
- **Agent 版本控制**：仅 `beta` 草稿版可修改 `agent_config`；已发布版本只能更新 `agent_version_desc`。配置变更必须走“update draft → deploy”流程，直接修改已发布版本无效 [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)。

## 来源文档

- [API 概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)
- [认证方式](../../raw/application-api-reference/rag-api/rag-api-authentication.md)
- [限流策略](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)
- [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)
- [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md)
- [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)
- [查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)
- [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)
- [获取知识库监控数据](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)
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
- [数据导入](../../raw/application-api-reference/rag-api/rag-api-data-import.md)
- [新增类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-category.md)
- [查询类目列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-category.md)
- [删除类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-category.md)
- [查询文件列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-file.md)
- [查询文件详情](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-describe-file.md)
- [批量更新文件标签](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-batch-update-tag.md)
- [删除文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-file.md)
- [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)
- [从 OSS 批量导入](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-oss-import.md)
- [新增连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-connector.md)
- [查询连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-get-connector.md)
- [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)
- [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)
- [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md)
- [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)
- [创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)
- [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)
- [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)
- [发布 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-deploy.md)
- [删除 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-delete.md)
- [查询 Agent 列表](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-list.md)
- [查询 Agent 详情](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-get.md)
- [复制 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-copy.md)
- [注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)


