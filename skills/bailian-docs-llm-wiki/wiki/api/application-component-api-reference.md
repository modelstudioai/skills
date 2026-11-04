# application component api reference

本 API 参考文档面向开发者，系统性地描述了百炼平台 Application Component（应用组件）层提供的核心 OpenAPI 能力，覆盖数据连接（原应用数据）、知识库两大功能模块。所有接口均基于 `bailian/2023-12-29` 版本，采用 ROA 签名机制，支持多语言 SDK 封装调用。开发者需通过 RAM 用户最小权限原则进行授权，并在指定[业务空间（Workspace）](../concepts/workspace.md)上下文中使用。

## 支持的模型/功能

Application Component API 主要提供两类核心能力：

- **数据连接（原应用数据）**：用于管理非结构化文件与结构化表格数据。包括类目（Category）的增删查、文件（File）的上传（通过租约）、批量导入（OSS）、元信息查询（DescribeFile）、标签管理（UpdateFileTag / BatchUpdateFileTag）及解析配置（GetParseSettings / ChangeParseSetting）。该模块不支持通过 API 新增或删除数据表（即 `AddTable` 和 `DeleteTable` 接口虽存在，但文档明确指出“不支持通过 API 新增数据表” [AddCategory](../../raw/_short/api-bailian-2023-12-29-addcategory-e2fe0e0435ed504e.md)），相关操作需通过控制台完成。
- **知识库（Knowledge Base）**：用于构建、维护和检索私有知识索引。涵盖知识库全生命周期管理（CreateIndex / SubmitIndexJob / UpdateIndex / DeleteIndex）、文件级操作（SubmitIndexAddDocumentsJob / ListIndexDocuments / DeleteIndexDocument）、细粒度切片（Chunk）管理（AddChunk / UpdateChunk / DeleteChunk / ListChunks）以及在线检索（Retrieve）。值得注意的是，`Retrieve` 接口存在两种调用路径：OpenAPI 形式（需 AccessKey）与 Spring AI Alibaba 框架形式（需 API Key），二者协议与鉴权方式不同，详见其接口说明 [Retrieve](../../raw/_short/api-bailian-2023-12-29-retrieve-c8e6b8d718a30a84.md)。

> **注意**：文档 42（版本说明）指出 `CreateIndex` 和 `Retrieve` 接口在 2025-12-03 和 2024-07-23 发生了请求参数变更，但原始文档中未提供具体变更细节。开发者应以最新版 OpenAPI Explorer 或 SDK 文档为准，避免因参数过时导致调用失败。

## 关键参数

所有 API 均要求在请求路径中指定 `WorkspaceId`（业务空间 ID），这是资源隔离与权限控制的核心维度。关键参数按功能域归纳如下：

- **数据连接通用参数**：
  - `CategoryId`：类目 ID，由 `AddCategory` 返回，用于 `ListFile`、`ApplyFileUploadLease` 等接口。
  - `FileId`：文件 ID，由 `AddFile` 返回，用于 `DescribeFile`、`DeleteFile`、`UpdateFileTag` 等接口。
  - `ConnectorId`：连接器 ID，用于 `AddCategory`、`AddConnector` 等接口。
- **知识库通用参数**：
  - `IndexId`：知识库 ID，由 `CreateIndex` 返回，是 `SubmitIndexJob`、`Retrieve`、`DeleteIndexDocument` 等绝大多数知识库接口的必需参数。
  - `JobId`：任务 ID，由 `SubmitIndexJob` 或 `SubmitIndexAddDocumentsJob` 返回，用于 `GetIndexJobStatus` 查询状态。
- **分页与过滤参数**：
  - `MaxResults` / `PageSize` / `PageNumber`：用于 `ListCategory`、`ListFile`、`ListIndices` 等列表接口，控制返回数量与页码。
  - `NextToken`：用于 `ListCategory`、`ListFile` 的游标分页。
  - `DocumentStatus` / `DocumentName`：用于 `ListIndexDocuments`、`ListIndexFileDetails` 过滤文件状态与名称。

## 使用方式

1. **环境准备**：首先获取阿里云账号或 RAM 用户的 AccessKey（推荐使用 RAM 子账号并授予最小权限策略 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess`），并确定目标地域的接入点（如 `bailian.cn-beijing.aliyuncs.com`）[服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)。
2. **调用流程（以知识库为例）**：
   - 创建知识库：调用 `CreateIndex` 初始化，再调用 `SubmitIndexJob` 提交创建任务。
   - 追加文件：先调用 `ApplyFileUploadLease` 获取租约，再调用 `AddFile` 上传文件，最后调用 `SubmitIndexAddDocumentsJob` 将文件加入知识库索引。
   - 检索知识：直接调用 `Retrieve` 接口，传入 `Query` 文本即可。
3. **调试与开发**：强烈推荐使用 [OpenAPI Explorer](https://api.aliyun.com/api/bailian/2023-12-29) 进行在线调试，或集成官方 SDK（如 Java、Python、TypeScript 等），SDK 已封装签名逻辑，可极大降低接入成本 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)。

## 限制和注意事项

- **限流策略**：各接口均有严格 QPS 限制，常见值为 5 次/秒（如 `AddCategory`, `ListCategory`）或 10 次/秒（如 `AddFile`, `Retrieve`）。超出后将返回限流错误，需实现重试逻辑。
- **幂等性**：大部分查询类（`List*`, `Describe*`, `Get*`）和部分更新类（`Update*`, `Delete*`）接口声明为幂等；而创建类（`Add*`, `Create*`, `Submit*`）接口通常不具备幂等性，重复调用可能导致资源冗余。
- **安全与权限**：必须遵循最小权限原则。RAM 策略中的 `Action` 字段需精确匹配（如 `sfm:AddCategory`），且 `Resource` 字段当前均为 `*`（全部资源），不支持更细粒度的资源级授权 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)。
- **关键约束**：
  - `AddCategory`：每个业务空间最多创建 500 个类目。
  - `AddFile`：上传前必须先调用 `ApplyFileUploadLease` 获取有效租约。
  - `DeleteIndexDocument`：仅能删除状态为 `INSERT_ERROR` 或 `FINISH` 的文件，且操作不可逆。
  - `ListChunks`：`Fields` 参数用于过滤 Metadata 中的非私有字段（不以 `_` 开头），若需返回所有字段，应保持 `Fields` 为空数组。

## 来源文档

- [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)
- [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)
- [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)
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
- [BatchUpdateFileTag](../../raw/_short/api-bailian-2023-12-29-batchupdatefiletag-34a8f009de66cb8b.md)
- [DeleteFile](../../raw/_short/api-bailian-2023-12-29-deletefile-7e0409a458195fe2.md)
- [DeleteFiles](../../raw/_short/api-bailian-2023-12-29-deletefiles-96ef0815114e4e37.md)
- [GetParseSettings - 获取类目解析设置](../../raw/_short/api-bailian-2023-12-29-getparsesettings-522514560c54f49f.md)
- [GetAvailableParserTypes - 获取文件支持的解析器类型](../../raw/_short/api-bailian-2023-12-29-getavailableparsertypes-09561c4e0fb505d5.md)
- [AddTable](../../raw/_short/api-bailian-2023-12-29-addtable-6726351659db288d.md)
- [ChangeParseSetting](../../raw/_short/api-bailian-2023-12-29-changeparsesetting-59a7c69675f499ad.md)
- [AddConnector](../../raw/_short/api-bailian-2023-12-29-addconnector-7a3c9650409710fe.md)
- [UpdateTableFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-updatetablefromauthorized-d7436828bcf51602.md)
- [GetConnector](../../raw/_short/api-bailian-2023-12-29-getconnector-cb2e485a0efd52f7.md)
- [UpdateConnector](../../raw/_short/api-bailian-2023-12-29-updateconnector-6a24905a7d201597.md)
- [知识库](../../raw/_short/api-bailian-2023-12-29-dir-knowledge-base-f6f202ad9694348f.md)
- [CreateIndex - 创建知识库](../../raw/_short/api-bailian-2023-12-29-createindex-8bc613c75f8af371.md)
- [GetIndexJobStatus - 查询知识库创建或追加任务状态](../../raw/_short/api-bailian-2023-12-29-getindexjobstatus-1e88b6ccfffe0fe4.md)
- [SubmitIndexJob - 提交知识库创建任务](../../raw/_short/api-bailian-2023-12-29-submitindexjob-63b38294171880d4.md)
- [SubmitIndexAddDocumentsJob - 提交知识库文件追加任务](../../raw/_short/api-bailian-2023-12-29-submitindexadddocumentsjo-ec4f5cf285e2c447.md)
- [ListIndexFileDetails - 查询知识库文件详情](../../raw/_short/api-bailian-2023-12-29-listindexfiledetails-0e2036d0ef0d8fe8.md)
- [UpdateIndex - 更新知识库](../../raw/_short/api-bailian-2023-12-29-updateindex-551997e1d335e340.md)
- [DeleteIndexDocument - 删除知识库下的文件](../../raw/_short/api-bailian-2023-12-29-deleteindexdocument-0792a83f5a741348.md)
- [ListIndices - 查询知识库列表](../../raw/_short/api-bailian-2023-12-29-listindices-c555173be752eaaf.md)
- [DeleteIndex - 删除知识库](../../raw/_short/api-bailian-2023-12-29-deleteindex-500502bd6df1c49c.md)
- [ListChunks - 查询索引下的分片列表](../../raw/_short/api-bailian-2023-12-29-listchunks-30a6c87b93a583c6.md)
- [Retrieve - 检索知识库](../../raw/_short/api-bailian-2023-12-29-retrieve-c8e6b8d718a30a84.md)
- [ListIndexDocuments - 查询知识库文件列表](../../raw/_short/api-bailian-2023-12-29-listindexdocuments-9f0db0388c421903.md)
- [UpdateChunk - 修改切片](../../raw/_short/api-bailian-2023-12-29-updatechunk-589b46fcc24261f8.md)
- [DeleteChunk - 删除切片](../../raw/_short/api-bailian-2023-12-29-deletechunk-d249422088735d90.md)
- [GetIndexMonitor - 获取知识库监控数据](../../raw/_short/api-bailian-2023-12-29-getindexmonitor-3a609181d5c9c034.md)
- [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)
- [AddChunk - 新增切片](../../raw/_short/api-bailian-2023-12-29-addchunk-1607bcddf6713fd9.md)


