# application component api reference

本 API 参考文档面向开发者，汇总了百炼平台 Application Component（应用组件）层的核心 OpenAPI 接口规范，涵盖数据连接（原应用数据）与知识库两大功能模块。所有接口均基于 `bailian/2023-12-29` 版本，采用 ROA 风格，需通过阿里云 AccessKey 或 RAM 子账号凭证鉴权调用。建议优先使用官方 SDK 降低集成复杂度。

## 支持的模型/功能

Application Component API 主要提供两类核心能力：

- **数据连接（原应用数据）**：用于管理结构化与非结构化数据源，包括类目（Category）、文件（File）、表格（Table）、连接器（Connector）的全生命周期操作。支持本地上传、OSS 授权导入、解析配置等。例如，`AddCategory` 创建分类目录，`AddFilesFromAuthorizedOss` 从已授权 OSS Bucket 批量导入文件，`GetAvailableParserTypes` 查询文件类型对应的支持解析器 [原文标题](../../raw/_short/api-bailian-2023-12-29-getavailableparsertypes-09561c4e0fb505d5.md)。
- **知识库（Knowledge Base）**：提供 RAG 场景下知识库的创建、更新、检索与运维能力，覆盖文档搜索、数据查询、图片问答、音视频搜索四类知识库。关键操作包括 `CreateIndex` 初始化知识库、`SubmitIndexJob` 提交构建任务、`Retrieve` 实时语义检索，以及细粒度的 `ListChunks` / `AddChunk` / `DeleteChunk` 切片管理。注意：`Retrieve` 接口的请求参数在 2024-07-23 版本发生变更，详见 [原文标题](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md) 的版本说明。

> **注意**：`AddTable` 和 `UpdateTableFromAuthorizedOss` 文档（文档 20、21）明确支持表格数据连接器，但 `API目录`（文档 3）及 `数据连接（原应用数据）`（文档 4）的主目录中均未列出这两个 API，存在目录结构与实际能力不一致的问题。开发者应以具体接口文档为准。

## 关键参数

所有接口均需在路径中指定 `WorkspaceId`（业务空间 ID），该 ID 是资源隔离与权限控制的基础维度，必须通过百炼控制台获取。常见关键参数如下：

- **身份认证**：统一使用阿里云标准 AccessKey（`AccessKeyId` + `AccessKeySecret`）或 RAM 子账号凭证，通过签名机制鉴权。RAM 权限策略需显式授予对应 `sfm:*` 操作权限，例如 `sfm:AddCategory`、`sfm:Retrieve` 等 [原文标题](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)。
- **分页与游标**：`ListCategory`、`ListFile`、`ListIndices` 等列表接口采用 `NextToken` 游标模式（而非传统 `PageNumber/PageSIze`），首次请求仅需 `MaxResults`，后续请求将上一次返回的 `NextToken` 作为参数传入。
- **ID 引用**：各资源间通过 ID 关联，如 `AddFile` 返回 `FileId`，该 ID 可用于 `DescribeFile`、`DeleteFile` 或 `SubmitIndexAddDocumentsJob`；`CreateIndex` 返回 `IndexId`，是 `Retrieve`、`DeleteIndexDocument` 等操作的必需参数。
- **幂等性控制**：多数查询类接口（如 `ListCategory`, `DescribeFile`, `GetIndexJobStatus`）具有幂等性；而创建类（`AddCategory`, `CreateIndex`）和部分更新类（`ChangeParseSetting`, `SubmitIndexJob`）接口不具备幂等性，重复调用可能产生副作用，需业务侧自行保障。

## 使用方式

1. **环境准备**：确保已开通百炼服务，并在 RAM 中为调用者（主账号或子账号）授予 `AliyunBailianDataFullAccess`（读写）或 `AliyunBailianDataReadOnlyAccess`（只读）策略。详细授权模型见 [原文标题](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)。
2. **接入点选择**：根据部署地域选择对应公网或 VPC 接入地址，例如华北2（北京）地域的公网地址为 `bailian.cn-beijing.aliyuncs.com` [原文标题](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)。
3. **SDK 集成（推荐）**：直接下载并使用官方提供的多语言 SDK（Java/Python/Go 等），自动处理签名、重试、限流等细节。SDK 下载地址见 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)。
4. **调试与测试**：所有接口均支持在 [OpenAPI Explorer](https://api.aliyun.com) 中在线调试，可自动生成代码示例，快速验证请求格式与响应。

## 限制和注意事项

- **限流策略**：绝大多数接口有严格的 QPS 限制，常见值为 5~15 次/秒（如 `AddCategory`、`ListFile` 为 5 次/秒，`Retrieve`、`ListIndices` 为 10~15 次/秒）。超出后将返回限流错误，需实现客户端退避重试逻辑。
- **资源约束**：单个业务空间最多创建 500 个类目（`AddCategory`）；`BatchUpdateFileTag` 单次最多更新 100 个标签，总长度不超过 700 字符；`DeleteFiles` 单次最多删除 20 个文件。
- **功能边界**：
  - 数据表（Table）的增删改查**不支持纯 API 方式**，文档 5、6、15 明确指出“不支持通过 API 新增/查询/删除数据表”，相关操作需通过控制台完成。
  - `DeleteIndexDocument` 仅支持非结构化知识库（document/multimedia），不支持数据查询（table）和图片问答（image）类知识库；同理，`UpdateChunk` 也**仅支持文档搜索类知识库**（文档 41）。
- **安全最佳实践**：严禁在客户端或前端代码中硬编码主账号 AccessKey。务必遵循最小权限原则，为不同业务场景创建专用 RAM 用户并授予精确的 `sfm:*` 权限点。

## 来源文档

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
- [ChangeParseSetting](../../raw/_short/api-bailian-2023-12-29-changeparsesetting-59a7c69675f499ad.md)
- [AddTable](../../raw/_short/api-bailian-2023-12-29-addtable-6726351659db288d.md)
- [UpdateTableFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-updatetablefromauthorized-d7436828bcf51602.md)
- [AddConnector](../../raw/_short/api-bailian-2023-12-29-addconnector-7a3c9650409710fe.md)
- [UpdateConnector](../../raw/_short/api-bailian-2023-12-29-updateconnector-6a24905a7d201597.md)
- [GetConnector](../../raw/_short/api-bailian-2023-12-29-getconnector-cb2e485a0efd52f7.md)
- [知识库](../../raw/_short/api-bailian-2023-12-29-dir-knowledge-base-f6f202ad9694348f.md)
- [CreateIndex - 创建知识库](../../raw/_short/api-bailian-2023-12-29-createindex-8bc613c75f8af371.md)
- [GetIndexJobStatus - 查询知识库创建或追加任务状态](../../raw/_short/api-bailian-2023-12-29-getindexjobstatus-1e88b6ccfffe0fe4.md)
- [SubmitIndexJob - 提交知识库创建任务](../../raw/_short/api-bailian-2023-12-29-submitindexjob-63b38294171880d4.md)
- [Retrieve - 检索知识库](../../raw/_short/api-bailian-2023-12-29-retrieve-c8e6b8d718a30a84.md)
- [SubmitIndexAddDocumentsJob - 提交知识库文件追加任务](../../raw/_short/api-bailian-2023-12-29-submitindexadddocumentsjo-ec4f5cf285e2c447.md)
- [ListIndexFileDetails - 查询知识库文件详情](../../raw/_short/api-bailian-2023-12-29-listindexfiledetails-0e2036d0ef0d8fe8.md)
- [ListIndexDocuments - 查询知识库文件列表](../../raw/_short/api-bailian-2023-12-29-listindexdocuments-9f0db0388c421903.md)
- [DeleteIndexDocument - 删除知识库下的文件](../../raw/_short/api-bailian-2023-12-29-deleteindexdocument-0792a83f5a741348.md)
- [UpdateIndex - 更新知识库](../../raw/_short/api-bailian-2023-12-29-updateindex-551997e1d335e340.md)
- [ListIndices - 查询知识库列表](../../raw/_short/api-bailian-2023-12-29-listindices-c555173be752eaaf.md)
- [DeleteIndex - 删除知识库](../../raw/_short/api-bailian-2023-12-29-deleteindex-500502bd6df1c49c.md)
- [ListChunks - 查询索引下的分片列表](../../raw/_short/api-bailian-2023-12-29-listchunks-30a6c87b93a583c6.md)
- [AddChunk - 新增切片](../../raw/_short/api-bailian-2023-12-29-addchunk-1607bcddf6713fd9.md)
- [GetIndexMonitor - 获取知识库监控数据](../../raw/_short/api-bailian-2023-12-29-getindexmonitor-3a609181d5c9c034.md)
- [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)
- [UpdateChunk - 修改切片](../../raw/_short/api-bailian-2023-12-29-updatechunk-589b46fcc24261f8.md)
- [DeleteChunk - 删除切片](../../raw/_short/api-bailian-2023-12-29-deletechunk-d249422088735d90.md)
- [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)


