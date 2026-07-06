# application component api reference

百炼平台应用组件 API（`bailian/2023-12-29`）提供数据连接、知识库、Prompt 模板等应用构建能力的编程接口。API 采用 ROA 签名风格，覆盖文件管理、知识库全生命周期、Prompt 工程等核心场景，支持通过多语言 SDK 或自签名方式接入。

## 接入准备

### 服务接入点

百炼应用组件 API 目前支持以下区域，详见[服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)：

| 地域 | 地域 ID | 公网接入地址 | VPC 接入地址 |
| --- | --- | --- | --- |
| 华北2（北京） | cn-beijing | bailian.cn-beijing.aliyuncs.com | bailian-vpc.cn-beijing.aliyuncs.com |
| 新加坡 | ap-southeast-1 | bailian.ap-southeast-1.aliyuncs.com | bailian-vpc.ap-southeast-1.aliyuncs.com |

### SDK 与认证

推荐使用官方 SDK 调用，避免手动签名。SDK 下载地址：`https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29`。

调用前需准备：

1. **AccessKey**：通过阿里云控制台获取，建议为 RAM 用户创建独立 AccessKey
2. **RAM 授权**：RAM 用户需获取 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略，并加入目标[业务空间](../concepts/workspace.md)
3. **[业务空间](../concepts/workspace.md) ID（WorkspaceId）**：大部分接口都需要此参数作为路径参数

> **注意**：阿里云账号（主账号）拥有全部权限，无需额外授权，但出于安全考虑建议使用 RAM 用户调用。RAM 权限体系的代码为 `sfm`，授权粒度为操作级，详见[授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)。

## 数据连接（原应用数据）

数据连接模块负责文件和数据的导入、管理与解析配置，是知识库构建的数据基础。

### 类目管理

类目用于分类管理文件，每个[业务空间](../concepts/workspace.md)最多 500 个类目。

| API | 说明 | HTTP 方法 |
| --- | --- | --- |
| AddCategory | 新增类目 | POST |
| ListCategory | 获取类目列表 | POST |
| DeleteCategory | 永久删除类目 | POST |

### 文件管理

文件上传采用两步流程：先通过 `ApplyFileUploadLease` 获取上传租约，上传文件到临时存储后，再通过 `AddFile` 将文件导入数据连接。也可通过 `AddFilesFromAuthorizedOss` 直接从已授权的 OSS Bucket 导入。

| API | 说明 |
| --- | --- |
| ApplyFileUploadLease | 申请文件上传租约（用于知识库文件或会话交互文件） |
| AddFile | 从临时存储导入文件到数据连接 |
| AddFilesFromAuthorizedOss | 从已授权 OSS Bucket 批量导入文件 |
| DescribeFile | 查询单个文件的名称、类型、状态等信息 |
| ListFile | 获取指定类目下的文件列表 |
| UpdateFileTag | 更新单个文件标签 |
| BatchUpdateFileTag | 批量更新文件标签 |
| DeleteFile | 删除单个文件 |
| DeleteFiles | 批量删除文件 |

### 解析设置

控制文件在知识库中的解析方式。

| API | 说明 |
| --- | --- |
| GetParseSettings | 获取类目的解析设置 |
| GetAvailableParserTypes | 获取文件支持的解析器类型列表 |
| ChangeParseSetting | 修改类目的解析设置 |

### 表格与连接器

| API | 说明 |
| --- | --- |
| AddTable | 添加表格数据 |
| UpdateTableFromAuthorizedOss | 从已授权 OSS Bucket 更新表格 |
| AddConnector | 新增连接器（当前仅支持文件类型），限流 5 次/秒 |
| GetConnector | 获取连接器信息 |
| UpdateConnector | 编辑连接器配置 |

## 知识库管理

知识库是百炼 RAG 能力的核心组件，支持非结构化（文档/音视频）和结构化（数据查询/图片问答）两类知识库。完整的知识库 API 使用指南请参考[API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)。

### 创建流程

知识库创建是异步流程，需要按以下步骤操作：

1. **CreateIndex** — 初始化知识库，指定名称、类型、切片策略等配置。此接口不具备幂等性，重复调用会创建多个同名知识库
2. **SubmitIndexJob** — 提交创建任务，开始实际的文档解析和索引构建。高峰期可能耗时数小时
3. **GetIndexJobStatus** — 轮询任务状态（建议间隔 5 秒以上）

### 文档追加

对已有知识库追加文件使用 `SubmitIndexAddDocumentsJob`，需先通过 `AddFile` 上传文件。该接口不支持数据查询/图片问答类知识库。

### 检索

`Retrieve` 接口用于在指定知识库中检索信息，支持通过百炼 SDK（配合 AccessKey）或 Spring AI Alibaba（配合 API-Key）两种方式调用。该接口响应时间可能较长，建议合理设置超时与重试策略。

### 知识库配置与管理

| API | 说明 |
| --- | --- |
| UpdateIndex | 更新知识库配置（名称、描述、检索参数、规格类型等） |
| ListIndices | 获取业务空间下的知识库列表 |
| DeleteIndex | 永久删除知识库（不可逆，需先解除应用关联） |
| ListIndexFileDetails | 查询知识库下的文件详情 |
| ListIndexDocuments | 查询知识库下的文件列表 |
| DeleteIndexDocument | 删除知识库中的指定文件 |
| GetIndexMonitor | 获取知识库监控数据 |

### 切片管理

| API | 说明 |
| --- | --- |
| ListChunks | 查询文本切片列表（文档搜索类按文件查询，数据查询类获取全部） |
| UpdateChunk | 修改切片内容和标题（仅支持文档搜索类知识库） |
| DeleteChunk | 删除指定切片 |

知识库检索的关键参数包括：
- **DenseSimilarityTopK**：向量检索 Top K，范围 0-100，默认 100
- **SparseSimilarityTopK**：关键词检索 Top K，范围 0-100，默认 100
- 两者之和不超过 200
- **RerankMinScore**：排序最低分数，范围 0-1

## Prompt 模板管理

Prompt 模板支持创建、查询、更新、删除和列表操作，用于管理和复用 Prompt 工程成果。

| API | 说明 |
| --- | --- |
| CreatePromptTemplate | 创建 Prompt 模板（暂不支持文生图类型） |
| GetPromptTemplate | 获取指定 Prompt 模板详情 |
| UpdatePromptTemplate | 更新 Prompt 模板内容 |
| DeletePromptTemplate | 删除指定 Prompt 模板 |
| ListPromptTemplates | 获取 Prompt 模板列表 |

## 其他接口

| API | 说明 |
| --- | --- |
| ApplyTempStorageLease | 申请临时文件上传许可 |
| GetAlipayTransferStatus | 查询支付宝打赏状态 |
| GetAlipayUrl | 获取支付宝打赏 URL |

## 通用限制与注意事项

- **限流**：大部分接口限流为 10 次/秒，连接器相关接口为 5 次/秒。遇到限流请稍后重试
- **幂等性**：查询类接口（如 GetIndexJobStatus、Retrieve、ListIndices）通常具有幂等性；创建类接口（如 CreateIndex、SubmitIndexJob）不具备幂等性，需注意避免重复调用
- **异步操作**：知识库创建和追加文档为异步操作，通过 GetIndexJobStatus 轮询状态，GetIndexJobStatus 限流 20 次/分钟
- **版本演进**：API 持续迭代中，最新变更包括 CreateIndex 入参调整（2026-03-30）、UpdateIndex 新增（2026-01-19）等，详见[版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)
- **删除操作不可逆**：DeleteIndex、DeleteCategory 等删除操作为永久性删除，请谨慎操作

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







