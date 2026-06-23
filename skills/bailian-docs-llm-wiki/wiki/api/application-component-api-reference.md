# application component api reference

百炼平台应用组件 API（`bailian/2023-12-29`）提供了数据连接、知识库、Prompt 模板、长期记忆等核心功能的编程接口，采用 ROA 签名风格。开发者可通过官方多语言 SDK 调用这些接口来管理文件、构建知识库、执行检索以及管理 Prompt 模板等操作。所有接口均需在[业务空间](../concepts/workspace.md)（Workspace）上下文中调用，并支持 RAM 权限控制。

## 服务接入与鉴权

API 服务通过地域化接入点访问，当前支持以下地域：

| 地域 | 地域 ID | 公网接入地址 | VPC 接入地址 |
|------|---------|-------------|-------------|
| 华北2（北京） | cn-beijing | bailian.cn-beijing.aliyuncs.com | bailian-vpc.cn-beijing.aliyuncs.com |
| 新加坡 | ap-southeast-1 | bailian.ap-southeast-1.aliyuncs.com | bailian-vpc.ap-southeast-1.aliyuncs.com |

调用前需准备 AccessKey。建议使用 RAM 用户并按最小权限原则配置策略，RAM 代码为 `sfm`，授权粒度为操作级。详见 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)。

## 数据连接（原应用数据）

数据连接 API 用于管理类目、文件、连接器和表格，是构建知识库的数据基础。

### 类目管理

| API | 说明 | HTTP 方法 | 限流 |
|-----|------|-----------|------|
| AddCategory | 在[业务空间](../concepts/workspace.md)中创建类目，最多 500 个 | POST | 5 次/秒 |
| ListCategory | 查询类目列表，支持分页（NextToken） | POST | 5 次/秒 |
| DeleteCategory | 永久删除指定类目 | DELETE | 5 次/秒 |

> **注意**：不支持通过 API 新增或查询数据表，数据表操作需在控制台完成。

### 文件管理

文件上传采用两步流程：先调用 ApplyFileUploadLease 获取上传租约，再通过租约上传文件至临时存储，最后调用 AddFile 导入至数据连接。

| API | 说明 | 限流 |
|-----|------|------|
| [ApplyFileUploadLease](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-applyfileuploadlease.md) | 申请文件上传租约 | 10 次/秒 |
| AddFile | 从临时存储导入文件至数据连接 | 10 次/秒 |
| AddFilesFromAuthorizedOss | 从已授权 OSS Bucket 导入文件 | 5 次/秒 |
| ListFile | 查询指定类目下的文件列表 | 5 次/秒 |
| DescribeFile | 查询单个文件的状态和基本信息 | 10 次/秒 |
| UpdateFileTag | 更新单个文件标签 | - |
| BatchUpdateFileTag | 批量更新文件标签 | - |
| DeleteFile | 删除单个文件 | - |
| DeleteFiles | 批量删除文件 | - |

文件导入时需要指定解析器类型（`Parser` 参数），可选值包括：
- `DOCMIND` — 智能文档解析
- `DOCMIND_DIGITAL` — 电子文档解析
- `DOCMIND_LLM_VERSION` — 大模型文档解析
- `DASH_QWEN_VL_PARSER` — Qwen VL 解析
- `DOCMIND_LLM_VERSION_MEDIA` — 音视频解析
- `AUTO_SELECT` — 自动选择解析器

可通过 GetAvailableParserTypes 接口查询文件支持的解析器类型，通过 GetParseSettings / ChangeParseSetting 管理类目级解析设置。

### 连接器与表格

| API | 说明 |
|-----|------|
| AddConnector | 新增数据连接器 |
| GetConnector | 获取连接器信息 |
| UpdateConnector | 编辑连接器配置 |
| AddTable | 添加表格 |
| UpdateTableFromAuthorizedOss | 从已授权 OSS Bucket 更新表格 |

## 知识库

知识库 API 覆盖了从创建到检索的完整生命周期。详细用法参见 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)。

### 知识库生命周期

创建知识库需要两步：先调用 CreateIndex 初始化，再调用 SubmitIndexJob 提交创建任务。CreateIndex 本身不具备幂等性，重复调用会创建多个同名知识库。

| API | 说明 | 限流 |
|-----|------|------|
| CreateIndex | 初始化知识库（支持非结构化/结构化两类） | 10 次/秒 |
| SubmitIndexJob | 提交创建任务以完成知识库构建 | - |
| GetIndexJobStatus | 查询创建任务状态 | - |
| SubmitIndexAddDocumentsJob | 向已有知识库追加文档 | - |
| UpdateIndex | 更新知识库配置 | - |
| DeleteIndex | 永久删除知识库（不可逆） | 10 次/秒 |
| ListIndices | 查询知识库列表，支持分页和按名称查找 | 10 次/秒 |

> **注意**：删除知识库前需先解除与应用的关联（当前只能通过控制台操作）。删除知识库不会删除数据连接中已导入的文件。

### 知识库检索与文件管理

| API | 说明 |
|-----|------|
| Retrieve | 检索知识库内容 |
| ListIndexDocuments | 查询知识库下的文件列表 |
| ListIndexFileDetails | 查询知识库下的文件详情，支持按状态和名称过滤 |
| DeleteIndexDocument | 删除知识库下的指定文件 |
| GetIndexMonitor | 获取知识库监控数据（存储用量、检索 QPS） |

GetIndexMonitor 支持查询最长 30 天的监控数据，返回的时间窗口粒度会根据查询范围动态调整。

### 切片管理

| API | 说明 |
|-----|------|
| ListChunks | 查询文本切片列表 |
| UpdateChunk | 修改切片内容 |
| DeleteChunk | 删除切片（被删切片无法被检索召回） |

对于文档搜索或音视频搜索类知识库，ListChunks 可查询指定文件的所有切片；对于数据查询或图片问答类知识库，则获取全部切片信息。

## Prompt 模板

Prompt 模板 API 支持模板的完整 CRUD 操作。模板内容可包含 `${变量名}` 格式的占位符。

| API | 说明 |
|-----|------|
| CreatePromptTemplate | 创建 Prompt 模板（暂不支持文生图模板） |
| GetPromptTemplate | 根据模板 ID 获取模板详情 |
| UpdatePromptTemplate | 更新 Prompt 模板 |
| DeletePromptTemplate | 删除 Prompt 模板 |
| ListPromptTemplates | 获取 Prompt 模板列表 |

## 长期记忆

长期记忆 API 用于管理记忆体和记忆片段，支持对话上下文的持久化存储。

| API | 说明 |
|-----|------|
| CreateMemory | 创建长期记忆体 |
| GetMemory | 获取长期记忆体详情 |
| UpdateMemory | 更新长期记忆体 |
| DeleteMemory | 删除长期记忆体 |
| ListMemories | 获取长期记忆体列表 |
| CreateMemoryNode | 创建记忆片段 |
| GetMemoryNode | 获取记忆片段详情 |
| UpdateMemoryNode | 更新记忆片段 |
| DeleteMemoryNode | 删除记忆片段 |
| ListMemoryNodes | 获取记忆片段列表 |

## 其他接口

| API | 说明 |
|-----|------|
| ApplyTempStorageLease | 申请临时文件上传许可 |
| GetAlipayUrl | 获取支付宝打赏 URL |
| GetAlipayTransferStatus | 查询支付宝打赏状态 |

## 通用说明

- **SDK**：推荐使用官方 SDK（Java/TypeScript/Python/Go 等）调用，避免自行实现签名逻辑。自签名对接约需 5 个工作日，建议加入钉钉群 147535001692 获取指导。
- **权限**：RAM 用户需获取 `AliyunBailianDataFullAccess`（或对应只读策略），并加入[业务空间](../concepts/workspace.md)后方可调用。主账号可直接调用。
- **分页**：列表类接口统一使用 `NextToken` + `MaxResults` 或 `PageNumber` + `PageSize` 分页。
- **幂等性**：部分接口具有幂等性（如 DeleteCategory、ListFile、DescribeFile 等），部分不具有（如 AddCategory、AddFile、CreateIndex 等），具体见各接口说明。
- **限流**：各接口限流频率在 5-10 次/秒之间，遇限流请稍后重试。
- **版本变更**：API 持续迭代，最近变更包括 CreateIndex 入参更新、UpdateIndex 新增、GetIndexMonitor 新增等，详见 [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)。

## 来源文档

- [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)
- [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)
- [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)
- [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)
- [DeleteCategory - 删除类目](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-deletecategory.md)
- [ListCategory - 类目列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-listcategory.md)
- [AddCategory - 新增类目](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addcategory.md)
- [ApplyFileUploadLease - 申请文件上传租约](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-applyfileuploadlease.md)
- [AddFile - 添加文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addfile.md)
- [AddFilesFromAuthorizedOss - 从已授权OSS Bucket中导入文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addfilesfromauthorizedoss.md)
- [ListFile - 文件列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-listfile.md)
- [DescribeFile - 查询文件状态](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-describefile.md)
- [UpdateFileTag - 更新文件标签](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-updatefiletag.md)
- [DeleteFile - 删除文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-deletefile.md)
- [BatchUpdateFileTag - 批量更新文档标签](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-batchupdatefiletag.md)
- [GetParseSettings - 获取类目解析设置](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-getparsesettings.md)
- [DeleteFiles - 批量删除文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-deletefiles.md)
- [GetAvailableParserTypes - 获取文件支持的解析器类型](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-getavailableparsertypes.md)
- [ChangeParseSetting - 修改类目解析设置](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-changeparsesetting.md)
- [AddTable - 添加表格](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addtable.md)
- [AddConnector - 新增连接器](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addconnector.md)
- [UpdateTableFromAuthorizedOss - 从已授权OSS Bucket中选择文件更新表格](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-updatetablefromauthorizedoss.md)
- [GetConnector - 获取连接器信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-getconnector.md)
- [UpdateConnector - 编辑连接器](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-updateconnector.md)
- [CreateIndex - 创建知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-createindex.md)
- [SubmitIndexJob - 提交知识库创建任务](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-submitindexjob.md)
- [GetIndexJobStatus - 查询知识库创建任务状态](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-getindexjobstatus.md)
- [SubmitIndexAddDocumentsJob - 提交知识库追加任务](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-submitindexadddocumentsjob.md)
- [Retrieve - 检索知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-retrieve.md)
- [ListIndexDocuments - 查询知识库下的文件列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-listindexdocuments.md)
- [UpdateIndex - 更新知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-updateindex.md)
- [DeleteIndexDocument - 删除知识库下的文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-deleteindexdocument.md)
- [ListIndexFileDetails - 查询知识库下的文件详情](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-listindexfiledetails.md)
- [DeleteIndex - 删除知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-deleteindex.md)
- [ListIndices - 查询知识库列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-listindices.md)
- [DeleteChunk - 删除切片](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-deletechunk.md)
- [UpdateChunk - 修改切片](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-updatechunk.md)
- [ListChunks - 查询索引下的分片列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-listchunks.md)
- [GetIndexMonitor - 获取知识库监控数据](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-getindexmonitor.md)
- [CreatePromptTemplate - 创建Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-createprompttemplate.md)
- [GetPromptTemplate - 获取Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-getprompttemplate.md)
- [DeletePromptTemplate - 删除Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-deleteprompttemplate.md)
- [UpdatePromptTemplate - 更新Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-updateprompttemplate.md)
- [ListPromptTemplates - 获取Prompt模板列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-listprompttemplates.md)
- [GetAlipayTransferStatus - 查询支付宝打赏状态](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-getalipaytransferstatus.md)
- [GetAlipayUrl - 获取支付宝打赏URL](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-getalipayurl.md)
- [ApplyTempStorageLease - 申请临时文件上传许可](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-applytempstoragelease.md)
- [GetMemory - 获取长期记忆体](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-getmemory.md)
- [UpdateMemory - 更新长期记忆体](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-updatememory.md)
- [CreateMemory - 创建长期记忆体](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-creatememory.md)
- [DeleteMemory - 删除长期记忆体](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-deletememory.md)
- [ListMemories - 获取长期记忆体列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-listmemories.md)
- [GetMemoryNode - 获取记忆片段](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-getmemorynode.md)
- [CreateMemoryNode - 创建记忆片段](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-creatememorynode.md)
- [UpdateMemoryNode - 更新记忆片段](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-updatememorynode.md)
- [ListMemoryNodes - 获取记忆片段列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-listmemorynodes.md)
- [DeleteMemoryNode - 删除记忆片段](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-deletememorynode.md)




