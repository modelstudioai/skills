# application component api reference

百炼平台应用组件 API（`bailian/2023-12-29`）提供了数据连接、知识库、Prompt 模板、长期记忆等核心能力的 OpenAPI 接口，采用 ROA 签名风格。开发者可通过阿里云百炼 SDK 直接调用，也可使用自签名方式对接。所有接口均需传入 `WorkspaceId`（[业务空间](../concepts/workspace.md) ID），RAM 子账号需要先获取对应权限策略并加入[业务空间](../concepts/workspace.md)后才能调用。

## 服务接入点与鉴权

当前支持两个地域的接入点：

| 地域 | 地域 ID | 公网接入地址 | VPC 接入地址 |
|------|---------|-------------|-------------|
| 华北2（北京） | cn-beijing | bailian.cn-beijing.aliyuncs.com | bailian-vpc.cn-beijing.aliyuncs.com |
| 新加坡 | ap-southeast-1 | bailian.ap-southeast-1.aliyuncs.com | bailian-vpc.ap-southeast-1.aliyuncs.com |

调用前需准备 AccessKey，建议使用 RAM 用户而非主账号以降低安全风险。RAM 权限策略的 RamCode 为 `sfm`，授权粒度为操作级。大多数写操作需要 `AliyunBailianDataFullAccess` 策略，部分只读接口（如 DescribeFile、GetIndexJobStatus）也支持 `AliyunBailianDataReadOnlyAccess`。详见[授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)。

## 数据连接（原应用数据）

数据连接相关 API 用于管理类目、文件、解析设置、表格和连接器，是构建知识库的数据基础。

### 类目管理

| API | 说明 | 限流 | 幂等性 |
|-----|------|------|--------|
| AddCategory | 在[业务空间](../concepts/workspace.md)中新建类目，每空间最多 500 个 | 5 次/秒 | 否 |
| ListCategory | 查询类目列表，支持分页 | 5 次/秒 | 是 |
| DeleteCategory | 永久删除指定类目 | 5 次/秒 | 是 |

> **注意**：当前不支持通过 API 查询或新增数据表，数据表操作请通过控制台完成。

### 文件管理

文件上传采用两步流程：先调用 ApplyFileUploadLease 获取上传租约，使用返回的 URL 上传文件后，再调用 AddFile 将文件导入百炼。也可通过 AddFilesFromAuthorizedOss 直接从已授权的 OSS Bucket 导入。详见[ApplyFileUploadLease - 申请文件上传租约](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-applyfileuploadlease.md)。

| API | 说明 | 限流 |
|-----|------|------|
| ApplyFileUploadLease | 申请上传租约（知识库文件或会话交互文件） | 10 次/秒 |
| AddFile | 将临时存储文件导入数据连接 | 10 次/秒 |
| AddFilesFromAuthorizedOss | 从已授权 OSS Bucket 批量导入文件 | 5 次/秒 |
| DescribeFile | 查询文件基本信息（名称、类型、状态等） | 10 次/秒 |
| ListFile | 分页查询指定类目下的文件列表 | 5 次/秒 |
| UpdateFileTag | 更新单个文件的标签 | 5 次/秒 |
| BatchUpdateFileTag | 批量更新文件标签 | 5 次/秒 |
| DeleteFile | 删除单个文件 | 5 次/秒 |
| DeleteFiles | 批量删除文件 | 5 次/秒 |

AddFile 接口的 `Parser` 参数支持以下解析器类型：
- `DOCMIND`（智能文档解析）
- `DOCMIND_DIGITAL`（电子文档解析）
- `DOCMIND_LLM_VERSION`（大模型文档解析）
- `DASH_QWEN_VL_PARSER`（Qwen VL 解析）
- `DOCMIND_LLM_VERSION_MEDIA`（音视频解析）
- `AUTO_SELECT`（自动选择解析器）

### 解析设置

| API | 说明 |
|-----|------|
| GetParseSettings | 获取类目的解析设置 |
| GetAvailableParserTypes | 获取指定文件支持的解析器类型列表 |
| ChangeParseSetting | 修改类目的解析设置 |

### 表格与连接器

| API | 说明 |
|-----|------|
| AddTable | 添加表格 |
| UpdateTableFromAuthorizedOss | 从已授权 OSS Bucket 更新表格 |
| AddConnector | 新增连接器 |
| GetConnector | 获取连接器信息（当前仅支持文件连接器） |
| UpdateConnector | 编辑连接器名称和描述 |

连接器的 `StorageType` 支持 `OSS_CUSTOM`（自有 OSS 存储）和 `OSS_PLATFORM`（平台 OSS 存储）。

## Prompt 工程

Prompt 模板 API 支持对 Prompt 模板的完整 CRUD 操作。模板内容支持变量占位符（如 `${theme}`），系统会自动提取变量列表。详见[CreatePromptTemplate - 创建Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-createprompttemplate.md)。

| API | 方法 | 说明 |
|-----|------|------|
| CreatePromptTemplate | POST | 创建模板（暂不支持文生图模板） |
| GetPromptTemplate | GET | 按模板 ID 获取详情 |
| UpdatePromptTemplate | PATCH | 增量更新模板名称或内容 |
| DeletePromptTemplate | DELETE | 按模板 ID 删除 |
| ListPromptTemplates | GET | 分页查询模板列表，支持按名称和类型（System/Custom）过滤 |

## 知识库

知识库 API 是百炼 RAG 能力的核心，覆盖知识库的创建、数据导入、检索、文件与切片管理全流程。

### 知识库生命周期

创建知识库的典型流程为：CreateIndex -> SubmitIndexJob -> 轮询 GetIndexJobStatus 直到完成。详见[CreateIndex - 创建知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-createindex.md)。

| API | 说明 | 限流 |
|-----|------|------|
| CreateIndex | 创建知识库（非结构化或结构化），不具幂等性 | 10 次/秒 |
| SubmitIndexJob | 提交知识库创建任务，必须在 CreateIndex 后调用 | 10 次/秒 |
| SubmitIndexAddDocumentsJob | 向已有知识库追加文件（不支持数据查询/图片问答类） | 10 次/秒 |
| GetIndexJobStatus | 查询任务状态，调用间隔建议 5 秒以上 | - |
| UpdateIndex | 更新知识库配置（名称、描述、检索参数等） | - |
| ListIndices | 分页查询[业务空间](../concepts/workspace.md)下的知识库列表 | 10 次/秒 |
| DeleteIndex | 永久删除知识库（不可逆，不删除源文件） | 10 次/秒 |
| GetIndexMonitor | 获取知识库监控数据 | - |

> **注意**：CreateIndex 仅初始化知识库，必须后续调用 SubmitIndexJob 才能完成创建，否则将得到空知识库。CreateIndex 不具幂等性，重复调用会创建多个同名知识库。

UpdateIndex 支持调整检索参数：
- `DenseSimilarityTopK`：向量检索 Top K，范围 [0-100]，默认 100
- `SparseSimilarityTopK`：关键词检索 Top K，范围 [0-100]，默认 100
- 两者之和不超过 200
- `RerankMinScore`：排序最低分数，范围 [0-1]
- `PipelineCommercialType`：知识库规格（standard / enterprise）

### 知识库检索

Retrieve 接口用于在指定知识库中检索信息，支持通过百炼 SDK（AccessKey 鉴权）或 Spring AI Alibaba（API-Key 鉴权）调用。接口具有幂等性，但因包含复杂检索逻辑，响应时间可能较长，建议合理设置超时和重试策略。详见[Retrieve - 检索知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-retrieve.md)。

### 文件与切片管理

| API | 说明 |
|-----|------|
| ListIndexFileDetails | 查询知识库中文件的详细信息，支持按状态和名称过滤 |
| ListIndexDocuments | 查询知识库中文件的概要信息 |
| DeleteIndexDocument | 从知识库中删除指定文件 |
| ListChunks | 查询文件的切片列表（文档搜索类查指定文件，数据查询类查全部） |
| UpdateChunk | 修改切片内容和标题（仅支持文档搜索类知识库） |
| DeleteChunk | 删除指定切片 |

文件导入状态包括：`RUNNING`（构建中）、`FINISH`（成功）、`INSERT_ERROR`（导入失败）、`PARSE_FAILED`（解析失败）、`DOC_PARSING`（解析中）、`DELETED`（已删除）。

## 长期记忆

长期记忆 API 用于管理智能体的记忆能力，包括记忆体（Memory）和记忆片段（MemoryNode）两个层级。

| API | 说明 |
|-----|------|
| CreateMemory | 创建长期记忆体 |
| GetMemory | 获取记忆体详情 |
| UpdateMemory | 更新记忆体 |
| DeleteMemory | 删除记忆体 |
| ListMemories | 查询记忆体列表 |
| CreateMemoryNode | 创建记忆片段 |
| GetMemoryNode | 获取记忆片段详情 |
| UpdateMemoryNode | 更新记忆片段 |
| DeleteMemoryNode | 删除记忆片段 |
| ListMemoryNodes | 查询记忆片段列表 |

## 其他

| API | 说明 |
|-----|------|
| ApplyTempStorageLease | 申请临时文件上传许可 |
| GetAlipayTransferStatus | 查询支付宝打赏状态 |
| GetAlipayUrl | 获取支付宝打赏 URL |

## 通用注意事项

- 所有接口均需 `WorkspaceId` 路径参数，获取方式参见[业务空间](../concepts/workspace.md)文档
- 建议使用官方 SDK 调用而非自签名，自签名对接复杂度高（约需 5 个工作日）
- 分页查询使用 `NextToken` / `MaxResults` 模式（部分接口使用 `PageNumber` / `PageSize`）
- 各接口限流频率为 5-15 次/秒不等，触发限流后需等待后重试
- 版本变更历史可查看[版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)，近期变更包括 CreateIndex 入参调整、UpdateIndex 新增、GetIndexMonitor 新增等

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



