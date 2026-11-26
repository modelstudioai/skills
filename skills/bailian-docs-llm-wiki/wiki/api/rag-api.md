# rag api

RAG API 是百炼平台提供的知识库管理与检索服务接口，统一通过 Knowledge API（原 RAG API）提供。它支持知识库全生命周期管理、文档与切片操作、数据源导入、跨库联合检索及智能问答等核心能力，所有接口均基于 HTTPS 协议，采用 JSON 格式通信，并通过 API Key 鉴权。服务地址以业务空间 ID（`{workspace_id}`）为子域名，路径按功能分组，开发者需先完成[认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)并确认权限配置。

## 支持的模型/功能

RAG API 不直接暴露大模型调用，而是通过预置模型能力支撑上层功能：
- **嵌入模型**：支持 `text-embedding-v3`、`text-embedding-v4`、`qwen3.7-text-embedding` 等，用于知识库向量化（见[创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)）；
- **重排序模型**：支持 `qwen3-rerank` 等，用于检索后结果精排（见[查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)响应字段 `rerankModelName`）；
- **Wiki 抽取模型**：支持 `qwen3.8-flash`、`qwen3.8-max`、`qwen3.7-plus`，仅限旗舰版知识库开启 Wiki 时使用（见[更新知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)中 Wiki 配置参数）；
- **Agent 模型**：知识问答/检索 Agent 可配置 `qwen3.7-plus`、`qwen3.6-plus` 等模型（见[创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)请求体说明）。

> **注意**：文档 7 中 `embeddingModelName` 示例包含 `qwen3.7-text-embedding`，而文档 5 的示例响应中 `embeddingModelName` 为 `text-embedding-v4`，两者均为有效值；但文档 7 提到“基础文档问答未传时默认为 `text-emb...`”存在截断，实际默认值应以控制台最新文档或接口返回为准，建议显式指定。

## 关键参数

- **通用参数**：所有请求必须携带 `Authorization: Bearer <API-Key>` 头，`API-Key` 从[控制台 API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key)获取；Base URL 为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com`，其中 `{workspace_id}` 在[业务空间管理](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)中查看。
- **命名不一致问题**：多个接口存在参数命名风格混用：
  - 知识库管理类接口（如 `/rag/index/delete`）使用 `snake_case`（`index_id`），而切片管理类（如 `/rag/index/chunklist`）使用 `camelCase`（`indexId`）；
  - 文档删除接口明确警告：“参数缺失时服务端返回的 `Required parameter(IndexId) missing`，其中 `IndexId` 是服务端内部字段名，**不是**请求参数名，请仍按 `index_id` 传参”（见[删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)）；
  - 数据导入类接口（如 `/connector/dash/addFile`）中类目 ID 参数名为 `category`，而非 `categoryId`（见[注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)）。
- **特殊格式要求**：
  - 时间戳：`/rag/index/monitor` 接口要求 `startTimestamp`/`endTimestamp` 为**秒级 Unix 时间戳**（字符串或整数均可），非毫秒（见[获取知识库监控数据](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)）；
  - 文件大小：`/connector/dash/applyFileUploadLease` 要求 `sizeBytes` 必须以**字符串格式**传入（如 `"1048576"`），不能传数字（见[申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)）。

## 使用方式

1. **准备凭证**：获取 API Key 和业务空间 ID，按[认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)文档配置 `Authorization` Header；
2. **管理知识库**：使用 `/api/v1/indices/rag/index/` 前缀接口，例如：
   - 创建：`POST /create_v2`（支持一步创建+导入）；
   - 查询列表：`GET /list`（query string 传参）；
   - 更新：`POST /update`（可开关 Wiki 并配置抽取模型）；
3. **管理数据源**：使用 `/api/v1/connector/dash/` 前缀接口，例如：
   - 创建类目：`POST /addCategory`；
   - 上传文件：三步流程（`applyFileUploadLease` → OSS PUT → `addFile`）；
   - OSS 批量导入：`POST /addFilesFromAuthorizedOss`（需提前授权 SLR 角色）；
4. **运行时调用**：
   - **知识检索**：`POST /api/v1/indices/knowledge/search`，需先在控制台创建并发布[知识检索服务](../../../application-user-guide/agent-context/knowledge-base/service/rag-knowledge-retrieval.md)，传入 `agent_id` 和 `query`/`images`；
   - **知识问答**：`POST /api/v2/apps/knowledge/chat`，SSE 流式，`stream` 必须为 `true`，需传完整 `messages` 历史（见[知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)）；
5. **Agent 全生命周期管理**：使用 `/api/v1/indices/rag/app/` 前缀接口，先 `create` → `update`（beta 配置）→ `deploy`（获取 `agent_id`）→ 再调用运行时 API（见[Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)）。

## 限制和注意事项

- **限流规则**：知识库管理接口按 QPS 限流（如 `/rag/index/retrieve` 为 2000 QPS），知识检索与问答接口按每 10 秒请求数限流（如知识检索默认 10 次/10 秒）（见[限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)）；超限返回 HTTP `429` 及错误码 `RATE_LIMITED` 或 `THROTTLING.pipelineQPSLimit`。
- **不可逆操作**：删除知识库（`/delete`）、删除文档（`/delete_file`）、删除切片（`/chunk/delete`）、删除类目（`/deleteCategory`）均为**永久删除且不可恢复**，调用前务必确认（见[删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)、[删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)等）。
- **参数校验陷阱**：
  - `create_v2` 接口要求文件 ID 参数名为 `docIds`，但错误信息中提示为 `file_ids`（见[创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)）；
  - `delete_file` 接口严格区分 `index_id`（snake_case），传 `IndexId` 或 `indexId` 会返回 `Index.InvalidParameter`（见[删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)）；
- **Wiki 功能约束**：开启 Wiki 要求知识库为旗舰版（`enterprise`）且知识场景为 `basic_document_qa`；降配为标准版时若已开启 Wiki，将触发 `WikiEditionNotSupported` 错误（见[Knowledge（原RAG） API 错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)）。
- **错误处理**：所有错误响应结构统一，含 `error.code`（如 `INVALID_PARAMETER`）、`error.message` 和 `request_id`，便于排查（见[错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)）。

## 来源文档

- [概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)
- [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)
- [Knowledge（原RAG） API 错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)
- [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)
- [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md)
- [查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)
- [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)
- [更新知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)
- [获取知识库监控数据](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)
- [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)
- [文档管理](../../raw/application-api-reference/rag-api/rag-api-documents.md)
- [查询文档列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-documents.md)
- [查询文件详情列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-file-details.md)
- [删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)
- [切片管理](../../raw/application-api-reference/rag-api/rag-api-chunks.md)
- [新增切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-add-chunk.md)
- [查询切片列表](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-list-chunks.md)
- [删除切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-delete-chunk.md)
- [更新切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-update-chunk.md)
- [提交导入任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-submit-sync-job.md)
- [同步任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs.md)
- [查询任务状态](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-get-sync-job-status.md)
- [数据导入](../../raw/application-api-reference/rag-api/rag-api-data-import.md)
- [查询类目列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-category.md)
- [新增类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-category.md)
- [查询文件列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-file.md)
- [查询文件详情](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-describe-file.md)
- [删除类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-category.md)
- [删除文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-file.md)
- [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)
- [批量更新文件标签](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-batch-update-tag.md)
- [注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)
- [新增数据集](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-connector.md)
- [从 OSS 批量导入](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-oss-import.md)
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
- [查询数据集](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-get-connector.md)
- [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)


