# application component api reference

阿里云百炼平台应用组件 API（`bailian/2023-12-29`）提供了一组 ROA 风格的 OpenAPI，覆盖数据连接、知识库、[Prompt 工程](../concepts/prompt-engineering.md)等核心能力的全生命周期管理。开发者可通过官方 SDK 或自签名方式调用这些接口，在[业务空间](../concepts/workspace.md)维度下完成数据管理与知识库构建的自动化集成。所有接口均需要 AccessKey 认证，建议使用 RAM 用户并遵循最小权限原则。

## 接入准备

### 服务接入点

API 当前支持两个地域，详见 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)：

| 地域 | 地域 ID | 公网接入地址 | VPC 接入地址 |
|------|---------|-------------|-------------|
| 华北2（北京） | cn-beijing | bailian.cn-beijing.aliyuncs.com | bailian-vpc.cn-beijing.aliyuncs.com |
| 新加坡 | ap-southeast-1 | bailian.ap-southeast-1.aliyuncs.com | bailian-vpc.ap-southeast-1.aliyuncs.com |

### 认证与授权

- 推荐创建 RAM 用户并配置 AccessKey，避免使用阿里云主账号。
- RAM 用户需获取相应权限策略（如 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess`）并加入[业务空间](../concepts/workspace.md)后方可调用 API。
- 产品 RAM 代码为 `sfm`，授权粒度为操作级。详细权限点定义参见 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)。

### 调用方式

推荐使用官方 [SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)，支持多语言。自签名对接较为复杂，建议联系技术支持（钉钉群：147535001692）获取指导。

## 数据连接（原应用数据）

数据连接 API 管理文件的上传、分类和解析，是构建知识库的前置步骤。

### 类目管理

| 接口 | 说明 | 限流 |
|------|------|------|
| AddCategory | 新增类目（每空间最多 500 个） | 5 次/秒 |
| ListCategory | 查询类目列表（支持分页） | 5 次/秒 |
| DeleteCategory | 删除指定类目 | 5 次/秒 |

> **注意**：不支持通过 API 新增或查询数据表，需通过控制台操作。

### 文件管理

文件上传采用"租约"机制：先调用 `ApplyFileUploadLease` 获取上传地址，将文件 PUT 到该地址，再调用 `AddFile` 将文件导入百炼。也可通过 `AddFilesFromAuthorizedOss` 从已授权 OSS Bucket 批量导入。

| 接口 | 说明 | 限流 |
|------|------|------|
| ApplyFileUploadLease | 申请上传租约 | 10 次/秒 |
| AddFile | 导入文件到数据连接 | 10 次/秒 |
| AddFilesFromAuthorizedOss | 从授权 OSS 导入 | 5 次/秒 |
| ListFile | 查询文件列表 | 5 次/秒 |
| DescribeFile | 查询文件状态 | 10 次/秒 |
| UpdateFileTag / BatchUpdateFileTag | 更新文件标签（单个/批量） | 5 次/秒 |
| DeleteFile | 删除文件（仅限 PARSE_FAILED 或 PARSE_SUCCESS 状态） | 10 次/秒 |

文件导入时需指定解析器类型，可选项包括：
- `DOCMIND`（智能文档解析）
- `DOCMIND_DIGITAL`（电子文档解析）
- `DOCMIND_LLM_VERSION`（大模型文档解析）
- `DASH_QWEN_VL_PARSER`（Qwen VL 解析）
- `DOCMIND_LLM_VERSION_MEDIA`（音视频解析）
- `AUTO_SELECT`（自动选择）

可通过 `GetAvailableParserTypes` 查询指定文件类型支持的解析器，通过 `GetParseSettings` / `ChangeParseSetting` 管理类目级别的默认解析配置。

### 连接器与表格

| 接口 | 说明 |
|------|------|
| AddConnector | 新增连接器（当前仅支持文件类型） |
| GetConnector | 获取连接器信息 |
| AddTable | 为表格连接器添加表格 |
| UpdateTableFromAuthorizedOss | 从授权 OSS 更新表格数据 |

## 知识库

知识库 API 支持创建和管理两类知识库：基于文档/音视频的非结构化知识库，以及用于数据查询/图片问答的结构化知识库。详细流程参见 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)。

### 创建流程

知识库创建为异步过程，典型调用链：

1. `CreateIndex` — 初始化知识库（指定名称、类型、文档列表等）
2. `SubmitIndexJob` — 提交创建任务开始构建
3. `GetIndexJobStatus` — 轮询任务状态（建议间隔 5 秒以上）

> **注意**：`CreateIndex` 仅初始化作业，**必须**后续调用 `SubmitIndexJob` 才能完成创建，否则会得到一个空知识库。该接口不具幂等性，重复调用会创建多个同名知识库。

### 文件追加与删除

| 接口 | 说明 |
|------|------|
| SubmitIndexAddDocumentsJob | 向已有知识库追加文件（不支持结构化知识库） |
| DeleteIndexDocument | 删除知识库中的文件（仅限 INSERT_ERROR 或 FINISH 状态，不可逆） |
| ListIndexDocuments | 查询知识库文件列表 |
| ListIndexFileDetails | 查询文件详情 |

> **注意**：`DeleteIndexDocument` 删除的是知识库中的文件索引，不会影响数据连接中已导入的源文件。`DeleteFile` 删除的是数据连接中的文件，不会影响已构建好的知识库。

### 检索

`Retrieve` 接口用于在知识库中执行语义检索，支持向量检索与关键词检索的混合模式。由于涉及复杂匹配，响应时间可能较长，建议合理设置超时策略。也可通过 [Spring AI Alibaba](https://help.aliyun.com/zh/model-studio/spring-ai-alibaba-integrate-knowledge-base) 配合 API-Key 调用。

### 知识库管理

| 接口 | 说明 |
|------|------|
| UpdateIndex | 更新知识库配置（名称、检索参数、规格等） |
| ListIndices | 查询知识库列表 |
| DeleteIndex | 删除知识库（不可逆，需先解除应用关联） |
| GetIndexMonitor | 获取存储和 QPS 监控数据（查询范围最大 30 天） |

`UpdateIndex` 支持调整的关键参数包括：
- `DenseSimilarityTopK` / `SparseSimilarityTopK`：向量/关键词检索 Top K（两者之和不超过 200）
- `RerankMinScore`：排序最低分数（0-1）
- `PipelineCommercialType`：规格类型（standard / enterprise）

### 切片管理

| 接口 | 说明 |
|------|------|
| ListChunks | 查询文本切片列表 |
| UpdateChunk | 修改切片内容和标题（仅支持文档搜索类知识库） |
| DeleteChunk | 删除切片（硬删除，不可恢复） |

## [Prompt 工程](../concepts/prompt-engineering.md)

Prompt 模板 API 支持创建、获取、更新、删除和列表查询五个操作，用于管理可复用的 Prompt 模板。模板内容支持 `${variable}` 格式的变量占位符。

| 接口 | 说明 |
|------|------|
| CreatePromptTemplate | 创建模板（暂不支持文生图模板） |
| GetPromptTemplate | 获取模板详情 |
| UpdatePromptTemplate | 增量更新模板 |
| DeletePromptTemplate | 删除模板 |
| ListPromptTemplates | 列表查询（支持按名称搜索、类型过滤、分页） |

模板类型分为 `System`（系统预置）和 `Custom`（用户自定义）。

## 通用注意事项

- **[业务空间](../concepts/workspace.md)**：所有 API 均以 `WorkspaceId` 为顶层作用域，操作前需确保目标资源在正确的[业务空间](../concepts/workspace.md)中。
- **幂等性**：部分接口具有幂等性（如查询类接口），部分不具备（如 `AddCategory`、`CreateIndex`），调用前请查阅各接口文档。
- **限流**：所有接口均有限流限制（通常 5-15 次/秒），超限时返回限流错误，需稍后重试。
- **SDK 版本**：建议始终使用最新版 SDK 以获得完整功能支持和最佳兼容性。
- **版本变更**：API 持续迭代，近期变更包括 `CreateIndex` 入参调整、`DescribeFile` 返回结构变更、`UpdateIndex` 和 `GetIndexMonitor` 新增等，详见 [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)。

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



