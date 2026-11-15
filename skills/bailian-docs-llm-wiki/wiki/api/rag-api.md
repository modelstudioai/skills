# rag api

RAG API 是阿里云百炼平台提供的知识库全生命周期管理与语义检索/问答服务接口，覆盖知识库创建、文档导入、切片管理、监控查询、Agent 配置及运行时检索与问答等核心能力。所有接口均通过统一的业务空间 Endpoint 提供 HTTPS 服务，并采用 API Key 鉴权。开发者可通过编程方式构建端到端 RAG 应用，无需依赖控制台操作。

## 支持的模型/功能

RAG API 支持多类型知识库与多模态能力：
- **知识库类型**：`document`（文档搜索）、`table`（数据查询）、`image`（图片问答）、`multimedia`（音视频搜索），需与 `structureType`（`unstructured`/`structured`）匹配 [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。
- **嵌入模型**：通过 `embeddingModelName`（如 `text-embedding-v4`）和 `multimodalEmbeddingModelName`（如 `qwen3-vl-embedding`）指定，后者在 `knowledgeScene` 为 `image_qa` 或 `visual_perception_qa` 时必填。
- **重排序模型**：默认使用 `qwen3-rerank`，可在知识库创建或更新时配置 `rerankModelName` 及 `rerankMinScore`。
- **Agent 能力**：支持 `chat`（知识问答）与 `search`（联合检索）两类 Agent 场景，可配置 `agent_model`（如 `qwen3.7-plus`）、`agent_policy`（`turbo`/`agentic`）及混排策略 [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)。
- **检索与问答**：提供 `/api/v1/indices/knowledge/search`（跨库语义检索）与 `/api/v2/apps/knowledge/chat`（SSE 流式问答）两个运行时接口，均需已发布的 `agent_id` [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)。

> **注意**：文档 5 中 `knowledgeScene` 列出的 `visual_document_qa` 场景在控制台已下线，API 虽仍支持但不推荐新用；文档 38 和 39 中 `agent_config` 的 `enable_anti_leak` 等字段值类型为字符串（`"true"`/`"false"`），与常规布尔值不同，需严格按字符串传参。

## 关键参数

| 参数名 | 所属接口 | 说明 | 示例 |
|--------|----------|------|------|
| `workspace_id` | 全局 | 业务空间 ID，构成 Base URL：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com` | `llm-xxxxxxxxxxxx` |
| `Authorization: Bearer <API-Key>` | 全局 | 认证头，API Key 在[控制台 API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key)获取 [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md) | `Bearer ak-xxxxxxxx` |
| `index_id` / `id` / `pipelineId` | 知识库管理 | 知识库 ID 命名不一致：`delete` 接口用 `index_id`，`update` 用 `id`，`chunk` 相关接口用 `pipelineId` | `your-kb-id` |
| `docIds` | 导入与同步 | 文件 ID 列表参数名统一为 `docIds`（非 `file_ids` 或 `fileIds`），传错将导致 `Index.InvalidParameter` | `["file_xxx"]` |
| `agent_id` | 运行时 API | 知识检索与问答必需，由 Agent 管理 API 创建并发布后获得，未发布时调用返回错误 | `aid-xxxxxxxxxxxxxxxx` |
| `stream: true` | `/knowledge/chat` | 知识问答接口强制要求流式，`stream` 字段必须为 `true`，否则请求失败 | `{"stream": true}` |

## 使用方式

1. **准备凭证**：在[百炼控制台](https://bailian.console.aliyun.com/)获取 API Key 与业务空间 ID。
2. **构建 Base URL**：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com`。
3. **调用管理接口**（知识库/文档/切片/Agent）：
   - 使用 `POST`（多数）或 `GET`（如 `/list` 类查询）方法。
   - 请求头：`Authorization: Bearer <API-Key>` + `Content-Type: application/json`（POST 时）。
   - 请求体按接口文档传参，注意命名差异（如 `index_id` vs `id`）。
4. **调用运行时接口**（检索/问答）：
   - 检索：`POST /api/v1/indices/knowledge/search`，传 `agent_id` 和 `query`/`images`。
   - 问答：`POST /api/v2/apps/knowledge/chat`，`Accept: text/event-stream`，`input.messages` 传完整对话历史。
5. **处理响应**：所有接口返回统一 JSON 结构，成功时 `code` 为 `"Success"`，失败时解析 `error.code` 与 `error.message` [RAG API 错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)。

## 限制和注意事项

- **限流规则**：知识库管理接口按 QPS 限流（如 `/rag/index/retrieve` 为 2000 QPS），数据导入接口（如 `/describeFile`）为 10 QPS，知识检索与问答按每 10 秒请求数限流（默认 10 次）。超限返回 HTTP `429`，建议实现指数退避重试 [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)。
- **不可逆操作**：`DELETE` 类接口（知识库、文档、切片、类目、文件、Agent）均为软删除或永久删除，无恢复机制，调用前务必确认。
- **参数兼容性**：`/listFile` 和 `/listCategory` 接口的分页参数为 `maxResult`（单数），传 `maxResults` 将被静默忽略；`/applyFileUploadLease` 的 `sizeBytes` 必须为字符串（如 `"1048576"`），传数字会失败。
- **Agent 生命周期**：`agent_config` 仅允许修改 `beta` 草稿版本；已发布版本只能修改 `agent_version_desc`，如需更新配置，须先 `update` 草稿再 `deploy` 发布 [发布 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-deploy.md)。
- **时间戳格式**：`/monitor` 接口的 `startTimestamp`/`endTimestamp` 为秒级 Unix 时间戳（非毫秒），支持字符串或整数格式。

## 来源文档

- [概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)
- [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)
- [RAG API 错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)
- [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md)
- [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)
- [查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)
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
- [同步任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs.md)
- [提交导入任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-submit-sync-job.md)
- [查询任务状态](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-get-sync-job-status.md)
- [查询类目列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-category.md)
- [新增类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-category.md)
- [更新知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)
- [删除类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-category.md)
- [查询文件列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-file.md)
- [查询文件详情](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-describe-file.md)
- [删除文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-file.md)
- [批量更新文件标签](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-batch-update-tag.md)
- [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)
- [注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)
- [从 OSS 批量导入](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-oss-import.md)
- [查询数据集](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-get-connector.md)
- [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)
- [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)
- [数据导入](../../raw/application-api-reference/rag-api/rag-api-data-import.md)
- [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md)
- [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)
- [创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)
- [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)
- [发布 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-deploy.md)
- [删除 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-delete.md)
- [查询 Agent 列表](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-list.md)
- [新增数据集](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-connector.md)
- [查询 Agent 详情](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-get.md)
- [复制 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-copy.md)
- [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)
- [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)


