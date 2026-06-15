# application component api reference

百炼平台应用组件 API（`bailian/2023-12-29`）是阿里云大模型服务平台百炼提供的一组 RESTful 接口，用于以编程方式管理数据连接、知识库、Prompt 模板、长期记忆等应用组件资源。API 采用 ROA 签名风格，推荐通过官方 SDK 调用以简化签名计算。所有接口均需要通过 AccessKey 进行身份认证，并以[业务空间](../concepts/workspace.md)（WorkspaceId）作为资源隔离的基本单元。

## 接入准备

### 服务接入点

API 当前支持两个地域，每个地域提供公网和 VPC 两种接入地址：

| 地域 | 地域 ID | 公网接入地址 | VPC 接入地址 |
|------|---------|-------------|-------------|
| 华北2（北京） | cn-beijing | `bailian.cn-beijing.aliyuncs.com` | `bailian-vpc.cn-beijing.aliyuncs.com` |
| 新加坡 | ap-southeast-1 | `bailian.ap-southeast-1.aliyuncs.com` | `bailian-vpc.ap-southeast-1.aliyuncs.com` |

详见 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)。

### 认证与授权

调用 API 前需准备 AccessKey。出于安全考虑，建议创建 RAM 用户并配置最小权限策略，而非直接使用阿里云主账号。百炼的 RAM 代码（RamCode）为 `sfm`，授权粒度为操作级。常用权限策略包括：

- `AliyunBailianDataFullAccess`：数据读写全部权限
- `AliyunBailianDataReadOnlyAccess`：数据只读权限

RAM 用户调用前还需[加入业务空间](https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users)。详细的操作与资源权限映射请参见 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)。

### SDK 与调用方式

官方提供多语言 SDK，可通过 [SDK 下载页](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29) 获取。不建议自签名对接（复杂度高，预计需 5 个工作日）。所有接口均可在 [OpenAPI Explorer](https://api.aliyun.com/) 中在线调试。

## 数据连接（原应用数据）

数据连接 API 用于管理百炼平台中的类目、文件、表格和连接器等数据资源。

### 类目管理

| API | 说明 | 限流 |
|-----|------|------|
| AddCategory | 在指定[业务空间](../concepts/workspace.md)中创建类目（上限 500 个） | 5 次/秒 |
| ListCategory | 分页查询类目列表（支持 NextToken 分页） | 5 次/秒 |
| DeleteCategory | 永久删除指定类目 | 5 次/秒 |

### 文件管理

| API | 说明 | 限流 |
|-----|------|------|
| ApplyFileUploadLease | 申请上传租约，用于上传知识库文件或会话交互文件 | 5 次/秒 |
| AddFile | 将临时存储空间中的文件导入数据连接 | 5 次/秒 |
| AddFilesFromAuthorizedOss | 从已授权的 OSS Bucket 导入文件 | 5 次/秒 |
| ListFile | 分页查询指定类目下的文件列表 | 5 次/秒 |
| DescribeFile | 查询文件基本信息（名称、类型、状态等） | 5 次/秒 |
| UpdateFileTag | 更新单个文件标签 | 5 次/秒 |
| BatchUpdateFileTag | 批量更新文件标签 | 5 次/秒 |
| DeleteFile | 永久删除指定文件 | 5 次/秒 |
| DeleteFiles | 批量删除文件 | - |

### 解析设置

| API | 说明 |
|-----|------|
| GetParseSettings | 获取类目的文档解析设置 |
| GetAvailableParserTypes | 获取指定文件支持的解析器类型列表 |
| ChangeParseSetting | 修改类目的解析设置 |

### 表格与连接器

| API | 说明 |
|-----|------|
| AddTable | 添加数据表 |
| UpdateTableFromAuthorizedOss | 从已授权 OSS Bucket 选择文件更新表格 |
| AddConnector | 新增连接器 |
| GetConnector | 获取连接器信息（当前仅支持文件连接器） |
| UpdateConnector | 编辑连接器 |

> **注意**：数据表的新增不支持通过 API 操作，需通过控制台的[应用数据](https://bailian.console.aliyun.com/?tab=app#/data-center)页面完成。

文件管理的完整参数说明请参见 [AddFile - 添加文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addfile.md)。

## [Prompt 工程](../concepts/prompt-engineering.md)

Prompt 模板 API 提供模板的完整生命周期管理。

| API | 说明 |
|-----|------|
| CreatePromptTemplate | 创建 Prompt 模板（暂不支持文生图模板） |
| GetPromptTemplate | 获取指定 Prompt 模板详情 |
| UpdatePromptTemplate | 更新 Prompt 模板 |
| DeletePromptTemplate | 删除 Prompt 模板 |
| ListPromptTemplates | 获取 Prompt 模板列表 |

模板内容支持变量占位符语法（如 `${theme}`），可在运行时动态替换。详见 [CreatePromptTemplate - 创建Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-createprompttemplate.md)。

## 知识库

知识库 API 是本组件中最核心的功能模块，覆盖知识库全生命周期管理和检索。百炼支持两类知识库：基于文档或音视频的非结构化知识库，以及用于数据查询或图片问答的结构化知识库。

### 知识库生命周期

| API | 说明 | 限流 |
|-----|------|------|
| CreateIndex | 初始化知识库创建作业 | 10 次/秒 |
| SubmitIndexJob | 提交知识库创建任务（CreateIndex 后必须调用） | 5 次/秒 |
| GetIndexJobStatus | 查询创建/追加任务的执行状态 | 5 次/秒 |
| SubmitIndexAddDocumentsJob | 向已有知识库追加文件 | 5 次/秒 |
| UpdateIndex | 更新知识库配置 | - |
| ListIndices | 查询知识库列表 | 5 次/秒 |
| DeleteIndex | 删除知识库 | 5 次/秒 |
| GetIndexMonitor | 获取知识库监控数据（含规格信息） | - |

> **注意**：`CreateIndex` 不具备幂等性，重复调用会创建多个同名知识库。建议通过"先查询（ListIndices）、后创建"的逻辑实现幂等。调用 `CreateIndex` 后**必须**再调用 `SubmitIndexJob` 才能完成知识库构建，否则将得到空知识库。

### 知识库文档管理

| API | 说明 |
|-----|------|
| ListIndexDocuments | 查询知识库下的文件列表 |
| ListIndexFileDetails | 查询知识库下的文件详情 |
| DeleteIndexDocument | 删除知识库下的指定文件 |

### 知识库检索

`Retrieve` 接口用于在指定知识库中检索信息。支持通过阿里云百炼 SDK（AccessKey 认证）或 Spring AI Alibaba（API-Key 认证）两种方式调用。由于检索和匹配过程较复杂，响应时间可能较长，建议合理设置超时和重试策略。

### 切片管理

| API | 说明 |
|-----|------|
| ListChunks | 查询指定文件或知识库的切片列表 |
| UpdateChunk | 修改切片内容 |
| DeleteChunk | 删除指定切片 |

对于文档搜索或音视频搜索类知识库，`ListChunks` 查询指定文件的所有切片；对于数据查询或图片问答类知识库，则获取全部文本切片。详见 [CreateIndex - 创建知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-createindex.md)。

## 长期记忆

长期记忆 API 提供记忆体和记忆片段的管理能力，用于为智能体应用维护跨会话的上下文信息。

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
| ApplyTempStorageLease | 申请临时文件上传许可，用于获取临时存储空间的上传凭证 |
| GetAlipayUrl | 获取支付宝打赏 URL |
| GetAlipayTransferStatus | 查询支付宝打赏状态 |

## 通用约定

- **请求格式**：所有接口均通过 `POST` 方法调用，路径中包含 `{WorkspaceId}`
- **限流**：大多数接口限频 5 次/秒，`CreateIndex` 为 10 次/秒，遇限流请稍后重试
- **幂等性**：多数读取和删除接口具有幂等性；`CreateIndex` 不具有幂等性
- **分页**：列表接口统一采用 `MaxResults` + `NextToken` 分页模式
- **错误处理**：建议参考各接口文档中的错误码表和 [错误中心](https://api.aliyun.com/document/bailian/2023-12-29/errorCode) 处理异常

## 版本变更

API 版本标识为 `2023-12-29`，持续迭代中。近期主要变更包括新增 `UpdateIndex`（2026-01-19）、新增 `GetIndexMonitor`（2026-01-14）、`CreateIndex` 入参变更（2026-03-30）等。完整变更历史请参见 [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)。

## 来源文档

- [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)
- [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)
- [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)
- [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)
- [AddCategory - 新增类目](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addcategory.md)
- [ListCategory - 类目列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-listcategory.md)
- [DeleteCategory - 删除类目](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-deletecategory.md)
- [ApplyFileUploadLease - 申请文件上传租约](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-applyfileuploadlease.md)
- [ListFile - 文件列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-listfile.md)
- [AddFilesFromAuthorizedOss - 从已授权OSS Bucket中导入文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addfilesfromauthorizedoss.md)
- [AddFile - 添加文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addfile.md)
- [DescribeFile - 查询文件状态](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-describefile.md)
- [UpdateFileTag - 更新文件标签](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-updatefiletag.md)
- [DeleteFile - 删除文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-deletefile.md)
- [BatchUpdateFileTag - 批量更新文档标签](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-batchupdatefiletag.md)
- [GetParseSettings - 获取类目解析设置](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-getparsesettings.md)
- [GetAvailableParserTypes - 获取文件支持的解析器类型](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-getavailableparsertypes.md)
- [ChangeParseSetting - 修改类目解析设置](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-changeparsesetting.md)
- [AddTable - 添加表格](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addtable.md)
- [UpdateTableFromAuthorizedOss - 从已授权OSS Bucket中选择文件更新表格](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-updatetablefromauthorizedoss.md)
- [AddConnector - 新增连接器](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addconnector.md)
- [CreatePromptTemplate - 创建Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-createprompttemplate.md)
- [GetConnector - 获取连接器信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-getconnector.md)
- [GetPromptTemplate - 获取Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-getprompttemplate.md)
- [UpdatePromptTemplate - 更新Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-updateprompttemplate.md)
- [DeletePromptTemplate - 删除Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-deleteprompttemplate.md)
- [ListPromptTemplates - 获取Prompt模板列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-listprompttemplates.md)
- [CreateIndex - 创建知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-createindex.md)
- [GetIndexJobStatus - 查询知识库创建任务状态](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-getindexjobstatus.md)
- [SubmitIndexJob - 提交知识库创建任务](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-submitindexjob.md)
- [SubmitIndexAddDocumentsJob - 提交知识库追加任务](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-submitindexadddocumentsjob.md)
- [Retrieve - 检索知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-retrieve.md)
- [ListIndexDocuments - 查询知识库下的文件列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-listindexdocuments.md)
- [ListIndexFileDetails - 查询知识库下的文件详情](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-listindexfiledetails.md)
- [DeleteIndexDocument - 删除知识库下的文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-deleteindexdocument.md)
- [UpdateIndex - 更新知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-updateindex.md)
- [ListIndices - 查询知识库列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-listindices.md)
- [DeleteIndex - 删除知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-deleteindex.md)
- [ListChunks - 查询索引下的分片列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-listchunks.md)
- [DeleteChunk - 删除切片](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-deletechunk.md)
- [UpdateChunk - 修改切片](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-updatechunk.md)
- [GetIndexMonitor - 获取知识库监控数据](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-getindexmonitor.md)
- [GetAlipayUrl - 获取支付宝打赏URL](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-getalipayurl.md)
- [GetAlipayTransferStatus - 查询支付宝打赏状态](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-getalipaytransferstatus.md)
- [ApplyTempStorageLease - 申请临时文件上传许可](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-applytempstoragelease.md)
- [GetMemory - 获取长期记忆体](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-getmemory.md)
- [CreateMemory - 创建长期记忆体](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-creatememory.md)
- [UpdateMemory - 更新长期记忆体](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-updatememory.md)
- [DeleteMemory - 删除长期记忆体](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-deletememory.md)
- [ListMemories - 获取长期记忆体列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-listmemories.md)
- [CreateMemoryNode - 创建记忆片段](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-creatememorynode.md)
- [GetMemoryNode - 获取记忆片段](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-getmemorynode.md)
- [UpdateMemoryNode - 更新记忆片段](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-updatememorynode.md)
- [DeleteMemoryNode - 删除记忆片段](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-deletememorynode.md)
- [ListMemoryNodes - 获取记忆片段列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-listmemorynodes.md)
- [UpdateConnector - 编辑连接器](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-updateconnector.md)
- [DeleteFiles - 批量删除文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-deletefiles.md)





