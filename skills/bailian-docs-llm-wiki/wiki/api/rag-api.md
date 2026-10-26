# rag api

RAG API 是百炼平台提供的知识库管理与检索服务接口，支持开发者以编程方式完成知识库生命周期管理、文档导入、切片操作、联合语义检索及基于知识的智能问答。所有接口均通过 DashScope 网关统一提供，采用标准 RESTful 设计，以业务空间（`workspace_id`）为隔离单元，依赖 API Key 进行鉴权。

## 支持的模型/功能

RAG API 提供三类核心能力：**知识库管理**（含 CRUD、监控）、**数据导入**（含类目/文件/连接器全链路操作）和**知识检索与问答**（运行时服务）。  
- **知识库管理**：支持 `unstructured`（文档搜索、音视频搜索、图片问答）和 `structured`（数据查询）两类结构；嵌入模型（如 `text-embedding-v4`）、重排序模型（如 `qwen3-rerank`）及多模态模型（如 `qwen3-vl-embedding`）均可在创建或更新知识库时指定 [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。  
- **知识检索**：通过 `/api/v1/indices/knowledge/search` 接口实现跨知识库联合检索，支持文本+图片多模态输入，并可通过 `kb_search_configs` 动态传入 per-kb 过滤条件 [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)。  
- **知识问答**：通过 `/api/v2/apps/knowledge/chat` 提供 SSE 流式问答，严格要求 `stream=true`，响应按规划→工具调用→生成三阶段输出 [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)。  
> **注意**：文档 35 和文档 36 均指出知识检索接口路径为 `/api/v1/indices/knowledge/search`，但文档 35 中示例路径写为 `/api/v1/indices/knowledge/search`（正确），而文档 36 的“请求语法”区块中误写为 `/api/v1/indices/knowledge/search HTTP/1.1`（多出协议头），应以实际接口定义为准。

## 关键参数

- **通用参数**：所有接口需携带 `Authorization: Bearer <API-Key>` 头，Base URL 为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com`，其中 `{workspace_id}` 需从控制台获取 [概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)。  
- **知识库 ID 命名不一致**：多个接口对知识库 ID 的参数名不同——`/rag/index/update` 要求 `id`，`/rag/index/files` 要求 `index_id`，`/rag/list/index/file/details` 要求 `indexId`，`/rag/index/chunklist` 要求 `indexId`，`/rag/index/job/create` 要求 `indexId`，`/rag/index/delete_file` 要求 `index_id`。开发者需严格按各接口文档使用对应参数名，否则返回 `Index.InvalidParameter` 错误 [更新知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)。  
- **文件/切片 ID 参数名差异**：`/rag/index/delete_file` 使用 `doc_ids`（snake_case），而 `/rag/index/chunk/delete` 使用 `chunkIds`（camelCase），`/rag/index/create_v2` 使用 `docIds`（camelCase）[删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)。  
- **时间戳格式**：`/rag/index/monitor` 接口明确要求 `startTimestamp`/`endTimestamp` 为**秒级** Unix 时间戳（字符串或整数均可），与其他多数接口的毫秒级时间戳不同 [获取知识库监控数据](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)。

## 使用方式

1. **认证**：在控制台 [API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建并复制 API Key，通过 `Authorization` Header 传递。RAM 子账号需被授予 `AliyunBailianDataFullAccess` 权限并加入目标业务空间 [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)。  
2. **知识库工作流**：  
   - 先调用 `/api/v1/connector/dash/listCategory` 获取类目 ID；  
   - 再调用 `/api/v1/indices/rag/index/create_v2` 创建知识库并导入（传 `docIds`）；  
   - 后续可调用 `/api/v1/indices/rag/index/job/create` 追加导入；  
   - 检索前需确保知识库已发布（状态为 `FINISH`），可通过 `/api/v1/indices/rag/index_job/status` 查询任务状态 [提交导入任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-submit-sync-job.md)。  
3. **Agent 工作流**（检索/问答前置）：  
   - 先用管理 API（如 `/app/create`）创建 Agent 并配置 `kb_search_configs`；  
   - 调用 `/app/deploy` 发布 Agent，获取 `agent_id`；  
   - 最后用运行时 API（`/knowledge/search` 或 `/knowledge/chat`）传入该 `agent_id` 发起请求 [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)。  
4. **错误处理**：所有错误响应含 `request_id`，联系支持时必须提供；HTTP 429（限流）需按 `Retry-After` 头或指数退避重试；5xx 错误建议最多重试 3 次 [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)。

## 限制和注意事项

- **限流**：知识库管理接口中，`/rag/index/retrieve`（检索）QPS 上限为 2000，而 `/rag/index/monitor`（监控）仅为 1；数据导入接口 `/describeFile` QPS 为 10 [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)。  
- **不可逆操作**：`/rag/index/delete`（删除知识库）、`/rag/index/delete_file`（删除文档）、`/rag/index/chunk/delete`（删除切片）、`/connector/dash/deleteCategory`（删除类目）均为软/硬删除且**不可恢复**，调用前须二次确认 [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)。  
- **参数静默忽略**：`/connector/dash/listCategory` 和 `/connector/dash/listFile` 接口若传入 `maxResults`（复数）而非 `maxResult`（单数），参数会被静默忽略，导致分页异常 [查询类目列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-category.md)。  
- **文件上传特殊要求**：`/connector/dash/applyFileUploadLease` 要求 `sizeBytes` 必须传**字符串**（如 `"1048576"`），传数字会失败；`/connector/dash/addFile` 的类目参数名为 `category`（非 `categoryId`），与 `listFile` 接口不一致 [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)。

## 来源文档

- [概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)
- [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)
- [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)
- [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)
- [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md)
- [查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)
- [更新知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)
- [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)
- [文档管理](../../raw/application-api-reference/rag-api/rag-api-documents.md)
- [查询文档列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-documents.md)
- [查询文件详情列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-file-details.md)
- [获取知识库监控数据](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)
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
- [查询类目列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-category.md)
- [删除类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-category.md)
- [新增类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-category.md)
- [查询文件详情](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-describe-file.md)
- [查询文件列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-file.md)
- [删除文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-file.md)
- [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)
- [批量更新文件标签](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-batch-update-tag.md)
- [注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)
- [从 OSS 批量导入](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-oss-import.md)
- [查询连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-get-connector.md)
- [新增连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-connector.md)
- [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)
- [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)
- [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md)
- [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)
- [创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)
- [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)
- [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)
- [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)
- [发布 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-deploy.md)
- [删除 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-delete.md)
- [查询 Agent 列表](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-list.md)
- [复制 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-copy.md)
- [查询 Agent 详情](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-get.md)


