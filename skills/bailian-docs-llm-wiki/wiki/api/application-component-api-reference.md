# application component api reference

本 API 参考文档面向开发者，提供百炼平台应用组件（Application Component）的核心 OpenAPI 接口规范，涵盖数据连接（原应用数据）、知识库、Prompt 模板三大功能模块。所有接口均基于 `bailian/2023-12-29` 版本，采用 ROA 签名机制，支持通过官方 SDK 快速集成。开发者需预先配置 RAM 权限与业务空间访问权限方可调用。

## 支持的模型/功能

当前 API 覆盖以下核心能力模块：

- **数据连接（原应用数据）**：提供类目管理（`AddCategory`、`ListCategory`、`DeleteCategory`）、文件全生命周期操作（`ApplyFileUploadLease`、`AddFile`、`ListFile`、`DescribeFile`、`DeleteFile`、`DeleteFiles`）、OSS 批量导入（`AddFilesFromAuthorizedOss`）、连接器管理（`AddConnector`、`GetConnector`、`UpdateConnector`）及解析设置查询（`GetParseSettings`、`GetAvailableParserTypes`）。注意：**不支持通过 API 新增或删除数据表**，该操作仅限控制台完成 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)。
- **知识库（RAG）**：支持知识库创建与管理（`CreateIndex`、`SubmitIndexJob`、`UpdateIndex`、`ListIndices`、`DeleteIndex`）、文件追加与状态监控（`SubmitIndexAddDocumentsJob`、`GetIndexJobStatus`、`ListIndexDocuments`、`ListIndexFileDetails`、`GetIndexMonitor`）、内容检索（`Retrieve`）及细粒度切片操作（`ListChunks`、`AddChunk`、`UpdateChunk`、`DeleteChunk`、`DeleteIndexDocument`）。其中，`DeleteIndexDocument` 仅适用于文档搜索类知识库，**不支持数据查询/图片问答类知识库** [DeleteIndexDocument - 删除知识库下的文件](../../raw/_short/api-bailian-2023-12-29-deleteindexdocument-0792a83f5a741348.md)。
- **Prompt 模板**：提供模板的增删改查（`CreatePromptTemplate`、`GetPromptTemplate`、`UpdatePromptTemplate`、`DeletePromptTemplate`、`ListPromptTemplates`），但**暂不支持文生图 Prompt 模板的创建** [CreatePromptTemplate - 创建Prompt模板](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-1194e536beb0529a.md)。

> **注意**：文档 31 (`UpdateIndex`) 中引用的权限文档路径 `raw/model-user-guide/security-and-compliance/permission-management-overview.md` 与其他多处文档（如文档 3、25、27）一致引用 `https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user`，而该路径在原始文档中为有效 URL，此处路径为相对路径且不存在对应文件，属于文档生成错误，应以 URL 链接为准。

## 关键参数

- **通用路径参数**：几乎所有接口均需 `WorkspaceId`（业务空间 ID），需通过控制台获取，无枚举 API。
- **类目与文件标识**：`CategoryId`（来自 `AddCategory` 返回）、`FileId`（来自 `AddFile` 返回）、`IndexId`（来自 `CreateIndex` 返回）、`ChunkId`（来自 `ListChunks` 返回的 `Node.Metadata._id`）是关键资源标识符。
- **分页与过滤**：`List*` 类接口普遍支持 `MaxResults`/`PageSize`、`NextToken`/`PageNumber` 分页；支持按 `FileName`、`DocumentName`、`DocumentStatus`、`IndexName` 等字段过滤。
- **解析器控制**：`AddFile` 接口的 `Parser` 参数决定文件解析方式（如 `AUTO_SELECT`, `DOCMIND`），其可选值需通过 `GetAvailableParserTypes` 查询确认。
- **权限点（Action）**：每个 API 对应唯一 RAM Action，如 `sfm:AddCategory`、`sfm:Retrieve`、`sfm:CreatePromptTemplate`，授权时需在 RAM 策略中显式声明。

## 使用方式

1. **环境准备**：
   - 获取阿里云 AccessKey（推荐使用最小权限的 RAM 用户，而非主账号）[API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)。
   - 为 RAM 用户附加 `AliyunBailianDataFullAccess`（读写）或 `AliyunBailianDataReadOnlyAccess`（只读）策略，并将其加入目标业务空间。
2. **接入点选择**：根据部署地域选用对应公网或 VPC 接入地址，例如北京地域为 `bailian.cn-beijing.aliyuncs.com` [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)。
3. **调用流程（以知识库为例）**：
   - 先调用 `CreateIndex` 初始化知识库；
   - 再调用 `SubmitIndexJob` 提交创建任务；
   - 通过 `GetIndexJobStatus` 轮询任务状态直至完成；
   - 文件上传：`ApplyFileUploadLease` → 上传至租约地址 → `AddFile` 导入；
   - 追加文件：`SubmitIndexAddDocumentsJob` → `GetIndexJobStatus` 查询结果；
   - 检索：直接调用 `Retrieve`。
4. **调试工具**：所有接口均支持在 [OpenAPI Explorer](https://api.aliyun.com/) 中在线调试，自动生成各语言 SDK 示例代码。

## 限制和注意事项

- **限流策略**：各接口有独立 QPS 限制（如 `AddCategory`/`DeleteCategory` 为 5 次/秒，`ApplyFileUploadLease`/`AddFile` 为 10 次/秒），超限将返回 `429 Too Many Requests`，需实现退避重试。
- **幂等性**：`DeleteCategory`、`List*`、`Describe*`、`Get*`、`Update*`、`Delete*`（除 `DeleteFile` 外）等多数查询与更新类接口具备幂等性；`Add*`、`Create*`、`Submit*` 等创建类接口不具备幂等性，重复调用可能产生重复资源。
- **文件状态约束**：`DeleteFile` 仅允许删除 `PARSE_FAILED` 或 `PARSE_SUCCESS` 状态的文件；`DeleteIndexDocument` 仅允许删除 `INSERT_ERROR` 或 `FINISH` 状态的文件。
- **安全要求**：必须遵循最小权限原则（PoLP），禁止主账号密钥直连生产环境；OSS 导入需确保 Bucket 与百炼同账号，并正确配置 Referer 白名单（`*.console.aliyun.com`）。
- **SDK 依赖**：强烈建议使用官方最新版 [阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)，避免手动签名的复杂性与潜在错误。

## 来源文档

- [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)
- [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)
- [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)
- [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md)
- [数据连接（原应用数据）](../../raw/_short/api-bailian-2023-12-29-dir-data-connection-origi-a1f7f2601bd6f7cf.md)
- [AddCategory](../../raw/_short/api-bailian-2023-12-29-addcategory-e2fe0e0435ed504e.md)
- [DeleteCategory - 删除类目](../../raw/_short/api-bailian-2023-12-29-deletecategory-9838436bd2db3113.md)
- [ApplyFileUploadLease](../../raw/_short/api-bailian-2023-12-29-applyfileuploadlease-39e8ca15e0e9561a.md)
- [AddFile](../../raw/_short/api-bailian-2023-12-29-addfile-8c254b3500bc50bc.md)
- [AddFilesFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-addfilesfromauthorizedoss-879556d685a301b3.md)
- [ListFile](../../raw/_short/api-bailian-2023-12-29-listfile-360209e3a2479f14.md)
- [DescribeFile](../../raw/_short/api-bailian-2023-12-29-describefile-020886c28a208bf2.md)
- [BatchUpdateFileTag](../../raw/_short/api-bailian-2023-12-29-batchupdatefiletag-34a8f009de66cb8b.md)
- [DeleteFile](../../raw/_short/api-bailian-2023-12-29-deletefile-7e0409a458195fe2.md)
- [ListCategory](../../raw/_short/api-bailian-2023-12-29-listcategory-2521532ef3e828b3.md)
- [GetParseSettings - 获取类目解析设置](../../raw/_short/api-bailian-2023-12-29-getparsesettings-522514560c54f49f.md)
- [GetAvailableParserTypes - 获取文件支持的解析器类型](../../raw/_short/api-bailian-2023-12-29-getavailableparsertypes-09561c4e0fb505d5.md)
- [DeleteFiles](../../raw/_short/api-bailian-2023-12-29-deletefiles-96ef0815114e4e37.md)
- [AddTable](../../raw/_short/api-bailian-2023-12-29-addtable-6726351659db288d.md)
- [UpdateTableFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-updatetablefromauthorized-d7436828bcf51602.md)
- [AddConnector](../../raw/_short/api-bailian-2023-12-29-addconnector-7a3c9650409710fe.md)
- [GetConnector](../../raw/_short/api-bailian-2023-12-29-getconnector-cb2e485a0efd52f7.md)
- [UpdateConnector](../../raw/_short/api-bailian-2023-12-29-updateconnector-6a24905a7d201597.md)
- [知识库](../../raw/_short/api-bailian-2023-12-29-dir-knowledge-base-f6f202ad9694348f.md)
- [CreateIndex - 创建知识库](../../raw/_short/api-bailian-2023-12-29-createindex-8bc613c75f8af371.md)
- [SubmitIndexJob - 提交知识库创建任务](../../raw/_short/api-bailian-2023-12-29-submitindexjob-63b38294171880d4.md)
- [SubmitIndexAddDocumentsJob - 提交知识库文件追加任务](../../raw/_short/api-bailian-2023-12-29-submitindexadddocumentsjo-ec4f5cf285e2c447.md)
- [Retrieve - 检索知识库](../../raw/_short/api-bailian-2023-12-29-retrieve-c8e6b8d718a30a84.md)
- [ListIndexDocuments - 查询知识库文件列表](../../raw/_short/api-bailian-2023-12-29-listindexdocuments-9f0db0388c421903.md)
- [ListIndexFileDetails - 查询知识库文件详情](../../raw/_short/api-bailian-2023-12-29-listindexfiledetails-0e2036d0ef0d8fe8.md)
- [UpdateIndex - 更新知识库](../../raw/_short/api-bailian-2023-12-29-updateindex-551997e1d335e340.md)
- [DeleteIndexDocument - 删除知识库下的文件](../../raw/_short/api-bailian-2023-12-29-deleteindexdocument-0792a83f5a741348.md)
- [ListIndices - 查询知识库列表](../../raw/_short/api-bailian-2023-12-29-listindices-c555173be752eaaf.md)
- [DeleteIndex - 删除知识库](../../raw/_short/api-bailian-2023-12-29-deleteindex-500502bd6df1c49c.md)
- [ListChunks - 查询索引下的分片列表](../../raw/_short/api-bailian-2023-12-29-listchunks-30a6c87b93a583c6.md)
- [AddChunk - 新增切片](../../raw/_short/api-bailian-2023-12-29-addchunk-1607bcddf6713fd9.md)
- [UpdateChunk - 修改切片](../../raw/_short/api-bailian-2023-12-29-updatechunk-589b46fcc24261f8.md)
- [GetIndexJobStatus - 查询知识库创建或追加任务状态](../../raw/_short/api-bailian-2023-12-29-getindexjobstatus-1e88b6ccfffe0fe4.md)
- [DeleteChunk - 删除切片](../../raw/_short/api-bailian-2023-12-29-deletechunk-d249422088735d90.md)
- [GetIndexMonitor - 获取知识库监控数据](../../raw/_short/api-bailian-2023-12-29-getindexmonitor-3a609181d5c9c034.md)
- [Prompt 模板](../../raw/_short/api-bailian-2023-12-29-dir-prompt-engineering-11ee962a5f5d5d1e.md)
- [CreatePromptTemplate - 创建Prompt模板](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-1194e536beb0529a.md)
- [GetPromptTemplate - 获取Prompt模板](../../raw/_short/api-bailian-2023-12-29-getprompttemplate-584c357dd7cb48d6.md)
- [UpdatePromptTemplate - 更新Prompt模板](../../raw/_short/api-bailian-2023-12-29-updateprompttemplate-519fb4af5ea50522.md)
- [DeletePromptTemplate - 删除Prompt模板](../../raw/_short/api-bailian-2023-12-29-deleteprompttemplate-b441fa1b9c777b81.md)
- [其他](../../raw/_short/api-bailian-2023-12-29-dir-others-b9c3a16db11771f5.md)
- [ListPromptTemplates - 获取Prompt模板列表](../../raw/_short/api-bailian-2023-12-29-listprompttemplates-ab5ba5362e93cfcd.md)
- [GetAlipayTransferStatus - 查询支付宝打赏状态](../../raw/_short/api-bailian-2023-12-29-getalipaytransferstatus-04aa88852762fd85.md)
- [GetAlipayUrl - 获取支付宝打赏URL](../../raw/_short/api-bailian-2023-12-29-getalipayurl-e6e9715d5164f74a.md)
- [ApplyTempStorageLease - 申请临时文件上传许可](../../raw/_short/api-bailian-2023-12-29-applytempstoragelease-5a38ce0eefc66408.md)
- [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)
- [UpdateFileTag](../../raw/_short/api-bailian-2023-12-29-updatefiletag-f84d2af6a45d6553.md)
- [ChangeParseSetting](../../raw/_short/api-bailian-2023-12-29-changeparsesetting-59a7c69675f499ad.md)


