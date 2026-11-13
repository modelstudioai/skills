# rag api

RAG API 是百炼平台提供的知识库管理与检索服务接口，支持开发者以编程方式完成知识库的创建、更新、文档导入、切片管理、联合检索及智能问答等全流程操作。所有接口均基于 HTTPS 协议，通过统一的业务空间 Endpoint 和 API Key 鉴权访问，分为知识库管理、数据导入、Agent 管理、知识检索与问答四大功能域。

## 支持的模型/功能

RAG API 支持多模态与文本混合检索、结构化/非结构化知识库构建、细粒度切片控制及策略可配置的 Agent 封装能力：

- **嵌入模型**：可通过 `embeddingModelName`（如 `text-embedding-v4`）和 `multimodalEmbeddingModelName`（如 `qwen3-vl-embedding`）显式指定向量模型，分别用于文本与图文场景 [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。
- **重排序模型**：知识库级配置 `rerankModelName`（如 `qwen3-rerank`），支持 `rerankMinScore` 与 `rerankTopN` 等阈值控制 [查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)。
- **知识库类型与场景**：支持 `document`（基础/极速/视觉理解问答）、`table`（数据查询）、`image`（图片问答）、`multimedia`（音视频搜索）四类，每类绑定特定 `knowledgeScene` 与 `structureType` 组合 [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。
- **Agent 能力封装**：通过 Agent 管理 API 创建 `chat` 或 `search` 场景的运行实体，配置模型（`agent_model`）、策略（`turbo`/`agentic`）、安全开关（`enable_anti_leak`、`enable_citation`）及混排路由（`kb_router_model`、`hybrid_rerank`）等 [创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)。

> **注意**：文档 4 中 `knowledgeScene` 列出的 `visual_document_qa` 场景在控制台已下线，API 虽仍支持但不推荐使用；实际部署应优先选用 `basic_document_qa`、`lite_document_qa` 或 `visual_perception_qa`。

## 关键参数

以下为高频且易错的关键参数，需严格遵循命名、类型与约束：

- **认证与路由**：`Authorization: Bearer <API-Key>` 必须携带；Base URL 为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com`，其中 `{workspace_id}` 为业务空间 ID，非用户 UID 或项目 ID。
- **ID 字段命名不一致**：
  - 知识库 ID 在 `update` 接口为 `id`（非 `index_id` 或 `indexId`）[更新知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)；
  - 文档删除接口为 `index_id`（snake_case），而文件详情接口为 `indexId`（camelCase）[删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)；
  - 切片管理接口统一使用 `pipelineId`（非 `indexId`）[新增切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-add-chunk.md)。
- **时间戳格式**：监控接口 `startTimestamp`/`endTimestamp` 要求**秒级 Unix 时间戳**（字符串或整数均可），非毫秒 [获取知识库监控数据](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)。
- **文件大小传参**：`applyFileUploadLease` 接口的 `sizeBytes` 必须传**字符串**（如 `"1048576"`），传数字将导致失败 [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)。

## 使用方式

### 1. 基础流程
1. **准备凭证**：在[百炼控制台 API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key)创建并保管 API Key，按应用拆分、定期轮转 [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)；
2. **创建知识库**：调用 `/api/v1/indices/rag/index/create_v2`，指定 `name`、`structureType`、`sinkType` 及嵌入模型；
3. **导入数据**：通过数据导入 API（如 `applyFileUploadLease` → OSS PUT → `addFile`）或同步任务（`/index/job/create`）将文件注入知识库；
4. **构建 Agent**：调用 `/app/create` 创建 Agent，配置 `agent_config` 后通过 `/app/deploy` 发布，获取 `agent_id`；
5. **运行时调用**：使用 `agent_id` 调用 `/api/v1/indices/knowledge/search`（检索）或 `/api/v2/apps/knowledge/chat`（问答）。

### 2. 请求示例（检索）
```bash
curl -X POST "https://llm-xxxx.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search" \
  -H "Authorization: Bearer $BAILIAN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "aid-xxxx",
    "query": "如何配置 RAG API 的限流？"
  }'
```

## 限制和注意事项

- **限流规则**：
  - 知识库管理接口（如 `/index/list`、`/index/create_v2`）QPS 上限为 10；
  - 检索接口 `/rag/index/retrieve` QPS 上限为 2000，但知识检索运行时接口 `/knowledge/search` 默认**每 10 秒最多 10 次请求** [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)；
  - 触发限流返回 HTTP `429`，需依据 `Retry-After` 头或指数退避（1s/2s/4s）重试 [RAG API 错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)。

- **不可逆操作警告**：
  - 删除知识库（`/index/delete`）、删除文档（`/index/delete_file`）、删除切片（`/index/chunk/delete`）、删除类目（`/deleteCategory`）均为**永久删除，无法恢复**，调用前必须确认无业务依赖；
  - `deleteFile` 接口删除后，若该文件已被知识库引用，相关索引将失效 [删除文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-file.md)。

- **其他关键约束**：
  - 切片内容长度必须在 **10–6000 字符**之间，且不能超过知识库创建时设定的 `chunkSize` [更新切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-update-chunk.md)；
  - `kb_search_configs` 中的 `id` 必须属于 Agent 已绑定的知识库，同一请求中不可重复 [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)；
  - 知识问答接口 `stream` 字段**必须为 `true`**，否则请求失败 [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)。

## 来源文档

- [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)
- [RAG API 错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)
- [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)
- [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)
- [查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)
- [更新知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)
- [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)
- [概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)
- [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md)
- [文档管理](../../raw/application-api-reference/rag-api/rag-api-documents.md)
- [查询文档列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-documents.md)
- [查询文件详情列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-file-details.md)
- [删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)
- [切片管理](../../raw/application-api-reference/rag-api/rag-api-chunks.md)
- [新增切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-add-chunk.md)
- [查询切片列表](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-list-chunks.md)
- [更新切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-update-chunk.md)
- [删除切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-delete-chunk.md)
- [获取知识库监控数据](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)
- [同步任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs.md)
- [查询任务状态](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-get-sync-job-status.md)
- [数据导入](../../raw/application-api-reference/rag-api/rag-api-data-import.md)
- [查询类目列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-category.md)
- [新增类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-category.md)
- [查询文件列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-file.md)
- [查询文件详情](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-describe-file.md)
- [删除文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-file.md)
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
- [删除类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-category.md)
- [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)
- [发布 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-deploy.md)
- [创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)
- [查询 Agent 列表](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-list.md)
- [查询 Agent 详情](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-get.md)
- [复制 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-copy.md)
- [提交导入任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-submit-sync-job.md)
- [删除 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-delete.md)


