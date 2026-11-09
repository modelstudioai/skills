# rag api

RAG API 是百炼平台提供的知识库管理与检索服务接口，支持开发者以编程方式完成知识库创建、文档导入、切片管理、联合检索及智能问答等全链路操作。所有接口均基于 HTTPS 协议，通过统一的业务空间 Endpoint 和 API Key 鉴权，适用于构建企业级知识增强应用。核心能力分为三类：知识库管理（`/api/v1/indices/rag/`）、数据导入（`/api/v1/connector/dash/`）和运行时服务（`/api/v1/indices/knowledge/search` 与 `/api/v2/apps/knowledge/chat`）。

## 支持的模型/功能

RAG API 支持多模态与文本混合检索、结构化/非结构化知识库、多级切片策略及可配置重排序。关键能力包括：

- **知识库类型**：`document`（文档搜索）、`table`（数据查询）、`image`（图片问答）、`multimedia`（音视频搜索），对应 `knowledgeType` 参数；其中 `document` 类型支持 `basic_document_qa`、`visual_perception_qa`、`lite_document_qa` 等多种 `knowledgeScene` [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。
- **嵌入与重排模型**：可通过 `embeddingModelName`（如 `text-embedding-v4`）和 `rerankModelName`（如 `qwen3-rerank`）显式指定，响应中亦返回当前配置 [查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)。
- **Agent 封装能力**：通过 Agent 管理 API（`/api/v1/indices/rag/app/`）可创建、配置并发布检索或问答服务实例，其 `agent_config` 中定义 `kb_search_configs`、`rerank_top_n`、`hybrid_rerank` 等策略 [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)。
- **多模态支持**：`knowledgeScene=visual_perception_qa` 或 `image_qa` 时需传 `multimodalEmbeddingModelName`（如 `qwen3-vl-embedding`），且 `knowledgeType` 必须匹配 [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。

> **注意**：文档 6 明确要求 `knowledgeScene=visual_perception_qa` 时必须传 `multimodalEmbeddingModelName`，但文档 7 的响应示例中该字段为 `null`，表明实际部署可能使用默认模型；生产环境应显式传入以确保一致性。

## 关键参数

| 参数名 | 所属接口 | 说明 | 示例值 |
|--------|----------|------|--------|
| `index_id` / `id` | 多个接口 | 知识库 ID，命名不一致：删除/查询文档用 `index_id`，更新知识库用 `id` | `"your-kb-id"` |
| `docIds` | 创建知识库、提交导入任务 | 文件 ID 列表，参数名统一为 `docIds`（非 `file_ids` 或 `fileIds`），传错将被忽略 [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md) | `["file_xxx"]` |
| `pipelineId` | 切片管理、Agent 配置 | 知识库 ID 的别名，用于新增/更新/删除切片及 `kb_search_configs.id` | `"exg5ghdkag"` |
| `agent_id` | 知识检索、知识问答 | Agent 实例 ID，需在控制台创建并发布后获取，是运行时调用的必需凭证 [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md) | `"aid-xxxxxxxxxxxxxxxx"` |
| `search_filters` | 知识检索 | 按 `doc_id`、`tags` 或自定义 meta 字段过滤，支持嵌套 `_conditions` 实现 OR 条件 [概览](../../raw/application-api-reference/rag-api/rag-api-overview.md) | `[{"_operator": "OR", "_conditions": [{"tags": ["v2"]}, {"doc_id": "file_a"}]}]` |

> **注意**：文档 15 明确指出 `delete_file` 接口参数名为 `index_id`（snake_case），而文档 9 的 `update_index` 接口参数名为 `id`（无下划线），文档 12 的 `list_file_details` 使用 `indexId`（camelCase）。开发者需严格按接口文档命名，混用将导致 `InvalidParameter` 错误。

## 使用方式

### 1. 基础准备
- 获取 API Key：在[百炼控制台 API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key)创建并复制。
- 确定业务空间 ID（`{workspace_id}`）：格式如 `llm-xxxxxxxxxxxx`，在[业务空间管理](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)查看。
- Base URL 统一为：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com`

### 2. 典型流程示例（创建 → 导入 → 检索）
```bash
# 步骤1：创建知识库并导入文件（一步完成）
curl -X POST "$BASE_URL/api/v1/indices/rag/index/create_v2" \
  -H "Authorization: Bearer $BAILIAN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "产品文档",
    "description": "官方产品手册",
    "structureType": "unstructured",
    "sourceType": "DATA_CENTER_FILE",
    "docIds": ["file_xxx"]
  }'

# 步骤2：查询知识库列表获取 pipelineId
curl -G "$BASE_URL/api/v1/indices/rag/index/list" \
  -H "Authorization: Bearer $BAILIAN_API_KEY" \
  -d "page_size=1"

# 步骤3：调用知识检索（需先创建并发布 Agent）
curl -X POST "$BASE_URL/api/v1/indices/knowledge/search" \
  -H "Authorization: Bearer $BAILIAN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "aid-xxxxxxxxxxxxxxxx",
    "query": "如何配置API密钥？"
  }'
```

### 3. 运行时调用要点
- **知识检索**（`/api/v1/indices/knowledge/search`）：POST 请求，`query` 与 `images` 至少传一个，`kb_search_configs` 可动态覆盖部分过滤条件 [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)。
- **知识问答**（`/api/v2/apps/knowledge/chat`）：必须 `stream=true`，`input.messages` 传完整对话历史，`parameters.agent_options.session_files` 可临时传入会话文件 [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)。

## 限制和注意事项

- **限流规则**：
  - 知识库管理接口（如 `/rag/index/retrieve`）QPS 上限为 2000；
  - 知识检索与问答接口按“每 10 秒请求数”限流，默认 10 次/10秒；
  - 超限返回 HTTP `429`，建议按 `Retry-After` 头或指数退避（1s/2s/4s）重试 [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)。

- **安全与权限**：
  - API Key 具有账号级权限，严禁硬编码或提交至代码仓库，应使用环境变量存储 [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)；
  - RAM 子账号需授予 `AliyunBailianDataFullAccess` 权限并加入目标业务空间 [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)。

- **不可逆操作警告**：
  - 删除知识库（`/rag/index/delete`）、删除文档（`/rag/index/delete_file`）、删除切片（`/rag/index/chunk/delete`）均永久移除数据且无法恢复 [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)；
  - 删除类目（`/connector/dash/deleteCategory`）会使下属文件变为未归类状态 [删除类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-category.md)。

- **参数与格式陷阱**：
  - 时间戳：`/index/monitor` 接口要求**秒级** Unix 时间戳（非毫秒），而其他接口如 `/list-documents` 返回的是毫秒级时间戳 [获取知识库监控数据](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)；
  - 字符串数字：`applyFileUploadLease` 的 `sizeBytes` 必须传字符串（如 `"1048576"`），传数字将失败 [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)；
  - 分页参数：`listCategory` 和 `listFile` 使用 `maxResult`（单数），传 `maxResults` 会被静默忽略 [查询类目列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-category.md)。

## 来源文档

- [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)
- [概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)
- [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)
- [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)
- [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md)
- [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)
- [查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)
- [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)
- [更新知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)
- [获取知识库监控数据](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)
- [文档管理](../../raw/application-api-reference/rag-api/rag-api-documents.md)
- [查询文件详情列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-file-details.md)
- [查询文档列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-documents.md)
- [切片管理](../../raw/application-api-reference/rag-api/rag-api-chunks.md)
- [删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)
- [新增切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-add-chunk.md)
- [查询切片列表](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-list-chunks.md)
- [更新切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-update-chunk.md)
- [删除切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-delete-chunk.md)
- [提交导入任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-submit-sync-job.md)
- [同步任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs.md)
- [查询任务状态](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-get-sync-job-status.md)
- [查询类目列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-category.md)
- [新增类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-category.md)
- [删除类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-category.md)
- [查询文件列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-file.md)
- [删除文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-file.md)
- [查询文件详情](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-describe-file.md)
- [批量更新文件标签](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-batch-update-tag.md)
- [数据导入](../../raw/application-api-reference/rag-api/rag-api-data-import.md)
- [从 OSS 批量导入](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-oss-import.md)
- [新增连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-connector.md)
- [查询连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-get-connector.md)
- [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)
- [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)
- [注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)
- [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)
- [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)
- [创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)
- [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)
- [发布 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-deploy.md)
- [删除 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-delete.md)
- [查询 Agent 列表](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-list.md)
- [查询 Agent 详情](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-get.md)
- [复制 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-copy.md)
- [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)
- [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md)


