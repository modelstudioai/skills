# application component api reference

本 API 参考文档面向开发者，完整描述百炼平台 `application component`（应用组件）层提供的核心 OpenAPI 接口能力，聚焦于**数据连接（原应用数据）**和**知识库**两大核心功能模块。所有接口均基于 `bailian/2023-12-29` 版本，采用标准 ROA 签名机制，支持通过官方 SDK 或自签名方式调用。开发者需提前配置 RAM 权限与业务空间访问权限方可使用。

## 支持的模型/功能

API 当前提供两类核心能力：

1.  **数据连接（原应用数据）**：管理非结构化文件与结构化表格的生命周期。包括类目（Category）的增删查、文件（File）的上传（含 OSS 直传）、解析、标签管理、元信息查询等。该模块是知识库的数据源基础。[数据连接（原应用数据）](../../raw/_short/api-bailian-2023-12-29-dir-data-connection-origi-a1f7f2601bd6f7cf.md) 文档详细列出了所有相关接口。
2.  **知识库（Knowledge Base）**：构建、管理与检索私有知识。支持创建文档搜索、数据查询、图片问答、音视频搜索四类知识库；支持文件批量导入、切片（Chunk）级细粒度增删改查；支持向量/关键词混合检索（`Retrieve`）；并提供监控数据（`GetIndexMonitor`）用于性能分析。[知识库](../../raw/_short/api-bailian-2023-12-29-dir-knowledge-base-f6f202ad9694348f.md) 文档是此功能的总览入口。

> **注意**：文档 1 和文档 4 均提及“数据连接（原应用数据）”和“知识库”为两大主干目录，但文档 1 的 API 概览部分仅列举了数据连接下的部分接口（如 `AddCategory`, `ApplyFileUploadLease`），而未列出知识库相关接口，存在信息不完整。应以文档 4 的 [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md) 为准。

## 关键参数

- **`WorkspaceId`（业务空间 ID）**：几乎所有接口的必需路径参数，标识操作所属的业务空间。获取方式请参见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。
- **`CategoryId` / `FileId` / `IndexId` / `ConnectorId`**：各类资源的唯一标识符，通常由上游接口（如 `AddCategory`, `AddFile`, `CreateIndex`, `AddConnector`）返回，后续操作需依赖此 ID。
- **`Parser`（解析器类型）**：在 `AddFile` 和 `ChangeParseSetting` 等接口中指定，决定文件内容的解析策略。可选值包括 `DOCMIND`, `DOCMIND_DIGITAL`, `AUTO_SELECT` 等，具体列表及适用场景请参考 [GetAvailableParserTypes](../../raw/_short/api-bailian-2023-12-29-getavailableparsertypes-09561c4e0fb505d5.md) 接口返回结果。
- **分页参数**：`List*` 类接口（如 `ListCategory`, `ListFile`, `ListIndices`）普遍支持 `MaxResults`/`PageSize` 和 `NextToken`/`PageNumber` 进行分页，避免单次请求数据量过大。

## 使用方式

1.  **准备环境**：首先确保已获取阿里云账号或具备最小权限的 RAM 用户 AccessKey，并为其授予 `AliyunBailianDataFullAccess`（读写）或 `AliyunBailianDataReadOnlyAccess`（只读）策略。详细授权说明见 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)。
2.  **选择接入点**：根据部署地域选择对应的服务接入点（Endpoint），例如华北2（北京）为 `bailian.cn-beijing.aliyuncs.com`。完整列表见 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)。
3.  **调用流程**：
    - **数据连接**：典型流程为 `AddCategory` → `ApplyFileUploadLease` → 上传文件 → `AddFile` → `ListFile`。
    - **知识库**：典型流程为 `CreateIndex` → `SubmitIndexJob`（等待完成）→ `AddFile`（上传数据）→ `SubmitIndexAddDocumentsJob`（等待完成）→ `Retrieve`（检索）。对于切片级操作，可直接使用 `AddChunk`/`ListChunks`/`DeleteChunk`。
4.  **调试与开发**：强烈推荐使用 [OpenAPI Explorer](https://api.aliyun.com/api-tools/explorer/bailian) 进行在线调试，并利用其生成的 SDK 代码示例快速集成。

## 限制和注意事项

- **幂等性**：`List*`, `Describe*`, `Get*`, `Retrieve`, `DeleteIndexDocument`, `DeleteIndex`, `DeleteChunk`, `UpdateChunk` 等多数查询与删除类接口具有幂等性；而 `Add*`, `Submit*`, `Apply*` 等创建类接口不具备幂等性，重复调用可能产生冗余资源。
- **限流策略**：各接口均有明确的 QPS 限制（如 `AddCategory` 为 5 次/秒，`AddFile` 为 10 次/秒），超限将返回 `429 Too Many Requests`。生产环境需实现重试退避逻辑。
- **数据一致性**：`DeleteFile` 仅删除应用数据中的文件，**不会**同步删除已构建的知识库中的索引；反之，`DeleteIndexDocument` 仅删除知识库索引，**不会**删除应用数据中的原始文件。二者需按需独立调用。
- **功能边界**：API **不支持**通过接口新增或删除数据表（Table），此类操作必须通过控制台完成。`AddTable` 接口虽存在，但其文档（文档 20）与多处其他文档（如文档 1, 5, 6）中“不支持通过 API 新增数据表”的声明相矛盾。> **注意**：文档 6 (`AddCategory`)、文档 7 (`ListCategory`)、文档 15 (`DeleteFile`) 等多处明确声明“不支持通过 API 新增/删除数据表”，而文档 20 (`AddTable`) 却提供了该功能的接口说明，构成明显矛盾。开发者应以控制台操作为准，谨慎对待 `AddTable` 及相关表格接口。
- **安全最佳实践**：严禁使用主账号 AccessKey。务必遵循最小权限原则，为 RAM 用户分配精确到 `Action` 级别的权限策略。

## 来源文档

- [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)
- [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)
- [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)
- [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md)
- [数据连接（原应用数据）](../../raw/_short/api-bailian-2023-12-29-dir-data-connection-origi-a1f7f2601bd6f7cf.md)
- [AddCategory](../../raw/_short/api-bailian-2023-12-29-addcategory-e2fe0e0435ed504e.md)
- [ListCategory](../../raw/_short/api-bailian-2023-12-29-listcategory-2521532ef3e828b3.md)
- [DeleteCategory - 删除类目](../../raw/_short/api-bailian-2023-12-29-deletecategory-9838436bd2db3113.md)
- [AddFile](../../raw/_short/api-bailian-2023-12-29-addfile-8c254b3500bc50bc.md)
- [ApplyFileUploadLease](../../raw/_short/api-bailian-2023-12-29-applyfileuploadlease-39e8ca15e0e9561a.md)
- [ListFile](../../raw/_short/api-bailian-2023-12-29-listfile-360209e3a2479f14.md)
- [AddFilesFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-addfilesfromauthorizedoss-879556d685a301b3.md)
- [DescribeFile](../../raw/_short/api-bailian-2023-12-29-describefile-020886c28a208bf2.md)
- [UpdateFileTag](../../raw/_short/api-bailian-2023-12-29-updatefiletag-f84d2af6a45d6553.md)
- [DeleteFile](../../raw/_short/api-bailian-2023-12-29-deletefile-7e0409a458195fe2.md)
- [BatchUpdateFileTag](../../raw/_short/api-bailian-2023-12-29-batchupdatefiletag-34a8f009de66cb8b.md)
- [DeleteFiles](../../raw/_short/api-bailian-2023-12-29-deletefiles-96ef0815114e4e37.md)
- [GetParseSettings - 获取类目解析设置](../../raw/_short/api-bailian-2023-12-29-getparsesettings-522514560c54f49f.md)
- [GetAvailableParserTypes - 获取文件支持的解析器类型](../../raw/_short/api-bailian-2023-12-29-getavailableparsertypes-09561c4e0fb505d5.md)
- [AddTable](../../raw/_short/api-bailian-2023-12-29-addtable-6726351659db288d.md)
- [UpdateTableFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-updatetablefromauthorized-d7436828bcf51602.md)
- [ChangeParseSetting](../../raw/_short/api-bailian-2023-12-29-changeparsesetting-59a7c69675f499ad.md)
- [GetConnector](../../raw/_short/api-bailian-2023-12-29-getconnector-cb2e485a0efd52f7.md)
- [AddConnector](../../raw/_short/api-bailian-2023-12-29-addconnector-7a3c9650409710fe.md)
- [UpdateConnector](../../raw/_short/api-bailian-2023-12-29-updateconnector-6a24905a7d201597.md)
- [知识库](../../raw/_short/api-bailian-2023-12-29-dir-knowledge-base-f6f202ad9694348f.md)
- [GetIndexJobStatus - 查询知识库创建或追加任务状态](../../raw/_short/api-bailian-2023-12-29-getindexjobstatus-1e88b6ccfffe0fe4.md)
- [CreateIndex - 创建知识库](../../raw/_short/api-bailian-2023-12-29-createindex-8bc613c75f8af371.md)
- [SubmitIndexAddDocumentsJob - 提交知识库文件追加任务](../../raw/_short/api-bailian-2023-12-29-submitindexadddocumentsjo-ec4f5cf285e2c447.md)
- [SubmitIndexJob - 提交知识库创建任务](../../raw/_short/api-bailian-2023-12-29-submitindexjob-63b38294171880d4.md)
- [ListIndexDocuments - 查询知识库文件列表](../../raw/_short/api-bailian-2023-12-29-listindexdocuments-9f0db0388c421903.md)
- [Retrieve - 检索知识库](../../raw/_short/api-bailian-2023-12-29-retrieve-c8e6b8d718a30a84.md)
- [ListIndexFileDetails - 查询知识库文件详情](../../raw/_short/api-bailian-2023-12-29-listindexfiledetails-0e2036d0ef0d8fe8.md)
- [DeleteIndexDocument - 删除知识库下的文件](../../raw/_short/api-bailian-2023-12-29-deleteindexdocument-0792a83f5a741348.md)
- [ListIndices - 查询知识库列表](../../raw/_short/api-bailian-2023-12-29-listindices-c555173be752eaaf.md)
- [UpdateIndex - 更新知识库](../../raw/_short/api-bailian-2023-12-29-updateindex-551997e1d335e340.md)
- [AddChunk - 新增切片](../../raw/_short/api-bailian-2023-12-29-addchunk-1607bcddf6713fd9.md)
- [ListChunks - 查询索引下的分片列表](../../raw/_short/api-bailian-2023-12-29-listchunks-30a6c87b93a583c6.md)
- [DeleteIndex - 删除知识库](../../raw/_short/api-bailian-2023-12-29-deleteindex-500502bd6df1c49c.md)
- [DeleteChunk - 删除切片](../../raw/_short/api-bailian-2023-12-29-deletechunk-d249422088735d90.md)
- [UpdateChunk - 修改切片](../../raw/_short/api-bailian-2023-12-29-updatechunk-589b46fcc24261f8.md)
- [GetIndexMonitor - 获取知识库监控数据](../../raw/_short/api-bailian-2023-12-29-getindexmonitor-3a609181d5c9c034.md)
- [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)


