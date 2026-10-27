# application component api reference

本 API 参考文档面向开发者，系统性地描述了百炼平台 Application Component（应用组件）提供的核心 OpenAPI 接口能力，覆盖数据连接（原应用数据）、知识库两大核心功能模块。所有接口均基于 `bailian/2023-12-29` 版本，采用标准 ROA 签名机制，支持通过官方 SDK 或自签名方式调用。开发者需预先配置 RAM 权限与业务空间上下文方可使用。

## 支持的模型/功能

Application Component API 主要提供两类核心能力：

1.  **数据连接（原应用数据）**：用于管理非结构化文件和结构化表格数据。支持类目（Category）的增删查、文件（File）的上传（需先申请租约）、导入、查询、标签更新及删除；支持从已授权 OSS Bucket 批量导入文件或更新表格；支持连接器（Connector）的创建与管理；并提供解析器（Parser）配置能力，如为 `.pdf` 文件指定 `DOCMIND_DIGITAL` 解析器 [GetAvailableParserTypes - 获取文件支持的解析器类型](../../raw/_short/api-bailian-2023-12-29-getavailableparsertypes-09561c4e0fb505d5.md)。
2.  **知识库（Knowledge Base）**：用于构建和管理 RAG 知识库。支持知识库（Index）的创建（`CreateIndex`）、提交构建任务（`SubmitIndexJob`）、追加文档（`SubmitIndexAddDocumentsJob`）、检索（`Retrieve`）、查询列表（`ListIndices`）与删除（`DeleteIndex`）；支持对知识库内文件（`ListIndexDocuments`, `ListIndexFileDetails`）及文本切片（`ListChunks`, `AddChunk`, `UpdateChunk`, `DeleteChunk`）的精细化操作；并提供监控数据（`GetIndexMonitor`）与配置更新（`UpdateIndex`）能力。

> **注意**：`AddTable` 和 `UpdateTableFromAuthorizedOss` 接口明确仅适用于“表格连接器”，而 `AddCategory` 等类目接口的 `CategoryType` 参数在文档中仅列出 `UNSTRUCTURED`，且多处强调“暂不支持通过 API 查询数据表” [ListCategory](../../raw/_short/api-bailian-2023-12-29-listcategory-2521532ef3e828b3.md)，表明结构化数据管理与非结构化数据管理是分离的两条路径，不可混用。

## 关键参数

所有 API 均要求在请求路径中传入 `WorkspaceId`（业务空间 ID），这是资源隔离与权限控制的基础。其他关键参数按功能域划分：

*   **数据连接通用参数**：
    *   `CategoryId`: 类目 ID，由 `AddCategory` 返回，用于文件归属与解析设置。
    *   `FileId`: 文件 ID，由 `AddFile` 返回，用于文件详情查询（`DescribeFile`）、标签更新（`UpdateFileTag`）及删除（`DeleteFile`）。
    *   `LeaseId`: 上传租约 ID，由 `ApplyFileUploadLease` 返回，是调用 `AddFile` 的前置必要参数。
    *   `ConnectorId`: 连接器 ID，用于关联类目与底层存储（如 OSS）。
*   **知识库通用参数**：
    *   `IndexId`: 知识库 ID，由 `CreateIndex` 返回，是几乎所有知识库操作（`SubmitIndexJob`, `Retrieve`, `ListIndexDocuments`, `DeleteIndexDocument` 等）的必需参数。
    *   `JobId`: 任务 ID，由 `SubmitIndexJob` 或 `SubmitIndexAddDocumentsJob` 返回，用于轮询任务状态（`GetIndexJobStatus`）。
    *   `ChunkId`: 文本切片 ID，由 `ListChunks` 返回，用于切片的修改（`UpdateChunk`）与删除（`DeleteChunk`）。
*   **分页与过滤参数**：
    *   `MaxResults` / `PageSize` / `PageNumber`: 用于 `ListCategory`, `ListFile`, `ListIndices`, `ListChunks` 等列表接口的分页。
    *   `NextToken`: 用于 `ListCategory`, `ListFile` 等接口的游标分页。
    *   `DocumentName` / `EnableNameLike`: 用于 `ListIndexDocuments`, `ListIndexFileDetails` 的文件名精确或模糊过滤。

## 使用方式

1.  **环境准备**：首先，您需要一个阿里云账号，并遵循最小权限原则，创建具备 `AliyunBailianDataFullAccess`（读写）或 `AliyunBailianDataReadOnlyAccess`（只读）策略的 RAM 用户，获取其 AccessKey。详细步骤请参见 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md) 中的“账号与安全准备”章节。
2.  **接入点选择**：根据您的地域需求，选择对应的公网或 VPC 接入地址，例如华北2（北京）的公网地址为 `bailian.cn-beijing.aliyuncs.com` [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)。
3.  **SDK 调用（推荐）**：下载并集成对应语言的最新版百炼 SDK（版本 `2023-12-29`），SDK 会自动处理签名、重试等细节。所有接口文档均提供了 OpenAPI Explorer 的在线调试链接，可一键生成各语言 SDK 示例代码。
4.  **自签名调用（高级）**：若需自定义签名，必须严格遵循 ROA 签名规范。由于其复杂性，官方强烈建议加入钉钉群（147535001692）寻求技术支持，以避免因签名错误导致的接入失败。

## 限制和注意事项

*   **限流策略**：所有接口均有严格的 QPS 限制，开发者必须在代码中实现合理的重试与降级逻辑。常见限制包括：`DeleteCategory`（5次/秒）、`ApplyFileUploadLease`（10次/秒）、`ListFile`（5次/秒）、`Retrieve`（无明确说明，但需考虑响应延迟）[DeleteCategory - 删除类目](../../raw/_short/api-bailian-2023-12-29-deletecategory-9838436bd2db3113.md)。
*   **幂等性**：并非所有接口都具备幂等性。`CreateIndex`, `SubmitIndexJob`, `ApplyFileUploadLease`, `AddFile` 等接口不具备幂等性，重复调用可能导致资源重复创建或错误；而 `List*`, `Describe*`, `Delete*`, `Update*` 等多数查询与变更操作则具备幂等性。开发者应仔细阅读各接口文档中的“接口说明”部分。
*   **数据一致性**：`DeleteFile` 仅删除应用数据中的文件，**不会**影响已构建好的知识库；反之，`DeleteIndexDocument` 仅删除知识库中的索引，**不会**删除应用数据中的原始文件。两者是完全独立的操作，需根据业务目标谨慎选择。
*   **功能边界**：API 不支持直接删除数据表（`DeleteTable`），此操作必须通过控制台完成；`AddCategory` 等接口不支持新增数据表；`DeleteIndex` 接口要求知识库必须先与应用解除关联，此解绑操作也仅能在控制台完成。

## 来源文档

- [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)
- [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)
- [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md)
- [数据连接（原应用数据）](../../raw/_short/api-bailian-2023-12-29-dir-data-connection-origi-a1f7f2601bd6f7cf.md)
- [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)
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
- [AddCategory](../../raw/_short/api-bailian-2023-12-29-addcategory-e2fe0e0435ed504e.md)
- [ChangeParseSetting](../../raw/_short/api-bailian-2023-12-29-changeparsesetting-59a7c69675f499ad.md)
- [AddTable](../../raw/_short/api-bailian-2023-12-29-addtable-6726351659db288d.md)
- [UpdateTableFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-updatetablefromauthorized-d7436828bcf51602.md)
- [AddConnector](../../raw/_short/api-bailian-2023-12-29-addconnector-7a3c9650409710fe.md)
- [GetConnector](../../raw/_short/api-bailian-2023-12-29-getconnector-cb2e485a0efd52f7.md)
- [UpdateConnector](../../raw/_short/api-bailian-2023-12-29-updateconnector-6a24905a7d201597.md)
- [知识库](../../raw/_short/api-bailian-2023-12-29-dir-knowledge-base-f6f202ad9694348f.md)
- [ListCategory](../../raw/_short/api-bailian-2023-12-29-listcategory-2521532ef3e828b3.md)
- [GetAvailableParserTypes - 获取文件支持的解析器类型](../../raw/_short/api-bailian-2023-12-29-getavailableparsertypes-09561c4e0fb505d5.md)
- [CreateIndex](../../raw/_short/api-bailian-2023-12-29-createindex-8bc613c75f8af371.md)
- [GetIndexJobStatus](../../raw/_short/api-bailian-2023-12-29-getindexjobstatus-1e88b6ccfffe0fe4.md)
- [SubmitIndexAddDocumentsJob](../../raw/_short/api-bailian-2023-12-29-submitindexadddocumentsjo-ec4f5cf285e2c447.md)
- [Retrieve](../../raw/_short/api-bailian-2023-12-29-retrieve-c8e6b8d718a30a84.md)
- [SubmitIndexJob - 提交知识库创建任务](../../raw/_short/api-bailian-2023-12-29-submitindexjob-63b38294171880d4.md)
- [ListIndexDocuments](../../raw/_short/api-bailian-2023-12-29-listindexdocuments-9f0db0388c421903.md)
- [ListIndexFileDetails](../../raw/_short/api-bailian-2023-12-29-listindexfiledetails-0e2036d0ef0d8fe8.md)
- [UpdateIndex - 更新知识库](../../raw/_short/api-bailian-2023-12-29-updateindex-551997e1d335e340.md)
- [DeleteIndexDocument - 删除知识库下的文件](../../raw/_short/api-bailian-2023-12-29-deleteindexdocument-0792a83f5a741348.md)
- [ListIndices](../../raw/_short/api-bailian-2023-12-29-listindices-c555173be752eaaf.md)
- [DeleteIndex - 删除知识库](../../raw/_short/api-bailian-2023-12-29-deleteindex-500502bd6df1c49c.md)
- [AddChunk](../../raw/_short/api-bailian-2023-12-29-addchunk-1607bcddf6713fd9.md)
- [ListChunks - 查询索引下的分片列表](../../raw/_short/api-bailian-2023-12-29-listchunks-30a6c87b93a583c6.md)
- [UpdateChunk - 修改切片](../../raw/_short/api-bailian-2023-12-29-updatechunk-589b46fcc24261f8.md)
- [DeleteChunk - 删除切片](../../raw/_short/api-bailian-2023-12-29-deletechunk-d249422088735d90.md)
- [GetIndexMonitor - 获取知识库监控数据](../../raw/_short/api-bailian-2023-12-29-getindexmonitor-3a609181d5c9c034.md)
- [Prompt 模板](../../raw/_short/api-bailian-2023-12-29-dir-prompt-engineering-11ee962a5f5d5d1e.md)
- [GetPromptTemplate - 获取Prompt模板](../../raw/_short/api-bailian-2023-12-29-getprompttemplate-584c357dd7cb48d6.md)
- [CreatePromptTemplate - 创建Prompt模板](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-1194e536beb0529a.md)
- [UpdatePromptTemplate - 更新Prompt模板](../../raw/_short/api-bailian-2023-12-29-updateprompttemplate-519fb4af5ea50522.md)
- [ListPromptTemplates - 获取Prompt模板列表](../../raw/_short/api-bailian-2023-12-29-listprompttemplates-ab5ba5362e93cfcd.md)
- [DeletePromptTemplate - 删除Prompt模板](../../raw/_short/api-bailian-2023-12-29-deleteprompttemplate-b441fa1b9c777b81.md)
- [其他](../../raw/_short/api-bailian-2023-12-29-dir-others-b9c3a16db11771f5.md)
- [GetAlipayUrl - 获取支付宝打赏URL](../../raw/_short/api-bailian-2023-12-29-getalipayurl-e6e9715d5164f74a.md)
- [GetAlipayTransferStatus - 查询支付宝打赏状态](../../raw/_short/api-bailian-2023-12-29-getalipaytransferstatus-04aa88852762fd85.md)
- [ApplyTempStorageLease - 申请临时文件上传许可](../../raw/_short/api-bailian-2023-12-29-applytempstoragelease-5a38ce0eefc66408.md)
- [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)


