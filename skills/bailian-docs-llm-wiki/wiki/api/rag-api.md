# rag api

RAG API 是阿里云百炼平台提供的面向知识库构建与应用的编程接口，覆盖知识库管理、数据导入、切片操作、检索与问答全链路。所有接口通过统一的业务空间 Endpoint 提供服务，采用 API Key 鉴权，请求与响应均为 UTF-8 编码的 JSON 格式。开发者可通过该 API 实现知识库的自动化创建、文档批量处理、策略化检索及流式问答集成。

## 支持的模型/功能

RAG API 支持多模态与文本混合的知识处理能力，核心功能分为三类：

- **知识库管理**：支持 `unstructured`（非结构化文档）、`structured`（结构化表格）两类结构类型；知识库类型包括 `document`（文档搜索）、`table`（数据查询）、`image`（图片问答）、`multimedia`（音视频搜索）。不同场景需匹配对应向量模型：基础文档问答默认使用 `text-embedding-v3`，但可显式指定 `text-embedding-v4` 或 `qwen3.7-text-embedding`；视觉类场景（如 `visual_perception_qa`）必须传入 `multimodalEmbeddingModelName`（如 `qwen3-vl-embedding`）[原文标题](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。
- **知识检索与问答**：提供两个独立运行时服务：
  - `/api/v1/indices/knowledge/search`：跨知识库联合语义检索，依赖预发布的「知识检索服务」（Agent），其策略（多库权重、路由、混排等）在控制台或通过 Agent 管理 API 配置 [原文标题](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)；
  - `/api/v2/apps/knowledge/chat`：基于知识库的流式问答，强制要求 `stream=true`，响应按规划→工具调用→生成三阶段 SSE 输出，且不维护会话状态，需由客户端传入完整 `messages` 历史 [原文标题](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)。
- **Agent 全生命周期管理**：通过 `/api/v1/indices/rag/app/` 前缀接口实现 Agent 的创建、配置更新、发布、复制与删除。Agent 是检索与问答服务的运行实体，其 `agent_config` 承载全部策略，仅允许修改 `beta` 草稿版本；已发布版本仅能更新描述，如需变更配置须先更新草稿再重新发布 [原文标题](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)。

> **注意**：文档 5 中 `knowledgeScene` 列出的 `lite_document_qa` 场景要求 `sinkType=BUILT_IN`，而文档 6 的响应示例中 `rerankModelName` 返回 `qwen3-rerank`，但文档 37 未明确说明该重排模型是否支持 `lite_document_qa`。实际使用时请以控制台发布的 Agent 配置为准，避免硬编码模型名。

## 关键参数

- **认证与路由**：所有请求必须携带 `Authorization: Bearer <API-Key>` 头，并使用形如 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com` 的 Base URL，其中 `{workspace_id}` 为业务空间 ID（如 `llm-xxxxxxxxxxxx`）[原文标题](../../raw/application-api-reference/rag-api/rag-api-overview.md)。
- **知识库标识**：参数命名存在不一致。知识库 ID 在多数接口中为 `indexId`（camelCase），但在 `delete_file` 和 `delete_index` 接口中为 `index_id`（snake_case）；切片相关接口则使用 `pipelineId`；文档列表查询使用 `index_id`。务必严格按各接口文档要求传参，错误命名将导致 `Index.InvalidParameter` 错误 [原文标题](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)。
- **文件与类目关联**：数据导入环节存在关键字段名差异：`applyFileUploadLease` 和 `addFile` 接口的类目 ID 参数名为 `category`，而 `listFile`、`addFilesFromAuthorizedOss` 等接口使用 `categoryId`。混淆将导致 400 错误 [原文标题](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)。
- **分页与过滤**：分页参数命名不统一：知识库列表（`/list`）和文档列表（`/files`）使用 `page_number`/`page_size`（snake_case），而文件详情列表（`/list/index/file/details`）使用 `pageNumber`/`pageSize`（camelCase）[原文标题](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-file-details.md)。

## 使用方式

1. **准备凭证**：在百炼控制台 [API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 获取 API Key，并确认 RAM 子账号已获得 `AliyunBailianDataFullAccess` 权限且加入目标业务空间 [原文标题](../../raw/application-api-reference/rag-api/rag-api-authentication.md)。
2. **构建知识库**：
   - 若需一步完成创建与导入，调用 `/api/v1/indices/rag/index/create_v2`，注意 `sourceType` 决定必填参数分支（如 `DATA_CENTER_FILE` 必须传 `docIds`）；
   - 若需分步控制，先调用 `/api/v1/indices/rag/index/create` 创建空知识库，再通过 `/api/v1/indices/rag/index/job/create` 追加导入。
3. **管理数据源**：使用 `/api/v1/connector/dash/` 前缀接口管理类目、文件与数据集。上传文件需三步：`applyFileUploadLease` → OSS PUT → `addFile`；批量导入 OSS 文件前需确保已创建 `AliyunServiceRoleForBailian` 服务关联角色 [原文标题](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)。
4. **启用检索/问答**：
   - 先通过 Agent 管理 API（如 `/app/create` + `/app/deploy`）创建并发布检索或问答 Agent，获取 `agent_id`；
   - 调用 `/api/v1/indices/knowledge/search` 或 `/api/v2/apps/knowledge/chat`，传入 `agent_id` 及意图（`query`/`images` 或 `input.messages`）。

## 限制和注意事项

- **限流规则**：知识库管理接口按 QPS 限流（如 `/retrieve` 为 2000 QPS），而知识检索与问答接口按“每 10 秒请求数”限流（默认 10 次/10 秒）。超限时返回 HTTP `429`，建议实现指数退避重试 [原文标题](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)。
- **不可逆操作**：`delete_index`、`delete_file`、`deleteCategory`、`deleteFile` 等接口均不可逆，删除后数据无法恢复。调用前务必确认目标资源无业务依赖 [原文标题](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)。
- **参数校验陷阱**：
  - `create_v2` 接口校验失败时错误信息中的参数名为 `file_ids`，但实际请求体字段应为 `docIds`；
  - `listCategory` 接口的分页参数为 `maxResult`（单数），传 `maxResults` 将被静默忽略；
  - `applyFileUploadLease` 的 `sizeBytes` 必须以字符串格式传入（如 `"1048576"`），传数字将失败。
- **时间戳格式**：`/monitor` 接口的 `startTimestamp`/`endTimestamp` 为**秒级** Unix 时间戳（非毫秒），而其他接口（如 `/list-chunks` 响应中的 `gmt_modified`）为毫秒级，需注意单位转换 [原文标题](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)。

## 来源文档

- [概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)
- [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)
- [RAG API 错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)
- [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md)
- [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)
- [查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)
- [更新知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)
- [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)
- [获取知识库监控数据](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)
- [文档管理](../../raw/application-api-reference/rag-api/rag-api-documents.md)
- [查询文档列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-documents.md)
- [删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)
- [切片管理](../../raw/application-api-reference/rag-api/rag-api-chunks.md)
- [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)
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
- [查询文件详情列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-file-details.md)
- [删除文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-file.md)
- [新增切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-add-chunk.md)
- [查询文件详情](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-describe-file.md)
- [批量更新文件标签](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-batch-update-tag.md)
- [注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)
- [从 OSS 批量导入](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-oss-import.md)
- [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)
- [新增数据集](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-connector.md)
- [查询数据集](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-get-connector.md)
- [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)
- [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)
- [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md)
- [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)
- [创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)
- [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)
- [删除 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-delete.md)
- [发布 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-deploy.md)
- [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)
- [查询 Agent 详情](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-get.md)
- [复制 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-copy.md)
- [查询 Agent 列表](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-list.md)


