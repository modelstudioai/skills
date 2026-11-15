# application component api reference

本 API 参考文档面向开发者，提供百炼平台应用组件（Application Component）的核心 OpenAPI 接口规范，涵盖数据连接（原应用数据）、知识库两大核心能力模块。所有接口均基于 `bailian/2023-12-29` 版本，采用 ROA 签名机制，支持通过官方 SDK 或自签名方式调用。开发者需预先配置 RAM 用户权限与业务空间访问授权。

## 支持的模型/功能

本组件不直接提供大语言模型推理能力，而是聚焦于**结构化与非结构化数据管理**及**知识库全生命周期操作**两大核心功能域：

- **数据连接（原应用数据）**：提供类目（Category）管理、文件（File）上传/查询/标签更新/删除、OSS 批量导入、解析器配置等能力，支撑知识库的数据源准备。支持 UNSTRUCTURED（文档类目）和 SESSION_FILE（会话文件）两类类目类型，但明确不支持通过 API 新增或删除数据表（表格），该操作仅限控制台完成 [AddCategory](../../raw/_short/api-bailian-2023-12-29-addcategory-e2fe0e0435ed504e.md)。
- **知识库（Knowledge Base）**：覆盖知识库创建（`CreateIndex`）、提交构建（`SubmitIndexJob`）、追加文件（`SubmitIndexAddDocumentsJob`）、检索（`Retrieve`）、文件与切片（Chunk）管理、监控（`GetIndexMonitor`）等完整链路。支持 `unstructured`（文档/音视频）和 `structured`（数据查询/图片问答）两类知识库，但部分接口存在类型限制，例如 `UpdateChunk` 仅支持 `unstructured` 类型 [UpdateChunk](../../raw/_short/api-bailian-2023-12-29-updatechunk-589b46fcc24261f8.md)。

> **注意**：文档 43 (`AddChunk`) 声明支持 `document`/`table`/`image` 三类知识库，但文档 39 (`UpdateChunk`) 和文档 40 (`DeleteChunk`) 明确限定仅支持 `document`（即 `unstructured`）类型。此为功能范围不一致，实际开发中应以 `UpdateChunk` 和 `DeleteChunk` 的约束为准，`AddChunk` 对 `table`/`image` 的支持可能存在未公开的前置条件或已过时。

## 关键参数

- **`WorkspaceId`**：所有接口的必需路径参数，标识业务空间 ID。必须通过百炼控制台获取，当前版本无 API 可枚举业务空间 [ListIndices](../../raw/_short/api-bailian-2023-12-29-listindices-c555173be752eaaf.md)。
- **`CategoryId` / `FileId` / `IndexId` / `ChunkId`**：资源标识符，均为字符串类型，由上游接口（如 `AddCategory`, `AddFile`, `CreateIndex`, `ListChunks`）返回，不可自行构造。
- **`Parser`**：文件解析器类型，关键请求参数，用于 `AddFile` 和 `ApplyFileUploadLease`。有效值包括 `DOCMIND`, `DOCMIND_DIGITAL`, `DOCMIND_LLM_VERSION`, `DASH_QWEN_VL_PARSER`, `AUTO_SELECT` 等，具体支持列表需结合 `GetAvailableParserTypes` 接口动态查询。
- **分页参数**：`List*` 类接口普遍支持 `NextToken`（游标）或 `PageNumber`/`PageSize`（页码）进行分页，最大 `PageSize` 通常为 200。

## 使用方式

1. **环境准备**：
   - 获取阿里云 AccessKey（推荐使用 RAM 子账号，遵循最小权限原则）。
   - 在 RAM 控制台为子账号授予 `AliyunBailianDataFullAccess`（读写）或 `AliyunBailianDataReadOnlyAccess`（只读）策略，并确保其已加入目标业务空间。
   - 配置服务接入点（Endpoint），例如华北2（北京）地域为 `bailian.cn-beijing.aliyuncs.com` [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)。

2. **典型工作流（以构建知识库为例）**：
   - 调用 `AddCategory` 创建类目 → `ApplyFileUploadLease` 申请租约 → `AddFile` 上传文件。
   - 调用 `CreateIndex` 初始化知识库 → `SubmitIndexJob` 提交构建任务 → 轮询 `GetIndexJobStatus` 查询状态。
   - （可选）调用 `Retrieve` 进行检索，或 `ListIndexDocuments`/`ListChunks` 查看内容。

3. **SDK 优先**：强烈建议使用官方维护的 [阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)，它已封装签名逻辑并提供各语言示例，可显著降低接入复杂度。

## 限制和注意事项

- **限流策略**：所有接口均有严格 QPS 限制，常见值为 5 次/秒（如 `AddCategory`, `ListCategory`）或 10 次/秒（如 `AddFile`, `Retrieve`）。超出后将返回限流错误，需实现退避重试逻辑。
- **幂等性**：多数查询类（`List*`, `Describe*`, `Get*`）和部分操作类（`Delete*`, `Update*`）接口声明具备幂等性；而 `Add*`, `Apply*`, `Submit*` 等创建类接口通常不具备幂等性，重复调用可能导致资源冗余。
- **安全与权限**：`sfm:*` 权限点是 RAM 授权的核心，每个 API 对应唯一的 `Action`（如 `sfm:AddFile`），必须在策略中显式声明。`ConnectorId` 等敏感参数需从控制台获取，不可猜测。
- **功能边界**：API 不支持数据表的增删改查（CRUD），该能力仅存在于控制台；`DeleteIndexDocument` 删除的是知识库索引中的文件，不影响原始应用数据中的文件；`DeleteIndex` 删除知识库前需先解除其与智能体应用的关联，此步骤目前仅支持控制台操作。

## 来源文档

- [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)
- [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)
- [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)
- [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md)
- [AddCategory](../../raw/_short/api-bailian-2023-12-29-addcategory-e2fe0e0435ed504e.md)
- [数据连接（原应用数据）](../../raw/_short/api-bailian-2023-12-29-dir-data-connection-origi-a1f7f2601bd6f7cf.md)
- [ListCategory](../../raw/_short/api-bailian-2023-12-29-listcategory-2521532ef3e828b3.md)
- [DeleteCategory - 删除类目](../../raw/_short/api-bailian-2023-12-29-deletecategory-9838436bd2db3113.md)
- [AddFile](../../raw/_short/api-bailian-2023-12-29-addfile-8c254b3500bc50bc.md)
- [ApplyFileUploadLease](../../raw/_short/api-bailian-2023-12-29-applyfileuploadlease-39e8ca15e0e9561a.md)
- [AddFilesFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-addfilesfromauthorizedoss-879556d685a301b3.md)
- [ListFile](../../raw/_short/api-bailian-2023-12-29-listfile-360209e3a2479f14.md)
- [DescribeFile](../../raw/_short/api-bailian-2023-12-29-describefile-020886c28a208bf2.md)
- [BatchUpdateFileTag](../../raw/_short/api-bailian-2023-12-29-batchupdatefiletag-34a8f009de66cb8b.md)
- [UpdateFileTag](../../raw/_short/api-bailian-2023-12-29-updatefiletag-f84d2af6a45d6553.md)
- [DeleteFile](../../raw/_short/api-bailian-2023-12-29-deletefile-7e0409a458195fe2.md)
- [DeleteFiles](../../raw/_short/api-bailian-2023-12-29-deletefiles-96ef0815114e4e37.md)
- [GetParseSettings - 获取类目解析设置](../../raw/_short/api-bailian-2023-12-29-getparsesettings-522514560c54f49f.md)
- [GetAvailableParserTypes - 获取文件支持的解析器类型](../../raw/_short/api-bailian-2023-12-29-getavailableparsertypes-09561c4e0fb505d5.md)
- [UpdateTableFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-updatetablefromauthorized-d7436828bcf51602.md)
- [AddTable](../../raw/_short/api-bailian-2023-12-29-addtable-6726351659db288d.md)
- [ChangeParseSetting](../../raw/_short/api-bailian-2023-12-29-changeparsesetting-59a7c69675f499ad.md)
- [AddConnector](../../raw/_short/api-bailian-2023-12-29-addconnector-7a3c9650409710fe.md)
- [GetConnector](../../raw/_short/api-bailian-2023-12-29-getconnector-cb2e485a0efd52f7.md)
- [知识库](../../raw/_short/api-bailian-2023-12-29-dir-knowledge-base-f6f202ad9694348f.md)
- [UpdateConnector](../../raw/_short/api-bailian-2023-12-29-updateconnector-6a24905a7d201597.md)
- [CreateIndex - 创建知识库](../../raw/_short/api-bailian-2023-12-29-createindex-8bc613c75f8af371.md)
- [GetIndexJobStatus - 查询知识库创建或追加任务状态](../../raw/_short/api-bailian-2023-12-29-getindexjobstatus-1e88b6ccfffe0fe4.md)
- [SubmitIndexAddDocumentsJob - 提交知识库文件追加任务](../../raw/_short/api-bailian-2023-12-29-submitindexadddocumentsjo-ec4f5cf285e2c447.md)
- [SubmitIndexJob - 提交知识库创建任务](../../raw/_short/api-bailian-2023-12-29-submitindexjob-63b38294171880d4.md)
- [ListIndexDocuments - 查询知识库文件列表](../../raw/_short/api-bailian-2023-12-29-listindexdocuments-9f0db0388c421903.md)
- [ListIndexFileDetails - 查询知识库文件详情](../../raw/_short/api-bailian-2023-12-29-listindexfiledetails-0e2036d0ef0d8fe8.md)
- [Retrieve - 检索知识库](../../raw/_short/api-bailian-2023-12-29-retrieve-c8e6b8d718a30a84.md)
- [DeleteIndexDocument - 删除知识库下的文件](../../raw/_short/api-bailian-2023-12-29-deleteindexdocument-0792a83f5a741348.md)
- [UpdateIndex - 更新知识库](../../raw/_short/api-bailian-2023-12-29-updateindex-551997e1d335e340.md)
- [ListIndices - 查询知识库列表](../../raw/_short/api-bailian-2023-12-29-listindices-c555173be752eaaf.md)
- [DeleteIndex - 删除知识库](../../raw/_short/api-bailian-2023-12-29-deleteindex-500502bd6df1c49c.md)
- [ListChunks - 查询索引下的分片列表](../../raw/_short/api-bailian-2023-12-29-listchunks-30a6c87b93a583c6.md)
- [UpdateChunk - 修改切片](../../raw/_short/api-bailian-2023-12-29-updatechunk-589b46fcc24261f8.md)
- [DeleteChunk - 删除切片](../../raw/_short/api-bailian-2023-12-29-deletechunk-d249422088735d90.md)
- [GetIndexMonitor - 获取知识库监控数据](../../raw/_short/api-bailian-2023-12-29-getindexmonitor-3a609181d5c9c034.md)
- [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)
- [AddChunk - 新增切片](../../raw/_short/api-bailian-2023-12-29-addchunk-1607bcddf6713fd9.md)


