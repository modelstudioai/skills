# rag api

RAG API 是百炼平台提供的知识库全生命周期管理与语义检索/问答服务接口集合，覆盖知识库创建、文档导入、切片管理、Agent 配置及运行时检索与问答能力。所有接口通过 DashScope 网关统一提供，基于业务空间（`workspace_id`）隔离资源，采用 API Key 鉴权。开发者可通过该 API 实现知识库自动化构建、策略化检索与可编程问答集成。

## 支持的模型/功能

RAG API 本身不直接暴露大模型调用，但深度集成以下模型能力：

- **嵌入模型**：支持 `text-embedding-v4` 等文本嵌入模型，通过 `embeddingModelName` 参数在创建知识库时指定（见[创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)）；多模态场景支持 `qwen3-vl-embedding`，需配合 `knowledgeScene: image_qa` 或 `visual_perception_qa` 使用。
- **重排序模型**：默认启用 `qwen3-rerank`（见[查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)响应示例），支持通过 `rerankModelName` 自定义，但当前未开放独立配置接口。
- **问答模型**：知识问答（`/api/v2/apps/knowledge/chat`）依赖 Agent 配置中的 `agent_model`（如 `qwen3.7-plus`），该字段在[创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)和[更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)中设置。
- **路由与混排模型**：知识检索（`/api/v1/indices/knowledge/search`）支持 `kb_router_model`（知识库路由）与 `hybrid_rerank` 全局混排配置，均通过 Agent 的 `agent_config` 定义。

> **注意**：文档中提及的 `qwen3-vl-plus` 仅在 `parserConfig.modelName`（用于文件解析）和 `kb_router_model`（用于知识库路由）两个上下文中出现，二者语义不同，不可混用；前者属数据导入阶段，后者属检索运行时阶段。

## 关键参数

| 参数名 | 所属接口 | 说明 | 示例值 |
|--------|----------|------|--------|
| `workspace_id` | 全局 | 业务空间 ID，构成 Base URL 主机名，格式如 `llm-xxxxxxxxxxxx` | `llm-abcd12345678` |
| `Authorization: Bearer <API-Key>` | 全局 | 必填请求头，API Key 从[控制台 API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key)获取 | `Bearer sk-xxx` |
| `pipelineId` / `indexId` / `index_id` | 多处 | 知识库 ID 字段命名不一致：`pipelineId` 用于切片增删改（如[新增切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-add-chunk.md)）、`indexId` 用于部分文档/监控接口（如[查询文件详情列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-file-details.md)）、`index_id` 用于知识库删除与文档删除（如[删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)） | `your-kb-id` |
| `agent_id` | 知识检索/问答 | Agent 实例 ID，由 Agent 管理 API 创建并发布后获得，是运行时接口的必需参数 | `aid-xxxxxxxxxxxxxxxx` |
| `docIds` | 创建/导入 | 文件 ID 列表参数名统一为 `docIds`（非 `file_ids` 或 `fileIds`），见[创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)与[提交导入任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-submit-sync-job.md) |
| `search_filters` | 检索 | 支持嵌套 `_conditions` 表达 OR 条件，语法详见[知识库 SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) |

## 使用方式

1. **准备凭证**：在百炼控制台获取 API Key，并确认业务空间 ID（`workspace_id`）。
2. **构建 Base URL**：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com`。
3. **选择路径前缀**：
   - 知识库管理：`/api/v1/indices/rag/`
   - 数据导入：`/api/v1/connector/dash/`
   - Agent 管理：`/api/v1/indices/rag/app/`
   - 知识检索/问答（运行时）：`/api/v1/indices/knowledge/search` 或 `/api/v2/apps/knowledge/chat`
4. **调用流程**：
   - **知识库侧**：先调用数据导入接口（如 `addCategory` → `applyFileUploadLease` → `addFile`）准备数据，再调用 `create_v2` 创建知识库。
   - **Agent 侧**：使用 Agent 管理 API（`create` → `update` → `deploy`）创建并发布服务，获取 `agent_id`。
   - **运行时**：用 `agent_id` 调用 `/knowledge/search` 或 `/knowledge/chat`，其中问答接口 `stream` 必须为 `true`（见[知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)）。

## 限制和注意事项

- **限流规则**：知识库管理接口中，`/rag/index/retrieve`（检索）QPS 上限为 2000，而 `/rag/index/monitor`（监控）仅为 1 QPS；知识检索与问答运行时接口默认用户维度 25 QPS（见[知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)与[知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)）。超限返回 `429`，应遵循 `Retry-After` 头或指数退避（1s/2s/4s）。
- **参数命名不一致**：`indexId`（camelCase）与 `index_id`（snake_case）混用，例如 `listFileDetails` 接口要求 `indexId`，而 `delete_file` 接口强制要求 `index_id`；传错将返回 `Index.InvalidParameter`（见[删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)）。
- **不可逆操作警告**：删除知识库（`/delete`）、删除文档（`/delete_file`）、删除类目（`/deleteCategory`）均为软删除但数据不可恢复，调用前必须确认无业务依赖。
- **Agent 版本约束**：`agent_config` 仅允许修改 `beta` 草稿版本；已发布版本（如 `1`, `2`）只能修改 `agent_version_desc`，如需更新配置，必须先 `update` 草稿再 `deploy`（见[更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)与[发布 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-deploy.md)）。
- **文件上传特殊要求**：`applyFileUploadLease` 接口的 `sizeBytes` 必须以字符串格式传入（如 `"1048576"`），传数字将失败（见[申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)）。

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
- [获取知识库监控数据](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)
- [文档管理](../../raw/application-api-reference/rag-api/rag-api-documents.md)
- [查询文档列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-documents.md)
- [查询文件详情列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-file-details.md)
- [删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)
- [切片管理](../../raw/application-api-reference/rag-api/rag-api-chunks.md)
- [新增切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-add-chunk.md)
- [更新切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-update-chunk.md)
- [删除切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-delete-chunk.md)
- [同步任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs.md)
- [提交导入任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-submit-sync-job.md)
- [查询任务状态](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-get-sync-job-status.md)
- [数据导入](../../raw/application-api-reference/rag-api/rag-api-data-import.md)
- [查询类目列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-category.md)
- [新增类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-category.md)
- [删除类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-category.md)
- [查询文件列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-file.md)
- [查询文件详情](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-describe-file.md)
- [删除文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-file.md)
- [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)
- [注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)
- [从 OSS 批量导入](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-oss-import.md)
- [新增连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-connector.md)
- [查询连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-get-connector.md)
- [查询切片列表](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-list-chunks.md)
- [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)
- [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)
- [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)
- [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md)
- [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)
- [创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)
- [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)
- [发布 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-deploy.md)
- [删除 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-delete.md)
- [查询 Agent 列表](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-list.md)
- [查询 Agent 详情](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-get.md)
- [复制 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-copy.md)
- [批量更新文件标签](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-batch-update-tag.md)


