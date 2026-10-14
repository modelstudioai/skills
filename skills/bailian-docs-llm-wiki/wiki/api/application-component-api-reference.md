# application component api reference

本参考文档面向开发者，系统性地描述了百炼平台 Application Component（应用组件）的 OpenAPI 接口规范，涵盖数据连接（原应用数据）、知识库两大核心能力模块。所有接口均基于 `bailian/2023-12-29` 版本，采用标准 ROA 签名机制，支持通过官方 SDK 或自签名方式调用。

## 支持的模型/功能

Application Component API 主要提供两类核心能力：

- **数据连接（原应用数据）**：用于管理非结构化文件与结构化表格数据。支持类目（Category）的增删查、文件（File）的上传（含 OSS 导入）、元信息查询、标签管理及解析配置。例如，`AddCategory` 用于创建分类目录，`AddFilesFromAuthorizedOss` 支持从已授权的 OSS Bucket 批量导入文件 [AddFilesFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-addfilesfromauthorizedoss-879556d685a301b3.md)。
- **知识库（Knowledge Base）**：用于构建和管理 RAG 检索增强的知识库。支持知识库（Index）的全生命周期管理（创建、提交、更新、删除）、文档/切片（Chunk）的增删改查、检索（Retrieve）、状态监控等。例如，`CreateIndex` 初始化知识库，`SubmitIndexJob` 提交构建任务，`Retrieve` 执行语义检索 [Retrieve](../../raw/_short/api-bailian-2023-12-29-retrieve-c8e6b8d718a30a84.md)。

> **注意**：文档 25（知识库目录）中列出的 `ListIndices` 接口在文档 35 中其权限点被明确标识为 `sfm:ListIndex`，但文档 35 的标题与路径参数描述中均使用 `IndexId`，而文档 25 的链接指向 `api-bailian-2023-12-29-listindices.md`，其内容一致。此处无实质矛盾，但需注意 `ListIndex` 是权限点名称，`ListIndices` 是接口名称，二者在 RAM 策略中需对应使用。

## 关键参数

- **通用路径参数**：几乎所有接口均要求 `WorkspaceId`（业务空间 ID），用于隔离资源范围，必须通过控制台或相关 API 获取。
- **身份认证**：所有请求必须携带有效的 AccessKey（推荐使用最小权限的 RAM 用户凭证），并遵循 ROA 签名规范 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)。
- **核心业务参数**：
  - **类目操作**：`CategoryId`（由 `AddCategory` 返回）是 `ListCategory`、`DeleteCategory` 等操作的必需标识。
  - **文件操作**：`FileId`（由 `AddFile` 返回）是 `DescribeFile`、`DeleteFile`、`UpdateFileTag` 等操作的关键标识；`LeaseId`（由 `ApplyFileUploadLease` 返回）是 `AddFile` 上传流程的前置凭证。
  - **知识库操作**：`IndexId`（由 `CreateIndex` 返回）是 `SubmitIndexJob`、`Retrieve`、`DeleteIndex` 等绝大多数知识库接口的必需参数。
  - **分页与过滤**：`ListCategory`、`ListFile`、`ListIndices` 等列表接口普遍支持 `MaxResults`/`PageSize` 和 `NextToken` 进行分页；`ListIndexDocuments` 支持 `DocumentStatus` 和 `DocumentName` 进行状态与名称过滤。

## 使用方式

1. **环境准备**：确保已开通百炼服务，并在 RAM 中为调用者（RAM 用户或角色）授予 `AliyunBailianDataFullAccess`（读写）或 `AliyunBailianDataReadOnlyAccess`（只读）策略，或按需配置更细粒度的权限点（如 `sfm:ListCategory`, `sfm:Retrieve`）。
2. **接入点选择**：根据部署地域选择对应的公网或 VPC 接入地址，例如华北2（北京）的公网地址为 `bailian.cn-beijing.aliyuncs.com` [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)。
3. **调用流程**（以知识库为例）：
   - 调用 `CreateIndex` 创建知识库实例，获取 `IndexId`。
   - 调用 `AddFile` 将文件上传至应用数据。
   - 调用 `SubmitIndexJob` 提交构建任务，启动知识库索引过程。
   - 调用 `GetIndexJobStatus` 查询构建进度，直至状态为成功。
   - 调用 `Retrieve` 进行检索。
4. **调试工具**：强烈建议在 OpenAPI Explorer 中调试，可免去签名计算，自动生成各语言 SDK 示例代码。

## 限制和注意事项

- **限流策略**：各接口有独立的 QPS 限制，常见值为 5~15 次/秒（如 `AddCategory` 为 5 次/秒，`ListIndexDocuments` 为 15 次/秒）。超出将返回限流错误，需实现重试逻辑。
- **幂等性**：并非所有接口都具备幂等性。`AddCategory`、`AddFile`、`CreateIndex` 等创建类接口不具备幂等性，重复调用可能产生重复资源；而 `DeleteCategory`、`ListCategory`、`Retrieve` 等则具备幂等性。
- **功能边界**：
  - **数据表操作**：`AddTable` 可创建表格，但 `DeleteTable` 等操作未在本文档中提供，且明确说明“不支持通过 API 删除数据表”。
  - **知识库类型**：`UpdateChunk`、`DeleteChunk` 仅支持文档搜索类（`unstructured`）知识库，不支持数据查询或图片问答类。
  - **国际站支持**：`UpdateIndex` 和 `GetIndexMonitor` 接口明确声明“不支持国际站”。
- **安全最佳实践**：严禁使用主账号 AccessKey。务必遵循最小权限原则，为 RAM 用户配置精确的 `Action`（如 `sfm:Retrieve`）和 `Resource`（若支持资源级授权）。

## 来源文档

- [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)
- [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)
- [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)
- [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md)
- [数据连接（原应用数据）](../../raw/_short/api-bailian-2023-12-29-dir-data-connection-origi-a1f7f2601bd6f7cf.md)
- [AddCategory](../../raw/_short/api-bailian-2023-12-29-addcategory-e2fe0e0435ed504e.md)
- [DeleteCategory - 删除类目](../../raw/_short/api-bailian-2023-12-29-deletecategory-9838436bd2db3113.md)
- [ListCategory](../../raw/_short/api-bailian-2023-12-29-listcategory-2521532ef3e828b3.md)
- [ApplyFileUploadLease](../../raw/_short/api-bailian-2023-12-29-applyfileuploadlease-39e8ca15e0e9561a.md)
- [AddFile](../../raw/_short/api-bailian-2023-12-29-addfile-8c254b3500bc50bc.md)
- [AddFilesFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-addfilesfromauthorizedoss-879556d685a301b3.md)
- [ListFile](../../raw/_short/api-bailian-2023-12-29-listfile-360209e3a2479f14.md)
- [DescribeFile](../../raw/_short/api-bailian-2023-12-29-describefile-020886c28a208bf2.md)
- [UpdateFileTag](../../raw/_short/api-bailian-2023-12-29-updatefiletag-f84d2af6a45d6553.md)
- [BatchUpdateFileTag](../../raw/_short/api-bailian-2023-12-29-batchupdatefiletag-34a8f009de66cb8b.md)
- [DeleteFile](../../raw/_short/api-bailian-2023-12-29-deletefile-7e0409a458195fe2.md)
- [DeleteFiles](../../raw/_short/api-bailian-2023-12-29-deletefiles-96ef0815114e4e37.md)
- [GetAvailableParserTypes - 获取文件支持的解析器类型](../../raw/_short/api-bailian-2023-12-29-getavailableparsertypes-09561c4e0fb505d5.md)
- [ChangeParseSetting](../../raw/_short/api-bailian-2023-12-29-changeparsesetting-59a7c69675f499ad.md)
- [GetParseSettings - 获取类目解析设置](../../raw/_short/api-bailian-2023-12-29-getparsesettings-522514560c54f49f.md)
- [AddTable](../../raw/_short/api-bailian-2023-12-29-addtable-6726351659db288d.md)
- [UpdateTableFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-updatetablefromauthorized-d7436828bcf51602.md)
- [GetConnector](../../raw/_short/api-bailian-2023-12-29-getconnector-cb2e485a0efd52f7.md)
- [UpdateConnector](../../raw/_short/api-bailian-2023-12-29-updateconnector-6a24905a7d201597.md)
- [知识库](../../raw/_short/api-bailian-2023-12-29-dir-knowledge-base-f6f202ad9694348f.md)
- [CreateIndex](../../raw/_short/api-bailian-2023-12-29-createindex-8bc613c75f8af371.md)
- [SubmitIndexJob - 提交知识库创建任务](../../raw/_short/api-bailian-2023-12-29-submitindexjob-63b38294171880d4.md)
- [GetIndexJobStatus](../../raw/_short/api-bailian-2023-12-29-getindexjobstatus-1e88b6ccfffe0fe4.md)
- [Retrieve](../../raw/_short/api-bailian-2023-12-29-retrieve-c8e6b8d718a30a84.md)
- [SubmitIndexAddDocumentsJob](../../raw/_short/api-bailian-2023-12-29-submitindexadddocumentsjo-ec4f5cf285e2c447.md)
- [ListIndexDocuments](../../raw/_short/api-bailian-2023-12-29-listindexdocuments-9f0db0388c421903.md)
- [ListIndexFileDetails](../../raw/_short/api-bailian-2023-12-29-listindexfiledetails-0e2036d0ef0d8fe8.md)
- [UpdateIndex - 更新知识库](../../raw/_short/api-bailian-2023-12-29-updateindex-551997e1d335e340.md)
- [DeleteIndexDocument - 删除知识库下的文件](../../raw/_short/api-bailian-2023-12-29-deleteindexdocument-0792a83f5a741348.md)
- [ListIndices](../../raw/_short/api-bailian-2023-12-29-listindices-c555173be752eaaf.md)
- [ListChunks - 查询索引下的分片列表](../../raw/_short/api-bailian-2023-12-29-listchunks-30a6c87b93a583c6.md)
- [DeleteIndex - 删除知识库](../../raw/_short/api-bailian-2023-12-29-deleteindex-500502bd6df1c49c.md)
- [UpdateChunk - 修改切片](../../raw/_short/api-bailian-2023-12-29-updatechunk-589b46fcc24261f8.md)
- [AddConnector](../../raw/_short/api-bailian-2023-12-29-addconnector-7a3c9650409710fe.md)
- [AddChunk](../../raw/_short/api-bailian-2023-12-29-addchunk-1607bcddf6713fd9.md)
- [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)
- [GetIndexMonitor - 获取知识库监控数据](../../raw/_short/api-bailian-2023-12-29-getindexmonitor-3a609181d5c9c034.md)
- [DeleteChunk - 删除切片](../../raw/_short/api-bailian-2023-12-29-deletechunk-d249422088735d90.md)


