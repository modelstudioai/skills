# rag api

RAG API 是百炼平台提供的知识库管理与检索服务接口，覆盖知识库生命周期管理、文档与切片操作、数据导入、知识检索及问答等核心能力。所有接口均通过 DashScope 网关统一提供，采用 API Key 鉴权与业务空间（`{workspace_id}`）隔离。开发者需按功能分组调用对应路径前缀的接口，并严格遵循协议约定与限流规则。

## 支持的模型/功能

RAG API 支持多模态与文本混合检索、结构化/非结构化知识库构建、Wiki 自动化构建、以及基于 Agent 的知识问答与联合检索服务。  
- **嵌入模型**：支持 `text-embedding-v3`、`text-embedding-v4`、`qwen3.7-text-embedding` 等向量模型，可在创建知识库时通过 `embeddingModelName` 指定；多模态场景需配合 `multimodalEmbeddingModelName`（如 `qwen3-vl-plus`）[原文标题](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。  
- **重排模型**：支持 `qwen3-rerank` 等模型，配置于知识库级别（`rerankModelName`）或 Agent 级别（`kb_search_configs.rerank`），影响检索结果排序质量 [原文标题](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)。  
- **Wiki 功能**：旗舰版知识库支持 Wiki 自动构建，依赖 `wikiConfig.extraction.synthesisModelId`（如 `qwen3.8-max`）与 `extractionGranularity`（`focused`/`standard`/`exhaustive`）等参数，需在更新知识库时显式配置 [原文标题](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)。  
- **Agent 场景**：支持 `chat`（知识问答）与 `search`（知识检索）两类 Agent，其策略（`agent_policy`）、模型（`agent_model`）、安全能力（`enable_anti_leak`、`enable_citation`）均可编程化配置与发布。

> **注意**：文档 5 与文档 45 对 `agent_id` 的使用逻辑存在不一致表述——前者将 `agent_id` 定义为知识问答服务标识，后者明确其为知识检索服务实例 ID；实际应以运行时 API（`/api/v1/indices/knowledge/search` 和 `/api/v2/apps/knowledge/chat`）的前置要求为准：`agent_id` 是 Agent 管理 API 创建并发布后生成的唯一服务实例 ID，与具体场景强绑定，不可跨 `chat`/`search` 复用。

## 关键参数

| 参数名 | 所属接口 | 类型 | 说明 | 注意事项 |
|--------|----------|------|------|----------|
| `index_id` / `pipelineId` | 知识库管理、文档/切片操作 | string | 知识库唯一标识符 | 创建接口返回 `data.pipelineId`；部分接口（如删除知识库）要求字段名为 `index_id`，而其他接口（如查询切片）要求 `pipelineId`，命名不统一 [原文标题](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md) |
| `docIds` | 创建知识库、提交导入任务 | array<string> | 文件 ID 列表 | 参数名固定为 `docIds`（非 `file_ids` 或 `documentIds`），传错将触发 `Index.InvalidParameter` 错误 [原文标题](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md) |
| `search_filters` | 检索接口（`/retrieve`, `/knowledge/search`） | object | 文档/元数据过滤条件 | 支持 `_operator: "OR"` 与嵌套 `_conditions` 表达同一字段多值 OR 条件，语法详见 [知识库 SearchFilters](../more/how-to-use-search-filters.md) [原文标题](../../raw/application-api-reference/rag-api/rag-api-overview.md) |
| `stream` | 知识问答（`/knowledge/chat`） | boolean | 是否启用 SSE 流式响应 | **必须为 `true`**，当前版本不支持非流式调用，否则请求失败 [原文标题](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md) |
| `kb_search_configs` | 知识检索（`/knowledge/search`） | array<object> | 每个知识库的独立过滤与权重配置 | 元素含 `id`（知识库 ID）、`weight`、`search_filters` 等，用于精细化控制多库联合检索行为 [原文标题](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md) |

## 使用方式

1. **认证与端点**：获取 API Key 后，构造 Base URL `https://{workspace_id}.cn-beijing.maas.aliyuncs.com`，所有请求头携带 `Authorization: Bearer <API-Key>`。  
2. **知识库生命周期**：  
   - 创建：调用 `/api/v1/indices/rag/index/create_v2`，指定 `name`、`structureType`、`sinkType`、`sourceType` 及 `docIds` 等；  
   - 查询列表：`GET /api/v1/indices/rag/index/list`（query 参数）；  
   - 更新：`POST /api/v1/indices/rag/index/update`，可修改 `name`、`description`、`rerankMinScore` 及 Wiki 配置；  
   - 删除：`POST /api/v1/indices/rag/index/delete`，传 `index_id`。  
3. **文档与切片管理**：  
   - 查询文档：`GET /api/v1/indices/rag/index/files?index_id=xxx`；  
   - 删除文档：`POST /api/v1/indices/rag/index/delete_file`，传 `index_id` 与 `doc_ids` 数组；  
   - 查询切片：`POST /api/v1/indices/rag/index/chunklist`，传 `indexId`；  
   - 新增/更新/删除切片：分别调用 `/chunk/create`、`/chunk/update`、`/chunk/delete`，注意 `pipelineId` 与 `chunkId` 字段命名。  
4. **数据导入**：  
   - 先创建类目（`/connector/dash/addCategory`）与数据集（`/connector/dash/addConnector`）；  
   - 上传文件三步走：申请租约（`/applyFileUploadLease`，`sizeBytes` 必须为字符串）→ OSS PUT → 注册文件（`/addFile`，`category` 字段名非 `categoryId`）；  
   - 追加导入：`POST /api/v1/indices/rag/index/job/create`，传 `indexId` 与 `docIds` 或 `categoryIds`。  
5. **知识检索与问答**：  
   - 检索：`POST /api/v1/indices/knowledge/search`，传 `agent_id`、`query`/`images` 及可选 `kb_search_configs`；  
   - 问答：`POST /api/v2/apps/knowledge/chat`，`stream=true`，`input.messages` 为标准 DashScope 格式，`parameters.agent_options.session_files` 支持临时文件。

## 限制和注意事项

- **限流规则**：知识库管理接口按 QPS 限流（如 `/rag/index/retrieve` 为 2000 QPS），知识检索与问答接口按“每 10 秒请求数”限流（默认 10 次/10 秒）[原文标题](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)。超限返回 HTTP `429`，错误码 `RATE_LIMITED` 或 `THROTTLING.pipelineQPSLimit`。  
- **参数命名不一致**：`index_id`（snake_case）用于删除知识库、查询文档列表等接口；`indexId`（camelCase）用于查询切片、提交导入任务等接口；`pipelineId` 用于新增/更新切片。开发者需严格按接口文档要求传参，否则触发 `Index.InvalidParameter`。  
- **幂等性与不可逆操作**：  
  - 删除知识库、删除文档、删除切片、删除类目、删除文件均为**永久性、不可逆操作**，无回收站机制；  
  - `delete` 类接口（Agent、类目、文件）设计为幂等，重复调用不报错；  
  - `addChunk` 接口具有幂等性，但频繁调用会触发限流（≤10 次/秒）。  
- **时间戳格式**：监控接口 `/api/v1/indices/rag/index/monitor` 要求 `startTimestamp`/`endTimestamp` 为**秒级 Unix 时间戳**（字符串或整数均可），非毫秒，务必校验 [原文标题](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)。  
- **错误处理**：所有错误响应统一为 JSON 结构，含 `error.code`（如 `KB_NOT_FOUND`、`RETRIEVAL_TIMEOUT`）与 `error.message`；`RETRIEVAL_TIMEOUT` 建议降低 `top_k` 或切换更小重排模型 [原文标题](../../raw/application-api-reference/rag-api/rag-api-errors.md)。

## 来源文档

- [概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)
- [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)
- [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)
- [Knowledge（原RAG） API 错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)
- [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)
- [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md)
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
- [新增切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-add-chunk.md)
- [更新切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-update-chunk.md)
- [删除切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-delete-chunk.md)
- [同步任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs.md)
- [提交导入任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-submit-sync-job.md)
- [查询任务状态](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-get-sync-job-status.md)
- [数据导入](../../raw/application-api-reference/rag-api/rag-api-data-import.md)
- [新增类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-category.md)
- [删除类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-category.md)
- [查询文件列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-file.md)
- [查询文件详情](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-describe-file.md)
- [批量更新文件标签](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-batch-update-tag.md)
- [删除文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-file.md)
- [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)
- [注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)
- [从 OSS 批量导入](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-oss-import.md)
- [查询数据集](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-get-connector.md)
- [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)
- [查询类目列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-category.md)
- [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)
- [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md)
- [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)
- [新增数据集](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-connector.md)
- [创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)
- [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)
- [发布 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-deploy.md)
- [删除 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-delete.md)
- [查询 Agent 列表](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-list.md)
- [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)
- [复制 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-copy.md)
- [查询 Agent 详情](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-get.md)


