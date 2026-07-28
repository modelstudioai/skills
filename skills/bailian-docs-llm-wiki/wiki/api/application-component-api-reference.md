# application component api reference

阿里云百炼平台组件 OpenAPI（`bailian/2023-12-29`）是一组管控类接口，覆盖数据连接（原应用数据）、Prompt 模板、知识库（Index）三大能力域，以及切片管理、长期记忆等扩展接口。该 API 采用 ROA 签名风格，官方强烈建议通过多语言预置 SDK 调用而非自签名对接，详见 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)。

## 接入与鉴权

- **服务接入点**：目前支持华北2（北京，`bailian.cn-beijing.aliyuncs.com`）与新加坡（`bailian.ap-southeast-1.aliyuncs.com`）两个地域，均提供公网与 VPC 接入地址，完整列表见 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)。
- **凭证**：使用阿里云 AccessKey（非百炼 API-Key）签名调用。建议创建仅具备 API 访问权限的 RAM 用户，并按最小权限原则（PoLP）授权。
- **RAM 授权**：产品 RamCode 为 `sfm`，授权粒度为操作级。RAM 用户（子账号）通常需要 `AliyunBailianDataFullAccess` 策略（只读类接口也可用 `AliyunBailianDataReadOnlyAccess`），并**加入一个[业务空间](../concepts/workspace.md)**后才能调用；阿里云账号（主账号）可直接调用。各接口对应的 Action（如 `sfm:CreateIndex`、`sfm:Retrieve`）见 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)。
- **公共路径参数**：几乎所有接口都以 `WorkspaceId`（[业务空间](../concepts/workspace.md) ID，形如 `llm-xxxx`）作为路径参数，调用前需先确认目标资源所在的[业务空间](../concepts/workspace.md)。

## 能力分组与核心接口

### 数据连接（原应用数据）

管理类目、文件、解析设置与连接器：

- **类目**：`AddCategory`（每个业务空间最多 500 个类目）、`ListCategory`、`DeleteCategory`。
- **文件导入**：标准流程为 `ApplyFileUploadLease`（申请上传租约）→ 上传文件 → `AddFile`（凭 `LeaseId` 导入，并指定 `Parser` 解析器，如 `DOCMIND`、`DOCMIND_LLM_VERSION`、`DASH_QWEN_VL_PARSER`、`AUTO_SELECT` 等）；也可用 `AddFilesFromAuthorizedOss` 直接从同账号已授权的 OSS Bucket 导入。
- **文件管理**：`DescribeFile`（查解析状态）、`ListFile`、`UpdateFileTag` / `BatchUpdateFileTag`（标签最多 100 个、总长不超过 700 字符）、`DeleteFile` / `DeleteFiles`（单次最多 20 个，仅能删除 `PARSE_FAILED` 或 `PARSE_SUCCESS` 状态的文件）。
- **解析设置**：`GetParseSettings`、`GetAvailableParserTypes`（按扩展名查询可用解析器）、`ChangeParseSetting`（为特定文件类型指定解析方式）。
- **连接器与表格**：`AddConnector`（当前仅支持文件类型连接器）、`GetConnector`、`UpdateConnector`、`AddTable`、`UpdateTableFromAuthorizedOss`。

> **注意**：[AddConnector](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addconnector.md) 的接口说明中写的是需要 `sfm:AddCategory` 权限点，而其授权信息表为 `sfm:AddConnector`，两处不一致，疑为文档笔误，实际授权建议以 `AliyunBailianDataFullAccess` 策略整体覆盖。

> **注意**：数据表（结构化表格）的新增、上传数据与删除均**不支持通过 API 完成**，需在控制台的应用数据页面操作；`ListCategory` 也暂不支持查询数据表。

### Prompt 工程

`CreatePromptTemplate`、`GetPromptTemplate`、`UpdatePromptTemplate`（PATCH，增量更新）、`DeletePromptTemplate`、`ListPromptTemplates`（支持按名称关键字、`System`/`Custom` 类型过滤及 `nextToken` 分页）。模板内容用 `${变量名}` 声明变量，返回参数中会解析出 `variables` 列表。暂不支持文生图 Prompt 模板。

### 知识库（Index）

- **创建**：`CreateIndex` 仅初始化知识库作业，**必须**随后调用 `SubmitIndexJob` 才能真正完成构建，否则得到空知识库，完整流程见 [CreateIndex - 创建知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-createindex.md)。`CreateIndex` 不具幂等性，重复调用会产生多个同名知识库，建议“先查询、后创建”。
- **追加与状态**：`SubmitIndexAddDocumentsJob`（追加前需先用 `AddFile` 完成导入；不支持数据查询/图片问答类知识库）、`GetIndexJobStatus`（凭 `JobId` + `IndexId` 轮询任务状态，高峰期任务可能耗时数小时）。
- **检索**：`Retrieve` 在指定知识库中检索，可直接使用而不依赖百炼应用；响应包含复杂检索匹配，延迟可能较长，需合理设置超时与重试。也可通过应用调用的 `rag_options` 传入 `IndexId` 关联使用。
- **管理**：`ListIndices`、`UpdateIndex`（可调整名称、`RerankMinScore`、`DenseSimilarityTopK` 与 `SparseSimilarityTopK`——二者之和须 ≤ 200，以及标准版/旗舰版规格）、`DeleteIndex`（若知识库被应用引用需先在控制台解除关联；删除不可逆，但不影响应用数据中的文件）、`ListIndexDocuments` / `ListIndexFileDetails`（按 `DocumentStatus` 如 `FINISH`、`INSERT_ERROR` 过滤）、`DeleteIndexDocument`（仅能删除 `FINISH` 或 `INSERT_ERROR` 状态的文件）。
- **切片**：`ListChunks`（查询文本切片）、`UpdateChunk`（修改切片 content/title、控制是否参与检索，仅支持文档搜索类知识库）、`DeleteChunk`、`AddChunk`。

> **注意**：`ListIndexDocuments` 与 `ListIndexFileDetails` 的接口说明均写需要 `sfm:ListIndexFiles` 权限点，但 `ListIndexFileDetails` 授权表中的操作名为 `sfm:ListIndexFileDetails`，命名不一致；同样 `ListChunks` 对应的权限点是 `sfm:ChunkList`、`ListIndices` 对应 `sfm:ListIndex`，与接口名并非一一同名，编写细粒度 RAM 策略时需逐一核对。

### 其他

临时存储租约（`ApplyTempStorageLease`）、支付宝打赏（`GetAlipayUrl` / `GetAlipayTransferStatus`）以及长期记忆体与记忆片段的完整 CRUD（`CreateMemory` / `GetMemory` / `UpdateMemory` / `DeleteMemory` / `ListMemories`、`CreateMemoryNode` 等）。

## 使用要点与限制

- **[限流](../concepts/rate-limit.md)**：各接口独立[限流](../concepts/rate-limit.md)，常见为 5 次/秒（类目、连接器、列表类）或 10 次/秒（文件、知识库操作类），`ListIndexDocuments` 为 15 次/秒。触发[限流](../concepts/rate-limit.md)后应退避重试。
- **幂等性**：查询与删除类接口普遍幂等；创建类接口（`AddCategory`、`AddFile`、`CreateIndex`、`SubmitIndexJob` 等）不幂等，需要调用方自行防重。
- **分页**：数据连接类接口使用 `MaxResults` + `NextToken` 令牌分页；知识库列表类接口多用 `PageNumber` + `PageSize`。
- **删除语义**：`DeleteFile` 删除应用数据中的文件不影响已构建知识库；删除知识库中的文件需用 `DeleteIndexDocument`，且不会反向删除应用数据，两者相互独立。
- **版本变更**：该 API 仍在持续演进（如 `CreateIndex` 入参多次变更、新增 `UpdateIndex` / `GetIndexMonitor`），升级 SDK 前建议核对 [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)。

> **注意**：`GetIndexJobStatus` 文档自身建议“调用间隔 5 秒以上”，而 `SubmitIndexAddDocumentsJob` 文档中提示其限流为“不高于 20 次/分钟”（约 3 秒一次），两处口径略有出入，保守起见按每 5 秒以上轮询一次处理。

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
- [AddChunk - 新增切片](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-addchunk.md)


