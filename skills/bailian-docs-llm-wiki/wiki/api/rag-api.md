# rag api

RAG API 是百炼平台提供的面向开发者的一套知识库管理与检索服务接口，覆盖知识库生命周期管理、文档与切片操作、数据导入、Agent 配置及运行时检索/问答等全链路能力。所有接口均通过 DashScope 网关统一接入，采用标准 RESTful 设计与 Bearer Token 鉴权，支持结构化与非结构化知识场景。

## 支持的模型/功能

RAG API 支持多模态与文本混合检索、知识问答、知识路由、混排（rerank）、向量嵌入（embedding）及富文本文档解析等核心能力。  
- **知识库类型**：`document`（文档搜索）、`table`（数据查询）、`image`（图片问答）、`multimedia`（音视频搜索），对应 `structureType` 为 `unstructured` 或 `structured`；具体能力需匹配 `knowledgeScene`（如 `visual_perception_qa`、`basic_table_qa`）并指定相应模型 [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。  
- **嵌入模型**：支持 `text-embedding-v4` 等文本嵌入模型；多模态场景需显式传入 `multimodalEmbeddingModelName`（如 `qwen3-vl-embedding`）[创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。  
- **重排序模型**：默认使用 `qwen3-rerank`，可在知识库创建或更新时配置 `rerankModelName`，并在检索时通过 `kb_search_configs` 控制 per-kb 的 `rerank_top_n` 和 `rerank_min_score` [查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)。  
- **Agent 运行时模型**：知识问答与检索服务支持 `qwen3.7-plus`、`qwen3.6-plus` 等大模型，由 `agent_config.agent_model` 指定，且受 `agent_policy`（`turbo`/`agentic`）影响执行路径 [创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)。

> **注意**：文档中提及的 `visual_document_qa` 场景虽在 [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md) 中列为可选值，但控制台已移除该入口，不建议在新业务中使用。

## 关键参数

| 参数名 | 所属接口 | 说明 | 注意事项 |
|--------|----------|------|----------|
| `docIds` | `/api/v1/indices/rag/index/create_v2`, `/api/v1/indices/rag/index/job/create` | 创建或追加导入时指定的文件 ID 列表 | 参数名是 `docIds`（复数），非 `file_ids` 或 `documentIds`；校验失败时错误信息中误写为 `file_ids` [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md) |
| `index_id` / `indexId` | 多个接口 | 知识库 ID 字段名不统一 | 删除知识库（`/delete`）和删除文档（`/delete_file`）使用 `index_id`（snake_case）；而查询文档列表（`/files`）、查询切片列表（`/chunklist`）等使用 `indexId`（camelCase）；传错将返回 `Index.InvalidParameter` [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)、[删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md) |
| `category` / `categoryId` | 数据导入系列接口 | 类目 ID 字段名不一致 | `applyFileUploadLease` 和 `addFile` 使用 `category`；`listFile`、`addFilesFromAuthorizedOss` 等使用 `categoryId`；务必按接口文档严格匹配 [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)、[注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md) |
| `maxResult` | `/listCategory`, `/listFile` | 分页参数名 | 必须传 `maxResult`（单数），传 `maxResults`（复数）会被静默忽略 [查询类目列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-category.md) |

## 使用方式

1. **认证与端点**：所有请求需携带 `Authorization: Bearer <API-Key>` Header，并使用业务空间 ID 构造 Base URL：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com`；API Key 在 [控制台 API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 获取 [认证方式](../../raw/application-api-reference/rag-api/rag-api-authentication.md)。  
2. **典型流程**：  
   - **准备数据**：先调用数据导入接口（如 `addCategory` → `applyFileUploadLease` → `addFile`）将文件入库；  
   - **构建知识库**：调用 `/api/v1/indices/rag/index/create_v2` 创建知识库并同步导入，或用 `/api/v1/indices/rag/index/job/create` 追加导入；  
   - **配置服务**：通过 Agent 管理 API（`/app/create` → `/app/update` → `/app/deploy`）创建并发布知识问答/检索服务，获取 `agent_id`；  
   - **运行时调用**：对 `/api/v1/indices/knowledge/search`（检索）或 `/api/v2/apps/knowledge/chat`（问答）发起流式 POST 请求，传入 `agent_id` 与 `query`/`messages`。  
3. **请求格式**：除少数 GET 接口（如 `/list`、`/files`）外，其余均为 POST + JSON；请求体与响应体均为 UTF-8 编码 JSON；通用响应结构含 `code`、`status_code`、`data`、`request_id` 字段 [API 概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)。

## 限制和注意事项

- **限流策略**：各接口有独立 QPS 上限，例如检索接口 `/rag/index/retrieve` 为 2000 QPS，而监控接口 `/rag/index/monitor` 仅 1 QPS；超限返回 HTTP `429`，应遵循 `Retry-After` 头或指数退避重试 [限流策略](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)。  
- **不可逆操作**：删除知识库（`/delete`）、删除文档（`/delete_file`）、删除切片（`/chunk/delete`）、删除类目（`/deleteCategory`）均为软/硬删除且不可恢复，调用前必须确认 [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)、[删除类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-category.md)。  
- **参数兼容性**：`knowledgeType` 与 `knowledgeScene` 必须同时提供或同时省略；`sinkType` 为 `BUILT_IN` 时强制要求 `knowledgeScene` 为 `lite_document_qa`；`visual_perception_qa` 和 `image_qa` 场景必须提供 `multimodalEmbeddingModelName` [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。  
- **Agent 版本管理**：`agent_config` 仅允许修改 `beta` 草稿版本；已发布版本（如 `1`、`2`）只能修改 `agent_version_desc`，如需更新配置，必须先 `update` 草稿再 `deploy` 发布新版本 [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)。

## 来源文档

- [API 概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)
- [认证方式](../../raw/application-api-reference/rag-api/rag-api-authentication.md)
- [限流策略](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)
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
- [新增切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-add-chunk.md)
- [删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)
- [切片管理](../../raw/application-api-reference/rag-api/rag-api-chunks.md)
- [更新切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-update-chunk.md)
- [删除切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-delete-chunk.md)
- [同步任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs.md)
- [提交导入任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-submit-sync-job.md)
- [查询切片列表](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-list-chunks.md)
- [查询任务状态](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-get-sync-job-status.md)
- [数据导入](../../raw/application-api-reference/rag-api/rag-api-data-import.md)
- [查询类目列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-category.md)
- [删除类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-category.md)
- [新增类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-category.md)
- [查询文件列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-file.md)
- [查询文件详情](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-describe-file.md)
- [批量更新文件标签](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-batch-update-tag.md)
- [删除文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-file.md)
- [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)
- [从 OSS 批量导入](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-oss-import.md)
- [新增连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-connector.md)
- [查询连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-get-connector.md)
- [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)
- [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)
- [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md)
- [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)
- [创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)
- [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)
- [发布 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-deploy.md)
- [删除 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-delete.md)
- [查询 Agent 列表](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-list.md)
- [注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)
- [复制 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-copy.md)
- [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)
- [查询 Agent 详情](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-get.md)


