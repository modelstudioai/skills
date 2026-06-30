# application component api reference

百炼（Model Studio）「应用组件」API 参考，对应接口版本 `2023-12-29`。该版本 API 围绕百炼应用组件的数据接入、Prompt 工程、知识库（RAG）、长期记忆等能力提供一组 RESTful 接口，供开发者以编程方式管理百炼应用所需的数据与配置资源。本文按功能模块梳理各接口的用途、调用要点与典型流程，便于快速定位。

## 概述与版本

- **接口版本**：`2023-12-29`，所有接口的 `Version` 公共参数取值为 `2023-12-29`。
- **服务入口**：通过百炼统一接入点调用，详见「服务接入点」。调用时需携带阿里云鉴权信息（AccessKey + 安全凭证），并按 RAM 授权策略授予对应接口权限。
- **风格**：RPC 风格（POP），请求通过 HTTP/HTTPS 发起，参数以 Query 或 Body 形式传递，返回值为 JSON。
- **版本说明**：该版本为应用组件 API 的基线版本，后续迭代以变更集（changeset）形式记录新增、变更与废弃接口。

## 鉴权与接入

- 调用方需持有有效的阿里云 AccessKey，并通过 RAM 子账号或角色授权对应接口的调用权限（`ram` 接口说明中列出各接口所需的 Action 与 Resource）。
- 接入点域名、Region 选择参见「服务接入点」文档；建议生产环境使用 HTTPS 并按Region就近接入。
- 公共参数包含 `AccessKeyId`、`Signature`、`Timestamp`、`Version` 等，签名规则遵循阿里云 POP 通用签名算法。

## 数据接入

数据接入是应用组件 API 的核心，覆盖「类目 → 文件 → 解析 → 结构化数据」的完整链路，并支持通过连接器从外部数据源拉取数据。

### 类目管理

类目（Category）用于对导入百炼的文件进行分组管理，是组织知识库与数据源的逻辑容器。

| 接口 | 说明 |
| --- | --- |
| ListCategory | 查询类目列表。 |
| AddCategory | 新增类目。 |
| DeleteCategory | 删除类目。 |

调用要点：删除类目前应确认其下文件已清理或迁移，避免悬挂引用。

### 文件管理

支持本地文件上传与从已授权 OSS Bucket 导入两种方式，并提供文件生命周期与标签管理。

| 接口 | 说明 |
| --- | --- |
| ApplyFileUploadLease | 申请文件上传租约，获取上传凭证与目标地址后再上传文件流。 |
| AddFile | 添加文件，将已上传的文件登记到指定类目。 |
| AddFilesFromAuthorizedOss | 从已授权 OSS Bucket 中批量导入文件。 |
| DescribeFile | 查询单个文件的处理状态（解析/索引进度等）。 |
| ListFile | 查询文件列表，支持按类目、标签等过滤。 |
| UpdateFileTag | 更新单个文件标签。 |
| BatchUpdateFileTag | 批量更新文档标签，适用于大批量元数据修正。 |
| DeleteFile | 删除单个文件。 |
| DeleteFiles | 批量删除文件。 |

典型流程：`ApplyFileUploadLease` → 上传文件流到租约地址 → `AddFile` 登记 → 轮询 `DescribeFile` 等待解析完成 → 按需 `UpdateFileTag`/`BatchUpdateFileTag`。

### 解析设置

控制文件被解析为知识库可消费文本的方式。

| 接口 | 说明 |
| --- | --- |
| GetParseSettings | 获取类目的解析设置。 |
| GetAvailableParserTypes | 获取指定文件支持的解析器类型。 |
| ChangeParseSetting | 修改类目解析设置。 |

调用要点：解析器类型与文件格式相关，先调用 `GetAvailableParserTypes` 确认可选项，再通过 `ChangeParseSetting` 落地配置。

### 表格与连接器

支持将结构化表格与外部数据源接入百炼。

| 接口 | 说明 |
| --- | --- |
| AddTable | 添加表格。 |
| UpdateTableFromAuthorizedOss | 从已授权 OSS Bucket 中选择文件更新表格内容。 |
| AddConnector | 新增连接器，配置外部数据源连接。 |
| GetConnector | 获取连接器信息。 |
| UpdateConnector | 编辑连接器配置。 |

## Prompt 工程

提供 Prompt 模板的 CRUD 能力，便于复用与版本管理。

| 接口 | 说明 |
| --- | --- |
| CreatePromptTemplate | 创建 Prompt 模板。 |
| GetPromptTemplate | 获取 Prompt 模板详情。 |
| UpdatePromptTemplate | 更新 Prompt 模板。 |
| DeletePromptTemplate | 删除 Prompt 模板。 |
| ListPromptTemplates | 获取 Prompt 模板列表。 |

调用要点：模板中可使用变量占位符，调用方在推理时填充变量；更新模板不会自动影响已基于旧版本生成的应用，需重新发布或绑定。

## 知识库（RAG）

知识库（Index）是百炼 RAG 检索的核心资源，提供创建、追加、检索、切片管理与监控等能力。

### 知识库与任务

| 接口 | 说明 |
| --- | --- |
| CreateIndex | 创建知识库。 |
| SubmitIndexJob | 提交知识库创建任务（异步）。 |
| SubmitIndexAddDocumentsJob | 提交知识库追加文档任务，向已有知识库增量入库。 |
| GetIndexJobStatus | 查询知识库创建/追加任务状态。 |
| UpdateIndex | 更新知识库配置。 |
| ListIndices | 查询知识库列表。 |
| DeleteIndex | 删除知识库。 |

典型流程：`CreateIndex` 创建空库 → `SubmitIndexJob` 或 `SubmitIndexAddDocumentsJob` 触发异步入库 → `GetIndexJobStatus` 轮询至完成 → 检索可用后按需 `UpdateIndex` 调整配置。

### 检索与文件

| 接口 | 说明 |
| --- | --- |
| Retrieve | 检索知识库，返回命中的切片内容，是 RAG 推理的关键调用。 |
| ListIndexFileDetails | 查询知识库下的文件详情。 |
| ListIndexDocuments | 查询知识库下的文件列表。 |
| DeleteIndexDocument | 删除知识库下的文件。 |

### 切片与监控

| 接口 | 说明 |
| --- | --- |
| ListChunks | 查询索引下的分片（切片）列表。 |
| UpdateChunk | 修改切片内容或元数据。 |
| DeleteChunk | 删除切片。 |
| GetIndexMonitor | 获取知识库监控数据（检索量、命中率等）。 |

调用要点：`Retrieve` 的检索质量依赖入库时的解析与切片策略；当检索结果不理想时，可通过 `ListChunks` + `UpdateChunk` 人工修正关键切片，或 `DeleteChunk` 清理低质内容。

## 长期记忆

长期记忆体（Memory）用于持久化 Agent 跨会话的记忆，记忆体下可挂载多个记忆片段（MemoryNode）。

### 记忆体

| 接口 | 说明 |
| --- | --- |
| CreateMemory | 创建长期记忆体。 |
| GetMemory | 获取长期记忆体。 |
| UpdateMemory | 更新长期记忆体。 |
| DeleteMemory | 删除长期记忆体。 |
| ListMemories | 获取长期记忆体列表。 |

### 记忆片段

| 接口 | 说明 |
| --- | --- |
| CreateMemoryNode | 创建记忆片段。 |
| GetMemoryNode | 获取记忆片段。 |
| UpdateMemoryNode | 更新记忆片段。 |
| DeleteMemoryNode | 删除记忆片段。 |
| ListMemoryNodes | 获取记忆片段列表。 |

调用要点：记忆片段是记忆体的子资源，删除记忆体时应同步清理其下片段，或依赖服务端级联删除策略。

## 其他

| 接口 | 说明 |
| --- | --- |
| ApplyTempStorageLease | 申请临时文件上传许可，用于短期临时存储场景。 |
| GetAlipayUrl | 获取支付宝打赏 URL。 |
| GetAlipayTransferStatus | 查询支付宝打赏状态。 |

## 调用约定与最佳实践

- **幂等性**：文件上传、知识库任务提交等为异步接口，务必通过 `DescribeFile` / `GetIndexJobStatus` 轮询最终状态，不要仅依赖提交返回。
- **批量操作**：优先使用批量接口（`BatchUpdateFileTag`、`DeleteFiles`、`SubmitIndexAddDocumentsJob`）以减少请求次数与鉴权开销。
- **OSS 授权导入**：使用 `AddFilesFromAuthorizedOss` / `UpdateTableFromAuthorizedOss` 前，需先在百炼控制台完成 OSS Bucket 授权，避免因权限不足导致导入失败。
- **资源清理顺序**：删除类目、知识库、记忆体等父资源前，先清理其下子资源（文件、切片、记忆片段），防止残留与计费。
- **监控观测**：知识库上线后定期调用 `GetIndexMonitor` 关注检索量与命中率，结合 `ListChunks` 抽检切片质量，持续优化 RAG 效果。

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


