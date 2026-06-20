# application component api reference

百炼平台应用组件 API（`bailian/2023-12-29`）提供了一组 RESTful 接口，用于以编程方式管理数据连接、知识库、Prompt 模板、长期记忆等应用组件。API 采用 ROA 签名风格，支持多语言 SDK 调用，服务接入点覆盖华北2（北京）和新加坡两个地域。所有接口均需要通过 AccessKey 进行身份认证，建议使用 RAM 用户并遵循最小权限原则。

## 接入准备

调用应用组件 API 前需要完成以下准备：

- **获取 AccessKey**：通过 RAM 用户创建 AccessKey，避免直接使用阿里云主账号密钥。详见 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md) 中的账号安全说明。
- **服务接入点**：公网接入地址为 `bailian.<regionId>.aliyuncs.com`，VPC 接入地址为 `bailian-vpc.<regionId>.aliyuncs.com`。当前支持 `cn-beijing` 和 `ap-southeast-1` 两个地域，详见 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)。
- **RAM 授权**：RAM 用户需要获取对应的权限策略（如 `AliyunBailianDataFullAccess`）并加入业务空间后方可调用。授权粒度为操作级，RamCode 为 `sfm`，详见 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)。

## 数据连接（原应用数据）

数据连接 API 用于管理文件和类目，是构建知识库的数据基础。

### 类目管理

| API | 说明 | HTTP 方法 | 限流 |
|-----|------|-----------|------|
| AddCategory | 在业务空间中创建类目，每空间最多 500 个 | POST | 5 次/秒 |
| ListCategory | 查询类目列表，支持分页（NextToken） | POST | 5 次/秒 |
| DeleteCategory | 永久删除指定类目 | DELETE | 5 次/秒 |

> **注意**：不支持通过 API 新增或查询数据表，需通过控制台操作。

### 文件管理

| API | 说明 | HTTP 方法 | 限流 |
|-----|------|-----------|------|
| ApplyFileUploadLease | 申请上传租约，用于上传知识库或会话交互文件 | POST | 10 次/秒 |
| AddFile | 将临时存储空间的文件导入数据连接 | PUT | 10 次/秒 |
| AddFilesFromAuthorizedOss | 从已授权 OSS Bucket 导入文件 | POST | 5 次/秒 |
| ListFile | 查询类目下的文件列表，支持分页 | GET | 5 次/秒 |
| DescribeFile | 查询文件基本信息（名称、类型、状态等） | GET | 10 次/秒 |
| UpdateFileTag | 更新单个文件的标签 | PUT | 5 次/秒 |
| BatchUpdateFileTag | 批量更新文档标签，支持追加和覆盖模式 | PUT | - |
| DeleteFile | 删除单个文件（仅限 PARSE_FAILED 或 PARSE_SUCCESS 状态） | DELETE | 10 次/秒 |
| DeleteFiles | 批量删除文件，单次最多 20 个 | POST | 10 次/秒 |

文件上传流程为：先调用 `ApplyFileUploadLease` 获取租约，使用租约上传文件到临时存储，再调用 `AddFile` 将文件导入数据连接。`AddFile` 时需指定解析器类型，可选值包括 `DOCMIND`（智能文档解析）、`DOCMIND_DIGITAL`（电子文档解析）、`DOCMIND_LLM_VERSION`（大模型文档解析）、`DASH_QWEN_VL_PARSER`（Qwen VL 解析）、`DOCMIND_LLM_VERSION_MEDIA`（音视频解析）和 `AUTO_SELECT`（自动选择）。

> **注意**：DeleteFile / DeleteFiles 仅删除数据连接中的文件，不影响已构建的知识库。如需删除知识库中的文件，请使用 DeleteIndexDocument。

### 解析设置

| API | 说明 |
|-----|------|
| GetParseSettings | 查询类目的解析设置 |
| GetAvailableParserTypes | 获取文件支持的解析器类型列表 |
| ChangeParseSetting | 修改类目的解析设置 |

### 表格与连接器

| API | 说明 |
|-----|------|
| AddTable | 添加表格 |
| UpdateTableFromAuthorizedOss | 从已授权 OSS Bucket 中选择文件更新表格 |
| AddConnector | 新增连接器 |
| GetConnector | 获取连接器信息 |
| UpdateConnector | 编辑连接器 |

## 知识库管理

知识库 API 提供知识库全生命周期管理，包括创建、文档管理、检索和监控。

### 知识库 CRUD

| API | 说明 | HTTP 方法 |
|-----|------|-----------|
| CreateIndex | 创建知识库 | POST |
| UpdateIndex | 更新知识库配置 | PUT |
| ListIndices | 查询知识库列表 | GET |
| DeleteIndex | 删除知识库 | DELETE |

### 知识库任务

| API | 说明 |
|-----|------|
| SubmitIndexJob | 提交知识库创建任务（异步） |
| SubmitIndexAddDocumentsJob | 向已有知识库追加文档（异步） |
| GetIndexJobStatus | 查询知识库创建/追加任务的状态 |

知识库构建为异步流程：先调用 `CreateIndex` 创建知识库，然后通过 `SubmitIndexJob` 提交构建任务，使用 `GetIndexJobStatus` 轮询任务状态。后续追加文档使用 `SubmitIndexAddDocumentsJob`。

### 文档与切片管理

| API | 说明 |
|-----|------|
| ListIndexDocuments | 查询知识库下的文件列表 |
| ListIndexFileDetails | 查询知识库下的文件详情 |
| DeleteIndexDocument | 删除知识库中的文件 |
| ListChunks | 查询索引下的分片列表 |
| UpdateChunk | 修改切片内容 |
| DeleteChunk | 删除切片 |

### 检索与监控

| API | 说明 |
|-----|------|
| Retrieve | 检索知识库，返回相关文档片段 |
| GetIndexMonitor | 获取知识库监控数据 |

## Prompt 模板管理

Prompt 模板 API 支持模板的完整 CRUD 操作，模板内容支持 `${variable}` 格式的变量占位符。

| API | 说明 |
|-----|------|
| CreatePromptTemplate | 创建 Prompt 模板 |
| GetPromptTemplate | 根据模板 ID 获取模板内容及变量列表 |
| UpdatePromptTemplate | 更新 Prompt 模板 |
| DeletePromptTemplate | 删除 Prompt 模板 |
| ListPromptTemplates | 获取 Prompt 模板列表 |

## 长期记忆

长期记忆 API 提供记忆体和记忆片段（MemoryNode）两级管理能力。

| API | 说明 |
|-----|------|
| CreateMemory | 创建长期记忆体 |
| GetMemory | 获取长期记忆体详情 |
| UpdateMemory | 更新长期记忆体 |
| DeleteMemory | 删除长期记忆体 |
| ListMemories | 获取长期记忆体列表 |
| CreateMemoryNode | 创建记忆片段 |
| GetMemoryNode | 获取记忆片段 |
| UpdateMemoryNode | 更新记忆片段 |
| DeleteMemoryNode | 删除记忆片段 |
| ListMemoryNodes | 获取记忆片段列表 |

## 其他

| API | 说明 |
|-----|------|
| ApplyTempStorageLease | 申请临时文件上传许可 |
| GetAlipayUrl | 获取支付宝打赏 URL |
| GetAlipayTransferStatus | 查询支付宝打赏状态 |

## 通用说明

- **请求路径**：所有接口路径以 `/{WorkspaceId}/` 开头，WorkspaceId 为业务空间 ID。
- **幂等性**：查询类接口（List/Get/Describe）通常具有幂等性，创建类接口（Add/Create/Apply）通常不具备幂等性。
- **分页**：列表接口使用 `MaxResults` + `NextToken` 分页模式，NextToken 为空时表示数据已全部返回。
- **限流**：大部分接口限流为 5~10 次/秒，超限时请稍后重试。
- **SDK**：建议使用阿里云百炼 SDK 调用，避免自签名的复杂性。SDK 下载地址见 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)。

## 来源文档

- [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)
- [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)
- [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)
- [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)
- [AddCategory - 新增类目](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addcategory.md)
- [ListCategory - 类目列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-listcategory.md)
- [DeleteCategory - 删除类目](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-deletecategory.md)
- [ApplyFileUploadLease - 申请文件上传租约](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-applyfileuploadlease.md)
- [AddFilesFromAuthorizedOss - 从已授权OSS Bucket中导入文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addfilesfromauthorizedoss.md)
- [AddFile - 添加文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addfile.md)
- [ListFile - 文件列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-listfile.md)
- [DescribeFile - 查询文件状态](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-describefile.md)
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
- [GetIndexJobStatus - 查询知识库创建任务状态](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-getindexjobstatus.md)
- [CreateIndex - 创建知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-createindex.md)
- [UpdateConnector - 编辑连接器](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-updateconnector.md)
- [SubmitIndexJob - 提交知识库创建任务](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-submitindexjob.md)
- [SubmitIndexAddDocumentsJob - 提交知识库追加任务](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-submitindexadddocumentsjob.md)
- [ListIndexDocuments - 查询知识库下的文件列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-listindexdocuments.md)
- [ListIndexFileDetails - 查询知识库下的文件详情](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-listindexfiledetails.md)
- [Retrieve - 检索知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-retrieve.md)
- [UpdateIndex - 更新知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-updateindex.md)
- [DeleteIndexDocument - 删除知识库下的文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-deleteindexdocument.md)
- [DeleteIndex - 删除知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-deleteindex.md)
- [ListIndices - 查询知识库列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-listindices.md)
- [ListChunks - 查询索引下的分片列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-listchunks.md)
- [UpdateChunk - 修改切片](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-updatechunk.md)
- [DeleteChunk - 删除切片](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-deletechunk.md)
- [GetIndexMonitor - 获取知识库监控数据](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-getindexmonitor.md)
- [CreatePromptTemplate - 创建Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-createprompttemplate.md)
- [GetPromptTemplate - 获取Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-getprompttemplate.md)
- [UpdatePromptTemplate - 更新Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-updateprompttemplate.md)
- [DeletePromptTemplate - 删除Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-deleteprompttemplate.md)
- [ListPromptTemplates - 获取Prompt模板列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-listprompttemplates.md)
- [GetAlipayTransferStatus - 查询支付宝打赏状态](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-getalipaytransferstatus.md)
- [GetAlipayUrl - 获取支付宝打赏URL](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-getalipayurl.md)
- [ApplyTempStorageLease - 申请临时文件上传许可](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-applytempstoragelease.md)
- [GetMemory - 获取长期记忆体](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-getmemory.md)
- [DeleteMemory - 删除长期记忆体](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-deletememory.md)
- [CreateMemory - 创建长期记忆体](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-creatememory.md)
- [UpdateMemory - 更新长期记忆体](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-updatememory.md)
- [ListMemories - 获取长期记忆体列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-listmemories.md)
- [UpdateMemoryNode - 更新记忆片段](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-updatememorynode.md)
- [CreateMemoryNode - 创建记忆片段](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-creatememorynode.md)
- [DeleteMemoryNode - 删除记忆片段](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-deletememorynode.md)
- [GetMemoryNode - 获取记忆片段](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-getmemorynode.md)
- [ListMemoryNodes - 获取记忆片段列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-listmemorynodes.md)


