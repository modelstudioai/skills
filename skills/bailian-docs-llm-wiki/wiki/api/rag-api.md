# rag api

RAG API 是阿里云百炼平台提供的知识库全生命周期管理与语义检索/问答服务接口集合，覆盖知识库创建、文档导入、切片管理、Agent 配置及运行时检索与问答能力。所有接口通过 DashScope 网关统一提供，基于业务空间（workspace_id）隔离资源，采用 API Key 鉴权。开发者可通过该 API 实现知识库自动化构建、策略化检索与可编程问答集成。

## 支持的模型/功能

RAG API 本身不直接暴露大语言模型调用，但深度集成以下模型能力：

- **嵌入模型（Embedding）**：支持 `text-embedding-v4` 等文本向量模型，通过 `embeddingModelName` 参数在创建知识库时指定；多模态场景需使用 `qwen3-vl-embedding` 等模型，由 `multimodalEmbeddingModelName` 控制。
- **重排序模型（Rerank）**：默认启用 `qwen3-rerank`，可在知识库配置中通过 `rerankModelName` 覆盖；支持 `rerankMinScore`（最低分数阈值）、`rerankTopN`（重排数量）等精细化控制。
- **问答与检索 Agent 模型**：Agent 层支持 `qwen3.7-plus`、`qwen3.6-plus` 等大模型，通过 `agent_config.agent_model` 字段配置，详见 [创建 Agent](raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md) 文档。
- **解析模型**：文件解析阶段支持 `DOCMIND`、`DASH_QWEN_VL_PARSER`（需配合 `qwen3-vl-plus`）等专用模型，由 `parser` 和 `parserConfig` 参数控制。

> **注意**：文档 6 中 `knowledgeScene` 列出的 `visual_document_qa` 场景在控制台已下线，API 虽仍接受该值，但实际行为可能与文档描述不一致，建议优先使用 `basic_document_qa` 或 `lite_document_qa`。

## 关键参数

| 参数名 | 所属接口 | 类型 | 说明 | 示例 |
|--------|----------|------|------|------|
| `workspace_id` | 全局 | string | 业务空间 ID，构成 Base URL 的核心部分，格式如 `llm-xxxxxxxxxxxx`，在[业务空间管理](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)页面获取 | `llm-abcd12345678` |
| `Authorization: Bearer <API-Key>` | 全局 | header | 必填认证头，API Key 在[控制台 API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key)获取 | `Bearer sk-xxx` |
| `pipelineId` / `indexId` / `index_id` | 多接口 | body | 知识库 ID 字段命名不统一：`pipelineId` 用于切片增删改（如 [新增切片](raw/application-api-reference/rag-api/rag-api-chunks/rag-api-add-chunk.md)），`indexId` 用于查询类接口（如 [查询任务状态](raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-get-sync-job-status.md)），`index_id` 用于删除类接口（如 [删除知识库](raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)）。务必按接口文档要求传参，否则返回 `Index.InvalidParameter`。 | `your-kb-id` |
| `agent_id` | `/knowledge/search`, `/knowledge/chat` | body | 知识检索或问答服务的运行实体 ID，必须先通过 Agent 管理 API 创建并发布，详见 [Agent 管理概述](raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md) | `aid-xxxxxxxxxxxxxxxx` |
| `docIds` | `/create_v2`, `/job/create` | body | 文件 ID 列表，参数名固定为 `docIds`（非 `file_ids` 或 `documentIds`），错误命名将导致参数被忽略并报错 | `["file_xxx", "file_yyy"]` |

## 使用方式

1. **准备凭证**：在百炼控制台获取 API Key，并确认所属业务空间 ID（`workspace_id`）。
2. **构造 Base URL**：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com`。
3. **选择接口路径**：
   - 知识库管理：`/api/v1/indices/rag/...`（如 `/index/create_v2`, `/index/list`）
   - 数据导入：`/api/v1/connector/dash/...`（如 `/listCategory`, `/applyFileUploadLease`）
   - 运行时服务：`/api/v1/indices/knowledge/search`（检索）、`/api/v2/apps/knowledge/chat`（问答，SSE 流式）
4. **发起请求**：携带 `Authorization` Header 与符合规范的 JSON 请求体（POST）或 query string（GET）。
5. **处理响应**：所有接口返回统一结构，成功时 `code` 为 `"Success"`，失败时 `error.code` 包含业务错误码（如 `KB_NOT_FOUND`），并附带 `request_id` 用于问题排查。

示例（创建知识库）：
```bash
curl -X POST "https://llm-abcd12345678.cn-beijing.maas.aliyuncs.com/api/v1/indices/rag/index/create_v2" \
  -H "Authorization: Bearer $BAILIAN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "产品文档",
    "description": "官方产品手册",
    "structureType": "unstructured",
    "sinkType": "DEFAULT",
    "sourceType": "DATA_CENTER_FILE",
    "docIds": ["file_abc123"]
  }'
```

## 限制和注意事项

- **限流规则**：知识库管理接口有严格 QPS 限制，例如 `/rag/index/retrieve` 最高 2000 QPS，而 `/rag/index/monitor` 仅 1 QPS；运行时问答与检索接口默认用户维度 25 QPS。超限返回 `429`，应遵循 `Retry-After` 头或指数退避策略（1s/2s/4s）[错误码](raw/application-api-reference/rag-api/rag-api-errors.md)。
- **参数命名不一致**：多个接口存在字段命名差异，是高频出错点：
  - 知识库 ID：`pipelineId`（切片操作）、`indexId`（查询任务状态）、`index_id`（删除知识库/文档）；
  - 文件 ID 列表：`docIds`（创建/追加导入），而非 `file_ids`；
  - 类目 ID：`category`（`applyFileUploadLease`/`addFile`），而非 `categoryId`（`listFile`/`addFilesFromAuthorizedOss`）。
- **不可逆操作警告**：删除知识库（`/index/delete`）、删除文档（`/index/delete_file`）、删除类目（`/deleteCategory`）均为软删除但数据不可恢复，调用前必须二次确认。
- **时间戳格式**：监控接口 `/index/monitor` 要求 `startTimestamp`/`endTimestamp` 为**秒级** Unix 时间戳（字符串或整数均可），而其他接口如 `/list-chunks` 返回的 `gmt_modified` 为毫秒级，务必区分。
- **Agent 生命周期约束**：Agent 配置仅允许修改 `beta` 草稿版本；已发布版本（如 `1`, `2`）只能更新 `agent_version_desc`，如需变更配置，必须先 `update` 草稿再 `deploy` 发布新版本 [更新 Agent](raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)。

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
- [新增连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-connector.md)
- [查询连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-get-connector.md)
- [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)
- [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)
- [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)
- [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md)
- [文档管理](../../raw/application-api-reference/rag-api/rag-api-documents.md)
- [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)
- [创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)
- [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)
- [发布 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-deploy.md)
- [删除 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-delete.md)
- [查询 Agent 列表](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-list.md)
- [查询 Agent 详情](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-get.md)
- [复制 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-copy.md)


