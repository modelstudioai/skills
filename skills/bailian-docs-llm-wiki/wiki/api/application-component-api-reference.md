# application component api reference

阿里云百炼（Bailian，OpenAPI 版本 `bailian/2023-12-29`）提供一套 ROA 风格的 OpenAPI，用于以编程方式管理数据连接（原应用数据）、Prompt 模板、[知识库](../concepts/knowledge-base.md)（RAG Index）以及记忆（Memory）等应用组件。这些接口覆盖从文件上传、解析配置、[知识库](../concepts/knowledge-base.md)构建到检索召回的完整链路，是控制台能力背后的程序化入口，建议通过官方多语言 SDK 调用以免去自签名负担（[API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)）。

## 接入与鉴权

### 服务接入点

百炼 OpenAPI 当前在亚太区域提供两个服务接入点：华北2（北京，`cn-beijing`）和新加坡（`ap-southeast-1`），均提供公网接入地址与 VPC 接入地址。例如北京公网为 `bailian.cn-beijing.aliyuncs.com`，对应 VPC 地址为 `bailian-vpc.cn-beijing.aliyuncs.com`（[服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)）。

### 签名与 SDK

OpenAPI 采用 ROA 签名风格，官方已封装多语言 SDK，开发者可直接调用而无需关心签名细节。仅在特殊业务场景下才考虑自签名对接，该过程复杂（约需 5 个工作日），建议先通过服务钉钉群（147535001692）咨询技术支持。调用前需准备阿里云账号或 RAM 用户的 AccessKey（[API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)）。

### RAM 授权

百炼的 RAM 代码（RamCode）为 `sfm`，授权粒度为**操作级**。所有操作的资源类型均为「全部资源」（不支持资源级授权），权限策略通过 `Action`（如 `sfm:ListCategory`、`sfm:CreateIndex`）描述授权内容。RAM 用户（子账号）调用各接口前需：

1. 获取百炼 API 权限（授予 `AliyunBailianDataFullAccess` 策略，包含所需权限点；只读场景可用 `AliyunBailianDataReadOnlyAccess`）；
2. 加入对应[业务空间](../concepts/workspace.md)。

阿里云主账号默认拥有全部权限，可直接调用。建议遵循最小权限原则（PoLP）创建专用 RAM 用户，避免直接使用主账号 AccessKey（[授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)）。

### 公共路径参数

几乎所有接口的路径或请求参数中都包含 `WorkspaceId`（[业务空间](../concepts/workspace.md) ID），用于隔离不同[业务空间](../concepts/workspace.md)的资源。该 ID 可在百炼控制台首页左上角业务空间详情中获取。路径中的资源 ID（如 `CategoryId`、`FileId`、`IndexId`、`ConnectorId`）通常由对应创建接口返回，也可在控制台对应页签单击名称旁的 ID 图标获取。

## 数据连接（原应用数据）

数据连接用于在业务空间内分类、上传、解析和管理文件，是构建[知识库](../concepts/knowledge-base.md)的前置数据源。每业务空间最多创建 500 个类目；类目类型目前仅支持 `UNSTRUCTURED`（非结构化类目），数据表（表格）相关操作暂不支持通过 API 完成新增/查询/删除，需走控制台。

### 类目管理

| 接口 | 方法与路径 | 说明 |
| --- | --- | --- |
| AddCategory | `POST /{WorkspaceId}/datacenter/category/` | 新增类目，类目名 1~20 字符；非幂等；5 次/秒 |
| ListCategory | `POST /{WorkspaceId}/datacenter/categories` | 类目列表，支持 `NextToken`+`MaxResults` 分页；幂等；5 次/秒 |
| DeleteCategory | `DELETE /{WorkspaceId}/datacenter/category/{CategoryId}/` | 永久删除类目；幂等；5 次/秒 |

### 文件上传与导入

文件入库的标准流程是「申请上传租约 → 上传到临时存储 → AddFile 导入数据连接」。也可从已授权 OSS Bucket 批量导入。

- **ApplyFileUploadLease**（`POST /{WorkspaceId}/datacenter/category/{CategoryId}`）：申请上传租约，返回 `FileUploadLeaseId`。用于知识库文件时传入目标类目 ID（允许 `default`）；用于智能体会话交互文件时传 `default`。10 次/秒，非幂等。
- **AddFile**（`PUT /{WorkspaceId}/datacenter/file`）：将临时存储中的文件导入数据连接，需传入 `LeaseId` 与 `Parser`（解析器类型）。解析器取值包括 `DOCMIND`（智能文档解析）、`DOCMIND_DIGITAL`（电子文档解析）、`DOCMIND_LLM_VERSION`（大模型文档解析）、`DASH_QWEN_VL_PARSER`（Qwen VL 解析）、`DOCMIND_LLM_VERSION_MEDIA`（音视频解析）、`AUTO_SELECT`（自动选择）。10 次/秒，非幂等。
- **AddFilesFromAuthorizedOss**（`POST /{WorkspaceId}/datacenter/file/fromoss`）：从已授权 OSS Bucket 导入文件。Bucket 须与百炼同主账号并完成授权；不支持归档/冷归档/深度冷归档存储类型；支持内容加密与公共读写/公共读/私有 Bucket。开启 Referer 防盗链时须将 `*.console.aliyun.com` 加入白名单。5 次/秒，非幂等（[AddFilesFromAuthorizedOss - 从已授权OSS Bucket中导入文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addfilesfromauthorizedoss.md)）。

### 文件查询与标签

- **DescribeFile**（`GET /{WorkspaceId}/datacenter/file/{FileId}/`）：查询单个文件基本信息（名称、类型、状态等）；10 次/秒，幂等。
- **ListFile**（`GET /{WorkspaceId}/datacenter/files`）：列出类目下文件，`CategoryId` 必填，支持 `NextToken` 分页；5 次/秒，幂等。
- **UpdateFileTag**（`PUT /{WorkspaceId}/datacenter/file/{FileId}`）：更新单文件标签，最多 100 个标签、总长 ≤700 字符，每标签 ≤32 字符且不含空格；5 次/秒。
- **BatchUpdateFileTag**（`PUT /{WorkspaceId}/datacenter/batchupdatetag`）：批量更新标签，`UpdateMode` 支持 `APPEND`（追加）与 `OVERWRITE`（覆盖），返回每个文件的更新结果。
- **DeleteFile** / **DeleteFiles**：删除应用数据中的文件（不影响已构建知识库；删除知识库内文件须用 DeleteIndexDocument）。仅能删除状态为 `PARSE_FAILED` 或 `PARSE_SUCCESS` 的文件；批量删除单次最多 20 个；均 10 次/秒、幂等。

### 解析设置

- **GetParseSettings**（`GET /{WorkspaceId}/datacenter/parser/settings`）：查询类目下各文件类型的解析方式配置；10 次/秒，幂等。
- **GetAvailableParserTypes**（`GET /{WorkspaceId}/datacenter/parser/parsertype`）：按文件扩展名（doc/docx/ppt/pptx/xls/xlsx/md/txt/pdf/png/jpg/jpeg/bmp/gif/html 等）查询支持的解析器列表；10 次/秒，幂等。
- **ChangeParseSetting**（`PUT /{WorkspaceId}/datacenter/parser/settings`）：为类目内指定文件类型指定解析方式（如 .pdf 用大模型文档解析、.jpg 用 Qwen VL 解析）；10 次/秒，非幂等。

### 表格与连接器

- **AddTable**（`POST /{WorkspaceId}/datacenter/table`）：为表格数据连接器添加表格，需指定 `TableName`、`ConnectorId` 与 `TableColumns`（列名/列描述/数据类型）；10 次/秒，非幂等。
- **UpdateTableFromAuthorizedOss**（`PUT /{WorkspaceId}/datacenter/table/fromoss/{TableId}`）：用已授权 OSS Bucket 中的文件更新表格；5 次/秒，非幂等。
- **AddConnector**（`POST /{WorkspaceId}/datacenter/connector`）：创建连接器，**当前仅支持文件类型连接器**（`ConnectorType=FILE`），可配置自有 OSS（`OSS_CUSTOM`）或平台 OSS（`OSS_PLATFORM`）存储；5 次/秒，非幂等。
- **GetConnector**（`GET /{WorkspaceId}/datacenter/connector`）：按 `ConnectorName` 或 `ConnectorId` 查询连接器信息；5 次/秒，幂等。
- **UpdateConnector**（`PUT /{WorkspaceId}/datacenter/connector/{ConnectorId}`）：编辑连接器名称与描述；5 次/秒，非幂等。

> **注意**：AddConnector 接口说明中描述其权限点为 `sfm:AddCategory`，疑似文档错误，实际权限点应为 `sfm:AddConnector`（参见授权信息表中列出的是 `sfm:AddConnector`）。调用时以 RAM 策略 `AliyunBailianDataFullAccess` 为准。

## Prompt 模板

Prompt 模板用于沉淀可复用的提示词，支持变量占位（如 `${theme}`）。

| 接口 | 方法与路径 | 说明 |
| --- | --- | --- |
| CreatePromptTemplate | `POST /{workspaceId}/promptTemplates` | 创建模板，需 `name`+`content`；返回 `promptTemplateId`。**暂不支持文生图 Prompt 模板** |
| GetPromptTemplate | `GET /{workspaceId}/promptTemplates/{promptTemplateId}` | 获取模板，返回内容、变量列表等 |
| UpdatePromptTemplate | `PATCH /{workspaceId}/promptTemplates/{promptTemplateId}` | 增量更新，`name`/`content` 均可选 |
| DeletePromptTemplate | `DELETE /{workspaceId}/promptTemplates/{promptTemplateId}` | 删除模板 |
| ListPromptTemplates | `GET /{workspaceId}/promptTemplates` | 列表，支持按 `name` 关键字搜索、按 `type`（`System` 系统预置 / `Custom` 自定义）过滤，`maxResults`+`nextToken` 分页 |

错误码包括 `PromptTemplate.ContentInvalid`、`PromptTemplate.NameInvalid`、`PromptTemplate.TemplateNotFound`（404）、`PromptTemplate.InternalError`（500）。

## 知识库（RAG Index）

知识库将已解析的文件向量化并检索，是 RAG 应用的核心。支持两类：基于文档/音视频的**非结构化知识库**，以及用于数据查询/图片问答的**结构化知识库**。

### 创建与提交

知识库创建为两步式：先 CreateIndex 初始化作业并获得 `IndexId`，再 SubmitIndexJob 真正提交构建（否则得到空知识库）。

- **CreateIndex**（`POST /{WorkspaceId}/index/create`）：初始化知识库，`Name` 必填（1~20 字符）。非幂等，重复调用可能创建多个同名知识库，建议「先查后建」。10 次/秒。
- **SubmitIndexJob**（`POST /{WorkspaceId}/index/submit_index_job`）：提交 CreateIndex 任务完成创建，需 `IndexId`。任务执行需一定时间，高峰期可能数小时，完成前勿重复请求；用 GetIndexJobStatus 查状态。10 次/秒，非幂等（[SubmitIndexJob - 提交知识库创建任务](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-submitindexjob.md)）。
- **SubmitIndexAddDocumentsJob**（`POST /{WorkspaceId}/index/add_documents_to_index`）：向已有知识库追加已解析文件；调用前需先 AddFile 上传文件。**不支持数据查询/图片问答类知识库**。10 次/秒，非幂等。
- **GetIndexJobStatus**（`GET /{WorkspaceId}/index/job/status`）：查询创建/追加任务状态，需 `JobId`+`IndexId`。调用间隔建议 ≥5 秒；幂等。

> **注意**：GetIndexJobStatus 接口说明提示频繁调用会被限流，频率请勿高于 20 次/分钟（与常规的 10 次/秒不同）；而其他知识库接口多为 10 次/秒。轮询时务必控制节奏。

### 检索

- **Retrieve**（`POST /{WorkspaceId}/index/retrieve`）：在指定知识库中检索，`Query` 为原始输入文本（长度与字符无限制）。因含复杂检索与匹配，响应可能较长，需合理设置超时与重试。可通过百炼 SDK（配 AccessKey）或 Spring AI Alibaba（配 API-Key）调用。幂等。

### 知识库与文件管理

- **ListIndices**（`GET /{WorkspaceId}/index/list_indices`）：列出业务空间下知识库，支持 `IndexName` 查找、`PageNumber`/`PageSize` 分页；10 次/秒，幂等。
- **UpdateIndex**（`POST /{WorkspaceId}/index/update`）：更新知识库部分配置，如 `Name`、`Description`、`RerankMinScore`（0~1）、`DenseSimilarityTopK`（向量检索 TopK，0~100）、`SparseSimilarityTopK`（关键词检索 TopK，0~100，二者之和 ≤200）、`PipelineCommercialType`（`standard` 标准版 / `enterprise` 旗舰版）等；幂等。
- **DeleteIndex**（`POST /{WorkspaceId}/index/delete`）：永久删除知识库；若正被应用调用需先在控制台解除关联；不可逆，不影响应用数据中已导入文件；10 次/秒，幂等。
- **ListIndexDocuments**（`GET /{WorkspaceId}/index/list_index_documents`）：查询知识库下文件概要信息，`IndexId` 必填，可按 `DocumentStatus`（`INSERT_ERROR`/`RUNNING`/`DELETED`/`FINISH`）与 `DocumentName`（含 `EnableNameLike` 模糊匹配）过滤；15 次/秒，幂等。
- **ListIndexFileDetails**（`POST /{WorkspaceId}/index/list_index_file_detail`）：查询知识库下文件**详情**，过滤参数同上，`PageSize` 最大 10；幂等。
- **DeleteIndexDocument**（`POST /{WorkspaceId}/index/delete_index_document`）：删除知识库中文件，`DocumentIds` 为 `FileId` 列表。仅能删除状态为 `INSERT_ERROR` 或 `FINISH` 的文件；不可逆，删除后 Retrieve 无法再获取其内容；不影响应用数据中的原始文件；**不支持数据查询/图片问答类知识库**；10 次/秒，幂等。

### 切片管理

- **ListChunks**（`POST /{WorkspaceId}/index/list_chunks`）：查看文本切片列表。文档/音视频类知识库可查指定文件的所有切片；数据查询/图片问答类可获取全部文本切片信息。`Fields` 数组可对 Metadata 中非私有字段（非 `_` 前缀）做过滤。10 次/秒，幂等。
- **UpdateChunk**（`POST /{WorkspaceId}/chunk/update`）：修改切片的 `content` 与 `title`，并可设置是否参与检索；需 `PipelineId`（即知识库 ID）、`DataId`（文件 ID）、`ChunkId`（切片 ID，来自 ListChunks 返回的 `Node.Metadata._id`）。**仅支持文档搜索类知识库**。更新通常立即生效，高峰期秒级延迟；幂等；10 次/秒（[UpdateChunk - 修改切片](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-updatechunk.md)）。
- **DeleteChunk**：删除指定切片（接口在源文档列表中存在）。

## 记忆（Memory）

百炼提供记忆（Memory）相关接口，用于管理长期记忆库与记忆节点，支持智能体跨会话记忆能力。相关接口包括：

- **CreateMemory** / **GetMemory** / **UpdateMemory** / **DeleteMemory** / **ListMemories**：记忆库的增删改查。
- **CreateMemoryNode** / **GetMemoryNode** / **UpdateMemoryNode** / **DeleteMemoryNode** / **ListMemoryNodes**：记忆节点的增删改查。

> **注意**：本批次源文档未完整嵌入记忆类接口的请求/返回参数详情，调用前请以百炼官方 OpenAPI Explorer 的最新文档为准（参见 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md) 中的记忆段落）。

## 其他辅助接口

- **GetIndexMonitor**：查询知识库监控指标（2026-01-14 新增 OpenAPI）。
- **ApplyTempStorageLease**：申请临时存储租约。
- **GetAlipayTransferStatus** / **GetAlipayUrl**：涉及支付宝转账状态与支付链接的辅助接口。

## 版本变更要点

根据版本说明（[版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)），近期主要变更：

- 2026-03-30：`CreateIndex` 入参变更；`Retrieve` API 内部配置变更（不影响调用）。
- 2026-03-27：`CreateIndex` 入参变更。
- 2026-01-19：新增 `UpdateIndex` OpenAPI。
- 2026-01-15：`DescribeFile` 返回结构变更。
- 2026-01-14：新增 `GetIndexMonitor` OpenAPI。

## 通用注意事项

1. **幂等性差异**：查询类（List/Describe/Get）与删除类接口多为幂等；创建类（Add/Create/Submit/Apply）多为**非幂等**，重复调用会产生重复资源，需做好去重与「先查后建」逻辑。
2. **限流**：各接口限流频率不一（5/10/15 次/秒，GetIndexJobStatus 为 20 次/分钟），超频会被限流，应实现退避重试。
3. **资源 ID 来源**：`CategoryId`、`FileId`、`IndexId`、`ConnectorId`、`JobId`、`ChunkId` 等均由对应创建接口返回，也可在控制台对应页签获取。
4. **数据表限制**：API 暂不支持数据表的新增/查询/删除，相关操作需走控制台。
5. **知识库与数据连接的关系**：DeleteFile/DeleteFiles 删除应用数据中的文件，不影响已构建的知识库；DeleteIndexDocument 删除知识库中的文件，不影响应用数据中的原始文件。
6. **结构化知识库限制**：SubmitIndexAddDocumentsJob、DeleteIndexDocument、UpdateChunk 均不支持数据查询/图片问答类知识库，需通过控制台或相应文档说明操作。

## 来源文档

- [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)
- [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)
- [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)
- [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)
- [ListCategory - 类目列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-listcategory.md)
- [AddCategory - 新增类目](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addcategory.md)
- [DeleteCategory - 删除类目](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-deletecategory.md)
- [ApplyFileUploadLease - 申请文件上传租约](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-applyfileuploadlease.md)
- [AddFile - 添加文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addfile.md)
- [AddFilesFromAuthorizedOss - 从已授权OSS Bucket中导入文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addfilesfromauthorizedoss.md)
- [DescribeFile - 查询文件状态](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-describefile.md)
- [ListFile - 文件列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-listfile.md)
- [UpdateFileTag - 更新文件标签](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-updatefiletag.md)
- [BatchUpdateFileTag - 批量更新文档标签](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-batchupdatefiletag.md)
- [DeleteFile - 删除文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-deletefile.md)
- [DeleteFiles - 批量删除文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-deletefiles.md)
- [GetParseSettings - 获取类目解析设置](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-getparsesettings.md)
- [GetAvailableParserTypes - 获取文件支持的解析器类型](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-getavailableparsertypes.md)
- [ChangeParseSetting - 修改类目解析设置](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-changeparsesetting.md)
- [AddTable - 添加表格](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addtable.md)
- [UpdateTableFromAuthorizedOss - 从已授权OSS Bucket中选择文件更新表格](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-updatetablefromauthorizedoss.md)
- [AddConnector - 新增连接器](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addconnector.md)
- [GetConnector - 获取连接器信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-getconnector.md)
- [UpdateConnector - 编辑连接器](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-updateconnector.md)
- [CreatePromptTemplate - 创建Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-createprompttemplate.md)
- [GetPromptTemplate - 获取Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-getprompttemplate.md)
- [UpdatePromptTemplate - 更新Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-updateprompttemplate.md)
- [DeletePromptTemplate - 删除Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-deleteprompttemplate.md)
- [ListPromptTemplates - 获取Prompt模板列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-listprompttemplates.md)
- [GetIndexJobStatus - 查询知识库创建任务状态](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-getindexjobstatus.md)
- [CreateIndex - 创建知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-createindex.md)
- [SubmitIndexJob - 提交知识库创建任务](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-submitindexjob.md)
- [SubmitIndexAddDocumentsJob - 提交知识库追加任务](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-submitindexadddocumentsjob.md)
- [Retrieve - 检索知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-retrieve.md)
- [ListIndexFileDetails - 查询知识库下的文件详情](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-listindexfiledetails.md)
- [ListIndexDocuments - 查询知识库下的文件列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-listindexdocuments.md)
- [DeleteIndexDocument - 删除知识库下的文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-deleteindexdocument.md)
- [UpdateIndex - 更新知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-updateindex.md)
- [ListIndices - 查询知识库列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-listindices.md)
- [DeleteIndex - 删除知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-deleteindex.md)
- [ListChunks - 查询索引下的分片列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-listchunks.md)
- [UpdateChunk - 修改切片](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-updatechunk.md)
- [DeleteChunk - 删除切片](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-deletechunk.md)
- [GetIndexMonitor - 获取知识库监控数据](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-getindexmonitor.md)
- [GetAlipayTransferStatus - 查询支付宝打赏状态](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-getalipaytransferstatus.md)
- [GetAlipayUrl - 获取支付宝打赏URL](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-getalipayurl.md)
- [ApplyTempStorageLease - 申请临时文件上传许可](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-applytempstoragelease.md)
- [CreateMemory - 创建长期记忆体](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-creatememory.md)
- [GetMemory - 获取长期记忆体](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-getmemory.md)
- [UpdateMemory - 更新长期记忆体](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-updatememory.md)
- [DeleteMemory - 删除长期记忆体](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-deletememory.md)
- [ListMemories - 获取长期记忆体列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-listmemories.md)
- [CreateMemoryNode - 创建记忆片段](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-creatememorynode.md)
- [GetMemoryNode - 获取记忆片段](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-getmemorynode.md)
- [UpdateMemoryNode - 更新记忆片段](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-updatememorynode.md)
- [DeleteMemoryNode - 删除记忆片段](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-deletememorynode.md)
- [ListMemoryNodes - 获取记忆片段列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-listmemorynodes.md)


