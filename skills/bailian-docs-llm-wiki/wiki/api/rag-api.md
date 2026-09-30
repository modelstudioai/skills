# rag api

RAG API 是百炼平台提供的知识库管理与增强问答服务接口集合，支持知识库全生命周期管理、文档导入、切片操作、跨库检索及基于知识的智能问答。所有接口均通过 DashScope 网关统一接入，采用 RESTful 设计，以业务空间（workspace_id）为租户隔离单元。

## 支持的模型/功能

RAG API 提供三类核心能力：**知识库管理**（创建、更新、删除、监控）、**数据导入与文档管理**（类目/文件/连接器操作、OSS 批量导入）、**知识检索与问答**（联合语义检索、SSE 流式问答）。  
- **知识库类型**支持 `document`（文档搜索）、`table`（数据查询）、`image`（图片问答）、`multimedia`（音视频搜索），需与 `structureType`（`unstructured`/`structured`）匹配 [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。  
- **检索与问答**依赖预发布的 Agent 实体：知识检索调用 `/api/v1/indices/knowledge/search`，知识问答调用 `/api/v2/apps/knowledge/chat`，二者均需传入控制台生成的 `agent_id` [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md) 和 [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)。  
- **Agent 管理**提供全生命周期 API（创建、更新、发布、删除、复制），`agent_config` 封装模型、策略、路由等配置，是运行时 API 的前置依赖 [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)。

> **注意**：文档 6 中 `knowledgeScene` 列出的 `visual_document_qa` 场景在控制台已下线，但 API 仍接受该值；实际部署建议优先使用 `basic_document_qa` 或 `lite_document_qa`。

## 关键参数

- **认证**：所有请求必须携带 `Authorization: Bearer <API-Key>` 头，API Key 在控制台 [API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 获取 [认证方式](../../raw/application-api-reference/rag-api/rag-api-authentication.md)。  
- **Endpoint**：Base URL 格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com`，`{workspace_id}` 如 `llm-xxxxxxxxxxxx`，在[业务空间管理](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)中查看 [API 概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)。  
- **参数命名不一致**：部分接口使用 snake_case（如 `index_id`, `doc_ids`），部分使用 camelCase（如 `indexId`, `pageNumber`），需严格按各接口文档要求传参。例如删除文档必须用 `index_id`，而查询切片列表必须用 `indexId` [删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md) 和 [查询切片列表](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-list-chunks.md)。  
- **文件上传特殊要求**：申请 OSS 上传租约时，`sizeBytes` 必须以字符串格式传入（如 `"1048576"`），传数字将失败 [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)。

## 使用方式

1. **初始化**：获取 `workspace_id` 和 `API Key`，构造 Base URL。  
2. **构建知识库**：  
   - 先通过数据导入接口（如 `addCategory`, `addFile`）准备文件 [数据导入](../../raw/application-api-reference/rag-api/rag-api-data-import.md)；  
   - 再调用 `/api/v1/indices/rag/index/create_v2` 创建知识库并导入 [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。  
3. **管理内容**：使用 `/api/v1/indices/rag/index/chunk/*` 接口增删改查切片 [切片管理](../../raw/application-api-reference/rag-api/rag-api-chunks.md)。  
4. **发布服务能力**：  
   - 调用 Agent 管理 API 创建并发布 `search` 或 `chat` 场景的 Agent，获取 `agent_id`；  
   - 最后调用 `/api/v1/indices/knowledge/search` 或 `/api/v2/apps/knowledge/chat` 发起运行时请求。  
5. **错误处理**：所有响应含 `request_id`，用于问题排查；HTTP 429 需按 `Retry-After` 头或指数退避重试 [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)。

## 限制和注意事项

- **限流**：知识库管理接口 QPS 差异大，如检索接口上限 2000 QPS，而监控接口仅 1 QPS；知识检索与问答默认用户维度 25 QPS [限流策略](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)。  
- **不可逆操作**：删除知识库、文档、类目、文件均为永久删除，无回收站 [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)、[删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)、[删除类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-category.md)、[删除文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-file.md)。  
- **幂等性与并发**：新增切片接口具有幂等性；Agent 发布支持并发安全，底层通过 DB 唯一索引 + 冲突重试保障 [新增切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-add-chunk.md) 和 [发布 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-deploy.md)。  
- **参数校验陷阱**：`create_v2` 接口请求体字段 `docIds` 与错误提示中的 `file_ids` 不一致；`applyFileUploadLease` 的 `category` 字段名非 `categoryId` [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md) 和 [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)。

## 来源文档

- [API 概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)
- [认证方式](../../raw/application-api-reference/rag-api/rag-api-authentication.md)
- [限流策略](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)
- [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md)
- [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)
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
- [查询切片列表](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-list-chunks.md)
- [更新切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-update-chunk.md)
- [删除切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-delete-chunk.md)
- [同步任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs.md)
- [提交导入任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-submit-sync-job.md)
- [查询任务状态](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-get-sync-job-status.md)
- [数据导入](../../raw/application-api-reference/rag-api/rag-api-data-import.md)
- [查询类目列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-category.md)
- [查询文件列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-file.md)
- [新增类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-category.md)
- [删除类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-category.md)
- [删除文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-file.md)
- [查询文件详情](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-describe-file.md)
- [批量更新文件标签](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-batch-update-tag.md)
- [注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)
- [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)
- [从 OSS 批量导入](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-oss-import.md)
- [新增连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-connector.md)
- [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)
- [查询连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-get-connector.md)
- [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md)
- [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)
- [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)
- [创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)
- [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)
- [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)
- [发布 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-deploy.md)
- [删除 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-delete.md)
- [查询 Agent 列表](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-list.md)
- [复制 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-copy.md)
- [查询 Agent 详情](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-get.md)


