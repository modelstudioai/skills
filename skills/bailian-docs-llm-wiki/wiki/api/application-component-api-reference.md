# application component api reference

本 API 参考文档面向开发者，系统性地描述了百炼平台 `application component`（应用组件）层提供的核心 OpenAPI 能力，覆盖数据连接（原应用数据）、知识库两大核心功能模块。所有接口均基于 `bailian/2023-12-29` 版本，采用标准 ROA 签名机制，支持多语言 SDK 快速集成。开发者需通过 RAM 子账号进行最小权限授权，并在指定业务空间内调用。

## 支持的模型/功能

`application component` API 不直接提供大模型推理能力，而是聚焦于**数据接入、组织与检索增强（RAG）基础设施**，主要包含以下两类功能：

- **数据连接（原应用数据）**：用于管理非结构化文件和结构化表格数据。支持类目（Category）的增删查、文件（File）的上传（含 OSS 授权导入）、解析、标签管理、元数据查询等全生命周期操作。该模块是知识库的数据源基础，[API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)中明确指出“不支持通过 API 新增数据表”，但后续文档 [AddTable](../../raw/_short/api-bailian-2023-12-29-addtable-6726351659db288d.md) 已提供该能力，表明此为过时信息。
- **知识库（Knowledge Base）**：提供完整的 RAG 服务链路，包括知识库（Index）的创建、更新、删除、监控；文件的索引构建（SubmitIndexJob）、追加（SubmitIndexAddDocumentsJob）与状态查询（GetIndexJobStatus）；以及最终的语义检索（Retrieve）。支持文档搜索、数据查询、图片问答、音视频搜索等多种知识库类型，其能力边界在 [CreateIndex](../../raw/_short/api-bailian-2023-12-29-createindex-8bc613c75f8af371.md) 文档中有详细说明。

> **注意**：文档 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md) 中声明“不支持通过 API 新增数据表”，但独立的 [AddTable](../../raw/_short/api-bailian-2023-12-29-addtable-6726351659db288d.md) 接口已明确提供此功能，且其接口说明、权限点（`sfm:AddTable`）和请求语法均完整。因此，`API概览`中的该描述已过时，应以 `AddTable` 文档为准。

## 关键参数

所有 API 均需在路径或请求体中传递关键标识参数，确保资源定位与操作安全：

- **`WorkspaceId`（业务空间 ID）**：几乎所有接口的必填路径参数，用于限定操作范围。必须通过百炼控制台获取，当前版本无 API 可枚举业务空间列表（见 [ListIndexDocuments](../../raw/_short/api-bailian-2023-12-29-listindexdocuments-9f0db0388c421903.md) 说明）。
- **`CategoryId`（类目 ID）**：用于文件归属管理，由 `AddCategory` 接口返回，是 `AddFile`、`ListFile`、`ChangeParseSetting` 等接口的关键输入。
- **`FileId`（文件 ID）**：文件在应用数据中的唯一标识，由 `AddFile` 接口返回，是 `DescribeFile`、`DeleteFile`、`UpdateFileTag`、`DeleteIndexDocument` 等接口的核心参数。
- **`IndexId`（知识库 ID）**：知识库的唯一标识，由 `CreateIndex` 接口返回，是 `SubmitIndexJob`、`Retrieve`、`ListIndexDocuments`、`DeleteIndex` 等所有知识库操作的必需参数。
- **`Parser`（解析器）**：在 `AddFile` 和 `ChangeParseSetting` 接口中指定，用于控制文件解析逻辑。有效值包括 `DOCMIND`、`DOCMIND_DIGITAL`、`AUTO_SELECT` 等，具体可调用 `GetAvailableParserTypes` 查询支持列表。

## 使用方式

1. **环境准备**：首先在阿里云 RAM 控制台创建子账号，授予其 `AliyunBailianDataFullAccess`（读写）或 `AliyunBailianDataReadOnlyAccess`（只读）策略，并将其加入目标业务空间。强烈建议遵循最小权限原则，避免使用主账号 AccessKey。
2. **SDK 集成（推荐）**：下载并安装最新版 [阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)，它已封装签名、重试、限流等复杂逻辑。例如，调用 `AddCategory` 仅需初始化客户端并传入参数。
3. **自签名对接（备选）**：若需自定义签名，必须严格遵循 [ROA](https://help.aliyun.com/zh/sdk/product-overview/roa-mechanism) 机制。由于流程复杂（约 5 个工作日），官方强烈建议加入钉钉群（147535001692）寻求技术支持。
4. **典型工作流**：
   - **数据准备**：`AddCategory` → `ApplyFileUploadLease` → `AddFile`（或 `AddFilesFromAuthorizedOss`）。
   - **知识库构建**：`CreateIndex` → `SubmitIndexJob`（等待 `GetIndexJobStatus` 返回成功）→ `Retrieve`。
   - **知识库更新**：`AddFile`（新文件）→ `SubmitIndexAddDocumentsJob`（追加索引）。
5. **调试工具**：所有接口均支持在 [OpenAPI Explorer](https://api.aliyun.com/explorer) 中在线调试，可自动生成各语言 SDK 示例代码。

## 限制和注意事项

- **限流策略**：不同接口有严格的 QPS 限制，例如 `AddCategory`、`ListCategory`、`DeleteCategory` 为 5 次/秒；`ApplyFileUploadLease`、`AddFile`、`Retrieve` 为 10 次/秒；`ListIndexDocuments` 为 15 次/秒。超限将返回错误，需实现指数退避重试。
- **幂等性**：多数查询类接口（如 `ListCategory`, `ListFile`, `GetIndexJobStatus`）具有幂等性，可安全重试；而创建类（`AddCategory`, `AddFile`）和删除类（`DeleteCategory`, `DeleteFile`）接口不具备幂等性，重复调用可能导致意外结果（如创建多个同名类目）。
- **数据一致性**：`DeleteFile` 仅删除应用数据中的文件，不影响已构建的知识库；反之，`DeleteIndexDocument` 仅删除知识库索引，不影响原始应用数据文件。二者不可混淆。
- **功能边界**：`application component` API 不处理模型推理，也不支持直接通过 API 创建或管理智能体（Agent）应用本身，这些属于更高层级的 `agent component` 范畴。
- **地域与接入点**：服务支持多个地域，如华北2（北京）和新加坡，需根据业务部署选择对应的公网或 VPC 接入地址，详情见 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md) 文档。

## 来源文档

- [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)
- [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)
- [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)
- [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md)
- [数据连接（原应用数据）](../../raw/_short/api-bailian-2023-12-29-dir-data-connection-origi-a1f7f2601bd6f7cf.md)
- [AddCategory](../../raw/_short/api-bailian-2023-12-29-addcategory-e2fe0e0435ed504e.md)
- [ListCategory](../../raw/_short/api-bailian-2023-12-29-listcategory-2521532ef3e828b3.md)
- [DeleteCategory - 删除类目](../../raw/_short/api-bailian-2023-12-29-deletecategory-9838436bd2db3113.md)
- [ApplyFileUploadLease](../../raw/_short/api-bailian-2023-12-29-applyfileuploadlease-39e8ca15e0e9561a.md)
- [AddFile](../../raw/_short/api-bailian-2023-12-29-addfile-8c254b3500bc50bc.md)
- [AddFilesFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-addfilesfromauthorizedoss-879556d685a301b3.md)
- [ListFile](../../raw/_short/api-bailian-2023-12-29-listfile-360209e3a2479f14.md)
- [DescribeFile](../../raw/_short/api-bailian-2023-12-29-describefile-020886c28a208bf2.md)
- [UpdateFileTag](../../raw/_short/api-bailian-2023-12-29-updatefiletag-f84d2af6a45d6553.md)
- [BatchUpdateFileTag](../../raw/_short/api-bailian-2023-12-29-batchupdatefiletag-34a8f009de66cb8b.md)
- [DeleteFile](../../raw/_short/api-bailian-2023-12-29-deletefile-7e0409a458195fe2.md)
- [DeleteFiles](../../raw/_short/api-bailian-2023-12-29-deletefiles-96ef0815114e4e37.md)
- [GetParseSettings - 获取类目解析设置](../../raw/_short/api-bailian-2023-12-29-getparsesettings-522514560c54f49f.md)
- [GetAvailableParserTypes - 获取文件支持的解析器类型](../../raw/_short/api-bailian-2023-12-29-getavailableparsertypes-09561c4e0fb505d5.md)
- [AddTable](../../raw/_short/api-bailian-2023-12-29-addtable-6726351659db288d.md)
- [UpdateTableFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-updatetablefromauthorized-d7436828bcf51602.md)
- [AddConnector](../../raw/_short/api-bailian-2023-12-29-addconnector-7a3c9650409710fe.md)
- [GetConnector](../../raw/_short/api-bailian-2023-12-29-getconnector-cb2e485a0efd52f7.md)
- [UpdateConnector](../../raw/_short/api-bailian-2023-12-29-updateconnector-6a24905a7d201597.md)
- [知识库](../../raw/_short/api-bailian-2023-12-29-dir-knowledge-base-f6f202ad9694348f.md)
- [ChangeParseSetting](../../raw/_short/api-bailian-2023-12-29-changeparsesetting-59a7c69675f499ad.md)
- [CreateIndex - 创建知识库](../../raw/_short/api-bailian-2023-12-29-createindex-8bc613c75f8af371.md)
- [GetIndexJobStatus - 查询知识库创建或追加任务状态](../../raw/_short/api-bailian-2023-12-29-getindexjobstatus-1e88b6ccfffe0fe4.md)
- [SubmitIndexAddDocumentsJob - 提交知识库文件追加任务](../../raw/_short/api-bailian-2023-12-29-submitindexadddocumentsjo-ec4f5cf285e2c447.md)
- [Retrieve - 检索知识库](../../raw/_short/api-bailian-2023-12-29-retrieve-c8e6b8d718a30a84.md)
- [SubmitIndexJob - 提交知识库创建任务](../../raw/_short/api-bailian-2023-12-29-submitindexjob-63b38294171880d4.md)
- [ListIndexDocuments - 查询知识库文件列表](../../raw/_short/api-bailian-2023-12-29-listindexdocuments-9f0db0388c421903.md)
- [ListIndexFileDetails - 查询知识库文件详情](../../raw/_short/api-bailian-2023-12-29-listindexfiledetails-0e2036d0ef0d8fe8.md)
- [UpdateIndex - 更新知识库](../../raw/_short/api-bailian-2023-12-29-updateindex-551997e1d335e340.md)
- [DeleteIndexDocument - 删除知识库下的文件](../../raw/_short/api-bailian-2023-12-29-deleteindexdocument-0792a83f5a741348.md)
- [ListIndices - 查询知识库列表](../../raw/_short/api-bailian-2023-12-29-listindices-c555173be752eaaf.md)
- [DeleteIndex - 删除知识库](../../raw/_short/api-bailian-2023-12-29-deleteindex-500502bd6df1c49c.md)
- [ListChunks - 查询索引下的分片列表](../../raw/_short/api-bailian-2023-12-29-listchunks-30a6c87b93a583c6.md)
- [UpdateChunk - 修改切片](../../raw/_short/api-bailian-2023-12-29-updatechunk-589b46fcc24261f8.md)
- [AddChunk - 新增切片](../../raw/_short/api-bailian-2023-12-29-addchunk-1607bcddf6713fd9.md)
- [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)
- [DeleteChunk - 删除切片](../../raw/_short/api-bailian-2023-12-29-deletechunk-d249422088735d90.md)
- [GetIndexMonitor - 获取知识库监控数据](../../raw/_short/api-bailian-2023-12-29-getindexmonitor-3a609181d5c9c034.md)


